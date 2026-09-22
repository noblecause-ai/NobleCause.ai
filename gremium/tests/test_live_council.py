"""Offline evidence for 0.6. Synthetic provider data is never a real B4 proof."""
import copy
import json
import re
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'gremium'))
import council_state as state
import cost_bounds
import live_debate
import live_session
import openrouter
import organizations
import process_config
import run_session
from test_openrouter import SPECS, envelope, stub_http, metadata


def fenced(obj, prose='Begründung.'):
    return prose + '\n```json\n' + json.dumps(obj, ensure_ascii=False) + '\n```'


def vote_payload(name=None):
    name = name or organizations.load_registry(ROOT/'organizations.json')['orgs'][0]['canonical_name']
    return {'confidence':.8, 'recommendations':[{'pillar':p, 'title':'Belegter Testfall',
        'decision':'recommend', 'abstention_reason':None, 'donation_url':'https://example.org/untrusted',
        'organization':name, 'confidence':.8, 'conditional':False, 'reservation':None} for p in 'ABCD']}


def usage(spec):
    text = (json.dumps({'next_model_id':spec['response_format']['json_schema']['schema']['properties']['next_model_id']['enum'][0],
                       'question':'Synthetische Frage'}) if spec.get('response_format') else 'Answer')
    response, gen = envelope(spec,text)
    _, result = openrouter.validate_response(spec,response,gen)
    result['provenance'].update(raw_artifact='raw/test-response.json',generation_artifact='raw/test-generation.json')
    return result


def synthetic_policies(tmp_path, specs=SPECS):
    policies = {}
    for spec in specs:
        proof = {'model':spec['model'], 'endpoint':spec['openrouter']['endpoint'],
                 'quantization':spec['openrouter']['quantization'], 'max_request_bytes':200000,
                 'input_tokens':20000, 'review_reference':'SYNTHETIC TEST ONLY', 'covers_message_framing':True}
        p=tmp_path/f"synthetic-{spec['family']}.json"
        p.write_bytes(state.encoded(proof))
        policies[spec['model']]={**proof,'basis':'reviewed_provider_envelope','evidence_path':p.name,
                                 'evidence_sha256':state.digest(p.read_bytes())}
    return policies


class FakeCalls:
    instances=[]
    def __init__(self, directory=None, events=None, budget=None, fx=None):
        self.calls=[]
        self.budget=budget
        self.instances.append(self)

    def run(self,spec,system,user,phase,step,limit,remaining):
        self.calls.append((spec,system,user,phase,step,remaining))
        if step.startswith('initial'):
            text=fenced(vote_payload(), 'Unabhängiges Erstvotum ' + spec['model'])
        elif step.startswith('chair-'):
            allowed=json.loads(user.rsplit('Zulässige nächste Redner: ',1)[1])
            text=json.dumps({'next_model_id':allowed[-1], 'question':f'Frage {step}?'})
        elif step.startswith('speech-'):
            other=next(s['model'] for s in SPECS if s['model']!=spec['model'])
            text=fenced({'addressees':[other], 'objection':True, 'reply_to':[]}, 'Einwand ' + step)
        elif step.startswith('final-'):
            obligations=json.loads(user.rsplit('Einzeln zu beantwortende Einwände (Ereignisnummern): ',1)[1])
            text=fenced({**vote_payload(),'objections':{'assessment':'Alle Einwände geprüft.',
                'answers':[{'event_seq':n,'response':'Ich präzisiere die Quellenlage.'} for n in obligations]}},
                '## Einwände\nIch beantworte die Einwände ausdrücklich.\n## Dissens\nSchlussposition '+spec['model'])
        else:
            text=fenced({'summary':'Synthetische Zusammenfassung.','dissent_highlights':['Quellenlage bleibt unsicher.']})
        return text,usage(spec)

    def costs(self):
        return {'currency':'EUR','total':0,'fx_rate_usd_eur':.85,'by_model':[]}


def conduct(tmp_path, caller=None, **options):
    events=state.Events(tmp_path/'events.json','synthetic')
    caller=caller or FakeCalls()
    limits=json.loads((ROOT/'gremium/config.json').read_text())['live_council']['output_limits']
    result=live_debate.conduct(SPECS,SPECS[0],'GLEICHE BELEGE','SYSTEM',caller,events,limits,**options)
    return result,caller,events


def test_sequential_shared_context_independent_votes_and_fair_chair(tmp_path):
    result,caller,events=conduct(tmp_path)
    assert len(caller.calls)==31
    initial=[c for c in caller.calls if c[4].startswith('initial-')]
    assert len({c[2] for c in initial})==1
    speeches=[c for c in caller.calls if c[4].startswith('speech-')]
    for i,c in enumerate(speeches):
        for j in range(i):
            assert f'Einwand speech-{j}' in c[2]
        assert f'Einwand speech-{i}' not in c[2]
    counts={s['model']:sum(c[0]['model']==s['model'] for c in speeches) for s in SPECS}
    assert set(counts.values())=={2}
    finals=[c for c in caller.calls if c[4].startswith('final-')]
    for c in finals:
        assert 'Einwand speech-9' in c[2]
        assert 'Schlussposition' not in c[2]
    assert len(result['rounds'][-1]['votes'])==5
    assert all(r['convergence']['count']==5 for r in result['recommendations'])
    state.validate_events(events.record)


