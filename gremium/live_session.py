"""Backend entry point for 0.6. Default-off; optional explicit file publisher."""
import datetime
import json
from pathlib import Path

import openrouter
import prompts
from ballot_status import CONTRACT
from cost_bounds import Budget, InputBounds
from council_state import VERSION, Events, atomic_write, chair_for, digest, encoded, process_lock, validate_record
from envtools import load_env, require_keys
from live_debate import CHAIR_SYSTEM, FINAL_TASK, SPEECH_TASK, SUMMARY_TASK, chair_response_format, conduct


def revalidate_saved_call(directory, spec, step, reason, *, delayed_generation=None):
    """Explicit offline revalidation after a documented adapter correction.

    Original request, response, billing and failed result remain unchanged.
    This function never makes a network request or repairs model content.
    """
    directory = Path(directory)
    stem = f'{step}-{spec["family"]}'
    paths = {k:directory/f'{stem}-{k}.json' for k in ('request','response','generation','endpoint','result')}
    original = json.loads(paths['result'].read_text())
    generation_path = paths['generation']
    if delayed_generation is not None:
        generation_path = Path(delayed_generation)
        if (generation_path.parent.resolve() != directory.resolve() or generation_path.is_symlink()
                or not generation_path.name.startswith(stem+'-generation-delayed-')
                or generation_path.suffix != '.json'):
            raise ValueError('Verspäteter Beleg muss eine eigene lokale Rohdatei sein')
        if (original.get('outcome') != 'unavailable'
                or (openrouter.decode(paths['generation'].read_bytes()).get('error') or {}).get('code') != 404):
            raise ValueError('Verspäteter Beleg verlangt einen ursprünglichen Generation-404')
    elif original.get('outcome') != 'invalid':
        raise ValueError('Nachprüfung verlangt einen dokumentierten ungültigen Originalbefund')
    if not reason.strip():
        raise ValueError('Nachprüfung verlangt einen dokumentierten ungültigen Originalbefund')
    endpoint = json.loads(paths['endpoint'].read_text())
    text, usage = openrouter.validate_response(spec,openrouter.decode(paths['response'].read_bytes()),
        openrouter.decode(generation_path.read_bytes()),endpoint.get('canonical_model'))
    request = json.loads(paths['request'].read_text())
    if request['model'] != spec['model'] or request['provider']['only'] != [spec['openrouter']['endpoint']]:
        raise ValueError('Nachprüfung darf keinen anderen Modellauftrag bestätigen')
    usage['provenance']['raw_artifact']='raw/'+paths['response'].name
    usage['provenance']['generation_artifact']='raw/'+generation_path.name
    result={'outcome':'valid', **usage, 'reason':reason,
            'original_sha256':{k:digest(p.read_bytes()) for k,p in paths.items()}}
    if delayed_generation is not None:
        result['delayed_generation']={'name':generation_path.name,'sha256':digest(generation_path.read_bytes())}
    with (directory/f'{stem}-revalidated.json').open('xb') as stream:
        stream.write(encoded(result))
    return text, usage


