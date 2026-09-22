#!/usr/bin/env bash
set -euo pipefail
# Existing dedicated deploy identity/host pin, no API key on the VPS.
export RSYNC_RSH='ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10'
remote='noblecause@185.143.100.222'
runtime='/home/noblecause/council-runtime'
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 "$remote" \
  "test -x '$runtime/venv/bin/python' && test -w /srv/noblecause/live && mkdir -p '$runtime/gremium' '$runtime/schema'"
rsync -az gremium/publish_live.py gremium/council_state.py "$remote:$runtime/gremium/"
rsync -az schema/live-events.schema.json "$remote:$runtime/schema/"
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 "$remote" \
  "cd '$runtime/gremium' && ../venv/bin/python -c 'import publish_live, jsonschema; print(\"SSH-Publisher und Schema-Validator bereit\")'"
