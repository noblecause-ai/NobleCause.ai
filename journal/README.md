# Wart-Journal

Wöchentliche Research-Einträge des Warts (Fable, `claude-fable-5`) mit Web-Suche.
Jeder Eintrag ist unveränderlich, sobald veröffentlicht.

## Verzeichnisstruktur

```
journal/
  YYYY-MM-DD/
    entry.json      # strukturierter Eintrag (siehe Schema)
    raw/
      prompt-user.txt
      wart-content.md
      wart-response.json   # vollständige API-Antwort
```

## Schema `entry.json` (v1)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `schema_version` | `1` | Schema-Version |
| `date` | ISO-Datum | Tag des Laufs |
| `session_ref` | string | ID der referenzierten Sitzung (z. B. `2026-07`) |
| `model` | string | API-Modell (z. B. `claude-fable-5`) |
| `search_queries` | string[] | Wörtliche Suchanfragen |
| `findings` | object[] | Kernfunde mit `pillar`, `topic`, `summary`, `source`, `source_date` |
| `rejected_findings` | object[] | Verworfene Funde: `query_or_topic`, `reason` |
| `delta_assessment` | string | Delta-Bewertung seit der referenzierten Sitzung |
| `convene` | boolean | Einberufung vor der regulären Monatssitzung? |
| `convene_rationale` | string | Begründung der Einberufungs-Entscheid |
| `content_md` | string | Lesbare Dossier-Fassung (ohne JSON-Zaun) |
| `costs` | object | Token- und Suchkosten in EUR |
| `actions_run_url` | string \| null | Link zum GitHub-Actions-Lauf |

## Einberufungskriterien

Der Wart beruft das Gremium nur ein, wenn mindestens eines zutrifft:

1. Neue Evidenz widerspricht einer bestehenden Empfehlung substantiell.
2. Eine wesentliche Funding-Lücke wurde geschlossen oder neu geöffnet.
3. Ein neues, von den Säulen erfasstes Risiko oder eine Chance von Rang.

Im Zweifel **nicht** einberufen (Demut-Kanon).
