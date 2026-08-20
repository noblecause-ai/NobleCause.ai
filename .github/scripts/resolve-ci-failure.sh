#!/usr/bin/env bash

# Schliesst nach einem erfolgreichen Workflow-Lauf dessen offene Altalarme.
# Issue-Pflege ist Beobachtbarkeit, nicht der fachliche Lauf: Ein temporaerer
# GitHub-API-Fehler darf einen gruenen Wart-/Session-/Deploy-Lauf nicht rot machen.

set -u

LABEL="${1:?ci-failure-Label fehlt}"
RUN_URL="${2:?Run-URL fehlt}"

if ! NUMBERS=$(gh issue list \
  --label "$LABEL" \
  --state open \
  --limit 100 \
  --json number \
  --jq '.[].number'); then
  echo "::warning::Offene Issues fuer $LABEL konnten nicht gelesen werden; der fachliche Lauf bleibt gruen."
  exit 0
fi

if [ -z "$NUMBERS" ]; then
  echo "Kein offener Altalarm fuer $LABEL."
  exit 0
fi

BODY="Automatische Erholung bestätigt: Der Lauf $RUN_URL wurde erfolgreich abgeschlossen. Dieses Altalarm-Issue wird geschlossen; ein künftiger neuer Fehler wird wieder unter dem Label \`$LABEL\` gemeldet."

while IFS= read -r NUMBER; do
  [ -n "$NUMBER" ] || continue
  if gh issue close "$NUMBER" --reason completed --comment "$BODY"; then
    echo "Altalarm #$NUMBER ($LABEL) geschlossen."
  else
    echo "::warning::Altalarm #$NUMBER ($LABEL) konnte nicht geschlossen werden; der fachliche Lauf bleibt gruen."
  fi
done <<< "$NUMBERS"
