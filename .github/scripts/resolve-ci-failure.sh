#!/usr/bin/env bash

# Schliesst nach einem erfolgreichen Workflow-Lauf offene, labelgebundene
# Betriebsalarme. Issue-Pflege ist Beobachtbarkeit, nicht der fachliche Lauf:
# Ein temporaerer GitHub-API-Fehler darf einen gruenen Lauf nicht rot machen.

set -u

LABEL="${1:?Issue-Label fehlt}"
RUN_URL="${2:?Run-URL fehlt}"
KIND="${3:-failure}"

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

if [ "$KIND" = "due" ]; then
  BODY="Automatischer Sitzungsabschluss bestätigt: Der scharfe Lauf $RUN_URL hat einen neuen Sitzungsrekord veröffentlicht. Die Fälligkeit ist damit erledigt; ein künftiger Termin wird wieder unter dem Label \`$LABEL\` gemeldet."
else
  BODY="Automatische Erholung bestätigt: Der Lauf $RUN_URL wurde erfolgreich abgeschlossen. Dieses Altalarm-Issue wird geschlossen; ein künftiger neuer Fehler wird wieder unter dem Label \`$LABEL\` gemeldet."
fi

while IFS= read -r NUMBER; do
  [ -n "$NUMBER" ] || continue
  if gh issue close "$NUMBER" --reason completed --comment "$BODY"; then
    echo "Altalarm #$NUMBER ($LABEL) geschlossen."
  else
    echo "::warning::Altalarm #$NUMBER ($LABEL) konnte nicht geschlossen werden; der fachliche Lauf bleibt gruen."
  fi
done <<< "$NUMBERS"
