"""All HTTP is stubbed. These contracts do not attest real provider behaviour."""
import copy
import json
import sys
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import pytest
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'gremium'))
import openrouter as adapter
import run_session
import run_commission

SPECS = json.loads((ROOT / 'gremium/openrouter-candidates.json').read_text())['models']


def envelope(spec, text='Answer'):
    native = 'end_turn' if spec['family'] == 'anthropic' else 'stop'
    usage = {'prompt_tokens': 10, 'completion_tokens': 20, 'total_tokens': 30, 'cost': 0.002,
             'completion_tokens_details': {'reasoning_tokens': 5}, 'prompt_tokens_details': {'cached_tokens': 0}}
    response = {'id': 'gen-test', 'model': spec['model'], 'provider': spec['openrouter']['provider_name'],
                'choices': [{'finish_reason': 'stop', 'native_finish_reason': native,
                             'message': {'role': 'assistant', 'content': text}}], 'usage': usage}
    generation = {'data': {'id': 'gen-test', 'model': spec['model'], 'provider_name': response['provider'],
                           'finish_reason': 'stop', 'native_finish_reason': native,
                           'native_tokens_prompt': 10, 'native_tokens_completion': 20,
                           'native_tokens_reasoning': 5, 'native_tokens_cached': 0, 'total_cost': .002,
                           'cancelled': False, 'is_byok': False}}
    return response, generation


def metadata(spec):
    c = spec['openrouter']
    return {'tag': c['endpoint'], 'provider_name': c['provider_name'], 'model_id': spec['model'],
            'status': 0, 'quantization': c['quantization'], 'context_length': c['context_length'],
            'max_completion_tokens': c['max_output_tokens'],
            'supported_parameters': ['reasoning', c['token_parameter']],
            'pricing': {k: str(Decimal(str(v)) / 1_000_000) for k, v in c['max_price'].items()}}


def stub_http(monkeypatch, spec, response=None, generation=None, endpoint=None, failure=None):
    resp, gen = envelope(spec)
    resp = resp if response is None else response
    gen = gen if generation is None else generation
    ep = metadata(spec) if endpoint is None else endpoint
    calls = []
    def http(method, path, payload=None):
        calls.append((method, path, payload))
        if path == '/models':
            obj = {'data': [{'id': spec['model'], 'reasoning': {'supported_efforts': [spec['openrouter']['reasoning_effort']]}}]}
        elif path.endswith('/endpoints'):
            obj = {'data': {'id': spec['model'], 'endpoints': [ep]}}
        elif path == '/chat/completions':
            if failure:
                raise failure
            obj = resp
        elif path.startswith('/generation?id='):
            obj = gen
        elif path == '/key':
            obj = {'data': {'limit': 5, 'limit_remaining': 4}}
        elif path == '/credits':
            obj = {'data': {'total_credits': 10, 'total_usage': 2}}
        else:
            raise AssertionError(path)
        return ('  ' + json.dumps(obj) + '\n').encode()
    monkeypatch.setattr(adapter, 'http', http)
    return calls


def structured_chair():
    from live_debate import chair_response_format
    spec={**SPECS[0],'response_format':chair_response_format([SPECS[1]['model']])}
    ep=metadata(spec)
    ep['supported_parameters']+=['response_format','structured_outputs']
    return spec,ep


def test_strict_moderation_preserves_escaped_quotes_and_pins_endpoint(tmp_path,monkeypatch):
    spec,ep=structured_chair()
    text=json.dumps({'next_model_id':SPECS[1]['model'],'question':'Was bedeutet "wirksam" hier?'},ensure_ascii=False)
    response,generation=envelope(spec,text)
    calls=stub_http(monkeypatch,spec,response,generation,endpoint=ep)
    result,usage=adapter.call(spec,'s','u',4096,tmp_path,'chair-0',spent_eur=0,cap_eur=15,fx=.85)
    assert result==text and usage['billed_usd']=='0.002'
    request=next(c[2] for c in calls if c[0]=='POST')
    assert request['response_format']==spec['response_format']
    assert request['provider']['only']==[spec['openrouter']['endpoint']]
    assert request['provider']['require_parameters'] is True and request['provider']['allow_fallbacks'] is False
    assert json.loads((tmp_path/'chair-0-anthropic-response.json').read_bytes())['choices'][0]['message']['content']==text
    assert sum(c[0]=='POST' for c in calls)==1


