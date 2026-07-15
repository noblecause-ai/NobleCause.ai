# Datenvertrag — Startseite (sol-build) ↔ Backend

Ziel: **reiner Swap.** Der echte Generator (`gremium/run_session.py`) erzeugt genau
das, was `sol-build/build.py` konsumiert. **Das Frontend parst nie Prosa.** Kanonisches
Schema: `schema/session.schema.json` (Repo-Root; die frühere Dublette
`sitzung.schema.json` ist ersatzlos entfallen).

## Quellen, die das Frontend liest
| Quelle | Rolle |
|---|---|
| `sessions/<id>/session.json` | Die Sitzung (Empfehlungen, Runden **mit strukturierten Voten**, Kosten, Korrektur-Vermerk). |
| `organizations.json` | Kanonischer Name, **`beschreibung`** (faktisch), `donation_url`. Einzige Quelle für Spendenlink + Org-Beschreibung. |
| `sol-build/frontend-config.json` | Präsentations-Konstanten (Säulen-Labels/Symbole, Text der Führungsregel, institutionelle Vorraum-Copy). Keine Beratungsdaten. |
| `sessions/`-Verzeichnis | Archiv „Frühere Sitzungen" wird build-seitig daraus abgeleitet (Nummer/Titel/Datum/Kurzergebnis). |

## Schritt-1-Fund (behoben)
`session.json` trug bisher je Votum nur `{model, content_md (Prosa), confidence}`. Die
strukturierten Empfehlungen lebten nur in `raw/`; der Aggregator parste sie zur
Laufzeit und verwarf sie danach (`votes_of()` behielt nur `confidence`). Ein Frontend
hätte die Protokollspalten und die Revision nur durch **Prosa-Parsing** gewinnen können.
**Behoben:** `rounds[].votes[].recommendations[]` (registry-aufgelöst) ist jetzt Teil
des Schemas und des Generators; die drei Bestandssitzungen wurden deterministisch aus
`raw/` nachgezogen (`reaggregate.py --backfill-votes`, kein Text geändert).

## Disposition je Abweichung (Sols frühere `sitzung.json` ↔ echter Output)
| Feld (Sols Prototyp) | Disposition | Umsetzung |
|---|---|---|
| `rounds[].votes[].recommendations[]` | **→ Backend** | im Schema + `run_session.votes_of()` + Backfill (Schritt 1) |
| `recommendations[].rationale_md` | **entfällt** | von der Karte entfernt; keine erfundene/summarizer-Begründung (Schritt 3) |
| `presentation.pillar_labels` / `pillar_symbols` | **Frontend-Konstante** | `frontend-config.json` (Präsentations-Metadaten, keine Beratungsdaten) |
| `presentation.focus_rule` (Regeltext) | **Frontend-Konstante** | `frontend-config.json` (beschreibt die deterministische Regel, nicht pro Sitzung) |
| `presentation.archive` | **Build-abgeleitet** | `build.py` liest das `sessions/`-Verzeichnis; (Empfehlung, nicht gebaut: Backend-`sessions/index.json`) |
| Dateiname `sitzung.json` | **kanonisch `session.json`** | Frontend liest `sessions/<id>/session.json` |
| ausgelassene Wart-Felder (`wart_dossier`, `designation`, `led_by`, `wart_opening_md`, `wart_moderation_md`) | **bleiben Backend** | Startseite ignoriert sie tolerant; die Vorraum-Copy (Späher/Wart) ist institutionelle `frontend-config`-Konstante, macht keine Sitzungs-Aussage |

## Neues Backend-Feld: `rounds[].votes[].recommendations[]`
```json
{ "pillar": "A", "organization_id": "helen-keller-international",
  "organization": "Helen Keller International", "title": "…", "confidence": 0.55 }
```
- Registry-aufgelöst (`organizations.resolve`); unbekannte Org → weggelassen + Warnung
  (nie stiller Textfall).
- **Revision** = pro Modell/Säule `initial_vote.organization_id` ≠ `final_vote.organization_id`.
  Belegt: Sitzung 3, Säule A: GPT & Gemini `TaRL Africa → Helen Keller International`.
- Registry deckt jetzt **alle** r1+r2-Votenstrings (0 unresolved); dafür neu:
  `tarl-africa`, `global-road-safety-partnership` (Runde-1-Voten, kein Konsens) +
  NTI-/GovAI-Alias-Varianten.

## Neues Registry-Feld: `beschreibung` (Schritt 3)
Faktische, neutrale Kurzbeschreibung „was die Org tut" — **ohne vergleichende Wertung,
kein persuasiver Text**. Einzige Begründung auf der Karte = Konvergenz (Stimmenzahl) +
diese faktische Beschreibung.

## Notiz für die Content-Kaskade (F4)
Publizierte **Sitzungstitel nicht** vom Frontend ändern. Der aktuelle Titel „Auflösung
des Säule-A-Dissens" enthält Fachsprache; er erscheint bewusst NICHT auf der
Antwortebene (dort Klartext). **Empfehlung an die Redaktion:** künftige Sitzungstitel
jargonfrei formulieren (Backend/Content-Kaskade, nicht Frontend).