class Calls:
    def __init__(self, directory, events, budget, fx):
        self.directory, self.events, self.budget, self.fx = Path(directory), events, budget, fx
        self.usage = []

    def run(self, spec, system, user, phase, step, limit, remaining):
        if step.startswith('chair-') and spec.get('chair_reasoning_effort'):
            spec = {**spec, 'openrouter':{**spec['openrouter'], 'reasoning_effort':spec['chair_reasoning_effort']}}
        request = openrouter.request_for(spec, system, user, limit)
        stem = f'{step}-{spec["family"]}'
        paths = {k: self.directory / f'{stem}-{k}.json' for k in ('request', 'response', 'generation', 'endpoint', 'result')}
        if paths['request'].exists():
            generation_path = paths['generation']
            if json.loads(paths['request'].read_text()) != request:
                raise ValueError('Wiederaufnahme verändert einen bereits angeforderten Aufruf')
            recorded = json.loads(paths['result'].read_text()) if paths['result'].exists() else {}
            if recorded.get('outcome') != 'valid':
                approval = self.directory/f'{stem}-revalidated.json'
                if approval.exists():
                    revalidated = json.loads(approval.read_text())
                    if revalidated.get('original_sha256') != {k:digest(p.read_bytes()) for k,p in paths.items()}:
                        raise ValueError('Nachprüfungsbeleg passt nicht zu unveränderten Originaldateien')
                    delayed = revalidated.get('delayed_generation')
                    if delayed is not None:
                        name = delayed.get('name','')
                        if Path(name).name != name or not name.startswith(stem+'-generation-delayed-') or not name.endswith('.json'):
                            raise ValueError('Ungültiger verspäteter Belegpfad')
                        generation_path = self.directory/name
                        if generation_path.is_symlink() or digest(generation_path.read_bytes()) != delayed.get('sha256'):
                            raise ValueError('Verspäteter Abrechnungsbeleg verändert')
                    recorded = {k:v for k,v in revalidated.items() if k not in ('reason','original_sha256','delayed_generation')}
            if recorded.get('outcome') != 'valid':
                raise openrouter.OpenRouterError('Ungeklärter/fehlgeschlagener Aufruf; keine erneute Inferenz')
            endpoint = json.loads(paths['endpoint'].read_text())
            text, usage = openrouter.validate_response(spec, openrouter.decode(paths['response'].read_bytes()),
                                                      openrouter.decode(generation_path.read_bytes()), endpoint.get('canonical_model'))
            usage['provenance']['raw_artifact'] = 'raw/' + paths['response'].name
            usage['provenance']['generation_artifact'] = 'raw/' + generation_path.name
            if usage != {k:v for k,v in recorded.items() if k != 'outcome'}:
                raise ValueError('Abrechnungs- oder Herkunftsbeleg verändert')
        else:
            if any(p.exists() for p in paths.values()):
                raise openrouter.OpenRouterError('Unvollständige Aufrufartefakte; keine erneute Inferenz')
            tokens, reserve = self.budget.check(spec, request, limit, remaining)
            key = openrouter.decode(openrouter.http('GET', '/key'))['data']
            if (key.get('limit_reset') is not None or key.get('limit') is None
                    or openrouter.amount(key['limit_remaining']) <= 0):
                raise openrouter.OpenRouterError('Finanziertes, nicht zurückgesetztes Key-Limit erforderlich')
            if not self.budget.observe and openrouter.amount(key['limit_remaining']) < openrouter.worst_case_usd(spec, limit, tokens) + reserve:
                raise openrouter.OpenRouterError('Key-Limit deckt Aufruf und Abschlussreserve nicht')
            self.events.once('waiting-' + step, 'waiting', phase, model=spec['model'],
                             role='chair' if step.startswith(('chair-', 'summary')) else 'member',
                             data={'cost_mode':'observe' if self.budget.observe else 'bounded', 'input_bound': tokens,
                                   'closure_reserve_usd':None if self.budget.observe else str(reserve),
                                   'spent_usd': str(self.budget.spent)})
            # Includes a heartbeat failure and a reused waiting event on resume.
            # A failed public feed must stop before the next paid inference.
            self.events.publish()
            try:
                text, usage = openrouter.call(spec, system, user, limit, self.directory, step,
                    spent_eur=self.budget.spent * self.fx, cap_eur=(self.budget.cap - reserve) * self.fx,
                    fx=self.fx, input_bound=tokens, observe_costs=self.budget.observe)
            except openrouter.OpenRouterError as exc:
                if exc.usage is not None:
                    self.account(spec, step, {**exc.usage, 'outcome':exc.outcome})
                raise
        self.account(spec, step, usage)
        return text, usage

    def account(self, spec, step, usage):
        """Account for paid failures too; a valid bill is not a valid vote."""
        self.usage.append((spec, step, usage))
        try:
            self.budget.record(usage)
        finally:
            atomic_write(self.directory.parent/'costs-live.json', encoded(self.costs()))
        print(f"{step} · {spec['label']}: {usage['billed_usd']} Credits; bestätigt gesamt {self.budget.spent}", flush=True)

    def costs(self):
        entries = []
        for spec, step, usage in self.usage:
            usd = openrouter.amount(usage['billed_usd'])
            role = {'initial':'initial_vote','chair':'moderation','speech':'contribution','final':'final_vote','summary':'summary'}[step.split('-')[0]]
            reasoning = (usage['provenance']['usage'].get('completion_tokens_details') or {}).get('reasoning_tokens')
            entries.append({'model':spec['model'], 'label':spec['label'], 'step':step,
                            'role':role, 'reasoning_effort':spec['openrouter']['reasoning_effort'],
                            'reasoning_tokens':reasoning,
                            'visible_output_tokens':None if reasoning is None else usage['output_tokens']-reasoning,
                            'input_tokens':usage['input_tokens'], 'output_tokens':usage['output_tokens'],
                            'usd':float(usd), 'eur':float(usd * self.fx), 'cost_basis':'billed', 'transport':'openrouter_api',
                            'outcome':usage.get('outcome','valid')})
        totals = {}
        for spec, step, usage in self.usage:
            t = totals.setdefault(spec['model'], {'model':spec['model'], 'label':spec['label'], 'calls':0, 'usd':openrouter.amount(0)})
            t['calls'] += 1
            t['usd'] += openrouter.amount(usage['billed_usd'])
        roles = {}
        for entry, (_, _, usage) in zip(entries, self.usage):
            key = (entry['model'],entry['role'])
            t = roles.setdefault(key, {'model':entry['model'], 'label':entry['label'], 'role':entry['role'],
                                      'calls':0, 'input_tokens':0, 'output_tokens':0, 'usd':openrouter.amount(0)})
            t['calls'] += 1
            t['input_tokens'] += usage['input_tokens']
            t['output_tokens'] += usage['output_tokens']
            t['usd'] += openrouter.amount(usage['billed_usd'])
        return {'currency':'EUR', 'total':float(self.budget.spent * self.fx), 'total_usd':str(self.budget.spent),
                'fx_rate_usd_eur':float(self.fx), 'by_model':entries,
                'totals_by_model':[{**v,'usd':str(v['usd'])} for v in totals.values()],
                'totals_by_model_role':[{**v,'usd':str(v['usd'])} for v in roles.values()]}