@pytest.mark.parametrize('missing',['response_format','structured_outputs'])
def test_strict_moderation_unsupported_pin_stops_before_inference(tmp_path,monkeypatch,missing):
    spec,ep=structured_chair();ep['supported_parameters'].remove(missing)
    calls=stub_http(monkeypatch,spec,endpoint=ep)
    with pytest.raises(adapter.OpenRouterError,match='does not support strict'):
        adapter.call(spec,'s','u',4096,tmp_path,'chair-0',spent_eur=0,cap_eur=15,fx=.85)
    assert not any(c[0]=='POST' for c in calls)
    assert not list(tmp_path.glob('*request.json'))


@pytest.mark.parametrize('text',[
    '{"next_model_id":"openai/gpt-6-astra","question":"Was heißt "wirksam"?"}',
    '{"next_model_id":"sixth-seat","question":"Frage?"}',
    '{"next_model_id":"openai/gpt-6-astra"}',
    '{"next_model_id":"openai/gpt-6-astra","question":"Frage?","extra_vote":true}',
    '```json\n{"next_model_id":"openai/gpt-6-astra","question":"Frage?"}\n```',
])
def test_strict_moderation_invalid_output_keeps_bill_and_original_without_retry(tmp_path,monkeypatch,text):
    spec,ep=structured_chair();response,generation=envelope(spec,text)
    calls=stub_http(monkeypatch,spec,response,generation,endpoint=ep)
    with pytest.raises(adapter.OpenRouterError,match='violates requested schema') as error:
        adapter.call(spec,'s','u',4096,tmp_path,'chair-0',spent_eur=0,cap_eur=15,fx=.85)
    assert error.value.usage['billed_usd']=='0.002'
    assert sum(c[0]=='POST' for c in calls)==1
    assert json.loads((tmp_path/'chair-0-anthropic-response.json').read_bytes())['choices'][0]['message']['content']==text
    result=json.loads((tmp_path/'chair-0-anthropic-result.json').read_text())
    assert result['outcome']=='invalid' and result['retry_allowed'] is False
    assert result['confirmed_usage']['billed_usd']=='0.002'


@pytest.mark.parametrize('spec', SPECS, ids=lambda s:s['family'])
def test_five_parameter_pinning_raw_and_billed_contract(spec, tmp_path, monkeypatch):
    calls = stub_http(monkeypatch, spec)
    text, usage = run_session.call_model(spec, 'SYSTEM', 'USER', 32768, tmp_path, 'r1',
                                         budget={'spent_eur': 0, 'cap_eur': 15, 'fx': .85})
    request = next(c[2] for c in calls if c[0] == 'POST')
    assert request['messages'] == [{'role':'system','content':'SYSTEM'}, {'role':'user','content':'USER'}]
    assert request['provider']['only'] == [spec['openrouter']['endpoint']]
    assert request['provider']['order'] == request['provider']['only']
    assert request['provider']['allow_fallbacks'] is False
    assert request['provider']['require_parameters'] is True
    assert request['provider']['data_collection'] == 'deny'
    assert not {'tools','plugins','models','route','preset','cache_control'} & request.keys()
    if spec['openrouter']['quantization'] != 'unknown':
        assert request['provider']['quantizations'] == [spec['openrouter']['quantization']]
    else:
        assert 'quantizations' not in request['provider']
    assert request['usage'] == {'include':True}
    assert request['reasoning']['effort'] == spec['openrouter']['reasoning_effort']
    assert request[spec['openrouter']['token_parameter']] == 32768
    assert (tmp_path/f"r1-{spec['family']}-response.json").read_bytes().startswith(b'  {')
    assert text == 'Answer' and usage['billed_usd'] == '0.002'
    assert usage['provenance']['quantization'] == spec['openrouter']['quantization']
    assert usage['provenance']['cost_basis'] == 'billed'
    assert 'Authorization' not in (tmp_path/f"r1-{spec['family']}-request.json").read_text()
    before = len(calls)
    with pytest.raises(adapter.OpenRouterError, match='repetition'):
        adapter.call(spec, 'S', 'U', 100, tmp_path, 'r1',spent_eur=0,cap_eur=15,fx=.85)
    assert not any(c[0]=='POST' for c in calls[before:])


