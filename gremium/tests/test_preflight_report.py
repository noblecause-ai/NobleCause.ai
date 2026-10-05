"""A successful report must never misrepresent a failed or missing probe."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

GREMIUM = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('outcome,expected', [
    ('success', 'ready'), ('failure', 'not_ready'), ('skipped', 'not_checked'),
    ('cancelled', 'not_checked'), ('', 'not_checked'),
])
def test_report_preserves_diagnostic_outcome_without_alarm(tmp_path, outcome, expected):
    if outcome != 'skipped':
        (tmp_path/'run.log').write_text('completion: 14 > 13 USD/1M tokens; no inference\n<untrusted>')
    summary = tmp_path/'summary.md'
    env = {**os.environ, 'PREFLIGHT_OUTCOME': outcome, 'REMAINING_CREDITS': '15.965438716',
           'GITHUB_STEP_SUMMARY': str(summary)}
    result = subprocess.run([sys.executable, str(GREMIUM/'preflight_report.py')],
                            cwd=tmp_path, env=env, capture_output=True, text=True)
    assert result.returncode == 0
    data = json.loads((tmp_path/'preflight-status.json').read_text())
    assert data['check_status'] == expected
    assert data['probe_outcome'] == outcome
    assert data['remaining_credits'] == '15.965438716'
    assert data['inference_calls'] == 0
    text = summary.read_text()
    assert '<untrusted>' not in text
    if outcome == 'failure':
        assert 'Anschluss aktuell nicht freigegeben' in text
        assert 'completion: 14 &gt; 13' in text
    if outcome == 'skipped':
        assert 'Kein Prüfprotokoll vorhanden' in text
