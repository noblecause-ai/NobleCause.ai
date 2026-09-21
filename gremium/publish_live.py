"""Atomic public snapshots and an offline replay; no model calls or record edits.

The destination is a dedicated directory served at /live/. Deploys must neither
delete it nor supply a stale current.json. Per-session files remain available.
"""
import argparse
import copy
import datetime
import json
import re
import shlex
import subprocess
import sys
import threading
import time
from decimal import Decimal
from pathlib import Path

from council_state import atomic_write, encoded, validate_events, digest, process_lock


class PublicationError(RuntimeError):
    pass


# Display continuity approved with the chat mock. These are predecessor symbols,
# not new model commissions; attribution is disclosed separately from the speaker.
PREDECESSOR_SYMBOLS = {
    'anthropic/claude-fable-5.1': 'claude-opus-5',
    'openai/gpt-6-astra': 'gpt-5.6-sol',
}


def validate_destination(destination, source, root):
    destination, source, root = map(lambda p: Path(p).resolve(), (destination, source, root))
    if (destination.is_relative_to(source) or source.is_relative_to(destination)
            or destination == root or root.is_relative_to(destination)
            or any(destination.is_relative_to(root / p) for p in ('sessions', 'journal', 'commissions', 'site/static'))):
        raise ValueError('Live-Feed braucht ein getrenntes, nicht versioniertes Zielverzeichnis')
    return destination


def public_session(descriptor, registry=None):
    session_id = descriptor['id']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', session_id):
        raise ValueError('Sitzungs-ID ist kein einfacher Dateiname')
    registry = {m['model']: m for m in (registry or {}).get('models', [])}
    participants = []
    for model in descriptor['config']['models']:
        item = {k: model[k] for k in ('model', 'label', 'family')}
        item.update({k: model['openrouter'][k] for k in ('endpoint', 'provider_name', 'quantization')})
        symbol_model = model['model'] if model['model'] in registry else PREDECESSOR_SYMBOLS.get(model['model'])
        asset = registry.get(symbol_model, {}).get('asset')
        if asset and re.fullmatch(r'/media/medallions/[a-zA-Z0-9._-]+\.avif', asset):
            item.update(medallion=asset.replace('.avif', '-lo.avif'), medallion_source_model=symbol_model)
        participants.append(item)
    return {**{k: descriptor[k] for k in ('id', 'number', 'date', 'title', 'question', 'chair')},
            'procedure_version': '0.6', 'participants': participants}


def public_costs(record):
    """Only evidenced costs visible by this event; never expose hidden votes."""
    seen, totals = set(), {}
    confirmed = Decimal(0)
    for event in record['events']:
        data = event['data']
        for key in ('spent_usd', 'spent_usd_confirmed'):
            if data.get(key) is not None:
                amount = Decimal(str(data[key]))
                if not amount.is_finite() or amount < 0:
                    raise ValueError('Ungültiger bestätigter Kostenstand')
                confirmed = max(confirmed, amount)
        sources = [(event['model'], data.get('provenance'))]
        sources += [(v['model'], v.get('provenance')) for v in data.get('votes', [])]
        for model, proof in sources:
            if not proof or proof.get('cost_basis') != 'billed':
                continue
            generation = proof['generation_id']
            if generation in seen:
                continue
            seen.add(generation)
            amount = Decimal(str(proof['cost']))
            if not amount.is_finite() or amount < 0:
                raise ValueError('Ungültiger Kostenbeleg')
            totals[model] = totals.get(model, Decimal(0)) + amount
    assigned = sum(totals.values(), Decimal(0))
    return {'total_usd': str(max(confirmed, assigned)),
            'by_model': [{'model': model, 'usd': str(value)} for model, value in totals.items()],
            'unassigned_usd': str(max(Decimal(0), confirmed - assigned)),
            'unresolved': bool(record['events'] and record['events'][-1]['data'].get('costs_may_be_unresolved'))}


