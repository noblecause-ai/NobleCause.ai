# audit/findings.md — Bug- und Risiko-Liste (gremium/)

Systematisch gegen die bekannte Fehlersignatur (Determinismus / Schema /
still-ratende Logik / Fehlerpfade / Geld / Verfassung). **Kalibriert:** jede
Agenten-Behauptung am Code gegengeprüft; überzogene/widerlegte unten unter
„Geprüft & entwarnt". Kein Fund wurde behoben (Auftrag: dokumentieren).

**Zählung (real):** 2 kritisch · 6 hoch · 9 mittel · 5 niedrig = **22 Funde.**
Wichtigster Befund vorab: **der Aggregations-Kern (die Verfassung) urteilt NICHT —
er zählt sauber** (F-K1 verifiziert). Die kritischen/hohen Funde clustern im
**Wart-Pfad** und in generischer Robustheit (fehlende Schema-Validierung, stille
Drops), nicht im Konsens-Zähler.

---

## KRITISCH

### K1 — `fallback_from_markdown` rät publizierte Inhalte zusammen
`run_wart.py:55–74` · Kat. still-ratende Logik / Geld-nah (Journal ist publiziert).
Bei fehlgeschlagenem JSON-Parse (Antwort `end_turn`, aber ```json unvollständig)
rekonstruiert die Funktion `convene`, `delta_assessment`, `convene_rationale`,
`search_queries` **per Regex aus Prosa** und setzt `findings=[]`/`rejected_findings=[]`
hart. Das Ergebnis wird als `journal/<date>/entry.json` **publiziert**. Effekt: ein
Journal-Eintrag kann geratene Prosa + **leere Funde** zeigen, obwohl das Modell Funde
lieferte. Exakt die in P0.0 (Aggregator) entfernte Signatur — hier noch aktiv. Der
`stop_reason≠end_turn`-Guard (`:290`) fängt sie NICHT (er greift nur bei Refusal/
max_tokens, nicht bei vollständigem Turn mit kaputtem JSON).

### K2 — `latest_session()` nicht-deterministisch (Datums-Gleichstand)
`run_wart.py:93` · Kat. Determinismus. `entries.sort(key=lambda x: x[0], reverse=True)`
sortiert **nur nach `date`**, ohne Tiebreak. Alle drei Sitzungen tragen `2026-07-07`
→ die „jüngste Sitzung", auf die der Wart seine Recherche bezieht, hängt von der
`iterdir()`-Reihenfolge ab (Dateisystem). **Derselbe Bug-Typ wie der bereits behobene
Frontend-„jüngste Sitzung"-Bug** — im Backend noch offen. Effekt: der Wart
recherchiert evtl. gegen die falsche Sitzung; `session_ref`/Kontext im publizierten
Journal falsch. (Gegenstück `run_session.prior_session` ist NICHT betroffen — es
sortiert nach eindeutiger `number`, verifiziert.)

## HOCH

### H1 — Keine Schema-Validierung von Modell-Ausgaben; stiller Drop
`run_session.py` (`extract_json_block`-None → Votum verschwindet) · Kat. Schema.
Liefert ein Modell unparsebares JSON, gibt `extract_json_block` `None`; das Votum
trägt dann `0` Empfehlungen zur Aggregation bei — **nur stderr, kein Vermerk in
session.json**. Ein „Zähl"-System, das stillschweigend eine Stimme verliert. (Das
`unresolved`-Netz greift NUR bei unbekannter Org, nicht bei Parse-Fehler.)

### H2 — Key-Toleranz nur auf äußerem Feld; innere deutsche Keys droppen still
`run_session.py:286` + `:323/:325` · Kat. Schema. `_vote_recommendations` toleriert
`recommendations`/`empfehlungen` (äußere Liste), aber die inneren Zugriffe
`r.get("pillar")`/`r.get("organization")` sind **nicht** tolerant. Ein Modell mit
deutschen INNEREN Keys (`säule`/`organisation`) → `.get("pillar")` = None → Votum
still übersprungen (`:324 continue`). Der Opus-2026-07c-Fall hatte englische innere
Keys (deshalb geheilt); die Klasse bleibt offen. Der Code-Kommentar „werden gelesen,
NICHT verschluckt" gilt nur für den äußeren Key.

### H3 — Keine Validierung von `config.json` (KeyError mitten im Lauf)
`run_session.py` (`config["max_output_tokens"]`, `config["models"]`,
`config["fx_rate_usd_eur"]`), `run_wart.py:163` (`wart_cfg['model']`),
`compute_wart_costs` (`usd_per_1m_*`) · Kat. Schema. Direktzugriff ohne `.get`/
Validierung; fehlender/umbenannter Key → KeyError erst NACH bezahlten Calls. Kein
`schema_version` in `config.json`.

### H4 — `call_model`-Abbruch nimmt Kosten & Erkenntnis mit
`run_session.py` `call_model` (2-Versuch-Retry) · Kat. Fehlerpfade. Scheitert ein
Modell 2×, wird `RuntimeError` geworfen → Lauf bricht ab; bereits bezahlte Voten +
Teil-`raw/` liegen da, aber **kein `session.json`** → beim Re-Lauf zählt `number` neu,
Kosten verloren ohne Protokoll-Spur. „Abbruch nimmt Erkenntnis mit"-Signatur.

### H5 — `--budget-cap` wird nie durchgesetzt
`run_session.py` `check_budget` · Kat. Geld. Trotz `--budget-cap`-Flag **warnt** die
Funktion nur auf stderr und schreibt die Sitzung regardless. Eine Sitzung über Budget
wird publiziert; der „Deckel" ist keiner.

### H6 — `convene`-Boolean eines EINZELNEN Modells verstellt den Kalender
`run_wart.py:314,341` · Kat. Verfassung. Das vom Wart (ein Modell) gelieferte
`convene` (True/False) setzt **unmittelbar** `next_session` (+7d statt +30d), ohne
Zählung/Review. Dies ist die einzige Stelle, an der ein einzelner LLM-Output zu einer
**Terminentscheidung** wird (nicht „zählen", sondern „entscheiden"). Ob der Wart das
per Design darf, ist eine Steward-/Verfassungsfrage — als Charakteristik gemeldet,
Schweregrad hoch wegen Kaskadenwirkung auf den nächsten Zyklus.

## MITTEL

- **M1** `run_wart.next_regular_session`/`next_monday_0600_utc` nutzen `date.today()`
  (naiv, lokal) für die +7d-Convene-Schwelle → zeitzonenabhängig. `run_wart.py:142–148`. Kat. Determinismus.
- **M2** `generate_summary` prüft nur `"summary"`-Key; `dissent_highlights` fällt still
  auf `[]` → publizierte Sitzung verliert Highlights ohne lauten Fehler. `run_session.py`. Kat. Schema.
- **M3** Modell-`confidence` wird ungeprüft gemittelt (kein `[0,1]`-Check) → publizierte
  `confidence` kann außerhalb des Bereichs liegen. `aggregate_recommendations`. Kat. Schema.
- **M4** Regex-Extraktoren `strip_json_block`/`extract_dissent`/`extract_search_queries`
  liefern bei Formatabweichung still Default/`None` (publizierte `dissent_md`/
  `search_queries` können unvollständig sein). `run_session.py`. Kat. still-ratend.
  (Funktionieren auf den Ist-Daten — Golden-Tests grün — aber fragil.)
- **M5** Nicht-atomare Mehrdatei-Schreibung: `session.json`/`entry.json` VOR
  `schedule.json`; scheitert Letzteres, ist der Zeitplan stale, das Protokoll aber
  committet. `run_session.py`/`run_wart.py`. Kat. Fehlerpfade.
- **M6** `run_wart`: lokaler Abbruch nach dem bezahlten Call lässt `journal/<date>/raw/`
  uncommittet zurück; Re-Lauf gleiches Datum bricht ab. (CI mildert via
  `upload-artifact`.) Kat. Fehlerpfade.
- **M7** `donation_canary.check` — Startseiten-Redirect-Erkennung greift NUR, wenn die
  konfigurierte URL einen Pfad hat: `if conf_path and not final_path` (`:67-ff`). Eine
  **Bare-Domain**-`donation_url` (kein Pfad), die auf die Startseite fällt, würde als OK
  gewertet. Aktuell haben alle URLs Pfade → latent, aber geld-kritisch. Kat. Geld.
- **M8** `config.json`-Preise statisch/unversioniert → `costs` wird falsch, wenn ein
  Anbieter die Preise ändert; kein Abgleich. Kat. Geld.
- **M9** `organizations.py`/`config.json` werden ohne JSON-Schema geladen (`data["organizations"]`
  vorausgesetzt) → korrupte/umbenannte Struktur crasht statt lauter Validierung. Kat. Schema.

## NIEDRIG

- **N1** `aggregate_recommendations` `max(groups, key=…)` (`:327`) hat keinen
  deterministischen Tiebreak bei gleicher Modellzahl. Mit **3 Modellen nicht
  auslösbar** (ein Gewinner ≥2 ist eindeutig); latent ab ≥4 Modellen. Kat. Determinismus.
- **N2** `_conditional` (Marker-Regex über `title`) kann ein Votum fälschlich als
  konditional markieren, dessen Titel „vertag/bedingt" in anderem Sinn enthält.
  Dokumentierte, transparente Regel; niedriges Risiko. Kat. still-ratend.
- **N3** `check_fable_available` ist toter Code (in `main()` nicht aufgerufen),
  `/tmp`-Fallback. Kat. Fehlerpfade.
- **N4** `envtools.load_env` `.env`-Parser akzeptiert beliebige Key-Namen, strippt nur
  äußere Quotes. Für den Zweck ok; nicht defensiv. Kat. Schema.
- **N5** `donation_url` fehlt ein Null-Check nach `organizations.get(id)`
  (Consensus-/individual_votes-Pfad). Durch `resolve()` **nicht erreichbar** (id stets
  in Registry) → rein defensiv. Kat. Geld.

---

## Geld-Pfad-Gesamtbild (Kat. e)
Nach P0.0 kommt `donation_url` **ausschließlich aus der Registry** (nicht aus dem
Modell-Votum) — der teuerste Fehlertyp ist strukturell entschärft. Restrisiken:
**M7** (Canary-Lücke bei Bare-Domain), **M8** (Preis-Drift), **N5** (defensiver
Null-Check). Kein aktiver kritischer Geld-Bug gefunden.

## Verfassungs-Gesamtbild (Kat. f) — „urteilt der Code, wo er zählen dürfte?"
- **Aggregator (`aggregate_recommendations`): ZÄHLT, urteilt nicht** — Auflösung
  deterministisch über die Registry, Konsens = ≥2 verschiedene Modelle, kein LLM im
  Zählweg. **Verifiziert sauber (F-K1 unten).** Das ist der constitutionelle Kern.
- **Einzige echte „Urteils"-Stelle: H6** (Wart-`convene` → Terminentscheidung).
- Wart-Eröffnung/Moderation/Dossier und `generate_summary` sind LLM-Texte, die
  publiziert bzw. in Prompts injiziert werden — **das ist Design** (Wart-geleiteter
  Modus; Summary ist die deklarierte „Leserfassung"; Dossier ist als „keine Empfehlung"
  gekennzeichnet), kein Bug. Sie beeinflussen Voten (dokumentiert) → als Charakteristik
  vermerkt, nicht als Verstoß.

## Geprüft & entwarnt (Agenten-Behauptungen, am Code widerlegt)
- **`extract_json_block` „bricht beim ersten `}` ab"** — FALSCH. Depth-Balancer über
  verschachtelte `{}` verifiziert (`{"findings":[{...},{...}]}` korrekt geparst).
- **`prior_session` nicht-deterministisch (kritisch)** — nach `number` (eindeutig 1/2/3)
  sortiert → deterministisch. Kein Fund.
- **`donation_url` → `None.get()` AttributeError (kritisch)** — durch `resolve()`
  unerreichbar (aufgelöste id stets in Registry). Nur defensiver Null-Check offen (N5).
- **Aggregator „LLM-Output formt Aggregation" (kritisch)** — der Aggregator nutzt nur
  `pillar`/`organization`/`confidence` als DATEN und zählt; kein LLM entscheidet. Kein
  Verfassungsbruch. (Range-Check-Lücke separat als M3.)

## Golden-Test-Blocker
**Keiner behebt-pflichtig.** F-K2 (`latest_session`-Determinismus) verhindert einen
*deterministischen* Golden Test dieser Funktion — dokumentiert in
`tests/golden/test_golden_determinism.py` (nicht umgangen), gemeldet als K2. Alle
anderen Golden Tests konnten geschrieben werden (10 grün).