def test_chair_cannot_grant_extra_turn_or_invent_a_member(tmp_path):
    class BadChair(FakeCalls):
        def run(self,*args):
            if args[4]=='chair-0':
                return fenced({'next_model_id':'sixth-seat','question':'x'}),usage(SPECS[0])
            return super().run(*args)
    caller=BadChair()
    with pytest.raises(ValueError,match='Wortvergabe'):
        conduct(tmp_path,caller)
    assert len(caller.calls)==5


def test_self_address_is_retained_as_observation_without_reassigning_speaker(tmp_path):
    originals=[]
    class SelfAddress(FakeCalls):
        def run(self,*args):
            text,u=super().run(*args)
            if args[4]=='speech-0':
                text=fenced({'addressees':[args[0]['model']], 'objection':True, 'reply_to':[]},
                            'Ich widerspreche GLM, obwohl ich hier selbst auf diesem Sitz spreche.')
                originals.append(text)
            return text,u
    result,caller,events=conduct(tmp_path,SelfAddress())
    first=next(e for e in events.record['events'] if e['kind']=='contribution')
    assert first['model']==SPECS[-1]['model'] and first['content_md']==originals[0]
    assert first['data']['addressees']==[first['model']]
    assert first['data']['identity_observation']=={'kind':'self_addressed_contribution',
        'actual_speaker':first['model'],'self_addressed':True}
    final=next(c for c in caller.calls if c[4].startswith('final-') and c[0]['model']==first['model'])
    assert first['seq'] in json.loads(final[2].rsplit('Einzeln zu beantwortende Einwände (Ereignisnummern): ',1)[1])
    assert len(caller.calls)==31 and len(result['rounds'][-1]['votes'])==5
    assert sum(c[0]['model']==first['model'] for c in caller.calls if c[4].startswith('speech-'))==2


def test_budget_closes_debate_but_keeps_five_final_votes(tmp_path):
    class ShortBudget(FakeCalls):
        def run(self,*args):
            if args[4]=='chair-2':
                raise cost_bounds.InsufficientBudget('reserve')
            return super().run(*args)
    result,caller,events=conduct(tmp_path,ShortBudget())
    assert len([c for c in caller.calls if c[4].startswith('speech-')])==2
    assert len(result['rounds'][-1]['votes'])==5
    assert next(e for e in events.record['events'] if e['kind']=='debate_closed')['data']['reason']=='closure_budget_reserved'


def test_oversized_speech_stops_without_truncation_or_repair(tmp_path):
    class LongSpeech(FakeCalls):
        def run(self,*args):
            text,u=super().run(*args)
            if args[4]=='speech-0':
                text=fenced({'addressees':[],'objection':False,'reply_to':[]},' '.join(['Wort']*181))
            return text,u
    caller=LongSpeech()
    with pytest.raises(ValueError,match='180 Wörtern'):
        conduct(tmp_path,caller)
    assert len(caller.calls)==7


@pytest.mark.parametrize('count', [186, 200, 201])
def test_session_amendment_records_small_overrun_and_retains_hard_ceiling(tmp_path, count):
    original = fenced({'addressees':[], 'objection':False, 'reply_to':[]}, ' '.join(['Wort']*count))
    class LongSpeech(FakeCalls):
        def run(self, *args):
            text, u = super().run(*args)
            return (original if args[4]=='speech-0' else text), u
    caller = LongSpeech()
    amendment = {'max_words':200, 'amendment_version':'0.6-speech-limit-1', 'sha256':'documented'}
    if count > 200:
        with pytest.raises(ValueError, match='180 Wörtern'):
            conduct(tmp_path, caller, speech_amendment=amendment)
        assert len(caller.calls)==7
    else:
        result, caller, events = conduct(tmp_path, caller, speech_amendment=amendment)
        contribution = next(e for e in events.record['events'] if e['kind']=='contribution')
        assert contribution['content_md']==original
        assert contribution['data']['word_limit_observation']['word_count']==count
        assert len([c for c in caller.calls if c[4].startswith('speech-')])==10
        assert len(result['rounds'][-1]['votes'])==5


@pytest.mark.parametrize('case', ['no_section','no_assessment','missing_answer','section_after_vote'])
def test_final_without_objection_answer_is_incomplete(case):
    obj={**vote_payload(),'objections':{'assessment':'Prüfung','answers':[{'event_seq':7,'response':'Antwort'}]}}
    prose='## Einwände\nIch antworte begründet.\n## Dissens\nKeine Änderung.'
    if case=='no_section':prose='Nur eine Empfehlung.'
    if case=='section_after_vote':prose='Meine Empfehlung steht schon fest.\n'+prose
    if case=='no_assessment':obj['objections']['assessment']=''
    if case=='missing_answer':obj['objections']['answers']=[]
    with pytest.raises(ValueError,match='Einw[aä]nd'):
        live_debate.vote(fenced(obj,prose),SPECS,SPECS[0],final=True,objections=[7])


