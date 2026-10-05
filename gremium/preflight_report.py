"""Read-only monitor report. Never changes the strict execution preflight."""
import datetime as dt
import html
import json
import os
from pathlib import Path


def report(outcome, remaining, log):
    # Use the step's original outcome, NOT its continue-on-error conclusion.
    status = {'success': 'ready', 'failure': 'not_ready'}.get(outcome, 'not_checked')
    data = {'check_status': status, 'probe_outcome': outcome,
            'remaining_credits': remaining or None, 'inference_calls': 0,
            'checked_at': dt.datetime.now(dt.timezone.utc).isoformat()}
    title = {'ready': 'Anschlussprüfung bestanden', 'not_ready': 'Anschluss aktuell nicht freigegeben',
             'not_checked': 'Anschlussprüfung nicht abgeschlossen'}[status]
    summary = (f'## {title}\n\n'
               'Stiller Statusbericht; keine Modellaufrufe. Der Workflow-Abschluss bestätigt '
               'keine Freigabe für bezahlte Läufe. Diese prüfen alle benötigten Anschlüsse '
               'und das Budget weiterhin strikt vor der ersten Zahlung.\n\n'
               f'Verbleibende Credits: {html.escape(remaining) if remaining else "nicht ermittelt"}.\n\n'
               f'<details><summary>Prüfprotokoll</summary><pre>{html.escape(log[-20000:])}</pre></details>\n')
    return data, summary


def main():
    log = Path('run.log').read_text() if Path('run.log').exists() else 'Kein Prüfprotokoll vorhanden.'
    data, summary = report(os.environ.get('PREFLIGHT_OUTCOME', ''),
                           os.environ.get('REMAINING_CREDITS', ''), log)
    Path('preflight-status.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a') as stream:
            stream.write(summary)
    print(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    main()
