"""Autonomy tests never send paid calls: due dates, holds and existing adapters."""
import datetime as dt
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'gremium'))
import regular_operation as operation
import openrouter_scout

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


def dossier(root, date='2026-09-21'):
    path=root/'journal'/date/'entry.json';path.parent.mkdir()
    data=json.loads((REPO/'sessions/2026-09-21-live/research.json').read_text())
    data['date']=date
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


def test_due_session_reuses_current_dossier_and_stable_id(root,config):
    dossier(root)
    reschedule(root,next_session='2026-09-21T12:00:00Z')
    p=operation.plan(root,config,'session',NOW)
    assert p['session_id']=='2026-09-21-regular' and p['dossier']=='journal/2026-09-21/entry.json'
    assert operation.plan(root,config,'session',NOW+dt.timedelta(days=1))['session_id']==p['session_id']


@pytest.mark.parametrize('age',[8,-1])
def test_stale_and_future_dossiers_cannot_trigger_session(root,config,age):
    dossier(root,(NOW.date()-dt.timedelta(days=age)).isoformat())
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


def test_session_dispatch_uses_approved_question_not_steward_preparation(root,config,monkeypatch):
    path=dossier(root)
    (root/'next-session.json').write_text('{"question":"MUST NOT BE USED"}')
    calls=[]
    def run(command,**kwargs):
        calls.append(command)
        if 'run_session.py' in command[1]:
            (root/'sessions/test-session').mkdir()
        return SimpleNamespace(returncode=0)
    monkeypatch.setattr(operation.subprocess,'run',run)
    monkeypatch.setattr(openrouter_scout,'key_state',lambda:{'limit_remaining':'18.25'})
    operation.execute(root,config,{'kind':'session','session_id':'test-session','dossier':str(path.relative_to(root))})
    command=calls[0]
    assert '--public-session' in command and '--observe-costs' in command and '--regular-operation' in command
    assert command[command.index('--question')+1]==config['regular_operation']['question']
    assert command[command.index('--budget-cap')+1]=='15.5125'
    assert '--resume' not in command
    assert (root/'sessions/test-session/research-raw/original.json').read_bytes()==b'{"unchanged":true}\n'


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
