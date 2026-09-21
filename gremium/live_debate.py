"""Bounded, sequential conversation; independent votes at both ends."""
import json
import re

import prompts
from ballot_status import CONTRACT, read_decision
from cost_bounds import InsufficientBudget

CHAIR_SYSTEM = prompts.SYSTEM + '''\n\n## Dein Auftrag: Vorsitz und Wortvergabe

Du führst als stimmberechtigtes Ratsmitglied den Vorsitz. Wähle aus der
angegebenen Liste den nächsten Redner und stelle eine kurze sachliche Frage,
die die gemeinsame Prüfung voranbringt. Eigene Sachargumente gehören in deine
getrennten Redebeiträge. Lass begründete Zustimmung und Widerspruch zu.
Antworte ausschließlich mit einem gültigen JSON-Objekt ohne Markdown-Zaun:
{"next_model_id": "exakte ID aus der Liste", "question": "Frage"}.'''

SPEECH_TASK = '''## Dein Auftrag: Beitrag zur laufenden Beratung

Antworte auf die Frage des Vorsitzes und greife den bisherigen Verlauf auf.
Stimme begründet zu, widersprich oder präzisiere. Dein Sachbeitrag umfasst
höchstens 180 Wörter; das Schlussvotum folgt in einer eigenen Runde.
Beende mit einem JSON-Block in einem ```json-Zaun:
{"addressees": ["exakte fremde Modell-ID"], "objection": false, "reply_to": []}.
objection ist ein echtes Boolean: erhebst du einen Einwand gegen eine Position
der Adressaten? reply_to enthält nur Nummern früherer Ereignisse dieser Sitzung.
Der JSON-Block zählt nicht zum Wortkontingent.'''

FINAL_TASK = '''## Dein Auftrag: Schlussvotum nach der Beratung

Beantworte vor deinem Schlussvotum die an dich gerichteten Einwände.
Beginne mit einem inhaltlichen Abschnitt „## Einwände“; benenne,
was du übernimmst, verwirfst oder enger fasst und warum. Auch wenn keine
Einwände vorliegen, sage das ausdrücklich. Berücksichtige danach den gesamten
Verlauf. Du darfst deine Erstposition halten oder ändern und begründest beides.
Schreibe auch „## Dissens“ und halte verbleibende Unterschiede fest.

''' + prompts.LIVE_VOTE_FORMAT + '''

Ergänze dasselbe JSON-Votum um das Feld:
"objections": {"assessment": "deine Einordnung", "answers":
[{"event_seq": 1, "response": "begründete Antwort"}]}.
answers muss jeden im Auftrag gelisteten Einwand einzeln beantworten; ohne
gelistete Einwände ist es eine leere Liste. Nur dein Schlussvotum wird gezählt.'''

SUMMARY_TASK = '''## Dein Auftrag: Leserfassung der Sitzung

Fasse die abgeschlossene Beratung in fünf bis acht Sätzen zusammen. Die
gezählten Stimmen bleiben unverändert. Halte verbleibenden Dissens fest.
Nenne Enthaltungen getrennt von Empfehlungen und ungültigen Voten; der
Nenner bleibt fünf. Nicht zuordenbare Organisationen bleiben ausdrücklich offen.
Antworte ausschließlich mit einem JSON-Block in einem ```json-Zaun:
{"summary": "Leserfassung", "dissent_highlights": ["Verbleibender Dissens"]}.'''


def chair_response_format(allowed):
    return {'type':'json_schema', 'json_schema':{'name':'council_word_assignment', 'strict':True,
        'schema':{'type':'object', 'properties':{
            'next_model_id':{'type':'string', 'enum':list(allowed), 'description':'Nächster Redner aus der zulässigen Liste'},
            'question':{'type':'string', 'description':'Kurze sachliche Frage des Vorsitzes'}},
            'required':['next_model_id','question'], 'additionalProperties':False}}}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def vote(text, models, spec, *, final=False, objections=()):
    import run_session as session
    parsed = session.extract_json_block(text)
    if not isinstance(parsed, dict):
        raise ValueError('Votum ohne strukturierten Abschluss')
    recs = parsed.get('recommendations')
    if (not isinstance(recs, list) or len(recs) != 4 or not all(isinstance(r, dict) for r in recs)
            or {r.get('pillar') for r in recs} != set('ABCD')
            or not all(read_decision(r) for r in recs)):
        raise ValueError('Unvollständiges Vier-Säulen-Votum')
    if final:
        section = re.match(r'\s*## Einwände[^\S\n]*\n([^#`]+)', text)
        obj = parsed.get('objections')
        if not section or not section[1].strip() or not isinstance(obj, dict) or not nonempty(obj.get('assessment')):
            raise ValueError('Schlussvotum ohne Einwands-Teil ist unvollständig')
        answers = obj.get('answers')
        if (not isinstance(answers, list) or any(not isinstance(a, dict) or type(a.get('event_seq')) is not int
                                               or not nonempty(a.get('response')) for a in answers)
                or len(answers) != len(objections) or {a['event_seq'] for a in answers} != set(objections)):
            raise ValueError('Schlussvotum beantwortet nicht alle adressierten Einwände')
    return {**spec, 'text': text, 'parsed': parsed}