@pytest.mark.parametrize('target,key,value', [
    ('response','model','wrong'), ('response','provider',None), ('generation','provider_name','wrong'),
    ('generation','model','wrong'), ('generation','id','gen-other'), ('generation','total_cost',.003),
    ('generation','native_tokens_prompt',11), ('generation','native_tokens_completion',21),
    ('generation','native_tokens_reasoning',None), ('generation','native_tokens_cached',1),
    ('generation','cancelled',True), ('generation','is_byok',True), ('generation','num_search_results',1),
])
def test_mismatches_never_valid(target,key,value,tmp_path,monkeypatch):
    spec=SPECS[0]; resp, gen = envelope(spec)
    (resp if target=='response' else gen['data'])[key]=value
    calls=stub_http(monkeypatch,spec,resp,gen)
    with pytest.raises(adapter.OpenRouterError):
        adapter.call(spec,'S','U',100,tmp_path,'r1',spent_eur=0,cap_eur=15,fx=.85)
    result=json.loads((tmp_path/'r1-anthropic-result.json').read_text())
    assert result['outcome']=='invalid' and result['retry_allowed'] is False
    assert sum(c[0]=='POST' for c in calls)==1
    assert (tmp_path/'r1-anthropic-response.json').exists()


@pytest.mark.parametrize('native,normalized,outcome',[(None,'content_filter','invalid'),('refusal','content_filter','refusal'),('max_tokens','length','invalid'),('mystery','stop','invalid'),('end_turn','length','invalid')])
def test_native_stop_classification(native,normalized,outcome):
    spec=SPECS[0];r,g=envelope(spec)
    r['choices'][0].update(native_finish_reason=native,finish_reason=normalized)
    g['data'].update(native_finish_reason=native,finish_reason=normalized)
    with pytest.raises(adapter.OpenRouterError) as e: adapter.validate_response(spec,r,g)
    assert e.value.outcome==outcome


@pytest.mark.parametrize('value',[None,True,-1,float('nan'),'missing'])
def test_invalid_usage(value):
    r,g=envelope(SPECS[0]);r['usage']['prompt_tokens']=value
    with pytest.raises(adapter.OpenRouterError): adapter.validate_response(SPECS[0],r,g)


@pytest.mark.parametrize('key,value',[('quantization','fp4'),('status',-1),('context_length',12),('supported_parameters',[]),('max_completion_tokens',2),('provider_name','wrong')])
def test_endpoint_drift_is_write_free(key,value,tmp_path,monkeypatch):
    ep=metadata(SPECS[0]);ep[key]=value
    calls=stub_http(monkeypatch,SPECS[0],endpoint=ep)
    with pytest.raises(adapter.OpenRouterError):
        adapter.call(SPECS[0],'s','u',100,tmp_path,'r1',spent_eur=0,cap_eur=15,fx=.85)
    assert list(tmp_path.iterdir())==[] and not any(c[0]=='POST' for c in calls)


def test_price_increase_and_no_budget_are_write_free(tmp_path,monkeypatch):
    ep=metadata(SPECS[0]);ep['pricing']['prompt']='1'
    calls=stub_http(monkeypatch,SPECS[0],endpoint=ep)
    with pytest.raises(adapter.OpenRouterError,match='price'): adapter.call(SPECS[0],'s','u',100,tmp_path,'r1',spent_eur=0,cap_eur=15,fx=.85)
    with pytest.raises(adapter.OpenRouterError,match='Budget'): adapter.call(SPECS[0],'s','u',100,tmp_path,'r1',spent_eur=14,cap_eur=15,fx=.85)
    assert not list(tmp_path.iterdir())
    assert not any(c[0]=='POST' for c in calls)


