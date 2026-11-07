"""Autonomy tests never send paid calls: due dates, holds and existing adapters."""
import datetime as dt
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'gremium'))
from council_state import digest, encoded
import regular_operation as operation
import openrouter
import openrouter_scout
import preflight
from test_live_council import synthetic_policies

NOW = dt.datetime(2026,9,22,12,tzinfo=dt.timezone.utc)


@pytest.fixture
def config():
    return json.loads((REPO/'gremium/config.json').read_text())


@pytest.fixture
def root(tmp_path, monkeypatch):
    (tmp_path/'schedule.json').write_text(json.dumps({
        'next_research':'2026-09-28T06:00:00Z','next_session':'2026-10-21T12:00:00Z','unknown':{'keep':True},
        'council_rotation':{'procedure_version':'0.6','next_index':1,'accepted':{}}}))
    (tmp_path/'sessions').mkdir()
    (tmp_path/'journal').mkdir()
    monkeypatch.setenv('GITHUB_RUN_ID','123')
    monkeypatch.setenv('GITHUB_RUN_ATTEMPT','1')
    return tmp_path


def reschedule(root, **fields):
    p=root/'schedule.json'
    data=json.loads(p.read_text());data.update(fields);p.write_text(json.dumps(data))


def dossier(root, config, date='2026-09-21'):
    path=root/'journal'/date/'entry.json';path.parent.mkdir()
    data={'date': date, 'research_mode': 'blind_then_compare',
          'scouts': [{'model': scout['model'], 'findings': [{'topic': 'Evidence'}],
                      'research_provenance': {'query_log_complete': False}} for scout in config['scouts']]}
    path.write_text(json.dumps(data))
    (path.parent/'raw').mkdir()
    (path.parent/'raw/original.json').write_bytes(b'{"unchanged":true}\n')
    return path


def test_approved_production_defaults_and_no_premature_calls(root,config):
    assert operation.configuration(config)['cost_mode']=='observe'
    for kind in ('research','session'):
        result=operation.plan(root,config,kind,NOW)
        assert result['ready'] is False and result['chair']=='openai/gpt-6-astra'
    assert not list((root/'journal').iterdir())


def test_due_research_catches_up_after_monday_without_rotating(root,config):
    reschedule(root,next_research='2026-09-21T06:00:00Z')
    p=operation.plan(root,config,'research',NOW)
    assert p['ready'] and p['date']=='2026-09-22' and p['rotation_index']==1


def test_council_tariff_hold_does_not_block_weekly_research(root, config):
    config['scouts'][0] = config.get('exa_discovery_candidate', config['scouts'][0])
    hold = {'reason': 'Tarif und Abschlussreserve ungeprüft'}
    reschedule(root, next_research='2026-09-21T06:00:00Z',
               regular_operation={'session_hold': hold})
    assert operation.inspect_plan(root, config, 'session')['session_hold'] == hold
    assert operation.plan(root, config, 'research', NOW)['ready'] is True
    with pytest.raises(RuntimeError, match='Tarif- und Budgetfreigabe'):
        operation.plan(root, config, 'session', NOW)
    with pytest.raises(RuntimeError, match='gesperrt'):
        operation.reserve(root, {'kind': 'session', 'due': '2026-09-21T06:00:00Z'})


def test_due_session_reuses_current_dossier_and_stable_id(root,config):
    dossier(root, config)
    config['live_council']['input_bounds'] = synthetic_policies(root)
    reschedule(root,next_session='2026-09-21T12:00:00Z')
    p=operation.plan(root,config,'session',NOW)
    assert p['session_id']=='2026-09-21-regular' and p['dossier']=='journal/2026-09-21/entry.json'
    budget = {key: openrouter.amount(value) for key, value in p['budget'].items()}
    assert budget['closure_usd'] > 0
    assert budget['total_usd'] == budget['initial_usd'] + budget['debate_usd'] + budget['closure_usd']
    assert operation.plan(root,config,'session',NOW+dt.timedelta(days=1))['session_id']==p['session_id']


def test_due_session_requires_proof_of_grok_billed_output_limit(root, config):
    dossier(root, config)
    policies = synthetic_policies(root)
    grok = policies[openrouter.MODELS['spacexai']]
    path = root / grok['evidence_path']
    proof = json.loads(path.read_text())
    grok['verified_billed_output_limits'] = proof['verified_billed_output_limits'] = [4096]
    path.write_bytes(encoded(proof))
    grok['evidence_sha256'] = digest(path.read_bytes())
    config['live_council']['input_bounds'] = policies
    reschedule(root, next_session='2026-09-21T12:00:00Z')
    with pytest.raises(operation.MissingBound, match='Ausgabegrenze einschließlich Reasoning'):
        operation.plan(root, config, 'session', NOW)