def settings(config):
    cfg = config['live_council']
    if cfg.get('procedure_version') != VERSION:
        raise ValueError('Unbekannte Live-Verfahrensversion')
    openrouter.validate_roster(cfg['models'])
    expected = {'initial','chair','debate','final','summary','weekly'}
    if set(cfg['output_limits']) != expected or any(type(v) is not int or v <= 0 for v in cfg['output_limits'].values()):
        raise ValueError('Rollenlimits fehlen')
    return cfg


def dossier_context(root, config, path, today):
    """Use the existing weekly research, without paying to rediscover it."""
    from scout_context import historical_comparison
    source = Path(path)
    payload = source.read_bytes()
    entry = json.loads(payload)
    expected = {s['model'] for s in config['scouts']}
    reports = entry.get('scouts', [])
    if (entry.get('research_mode') != 'blind_then_compare' or len(reports) != 3
            or {s.get('model') for s in reports} != expected
            or any(not s.get('findings') or not s.get('research_provenance') for s in reports)):
        raise ValueError('Pilot braucht drei nachvollziehbare blinde Scout-Berichte')
    age = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(entry['date'])).days
    if not 0 <= age <= 7:
        raise ValueError('Scout-Dossier ist zukünftig oder älter als sieben Tage')
    previous = []
    for p in (root / 'sessions').glob('*/session.json'):
        data = json.loads(p.read_text())
        previous.append((data.get('number', 0), data))
    prior = max(previous, key=lambda p:p[0])[1] if previous else {}
    # No convocation judgement from the weekly chair is smuggled into initial votes.
    context = json.dumps({'research_date':entry['date'], 'scouts':reports}, ensure_ascii=False)
    history = historical_comparison(root, today, prior['id'], prior) if prior else ''
    projection = config['live_council'].get('context_projection', 'full')
    if projection == 'compact_evidence_v1':
        from council_context import compact_context
        context = compact_context(entry, prior)
    elif projection == 'full':
        context += '\n\n' + history
    else:
        raise ValueError('Unbekannte Kontextprojektion')
    info = {'date':entry['date'], 'sha256':digest(payload), 'reused':True,
            'context_projection':projection, 'history_sha256':digest(history.encode())}
    return context, payload, info, len(previous) + 1, history.encode()