@pytest.mark.parametrize('distribution,expected', [([0,0,1,2,3],False),([0,0,1,1,2],False),([0,0,0,1,2],True)])
def test_versioned_three_of_five_rule(distribution,expected):
    orgs=organizations.load_registry(ROOT/'organizations.json')['orgs']
    votes=[{'label':f'm{i}','parsed':vote_payload(orgs[n]['canonical_name'])} for i,n in enumerate(distribution)]
    recs,_=run_session.aggregate_recommendations(votes,procedure_version='0.6')
    assert all(r['has_consensus'] is expected for r in recs)
    if expected:assert recs[0]['convergence']['total']==5
    if distribution==[0,0,1,2,3]:
        assert run_session.aggregate_recommendations(votes)[0][0]['has_consensus'] is True


def test_invalid_votes_do_not_reduce_the_denominator():
    votes=[{'label':f'm{i}','parsed':vote_payload() if i<2 else None} for i in range(5)]
    recs,_=run_session.aggregate_recommendations(votes,procedure_version='0.6')
    assert not recs[0]['has_consensus'] and recs[0]['votes_invalid']==3


def test_event_append_only_gap_tamper_and_mirror(tmp_path):
    events=state.Events(tmp_path/'events.json','test')
    a=events.append('started','setup')
    b=events.once('speech','contribution','debate',model=SPECS[0]['model'],role='member',text='Wörtlich: ä\n')
    snapshot=copy.deepcopy(events.record)
    events.mirror(tmp_path/'public/events.json')
    events.append('aborted','terminal',data={'cause':'synthetic'})
    events.mirror(tmp_path/'public/events.json')
    assert events.record['events'][:2]==snapshot['events']
    assert events.once('speech','contribution','debate',model=SPECS[0]['model'],role='member',text='Wörtlich: ä\n')==b
    with pytest.raises(ValueError,match='umschreiben'):
        events.once('speech','contribution','debate',text='changed')
    for field,value in [('seq',5),('content_md','changed')]:
        bad=copy.deepcopy(snapshot);bad['events'][1][field]=value
        with pytest.raises(ValueError):state.validate_events(bad)
    state.atomic_write(events.path,state.encoded(snapshot))
    old=state.Events(events.path,'test')
    with pytest.raises(ValueError,match='ersetzt'):
        old.mirror(tmp_path/'public/events.json')


def test_missing_bound_and_changed_evidence_block_before_call(tmp_path):
    bound=cost_bounds.InputBounds({},tmp_path)
    with pytest.raises(cost_bounds.MissingBound):bound.policy(SPECS[0])
    policies=synthetic_policies(tmp_path)
    bound=cost_bounds.InputBounds(policies,tmp_path)
    budget=cost_bounds.Budget('1',bound)
    request=openrouter.request_for(SPECS[0],'s','u',2000)
    # A next call alone fits, but its mandatory closure does not.
    with pytest.raises(cost_bounds.InsufficientBudget):
        budget.check(SPECS[0],request,2000,[(SPECS[0],32768)])
    (tmp_path/policies[SPECS[0]['model']]['evidence_path']).write_text('{}')
    with pytest.raises(cost_bounds.MissingBound):bound.tokens(SPECS[0],request)


def test_cached_calls_never_repeat_inference_and_reject_changed_request(tmp_path,monkeypatch):
    policies=synthetic_policies(tmp_path)
    bound=cost_bounds.InputBounds(policies,tmp_path)
    events=state.Events(tmp_path/'events.json','resume')
    calls=stub_http(monkeypatch,SPECS[0])
    runner=live_session.Calls(tmp_path,events,cost_bounds.Budget(10,bound),openrouter.amount('.85'))
    text,first=runner.run(SPECS[0],'s','u','initial','initial-0',2000,[])
    second=live_session.Calls(tmp_path,events,cost_bounds.Budget(10,bound),openrouter.amount('.85'))
    assert second.run(SPECS[0],'s','u','initial','initial-0',2000,[])[1]==first
    assert sum(c[0]=='POST' for c in calls)==1
    assert second.budget.spent==openrouter.amount(first['billed_usd'])
    with pytest.raises(ValueError,match='verändert'):
        second.run(SPECS[0],'s','different','initial','initial-0',2000,[])
    result=tmp_path/'initial-0-anthropic-result.json'
    result.unlink()  # Response exists, but billing was not confirmed durably.
    with pytest.raises(openrouter.OpenRouterError,match='keine erneute Inferenz'):
        second.run(SPECS[0],'s','u','initial','initial-0',2000,[])
    assert sum(c[0]=='POST' for c in calls)==1