@pytest.mark.parametrize(('available', 'ready'), [('6', 'false'), ('20', 'true')])
def test_session_preflight_exposes_funding_gate_without_inference(root, config, monkeypatch, available, ready):
    home = root / 'gremium'
    home.mkdir()
    config['live_council']['input_bounds'] = synthetic_policies(root)
    (home / 'config.json').write_text(json.dumps(config))
    output = root / 'github-output'
    monkeypatch.setenv('GITHUB_OUTPUT', str(output))
    monkeypatch.setenv('OPENROUTER_API_KEY', 'synthetic-key')
    monkeypatch.setattr(preflight, 'HERE', home)
    monkeypatch.setattr(sys, 'argv', ['preflight.py', '--session-budget'])
    monkeypatch.setattr(openrouter_scout, 'key_state', lambda: {'limit_remaining': '20', 'limit': '40'})
    monkeypatch.setattr(openrouter, 'account_credit_remaining', lambda: openrouter.amount(available))
    monkeypatch.setattr(openrouter, 'endpoint_preflight', lambda *a, **kw: None)
    monkeypatch.setattr(openrouter_scout, 'endpoint_check', lambda *a: None)
    def http(method, path):
        assert method == 'GET'
        return b'{}'
    monkeypatch.setattr(openrouter, 'http', http)
    preflight.main()
    assert f'session_budget_ready={ready}' in output.read_text().splitlines()


def test_due_session_without_proof_is_held_before_reservation(root, config):
    config['live_council']['input_bounds'] = {}
    reschedule(root, next_session='2026-09-21T12:00:00Z')
    with pytest.raises(operation.MissingBound):
        operation.plan(root, config, 'session')
    result = operation.inspect_plan(root, config, 'session')
    assert result['status'] == 'held' and result['ready'] is False
    assert 'kein belegter Input-Bound' in result['budget_hold']


@pytest.mark.parametrize('age',[8,-1])
def test_stale_and_future_dossiers_cannot_trigger_session(root,config,age):
    config['live_council']['input_bounds'] = synthetic_policies(root)
    dossier(root, config, (NOW.date()-dt.timedelta(days=age)).isoformat())
    reschedule(root,next_session='2026-09-22T12:00:00Z')
    with pytest.raises(RuntimeError,match='Drei-Scout'):
        operation.plan(root,config,'session',NOW)


def test_partial_paid_attempt_is_not_silently_repeated(root,config):
    reschedule(root,next_research='2026-09-21T06:00:00Z')
    (root/'journal/2026-09-22').mkdir()
    with pytest.raises(RuntimeError,match='Artefakte'):
        operation.plan(root,config,'research',NOW)


def test_durable_reservation_survives_runner_crash_and_rerun(root,config,monkeypatch):
    reschedule(root,next_research='2026-09-21T06:00:00Z')
    task=operation.plan(root,config,'research',NOW)
    operation.reserve(root,task)
    with pytest.raises(RuntimeError,match='begonnener Lauf'):
        operation.plan(root,config,'research',NOW)
    assert operation.plan(root,config,'research',NOW,reserved=True)['ready']
    monkeypatch.setenv('GITHUB_RUN_ATTEMPT','2')
    with pytest.raises(RuntimeError,match='begonnener Lauf'):
        operation.plan(root,config,'research',NOW,reserved=True)
    assert json.loads((root/'schedule.json').read_text())['unknown']=={'keep':True}


def test_failure_hold_and_success_preserve_unknown_schedule_and_rotation(root,config):
    operation.reserve(root,{'kind':'research','due':'2026-09-21T06:00:00Z'})
    operation.block(root,'research','TransportError')
    with pytest.raises(RuntimeError,match='angehalten'):
        operation.plan(root,config,'session',NOW)
    state=json.loads((root/'schedule.json').read_text())
    assert state['unknown']=={'keep':True} and state['council_rotation']['next_index']==1
    state['regular_operation'].pop('blocked')
    (root/'schedule.json').write_text(json.dumps(state))
    operation.finish(root)
    state=json.loads((root/'schedule.json').read_text())
    assert 'inflight' not in state['regular_operation']
    assert state['regular_operation']['last_completed']['owner']=='123.1'
    assert state['council_rotation']['next_index']==1


