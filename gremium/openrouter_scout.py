"""Thin native-search transport: immutable evidence, billed costs, explicit gaps.

No inference retries, fallback models or synthetic query logs. A configured,
non-resetting OpenRouter key limit is the server-side spending backstop;
native search counts/output limits are requests, not a per-call cost guarantee.
"""
import datetime
import json
import time
from urllib.parse import quote

from openrouter import OpenRouterError, amount, decode, http, integer

APPROVED = {
    'x-ai/grok-4.6': ('spacexai', 'xai/zdr', 'xAI', 'native', 'completed'),
    'perplexity/sonar-pro': ('perplexity', 'perplexity', 'Perplexity', 'intrinsic', 'stop'),
    'anthropic/claude-opus-5': ('anthropic', 'anthropic', 'Anthropic', 'native', 'end_turn'),
}
WART_MODEL = 'anthropic/claude-fable-5'
WART_ENDPOINT = ('anthropic', 'anthropic', 'Anthropic', 'none', 'end_turn')


def expected_endpoint(spec):
    if spec.get('role') == 'wart' and spec.get('model') == WART_MODEL:
        return WART_ENDPOINT
    return APPROVED.get(spec.get('model'))


class ScoutAccountingError(OpenRouterError):
    """Never swallowed by the multi-Scout partial-success path."""


def contract(spec):
    cfg = spec.get('openrouter') or {}
    expected = expected_endpoint(spec)
    if (not expected or spec.get('transport') != 'openrouter_api'
            or (spec.get('family'), cfg.get('endpoint'), cfg.get('provider_name'), cfg.get('search_engine')) != expected[:4]
            or cfg.get('allow_fallbacks') is not False):
        raise ValueError('Unapproved Scout model/provider/search configuration')
    if not integer(spec.get('max_output_tokens')) or (cfg.get('search_engine') != 'none' and not integer(spec.get('max_web_search_uses'))):
        raise ValueError('Positive Scout output/search limits required')
    for field in ('prompt', 'completion'):
        amount((cfg.get('max_price') or {}).get(field))
    amount(cfg.get('max_search_price_usd'))
    return cfg


def key_state():
    data = decode(http('GET', '/key')).get('data') or {}
    safe = {k: data.get(k) for k in ('limit', 'limit_reset', 'limit_remaining', 'usage')}
    if (safe['limit_reset'] is not None or amount(safe['limit']) <= 0
            or amount(safe['limit_remaining']) <= 0 or amount(safe['usage']) >= amount(safe['limit'])):
        raise ScoutAccountingError('A non-resetting, funded key limit is required; no call sent')
    return safe


def request_for(spec, system, user):
    cfg = contract(spec)
    request = {
        'model': spec['model'], 'stream': False, 'max_tokens': spec['max_output_tokens'],
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        'usage': {'include': True},
        'provider': {'only': [cfg['endpoint']], 'order': [cfg['endpoint']],
                     'allow_fallbacks': False, 'require_parameters': True,
                     'data_collection': 'deny', 'max_price': cfg['max_price']},
    }
    if cfg.get('reasoning_effort'):
        request['reasoning'] = {'effort': cfg['reasoning_effort']}
    if cfg['quantization'] != 'unknown':
        request['provider']['quantizations'] = [cfg['quantization']]
    if cfg['search_engine'] == 'intrinsic':
        request['web_search_options'] = {'search_context_size': cfg['search_context_size']}
    elif cfg['search_engine'] == 'native':
        n = spec['max_web_search_uses']
        request['tools'] = [{'type': 'openrouter:web_search', 'parameters': {
            'engine': 'native', 'max_uses': n, 'max_results': 5,
            'max_total_results': n * 5, 'max_characters': 2000,
        }}]
        request['max_tool_calls'] = n
    return request


