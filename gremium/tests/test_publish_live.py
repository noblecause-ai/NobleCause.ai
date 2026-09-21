"""Offline tests for publication order, retention and fail-before-inference."""
import copy
import json
import shutil
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'gremium'))
import council_state as state
import cost_bounds
import live_session
import openrouter
import publish_live as public
from test_live_council import setup_run, SPECS


def descriptor(session_id='synthetic'):
    return {'id': session_id, 'number': 6, 'date': '2026-09-21', 'title': 'Synthetischer Test',
            'question': 'Testfrage', 'chair': {'model': SPECS[0]['model'], 'rotation_index': 0},
            'config': {'models': SPECS}, 'secret': 'MUST NOT LEAK', 'prompts': 'PRIVATE PROMPT'}


def setup(tmp_path):
    meta = public.public_session(descriptor())
    sink = public.FilePublisher(tmp_path / 'public', meta, mode='replay')
    events = state.Events(tmp_path / 'local/events.json', meta['id'], publisher=sink)
    return sink, events


def test_atomic_archive_and_current_keep_original_words_and_prefix(tmp_path):
    sink, events = setup(tmp_path)
    events.append('started', 'setup')
    initial = (tmp_path / 'public/current.json').read_bytes()
    first = json.loads(initial)['record']['events'][0]
    words = 'Eine wörtliche Äußerung.\n\n**Kein Ersatztext.**'
    events.append('contribution', 'debate', model=SPECS[2]['model'], role='member', text=words)
    current = json.loads((tmp_path / 'public/current.json').read_text())
    assert current['record']['events'][0] == first
    assert current['record']['events'][-1]['content_md'].encode() == words.encode()
    assert (tmp_path / 'public/sessions/synthetic/events.json').read_bytes() == events.path.read_bytes()
    assert (tmp_path / 'public/sessions/synthetic/snapshot.json').read_bytes() == (tmp_path / 'public/current.json').read_bytes()
    assert 'secret' not in current['session'] and 'prompts' not in current['session']
    with pytest.raises(public.PublicationError):
        sink(json.loads(initial)['record'])


def test_changed_validly_rehashed_event_is_not_allowed(tmp_path):
    sink, events = setup(tmp_path)
    events.append('started', 'setup')
    altered = copy.deepcopy(events.record)
    e = altered['events'][0]
    e['content_md'] = 'changed'
    e['content_sha256'] = state.digest(e['content_md'].encode())
    e['sha256'] = state.digest({k: v for k, v in e.items() if k != 'sha256'})
    state.validate_events(altered)
    with pytest.raises(public.PublicationError):
        sink(altered)


def test_closed_session_is_retained_when_next_session_begins(tmp_path):
    sink, events = setup(tmp_path)
    events.append('started', 'setup')
    other = public.FilePublisher(tmp_path/'public', public.public_session(descriptor('next')), mode='replay')
    new_events = state.Events(tmp_path/'next/events.json', 'next')
    new_events.append('started', 'setup')
    with pytest.raises(public.PublicationError): other(new_events.record)
    events.append('aborted', 'terminal')
    old = (tmp_path/'public/sessions/synthetic/events.json').read_bytes()
    other = public.FilePublisher(tmp_path/'public', public.public_session(descriptor('next')), mode='replay')
    other(new_events.record)
    assert (tmp_path/'public/sessions/synthetic/events.json').read_bytes() == old
    assert json.loads((tmp_path/'public/current.json').read_text())['session']['id'] == 'next'


def test_partial_publication_failure_retains_local_event_and_latches(tmp_path, monkeypatch):
    sink, events = setup(tmp_path)
    events.append('started', 'setup')
    before = (tmp_path/'public/current.json').read_bytes()
    write = public.atomic_write
    def fail_current(path, payload, **kwargs):
        if path.name == 'current.json': raise OSError('unavailable')
        write(path, payload, **kwargs)
    monkeypatch.setattr(public, 'atomic_write', fail_current)
    with pytest.raises(public.PublicationError): events.append('aborted', 'terminal')
    assert json.loads(events.path.read_text())['events'][-1]['kind'] == 'aborted'
    assert (tmp_path/'public/current.json').read_bytes() == before
    monkeypatch.setattr(public, 'atomic_write', write)
    with pytest.raises(public.PublicationError): events.publish()
    # An explicitly resumed publisher may finish publishing the retained prefix.
    restored = public.FilePublisher(tmp_path/'public', sink.session, mode='replay')
    restored(events.record)
    assert json.loads((tmp_path/'public/current.json').read_text())['record'] == events.record


def test_heartbeat_failure_is_observed_before_next_call(tmp_path, monkeypatch):
    sink, events = setup(tmp_path)
    events.append('started', 'setup')
    attempted = threading.Event()
    def fail(_record):
        attempted.set()
        raise OSError('heartbeat publication failed')
    monkeypatch.setattr(sink, '_write', fail)
    sink.start(interval=.01)
    assert attempted.wait(2)
    sink.close()
    with pytest.raises(public.PublicationError): events.publish()


def test_publication_failure_prevents_paid_inference(tmp_path, monkeypatch):
    def failure(_record): raise public.PublicationError('offline')
    events = state.Events(tmp_path/'events.json', 'synthetic', publisher=failure)
    monkeypatch.setattr(openrouter, 'http', lambda *a: b'{"data":{"limit":20,"limit_remaining":10,"limit_reset":null}}')
    def no_call(*a, **kw): pytest.fail('Inference must not run after a publication failure')
    monkeypatch.setattr(openrouter, 'call', no_call)
    calls = live_session.Calls(tmp_path/'raw', events, cost_bounds.Budget(10, observe=True), openrouter.amount('.85'))
    with pytest.raises(public.PublicationError): calls.run(SPECS[0], 's', 'u', 'initial', 'initial-0', 2000, [])