def run(root, config, args):
    root = Path(root)
    cfg = settings(config)
    if not args.dossier_json:
        raise ValueError('--dossier-json ist für den Live-Pilot erforderlich')
    if not args.session_id or Path(args.session_id).name != args.session_id or args.session_id in ('.','..'):
        raise ValueError('Live-Pilot braucht eine eindeutige einfache --session-id')
    public = getattr(args, 'public_session', False)
    if public and (args.output_dir or not getattr(args, 'live_feed_dir', None)):
        raise ValueError('Öffentliche Sitzung braucht einen Live-Feed und verwendet sessions/ als Rekordziel')
    output = root / 'sessions' if public else (Path(args.output_dir) if args.output_dir else root / '.review/live-sessions')
    output = output.resolve() / args.session_id
    if not public and any(output.is_relative_to(root / p) for p in ('sessions','journal','commissions','site')):
        raise ValueError('Backend-Pilot schreibt zunächst außerhalb veröffentlichter Rekorde')
    today = datetime.date.today().isoformat()
    if output.exists() and args.resume and (output/'run-input.json').exists():
        today = json.loads((output/'run-input.json').read_text())['date']
    context, research_bytes, research_info, number, history_bytes = dossier_context(root, config, args.dossier_json, today)
    observe = getattr(args, 'observe_costs', False)
    bounds = InputBounds(cfg.get('input_bounds', {}), root)
    if not observe:
        for spec in cfg['models']:
            bounds.policy(spec)
    fx = openrouter.amount(config['fx_rate_usd_eur'])
    if fx <= 0:
        raise ValueError('Positiver Wechselkurs erforderlich')
    budget = Budget(openrouter.amount(args.budget_cap) / fx, bounds, observe=observe)
    load_env(root / 'gremium', root)
    require_keys('OPENROUTER_API_KEY')
    openrouter.preflight(cfg['models'])
    with process_lock(root):
        schedule = json.loads((root / 'schedule.json').read_text())
        chair, index = chair_for(config, schedule)
        moderation_format = chair_response_format([m['model'] for m in cfg['models']])
        openrouter.preflight([{**chair, 'response_format':moderation_format,
            'openrouter':{**chair['openrouter'], 'reasoning_effort':chair['chair_reasoning_effort']}}])
        descriptor = {'id':args.session_id, 'question':args.question, 'title':args.title, 'date':today,
                      'chair':{'model':chair['model'],'rotation_index':index}, 'config':cfg,
                      'research':research_info, 'budget_cap_eur':str(args.budget_cap), 'fx':str(fx),
                      'cost_mode':'observe' if observe else 'bounded',
                      'ballot_contract':CONTRACT,
                      'manifest_sha256':digest((root/'manifest.md').read_bytes()),
                      'sources_sha256':digest((root/'gremium/sources.md').read_bytes()),
                      'context_sha256':digest(context.encode()), 'number':number,
                      'moderation_response_format':moderation_format,
                      'prompt_contract_sha256':digest({'system':prompts.SYSTEM_WITH_CONFLICT,
                          'context':prompts.SESSION_CONTEXT,'initial':prompts.LIVE_INITIAL_TASK,
                          'chair':CHAIR_SYSTEM,'speech':SPEECH_TASK,'final':FINAL_TASK,'summary':SUMMARY_TASK})}
        if public:
            descriptor['publication'] = 'live'
            registry = json.loads((root / 'models.json').read_text())
            by_model = {m['model']: m for m in registry['models']}
            for spec in cfg['models']:
                symbol = by_model.get(spec['model'], {})
                asset = symbol.get('asset')
                if (symbol.get('warden_review', {}).get('decision') != 'accepted' or not asset
                        or not (root / 'site/static' / asset.lstrip('/')).is_file()):
                    raise ValueError('Öffentliche Sitzung benötigt ein eigenes freigegebenes Medaillon je Sitz')
        if output.exists():
            if not args.resume:
                raise ValueError('Lauf existiert; Wiederaufnahme muss ausdrücklich gewählt werden')
            if json.loads((output/'run-input.json').read_text()) != descriptor:
                raise ValueError('Wiederaufnahme mit verändertem Auftrag/Konfiguration')
            if (output/'session.json').exists():
                return validate_record(output)
        else:
            output.mkdir(parents=True)
            atomic_write(output/'run-input.json', encoded(descriptor))
            atomic_write(output/'research.json', research_bytes)
            atomic_write(output/'history-full.md', history_bytes)
            atomic_write(output/'council-context.json', context.encode())
        (output/'raw').mkdir(exist_ok=True)
        publisher = None
        if getattr(args, 'live_feed_dir', None):
            from publish_live import FilePublisher, SshPublisher, public_session, validate_destination
            destination = validate_destination(args.live_feed_dir, output, root)
            meta = public_session(descriptor, json.loads((root/'models.json').read_text()))
            if getattr(args, 'live_feed_ssh', None):
                publisher = SshPublisher(destination, meta, host=args.live_feed_ssh,
                    identity=getattr(args, 'live_feed_identity', None), mode='live' if public else 'pilot')
            else:
                publisher = FilePublisher(destination, meta, mode='live' if public else 'pilot')
        events = Events(output/'events.json', args.session_id, publisher=publisher)
        events.once('start','started','setup',data={'chair':descriptor['chair'], 'research':research_info, 'dry_run':not public})
        if args.resume:
            events.append('resumed','setup',data={'retry_inference':False})
        attempt = sum(e['kind'] == 'resumed' for e in events.record['events'])
        caller = Calls(output/'raw',events,budget,fx)
        prompt = prompts.SESSION_CONTEXT.format(manifest=(root/'manifest.md').read_text(), sources=(root/'gremium/sources.md').read_text(),
            number=number, date=today, question=args.question, opening_section='', dossier_section=context)
        try:
            if publisher:
                events.publish()
                publisher.start()
            result = conduct(cfg['models'],chair,prompt,prompts.SYSTEM_WITH_CONFLICT,caller,events,cfg['output_limits'],
                             stop_after_first=getattr(args,'stop_after_first',False))
            if result.get('status') == 'initial_ready':
                checkpoint = {**result,'id':args.session_id,'costs':caller.costs()}
                atomic_write(output/'checkpoint.json',encoded(checkpoint))
                return checkpoint
            events.once(f'complete-{attempt}','completed','terminal',data={'spent_usd':str(budget.spent),'pilot_all_five_valid':True})
            record = {'schema_version':3,'procedure_version':VERSION,'council_transport':'openrouter_api',
                      'ballot_contract':CONTRACT,
                      'id':args.session_id,'number':number,'date':today,'title':args.title,'question':args.question,
                      'chair':descriptor['chair'],'participants':[{k:m[k] for k in ('model','family','label')} for m in cfg['models']],
                      'prompts':{'system':prompts.SYSTEM_WITH_CONFLICT,'context':prompt,
                                 'initial':prompt+'\n\n'+prompts.LIVE_INITIAL_TASK,'chair':CHAIR_SYSTEM,
                                 'speech':SPEECH_TASK,'final':FINAL_TASK,'summary':SUMMARY_TASK},
                      'status':'completed','dry_run':not public,'pilot':{'all_five_final_votes_valid':True},'tally_rule':'majority_3_of_5',
                      'research_source':research_info,'cost_mode':descriptor['cost_mode'],'costs':caller.costs(), **result,
                      'event_record':{'path':'events.json','sha256':digest((output/'events.json').read_bytes()),'event_count':len(events.record['events'])}}
            validate_record(output, record)
            atomic_write(output/'session.json',encoded(record))
            return record
        except BaseException as exc:
            # No exception contents from HTTP libraries enter the public event log.
            from publish_live import PublicationError
            try:
                events.append('aborted','terminal',data={'error_type':type(exc).__name__,'spent_usd_confirmed':str(budget.spent),
                                                        'costs_may_be_unresolved':True,'retry_inference':False})
            except PublicationError:
                pass  # append already retained the local abort; preserve the original failure.
            raise
        finally:
            if publisher:
                publisher.close()


