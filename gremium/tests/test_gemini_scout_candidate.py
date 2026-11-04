"""Gemini is prepared for acceptance testing, not activated by this change."""
import copy
import json
from pathlib import Path

import pytest

import openrouter_scout as adapter
from test_openrouter_scout import fixture

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = json.loads((ROOT / 'gremium/gemini-scout-candidate.json').read_text())


def test_google_candidate_uses_only_native_search_and_pinned_provider():
    model, ep, response, receipt = fixture(CANDIDATE)
    ep['native_tools'] = {'openrouter:web_search': {'type': 'google_search'}}
    adapter.endpoint_check(CANDIDATE, {'data': [model]}, {'data': {'endpoints': [ep]}})
    request = adapter.request_for(CANDIDATE, 'BLIND_SYSTEM', 'BLIND_USER')
    assert request['provider']['only'] == ['google-ai-studio']
    assert request['provider']['allow_fallbacks'] is False
    assert request['tools'][0]['parameters']['engine'] == 'native'
    text, usage, raw, _ = adapter.assess(CANDIDATE, response, receipt, model['canonical_slug'])
    assert raw['stop_reason'] == 'end_turn' and usage['billed_usd'] == '0.002'
    assert 'MODEL_CLAIM_ONLY' in text


def test_missing_google_native_tool_blocks_before_inference():
    model, ep, _, _ = fixture(CANDIDATE)
    with pytest.raises(ValueError, match='native Google Search'):
        adapter.endpoint_check(CANDIDATE, {'data': [model]}, {'data': {'endpoints': [ep]}})


def test_search_engine_fallback_receipt_is_never_accepted():
    model, _, response, receipt = fixture(CANDIDATE)
    receipt['data']['web_search_engine'] = 'exa'
    with pytest.raises(adapter.ScoutAccountingError, match='Native search'):
        adapter.assess(CANDIDATE, response, receipt, model['canonical_slug'])


def test_candidate_does_not_change_active_roster_or_blind_roles():
    from process_config import configured_scouts
    config = json.loads((ROOT / 'gremium/config.json').read_text())
    assert config['scouts'][0]['model'] == 'x-ai/grok-4.6'
    assert CANDIDATE['model'] not in {s['model'] for s in config['scouts']}
    proposed = copy.deepcopy(config)
    proposed['scouts'][0] = CANDIDATE
    assert configured_scouts(proposed)[0]['research_context'] == 'blind'
    assert proposed['live_council'] == config['live_council']