def test_known_hold_is_non_ready_in_inspection_but_still_blocks_execution(root, config):
    operation.reserve(root, {'kind': 'research', 'due': '2026-09-21T06:00:00Z'})
    operation.block(root, 'research', 'TransportError')
    before = (root / 'schedule.json').read_bytes()
    result = operation.inspect_plan(root, config, 'research')
    assert result['ready'] is False and result['status'] == 'held'
    assert result['blocked']['error_type'] == 'TransportError'
    assert result['inflight']['owner'] == '123.1'
    with pytest.raises(RuntimeError, match='angehalten'):
        operation.plan(root, config, 'research', NOW, reserved=True)
    assert (root / 'schedule.json').read_bytes() == before


def test_plan_only_exports_hold_without_reserving_or_executing(root, config, monkeypatch):
    here = root / 'gremium'
    here.mkdir()
    (here / 'config.json').write_text(json.dumps(config))
    operation.block(root, 'research', 'TransportError')
    before = (root / 'schedule.json').read_bytes()
    monkeypatch.setattr(operation, 'ROOT', root)
    monkeypatch.setattr(operation, 'execute', lambda *args: pytest.fail('Known hold executed'))
    monkeypatch.setenv('GITHUB_OUTPUT', str(root / 'outputs'))
    monkeypatch.setenv('GITHUB_STEP_SUMMARY', str(root / 'summary'))
    operation.main(['--kind', 'research', '--plan-only'])
    assert (root / 'outputs').read_text() == 'ready=false\n'
    assert 'weiterhin angehalten' in (root / 'summary').read_text()
    assert (root / 'schedule.json').read_bytes() == before


def test_session_dispatch_uses_approved_question_not_steward_preparation(root,config,monkeypatch):
    path=dossier(root, config)
    (root/'next-session.json').write_text('{"question":"MUST NOT BE USED"}')
    calls=[]
    def run(command,**kwargs):
        calls.append(command)
        if 'run_session.py' in command[1]:
            (root/'sessions/test-session').mkdir()
        return SimpleNamespace(returncode=0)
    monkeypatch.setattr(operation.subprocess,'run',run)
    monkeypatch.setattr(openrouter_scout,'key_state',lambda:{'limit_remaining':'18.25'})
    monkeypatch.setattr(openrouter,'account_credit_remaining',lambda:openrouter.amount('24'))
    operation.execute(root,config,{'kind':'session','session_id':'test-session',
                                  'dossier':str(path.relative_to(root)), 'budget': {'total_usd':'8.5'}})
    command=calls[0]
    assert '--public-session' in command and '--regular-operation' in command
    assert '--observe-costs' not in command
    assert command[command.index('--question')+1]==config['regular_operation']['question']
    assert command[command.index('--budget-cap')+1]=='7.225'
    assert '--resume' not in command
    assert (root/'sessions/test-session/research-raw/original.json').read_bytes()==b'{"unchanged":true}\n'


@pytest.mark.parametrize(('key_remaining', 'account_remaining'), [('6', '20'), ('20', '6')])
def test_session_cannot_dispatch_if_either_balance_is_too_low(root, config, monkeypatch, key_remaining, account_remaining):
    monkeypatch.setattr(openrouter_scout, 'key_state', lambda: {'limit_remaining': key_remaining})
    monkeypatch.setattr(openrouter, 'account_credit_remaining', lambda: openrouter.amount(account_remaining))
    monkeypatch.setattr(operation.subprocess, 'run', lambda *a, **kw: pytest.fail('Unfunded session dispatched'))
    with pytest.raises(operation.InsufficientBudget, match='vollständige Sitzung'):
        operation.execute(root, config, {'kind': 'session', 'budget': {'total_usd': '8.5'}})


def test_weekly_observe_mode_keeps_strict_contract_without_invented_bound(tmp_path,config,monkeypatch):
    import live_session
    spec=config['live_council']['models'][1]
    seen=[]
    monkeypatch.setattr(openrouter_scout,'key_state',lambda:seen.append('key') or {'limit_remaining':18})
    def call(*args,**kwargs):
        seen.append(kwargs)
        return '```json\n{"convene":false,"convene_rationale":"No material change"}\n```',{}
    monkeypatch.setattr(live_session.openrouter,'call',call)
    live_session.weekly_decision(spec,'s','u',tmp_path,config,1,15,tmp_path,observe_costs=True)
    assert seen[0]=='key' and seen[1]['observe_costs'] is True and seen[1]['input_bound'] is None
    monkeypatch.setattr(live_session.openrouter,'call',lambda *a,**kw:('```json\n{"convene":"false","convene_rationale":"x"}\n```',{}))
    with pytest.raises(SystemExit,match='Boolean'):
        live_session.weekly_decision(spec,'s','u',tmp_path,config,1,15,tmp_path,observe_costs=True)
