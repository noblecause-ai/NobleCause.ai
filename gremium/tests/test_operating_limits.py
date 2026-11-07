"""Offline calibration and transport regressions for accepted operational risk."""
import copy
import json
from pathlib import Path

import pytest

import cost_bounds
import council_state
import live_debate
import live_session
import openrouter
from test_openrouter import envelope, stub_http

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT/'gremium/config.json').read_text())
LIVE = CONFIG['live_council']
MODELS = {m['model']: m for m in LIVE['models']}


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setattr(openrouter, 'http', lambda *a, **kw: pytest.fail('Unstubbed network call'))


def test_both_full_archives_and_fifty_percent_growth_fit_operating_limits():
    bounds = cost_bounds.InputBounds(LIVE['input_bounds'], ROOT)
    counts = {}
    for name in ('2026-09-21-live', '2026-10-21-regular'):
        count = 0
        for path in (ROOT/'sessions'/name/'raw').glob('*-request.json'):
            stem = str(path).removesuffix('-request.json')
            request = json.loads(path.read_bytes())
            spec = MODELS[request['model']]
            endpoint = json.loads(Path(stem+'-endpoint.json').read_bytes())
            _, usage = openrouter.validate_response(
                spec, openrouter.decode(Path(stem+'-response.json').read_bytes()),
                openrouter.decode(Path(stem+'-generation.json').read_bytes()), endpoint.get('canonical_model'))
            limit = request[spec['openrouter']['token_parameter']]
            tokens = bounds.tokens(spec, request)
            output = bounds.output_tokens(spec, limit)
            openrouter.validate_usage_limits(spec, usage, limit, tokens, output)
            assert usage['input_tokens'] * 3 <= tokens * 2
            expanded = copy.deepcopy(request)
            original = expanded['messages'][1]['content']
            expanded['messages'][1]['content'] += original[:len(original)//2]
            bounds.tokens(spec, expanded)
            count += 1
        counts[name] = count
    assert counts == {'2026-09-21-live': 31, '2026-10-21-regular': 31}


def test_operational_quote_includes_output_margin_in_closure_and_full_session():
    bounds = cost_bounds.InputBounds(LIVE['input_bounds'], ROOT)
    grok = MODELS['x-ai/grok-4.6']
    quote = live_debate.session_budget(LIVE['models'], grok, LIVE['output_limits'], bounds)
    assert bounds.output_tokens(grok, 4096) == 6144
    assert bounds.output_tokens(grok, 16384) == 24576
    assert quote['closure_usd'] == openrouter.amount('3.5426396')
    assert quote['total_usd'] == openrouter.amount('11.612168')


def test_risk_acceptance_and_endpoint_are_required():
    policies = copy.deepcopy(LIVE['input_bounds'])
    spec = MODELS['x-ai/grok-4.6']
    rule = policies[spec['model']]
    bounds = cost_bounds.InputBounds(policies, ROOT)
    rule['risk_accepted'] = False
    with pytest.raises(cost_bounds.MissingBound):
        bounds.policy(spec)
    rule['risk_accepted'] = True
    rule['endpoint'] = 'another-provider'
    with pytest.raises(cost_bounds.MissingBound):
        bounds.policy(spec)


def test_serialized_utf8_limit_stops_before_any_network_or_call_artifact(tmp_path):
    spec = MODELS['x-ai/grok-4.6']
    bounds = cost_bounds.InputBounds(LIVE['input_bounds'], ROOT)
    raw = tmp_path/'raw'
    raw.mkdir()
    runner = live_session.Calls(raw, council_state.Events(tmp_path/'events.json', 'large'),
                                cost_bounds.Budget(30, bounds), openrouter.amount('.85'))
    with pytest.raises(cost_bounds.MissingBound, match='Eingabehülle'):
        runner.run(spec, 'system', 'ü' * 75000, 'debate', 'speech-0', 4096, [])
    assert not list(raw.iterdir())


def test_grok_safety_margin_is_reserved_before_a_debate_call(tmp_path):
    spec = MODELS['x-ai/grok-4.6']
    bounds = cost_bounds.InputBounds(LIVE['input_bounds'], ROOT)
    raw = tmp_path/'raw'
    raw.mkdir()
    runner = live_session.Calls(raw, council_state.Events(tmp_path/'events.json', 'reserve'),
                                cost_bounds.Budget('.19', bounds), openrouter.amount('.85'))
    with pytest.raises(cost_bounds.InsufficientBudget, match='Abschlussreserve'):
        runner.run(spec, 's', 'u', 'debate', 'speech-0', 4096, [(spec, 4096)])
    assert not list(raw.iterdir())


@pytest.mark.parametrize(('output_tokens', 'input_tokens', 'valid'), [(5000, 10, True), (7000, 10, False), (20, 33001, False)])
def test_grok_margin_replay_and_confirmed_overrun_costs(tmp_path, monkeypatch, output_tokens, input_tokens, valid):
    spec = MODELS['x-ai/grok-4.6']
    response, generation = envelope(spec)
    cost = str((openrouter.amount(output_tokens) * 6 + input_tokens * 2) / 1_000_000)
    reasoning = max(output_tokens-100, 0)
    response['usage'].update(prompt_tokens=input_tokens, completion_tokens=output_tokens,
                             total_tokens=output_tokens+input_tokens, cost=cost)
    response['usage']['completion_tokens_details']['reasoning_tokens'] = reasoning
    generation['data'].update(native_tokens_completion=output_tokens,
                              native_tokens_prompt=input_tokens, native_tokens_reasoning=reasoning, total_cost=cost)
    calls = stub_http(monkeypatch, spec, response, generation)
    bounds = cost_bounds.InputBounds(LIVE['input_bounds'], ROOT)
    raw = tmp_path/'raw'
    raw.mkdir()
    events = council_state.Events(tmp_path/'events.json', 'grok')
    runner = live_session.Calls(raw, events, cost_bounds.Budget(3, bounds), openrouter.amount('.85'))
    if valid:
        _, usage = runner.run(spec, 's', 'u', 'debate', 'speech-0', 4096, [])
        assert usage['provenance']['output_limit_observation'] == {'requested':4096, 'billed':5000}
        replay = live_session.Calls(raw, events, cost_bounds.Budget(3, bounds), openrouter.amount('.85'))
        assert replay.run(spec, 's', 'u', 'debate', 'speech-0', 4096, [])[1] == usage
        assert replay.budget.spent == openrouter.amount(cost)
    else:
        with pytest.raises(openrouter.OpenRouterError, match='configured allowance'):
            runner.run(spec, 's', 'u', 'debate', 'speech-0', 4096, [])
        result = json.loads((raw/'speech-0-spacexai-result.json').read_text())
        assert result['confirmed_usage']['billed_usd'] == cost
        assert runner.budget.spent == openrouter.amount(cost)
        with pytest.raises(openrouter.OpenRouterError, match='keine erneute Inferenz'):
            runner.run(spec, 's', 'u', 'debate', 'speech-0', 4096, [])
    assert sum(method == 'POST' for method, *_ in calls) == 1
    assert next(payload for method, _, payload in calls if method == 'POST')['max_tokens'] == 4096
