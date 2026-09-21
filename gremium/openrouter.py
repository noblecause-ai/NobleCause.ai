"""One explicit OpenRouter HTTP transport. No retry, routing fallback or SDK.

The active roster is still config.json. Candidate configuration is not activation.
Raw bytes precede interpretation. Any unresolved charge stops the entire run.
"""
import json
import os
import time
from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request

MODELS = {
    'anthropic': 'anthropic/claude-fable-5.1',
    'openai': 'openai/gpt-6-astra',
    'spacexai': 'x-ai/grok-4.6',
    'moonshotai': 'moonshotai/kimi-k3',
    'z-ai': 'z-ai/glm-5.3',
}
KEYS = {'anthropic': 'ANTHROPIC_API_KEY', 'openai': 'OPENAI_API_KEY', 'google': 'GEMINI_API_KEY'}
BASE = 'https://openrouter.ai/api/v1'


class OpenRouterError(RuntimeError):
    def __init__(self, message, outcome='invalid', usage=None):
        super().__init__(message)
        self.outcome = outcome
        self.usage = usage


def amount(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise OpenRouterError('Missing or invalid monetary value')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise OpenRouterError('Invalid monetary value') from exc
    if not result.is_finite() or result < 0:
        raise OpenRouterError('Non-finite or negative monetary value')
    return result


def integer(value):
    if type(value) is not int or value < 0:
        raise OpenRouterError('Missing or invalid token usage')
    return value


def decode(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise OpenRouterError('Duplicate response field')
            result[key] = value
        return result
    def invalid(_):
        raise OpenRouterError('Non-finite JSON')
    try:
        result = json.loads(data, object_pairs_hook=pairs, parse_constant=invalid, parse_float=Decimal)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise OpenRouterError('Malformed JSON response') from exc
    if not isinstance(result, dict):
        raise OpenRouterError('Response must be an object')
    return result


def http(method, path, payload=None):
    """One attempt only, including HTTP errors. No redirect carrying credentials."""
    from urllib.request import HTTPRedirectHandler, build_opener
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            raise OpenRouterError('Redirect refused; billing status unresolved', 'unavailable')
    key = os.environ.get('OPENROUTER_API_KEY', '')
    if not key or key != key.strip():
        raise OpenRouterError('OPENROUTER_API_KEY missing or malformed')
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    req = Request(BASE + path, data=body, method=method, headers={
        'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
    })
    try:
        with build_opener(NoRedirect).open(req, timeout=600 if method == 'POST' else 60) as response:
            return response.read()
    except HTTPError as exc:
        # Preserve provider error bodies too, without logging request headers.
        return exc.read()


def contract(spec):
    if spec.get('transport') != 'openrouter_api' or spec.get('model') != MODELS.get(spec.get('family')):
        raise OpenRouterError('Unapproved model or transport')
    cfg = spec.get('openrouter') or {}
    required = {'endpoint', 'provider_name', 'quantization', 'reasoning_effort',
                'max_output_tokens', 'max_price', 'context_length', 'token_parameter'}
    if set(cfg) != required:
        raise OpenRouterError('Incomplete or unexpected OpenRouter configuration')
    if not all(isinstance(cfg[k], str) and cfg[k].strip() == cfg[k] and cfg[k]
               for k in ['endpoint', 'provider_name', 'quantization', 'reasoning_effort']):
        raise OpenRouterError('Invalid endpoint contract')
    if cfg['token_parameter'] not in ('max_tokens', 'max_completion_tokens'):
        raise OpenRouterError('Invalid output parameter')
    if not integer(cfg['context_length']) or not integer(cfg['max_output_tokens']):
        raise OpenRouterError('Empty context/output limit')
    if set(cfg['max_price']) != {'prompt', 'completion'}:
        raise OpenRouterError('Explicit input and output price caps required')
    for v in cfg['max_price'].values():
        if not amount(v):
            raise OpenRouterError('Positive price caps required')
    return cfg


def validate_roster(models):
    transports = {m.get('transport', 'api') for m in models}
    if transports == {'api'}:
        if any(m.get('family') not in KEYS for m in models):
            raise OpenRouterError('Unsupported direct provider')
        return False
    if transports != {'openrouter_api'} or len(models) != 5 or {m.get('family') for m in models} != set(MODELS):
        raise OpenRouterError('Council requires all five fixed OpenRouter seats; no mixed transport')
    for spec in models:
        contract(spec)
    return True


def required_keys(specs):
    result = set()
    for spec in specs:
        if spec.get('transport', 'api') == 'openrouter_api':
            contract(spec)
            result.add('OPENROUTER_API_KEY')
        elif spec.get('transport', 'api') == 'api' and spec.get('family') in KEYS:
            result.add(KEYS[spec['family']])
        else:
            raise OpenRouterError('Unsupported transport/provider')
    return sorted(result)


def structured_format(spec):
    """Optional per-call schema; never an instruction to rewrite a response."""
    fmt = spec.get('response_format')
    if fmt is None:
        return None
    import jsonschema
    if not isinstance(fmt, dict) or set(fmt) != {'type', 'json_schema'} or fmt['type'] != 'json_schema':
        raise OpenRouterError('Unsupported structured response format')
    rule = fmt['json_schema']
    if (not isinstance(rule, dict) or set(rule) != {'name', 'strict', 'schema'}
            or rule['strict'] is not True or not isinstance(rule['name'], str) or not rule['name'].strip()
            or not isinstance(rule['schema'], dict)):
        raise OpenRouterError('Invalid strict response schema contract')
    try:
        jsonschema.Draft202012Validator.check_schema(rule['schema'])
    except jsonschema.SchemaError:
        raise OpenRouterError('Invalid response JSON schema') from None
    return fmt


def endpoint_preflight(spec):
    cfg = contract(spec)
    model = spec['model']
    catalog = decode(http('GET', '/models'))['data']
    candidates = [m for m in catalog if m.get('id') == model]
    if len(candidates) != 1 or candidates[0].get('alias_target'):
        raise OpenRouterError('Fixed model missing or alias')
    if cfg['reasoning_effort'] not in (candidates[0].get('reasoning') or {}).get('supported_efforts', []):
        raise OpenRouterError('Reasoning effort not supported')
    eps = decode(http('GET', '/models/' + model + '/endpoints'))['data']
    if eps.get('id') != model:
        raise OpenRouterError('Endpoint model mismatch')
    # Base slugs include variants. Never mistake a provider name for an exact pin.
    matching = [e for e in eps['endpoints'] if e.get('tag') == cfg['endpoint'] or
                ('/' not in cfg['endpoint'] and e.get('tag', '').startswith(cfg['endpoint'] + '/'))]
    if len(matching) != 1:
        raise OpenRouterError('Endpoint pin ambiguous or missing')
    ep = matching[0]
    if ep.get('model_id') != model or ep.get('provider_name') != cfg['provider_name']:
        raise OpenRouterError('Endpoint identity mismatch')
    if ep.get('status') != 0 or ep.get('quantization') != cfg['quantization']:
        raise OpenRouterError('Endpoint unavailable or precision drift')
    if ep.get('context_length') != cfg['context_length']:
        raise OpenRouterError('Context contract drift')
    supported = ep.get('supported_parameters') or []
    if any(p not in supported for p in ('reasoning', cfg['token_parameter'])):
        raise OpenRouterError('Endpoint does not support required parameters')
    if structured_format(spec) and not {'response_format', 'structured_outputs'} <= set(supported):
        raise OpenRouterError('Pinned endpoint does not support strict structured output')
    if integer(ep.get('max_completion_tokens')) < cfg['max_output_tokens']:
        raise OpenRouterError('Endpoint output limit too small')
    prices = ep.get('pricing') or {}
    for p in ('prompt', 'completion'):
        if amount(prices.get(p)) * 1_000_000 > amount(cfg['max_price'][p]):
            raise OpenRouterError('Endpoint price exceeds contract')
    # No additional per-call/tool/media charge may escape our bound.
    if any(amount(prices[k]) for k in ('request', 'image', 'audio') if k in prices):
        raise OpenRouterError('Unsupported additional charge')
    return {**ep, 'canonical_model': candidates[0].get('canonical_slug') or model}


def preflight(specs):
    active = [s for s in specs if s.get('transport') == 'openrouter_api']
    if not active:
        return
    key = decode(http('GET', '/key'))['data']
    credit = decode(http('GET', '/credits'))['data']
    if amount(credit['total_credits']) <= amount(credit['total_usage']):
        raise OpenRouterError('No account credit')
    if key.get('limit') is not None and amount(key.get('limit_remaining')) <= 0:
        raise OpenRouterError('No key credit remaining')
    for spec in active:
        endpoint_preflight(spec)


def request_for(spec, system, user, max_tokens):
    cfg = contract(spec)
    limit = min(integer(max_tokens), cfg['max_output_tokens'])
    if not limit:
        raise OpenRouterError('Output limit must be positive')
    request = {
        'model': spec['model'],
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        'stream': False, cfg['token_parameter']: limit,
        'reasoning': {'effort': cfg['reasoning_effort']},
        'usage': {'include': True},
        'provider': {'only': [cfg['endpoint']], 'order': [cfg['endpoint']],
                     'allow_fallbacks': False, 'require_parameters': True,
                     'data_collection': 'deny', 'max_price': cfg['max_price']},
    }

    if cfg['quantization'] != 'unknown':
        request['provider']['quantizations'] = [cfg['quantization']]
    fmt = structured_format(spec)
    if fmt is not None:
        request['response_format'] = json.loads(json.dumps(fmt))
    return request


def worst_case_usd(spec, max_tokens, input_bound=None):
    cfg = contract(spec)
    # Reserve the FULL advertised context: no guessed local tokenizer or char/token
    # estimate can silently under-reserve. This is deliberately conservative.
    # max_price rejects expensive long-context tiers instead of widening the cap.
    tokens = cfg['context_length'] if input_bound is None else integer(input_bound)
    if tokens > cfg['context_length']:
        raise OpenRouterError('Input bound exceeds context contract')
    return (Decimal(tokens) * amount(cfg['max_price']['prompt']) +
            Decimal(min(max_tokens, cfg['max_output_tokens'])) * amount(cfg['max_price']['completion'])) / 1_000_000


def reserve(spec, max_tokens, spent_eur, cap_eur, fx, input_bound=None):
    if amount(fx) <= 0:
        raise OpenRouterError('Positive exchange rate required')
    required = worst_case_usd(spec, max_tokens, input_bound) * amount(fx)
    if amount(spent_eur) + required > amount(cap_eur):
        raise OpenRouterError('Budget insufficient for worst-case next call; no request sent')


def validate_response(spec, response, generation, canonical_model=None):
    cfg = contract(spec)
    if not response.get('error') and (generation.get('error') or {}).get('code') == 404:
        raise OpenRouterError('Generation receipt delayed or unavailable; charge unresolved', 'unavailable')
    if response.get('error') or generation.get('error'):
        raise OpenRouterError('Provider error; charge unresolved', 'unavailable')
    data = generation.get('data') or {}
    gid = response.get('id')
    if not isinstance(gid, str) or not gid.startswith('gen-') or data.get('id') != gid:
        raise OpenRouterError('Missing or mismatched generation ID')
    if response.get('model') != spec['model'] or data.get('model') not in {spec['model'], canonical_model or spec['model']}:
        raise OpenRouterError('Requested/reported model mismatch')
    if response.get('provider') != cfg['provider_name'] or data.get('provider_name') != cfg['provider_name']:
        raise OpenRouterError('Missing or mismatched upstream')
    choices = response.get('choices')
    if not isinstance(choices, list) or len(choices) != 1:
        raise OpenRouterError('Exactly one choice required')
    choice = choices[0]
    stop, native = choice.get('finish_reason'), choice.get('native_finish_reason')
    if not isinstance(native, str) or not native or native != data.get('native_finish_reason'):
        raise OpenRouterError('Missing or mismatched native stop')
    if stop != data.get('finish_reason') or stop not in ('stop', 'content_filter', 'length', 'tool_calls', 'error'):
        raise OpenRouterError('Missing or mismatched normalized stop')
    usage = response.get('usage') or {}
    for key, other in [('prompt_tokens', 'native_tokens_prompt'), ('completion_tokens', 'native_tokens_completion')]:
        if integer(usage.get(key)) != integer(data.get(other)):
            raise OpenRouterError('Response/generation usage mismatch')
    if integer(usage.get('total_tokens')) != usage['prompt_tokens'] + usage['completion_tokens']:
        raise OpenRouterError('Total usage mismatch')
    for parent, field, other in [('completion_tokens_details', 'reasoning_tokens', 'native_tokens_reasoning'),
                                 ('prompt_tokens_details', 'cached_tokens', 'native_tokens_cached')]:
        detail = (usage.get(parent) or {}).get(field)
        if detail is not None or data.get(other) is not None:
            if integer(detail) != integer(data.get(other)):
                raise OpenRouterError('Detailed usage mismatch')
    response_cost = amount(usage.get('cost'))
    cost = amount(data.get('total_cost'))
    if 'usage' in data and amount(data['usage']) != cost:
        raise OpenRouterError('Generation credit usage mismatch')
    if response_cost != cost:
        # GLM receipts have used eight or nine fractional digits while the
        # completion used ten. Respect any finer precision in the receipt;
        # never round more coarsely than eight digits. Receipts have matched
        # both nearest rounding and decimal truncation. Book the actual bill
        # and retain the unmodified completion amount in provenance.
        quantum = Decimal(1).scaleb(min(-8, cost.as_tuple().exponent))
        represented = {response_cost.quantize(quantum, rounding=mode) for mode in (ROUND_HALF_UP, ROUND_DOWN)}
        if 'usage' not in data or cost not in represented:
            raise OpenRouterError('Response/generation cost mismatch; not billed')
    if data.get('cancelled') is not False or data.get('is_byok') is not False:
        raise OpenRouterError('Cancelled or unverified billing source')
    if any(data.get(k) not in (None, 0) for k in ('num_search_results', 'num_fetches', 'num_media_prompt', 'num_media_completion')):
        raise OpenRouterError('Unexpected tools/media')
    for obj in (response, data):
        if 'quantization' in obj and obj['quantization'] != cfg['quantization']:
            raise OpenRouterError('Reported precision mismatch')
        if 'endpoint' in obj and obj['endpoint'] != cfg['endpoint']:
            raise OpenRouterError('Reported endpoint mismatch')
    provenance = {
        'transport': 'openrouter_api', 'identity_source': 'api', 'gateway': 'openrouter',
        'requested_model': spec['model'], 'reported_model': response['model'],
        'generation_model': data['model'],
        'upstream_provider': response['provider'], 'endpoint': cfg['endpoint'],
        'quantization': cfg['quantization'], 'generation_id': gid,
        'finish_reason': stop, 'native_finish_reason': native,
        'usage': json.loads(json.dumps(usage, default=float)), 'cost': float(cost), 'cost_basis': 'billed',
    }
    confirmed = {'input_tokens': usage['prompt_tokens'], 'output_tokens': usage['completion_tokens'],
                 'billed_usd': str(cost), 'provenance': provenance}
    message = choice.get('message') or {}
    if choice.get('error') or message.get('tool_calls') or message.get('role') != 'assistant':
        raise OpenRouterError('Unexpected response/tool call', usage=confirmed)
    text = message.get('content')
    if native in ('refusal', 'content_filter'):
        raise OpenRouterError('Native refusal; raw response retained', 'refusal', usage=confirmed)
    if stop == 'length':
        raise OpenRouterError('Output token limit reached; incomplete response', usage=confirmed)
    if not isinstance(text, str) or not text.strip():
        raise OpenRouterError('No unambiguous response text', usage=confirmed)
    expected = {'end_turn'} if spec['family'] == 'anthropic' else ({'stop', 'completed'} if spec['family'] in ('openai', 'spacexai') else {'stop'})
    if stop != 'stop' or native not in expected or message.get('refusal'):
        raise OpenRouterError('Incomplete or unknown native completion', usage=confirmed)
    fmt = structured_format(spec)
    if fmt is not None:
        import jsonschema
        try:
            parsed = decode(text.encode())
            jsonschema.Draft202012Validator(fmt['json_schema']['schema']).validate(parsed)
        except (OpenRouterError, jsonschema.ValidationError):
            raise OpenRouterError('Structured response violates requested schema; no repair', usage=confirmed) from None
    return text, confirmed


def call(spec, system, user, max_tokens, raw_dir, tag, *, spent_eur, cap_eur, fx, input_bound=None, observe_costs=False):
    # Before request artefact creation: contract, budget and endpoint check.
    request = request_for(spec, system, user, max_tokens)
    if observe_costs:
        if input_bound is not None or amount(fx) <= 0:
            raise OpenRouterError('Kostenbeobachtung verlangt einen ausdrücklich unbegrenzten Input')
        if amount(spent_eur) >= amount(cap_eur):
            raise OpenRouterError('Abgerechnetes Testbudget erreicht; kein Folgeaufruf')
    else:
        reserve(spec, max_tokens, spent_eur, cap_eur, fx, input_bound)
    endpoint = endpoint_preflight(spec)
    stem = f'{tag}-{spec["family"]}'
    paths = {k: raw_dir / f'{stem}-{k}.json' for k in ('request', 'response', 'generation', 'endpoint', 'result')}
    if any(p.exists() for p in paths.values()):
        raise OpenRouterError('Existing call artifacts; repetition forbidden')
    def save(key, data):
        with paths[key].open('xb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        directory_fd = os.open(raw_dir, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    save('request', json.dumps(request, ensure_ascii=False).encode())
    save('endpoint', json.dumps(endpoint, ensure_ascii=False, default=float).encode())
    try:
        raw = http('POST', '/chat/completions', request)
        save('response', raw)
        response = decode(raw)
        gid = response.get('id')
        if response.get('error') or not isinstance(gid, str) or not gid.startswith('gen-'):
            raise OpenRouterError('No usable generation ID; charge unresolved', 'unavailable')
        # Billing metadata can lag a successful completion by over 30 seconds.
        # Only repeat the read; never repeat the paid inference.
        for attempt, delay in enumerate((0, 2, 8, 20, 30, 30, 30)):
            if delay:
                time.sleep(delay)
            generation_raw = http('GET', '/generation?id=' + quote(gid, safe=''))
            with (raw_dir / f'{stem}-generation-attempt-{attempt}.json').open('xb') as stream:
                stream.write(generation_raw)
            generation_status = decode(generation_raw)
            if isinstance(generation_status.get('data'), dict) or (generation_status.get('error') or {}).get('code') != 404:
                break
        save('generation', generation_raw)
        text, usage = validate_response(spec, response, decode(generation_raw), endpoint.get('canonical_model'))
        if (input_bound is not None and usage['input_tokens'] > input_bound) or (not observe_costs and usage['output_tokens'] > min(max_tokens, spec['openrouter']['max_output_tokens'])):
            raise OpenRouterError('Billed tokens exceeded proven bound; stop')
        if observe_costs and usage['output_tokens'] > min(max_tokens, spec['openrouter']['max_output_tokens']):
            usage['provenance']['output_limit_observation'] = {'requested': max_tokens, 'billed': usage['output_tokens']}
        if not observe_costs and amount(usage['billed_usd']) > worst_case_usd(spec, max_tokens, input_bound):
            raise OpenRouterError('Billed cost exceeded reserved bound; stop')
        usage['provenance']['raw_artifact'] = 'raw/' + paths['response'].name
        usage['provenance']['generation_artifact'] = 'raw/' + paths['generation'].name
        save('result', json.dumps({'outcome': 'valid', **usage}, ensure_ascii=False, default=float).encode())
        return text, usage
    except Exception as exc:
        outcome = getattr(exc, 'outcome', 'unavailable')
        # Exception messages from HTTP libraries could contain secrets. Keep only
        # our controlled validation messages; bytes contain the actual evidence.
        message = str(exc) if isinstance(exc, OpenRouterError) else 'Transport/parse failure; billing unresolved'
        confirmed = getattr(exc, 'usage', None)
        if confirmed:
            confirmed['provenance']['raw_artifact'] = 'raw/' + paths['response'].name
            confirmed['provenance']['generation_artifact'] = 'raw/' + paths['generation'].name
        result = {'outcome': outcome, 'failure': message, 'retry_allowed': False}
        if confirmed:
            result['confirmed_usage'] = confirmed
        save('result', json.dumps(result, ensure_ascii=False, default=float).encode())
        raise OpenRouterError(message, outcome, usage=confirmed) from None