def test_timeout_never_retries_or_falls_back(tmp_path,monkeypatch):
    calls=stub_http(monkeypatch,SPECS[0],failure=TimeoutError('do not expose this credential-like diagnostic'))
    with pytest.raises(adapter.OpenRouterError,match='billing unresolved'):
        run_session.call_model(SPECS[0],'s','u',100,tmp_path,'r1',budget={'spent_eur':0,'cap_eur':15,'fx':.85})
    assert sum(c[0]=='POST' for c in calls)==1
    result=(tmp_path/'r1-anthropic-result.json').read_text()
    assert 'unavailable' in result and 'credential-like' not in result


def test_credit_preflight_and_keys(monkeypatch):
    calls=stub_http(monkeypatch,SPECS[0]);adapter.preflight([SPECS[0]])
    assert adapter.required_keys(SPECS)==['OPENROUTER_API_KEY']
    assert adapter.required_keys(SPECS+[{'family':'anthropic'}])==['ANTHROPIC_API_KEY','OPENROUTER_API_KEY']
    assert not any(c[0]=='POST' for c in calls)


@pytest.mark.parametrize('models',[SPECS[:4],SPECS+[SPECS[0]],SPECS[:4]+[{'family':'google','model':'g'}], [{'family':'anthropic','model':'m','transport':'subscription_sdk'}]])
def test_no_mixed_or_incomplete_roster(models):
    with pytest.raises(adapter.OpenRouterError): adapter.validate_roster(models)


def test_forbidden_model_variants():
    for model in ['openrouter/auto','anthropic/claude-fable-5.1:free','anthropic/claude-fable-latest','wrong']:
        spec=copy.deepcopy(SPECS[0]);spec['model']=model
        with pytest.raises(adapter.OpenRouterError):adapter.contract(spec)


def test_billed_costs_do_not_use_list_prices():
    spec=SPECS[0]
    result=run_session.compute_costs({spec['model']:{'input_tokens':10,'output_tokens':20,'billed_usd':'0.002'}},[spec],.85)
    assert result['by_model'][0]['usd']==.002
    assert result['by_model'][0]['cost_basis']=='billed'


def test_phase_barrier_stops_invalid_votes_and_challenges(tmp_path):
    for kind,entries in [('r1',[]),('challenge',[{'model':s['model'],'status':'invalid'} for s in SPECS]),('r2',[{'model':s['model'],'parsed':None} for s in SPECS])]:
        with pytest.raises(SystemExit,match='Phasenbarriere'):run_session.openrouter_phase_barrier(SPECS,entries,kind,tmp_path)
    # Historical API semantics are unchanged.
    run_session.openrouter_phase_barrier([{'model':'old'}],[],'r1',tmp_path)


def test_session_missing_key_precedes_any_write(tmp_path,monkeypatch):
    cfg=json.loads((ROOT/'gremium/config.json').read_text());cfg['models']=SPECS
    cfg['features']['live_council']['enabled']=False
    cfg['features']['three_scouts']['enabled']=False
    here=tmp_path/'gremium';here.mkdir();(here/'config.json').write_text(json.dumps(cfg))
    monkeypatch.setattr(run_session,'HERE',here);monkeypatch.setattr(run_session,'ROOT',tmp_path)
    monkeypatch.setattr(run_session,'load_env',lambda *a:None)
    monkeypatch.delenv('OPENROUTER_API_KEY',raising=False)
    monkeypatch.setattr(sys,'argv',['run_session','--question','q','--title','t'])
    before=set(tmp_path.rglob('*'))
    with pytest.raises(SystemExit):run_session.main()
    assert set(tmp_path.rglob('*'))==before


