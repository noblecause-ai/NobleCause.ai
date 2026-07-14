# audit/inventory.md — Backend-Inventar (gremium/)

Charakterisierung des deterministischen Kerns. Stand: 2026-07-15, Commit-Basis
`master`. Reine Beschreibung — kein Verhalten geändert.

## Überblick

| Datei | Zeilen | Rolle |
|---|---|---|
| `run_session.py` | 928 | Orchestrator einer Gremium-Sitzung (Einstiegspunkt) |
| `run_wart.py` | 346 | Wöchentlicher Wart-Research-Lauf (Einstiegspunkt) |
| `prompts.py` | 305 | Prompt-Vorlagen (redaktionell, **tabu** — nur inventarisiert) |
| `reaggregate.py` | 148 | Re-Aggregations-Werkzeug (P0.0, dry-run/`--write`) |
| `donation_canary.py` | 114 | Wöchentlicher Spendenlink-Wächter (P0.0) |
| `preflight.py` | 97 | Täglicher API-Key-Canary (P0.0) |
| `organizations.py` | 61 | Deterministische Org-Registry-Auflösung (P0.0) |
| `envtools.py` | 68 | `.env`-Laden (CI-sicher) + `require_keys` (P0.0) |
| `config.json` | 45 | Modelle, Preise, Token-Budgets |
| `Makefile`, `requirements.txt`, `sources.md`, `README.md`, `.env.example` | — | Infrastruktur/Doku |

Zwei Einstiegspunkte, gemeinsame Bibliotheken: `organizations.py`, `envtools.py`
werden von beiden genutzt; `reaggregate.py` importiert aus `run_session.py`.

---

## run_session.py — Sitzungs-Orchestrator
Deterministischer Ablauf (kein LLM steuert den Prozess): Modelle liefern Voten,
der Code zählt. Public/Modul-Funktionen (Auswahl mit Wirkung):

