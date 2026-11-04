"""The approved one-credit test cannot run as an ordinary monitor or retry."""
import datetime as dt
import json
from pathlib import Path

import pytest

import gemini_scout_canary as canary

ROOT = Path(__file__).resolve().parents[2]
SPEC = json.loads((ROOT / 'gremium/gemini-scout-candidate.json').read_text())
KEY = {'limit': '33.87', 'limit_reset': None,
       'usage': canary.BASE_USAGE, 'limit_remaining': '0.999314693'}


@pytest.fixture
def root(tmp_path, monkeypatch):
    (tmp_path / 'gremium').mkdir()
    (tmp_path / 'gremium/gemini-scout-candidate.json').write_text(json.dumps(SPEC))
    for name, value in {'GITHUB_EVENT_NAME': 'workflow_dispatch',
                        'GITHUB_REF': 'refs/heads/codex/gemini-scout-canary-20261104',
                        'GITHUB_REPOSITORY': 'noblecause-ai/NobleCause.ai',
                        'GITHUB_RUN_ATTEMPT': '1'}.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(canary.scout, 'key_state', lambda: KEY.copy())
    return tmp_path


def answer():
    return {'findings': [{'pillar': 'B', 'topic': 'Primary evidence', 'summary': 'Measured outcome.',
                         'source': 'https://example.org/study', 'source_language': 'en',
                         'evidence_type': 'Trial', 'source_date': '2026-01-01', 'event_date': None,
                         'uncertainty': 'Transfer uncertain.', 'counterevidence': 'Mixed results.'}],
            'search_queries': ['primary study'], 'rejected_findings': [], 'delta_assessment': 'Uncertain.'}


def test_default_does_not_call_a_provider(root, monkeypatch):
    monkeypatch.setattr(canary.scout, 'call_scout', lambda *args: pytest.fail('No authorized paid call'))
    assert canary.run(root)['inference_calls'] == 0


@pytest.mark.parametrize('change', [{'limit': 40, 'limit_remaining': 7},
                                  {'usage': '32.88'}, {'limit_reset': 'daily'}])
def test_no_paid_call_without_the_exact_budget_and_starting_usage(root, monkeypatch, change):
    monkeypatch.setattr(canary.scout, 'key_state', lambda: {**KEY, **change})
    monkeypatch.setattr(canary.scout, 'call_scout', lambda *args: pytest.fail('Unsafe test budget'))
    with pytest.raises(ValueError, match='server-side key room'):
        canary.run(root, paid=True)


def test_workflow_rerun_cannot_repeat_inference(root, monkeypatch):
    monkeypatch.setenv('GITHUB_RUN_ATTEMPT', '2')
    monkeypatch.setattr(canary.scout, 'call_scout', lambda *args: pytest.fail('Inference retried'))
    with pytest.raises(ValueError, match='single approved'):
        canary.run(root, paid=True)


def test_paid_canary_uses_the_unchanged_blind_prompt_and_no_other_models(root, monkeypatch):
    calls = []
    def call(spec, system, user, output):
        calls.append(spec['model'])
        assert system == canary.prompts.scout_system_for(SPEC, canary.prompts.SCOUT_SYSTEM)
        assert user == canary.prompts.SCOUT_BLIND_USER.format(
            question=canary.prompts.SCOUT_BLIND_QUESTION, as_of='2026-11-04')
        return json.dumps(answer()), {'billed_usd': '.2', 'research_provenance': {}}, {'stop_reason': 'end_turn'}, []
    monkeypatch.setattr(canary.scout, 'call_scout', call)
    result = canary.run(root, paid=True)
    assert calls == ['google/gemini-4-argon'] and result['status'] == 'technical_pass'
    assert result['dossier_requires_source_review'] is True and result['production_changed'] is False


def test_uncertain_charge_is_retained_as_an_attempt_and_never_retried(root, monkeypatch):
    calls = []
    def call(spec, system, user, output):
        calls.append(spec['model'])
        (output / 'openrouter-request.json').write_text('{}')
        raise canary.scout.ScoutAccountingError('SECRET_MUST_NOT_APPEAR')
    monkeypatch.setattr(canary.scout, 'call_scout', call)
    result = canary.run(root, paid=True)
    assert result['status'] == 'failed' and result['inference_calls'] == len(calls) == 1
    saved = (root / 'gremium/.probe-raw/gemini-canary/canary-status.json').read_text()
    assert 'SECRET_MUST_NOT_APPEAR' not in saved


def test_dossier_rejects_future_and_missing_sources():
    parsed = answer()
    parsed['findings'][0]['source_date'] = '2026-11-05'
    with pytest.raises(ValueError, match='Future'):
        canary.check_dossier(json.dumps(parsed), 'end_turn', SPEC, dt.date(2026, 11, 4))
    parsed = answer()
    parsed['findings'][0]['source'] = ''
    with pytest.raises(ValueError, match='source'):
        canary.check_dossier(json.dumps(parsed), 'end_turn', SPEC, dt.date(2026, 11, 4))