def test_commission_missing_key_precedes_any_write(tmp_path,monkeypatch):
    monkeypatch.setattr(run_commission,'load_env',lambda *a:None)
    monkeypatch.delenv('OPENROUTER_API_KEY',raising=False)
    with pytest.raises(SystemExit) as exc:
        run_commission._run(tmp_path,{'models':SPECS,'fx_rate_usd_eur':.85},SimpleNamespace(date='2026-09-19',convened='2026-09-19',commission_id='offline-only',dry_run=False))
    assert exc.value.code == 1
    assert not list(tmp_path.iterdir())


def synthetic_vote():
    orgs=json.loads((ROOT/'organizations.json').read_text())['organizations']
    org=orgs[0]
    return 'Independent text\n```json\n'+json.dumps({'recommendations':[
        {'pillar':p,'organization':org['canonical_name'],'title':'Synthetic','confidence':.8,'conditional':False,'reservation':None} for p in 'ABCD']})+'\n```'


def synthetic_run(tmp_path,monkeypatch,invalid_phase=None):
    cfg=json.loads((ROOT/'gremium/config.json').read_text());cfg['models']=copy.deepcopy(SPECS)
    cfg['features']['deliberation_0_5']['enabled']=True
    cfg['features']['live_council']['enabled']=False
    cfg['features']['three_scouts']['enabled']=False
    here=tmp_path/'gremium';here.mkdir();(here/'config.json').write_text(json.dumps(cfg))
    for name in ['manifest.md','organizations.json','schedule.json']:
        (tmp_path/name).write_bytes((ROOT/name).read_bytes())
    (here/'sources.md').write_text('Synthetic evidence')
    (tmp_path/'sessions').mkdir()
    monkeypatch.setattr(run_session,'ROOT',tmp_path);monkeypatch.setattr(run_session,'HERE',here)
    monkeypatch.setattr(run_session,'load_env',lambda *a:None)
    monkeypatch.setattr(run_session,'require_keys',lambda *a:None)
    monkeypatch.setattr(adapter,'preflight',lambda *a:None)
    monkeypatch.setattr(adapter,'endpoint_preflight',metadata)
    monkeypatch.setattr(run_session,'prior_session',lambda:(None,None))
    monkeypatch.setattr(run_session,'generate_summary',lambda *a,**kw:('Summary',[],{'input_tokens':0,'output_tokens':0},None))
    import organizations
    organizations.load_registry(ROOT/'organizations.json')
    calls=[];responses={}
    def http(method,path,payload=None):
        if method=='POST':
            spec=next(s for s in SPECS if s['model']==payload['model'])
            n=sum(m==spec['model'] for m in calls);calls.append(spec['model'])
            text=synthetic_vote()
            if n==1:
                target=SPECS[(SPECS.index(spec)+1)%5]['model']
                text='```json\n'+json.dumps({'target_model_id':target,'stance':'dispute','claim':'Claim','challenge':'Challenge','why_decisive':'Evidence'})+'\n```'
            if n==invalid_phase:text='Invalid unstructured output'
            r,g=envelope(spec,text);gid=f'gen-{len(calls)}';r['id']=gid;g['data']['id']=gid;responses[gid]=g
            return json.dumps(r).encode()
        return json.dumps(responses[path.split('=')[1]]).encode()
    monkeypatch.setattr(adapter,'http',http)
    monkeypatch.setattr(sys,'argv',['run_session','--question','Synthetic','--title','Offline','--session-id','synthetic'])
    return calls


def test_full_five_seat_three_phase_record_and_schema(tmp_path,monkeypatch):
    calls=synthetic_run(tmp_path,monkeypatch)
    run_session.main()
    session=json.loads((tmp_path/'sessions/synthetic/session.json').read_text())
    assert calls==[s['model'] for s in SPECS]*3
    assert session['council_transport']=='openrouter_api'
    voices=[v for r in session['rounds'] for v in r.get('votes',[])+r.get('exchanges',[])]
    assert len(voices)==15 and all(v['provenance']['cost_basis']=='billed' for v in voices)
    validator=jsonschema.Draft202012Validator(json.loads((ROOT/'schema/session.schema.json').read_text()))
    validator.validate(session)
    del voices[0]['provenance']['upstream_provider']
    assert list(validator.iter_errors(session))