def test_canonical_model_and_delayed_accounting_only_repeat_reads(tmp_path,monkeypatch):
    spec=SPECS[2];r,g=envelope(spec)
    r['choices'][0]['native_finish_reason']='completed';g['data']['native_finish_reason']='completed'
    g['data']['model']='canonical-dated-grok'
    base=stub_http(monkeypatch,spec,r,g)
    original=openrouter.http;attempts=[]
    def http(method,path,payload=None):
        if path=='/models':
            data=json.loads(original(method,path,payload));data['data'][0]['canonical_slug']='canonical-dated-grok'
            return json.dumps(data).encode()
        if path.startswith('/generation'):
            attempts.append(path)
            if len(attempts)==1:return b'{"error":{"code":404}}'
        return original(method,path,payload)
    monkeypatch.setattr(openrouter,'http',http);monkeypatch.setattr(openrouter.time,'sleep',lambda _:None)
    text,u=openrouter.call(spec,'s','u',2000,tmp_path,'once',spent_eur=0,cap_eur=15,fx=.85)
    assert u['provenance']['generation_model']=='canonical-dated-grok'
    assert len(attempts)==2 and sum(c[0]=='POST' for c in base)==1


def setup_run(tmp_path,monkeypatch):
    cfg=json.loads((ROOT/'gremium/config.json').read_text())
    (tmp_path/'gremium').mkdir()
    for name in ['manifest.md','schedule.json','organizations.json']:
        shutil.copyfile(ROOT/name,tmp_path/name)
    (tmp_path/'gremium/sources.md').write_text('Öffentliche Belege')
    (tmp_path/'sessions').mkdir()
    cfg['live_council']['input_bounds']=synthetic_policies(tmp_path)
    dossier=tmp_path/'dossier.json'
    dossier.write_text(json.dumps({'date':live_session.datetime.date.today().isoformat(),'research_mode':'blind_then_compare',
        'scouts':[{'model':s['model'],'findings':[{'topic':'Evidence'}],'research_provenance':{'query_log_complete':False}} for s in cfg['scouts']]}))
    args=SimpleNamespace(dossier_json=str(dossier),session_id='test',output_dir=str(tmp_path/'runs'),resume=False,
                         question='Testfrage',title='Testtitel',budget_cap=15)
    monkeypatch.setattr(live_session,'load_env',lambda *a:None)
    monkeypatch.setattr(live_session,'require_keys',lambda *a:None)
    monkeypatch.setattr(openrouter,'preflight',lambda *a:None)
    monkeypatch.setattr(live_session,'Calls',FakeCalls)
    return cfg,args


def test_full_backend_record_byte_equality_rotation_and_resume(tmp_path,monkeypatch):
    cfg,args=setup_run(tmp_path,monkeypatch)
    schedule=json.loads((tmp_path/'schedule.json').read_text())
    schedule['council_rotation']={'procedure_version':'0.6','next_index':0,'custom':'keep'}
    (tmp_path/'schedule.json').write_text(json.dumps(schedule))
    before=(tmp_path/'schedule.json').read_bytes()
    record=live_session.run(tmp_path,cfg,args)
    directory=tmp_path/'runs/test'
    assert state.validate_record(directory)==record
    assert record['chair']['model']==SPECS[0]['model']
    assert (tmp_path/'schedule.json').read_bytes()==before
    with pytest.raises(ValueError,match='Probelauf'):state.accept_session(tmp_path,directory,cfg)
    args.resume=True
    n=len(FakeCalls.instances)
    assert live_session.run(tmp_path,cfg,args)==record
    assert len(FakeCalls.instances)==n
    # Explicit acceptance of a synthetic non-dry-run; no publication occurs.
    record['dry_run']=False
    state.atomic_write(directory/'session.json',state.encoded(record))
    assert state.accept_session(tmp_path,directory,cfg) is True
    assert state.accept_session(tmp_path,directory,cfg) is False
    after=json.loads((tmp_path/'schedule.json').read_text())
    assert after['council_rotation']['next_index']==1
    assert after['council_rotation']['custom']=='keep'
    assert state.chair_for(cfg,after)[0]['model']==SPECS[1]['model']
    assert all(after[k]==v for k,v in json.loads(before).items() if k not in ('last_session','next_session','council_rotation'))
    record['rounds'][1]['contributions'][0]['content_md']='changed'
    state.atomic_write(directory/'session.json',state.encoded(record))
    with pytest.raises(ValueError,match='bytegleichen'):state.validate_record(directory)


def test_regular_policy_is_archived_in_start_event_without_changing_prompt(tmp_path,monkeypatch):
    cfg,args=setup_run(tmp_path,monkeypatch)
    args.regular_operation=True
    record=live_session.run(tmp_path,cfg,args)
    directory=tmp_path/'runs/test'
    policy=json.loads((directory/'speech-policy.json').read_text())
    assert policy['amendment_version']=='0.6-speech-limit-2'
    assert policy['max_words']==200 and policy['prompt_limit']==180
    events=json.loads((directory/'events.json').read_text())['events']
    assert events[0]['data']['procedure_amendment']==policy
    assert json.loads((directory/'run-input.json').read_text())['speech_policy']==policy
    assert '180 Wörter' in record['prompts']['speech']
    args.resume=True
    assert live_session.run(tmp_path,cfg,args)==record


