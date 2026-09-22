#!/usr/bin/env python3
"""Fälligkeit steuert vorhandene Läufe; keine Modellentscheidung über Mechanik.

GitHub hält die gemeinsame Prozesssperre vom Checkout bis zum Push. Dieser
Controller erfindet keine Fragen, wiederholt keine Inferenz und verändert keine
historischen Rekorde. --check-only ist auch in Produktion ohne Modellaufrufe.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from council_state import atomic_write, chair_for, encoded
from process_config import configured_scouts, feature_enabled

ROOT = Path(__file__).resolve().parents[1]


def configuration(config):
    policy = config.get('regular_operation') or {}
    speech = policy.get('speech_policy') or {}
    if (policy.get('enabled') is not True or policy.get('cost_mode') != 'observe'
            or not feature_enabled(config, 'live_council') or not feature_enabled(config, 'three_scouts')
            or not all(isinstance(policy.get(k), str) and policy[k].strip() for k in ('question', 'title'))
            or speech.get('scope') != 'regular_operation' or speech.get('procedure_version') != '0.6'
            or speech.get('amendment_version') != '0.6-speech-limit-2'
            or speech.get('prompt_limit') != 180 or speech.get('max_words') != 200
            or not speech.get('approved_on') or not speech.get('authorization_reference')):
        raise ValueError('Kein freigegebener Regelbetrieb konfiguriert')
    configured_scouts(config)
    return policy


def timestamp(value):
    date = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if date.tzinfo is None:
        raise ValueError('Fälligkeit braucht eine Zeitzone')
    return date


def owner():
    run = os.environ.get('GITHUB_RUN_ID')
    attempt = os.environ.get('GITHUB_RUN_ATTEMPT')
    if not run or not attempt:
        raise RuntimeError('Regelbetrieb braucht eine eindeutige GitHub-Laufkennung')
    return run + '.' + attempt


def plan(root, config, kind, now=None, *, reserved=False):
    root = Path(root)
    configuration(config)
    schedule = json.loads((root/'schedule.json').read_text())
    blocked = (schedule.get('regular_operation') or {}).get('blocked')
    if blocked:
        raise RuntimeError('Regelbetrieb nach unvollständigem Lauf angehalten; Belege und Betriebsalarm prüfen')
    inflight = (schedule.get('regular_operation') or {}).get('inflight')
    if inflight and (not reserved or inflight.get('owner') != owner() or inflight.get('kind') != kind):
        raise RuntimeError('Ein begonnener Lauf ist noch nicht abgeschlossen; keine bezahlte Wiederholung')
    if reserved and not inflight:
        raise RuntimeError('Keine vorab veröffentlichte Laufreservierung')
    now = now or dt.datetime.now(dt.timezone.utc)
    due = schedule['next_research' if kind == 'research' else 'next_session']
    chair, index = chair_for(config, schedule)
    result = {'kind':kind, 'due':due, 'ready':now >= timestamp(due),
              'chair':chair['model'], 'rotation_index':index}
    if not result['ready']:
        return result
    if kind == 'research':
        target = root/'journal'/now.date().isoformat()
        if target.exists():
            raise RuntimeError('Fälliger Wochenlauf hat bereits Artefakte; keine automatische Wiederholung')
        result['date'] = now.date().isoformat()
    else:
        # ID follows the due date, never the runner/retry date.
        sid = timestamp(due).date().isoformat() + '-regular'
        if (root/'sessions'/sid).exists():
            raise RuntimeError('Fällige Sitzung hat bereits Artefakte; keine automatische Wiederholung')
        candidates = []
        from live_session import dossier_context
        for path in (root/'journal').glob('*/entry.json'):
            entry = json.loads(path.read_text())
            if entry.get('research_mode') != 'blind_then_compare':
                continue
            try:
                dossier_context(root, config, path, now.date().isoformat())
            except ValueError:
                continue
            candidates.append((entry['date'], path))
        if not candidates:
            raise RuntimeError('Kein höchstens sieben Tage altes, vollständiges Drei-Scout-Dossier verfügbar')
        date, dossier = max(candidates, key=lambda row:(row[0],str(row[1])))
        result.update(session_id=sid, dossier=str(dossier.relative_to(root)), research_date=date)
    return result


def reserve(root, task):
    path = Path(root)/'schedule.json'
    schedule = json.loads(path.read_text())
    state = schedule.setdefault('regular_operation', {})
    if state.get('inflight') or state.get('blocked'):
        raise RuntimeError('Regelbetrieb bereits reserviert oder gesperrt')
    state['inflight'] = {'owner':owner(), 'kind':task['kind'], 'due':task['due']}
    atomic_write(path, encoded(schedule))


def finish(root):
    path = Path(root)/'schedule.json'
    schedule = json.loads(path.read_text())
    state = schedule['regular_operation']
    if state['inflight']['owner'] != owner():
        raise RuntimeError('Fremde Laufreservierung darf nicht abgeschlossen werden')
    state['last_completed'] = state.pop('inflight')
    atomic_write(path, encoded(schedule))


def block(root, kind, error_type):
    """Persist only controlled diagnostics, never exception text or credentials."""
    path = Path(root)/'schedule.json'
    schedule = json.loads(path.read_text())
    state = schedule.setdefault('regular_operation', {})
    state.setdefault('blocked', {'kind':kind, 'error_type':error_type,
        'at':dt.datetime.now(dt.timezone.utc).isoformat(), 'actions_run_id':os.environ.get('GITHUB_RUN_ID')})
    atomic_write(path, encoded(schedule))


def execute(root, config, task):
    """Existing adapters remain the only route to paid calls."""
    import openrouter_scout
    root = Path(root)
    policy = configuration(config)
    cap = openrouter_scout.amount(openrouter_scout.key_state()['limit_remaining']) * openrouter_scout.amount(config['fx_rate_usd_eur'])
    base = [sys.executable]
    if task['kind'] == 'research':
        command = base + [str(root/'gremium/run_wart.py'), '--date', task['date'], '--observe-costs', '--budget-cap', str(cap)]
    else:
        command = base + [str(root/'gremium/run_session.py'), '--live-council', '--public-session',
            '--regular-operation', '--observe-costs', '--budget-cap',str(cap),
            '--question',policy['question'],'--title',policy['title'], '--session-id',task['session_id'],
            '--dossier-json',str(root/task['dossier']), '--live-feed-dir',str(root/'.automation/live'),
            '--live-feed-ssh','noblecause@185.143.100.222']
    subprocess.run(command, cwd=root, check=True)
    if task['kind'] == 'session':
        # Keep the paid Scout originals alongside the reused dossier.
        source = (root/task['dossier']).parent/'raw'
        destination = root/'sessions'/task['session_id']/'research-raw'
        if source.is_dir():
            shutil.copytree(source, destination)
    subprocess.run(base + [str(root/'gremium/schema_gate.py'),'all'], cwd=root, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', choices=['research','session'], required=True)
    parser.add_argument('--plan-only', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--reserve', action='store_true')
    parser.add_argument('--reserved', action='store_true')
    args = parser.parse_args(argv)
    config = json.loads((ROOT/'gremium/config.json').read_text())
    task = plan(ROOT, config, args.kind, reserved=args.reserved)
    print(json.dumps(task,ensure_ascii=False),flush=True)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a') as stream:
            stream.write('ready=' + str(task['ready']).lower() + '\n')
    if args.plan_only or args.check_only or not task['ready']:
        return
    if args.reserve:
        reserve(ROOT, task)
        return
    if not args.reserved:
        parser.error('Bezahlter Betrieb benötigt eine zuvor committete --reserve und --reserved')
    try:
        from envtools import load_env
        load_env(ROOT/'gremium', ROOT)
        execute(ROOT, config, task)
        finish(ROOT)
    except BaseException as exc:
        block(ROOT, args.kind, type(exc).__name__)
        raise


if __name__ == '__main__':
    main()