@pytest.mark.parametrize('phase,expected_calls',[(0,5),(1,10),(2,15)])
def test_orchestrator_never_crosses_invalid_phase(tmp_path,monkeypatch,phase,expected_calls):
    calls=synthetic_run(tmp_path,monkeypatch,phase)
    before=(tmp_path/'schedule.json').read_bytes()
    with pytest.raises(SystemExit,match='Phasenbarriere'):run_session.main()
    assert len(calls)==expected_calls
    assert not (tmp_path/'sessions/synthetic/session.json').exists()
    assert (tmp_path/'schedule.json').read_bytes()==before


def test_ambiguous_endpoint_rejected(monkeypatch):
    spec=SPECS[0]
    def http(method,path,payload=None):
        if path=='/models':return json.dumps({'data':[{'id':spec['model'],'reasoning':{'supported_efforts':['max']}}]}).encode()
        ep=metadata(spec);other={**ep,'tag':'anthropic/other'}
        return json.dumps({'data':{'id':spec['model'],'endpoints':[ep,other]}}).encode()
    monkeypatch.setattr(adapter,'http',http)
    with pytest.raises(adapter.OpenRouterError,match='ambiguous'):adapter.endpoint_preflight(spec)


def test_decimal_cost_mismatch_not_hidden_by_float_rounding():
    r,g=envelope(SPECS[0]);r['usage']['cost']='0.0020000000000000000001'
    with pytest.raises(adapter.OpenRouterError,match='cost mismatch'):adapter.validate_response(SPECS[0],r,g)


@pytest.mark.parametrize('reported,billed,other',[
    ('0.0162091908','0.01620919','0.01620920'),
    ('0.0165124872','0.016512487','0.016512488'),
    ('0.0167890536','0.016789053','0.016789055'),
])
def test_generation_decimal_rounding_requires_matching_credit_receipt_and_books_it(reported,billed,other):
    r,g=envelope(SPECS[4]);r['usage']['cost']=reported
    g['data'].update(total_cost=billed,usage=billed)
    _,usage=adapter.validate_response(SPECS[4],r,g)
    assert usage['billed_usd']==billed
    assert usage['provenance']['usage']['cost']==reported
    g['data'].update(total_cost=other,usage=other)
    with pytest.raises(adapter.OpenRouterError,match='cost mismatch'):adapter.validate_response(SPECS[4],r,g)
    g['data']['usage']=billed
    with pytest.raises(adapter.OpenRouterError,match='credit usage mismatch'):adapter.validate_response(SPECS[4],r,g)


@pytest.mark.parametrize('field,value',[('quantization','fp4'),('endpoint','other'),('usage',.003)])
def test_generation_precision_endpoint_and_credit_drift(field,value):
    r,g=envelope(SPECS[0]);g['data'][field]=value
    with pytest.raises(adapter.OpenRouterError):adapter.validate_response(SPECS[0],r,g)


def test_no_credit_aborts_without_inference(monkeypatch):
    calls=[]
    def http(method,path,payload=None):
        calls.append(method)
        return json.dumps({'data': {'limit':1,'limit_remaining':0} if path=='/key' else {'total_credits':1,'total_usage':1}}).encode()
    monkeypatch.setattr(adapter,'http',http)
    with pytest.raises(adapter.OpenRouterError,match='credit'):adapter.preflight(SPECS)
    assert 'POST' not in calls


