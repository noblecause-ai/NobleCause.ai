"""Versioned rotation and append-only event files; no model decides mechanics."""
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path

VERSION = '0.6'
ORDER = (
    'anthropic/claude-fable-5.1', 'openai/gpt-6-astra', 'x-ai/grok-4.6',
    'moonshotai/kimi-k3', 'z-ai/glm-5.3',
)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else encoded(value)).hexdigest()


def atomic_write(path, payload, *, mode=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        if mode is not None:
            os.fchmod(fd, mode)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextlib.contextmanager
def process_lock(root):
    """One lock for weekly decisions, sessions and rotation acceptance."""
    with (Path(root) / '.gremium.lock').open('a') as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Ein anderer Gremium-Lauf hält die Prozesssperre') from None
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def chair_for(config, schedule):
    settings = config['live_council']
    if tuple(settings['rotation']) != ORDER:
        raise ValueError('Unbekannte Vorsitzrotation')
    models = settings['models']
    if len(models) != 5 or {s['model'] for s in models} != set(ORDER):
        raise ValueError('Live-Rat verlangt die fünf genehmigten Sitze')
    state = schedule.get('council_rotation', {})
    if state and state.get('procedure_version') != VERSION:
        raise ValueError('Unbekannte Rotationsversion')
    index = state.get('next_index', 0)
    if type(index) is not int or not 0 <= index < 5:
        raise ValueError('Ungültiger Rotationsindex')
    return next(s for s in models if s['model'] == ORDER[index]), index


def validate_events(record):
    import jsonschema
    schema = json.loads((Path(__file__).resolve().parents[1] / 'schema/live-events.schema.json').read_text())
    jsonschema.validate(record, schema)
    previous = '0' * 64
    for number, event in enumerate(record['events'], 1):
        if event['seq'] != number or event['session_id'] != record['session_id']:
            raise ValueError('Ereignisnummern lückenhaft oder falsche Sitzung')
        if event['content_sha256'] != digest(event['content_md'].encode()):
            raise ValueError('Ereigniswortlaut verändert')
        if event['previous_sha256'] != previous or event['sha256'] != digest({k:v for k,v in event.items() if k != 'sha256'}):
            raise ValueError('Ereignis-Hashkette verändert')
        previous = event['sha256']


class Events:
    def __init__(self, path, session_id, publisher=None):
        self.path = Path(path)
        self.publisher = publisher
        self.record = json.loads(self.path.read_text()) if self.path.exists() else {
            'procedure_version': VERSION, 'session_id': session_id, 'events': [],
        }
        validate_events(self.record)
        if self.record['session_id'] != session_id:
            raise ValueError('Falscher Ereignisstrom')

    def append(self, kind, phase, *, model=None, role='system', text='', data=None):
        # Detect another writer or disk tampering before replacing a snapshot.
        if self.path.exists() and json.loads(self.path.read_text()) != self.record:
            raise ValueError('Ereignisstrom außerhalb dieses Laufs geändert')
        events = self.record['events']
        event = {
            'seq': len(events) + 1, 'session_id': self.record['session_id'],
            'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'kind': kind, 'phase': phase, 'model': model, 'role': role,
            'content_md': text, 'content_sha256': digest(text.encode()), 'data': data or {},
            'previous_sha256': events[-1]['sha256'] if events else '0' * 64,
        }
        event['sha256'] = digest(event)
        candidate = {**self.record, 'events': events + [event]}
        validate_events(candidate)
        atomic_write(self.path, encoded(candidate))
        self.record = candidate
        self.publish()
        return event

    def publish(self):
        if self.publisher is not None:
            self.publisher(self.record)

    def once(self, key, kind, phase, **kwargs):
        """Replaying a completed call never republishes or alters its event."""
        existing = [e for e in self.record['events'] if e['data'].get('step') == key]
        data = {**kwargs.pop('data', {}), 'step': key}
        if existing:
            if len(existing) != 1:
                raise ValueError('Doppelter Ereignisschritt')
            event = existing[0]
            expected = {'kind': kind, 'phase': phase, 'model': kwargs.get('model'),
                        'role': kwargs.get('role', 'system'), 'content_md': kwargs.get('text', ''), 'data': data}
            if any(event[k] != v for k, v in expected.items()):
                raise ValueError('Wiederaufnahme würde ein Ereignis umschreiben')
            return event
        return self.append(kind, phase, data=data, **kwargs)

    def mirror(self, destination):
        """Optional file sink for a future publisher; never run in a dry-run."""
        destination = Path(destination)
        if destination.exists():
            previous = json.loads(destination.read_text())
            validate_events(previous)
            n = len(previous['events'])
            if previous['session_id'] != self.record['session_id'] or previous['events'] != self.record['events'][:n]:
                raise ValueError('Publizierter Ereignisstrom darf nicht ersetzt werden')
        atomic_write(destination, self.path.read_bytes())


def validate_record(directory, session=None):
    import jsonschema
    directory = Path(directory)
    if session is None:
        session = json.loads((directory / 'session.json').read_text())
    schema = json.loads((Path(__file__).resolve().parents[1] / 'schema/session.schema.json').read_text())
    jsonschema.validate(session, schema)
    if session.get('procedure_version') != VERSION:
        raise ValueError('Kein 0.6-Rekord')
    payload = (directory / 'events.json').read_bytes()
    events = json.loads(payload)
    validate_events(events)
    reference = session['event_record']
    if (digest(payload) != reference['sha256'] or len(events['events']) != reference['event_count']
            or events['session_id'] != session['id']):
        raise ValueError('Endrekord und Ereignisstrom stimmen nicht überein')
    indexed = {e['seq']: e for e in events['events']}
    ids = [p['model'] for p in session['participants']]
    if set(ids) != set(ORDER) or len(ids) != 5 or session['chair']['model'] != ORDER[session['chair']['rotation_index']]:
        raise ValueError('Rekord hat eine andere Sitz- oder Vorsitzbesetzung')
    for kind in ('initial_vote', 'final_vote'):
        rounds = [r for r in session['rounds'] if r['kind'] == kind]
        if len(rounds) != 1:
            raise ValueError('Votumsphase fehlt oder doppelt')
        votes = rounds[0]['votes']
        voters = [v['model'] for v in votes]
        if len(set(voters)) != len(voters) or not set(voters) <= set(ids):
            raise ValueError('Ungültige oder doppelte Sitzstimme')
        if session['status'] == 'completed' and set(voters) != set(ids):
            raise ValueError('Erfolgreicher Pilot benötigt fünf gültige Voten')
    counts = dict.fromkeys(ids, 0)
    selected = None
    for event in events['events']:
        if event['kind'] == 'moderation':
            selected = event['data']['next_model_id']
            if (event['model'] != session['chair']['model'] or event['role'] != 'chair'
                    or selected not in ids or counts[selected] != min(counts.values())):
                raise ValueError('Unzulässige Wortvergabe im Ereignisrekord')
        if event['kind'] == 'contribution':
            if event['model'] != selected or event['role'] != 'member' or counts[selected] >= 2:
                raise ValueError('Ungleiche Redeanteile im Ereignisrekord')
            counts[selected] += 1
            selected = None
    for round_ in session['rounds']:
        for item in round_.get('votes', []) + round_.get('contributions', []):
            event = indexed[item['event_seq']]
            if round_['kind'] in ('initial_vote', 'final_vote'):
                vote = next(v for v in event['data']['votes'] if v['model'] == item['model'])
                expected = vote['content_md']
            else:
                expected = event['content_md']
            if item['content_md'].encode() != expected.encode():
                raise ValueError('Feed und Endrekord müssen bytegleichen Wortlaut enthalten')
    if session['status'] == 'completed' and (not session['pilot']['all_five_final_votes_valid'] or events['events'][-1]['kind'] != 'completed'):
        raise ValueError('Erfolgreicher Pilot ohne gültigen Abschluss')
    if session.get('ballot_contract'):
        from ballot_status import check_contract, read_decision
        from run_session import extract_json_block
        check_contract(session['ballot_contract'])
        final_ballots = {}
        for round_ in session['rounds']:
            if round_['kind'] not in ('initial_vote', 'final_vote'):
                continue
            for vote in round_['votes']:
                parsed = extract_json_block(vote['content_md'])
                ballots = parsed.get('recommendations', []) if isinstance(parsed, dict) else []
                if (len(ballots) != 4 or not all(read_decision(b) for b in ballots)
                        or {b.get('pillar') for b in ballots} != set('ABCD')):
                    raise ValueError('Rekord ohne vier explizite Säulenentscheidungen')
                by_pillar = {b['pillar']:b for b in ballots}
                for item in vote['recommendations']:
                    original = by_pillar[item['pillar']]
                    if (item.get('decision') != original['decision']
                            or item.get('abstention_reason') != original['abstention_reason']):
                        raise ValueError('Strukturierte Entscheidung widerspricht dem Rohvotum')
                for b in ballots:
                    if b['decision'] == 'abstain' and not any(i['pillar']==b['pillar'] and i['decision']=='abstain' for i in vote['recommendations']):
                        raise ValueError('Enthaltung fehlt in der strukturierten Anzeige')
                if round_['kind'] == 'final_vote':
                    final_ballots[vote['model']] = by_pillar
        labels = {p['model']:p['label'] for p in session['participants']}
        for rec in session['recommendations']:
            abstentions = sorted([{'model':labels[m], 'reason':b[rec['pillar']]['abstention_reason']}
                for m,b in final_ballots.items() if b[rec['pillar']]['decision']=='abstain'], key=lambda a:a['model'])
            if (rec['abstentions'] != abstentions or rec['votes_abstained'] != len(abstentions)
                    or rec['votes_valid'] + rec['votes_invalid'] + rec['votes_abstained'] != 5
                    or {a['model'] for a in abstentions} & set(rec.get('convergence', {}).get('models', []))):
                raise ValueError('Auszählung behandelt Enthaltungen nicht getrennt')
    return session


def accept_session(root, directory, config):
    """Explicit acceptance only; dry-runs/aborts never consume a rotation slot."""
    root, directory = Path(root), Path(directory)
    with process_lock(root):
        session = validate_record(directory)
        if session.get('dry_run') or session['status'] != 'completed' or not session['pilot']['all_five_final_votes_valid']:
            raise ValueError('Probelauf oder unvollständiger Pilot kann nicht übernommen werden')
        path = root / 'schedule.json'
        schedule = json.loads(path.read_text())
        rotation = schedule.get('council_rotation', {})
        accepted = rotation.get('accepted', {})
        record_hash = digest((directory / 'session.json').read_bytes())
        if session['id'] in accepted:
            if accepted[session['id']] != record_hash:
                raise ValueError('Übernommener Rekord wurde geändert')
            return False
        chair, index = chair_for(config, schedule)
        if session['chair'] != {'model': chair['model'], 'rotation_index': index}:
            raise ValueError('Vorsitzrotation hat sich seit Sitzungsbeginn geändert')
        schedule['council_rotation'] = {**rotation, 'procedure_version': VERSION, 'next_index': (index + 1) % 5,
                                        'accepted': {**accepted, session['id']: record_hash}}
        schedule['last_session'] = session['date']
        schedule['next_session'] = (datetime.date.fromisoformat(session['date']) + datetime.timedelta(days=30)).isoformat() + 'T12:00:00Z'
        atomic_write(path, encoded(schedule))
        return True