def test_failed_final_validation_never_writes_success_record(tmp_path,monkeypatch):
    cfg,args=setup_run(tmp_path,monkeypatch)
    def invalid(*args):
        raise ValueError('Injected cross-file validation failure')
    monkeypatch.setattr(live_session,'validate_record',invalid)
    with pytest.raises(ValueError,match='validation failure'):
        live_session.run(tmp_path,cfg,args)
    directory=tmp_path/'runs/test'
    assert not (directory/'session.json').exists()
    events=json.loads((directory/'events.json').read_text())
    assert events['events'][-1]['kind']=='aborted'
    state.validate_events(events)
    # Retrying finalization keeps the failed attempt and appends a fresh completion.
    monkeypatch.setattr(live_session,'validate_record',state.validate_record)
    args.resume=True
    assert live_session.run(tmp_path,cfg,args)['status']=='completed'
    events=json.loads((directory/'events.json').read_text())
    assert events['events'][-1]['kind']=='completed'
    assert any(e['kind']=='resumed' for e in events['events'])


@pytest.mark.parametrize('index',range(5))
def test_all_five_models_can_hold_weekly_role(index):
    cfg=json.loads((ROOT/'gremium/config.json').read_text());cfg['features']['live_council']['enabled']=True
    cfg['features']['three_scouts']['enabled']=True
    cfg.pop('wart')  # No standing external Wart dependency in the new procedure.
    schedule={'council_rotation':{'procedure_version':'0.6','next_index':index}}
    spec=process_config.configured_wart(cfg,schedule)
    assert spec['model']==SPECS[index]['model'] and spec['role']=='weekly_chair'
    assert len(process_config.configured_scouts(cfg))==3


def test_live_weekly_role_requires_three_blind_scouts():
    cfg=json.loads((ROOT/'gremium/config.json').read_text())
    cfg['features']['three_scouts']['enabled']=False
    cfg['features']['live_council']['enabled']=True
    with pytest.raises(ValueError,match='drei genehmigten'):
        process_config.configured_scouts(cfg)


@pytest.mark.parametrize('value',[True,False,'false',None])
def test_weekly_chair_uses_strict_existing_boolean_contract(value,tmp_path,monkeypatch):
    cfg=json.loads((ROOT/'gremium/config.json').read_text());cfg['live_council']['input_bounds']=synthetic_policies(tmp_path)
    monkeypatch.setattr(openrouter,'call',lambda *a,**kw:(fenced({'convene':value,'convene_rationale':'Begründung'}),usage(SPECS[1])))
    if type(value) is bool:
        assert live_session.weekly_decision(SPECS[1],'s','u',tmp_path,cfg,0,2,tmp_path)[2]['stop_reason']=='end_turn'
    else:
        with pytest.raises(SystemExit):live_session.weekly_decision(SPECS[1],'s','u',tmp_path,cfg,0,2,tmp_path)


def test_weekly_native_refusal_is_preserved_not_a_false_decision(tmp_path,monkeypatch):
    cfg=json.loads((ROOT/'gremium/config.json').read_text());cfg['live_council']['input_bounds']=synthetic_policies(tmp_path)
    spec=SPECS[0]
    response={'model':spec['model'],'provider':spec['openrouter']['provider_name'],
              'choices':[{'native_finish_reason':'refusal','finish_reason':'content_filter'}]}
    raw=state.encoded(response);path=tmp_path/'chair-weekly-anthropic-response.json'
    def refuse(*a,**kw):
        path.write_bytes(raw)
        raise openrouter.OpenRouterError('billing unavailable')
    monkeypatch.setattr(openrouter,'call',refuse)
    with pytest.raises(live_session.WeeklyRefusal):
        live_session.weekly_decision(spec,'s','u',tmp_path,cfg,0,2,tmp_path)
    assert path.read_bytes()==raw