def test_commission_uses_shared_transport_offline(tmp_path,monkeypatch):
    monkeypatch.setattr(run_commission,'load_env',lambda *a:None)
    monkeypatch.setattr(run_commission,'require_keys',lambda *a:None)
    monkeypatch.setattr(adapter,'preflight',lambda *a:None)
    monkeypatch.setattr(adapter,'endpoint_preflight',metadata)
    outputs={};calls=[]
    def http(method,path,payload=None):
        if method=='POST':
            spec=next(s for s in SPECS if s['model']==payload['model'])
            calls.append(spec['model'])
            r,g=envelope(spec,'MOTIV: Synthetisches Relief.\n\nBEGRÜNDUNG: Offline-Test der gemeinsamen Maschine.')
            r['id']=f'gen-order-{len(calls)}';g['data']['id']=r['id'];outputs[r['id']]=g
            return json.dumps(r).encode()
        return json.dumps(outputs[path.split('=')[1]]).encode()
    monkeypatch.setattr(adapter,'http',http)
    result=run_commission._run(tmp_path,{'models':SPECS,'fx_rate_usd_eur':.85},SimpleNamespace(date='2026-09-19',convened='2026-09-19',commission_id='synthetic',dry_run=False))
    assert calls==[s['model'] for s in SPECS]
    # Only synthetic tmp_path receives outputs. Every order contains the matched evidence.
    orders=result['commission']['orders']
    assert len(orders)==5 and all(o['usage']['provenance']['cost_basis']=='billed' for o in orders)


@pytest.mark.parametrize('raw',[b'[]',b'not-json',b'{"a":1,"a":2}',b'{"cost":NaN}'])
def test_malformed_raw_is_invalid(raw):
    with pytest.raises(adapter.OpenRouterError) as exc:adapter.decode(raw)
    assert exc.value.outcome=='invalid'


def test_generation_unavailable_never_repeats_inference(tmp_path,monkeypatch):
    waits=[]
    monkeypatch.setattr(adapter.time,'sleep',waits.append)
    calls=stub_http(monkeypatch,SPECS[0],generation={'error':{'code':404}})
    with pytest.raises(adapter.OpenRouterError,match='Generation receipt delayed'):
        adapter.call(SPECS[0],'s','u',100,tmp_path,'r1',spent_eur=0,cap_eur=15,fx=.85)
    assert sum(c[0]=='POST' for c in calls)==1
    assert waits==[2,8,20,30,30,30]
    assert len(list(tmp_path.glob('*-generation-attempt-*.json')))==7
    assert json.loads((tmp_path/'r1-anthropic-result.json').read_text())['outcome']=='unavailable'


def test_delayed_generation_after_old_timeout_keeps_single_paid_call(tmp_path,monkeypatch):
    waits=[];reads=[]
    monkeypatch.setattr(adapter.time,'sleep',waits.append)
    calls=stub_http(monkeypatch,SPECS[0])
    original=adapter.http
    def delayed(method,path,payload=None):
        if path.startswith('/generation?'):
            reads.append(path)
            if len(reads)<=4:return b'{"error":{"code":404}}'
        return original(method,path,payload)
    monkeypatch.setattr(adapter,'http',delayed)
    text,usage=adapter.call(SPECS[0],'s','u',100,tmp_path,'r1',spent_eur=0,cap_eur=15,fx=.85)
    assert text and usage['billed_usd']=='0.002'
    assert len(reads)==5 and waits==[2,8,20,30]
    assert sum(c[0]=='POST' for c in calls)==1
    assert json.loads((tmp_path/'r1-anthropic-generation-attempt-3.json').read_text())['error']['code']==404


@pytest.mark.parametrize('observe', [False, True])
def test_complete_provider_token_overrun_is_observed_only_in_explicit_cost_mode(tmp_path,monkeypatch,observe):
    spec=SPECS[2]
    response,generation=envelope(spec)
    stub_http(monkeypatch,spec,response,generation)
    if not observe:
        with pytest.raises(adapter.OpenRouterError,match='Billed tokens exceeded'):
            adapter.call(spec,'s','u',10,tmp_path,'once',spent_eur=0,cap_eur=15,fx=.85)
    else:
        text,usage=adapter.call(spec,'s','u',10,tmp_path,'once',spent_eur=0,cap_eur=15,fx=.85,observe_costs=True)
        assert text=='Answer'
        assert usage['provenance']['output_limit_observation']=={'requested':10,'billed':20}
