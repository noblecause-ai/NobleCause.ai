# audit/data-contract.md — Datenvertrag (Naht zum Frontend)

Formale Spezifikation der publizierten Dateien, **aus den echten Dateien
abgeleitet** (nicht gewünscht). Formale Schemas: `schema/*.json` (draft 2020-12).
In diesem Lauf **nur spezifiziert, nicht im Code erzwungen.**

## Die vier Dateien
| Datei | Schema | Erzeuger | Frontend nutzt |
|---|---|---|---|
| `sessions/<id>/session.json` | `schema/session.schema.json` | `run_session.py` (+ `reaggregate.py`) | Empfehlungen, Konsens, Konvergenz, Dissens, Kosten |
| `schedule.json` | `schema/schedule.schema.json` | `run_wart.write_schedule` / `run_session.advance_schedule` | Countdown |
| `organizations.json` | `schema/organizations.schema.json` | manuell kuratiert (+ Canary-`verified_at`) | Spendenlink-Quelle |
| `kosten.json` | `schema/kosten.schema.json` **(VORSCHLAG)** | **existiert nicht (P0.4)** | Kosten-Übersicht |

---

## Inkonsistenzen HEUTE (markiert für die Naht)

1. **`schema_version` unterscheidet Formänderungen NICHT.** Alle drei Sitzungen
   tragen `schema_version: 2`, obwohl sich Felder änderten (P0.0 fügte
   `organization_id`, `convergence.conditional_count`, `convergence.votes[]`,
   `conditional`/`reservation`, `correction_notice`, `unresolved_votes` hinzu). Ein
   Frontend kann nicht per Version fallunterscheiden. → **Empfehlung: Version bumpen,
   sobald Validierung eingebaut wird.**

2. **`recommendations[]` ist eine diskriminierte Union über `has_consensus`:**
   - `true`: `convergence{count,total,conditional_count,models[],votes[]}`, `organization_id`, `donation_url` gesetzt.
   - `false`: `individual_votes[]` (je Votum org/id/url/model/conditional/reservation), Top-`organization`/`donation_url`/`confidence` **null**.
   Kein Fehler — aber das Frontend MUSS beide Formen behandeln (Dissens gleichwertig).

3. **`rounds[]` ist eine diskriminierte Union über `kind`** (`wart_opening`/`wart_dossier`/
   `wart_moderation` → `content_md`/`wart{}`; `initial_vote`/`final_vote` → `votes[]`).
   Round-Nummern gemischt int/float (`1.5` für Moderation).

4. **`dissent_highlights` mal Liste, mal String** (Typ inkonsistent über Sitzungen).

5. **Kosten: zwei unvereinbare Formen.** `session.costs = {currency,total,fx_rate_usd_eur,
   by_model[{model,label,input_tokens,output_tokens,usd,eur}]}` vs. `journal.entry.costs =
   {currency,total,fx_rate_usd_eur,model,input_tokens,output_tokens,usd_tokens,
   usd_web_search,usd_total,web_search_requests}` (flach, ein Modell, Web-Suche-Felder).
   Ein zukünftiges `kosten.json` muss beide Quellen normalisieren.

6. **`model` vs `label`:** `participants[]`, `costs.by_model[]`, `convergence.votes[]`
   nutzen teils den API-`model`-String, teils das Anzeige-`label` („Claude Opus"). In
   `convergence.models[]`/`votes[].model` steht das **label**, in `costs.by_model[].model`
   der **API-String**. Uneinheitliche Modell-Identität. → Frontend braucht eine
   eindeutige Attribution; heute muss es beide kennen.

7. **Optionale Top-Level-Felder** (nur bei Wart-Leitung/Re-Aggregation):
   `wart_dossier`, `correction_notice`, `designation`, `led_by`, `wart_opening_md`,
   `wart_moderation_md`. Frontend muss deren Abwesenheit tolerieren.

8. **`donation_url` nullable** (Registry + individual_votes): `null` = „Kein offizieller
   Spendenweg auffindbar" (ehrlich rendern, kein toter Link).

---

## Vom neuen Frontend benötigte Felder (verlässliche Naht)
| Bedarf | Feld(er) |
|---|---|
| Empfehlung je Säule | `recommendations[].pillar`, `.title`, `.organization` |
| Konsens-Zustand | `recommendations[].has_consensus` |
| Konvergenz | `recommendations[].convergence.count` / `.total` |
| Konditional + Vorbehalt | `convergence.conditional_count`, `convergence.votes[].conditional/.reservation` |
| Spendenweg | `recommendations[].donation_url` (nullable → ehrlicher Vermerk) |
| Modell-Attribution bei Dissens | `individual_votes[].model` / `.organization` / `.donation_url` |
| Kosten | `session.costs.total` (Detail: `by_model[]`); künftig `kosten.json` |
| Countdown | `schedule.json.next_research` / `.next_session` |
| Korrektur-Transparenz | `session.correction_notice.text` |

**Empfehlung für die Naht:** Diese Schemas später (a) im Backend beim Schreiben
validieren (`jsonschema` gegen `schema/*.json`, bricht laut statt still), (b) im
Frontend als Vertrag verwenden. Vor Einbau: Inkonsistenzen 1/5/6 auflösen
(Version-Bump; Kosten vereinheitlichen; eine Modell-Identität). Nicht Teil dieses
Audits.
