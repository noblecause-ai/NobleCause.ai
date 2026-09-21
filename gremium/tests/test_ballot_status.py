"""Explicit abstentions: one vote per seat, unchanged majority, original text."""
import copy
import json

import pytest

from test_live_council import (ROOT, SPECS, FakeCalls, fenced, setup_run,
                              vote_payload, live_session, state, run_session, organizations)
from ballot_status import CONTRACT, read_decision
import live_debate


def abstain(rec):
    return {**rec, 'decision':'abstain', 'organization':None, 'donation_url':None,
            'conditional':None, 'reservation':None, 'confidence':None,
            'abstention_reason':'Ungeklärter Interessenkonflikt; NTI bleibt Prüfkandidat.'}


def tally(votes):
    return run_session.aggregate_recommendations(votes, procedure_version='0.6', ballot_contract=CONTRACT)


@pytest.mark.parametrize('support', [0, 2, 3, 4, 5])
def test_abstentions_do_not_support_or_lower_majority_or_count_as_invalid(support):
    votes = [{'label':f'm{i}', 'parsed':vote_payload()} for i in range(5)]
    for v in votes[support:]:
        v['parsed']['recommendations'] = [abstain(r) for r in v['parsed']['recommendations']]
    recs, unresolved = tally(votes)
    assert unresolved == []
    for rec in recs:
        assert rec['has_consensus'] is (support >= 3)
        assert (rec['votes_valid'], rec['votes_abstained'], rec['votes_invalid']) == (support, 5-support, 0)
        assert [a['model'] for a in rec['abstentions']] == [f'm{i}' for i in range(support, 5)]
        if support >= 3:
            assert rec['convergence']['count'] == support and rec['convergence']['total'] == 5
            assert rec['confidence'] == .8


@pytest.mark.parametrize('changes', [
    {'decision':None}, {'decision':'yes'}, {'decision':True},
    {'decision':'abstain'}, # Org + conditional from recommendation: conflicting.
    {'abstention_reason':'Enthaltung steht nur im Freitext'},
    {'conditional':'false'}, {'conditional':True, 'reservation':None},
    {'conditional':False, 'reservation':'Bedingung'},
])
def test_missing_or_conflicting_status_is_invalid_without_prose_guessing(changes):
    obj = vote_payload()
    obj['recommendations'][2].update(changes)
    votes = [{'label':'m0', 'parsed':obj}]
    rec = tally(votes)[0][2]
    assert rec['votes_valid'] == rec['votes_abstained'] == 0
    assert rec['votes_invalid'] == 5 and rec['warnings']
    with pytest.raises(ValueError, match='Vier-Säulen'):
        live_debate.vote(fenced(obj), SPECS, SPECS[0])


def test_duplicate_recommendation_and_abstention_for_same_pillar_is_invalid():
    obj = vote_payload()
    obj['recommendations'].append(abstain(obj['recommendations'][2]))
    rec = tally([{'label':'m0','parsed':obj}])[0][2]
    assert rec['votes_valid'] == rec['votes_abstained'] == 0
    with pytest.raises(ValueError, match='Sitzstimme'):
        tally([{'label':'m0','parsed':obj}, {'label':'m0','parsed':obj}])


def test_abstention_requires_reason_and_null_recommendation_fields():
    rec = abstain(vote_payload()['recommendations'][2])
    assert read_decision(rec) == 'abstain'
    for field in ('organization','donation_url','conditional','reservation'):
        assert read_decision({**rec,field:False}) is None
    for reason in ('', '  ', None, False):
        assert read_decision({**rec,'abstention_reason':reason}) is None
    for field in ('decision','abstention_reason','organization'):
        missing = {k:v for k,v in rec.items() if k != field}
        assert read_decision(missing) is None


def test_old_contract_keeps_its_historical_interpretation():
    obj = vote_payload()
    for r in obj['recommendations']:
        r.pop('decision');r.pop('abstention_reason')
    obj['recommendations'][2]['reservation'] = 'Enthaltung im alten Freitext'
    obj['recommendations'][2]['conditional'] = True
    votes = [{'label':f'm{i}','parsed':copy.deepcopy(obj)} for i in range(5)]
    old = run_session.aggregate_recommendations(votes,procedure_version='0.6')[0][2]
    assert old['convergence']['count'] == 5 and 'votes_abstained' not in old
    new = tally(votes)[0][2]
    assert new['votes_valid'] == 0 and new['votes_invalid'] == 5


def test_youth_impact_registry_is_explicit_and_donation_url_comes_from_registry():
    organizations.load_registry(ROOT/'organizations.json')
    assert organizations.resolve('Youth Impact') == organizations.resolve('Young 1ove') == 'youth-impact'
    assert organizations.resolve('ConnectEd') is None # Program is not an organization alias.
    votes = [{'label':f'm{i}', 'parsed':vote_payload('Youth Impact')} for i in range(5)]
    recs, unresolved = tally(votes)
    assert not unresolved
    assert all(r['organization_id']=='youth-impact' and r['donation_url']=='https://www.youth-impact.org/donate' for r in recs)
    votes[0]['parsed']['recommendations'][0]['organization'] = 'Unknown new candidate'
    recs, unresolved = tally(votes)
    assert unresolved == [{'pillar':'A','organization':'Unknown new candidate','model':'m0'}]
    assert recs[0]['convergence']['count'] == 4 and recs[0]['votes_invalid'] == 1


def test_full_session_preserves_abstention_in_raw_feed_projection_and_tally(tmp_path, monkeypatch):
    class AbstainingCalls(FakeCalls):
        def run(self, *args):
            text, usage = super().run(*args)
            if args[0]['model'] == SPECS[1]['model'] and args[4].startswith(('initial-', 'final-')):
                obj = run_session.extract_json_block(text)
                obj['recommendations'][2] = abstain(obj['recommendations'][2])
                text = fenced(obj, run_session.strip_json_block(text))
            return text, usage
    cfg,args = setup_run(tmp_path, monkeypatch)
    monkeypatch.setattr(live_session,'Calls',AbstainingCalls)
    record = live_session.run(tmp_path,cfg,args)
    assert record['ballot_contract'] == CONTRACT
    rec = record['recommendations'][2]
    assert (rec['convergence']['count'],rec['convergence']['total'],rec['votes_abstained'],rec['votes_invalid']) == (4,5,1,0)
    for round_ in (record['rounds'][0],record['rounds'][2]):
        projection = next(v for v in round_['votes'] if v['model']==SPECS[1]['model'])['recommendations'][2]
        assert projection['decision']=='abstain' and projection['organization_id'] is None
    assert state.validate_record(tmp_path/'runs/test') == record
    bad = copy.deepcopy(record)
    bad['recommendations'][2]['convergence']['models'].append(SPECS[1]['label'])
    with pytest.raises(ValueError,match='Enthaltungen'):
        state.validate_record(tmp_path/'runs/test',bad)