@pytest.mark.parametrize('observe',[False,True])
def test_complete_transport_resume_after_paid_reply_without_double_charge(tmp_path,monkeypatch,observe):
    real_calls=live_session.Calls
    cfg,args=setup_run(tmp_path,monkeypatch)
    args.observe_costs=observe
    if observe:
        cfg['live_council']['input_bounds']={}
    monkeypatch.setattr(live_session,'Calls',real_calls)
    monkeypatch.setattr(openrouter,'endpoint_preflight',metadata)
    generator=FakeCalls(); generations={}; posted=[]; counters={}
    def http(method,path,payload=None):
        if path=='/key':return b'{"data":{"limit":10,"limit_remaining":10,"limit_reset":null}}'
        if path.startswith('/generation?id='):
            return json.dumps(generations[path.split('=')[1]]).encode()
        assert method=='POST' and path=='/chat/completions'
        spec=next(s for s in SPECS if s['model']==payload['model'])
        system,user=[m['content'] for m in payload['messages']]
        if system==live_debate.CHAIR_SYSTEM:prefix='chair'
        elif live_debate.FINAL_TASK in user:prefix='final'
        elif live_debate.SPEECH_TASK in user:prefix='speech'
        elif live_debate.SUMMARY_TASK in user:prefix='summary'
        else:prefix='initial'
        index=counters.get(prefix,0);counters[prefix]=index+1
        step='summary' if prefix=='summary' else f'{prefix}-{index}'
        text,_=generator.run(spec,system,user,prefix,step,8192,[])
        r,g=envelope(spec,text)
        gid=f'gen-{len(posted)+1}';r['id']=gid;g['data']['id']=gid;generations[gid]=g
        posted.append(payload)
        return json.dumps(r).encode()
    monkeypatch.setattr(openrouter,'http',http)
    if observe:
        args.stop_after_first=True
        checkpoint=live_session.run(tmp_path,cfg,args)
        assert checkpoint['status']=='initial_ready' and len(posted)==1
        assert not (tmp_path/'runs/test/session.json').exists()
        feed=json.loads((tmp_path/'runs/test/events.json').read_text())['events']
        assert feed[-1]['kind']=='checkpoint' and not any(e['kind']=='initial_votes' for e in feed)
        args.stop_after_first=False
        args.resume=True
    original=state.Events.once
    tripped=[]
    def interrupt_after_reply(self,key,*a,**kw):
        if key=='contribution-2' and not tripped:
            tripped.append(True)
            raise RuntimeError('Simulated crash after persisted paid response, before event')
        return original(self,key,*a,**kw)
    monkeypatch.setattr(state.Events,'once',interrupt_after_reply)
    with pytest.raises(RuntimeError):live_session.run(tmp_path,cfg,args)
    charged_before=len(posted)
    assert charged_before==11
    args.resume=True
    record=live_session.run(tmp_path,cfg,args)
    assert len(posted)==31
    assert len(set(json.dumps(p,sort_keys=True) for p in posted))==31
    assert record['costs']['total']==pytest.approx(31*.002*.85)
    assert state.validate_record(tmp_path/'runs/test')==record
    assert any(e['kind']=='aborted' for e in json.loads((tmp_path/'runs/test/events.json').read_text())['events'])
    # The versioned replay must reproduce the original tally, including its wording.
    import reaggregate
    votes=reaggregate.final_votes_from_raw(tmp_path/'runs/test',record)
    recs,unresolved=run_session.aggregate_recommendations(votes,procedure_version=record['procedure_version'],
        ballot_contract=record['ballot_contract'])
    assert recs==record['recommendations'] and unresolved==record['unresolved_votes']
    costs=json.loads((tmp_path/'runs/test/costs-live.json').read_text())
    assert sum(t['calls'] for t in costs['totals_by_model'])==31
    assert costs['total_usd']==str(openrouter.amount('.002')*31)
    assert record['cost_mode']==('observe' if observe else 'bounded')
    moderation=[c for c in costs['totals_by_model_role'] if c['role']=='moderation']
    assert len(moderation)==1 and moderation[0]['calls']==10
    assert sum(c['calls'] for c in costs['totals_by_model_role'])==31
    assert all(e['reasoning_effort']=='low' for e in costs['by_model'] if e['role']=='moderation')
    assert all(p['reasoning']['effort']=='low' for p in posted if p['messages'][0]['content']==live_debate.CHAIR_SYSTEM)
    assert posted[0]['reasoning']['effort']=='medium'
    # Every stateless role receives the actual constitution and the common
    # persona, while only initial votes receive the independent-vote task.
    manifest=(tmp_path/'manifest.md').read_text()
    for index,payload in enumerate(posted):
        system,user=[m['content'] for m in payload['messages']]
        assert system.startswith(live_session.prompts.SYSTEM)
        assert user.count(manifest)==1
        assert (live_session.prompts.LIVE_INITIAL_TASK in user)==(index<5)
    assert live_session.prompts.LIVE_VOTE_FORMAT in posted[-2]['messages'][1]['content']
    assert record['prompts']['initial']==posted[0]['messages'][1]['content']
    assert record['prompts']['summary']==live_debate.SUMMARY_TASK
    steering=[p for p in posted if p['messages'][0]['content']==live_debate.CHAIR_SYSTEM]
    assert len(steering)==10
    for payload in steering:
        allowed=json.loads(payload['messages'][1]['content'].rsplit('Zulässige nächste Redner: ',1)[1])
        assert payload['response_format']==live_debate.chair_response_format(allowed)
    assert all('response_format' not in p for p in posted if p not in steering)


def test_compact_context_keeps_evidence_and_reservations_without_technical_dump():
    from council_context import compact_context
    finding={'pillar':'A','topic':'Unchanged topic','summary':'Quantitative evidence: 42%',
             'source':'https://example.test/study','uncertainty':'small sample','counterevidence':'failed replication'}
    report={'model':'scout','content_md':'Original prose','findings':[finding],
            'rejected_findings':[{'topic':'Rejected','reason':'Bad source'}], 'search_queries':['query'],
            'research_provenance':{'generation_id':'MUST_NOT_ENTER','query_log_complete':False,
                'citations':[{'url':finding['source'],'title':'source','start_index':100}],
                'warnings':['Incomplete search log']}}
    prior={'id':'previous','date':'2026-09-01','recommendations':[{'pillar':'A','title':'Prior title',
           'organization':'Org','convergence':{'count':2,'total':3,'conditional_count':1,
             'votes':[{'model':'one','conditional':True,'reservation':'Mandatory caveat'}]}}]}
    compact=compact_context({'date':'2026-09-20','scouts':[report]},prior)
    data=json.loads(compact)
    assert data['scouts'][0]['findings']==[finding]
    assert data['scouts'][0]['rejected_findings']==report['rejected_findings']
    assert data['scouts'][0]['content_md']=='Original prose'
    assert data['scouts'][0]['source_disclosure']['finding_sources_in_api_citations']==[finding['source']]
    assert 'Mandatory caveat' in compact and 'MUST_NOT_ENTER' not in compact
    assert data['scouts'][0]['search_queries_self_reported']==['query']


