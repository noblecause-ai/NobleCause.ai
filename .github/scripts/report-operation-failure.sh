#!/usr/bin/env bash
set -euo pipefail
label='ci-failure:regular-operation'
gh label create "$label" --color B60205 --description 'Autonomer Ratsbetrieb braucht Prüfung' 2>/dev/null || true
number=$(gh issue list --label "$label" --state open --limit 1 --json number --jq '.[0].number // empty')
# One open alarm suffices; repeated free checks must not send daily comments.
if [ -n "$number" ]; then
  echo "Betriebsalarm #$number bleibt offen; keine erneute Benachrichtigung."
  exit 0
fi
python3 - <<'PY'
import os
from pathlib import Path
url=f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
log=Path('run.log').read_text()[-3000:] if Path('run.log').exists() else '(kein Log)'
Path('operation-failure.md').write_text(f'Autonomer Ratsbetrieb unterbrochen: {url}\n\nRohbelege bleiben erhalten. Fehlgeschlagene Modellaufrufe werden nicht automatisch wiederholt. Nach einem begonnenen Lauf ist die Betriebssperre in schedule.json zu prüfen; bloße Anschlussfehler werden kostenlos erneut geprüft.\n\n```text\n{log}\n```\n')
PY
gh issue create --title 'Regelbetrieb: Prüfung erforderlich' --label "$label" --body-file operation-failure.md
