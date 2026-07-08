# sessions/ — Deliberations-Protokolle

Jede Gremium-Sitzung ist ein Ordner `YYYY-MM/` (bei mehreren Sitzungen pro Monat:
Suffix ohne Extra-Bindestrich, z. B. `2026-07b`, `2026-07c`).
Git ist die Datenbank: Ein Protokoll gilt als veröffentlicht, sobald es auf `master` liegt.
Die Site rendert alles unter `sessions/` zur Build-Zeit automatisch.

## Struktur eines Sitzungsordners

```
sessions/2026-07/
├── session.json   # das maschinenlesbare Protokoll (Schema unten)
└── raw/           # Rohartefakte des Laufs
    ├── r1-anthropic.json
    ├── r1-openai.json
    ├── r1-google.json
    ├── r2-anthropic.json
    ├── r2-openai.json
    ├── r2-google.json
    ├── summary-anthropic.json   # Standardmodus
    ├── summary-wart.json        # Wart-Leitung
    ├── r0-opening.json          # Wart-Leitung
    ├── r0-wart.json             # Wart-Dossier (mit Web-Suche)
    ├── moderation-wart.json     # Wart-Moderation nach Runde 1
    └── prompt-*.txt             # mitveröffentlichte Prompt-Artefakte
```

## Schema `session.json` (Version 2)

| Feld | Typ | Bedeutung |
|---|---|---|
| `schema_version` | int | `2` (aktuell); `1` = Legacy ohne Kurzfassung |
| `id` | string | Ordnername, z. B. `"2026-07"` |
| `number` | int | laufende Sitzungsnummer (1, 2, …) |
| `date` | string | Datum des Laufs, ISO `YYYY-MM-DD` |
| `title` | string | Kurztitel der Sitzung |
| `question` | string | die vollständige Fragestellung |
| `summary` | string | Kurzfassung (5–8 Sätze), ab v2 |
| `dissent_highlights` | array | 3–5 Kernpunkte des Dissenses, ab v2 |
| `participants` | array | je Modell: `family`, `model`, `label` |
| `prompts` | object | `system`, `round1`, `round2` |
| `rounds` | array | Laufphasen (`initial_vote`, `final_vote`, optional Wart-Phasen), siehe unten |
| `dissent_md` | string | Dissens-Rohfassung (Markdown) |
| `recommendations` | array | siehe unten |
| `costs` | object | `currency`, `total`, `fx_rate_usd_eur`, `by_model[]` |
| `designation` | string \| null | optional, z. B. `"Gründungssitzung"` |
| `led_by` | object \| null | optional, z. B. `{ model, label }` |
| `wart_opening_md` | string \| null | optionaler Eröffnungstext (Wart-Leitung) |
| `wart_moderation_md` | string \| null | optionale Moderationsnotiz (Wart-Leitung) |
| `wart_dossier` | object \| null | optionales Dossierobjekt inkl. Suchanfragen/Kosten |

### `recommendations[]` (ab v2)

Bei Konsens (`has_consensus: true`):
- `pillar`, `title`, `organization`, `donation_url`, `confidence`, `rationale_md`
- `convergence`: `{ count, total, models[] }` — für Konvergenz-Punkte im Template

Ohne Konsens (`has_consensus: false`):
- `individual_votes[]`: je `{ title, organization, donation_url, confidence, model }`

### `rounds[]`

Standardmodus:

```json
{
  "round": 1,
  "kind": "initial_vote",
  "votes": [
    {
      "model": "exakter-api-string",
      "content_md": "das Votum als Markdown",
      "confidence": 0.7
    }
  ]
}
```

Wart-geleitete Sitzung (Beispiel `2026-07c`):
- `{"round": -1, "kind": "wart_opening", ...}`
- `{"round": 0, "kind": "wart_dossier", ...}`
- `{"round": 1, "kind": "initial_vote", ...}`
- `{"round": 1.5, "kind": "wart_moderation", ...}`
- `{"round": 2, "kind": "final_vote", ...}`

Hinweis zu Kosten:
- `costs.by_model[]` kann neben Council/Summarizer auch eine Wart-Zeile
  enthalten (inklusive Web-Suchkosten).

## Regeln

- **Nichts kürzen:** `raw/` enthält die unveränderten API-Antworten. Transparenz schlägt Ordnerschönheit.
- **Kosten sind Pflicht:** keine Sitzung ohne `costs`-Block.
- **Dissens ist Pflicht:** wenn es keinen gibt, steht das explizit da.
- Empfehlungen verlinken ausschließlich auf offizielle Spendenwege der Organisationen.
- Schema-Änderungen erhöhen `schema_version` und werden hier dokumentiert.

## Version 1 (Legacy)

Sitzungen mit `schema_version: 1` haben kein `summary`, `dissent_highlights` oder `convergence`.
Die Site rendert sie mit Fallbacks; neue Sitzungen nutzen Schema 2.
