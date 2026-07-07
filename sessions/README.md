# sessions/ — Deliberations-Protokolle

Jede Gremium-Sitzung ist ein Ordner `YYYY-MM/` (bei mehreren Sitzungen pro Monat: `YYYY-MM-b/` usw.).
Git ist die Datenbank: Ein Protokoll gilt als veröffentlicht, sobald es auf `master` liegt.
Die Site rendert alles unter `sessions/` zur Build-Zeit automatisch.

## Struktur eines Sitzungsordners

```
sessions/2026-07/
├── session.json   # das maschinenlesbare Protokoll (Schema unten)
└── raw/           # Rohantworten der API-Calls, 1 JSON-Datei pro Call
    ├── r1-anthropic.json
    ├── r1-openai.json
    ├── r1-google.json
    ├── r2-anthropic.json
    ├── r2-openai.json
    ├── r2-google.json
    └── summary-anthropic.json   # ab Schema v2
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
| `rounds` | array | 2 Einträge, siehe unten |
| `dissent_md` | string | Dissens-Rohfassung (Markdown) |
| `recommendations` | array | siehe unten |
| `costs` | object | `currency`, `total`, `fx_rate_usd_eur`, `by_model[]` |

### `recommendations[]` (ab v2)

Bei Konsens (`has_consensus: true`):
- `pillar`, `title`, `organization`, `donation_url`, `confidence`, `rationale_md`
- `convergence`: `{ count, total, models[] }` — für Konvergenz-Punkte im Template

Ohne Konsens (`has_consensus: false`):
- `individual_votes[]`: je `{ title, organization, donation_url, confidence, model }`

### `rounds[]`

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

## Regeln

- **Nichts kürzen:** `raw/` enthält die unveränderten API-Antworten. Transparenz schlägt Ordnerschönheit.
- **Kosten sind Pflicht:** keine Sitzung ohne `costs`-Block.
- **Dissens ist Pflicht:** wenn es keinen gibt, steht das explizit da.
- Empfehlungen verlinken ausschließlich auf offizielle Spendenwege der Organisationen.
- Schema-Änderungen erhöhen `schema_version` und werden hier dokumentiert.

## Version 1 (Legacy)

Sitzungen mit `schema_version: 1` haben kein `summary`, `dissent_highlights` oder `convergence`.
Die Site rendert sie mit Fallbacks; neue Sitzungen nutzen Schema 2.