def endpoint_check(spec, catalog, endpoints):
    cfg = contract(spec)
    models = [m for m in catalog['data'] if m.get('id') == spec['model']]
    matches = [e for e in endpoints['data']['endpoints'] if e.get('tag') == cfg['endpoint']]
    if len(models) != 1 or len(matches) != 1:
        raise ValueError('Scout model or pinned endpoint missing/ambiguous')
    model, ep = models[0], matches[0]
    if (model.get('alias_target') or ep.get('status') != 0 or ep.get('model_id') != spec['model']
            or ep.get('provider_name') != cfg['provider_name'] or ep.get('quantization') != cfg['quantization']):
        raise ValueError('Scout endpoint identity/availability changed')
    required = {'max_tokens'}
    if cfg['search_engine'] != 'none':
        required.add('web_search_options' if cfg['search_engine'] == 'intrinsic' else 'tools')
    if cfg.get('reasoning_effort'):
        required.add('reasoning')
        if cfg['reasoning_effort'] not in (model.get('reasoning') or {}).get('supported_efforts', []):
            raise ValueError('Scout reasoning setting unsupported')
    if not required <= set(ep.get('supported_parameters') or []) or integer(ep.get('max_completion_tokens')) < spec['max_output_tokens']:
        raise ValueError('Scout parameters/output limit unsupported')
    for field in ('prompt', 'completion'):
        if amount(ep['pricing'].get(field)) * 1_000_000 > amount(cfg['max_price'][field]):
            raise ValueError('Scout token price increased')
    if cfg['search_engine'] != 'none' and amount(ep['pricing'].get('web_search')) > amount(cfg['max_search_price_usd']):
        raise ValueError('Scout search price increased')
    return model


def assess(spec, response, generation, canonical_model):
    """Validate billing first; return honest observations, never inferred queries."""
    cfg = contract(spec)
    data = generation.get('data') or {}
    usage = response.get('usage') or {}
    if (response.get('error') or generation.get('error') or not str(response.get('id', '')).startswith('gen-')
            or data.get('id') != response.get('id') or data.get('cancelled') is not False or data.get('is_byok') is not False):
        raise ScoutAccountingError('Generation/billing source unresolved')
    cost = amount(usage.get('cost'))
    if cost != amount(data.get('total_cost')) or ('usage' in data and cost != amount(data['usage'])):
        raise ScoutAccountingError('Response/generation billing mismatch')
    for a, b in [('prompt_tokens', 'native_tokens_prompt'), ('completion_tokens', 'native_tokens_completion')]:
        if integer(usage.get(a)) != integer(data.get(b)):
            raise ScoutAccountingError('Response/generation token usage mismatch')
    if integer(usage.get('total_tokens')) != usage['prompt_tokens'] + usage['completion_tokens']:
        raise ScoutAccountingError('Total token usage mismatch')
    if (response.get('model') != spec['model'] or data.get('model') not in {spec['model'], canonical_model}
            or response.get('provider') != cfg['provider_name'] or data.get('provider_name') != cfg['provider_name']):
        raise ScoutAccountingError('Scout model/provider identity mismatch; billing retained in raw artifacts')
    if cfg['search_engine'] == 'native' and data.get('web_search_engine') != 'native':
        raise ScoutAccountingError('Native search engine not confirmed; no silent engine fallback')
    choices = response.get('choices') or []
    if len(choices) != 1:
        raise ScoutAccountingError('Ambiguous Scout response')
    choice = choices[0]
    message = choice.get('message') or {}
    native = choice.get('native_finish_reason')
    if native != data.get('native_finish_reason') or choice.get('finish_reason') != data.get('finish_reason'):
        raise ScoutAccountingError('Response/generation completion mismatch')
    if message.get('tool_calls') or message.get('role') != 'assistant':
        raise ScoutAccountingError('Unexpected client tool request/response role')
    expected = expected_endpoint(spec)[4]
    stop = 'end_turn' if native == expected and choice.get('finish_reason') == 'stop' else (native or 'unknown')
    if message.get('refusal') or native in ('refusal', 'content_filter'):
        stop = 'refusal'
    text = message.get('content') or ''
    if not isinstance(text, str) or not text.strip():
        stop, text = 'empty_response', ''
    counter = (usage.get('server_tool_use_details') or usage.get('server_tool_use') or {}).get('web_search_requests')
    if counter is not None:
        integer(counter)
    annotations = message.get('annotations') or []
    # Keep provider fields verbatim; none constitutes a complete query timeline.
    citations = [a['url_citation'] for a in annotations if a.get('type') == 'url_citation' and isinstance(a.get('url_citation'), dict)]
    researching = cfg['search_engine'] != 'none'
    warnings = ['Kein vollständiges Suchprotokoll; Suchanfragen im Modelltext sind Selbstauskunft.'] if researching else []
    if counter is not None and counter > spec.get('max_web_search_uses', 0):
        warnings.append('Der Anbieter hat mehr Suchen ausgeführt als angefordert.')
    if usage['completion_tokens'] > spec['max_output_tokens']:
        warnings.append('Abgerechnete Outputtokens einschließlich Suchablauf überschreiten das angeforderte Limit.')
    if researching and not counter and not citations:
        warnings.append('Keine Suche durch Suchzähler oder API-Zitate belegt.')
        if stop == 'end_turn':
            stop = 'search_unverified'
    provenance = {
        'transport': 'openrouter_api', 'generation_id': response['id'],
        'requested_model': spec['model'], 'reported_model': response['model'], 'generation_model': data['model'],
        'provider': response['provider'], 'endpoint': cfg['endpoint'],
        'finish_reason': choice.get('finish_reason'), 'native_finish_reason': native,
        'cost_basis': 'billed', 'billed_usd': str(cost),
        'search_engine_requested': cfg['search_engine'], 'search_engine_reported': data.get('web_search_engine'),
        'search_queries_source': 'model_self_report' if researching else None, 'query_log_complete': False if researching else None,
        'api_search_queries': None, 'web_search_requests': counter, 'citations': citations,
        'warnings': warnings,
    }
    result_usage = {'input_tokens': usage['prompt_tokens'], 'output_tokens': usage['completion_tokens'],
                    'billed_usd': str(cost), 'research_provenance': provenance}
    if counter is not None:
        result_usage['web_search_requests'] = counter
    return text, result_usage, {'stop_reason': stop}, []


