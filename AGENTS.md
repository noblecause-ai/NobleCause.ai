# AGENTS.md — Arbeitsregeln für NobleCause.ai

Dieses Dokument gilt für alle Agenten, die in diesem Repository arbeiten.

## Aktueller Auftrag

Der produktive Stand liegt auf `master`. Die drei statischen Räume und die
Rekordmaschine sind live; aktuell folgen Betriebsfestigkeit 0.4.1 und danach die
Deliberationsform 0.5 hinter einem standardmäßig ausgeschalteten Schalter.

Arbeitsbaum für Builds, Tests und Commits:
`~/Projects/nc-sanitize`. `~/Projects/NobleCause.ai` ist der kanonische
Hauptbaum. Beide teilen dasselbe Git-Repository. Andere Projekte unter
`~/Projects` gehören nicht zu NobleCause.ai und werden nicht angefasst.

## Rollen

- **Steward:** menschliche Letztinstanz; genehmigt Rekordkorrekturen, echte
  API-Läufe, Commit und Push.
- **Wart:** entscheidet über Rekordsemantik und öffentliche Verfahrenstexte.
- **Architekt:** priorisiert, entwirft, implementiert kleine klar begrenzte
  Änderungen und nimmt Baupakete ab.
- **CC:** führt größere oder unabhängig zu prüfende Baupakete aus.

Kleine deterministische Änderungen brauchen keine eigene Übergabekette. Bei
unerwartetem Zustand wird gestoppt und berichtet, nicht geraten.

## Rekordgrenzen

- `sessions/**`, `journal/**` und `commissions/**` sind veröffentlichte
  Rekorde. Rohantworten und publizierte Prosa werden nie umgeschrieben.
- Additive Korrekturhinweise oder deterministische Backfills abgeleiteter
  Strukturfelder benötigen einen belegten Präzedenzfall und Steward-Freigabe.
- `models.json` ist eine additive Registratur. Bestehende Einträge bleiben
  objektgleich; neue Epochen werden angehängt.
- Organisationsidentität kommt ausschließlich aus `organizations.json`.
  Kein Fuzzy-Matching und keine Identität aus freier Prosa.
- `next-session.json` ist Steward-Vorbereitung und keine automatische
  Dispatch-Eingabe. Frage und Titel werden beim echten Lauf ausdrücklich
  übergeben.
- `schedule.json` ist maschinengeschrieben. Schreibwege müssen unbekannte
  Felder erhalten.

## Technische Grenzen

- Die Site unter `site/` rendert vorhandene strukturierte Daten und aggregiert
  niemals selbst.
- Rekordtext bleibt in der Originalsprache. Die englische Site übersetzt keine
  Sitzungsprosa, Voten oder Korrekturhinweise maschinell.
- Fehlende Zulieferungen dürfen keinen stillen Ersatzinhalt erzeugen.
  Technische Fehler bleiben laut; explizite Modell-Verweigerungen werden als
  solche geführt.
- Prompts und Schemas werden nur im ausdrücklich freigegebenen Slice geändert.
- Neue Mechanismen werden nur gebaut, wenn vorhandene Infrastruktur die
  Anforderung nicht trägt.

## Abnahme

Im aktiven Arbeitsbaum:

```bash
gremium/.venv/bin/python -m pytest -p no:cacheprovider gremium/tests
gremium/.venv/bin/python gremium/schema_gate.py all
npm --prefix site test
npm --prefix site run build
git diff --check
```

Tests und Sichtprüfung werden proportional zum Risiko gewählt. API-Calls,
Rekordschreiben und Deploys werden nicht als bloße Tests ausgeführt.

## Git und Auslieferung

- Fremde oder unerklärte Änderungen bleiben unangetastet.
- Kein History-Rewrite und kein Force-Push.
- Commit nur nach Steward-Freigabe; Push nach `master` nur nach ausdrücklicher
  Freigabe und FF-only.
- Ein Push nach `master` löst den Produktions-Deploy aus.
- Temporäre Aufträge, Reviews und Chat-Übergaben werden nicht automatisch
  versioniert. Ins Repo gehören kanonische Entscheide, notwendige Provenienz
  und dauerhafte Betriebsdokumentation.