def test_explicit_azure_completed_revalidation_is_offline_additive_and_reusable(tmp_path,monkeypatch):
    spec=SPECS[1];response,generation=envelope(spec,fenced(vote_payload()))
    response['choices'][0]['native_finish_reason']='completed'
    generation['data']['native_finish_reason']='completed'
    raw=tmp_path/'raw';raw.mkdir()
    stem='initial-1-openai'
    values={'request':openrouter.request_for(spec,'s','u',16384),'response':response,'generation':generation,
            'endpoint':metadata(spec),'result':{'outcome':'invalid','failure':'Earlier adapter rejected completed','retry_allowed':False}}
    for key,value in values.items():(raw/f'{stem}-{key}.json').write_bytes(state.encoded(value))
    originals={p.name:p.read_bytes() for p in raw.iterdir()}
    def no_network(*args):raise AssertionError('Revalidation must never call a provider')
    monkeypatch.setattr(openrouter,'http',no_network)
    text,usage=live_session.revalidate_saved_call(raw,spec,'initial-1','Azure completed is a verified terminal success')
    assert usage['provenance']['native_finish_reason']=='completed'
    runner=live_session.Calls(raw,state.Events(tmp_path/'events.json','revalidate'),cost_bounds.Budget(4,observe=True),openrouter.amount('.85'))
    assert runner.run(spec,'s','u','initial','initial-1',16384,[])[0]==text
    assert all((raw/name).read_bytes()==value for name,value in originals.items())
    (raw/f'{stem}-result.json').write_text('{}')
    with pytest.raises(ValueError,match='Nachprüfungsbeleg'):
        runner.run(spec,'s','u','initial','initial-1',16384,[])


def test_delayed_generation_receipt_reuses_original_inference_and_detects_tampering(tmp_path,monkeypatch):
    spec=SPECS[3];response,generation=envelope(spec,fenced(vote_payload()))
    raw=tmp_path/'raw';raw.mkdir();stem='initial-3-'+spec['family']
    values={'request':openrouter.request_for(spec,'s','u',16384),'response':response,
            'generation':{'error':{'code':404}},'endpoint':metadata(spec),
            'result':{'outcome':'unavailable','failure':'Generation missing','retry_allowed':False}}
    for key,value in values.items():(raw/f'{stem}-{key}.json').write_bytes(state.encoded(value))
    originals={p.name:p.read_bytes() for p in raw.iterdir()}
    delayed=raw/f'{stem}-generation-delayed-1.json'
    wrong=copy.deepcopy(generation);wrong['data']['id']='gen-other'
    delayed.write_bytes(state.encoded(wrong))
    def no_network(*args):raise AssertionError('No repeat inference or network request allowed')
    monkeypatch.setattr(openrouter,'http',no_network)
    with pytest.raises(openrouter.OpenRouterError,match='generation ID'):
        live_session.revalidate_saved_call(raw,spec,'initial-3','Delayed billing',delayed_generation=delayed)
    delayed.write_bytes(state.encoded(generation))
    text,usage=live_session.revalidate_saved_call(raw,spec,'initial-3','Delayed billing',delayed_generation=delayed)
    assert usage['provenance']['generation_artifact']=='raw/'+delayed.name
    runner=live_session.Calls(raw,state.Events(tmp_path/'events.json','delayed'),cost_bounds.Budget(4,observe=True),openrouter.amount('.85'))
    assert runner.run(spec,'s','u','initial','initial-3',16384,[])[0]==text
    assert all((raw/name).read_bytes()==value for name,value in originals.items())
    delayed.write_bytes(state.encoded(wrong))
    with pytest.raises(ValueError,match='Abrechnungsbeleg verändert'):
        runner.run(spec,'s','u','initial','initial-3',16384,[])


def test_observation_mode_stops_on_actual_cost_and_retains_receipts(tmp_path,monkeypatch):
    spec=SPECS[0]
    stub_http(monkeypatch,spec)
    original=openrouter.http;posts=[]
    def http(method,path,payload=None):
        if path=='/key':return b'{"data":{"limit":10,"limit_remaining":1,"limit_reset":null}}'
        if method=='POST':posts.append(payload)
        return original(method,path,payload)
    monkeypatch.setattr(openrouter,'http',http)
    budget=cost_bounds.Budget('.001',observe=True)
    runner=live_session.Calls(tmp_path,state.Events(tmp_path/'events.json','observe'),budget,openrouter.amount('.85'))
    with pytest.raises(openrouter.OpenRouterError,match='Budget überschritten'):
        runner.run(spec,'s','u','initial','initial-0',2000,[])
    assert len(posts)==1
    assert json.loads((tmp_path/'initial-0-anthropic-result.json').read_text())['outcome']=='valid'
    costs=json.loads((tmp_path.parent/'costs-live.json').read_text())
    assert costs['total_usd']=='0.002'
    with pytest.raises(cost_bounds.InsufficientBudget):
        runner.run(spec,'s','u','initial','initial-1',2000,[])
    assert len(posts)==1


