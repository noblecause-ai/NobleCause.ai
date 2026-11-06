"""Replay the complete discovery path without Exa or OpenRouter network access."""
import datetime as dt
import json
from pathlib import Path

import pytest

import exa_scout as scout
import run_wart
from openrouter_scout import ScoutAccountingError

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / 'gremium/config.json').read_text())
SPEC = CONFIG['exa_discovery_candidate']
TODAY = dt.date(2026, 11, 6)
EXCERPT = 'The study found a measurable effect in two settings.'


@pytest.fixture
def replay(monkeypatch):
    monkeypatch.setenv('OPENROUTER_API_KEY', 'offline')
    monkeypatch.setenv('EXA_API_KEY', 'offline')
    monkeypatch.setattr(scout.router.time, 'sleep', lambda _: None)
    endpoint = {
        'tag': SPEC['openrouter']['endpoint'], 'model_id': SPEC['model'],
        'provider_name': 'PrimeIntellect', 'quantization': 'fp8', 'status': 0,
        'context_length': 262144, 'max_completion_tokens': 32768, 'native_tools': {},
        'supported_parameters': ['response_format', 'structured_outputs', 'reasoning', 'tool_choice', 'max_tokens'],
        'supports_tool_choice': {'none': True},
        'pricing': {'prompt': '0.000000010', 'completion': '0.000000092',
                    'input_cache_read': '0.000000009'},
    }
    model = {'id': SPEC['model'], 'reasoning': {'mandatory': False}}
    report = {'findings': [
        {'pillar': pillar, 'topic': 'Intervention', 'summary': 'Messbarer Effekt.',
         'source_id': source, 'excerpt': EXCERPT, 'source_language': 'en',
         'evidence_type': 'Feldstudie', 'uncertainty': 'Kleine Stichprobe.',
         'counterevidence': 'Zwei Standorte.'}
        for pillar, source in [('A', 'S1'), ('B', 'S2')]
    ], 'gaps': {'A': None, 'B': None, 'C': 'Keine Primärquelle.', 'D': 'Fehlende Daten.'},
        'delta_assessment': 'Begrenzte Evidenz in zwei Säulen.'}
    choice = {'finish_reason': 'stop', 'native_finish_reason': 'eos',
              'message': {'role': 'assistant'}}
    usage = {'prompt_tokens': 2400, 'completion_tokens': 600, 'total_tokens': 3000, 'cost': .00008}
    generation = {'id': 'gen-offline', 'model': SPEC['model'], 'provider_name': 'PrimeIntellect',
                  'finish_reason': 'stop', 'native_finish_reason': 'eos', 'cancelled': False,
                  'is_byok': False, 'total_cost': .00008,
                  'native_tokens_prompt': 2400, 'native_tokens_completion': 600}
    calls = []
    searches = []

    def http(method, path, payload=None):
        calls.append((method, path, payload))
        if path == '/key':
            value = {'data': {'limit': 40, 'limit_reset': None, 'usage': 34, 'limit_remaining': 6}}
        elif path == '/models':
            value = {'data': [model]}
        elif path.endswith('/endpoints'):
            value = {'data': {'endpoints': [endpoint]}}
        elif path == '/credits':
            value = {'data': {'total_credits': 109, 'total_usage': 34}}
        elif path == '/chat/completions':
            choice['message']['content'] = json.dumps(report)
            value = {'id': 'gen-offline', 'model': SPEC['model'], 'provider': 'PrimeIntellect',
                     'choices': [choice], 'usage': usage}
        elif path.startswith('/generation?'):
            reads = sum(p.startswith('/generation?') for _, p, _ in calls)
            value = {'data': generation} if reads == 4 else {'error': {'code': 404}}
        else:
            raise AssertionError(path)
        return json.dumps(value).encode()

    def search(request):
        searches.append(request)
        results = [{'url': url, 'title': 'Study', 'publishedDate': date, 'highlights': [EXCERPT]}
                   for url, date in [('https://uni.example/study#page', '2026-11-01'),
                                     ('https://health.example/report', '2026-10-28'),
                                     ('https://noblecause.ai/journal/2026-11-05/', '2026-11-05')]]
        return json.dumps({'results': results, 'requestId': f'R{len(searches)}',
                           'searchType': 'lite', 'costDollars': {'total': .004}}).encode()

    monkeypatch.setattr(scout.router, 'http', http)
    monkeypatch.setattr(scout, 'search', search)
    return calls, searches, endpoint, report, choice, generation


