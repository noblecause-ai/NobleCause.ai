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
    if (os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch'
            and os.environ.get('GITHUB_REF') == 'refs/heads/codex/receipt-recheck-20261104'
            and os.environ.get('GITHUB_REPOSITORY') == 'noblecause-ai/NobleCause.ai'):
        # A receipt lookup is never a production readiness check.
        path = Path('gremium/.probe-raw/receipt-recheck/reconciliation.json')
        receipt = json.loads(path.read_text()) if path.exists() else {}
        data = {'purpose': 'receipt_reconciliation',
                'receipt_status': receipt.get('status', 'not_checked'),
                'production_readiness': 'not_checked', 'inference_calls': 0,
                'generation_id': receipt.get('generation_id'),
                'billed_usd': receipt.get('billed_usd'),
                'receipt_error_code': receipt.get('receipt_error_code'),
                'originals_unchanged': receipt.get('originals_unchanged'),
                'key_after': receipt.get('key_after'),
                'checked_at': receipt.get('checked_at')}
        Path('preflight-status.json').write_text(json.dumps(data, indent=2, default=str)+'\n')
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a') as stream:
                stream.write('## Einmaliger Abrechnungsabruf\n\nNur GET; kein Modellaufruf, keine Produktionsfreigabe.\n\n```json\n' + json.dumps(data, indent=2, default=str) + '\n```\n')
        print(json.dumps(data, default=str))
    else:
        main()