class FilePublisher:
    def __init__(self, destination, session, *, mode='pilot'):
        if mode not in ('live', 'pilot', 'replay'):
            raise ValueError('Unbekannter Veröffentlichungsmodus')
        self.destination = Path(destination)
        self.session = copy.deepcopy(session)
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', session['id']):
            raise ValueError('Ungültige Sitzungs-ID')
        self.mode = mode
        self.record = None
        self.failure = None
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.thread = None

    def _write(self, record):
        validate_events(record)
        if record['session_id'] != self.session['id']:
            raise ValueError('Falsche Sitzung im Publisher')
        directory = self.destination / 'sessions' / self.session['id']
        event_path = directory / 'events.json'
        if event_path.exists():
            archive = json.loads(event_path.read_text())
            validate_events(archive)
            if (archive['session_id'] != record['session_id']
                    or archive['events'] != record['events'][:len(archive['events'])]):
                raise ValueError('Der publizierte Ereignisrekord darf nicht umgeschrieben werden')
        previous_path = directory / 'snapshot.json'
        if previous_path.exists():
            previous = json.loads(previous_path.read_text())
            validate_events(previous['record'])
            old = previous['record']['events']
            if (previous['session'] != self.session or previous['mode'] != self.mode
                    or old != record['events'][:len(old)]):
                raise ValueError('Ein publizierter Verlauf darf nicht umgeschrieben oder verkürzt werden')
        current = self.destination / 'current.json'
        if current.exists():
            active = json.loads(current.read_text())
            if active['session']['id'] != self.session['id']:
                if self.record is not None:
                    raise ValueError('Der aktive Zeiger gehört inzwischen zu einer anderen Sitzung')
                tail = active['record']['events'][-1:]
                if not tail or tail[0]['kind'] not in ('completed', 'aborted'):
                    raise ValueError('Eine andere Sitzung ist noch aktiv')
        snapshot = {'schema_version': 1, 'mode': self.mode, 'session': self.session,
                    'published_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'record': record, 'costs': public_costs(record)}
        # Exact original event encoding; the UI is a projection, not a replacement.
        atomic_write(event_path, encoded(record), mode=0o644)
        payload = encoded(snapshot)
        atomic_write(previous_path, payload, mode=0o644)
        atomic_write(current, payload, mode=0o644)

    def __call__(self, record):
        with self.lock:
            if self.failure is not None:
                raise PublicationError('Live-Publikation unterbrochen; keine weiteren Modellaufrufe') from self.failure
            try:
                self._write(record)
                self.record = copy.deepcopy(record)
            except Exception as exc:
                self.failure = exc
                raise PublicationError('Live-Publikation fehlgeschlagen; lokaler Ereignisrekord bleibt erhalten') from exc

    def start(self, interval=15):
        """A stale heartbeat is distinguishable from a long model response."""
        if self.thread is not None:
            return
        def heartbeat():
            while not self.stop.wait(interval):
                with self.lock:
                    if self.record is None or self.failure is not None:
                        continue
                    try:
                        self._write(self.record)
                    except Exception as exc:
                        self.failure = exc
        self.thread = threading.Thread(target=heartbeat, daemon=True, name='council-feed')
        self.thread.start()

    def close(self):
        self.stop.set()
        if self.thread is not None:
            self.thread.join(timeout=2)


class SshPublisher(FilePublisher):
    """The same file contract on the existing VPS, acknowledged before inference."""
    def __init__(self, destination, session, *, host, identity=None, mode='live',
                 runtime='/home/noblecause/council-runtime', remote_destination='/srv/noblecause/live'):
        super().__init__(destination, session, mode=mode)
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.@-]*', host):
            raise ValueError('Ungültiger SSH-Host')
        self.command = ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=10']
        if identity:
            self.command += ['-i', str(identity), '-o', 'IdentitiesOnly=yes']
        self.command += [host, shlex.join([runtime + '/venv/bin/python', runtime + '/gremium/publish_live.py',
                                          '--receive', '--destination', remote_destination])]

    def _write(self, record):
        super()._write(record)
        request = {'session': self.session, 'mode': self.mode, 'record': record,
                   'continuing': self.record is not None}
        result = subprocess.run(self.command, input=encoded(request), capture_output=True, timeout=30, check=True)
        acknowledgement = json.loads(result.stdout)
        if acknowledgement != {'session_id': self.session['id'], 'sha256': digest(encoded(record))}:
            raise ValueError('VPS bestätigt einen anderen Ereignisrekord')


def receive(destination, request):
    """Authenticated SSH input only; all local invariants apply under one VPS lock."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with process_lock(destination):
        current = destination / 'current.json'
        if request.get('continuing') and current.exists():
            if json.loads(current.read_text())['session']['id'] != request['session']['id']:
                raise ValueError('Der aktive Zeiger gehört inzwischen einer anderen Sitzung')
        publisher = FilePublisher(destination, request['session'], mode=request['mode'])
        publisher(request['record'])
        return {'session_id': request['session']['id'], 'sha256': digest(encoded(request['record']))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', type=Path, help='Vorhandener Sitzungsordner mit run-input.json und events.json')
    parser.add_argument('--receive', action='store_true', help='Geprüften Snapshot über authentifiziertes SSH-stdin empfangen')
    parser.add_argument('--destination', type=Path, required=True, help='Eigenes Verzeichnis, lokal z. B. site/build/live')
    parser.add_argument('--replay', action='store_true', help='Vorhandene Ereignisse zeitlich gestaffelt wiedergeben')
    parser.add_argument('--interval', type=float, default=2, help='Sekunden zwischen Originalereignissen')
    parser.add_argument('--through', type=int, help='Nur diesen ursprünglichen Ereignisstand ausgeben')
    args = parser.parse_args()
    if args.receive:
        print(json.dumps(receive(args.destination, json.load(sys.stdin))))
        return
    if args.source is None:
        parser.error('Quellordner fehlt')
    if args.interval < .1 or args.interval > 60:
        parser.error('--interval muss zwischen 0.1 und 60 liegen')
    record = json.loads((args.source / 'events.json').read_text())
    validate_events(record)
    descriptor = json.loads((args.source / 'run-input.json').read_text())
    root = Path(__file__).resolve().parents[1]
    try:
        destination = validate_destination(args.destination, args.source, root)
    except ValueError as exc:
        parser.error(str(exc))
    total = len(record['events']) if args.through is None else args.through
    if not 1 <= total <= len(record['events']):
        parser.error('--through liegt außerhalb des Ereignisrekords')
    publisher = FilePublisher(destination, public_session(descriptor, json.loads((root / 'models.json').read_text())), mode='replay')
    for length in (range(1, total + 1) if args.replay else [total]):
        publisher({**record, 'events': record['events'][:length]})
        if args.replay and length < total:
            time.sleep(args.interval)
    print(f"Wiedergabe: {total} Originalereignisse, keine Modellaufrufe. Ziel: {destination}")


if __name__ == '__main__':
    main()