class WeeklyRefusal(RuntimeError):
    def __init__(self, artifact):
        self.artifact = artifact
        super().__init__('Native Verweigerung des Wochenvorsitzes; Rohbeleg erhalten')


def weekly_decision(spec, system, user, raw_dir, config, spent_eur, cap_eur, root):
    """Same Council transport, with the existing strict weekly decision parser."""
    from run_wart import parse_wart_decision
    cfg = settings(config)
    bound = InputBounds(cfg.get('input_bounds', {}), root)
    limit = cfg['output_limits']['weekly']
    request = openrouter.request_for(spec, system, user, limit)
    tokens = bound.tokens(spec, request)
    try:
        text, usage = openrouter.call(spec, system, user, limit, raw_dir, 'chair-weekly',
            spent_eur=spent_eur, cap_eur=cap_eur, fx=config['fx_rate_usd_eur'], input_bound=tokens)
    except openrouter.OpenRouterError:
        artifact = Path(raw_dir) / f'chair-weekly-{spec["family"]}-response.json'
        if artifact.exists():
            raw = openrouter.decode(artifact.read_bytes())
            choices = raw.get('choices') or []
            if (raw.get('model') == spec['model'] and raw.get('provider') == spec['openrouter']['provider_name']
                    and len(choices) == 1 and choices[0].get('native_finish_reason') in ('refusal','content_filter')):
                raise WeeklyRefusal('raw/' + artifact.name) from None
        raise
    parse_wart_decision(text)  # strict bool; no guessed or coerced judgement
    return text, usage, {'stop_reason':'end_turn'}