def transcript(events):
    return '\n\n'.join(
        f"### Ereignis {e['seq']} · {e['role']} · {e['model'] or 'Programm'}\n{e['content_md']}"
        for e in events if e['kind'] in ('initial_votes', 'moderation', 'contribution')
    )


def conduct(models, chair, context, system, caller, events, limits, *, stop_after_first=False, speech_amendment=None):
    """caller.run performs/replays one evidenced call and records actual cost."""
    import run_session as session
    ids = [m['model'] for m in models]
    closure = [(m, limits['final']) for m in models] + [(chair, limits['summary'])]
    initial_prompt = context + '\n\n' + prompts.LIVE_INITIAL_TASK
    initial = []
    for i, spec in enumerate(models):
        remaining = [(m, limits['initial']) for m in models[i+1:]] + closure
        text, usage = caller.run(spec, system, initial_prompt, 'initial', f'initial-{i}', limits['initial'], remaining)
        entry = vote(text, models, spec)
        entry['provenance'] = usage['provenance']
        initial.append(entry)
        if i == 0 and stop_after_first:
            events.once('first-vote-checkpoint','checkpoint','initial',model=spec['model'],role='member',
                        data={'status':'initial_ready','vote_revealed':False})
            return {'status':'initial_ready','model':spec['model']}
    # Reveal only once all independent calls are complete. Raw text is never cut.
    public_initial = [{'model': v['model'], 'content_md': v['text'], 'provenance': v['provenance']} for v in initial]
    first = events.once('initial-reveal', 'initial_votes', 'initial',
                        text='\n\n'.join(f"### {v['model']}\n{v['content_md']}" for v in public_initial),
                        data={'votes': public_initial})
    visible = [first]
    counts = dict.fromkeys(ids, 0)
    contributions = []
    closed_reason = 'ten_contributions'
    for turn in range(10):
        allowed = [m for m in ids if counts[m] == min(counts.values())]
        prompt = context + '\n\n## Gespräch\n' + transcript(visible)
        prompt += '\n\nZulässige nächste Redner: ' + json.dumps(allowed, ensure_ascii=False)
        try:
            moderator = {**chair, 'response_format':chair_response_format(allowed)}
            text, usage = caller.run(moderator, CHAIR_SYSTEM, prompt, 'debate', f'chair-{turn}', limits['chair'], closure)
        except InsufficientBudget:
            closed_reason = 'closure_budget_reserved'
            break
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        if (not isinstance(parsed, dict) or parsed.get('next_model_id') not in allowed
                or not nonempty(parsed.get('question'))):
            raise ValueError('Ungültige Wortvergabe; kein bezahlter Reparaturaufruf')
        target = parsed['next_model_id']
        moderation = events.once(f'moderation-{turn}', 'moderation', 'debate', model=chair['model'], role='chair',
                                 text=text, data={'next_model_id': target, 'question': parsed['question'], 'provenance': usage['provenance']})
        visible.append(moderation)
        spec = next(m for m in models if m['model'] == target)
        prompt = context + '\n\n## Gespräch\n' + transcript(visible) + '\n\n' + SPEECH_TASK
        try:
            text, usage = caller.run(spec, system, prompt, 'debate', f'speech-{turn}', limits['debate'], closure)
        except InsufficientBudget:
            closed_reason = 'closure_budget_reserved'
            break
        parsed = session.extract_json_block(text)
        if (not isinstance(parsed, dict) or type(parsed.get('objection')) is not bool
                or not isinstance(parsed.get('addressees'), list)
                or any(m not in ids for m in parsed['addressees'])
                or len(set(parsed['addressees'])) != len(parsed['addressees'])
                or (parsed['objection'] and not parsed['addressees'])
                or not isinstance(parsed.get('reply_to'), list)
                or any(type(n) is not int or n not in {e['seq'] for e in visible} for n in parsed['reply_to'])
                or not session.strip_json_block(text).strip()):
            raise ValueError('Ungültiger Debattenbeitrag')
        words = session.strip_json_block(text).split()
        word_count = len(words)
        if word_count > (speech_amendment['max_words'] if speech_amendment else 180):
            raise ValueError('Debattenbeitrag überschreitet das Redekontingent von 180 Wörtern')
        observations = {}
        if word_count > 180:
            observations['word_limit_observation'] = {
                'limit':180, 'word_count':word_count, 'excess':word_count-180,
                'lexical_word_count':sum(any(c.isalnum() for c in word) for word in words),
                'counting_method':'whitespace_split_without_json',
                'amendment_version':speech_amendment['amendment_version'],
                'amendment_sha256':speech_amendment['sha256']}
        if target in parsed['addressees']:
            # The Steward requires mistaken self-identification to remain an
            # observable result. Preserve the literal target, speaker and text;
            # do not infer another speaker or alter its vote/speaking quota.
            observations['identity_observation'] = {'kind':'self_addressed_contribution',
                'actual_speaker':target, 'self_addressed':True}
        event = events.once(f'contribution-{turn}', 'contribution', 'debate', model=target, role='member', text=text,
                            data={**parsed, **observations, 'provenance': usage['provenance']})
        visible.append(event)
        contributions.append(event)
        counts[target] += 1
    events.once('debate-close', 'debate_closed', 'debate', data={'reason': closed_reason, 'speaking_counts': counts})
    frozen = transcript(visible)
    final = []
    for i, spec in enumerate(models):
        obligations = [e['seq'] for e in contributions if e['data']['objection'] and spec['model'] in e['data']['addressees']]
        prompt = context + '\n\n## Vollständige abgeschlossene Debatte\n' + frozen
        prompt += '\n\n## Dein Erstvotum\n' + initial[i]['text'] + '\n\n' + FINAL_TASK
        prompt += '\nEinzeln zu beantwortende Einwände (Ereignisnummern): ' + json.dumps(obligations)
        remaining = [(m, limits['final']) for m in models[i+1:]] + [(chair, limits['summary'])]
        text, usage = caller.run(spec, system, prompt, 'final', f'final-{i}', limits['final'], remaining)
        entry = vote(text, models, spec, final=True, objections=obligations)
        entry['provenance'] = usage['provenance']
        final.append(entry)
    public_final = [{'model': v['model'], 'content_md': v['text'], 'provenance': v['provenance']} for v in final]
    last = events.once('final-reveal', 'final_votes', 'final', data={'votes': public_final})
    recs, unresolved = session.aggregate_recommendations(final, procedure_version='0.6', ballot_contract=CONTRACT)
    summary_prompt = context + '\n\n' + SUMMARY_TASK + '\n\n'
    summary_prompt += json.dumps({'final_votes': public_final, 'recommendations': recs}, ensure_ascii=False)
    text, usage = caller.run(chair, system, summary_prompt, 'summary', 'summary', limits['summary'], [])
    summary = session.extract_json_block(text)
    if (not isinstance(summary, dict) or not nonempty(summary.get('summary'))
            or not isinstance(summary.get('dissent_highlights'), list)
            or not all(nonempty(v) for v in summary['dissent_highlights'])):
        raise ValueError('Ungültige Leserfassung')
    events.once('summary', 'summary', 'summary', model=chair['model'], role='chair', text=text, data={'provenance': usage['provenance']})

    def public_votes(votes, event):
        return [{'model': v['model'], 'content_md': v['text'], 'provenance': v['provenance'],
                 'event_seq': event['seq'], 'confidence': v['parsed'].get('confidence'),
                 'recommendations': session.structured_vote_recs(v['parsed'], ballot_contract=CONTRACT)} for v in votes]

    return {'summary': summary['summary'], 'dissent_highlights': summary['dissent_highlights'],
            'recommendations': recs, 'unresolved_votes': unresolved, 'dissent_md': session.build_dissent(final),
            'rounds': [
                {'round': 1, 'kind': 'initial_vote', 'votes': public_votes(initial, first)},
                {'round': 1.5, 'kind': 'live_debate', 'contributions': [
                    {'model': e['model'], 'role': e['role'], 'content_md': e['content_md'], 'event_seq': e['seq']}
                    for e in visible if e['kind'] in ('moderation', 'contribution')]},
                {'round': 2, 'kind': 'final_vote', 'votes': public_votes(final, last)},
            ]}