- `extract_json_block(text)->dict|None` — letzten ```json-Block per Klammer-Balance
  parsen. Rein. (Balanciert korrekt über verschachtelte `{}` — verifiziert.)
- `strip_json_block(text)->str` / `extract_dissent(text)` / `extract_search_queries(text)`
  — Regex-Extraktoren aus Prosa. Rein.
- `prior_session()->(id,dict)` — liest `sessions/*/session.json`, sortiert nach
  **(number, date) absteigend** → jüngste. **Liest** Platte.
- `resolve_session_id(sessions_dir, base)->str` — erster freier Suffix b/c/… Rein.
- `advance_schedule(session_date)` — **schreibt** `ROOT/schedule.json` (`next_session`
  = +30 Tage), andere Felder erhalten.
- `call_anthropic/openai/google(model,system,user,max_tokens)->(text,usage,raw)` —
  je ein API-Call. `call_wart_dossier(...)` zusätzlich mit `web_search`-Tool.
  `call_model(spec,...,raw_dir,tag)` — Dispatch nach Familie, **2-Versuch-Retry**,
  **schreibt** `raw/{tag}-{family}.json`.
- `_vote_recommendations(parsed)->list` — `recommendations` **oder** `empfehlungen`
  (deutscher Key-Fallback), sonst `[]`.
- `_conditional(rec)->(bool,str|None)` — konditional-Marker-Regex über `title`.
- **`aggregate_recommendations(final_votes,total_models=None)->(recs,unresolved)`** —
  **der Kern**: je Säule Kandidaten via `organizations.resolve()` auf `org_id`, Gruppen
  nach `org_id`, Gewinner = meiste **verschiedene** Modelle; Konsens ≥2 Modelle;
  `donation_url`+`canonical_name` **aus Registry**; nie stilles Droppen (unbekannt →
  `unresolved`). Rein.
- `build_dissent`, `format_aggregation_for_summary`, `pillar_a_context` — Formatierung.
- `generate_summary(...)->(summary,highlights,usage)` — **ein Anthropic-Call**
  (Summarizer), verlangt `summary`-Key. **schreibt** `raw/summary-*.json`.
- `compute_wart_cost/compute_costs/check_budget` — Kostenrechnung (rein);
  `check_budget` **warnt** nur (kein Abbruch).

**Abhängigkeiten:** SDKs `anthropic`/`openai`/`google-genai` + `web_search`-Tool;
Env `ANTHROPIC_API_KEY`/`OPENAI_API_KEY`/`GEMINI_API_KEY`; liest `config.json`,
`manifest.md`, `sources.md`, `sessions/*/session.json`.
**Seiteneffekte (Reihenfolge):** `sessions/<id>/raw/` (mkdir zuerst) → viele
`raw/*.json` inkrementell → `organizations_unresolved.md` (append, falls unresolved)
→ **`sessions/<id>/session.json`** (finales Protokoll, zuletzt) → `schedule.json`.
**Abbruch-Rest:** bricht der Lauf nach `raw/`-mkdir aber vor `session.json` ab,
bleibt `sessions/<id>/` mit Teil-`raw/`, **ohne** `session.json`; `schedule.json`
unverändert; Re-Lauf mit gleicher id bricht ab („existiert bereits").

## run_wart.py — Wart-Research
- `extract_json_block`/`strip_json_block` — wie oben (eigene Kopien).
- **`fallback_from_markdown(text)->dict`** — rekonstruiert `search_queries`,
  `delta_assessment`, `convene`, `convene_rationale` **per Regex aus Prosa**;
  `findings`/`rejected_findings` **hart `[]`**. Ergebnis wird **publiziert**.
- `latest_session()->(id,dict)` — liest `sessions/*/session.json`, sortiert **nur
  nach Datum** (`x[0]`), kein Tiebreak.
- `call_wart(...)` — gestreamter Anthropic-Call mit `web_search`; **schreibt**
  `raw/wart-response.json`. `stop_reason≠end_turn` → Abbruch (P0.0-Guard).
- `next_monday_0600_utc`, `next_regular_session(session_date,convene)` — Terminlogik
  (`convene`→ +7 Tage statt +30). Nutzt `date.today()` (naiv).
- `compute_wart_costs`, `write_schedule(...)` — **schreibt** `schedule.json`.
**Seiteneffekte:** `journal/<date>/raw/` (mkdir zuerst, **vor** dem Call) →
`raw/wart-response.json`+`wart-content.md` → **`journal/<date>/entry.json`** →
`schedule.json`. **Abbruch-Rest:** `journal/<date>/raw/` bleibt (Rohantwort da,
`entry.json` nicht); Commit erfolgt nur im CI-Workflow.

## prompts.py — (nur Inventar, tabu)
Vorlagen: `SYSTEM`, `CONFLICT_OF_INTEREST`, `SYSTEM_WITH_CONFLICT`, `ROUND1`,
`ROUND2`, `SUMMARY`, `WART_SYSTEM`, `WART_USER`, `WART_DOSSIER_SYSTEM/USER`,
`WART_LEAD_SYSTEM`, `WART_OPENING_USER`, `WART_FOUNDING_DOSSIER_USER`,
`WART_MODERATION_USER`, `WART_SUMMARY(=SUMMARY)`. `ROUND1/ROUND2/WART_USER` geben das
JSON-Schema vor, das die Modelle liefern sollen (u. a. `donation_url` im Votum —
wird aber vom Aggregator verworfen und durch die Registry ersetzt).

## Support-Bibliotheken (P0.0, überwiegend geprüft)
- `organizations.py` — `load_registry(path)` (Alias→id-Map, Kollisions-Check bei
  Load), `resolve(str)->id|None`, `get(id)->dict|None`. Liest `organizations.json`.
- `envtools.py` — `load_env(here,root)` (No-op bei `CI=true`), `require_keys(*names)`
  (Fail-fast; loggt nur Länge).
- `preflight.py` — `ping_anthropic/openai/google`, `main()`; drei Minimal-Live-Calls,
  Exit 1 bei Ausfall. Kein Datenschreiben.
- `donation_canary.py` — `check(url)->(status,code,detail)` (folgt Redirects manuell,
  erkennt Startseiten-Landung), `published_org_ids()`, `main()` (Fail nur bei defektem
  **publiziertem** Weg). Liest `organizations.json`+`sessions/*`.
- `reaggregate.py` — `text_of(raw,family)`, `final_votes_from_raw`, `diff_session`,
  `main()` (`--write`). Rechnet `recommendations` neu; injiziert `correction_notice`.
- `config.json` — `fx_rate_usd_eur`, `max_output_tokens`, `summarizer{}`, `wart{}`,
  `models[]` (Familie/Modell/Label/Preise). Kein `schema_version`.

---

## Datenfluss (ASCII)

```
             KEYS (env)          config.json   manifest.md/sources.md
                │                     │              │
                ▼                     ▼              ▼
  ┌──────────────────────── run_session.main() ───────────────────────────┐
  │ prior_session() ←── sessions/*/session.json  (Kontext)                 │
  │      │                                                                 │
  │ [Wart-Leitung? Eröffnung/Dossier via Fable+web_search] ─┐             │
  │ Runde 1 (Opus/GPT/Gemini) → call_model → raw/r1-*.json  │  LLM-Voten  │
  │ [Moderation via Fable]                                   │             │
  │ Runde 2                    → call_model → raw/r2-*.json  ┘             │
  │      │                                                                 │
  │ aggregate_recommendations(r2)  ── organizations.resolve() ──▶ registry │
  │      │  (ZÄHLT, urteilt nicht: ≥2 Modelle=Konsens, URL aus Registry)   │
  │      ├─ unresolved → organizations_unresolved.md (append)              │
  │ generate_summary()  (1 Anthropic-Call → summary-Text)                  │
  │      ▼                                                                 │
  │ ★ sessions/<id>/session.json  (PUBLIZIERT — Site rendert dies)         │
  │ ★ schedule.json (next_session +30d)                                    │
  └────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────── run_wart.main() ──────────────────────────────┐
  │ latest_session() ←── sessions/*/session.json  (⚠ Datums-Sort, s. Bug)  │
  │ call_wart() Fable+web_search → raw/wart-response.json                  │
  │ extract_json_block()  ── fehlschlägt? ──▶ fallback_from_markdown()     │
  │      │                                    (⚠ RÄT publizierte Inhalte)  │
  │ convene(bool aus Modell) ──▶ next_regular_session (+7d/+30d)           │
  │      ▼                                                                 │
  │ ★ journal/<date>/entry.json (PUBLIZIERT)   ★ schedule.json            │
  └────────────────────────────────────────────────────────────────────────┘

  Wächter (CI, kein Publikationspfad):
    preflight.py → 3 Key-Live-Calls   donation_canary.py → prüft donation_urls
```

**Publizierte Artefakte entstehen** an den mit ★ markierten Stellen (zuletzt im
Lauf). **Halbfertiges bei Abbruch:** `sessions/<id>/raw/` bzw. `journal/<date>/raw/`
(vor dem finalen Write angelegt) — siehe Fehlerpfad-Funde in `findings.md`.
