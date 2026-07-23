# NobleCause SOL build (nachgebessert)

Statischer, datengetriebener Startseiten-Prototyp. **Nachbesserungsstand:** siehe
`NACHBESSERUNG.md`. Liest die **echten** Backend-Daten (kein Beispiel-`sitzung.json` mehr).

## Bauen

```bash
python build.py            # braucht jsonschema
python -m http.server 8000
```

Danach `http://localhost:8000/` öffnen.

`build.py` liest die jüngste Sitzung aus `../sessions/<id>/session.json`, die Registry
aus `../organizations.json` und Präsentations-Konstanten aus `frontend-config.json`,
validiert gegen das kanonische `../schema/session.schema.json` und erzeugt `index.html`.
**Das Frontend parst nie Prosa** — Protokollspalten und Revisionen kommen aus den
strukturierten Voten (`rounds[].votes[].recommendations[]`). Der Kartentext „was die
Org tut" kommt aus `organizations.json.beschreibung`; es gibt **kein** erfundenes
„Warum". JavaScript ist nur Kür für Reiter und Tastatursteuerung.

## Verwendete Felder aus dem Sitzungs-Schema

- Grunddaten: `id`, `number`, `date`, `title`, `question`, `summary`
- Modelle: `participants[]`
- Beratungsrunden: `rounds[]`, insbesondere `initial_vote` und `final_vote`
- Ergebnis: `recommendations[]`
- Einigkeit: `has_consensus`, `convergence.count`, `convergence.total`
- Vorbehalte: `convergence.conditional_count`, `convergence.votes[].reservation`
- Uneinigkeit: `individual_votes[]`
- Spendenwege: `donation_url`
- Kosten: `costs.total`, `costs.by_model[]`
- Transparenz: `dissent_md`, `correction_notice`

Die führende Empfehlung wird nicht redaktionell ausgewählt. Die Regel lautet: höchster Stimmenanteil, danach höhere Konfidenz, danach Säule A bis D.

## JavaScript ist nur Kür

Ohne JavaScript bleiben sichtbar und nutzbar:

- alle vier Empfehlungen mit direkten Links
- alle drei Modelle in beiden Runden
- sichtbare Meinungsänderungen
- Ergebnis und Kosten
- frühere Sitzungen
- sämtliche Sprunglinks

Mit JavaScript werden lediglich die drei Protokollteile als zugängliche Reiter bedienbar. Pfeiltasten, Pos1 und Ende funktionieren im Reiterband.

## Lücken im Datenvertrag

Das Schema aus PR #10 heißt dort `session.schema.json`; als Alias für den Bauauftrag liegt dieselbe Fassung hier unter `sitzung.schema.json`. Das Schema enthält die Rohtexte der Voten nur als `content_md`. Daraus kann das Frontend eine konkrete Meinungsänderung nicht zuverlässig und deterministisch ableiten. Für diesen Prototyp besitzen die Voten deshalb zusätzlich strukturierte `recommendations[]`. Das ist durch `additionalProperties: true` schema-valid, sollte aber im gemeinsamen Datenvertrag ausdrücklich festgelegt werden.

Das Sitzungs-Schema enthält außerdem kein Archiv früherer Sitzungen. Damit trotzdem nur eine JSON-Datei benötigt wird, liegt die Registerliste vorläufig unter `presentation.archive`. Für die Integration sollte sie aus einer separaten, buildseitig erzeugten Sitzungsübersicht kommen oder Teil eines klar definierten Startseiten-Datenvertrags werden.

Die Begriffe und Symbole der vier Säulen liegen vorläufig unter `presentation.pillar_labels` und `presentation.pillar_symbols`. Sie sind Darstellungsmetadaten, keine Beratungsdaten.

## Assets

- `site/static/ratssaal.png`
- `site/static/vorraum.png`

Die Zählmaschine wird im Prototyp als kleine CSS-Ebene über dem vorhandenen Ratssaal-Plate ergänzt, weil das verfügbare Einzelbild noch die ältere, leere Mitte zeigt.

## Barrierefreiheit

- sichtbarer Sprunglink
- semantische Überschriften und Landmarken
- Mindesthöhe von 48 px für zentrale Links und Reiter
- Tastatursteuerung der Reiter
- `prefers-reduced-motion`
- Modus für erhöhten Kontrast
- keine externen Schriften, Tracker oder CDNs
- auf Mobilgeräten steht die Antwort vor der Rauminszenierung

## Zustände

Der Renderer trägt drei Ergebnisformen:

1. Einigkeit
2. Einigkeit mit Vorbehalt
3. Keine Einigung mit gleichwertigen Einzelvoten und jeweils eigenem Spendenlink

Die aktuelle Sitzung zeigt die ersten beiden Formen. Die Archivzeile der ersten Sitzung zeigt Uneinigkeit als normales Ergebnis. `tests/test_render_states.py` prüft zusätzlich die dritte Kartenform direkt am Renderer.