@pytest.mark.parametrize('native,normalized',[('max_tokens','length'),('refusal','content_filter')])
def test_paid_failure_keeps_confirmed_model_costs_without_retry(tmp_path,monkeypatch,native,normalized):
    spec=SPECS[0];response,generation=envelope(spec,'')
    response['choices'][0].update(finish_reason=normalized,native_finish_reason=native)
    generation['data'].update(finish_reason=normalized,native_finish_reason=native)
    calls=stub_http(monkeypatch,spec,response,generation)
    raw=tmp_path/'raw';raw.mkdir()
    budget=cost_bounds.Budget(4,observe=True)
    runner=live_session.Calls(raw,state.Events(tmp_path/'events.json','failed'),budget,openrouter.amount('.85'))
    with pytest.raises(openrouter.OpenRouterError):
        runner.run(spec,'s','u','initial','initial-0',2000,[])
    assert budget.spent==openrouter.amount('.002')
    result=json.loads((raw/'initial-0-anthropic-result.json').read_text())
    assert result['outcome']!='valid' and result['confirmed_usage']['billed_usd']=='0.002'
    costs=json.loads((tmp_path/'costs-live.json').read_text())
    assert costs['total_usd']=='0.002' and costs['by_model'][0]['outcome']!='valid'
    with pytest.raises(openrouter.OpenRouterError,match='keine erneute Inferenz'):
        runner.run(spec,'s','u','initial','initial-0',2000,[])
    assert sum(c[0]=='POST' for c in calls)==1


@pytest.mark.parametrize('mode',['valid','invalid','refusal'])
def test_weekly_runner_chair_result_and_refusal_record(tmp_path,monkeypatch,mode):
    import run_wart
    import jsonschema
    cfg=json.loads((ROOT/'gremium/config.json').read_text())
    cfg['features']['live_council']['enabled']=True;cfg['features']['three_scouts']['enabled']=True
    cfg['live_council']['input_bounds']=synthetic_policies(tmp_path)
    here=tmp_path/'gremium';here.mkdir();(here/'config.json').write_text(json.dumps(cfg))
    (tmp_path/'manifest.md').write_text('SYNTHETIC MANIFEST')
    previous=tmp_path/'sessions/previous';previous.mkdir(parents=True)
    (previous/'session.json').write_text(json.dumps({'id':'previous','number':1,'date':'2026-09-14','question':'historical','recommendations':[]}))
    (tmp_path/'schedule.json').write_text(json.dumps({'custom':'keep','next_session':'2026-10-14T12:00:00Z'}))
    def scout(spec,system,user,directory):
        return (fenced({'findings':[{'pillar':'A','topic':'finding','source':'https://example.test'}],
                        'rejected_findings':[],'search_queries':[],'delta_assessment':'Current evidence'}),
                {'input_tokens':1,'output_tokens':1,'billed_usd':'0.002'}, {'stop_reason':'end_turn'}, [])
    def council(spec,system,user,limit,directory,tag,**kw):
        if mode=='refusal':
            (directory/f'{tag}-{spec["family"]}-response.json').write_text(json.dumps({
                'model':spec['model'],'provider':spec['openrouter']['provider_name'],
                'choices':[{'native_finish_reason':'refusal'}]}))
            raise openrouter.OpenRouterError('Native refusal','refusal')
        value='false' if mode=='invalid' else False
        return fenced({'convene':value,'convene_rationale':'No material change'}),usage(spec)
    monkeypatch.setattr(run_wart,'ROOT',tmp_path);monkeypatch.setattr(run_wart,'HERE',here)
    monkeypatch.setattr(run_wart,'load_env',lambda *a:None);monkeypatch.setattr(run_wart,'require_keys',lambda *a:None)
    monkeypatch.setattr(run_wart,'call_scout',scout);monkeypatch.setattr(openrouter,'call',council)
    monkeypatch.setattr(sys,'argv',['run_wart.py','--date','2026-09-20'])
    if mode=='invalid':
        with pytest.raises(SystemExit,match='Boolean'):run_wart.main()
        assert not (tmp_path/'journal/2026-09-20/entry.json').exists()
        return
    run_wart.main()
    entry=json.loads((tmp_path/'journal/2026-09-20/entry.json').read_text())
    jsonschema.validate(entry,json.loads((ROOT/'schema/journal.schema.json').read_text()))
    assert entry['decision_role']=='weekly_chair'
    assert entry['decision_model']==SPECS[0]['model']
    if mode=='refusal':assert entry['kind']=='refusal' and 'convene' not in entry
    else:assert entry['convene'] is False
    assert json.loads((tmp_path/'schedule.json').read_text())['custom']=='keep'
