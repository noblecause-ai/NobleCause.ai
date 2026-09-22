"""Native search observations are distinct from model claims and billing."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'gremium'))
import openrouter_scout as adapter
import run_session
import run_wart

SPECS = json.loads((ROOT / 'gremium/config.json').read_text())['scouts']


def fixture(spec):
    cfg = spec['openrouter']
    canonical = spec['model'] + '-dated'
    model = {'id': spec['model'], 'canonical_slug': canonical,
             'reasoning': {'supported_efforts': [cfg.get('reasoning_effort')]}}
    ep = {'tag': cfg['endpoint'], 'model_id': spec['model'], 'provider_name': cfg['provider_name'],
          'status': 0, 'quantization': cfg['quantization'], 'max_completion_tokens': 8000,
          'supported_parameters': ['max_tokens', 'tools', 'web_search_options', 'reasoning'],
          'pricing': {'prompt': cfg['max_price']['prompt'] / 1_000_000,
                      'completion': cfg['max_price']['completion'] / 1_000_000,
                      'web_search': cfg['max_search_price_usd']}}
    text = '```json\n' + json.dumps({'findings': [], 'search_queries': ['MODEL_CLAIM_ONLY'],
                                    'rejected_findings': [], 'delta_assessment': 'Evidence summary'}) + '\n```'
    native = adapter.expected_endpoint(spec)[4]
    response = {'id': 'gen-test', 'model': spec['model'], 'provider': cfg['provider_name'],
                'choices': [{'finish_reason': 'stop', 'native_finish_reason': native,
                             'message': {'role': 'assistant', 'content': text, 'annotations': [
                                 {'type': 'url_citation', 'url_citation': {'url': 'https://example.org/source', 'title': 'Evidence'}}]}}],
                'usage': {'prompt_tokens': 10, 'completion_tokens': 20, 'total_tokens': 30, 'cost': .002}}
    generation = {'data': {'id': 'gen-test', 'model': canonical, 'provider_name': cfg['provider_name'],
                           'finish_reason': 'stop', 'native_finish_reason': native, 'total_cost': .002,
                           'native_tokens_prompt': 10, 'native_tokens_completion': 20,
                           'web_search_engine': 'native' if cfg['search_engine'] == 'native' else None,
                           'cancelled': False, 'is_byok': False}}
    return model, ep, response, generation


def stub(monkeypatch, spec, mutation=None, pending=False):
    model, ep, response, generation = fixture(spec)
    if mutation:
        mutation(response, generation)
    calls = []
    def http(method, path, payload=None):
        calls.append((method, path, payload))
        if path == '/key':
            result = {'data': {'limit': 10, 'limit_reset': None, 'usage': 3, 'limit_remaining': 7}}
        elif path == '/models':
            result = {'data': [model]}
        elif path.endswith('/endpoints'):
            result = {'data': {'endpoints': [ep]}}
        elif path == '/chat/completions':
            result = response
        elif path.startswith('/generation?'):
            count = sum(c[1].startswith('/generation?') for c in calls)
            result = {'error': {'code': 404}} if pending and count == 1 else generation
        else:
            raise AssertionError(path)
        return json.dumps(result).encode()
    monkeypatch.setattr(adapter, 'http', http)
    monkeypatch.setattr(adapter.time, 'sleep', lambda _: None)
    return calls


@pytest.mark.parametrize('spec', SPECS, ids=lambda s: s['family'])
def test_pinned_native_search_records_billing_and_explicit_gaps(tmp_path, monkeypatch, spec):
    calls = stub(monkeypatch, spec)
    text, usage, raw, queries = adapter.call_scout(spec, 'SYSTEM', 'USER', tmp_path)
    assert raw['stop_reason'] == 'end_turn'
    assert queries == [] and 'MODEL_CLAIM_ONLY' in text
    proof = usage['research_provenance']
    assert proof['query_log_complete'] is False and proof['api_search_queries'] is None
    assert proof['web_search_requests'] is None
    assert proof['citations'][0]['url'] == 'https://example.org/source'
    assert usage['billed_usd'] == '0.002'
    request = next(c[2] for c in calls if c[0] == 'POST')
    assert request['provider']['only'] == [spec['openrouter']['endpoint']]
    assert request['provider']['allow_fallbacks'] is False
    assert request['messages'] == [{'role': 'system', 'content': 'SYSTEM'}, {'role': 'user', 'content': 'USER'}]
    assert ('web_search_options' in request) == (spec['family'] == 'perplexity')
    assert ('tools' in request) == (spec['family'] != 'perplexity')
    assert json.loads((tmp_path / 'openrouter-result.json').read_text())['billed_usd'] == '0.002'
    with pytest.raises(adapter.ScoutAccountingError, match='no repeat'):
        adapter.call_scout(spec, 'SYSTEM', 'USER', tmp_path)
    assert sum(c[0] == 'POST' for c in calls) == 1


def test_generation_polling_never_repeats_inference(tmp_path, monkeypatch):
    calls = stub(monkeypatch, SPECS[0], pending=True)
    adapter.call_scout(SPECS[0], 's', 'u', tmp_path)
    assert sum(c[0] == 'POST' for c in calls) == 1
    assert (tmp_path / 'openrouter-generation-1.json').exists()


@pytest.mark.parametrize('mutation', [
    lambda r, g: g['data'].update(total_cost=.003),
    lambda r, g: g['data'].update(model='unapproved-model'),
    lambda r, g: r.update(provider='wrong-provider'),
    lambda r, g: g['data'].update(native_tokens_prompt=11),
    lambda r, g: g['data'].update(web_search_engine='exa'),
])
def test_unresolved_response_aborts_remaining_scouts(tmp_path, monkeypatch, mutation):
    calls = stub(monkeypatch, SPECS[0], mutation=mutation)
    monkeypatch.setattr(run_wart, 'ROOT', tmp_path)
    with pytest.raises(adapter.ScoutAccountingError):
        run_wart.collect_scout_reports(SPECS, 's', 'u', tmp_path / 'raw')
    assert sum(c[0] == 'POST' for c in calls) == 1
    assert (tmp_path / 'raw/scout-1/openrouter-failure.json').exists()
    assert not (tmp_path / 'raw/scout-2').exists()


def test_native_counter_and_output_overruns_are_disclosed():
    spec = SPECS[0]
    model, ep, response, generation = fixture(spec)
    response['usage'].update(server_tool_use_details={'web_search_requests': 13}, completion_tokens=9000, total_tokens=9010)
    generation['data']['native_tokens_completion'] = 9000
    text, usage, raw, queries = adapter.assess(spec, response, generation, model['canonical_slug'])
    assert raw['stop_reason'] == 'end_turn' and queries == []
    assert usage['web_search_requests'] == 13
    assert len(usage['research_provenance']['warnings']) == 3


def test_no_api_search_evidence_is_not_a_successful_research_result():
    spec = SPECS[2]
    model, _, response, generation = fixture(spec)
    response['choices'][0]['message'].pop('annotations')
    assert adapter.assess(spec, response, generation, model['canonical_slug'])[2]['stop_reason'] == 'search_unverified'


def test_truncated_response_keeps_billed_usage():
    spec = SPECS[2]
    model, _, response, generation = fixture(spec)
    response['choices'][0].update(finish_reason='length', native_finish_reason='max_tokens')
    generation['data'].update(finish_reason='length', native_finish_reason='max_tokens')
    result = adapter.assess(spec, response, generation, model['canonical_slug'])
    assert result[2]['stop_reason'] == 'max_tokens' and result[1]['billed_usd'] == '0.002'


def test_both_cost_paths_use_billed_amount_without_guessing_search_count():
    spec = SPECS[1]
    model, _, response, generation = fixture(spec)
    usage = adapter.assess(spec, response, generation, model['canonical_slug'])[1]
    weekly = run_wart.compute_role_costs(usage, spec, .85)
    assert weekly['usd_total'] == .002 and weekly['web_search_requests'] is None
    total = run_session.empty_wart_usage()
    run_session.accumulate_wart_usage(total, usage)
    session = run_session.compute_wart_cost(total, spec, .85)
    assert session['usd'] == .002 and session['web_search_requests'] is None


@pytest.mark.parametrize('data', [
    {'limit': None, 'usage': 0, 'limit_remaining': None},
    {'limit': 10, 'usage': 10, 'limit_remaining': 0},
    {'limit': 10, 'usage': 3, 'limit_remaining': 7, 'limit_reset': 'monthly'},
])
def test_missing_or_exhausted_key_limit_blocks_inference(monkeypatch, data):
    monkeypatch.setattr(adapter, 'http', lambda method, path: json.dumps({'data': data}).encode())
    with pytest.raises(adapter.OpenRouterError):
        adapter.key_state()


def test_weekly_record_persists_search_limitations_and_billed_costs(tmp_path, monkeypatch):
    cfg = json.loads((ROOT / 'gremium/config.json').read_text())
    cfg['features']['three_scouts']['enabled'] = True
    cfg['features']['live_council']['enabled'] = False
    here = tmp_path / 'gremium'
    here.mkdir()
    (here / 'config.json').write_text(json.dumps(cfg))
    session_dir = tmp_path / 'sessions/2026-08'
    session_dir.mkdir(parents=True)
    (session_dir / 'session.json').write_text(json.dumps({
        'number': 4, 'date': '2026-08-06', 'question': 'HISTORY_ONLY', 'recommendations': [],
    }))
    (tmp_path / 'schedule.json').write_text('{}')
    seen = []
    def native_call(spec, system, user, raw_dir):
        assert 'HISTORY_ONLY' not in system + user
        seen.append(spec['model'])
        model, _, response, generation = fixture(spec)
        return adapter.assess(spec, response, generation, model['canonical_slug'])
    def wart_call(spec, system, user, raw_dir):
        assert len(seen) == 3 and 'Selbstauskunft' in user
        return ('```json\n{"convene":false,"convene_rationale":"No trigger."}\n```',
                {'input_tokens': 1, 'output_tokens': 1, 'billed_usd': '0.001'}, {'stop_reason': 'end_turn'})
    monkeypatch.setattr(run_wart, 'ROOT', tmp_path)
    monkeypatch.setattr(run_wart, 'HERE', here)
    monkeypatch.setattr(run_wart, 'load_env', lambda *a: None)
    required = []
    monkeypatch.setattr(run_wart, 'require_keys', lambda *a: required.extend(a))
    monkeypatch.setattr(adapter, 'call_scout', native_call)
    monkeypatch.setattr(run_wart, 'call_wart_decision', wart_call)
    monkeypatch.setattr(sys, 'argv', ['run_wart.py', '--date', '2026-09-20'])
    run_wart.main()
    entry = json.loads((tmp_path / 'journal/2026-09-20/entry.json').read_text())
    assert set(required) == {'OPENROUTER_API_KEY'}
    assert all(s['research_provenance']['query_log_complete'] is False for s in entry['scouts'])
    assert all(c['usd_total'] == .002 and c['cost_basis'] == 'billed' for c in entry['costs']['components']['scouts'])
    assert 'Selbstauskunft' in entry['content_md']
    from jsonschema import Draft202012Validator
    Draft202012Validator(json.loads((ROOT / 'schema/journal.schema.json').read_text())).validate(entry)


def test_wart_uses_same_model_without_search_or_direct_key(tmp_path, monkeypatch):
    spec = json.loads((ROOT / 'gremium/config.json').read_text())['wart_openrouter']
    def decision(response, generation):
        response['choices'][0]['message'].update(
            content='```json\n{"convene":false,"convene_rationale":"No material change."}\n```', annotations=[])
    calls = stub(monkeypatch, spec, mutation=decision)
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    text, usage, raw = run_wart.call_wart_decision(spec, 's', 'u', tmp_path)
    assert run_wart.parse_wart_decision(text)['convene'] is False
    assert raw['stop_reason'] == 'end_turn' and usage['billed_usd'] == '0.002'
    request = next(c[2] for c in calls if c[0] == 'POST')
    assert request['model'] == 'anthropic/claude-fable-5'
    assert not {'tools', 'plugins', 'web_search_options'} & request.keys()


def test_session_wart_opening_and_summary_share_gateway(tmp_path, monkeypatch):
    spec = json.loads((ROOT / 'gremium/config.json').read_text())['wart_openrouter']
    seen = []
    def call(spec, system, user, raw_dir, tag, max_tokens=None):
        seen.append(tag)
        return ('```json\n{"summary":"Short summary","dissent_highlights":[]}\n```',
                {'input_tokens': 1, 'output_tokens': 1, 'billed_usd': '0.002'}, {'stop_reason': 'end_turn'})
    monkeypatch.setattr(adapter, 'call_wart', call)
    run_session.call_wart_simple(spec, 's', 'u', tmp_path, 'opening')
    result = run_session.generate_summary('q', [], [], '', spec, tmp_path, summary_prompt=run_session.prompts.WART_SUMMARY)
    assert seen == ['opening', 'summary-wart'] and result[0] == 'Short summary'
    assert result[2]['billed_usd'] == '0.002'
