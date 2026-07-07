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
    └── ...
```

## Schema `session.json` (Version 1)

| Feld | Typ | Bedeutung |
|---|---|---|
| `schema_version` | int | immer `1` |
| `id` | string | Ordnername, z. B. `"2026-07"` |
| `number` | int | laufende Sitzungsnummer (1, 2, …) |
| `date` | string | Datum des Laufs, ISO `YYYY-MM-DD` |
| `title` | string | Kurztitel der Sitzung |
| `question` | string | die vollständige Fragestellung |
| `participants` | array | je Modell: `family`, `model` (exakter API-String), `label` (Anzeigename) |
| `prompts` | object | `system`, `round1`, `round2` — wörtlich, wie an die APIs gesendet |
| `rounds` | array | 2 Einträge, siehe unten |
| `dissent_md` | string | Dissens-Abschnitt (Markdown); wo die Schlussvoten auseinanderliegen und warum |
| `recommendations` | array | je Empfehlung: `pillar` (A–D), `title`, `organization`, `donation_url` (offizieller Spendenweg der Organisation), `rationale_md`, `confidence` (0–1) |
| `costs` | object | `currency`, `total`, `fx_rate_usd_eur`, `by_model[]` mit `model`, `input_tokens`, `output_tokens`, `usd`, `eur` |

### `rounds[]`

```json
{
  "round": 1,
  "kind": "initial_vote",        // Runde 2: "final_vote"
  "votes": [
    {
      "model": "exakter-api-string",
      "content_md": "das Votum als Markdown",
      "confidence": 0.7           // Selbsteinschätzung des Modells, 0–1
    }
  ]
}
```

## Regeln

- **Nichts kürzen:** `raw/` enthält die unveränderten API-Antworten (inkl. Usage-Metadaten). Transparenz schlägt Ordnerschönheit.
- **Kosten sind Pflicht:** keine Sitzung ohne `costs`-Block.
- **Dissens ist Pflicht:** wenn es keinen gibt, steht das explizit da („Die Schlussvoten konvergieren in …").
- Empfehlungen verlinken ausschließlich auf offizielle Spendenwege der Organisationen — durch dieses System fließt kein Geld.
- Schema-Änderungen erhöhen `schema_version` und werden hier dokumentiert.