def test_discovery_replays_weekly_entrypoint_with_exact_sources_and_one_inference(tmp_path, replay):
    calls, searches, _, _, _, _ = replay
    text, usage, raw, queries = run_wart.call_scout(SPEC, 'history A', 'history B', tmp_path, as_of=TODAY)
    assert raw['stop_reason'] == 'end_turn'
    assert len(searches) == len(queries) == 6
    assert all(s['type'] == 'lite' and s['numResults'] == 3 and s['contents'] == {'highlights': True} for s in searches)
    assert len([s for s in calls if s[1].startswith('/generation?')]) == 4
    assert (tmp_path / 'openrouter-generation-3.json').exists()
    request, = [payload for method, _, payload in calls if method == 'POST']
    assert request['provider']['only'] == ['primeintellect/fp8']
    assert request['provider']['allow_fallbacks'] is False
    assert request['provider']['max_price'] == {'prompt': '0.02', 'completion': '0.2'}
    assert request['tool_choice'] == 'none' and 'tools' not in request and 'web_search_options' not in request
    assert {plugin['id']: plugin['enabled'] for plugin in request['plugins']} == dict.fromkeys(
        ('web', 'response-healing', 'file-parser', 'armor', 'pareto-router', 'auto-router'), False,
    )
    assert request['response_format']['json_schema']['strict'] is True
    assert 'history A' not in str(request) and 'history B' not in str(request)
    assert 'noblecause.ai/journal' not in str(request)
    parsed = run_wart.parse_scout_answer(text)
    assert parsed['search_queries'] == queries
    assert [f['source'] for f in parsed['findings']] == ['https://uni.example/study', 'https://health.example/report']
    provenance = usage['research_provenance']
    assert provenance['query_log_complete'] is True and provenance['api_search_queries'] == queries
    assert provenance['billed_usd'] == '0.00008' and provenance['exa_billed_usd'] == '0.024'
    assert run_wart.compute_role_costs(usage, SPEC, 1)['usd_total'] == .02408
    assert float(json.loads((tmp_path / 'budget.json').read_text())['total_bound_usd']) <= .15
    with pytest.raises(scout.ExaScoutError, match='already attempted'):
        scout.call_scout(SPEC, tmp_path, TODAY)
    assert sum(c[0] == 'POST' for c in calls) == 1 and len(searches) == 6


@pytest.mark.parametrize('changed', [
    {'context_length': 1_048_576},
    {'pricing': {'prompt': '.000000010', 'completion': '.000001', 'overrides': [{}]}},
    {'pricing': {'prompt': '.000000010', 'completion': '.000000092', 'request': '.1'}},
])
def test_budget_drift_stops_before_search_or_inference(tmp_path, replay, changed):
    calls, searches, endpoint, _, _, _ = replay
    endpoint.update(changed)
    with pytest.raises(ValueError):
        scout.call_scout(SPEC, tmp_path, TODAY)
    assert not searches and all(c[0] == 'GET' for c in calls)


def test_replay_budget_applies_before_any_paid_call(tmp_path, replay):
    calls, searches, _, _, _, _ = replay
    with pytest.raises(scout.ExaScoutError, match='authorized budget'):
        scout.evaluation_preflight(SPEC, tmp_path, limit=scout.Decimal('0.060'), search_bound=scout.Decimal(0))
    assert not searches and all(c[0] == 'GET' for c in calls)


def test_exa_rate_limit_stops_after_one_search_and_before_model(tmp_path, replay, monkeypatch):
    calls, searches, _, _, _, _ = replay

    def rate_limit(request):
        searches.append(request)
        raise scout.ExaScoutError('Exa returned HTTP 429; search stopped')

    monkeypatch.setattr(scout, 'search', rate_limit)
    with pytest.raises(scout.ExaScoutError, match='429'):
        scout.call_scout(SPEC, tmp_path, TODAY)
    assert len(searches) == 1 and all(c[0] == 'GET' for c in calls)
    assert (tmp_path / 'exa-1-failure.json').exists()


@pytest.mark.parametrize('failure', ['truncation', 'invented source', 'model search'])
def test_invalid_evaluation_retains_receipt_and_cannot_pass(tmp_path, replay, failure):
    calls, _, _, report, choice, generation = replay
    if failure == 'truncation':
        for obj in (choice, generation):
            obj.update(finish_reason='length', native_finish_reason='end_turn')
    elif failure == 'invented source':
        report['findings'][0]['source_id'] = 'S99'
    else:
        generation['num_search_results'] = 1
    with pytest.raises((scout.ExaScoutError, ScoutAccountingError)):
        scout.call_scout(SPEC, tmp_path, TODAY)
    assert sum(c[0] == 'POST' for c in calls) == 1
    assert (tmp_path / 'openrouter-generation-3.json').exists()
    assert not (tmp_path / 'exa-report.json').exists()


def test_discovery_failure_cannot_pay_for_other_scouts(tmp_path):
    attempted = []

    def caller(spec, system, user, directory):
        attempted.append(spec['model'])
        raise scout.ExaScoutError('No usable source package')

    with pytest.raises(RuntimeError, match='Keine weiteren Modellaufrufe'):
        run_wart.collect_scout_reports([SPEC, *CONFIG['scouts'][1:]], 'system', 'user', tmp_path, caller)
    assert attempted == [SPEC['model']]