def call_scout(spec, system, user, raw_dir):
    """One paid request. Only generation metadata may be polled (read-only)."""
    request = request_for(spec, system, user)
    def save(name, data):
        payload = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False, indent=2, default=str).encode()
        with (raw_dir / name).open('xb') as stream:
            stream.write(payload)
    # Directory creation and prompt recording belong to the existing runners.
    if (raw_dir / 'openrouter-request.json').exists():
        raise ScoutAccountingError('Scout request already exists; no repeat')
    key = key_state()
    catalog = decode(http('GET', '/models'))
    endpoint_raw = http('GET', '/models/' + spec['model'] + '/endpoints')
    model = endpoint_check(spec, catalog, decode(endpoint_raw))
    save('openrouter-model.json', model)
    save('openrouter-endpoint.json', endpoint_raw)
    save('openrouter-key-before.json', key)
    save('openrouter-request.json', request)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        response_raw = http('POST', '/chat/completions', request)
        save('openrouter-response.json', response_raw)
        response = decode(response_raw)
        gid = response.get('id')
        if response.get('error') or not isinstance(gid, str) or not gid.startswith('gen-'):
            raise ScoutAccountingError('No usable generation; stop before any further paid call')
        generation = {}
        for attempt in range(4):
            if attempt:
                time.sleep((2, 8, 20)[attempt - 1])
            generation_raw = http('GET', '/generation?id=' + quote(gid, safe=''))
            save(f'openrouter-generation-{attempt}.json', generation_raw)
            generation = decode(generation_raw)
            if isinstance(generation.get('data'), dict):
                break
        result = assess(spec, response, generation, model.get('canonical_slug') or model['id'])
        provenance = result[1]['research_provenance']
        provenance.update(started_at=started, finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                          response_artifact='openrouter-response.json', generation_artifact=f'openrouter-generation-{attempt}.json')
        save('openrouter-result.json', {'outcome': result[2]['stop_reason'], **result[1]})
        return result
    except Exception as exc:
        # Do not log arbitrary exception strings (HTTP libraries may include headers).
        save('openrouter-failure.json', {'outcome': 'unresolved', 'error_type': type(exc).__name__})
        if isinstance(exc, ScoutAccountingError):
            raise
        raise ScoutAccountingError('Scout call/verification failed; inspect immutable raw artifacts before continuing') from None


def disclosure(provenance):
    if not provenance:
        return ''
    return '\n\n**Recherchebelege:** ' + ' '.join(provenance['warnings'])


def call_wart(spec, system, user, raw_dir, tag, max_tokens=None):
    """Same fixed model as the direct Wart, same transport, no search tools."""
    if spec.get('role') != 'wart' or spec.get('model') != WART_MODEL:
        raise ValueError('Only the unchanged Wart model is approved for this route')
    routed = dict(spec)
    if max_tokens is not None:
        routed['max_output_tokens'] = min(max_tokens, spec['max_output_tokens'])
    directory = raw_dir / tag
    directory.mkdir(parents=True, exist_ok=True)
    text, usage, raw, _ = call_scout(routed, system, user, directory)
    raw['source_artifact'] = f'raw/{tag}/openrouter-response.json'
    return text, usage, raw