def test_costs_are_evidenced_deduplicated_and_withheld_votes_stay_hidden(tmp_path):
    sink, events = setup(tmp_path)
    events.append('waiting', 'initial', model=SPECS[0]['model'], role='member', data={'spent_usd': '0.4'})
    snapshot = json.loads((tmp_path/'public/current.json').read_text())
    assert snapshot['costs']['total_usd'] == '0.4'
    assert snapshot['costs']['by_model'] == []
    assert not any('votes' in e['data'] for e in snapshot['record']['events'])
    proof = {'cost_basis': 'billed', 'cost': .2, 'generation_id': 'unique'}
    for _ in range(2):
        events.append('contribution', 'debate', model=SPECS[0]['model'], role='member', text='Wortlaut', data={'provenance': proof})
    costs = public.public_costs(events.record)
    assert costs['by_model'] == [{'model': SPECS[0]['model'], 'usd': '0.2'}]
    assert costs['unassigned_usd'] == '0.2'


def test_full_runner_publishes_only_completed_vote_groups(tmp_path, monkeypatch):
    config, args = setup_run(tmp_path, monkeypatch)
    shutil.copyfile(ROOT/'models.json', tmp_path/'models.json')
    args.live_feed_dir = str(tmp_path/'public')
    session = live_session.run(tmp_path, config, args)
    snapshot = json.loads((tmp_path/'public/current.json').read_text())
    assert snapshot['mode'] == 'pilot'
    assert snapshot['record']['events'][-1]['kind'] == 'completed'
    reveals = [e for e in snapshot['record']['events'] if e['kind'] in ('initial_votes', 'final_votes')]
    assert [len(e['data']['votes']) for e in reveals] == [5, 5]
    assert (tmp_path/'public/sessions/test/events.json').read_bytes() == (tmp_path/'runs/test/events.json').read_bytes()
    assert session['dry_run'] is True


@pytest.mark.parametrize('session_id', ['../bad', '/bad', '', 'two/parts'])
def test_public_session_rejects_unsafe_paths(session_id):
    with pytest.raises(ValueError): public.public_session(descriptor(session_id))


@pytest.mark.parametrize('path', ['.', 'sessions', 'journal/feed', 'commissions/feed', 'site/static/live', '.review/source'])
def test_destination_cannot_overwrite_source_or_published_records(path, tmp_path):
    with pytest.raises(ValueError):
        public.validate_destination(tmp_path/path, tmp_path/'.review/source', tmp_path)


def test_previous_writer_cannot_reclaim_current_after_next_session(tmp_path):
    old, events = setup(tmp_path)
    events.append('completed', 'terminal')
    newer = public.FilePublisher(tmp_path/'public', public.public_session(descriptor('newer')), mode='replay')
    record = state.Events(tmp_path/'newer/events.json', 'newer')
    record.append('completed', 'terminal')
    newer(record.record)
    with pytest.raises(public.PublicationError): old(events.record)


def test_ssh_acknowledgement_and_remote_prefix_are_required(tmp_path, monkeypatch):
    import types
    meta = public.public_session(descriptor())
    source = state.Events(tmp_path/'source/events.json', 'synthetic')
    source.append('started', 'setup')
    sent=[]
    def transport(command, *, input, **kwargs):
        sent.append(command)
        result = public.receive(tmp_path/'remote', json.loads(input))
        return types.SimpleNamespace(stdout=json.dumps(result).encode())
    monkeypatch.setattr(public.subprocess, 'run', transport)
    sink = public.SshPublisher(tmp_path/'local', meta, host='noblecause@example.org')
    sink(source.record)
    assert (tmp_path/'remote/sessions/synthetic/events.json').read_bytes() == source.path.read_bytes()
    assert 'StrictHostKeyChecking=yes' in sent[0]
    other = public.public_session(descriptor('next'))
    source.append('completed', 'terminal')
    sink(source.record)
    next_events=state.Events(tmp_path/'next/events.json','next')
    next_events.append('started','setup')
    public.receive(tmp_path/'remote', {'session':other,'mode':'live','record':next_events.record})
    with pytest.raises(public.PublicationError): sink(source.record)
    assert json.loads((tmp_path/'remote/current.json').read_text())['session']['id'] == 'next'


def test_public_run_requires_own_symbols_and_advances_rotation_only_once(tmp_path, monkeypatch):
    cfg,args=setup_run(tmp_path,monkeypatch)
    args.public_session=True
    args.output_dir=None
    args.live_feed_dir=str(tmp_path/'feed')
    (tmp_path/'models.json').write_text(json.dumps({'models':[]}))
    with pytest.raises(ValueError,match='Medaillon'): live_session.run(tmp_path,cfg,args)
    assert not (tmp_path/'sessions/test').exists()
    symbols=[]
    for i,spec in enumerate(cfg['live_council']['models']):
        asset=f'/media/medallions/test-{i}.avif'
        path=tmp_path/'site/static'/asset.lstrip('/')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(b'synthetic asset')
        symbols.append({'model':spec['model'],'asset':asset,'warden_review':{'decision':'accepted'}})
    (tmp_path/'models.json').write_text(json.dumps({'models':symbols}))
    result=live_session.run(tmp_path,cfg,args)
    assert result['dry_run'] is False
    assert json.loads((tmp_path/'feed/current.json').read_text())['mode']=='live'
    assert state.accept_session(tmp_path,tmp_path/'sessions/test',cfg)
    assert not state.accept_session(tmp_path,tmp_path/'sessions/test',cfg)
    assert json.loads((tmp_path/'schedule.json').read_text())['council_rotation']['next_index']==1
