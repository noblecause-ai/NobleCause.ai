# Rekord-Inventar vor dem Merge — 2026-07-29

**Von:** CC (Diagnose) · **Auftrag:** Opus 5 — „Rekord-Inventar vor dem Merge" · **Stand:** 2026-07-29
**Regel eingehalten:** Diagnose only. Nichts gemergt, nichts gepusht, **keine Rekord-Datei angefasst**.
Erzeugt wurde allein dieser Bericht. Vor dem Vergleich `git fetch origin` (nur Refs aktualisiert).

## Referenzen

| Kürzel | Ref | HEAD |
|---|---|---|
| **O** | `origin/master` | `972a9ba` — „journal: Wart-Eintrag 2026-07-27" (vom Cron committet) |
| **M** | `master` (lokal) | `5071194` — „data: Rekord-Stamm + Bestell-Sondersitzung (commission-1)" |
| **F** | `feat/council-rooms` | `9db3738` — „feat(archive): Protokoll-Eingang am Pult" |

**Scope (Guard-Tabupfade):** `journal/**`, `sessions/**`, `schedule.json`, `schema/**`, `gremium/**`.
Dateizahl im Scope: O = 69, M = 72, F = 70.

---

## Kernbefund: zwei auseinandergelaufene Rekord-Linien

Es gibt **nicht** eine Wahrheit mit lokalem Vorlauf, sondern **zwei divergente Linien**, die je etwas
tragen, das die andere nicht hat:

- **O (origin/master)** = die **organische Cron-Historie.** Enthält als einzige den **Wart-Research
  vom 27.07.** (`journal/2026-07-27/` inkl. drei `raw/`-Dateien) und die **fortgeschriebene
  `schedule.json`** (`next_research 2026-08-03`, `last_journal /journal/2026-07-27/`). Es fehlen ihr:
  `schema/**`, die „Rekord-Stamm"-Anreicherung der Sessions, `gremium/run_commission.py`,
  `journal/2026-07-24` und die Kommission `journal/2026-07-27`.
- **M/F (lokal)** = der neu aufgebaute **„Rekord-Stamm".** Enthalten die **angereicherten Sessions**
  (+254–264 Zeilen je `session.json`), `schema/**`, `gremium/run_commission.py`, `journal/2026-07-24`
  und die **Kommission** unter `journal/2026-07-27`. Es fehlen ihnen: der **Wart-Research 27.07.** samt
  `raw/` und die **aktuelle `schedule.json`**.

**Die scharfe Kollision:** `journal/2026-07-27/` existiert auf **O als Wart-Research** und auf **M als
Kommission** — **dieselbe ID, völlig verschiedener Rekord** (Wortlaut unten). F hat den Eintrag gar
nicht. Diese ID muss der Wart auflösen (eine der beiden umnummerieren oder beide getrennt halten),
bevor gemergt wird.

**Merge-Gefahr im Tabupfad:** Auch `gremium/**` ist dreifach uneinig — ein blinder Merge feat→master
oder →origin kann sowohl den Cron-Rekord (O) als auch Code (`prompts.py`, `run_session.py`,
`reaggregate.py`, `run_commission.py`) rückwärts überschreiben.

---

## Tabelle: Bestand + Inhalts-Identität

Legende: **Y** = vorhanden, **–** = fehlt · **gleich** = inhaltsgleich, **DIFF** = Inhalt weicht ab,
**n/a** = auf einem der beiden Refs nicht vorhanden. Diff-Umfang in Klammern (Zeilen, `git diff --stat`).

### `journal/**`

| Eintrag | O | M | F | O↔M | O↔F | M↔F |
|---|:-:|:-:|:-:|---|---|---|
| `2026-07-07/` | Y | Y | Y | **DIFF** (+1) | **DIFF** (+1) | gleich |
| `2026-07-08/` | Y | Y | Y | gleich | gleich | gleich |
| `2026-07-08b/` | Y | Y | Y | gleich | gleich | gleich |
| `2026-07-08c/` | Y | Y | Y | **DIFF** (+1) | **DIFF** (+1) | gleich |
| `2026-07-20/` | Y | Y | Y | **DIFF** (+1) | **DIFF** (+1) | gleich |
| `2026-07-24/` | **–** | Y | Y | n/a | n/a | gleich |
| `2026-07-27/` | Y *(Wart)* | Y *(Kommission)* | **–** | **DIFF — Kollision** | n/a | n/a |
| `2026-07-27/raw/*` (3 Dateien) | Y | **–** | **–** | nur O | nur O | — |
| `README.md` | Y | Y | Y | gleich | gleich | gleich |

### `sessions/**`

| Eintrag | O | M | F | O↔M | O↔F | M↔F |
|---|:-:|:-:|:-:|---|---|---|
| `2026-07/session.json` | Y | Y | Y | **DIFF** (+258/−6) | **DIFF** | gleich |
| `2026-07b/session.json` | Y | Y | Y | **DIFF** (+254/−6) | **DIFF** | gleich |
| `2026-07c/session.json` | Y | Y | Y | **DIFF** (+254/−6) | **DIFF** | gleich |
| `README.md` | Y | Y | Y | gleich | gleich | gleich |

### `schema/**`

| Eintrag | O | M | F | O↔M | O↔F | M↔F |
|---|:-:|:-:|:-:|---|---|---|
| `kosten.schema.json` | **–** | Y | Y | n/a | n/a | gleich |
| `organizations.schema.json` | **–** | Y | Y | n/a | n/a | gleich |
| `schedule.schema.json` | **–** | Y | Y | n/a | n/a | gleich |
| `session.schema.json` | **–** | Y | Y | n/a | n/a | gleich |

### `schedule.json`

| Eintrag | O | M | F | O↔M | O↔F | M↔F |
|---|:-:|:-:|:-:|---|---|---|
| `schedule.json` | Y | Y | Y | **DIFF** | **DIFF** | **DIFF** (alle drei) |

### `gremium/**` (Code + Tabu-Kern; übrige Dateien inhaltsgleich)

| Eintrag | O | M | F | O↔M | O↔F | M↔F |
|---|:-:|:-:|:-:|---|---|---|
| `envtools.py` | Y | Y | Y | gleich | gleich | gleich |
| `preflight.py` | Y | Y | Y | gleich | gleich | gleich |
| `run_wart.py` | Y | Y | Y | gleich | gleich | gleich |
| `config.json` | Y | Y | Y | gleich | gleich | gleich |
| `organizations.py` | Y | Y | Y | gleich | gleich | gleich |
| `prompts.py` | Y | Y | Y | **DIFF** (M +30) | gleich | **DIFF** |
| `run_session.py` | Y | Y | Y | gleich | **DIFF** (F +27) | **DIFF** |
| `reaggregate.py` | Y | Y | Y | gleich | **DIFF** (F +37/−1) | **DIFF** |
| `run_commission.py` | **–** | Y | **–** | nur M (+265) | — | nur M |

> Die übrigen `gremium/`-Dateien (`.env.example`, `Makefile`, `README.md`, `requirements.txt`,
> `sources.md`, `donation_canary.py`, `tests/`) erscheinen in **keinem** der drei paarweisen
> `git diff --stat` über den Scope — sie sind auf O, M und F inhaltsgleich.

**Vollständige Liste der abweichenden Dateien je Paar** (`git diff --stat`, Tabu-Scope):
- **O↔M:** 18 Dateien (prompts.py, run_commission.py, journal 07-07/08c/20/24/27 + 27/raw, schedule.json, schema ×4, sessions ×3).
- **O↔F:** 18 Dateien (reaggregate.py, run_session.py, journal 07-07/08c/20/24 + 27/entry+raw *entfallen auf F*, schedule.json, schema ×4, sessions ×3).
- **M↔F:** 6 Dateien (prompts.py, reaggregate.py, run_commission.py, run_session.py, journal 27/entry.json, schedule.json).

---

## Die ID-Kollision: `journal/2026-07-27/entry.json` im Wortlaut

**Beide Fassungen tragen dieselbe Adresse `/journal/2026-07-27/`, sind aber verschiedene Rekorde.**
O ist der wöchentliche **Wart-Research** (mit `raw/prompt-user.txt`, `raw/wart-content.md`,
`raw/wart-response.json`); M ist die **Bestell-Kommission** (nur `entry.json`, keine `raw/`). F trägt
den Eintrag nicht.

### O — `origin/master:journal/2026-07-27/entry.json` (Wart-Research, `972a9ba`)

```json
{
  "schema_version": 1,
  "date": "2026-07-27",
  "session_ref": "2026-07",
  "model": "claude-fable-5",
  "search_queries": [
    "Helen Keller International vitamin A supplementation funding gap 2026",
    "Iodine Global Network salt iodization funding 2026",
    "Teaching at the Right Level evidence cost-effectiveness 2026",
    "Malaria Consortium seasonal malaria chemoprevention funding gap 2026",
    "Centre for the Governance of AI GovAI 2026 funding research",
    "Lead Exposure Elimination Project LEEP progress 2026",
    "GiveWell top charities update 2026",
    "malaria vaccine rollout coverage 2026",
    "EU AI Act general-purpose AI code of practice status 2026",
    "global lead poisoning elimination initiative funding 2026",
    "Global Fund replenishment malaria funding cuts 2026"
  ],
  "findings": [
    { "pillar": "A", "topic": "Helen Keller Intl VAS — Funding-Lage", "summary": "GiveWell-Grant von 23,6 Mio. USD (Dez. 2024) finanziert VAS in 7 Ländern bis Juni 2027; geschätzt 25x so kosteneffektiv wie Cash-Transfers; anhaltende Unsicherheit über VAD-Prävalenzdaten. Kurzfristige Lücke für Kleinspender geringer als vom Votum implizit angenommen.", "source": "GiveWell (Grant-Seite Dez. 2024)", "source_date": "2024-12" },
    { "pillar": "A", "topic": "IGN — Funding-Lage unklar", "summary": "Keine aktuelle, belastbare RFMF-Zahl auffindbar; einzige Schätzung (~1 Mio. USD/3 Jahre) stammt von ca. 2020. IGN publizierte Jan. 2026 Strategieplan 2025–2030 und beschreibt ein schwieriges Jahr für die Entwicklungs-Community. Datenlücke schwächt die Belastbarkeit des Votums mit Konfidenz 0.9.", "source": "Founders Pledge; IGN IDD Newsletter", "source_date": "2026-01" },
    { "pillar": "A", "topic": "TaRL — neue Evidenz und Attributionsfehler", "summary": "WWHGE-Synthese (2026) kodifiziert TaRL-Kernkomponenten; RCT in Côte d'Ivoire (2026) prüft Lehrkraft-Implementierung bei Skalierung. Kosten oft <10 USD/Kind/Jahr (J-PAL). Korrektur: TaRL stammt von Pratham (und TaRL Africa), nicht von Evidence Action — Protokoll-Attribution des GPT-Votums mutmaßlich fehlerhaft.", "source": "What Works Hub for Global Education; AERJ/Sage; J-PAL", "source_date": "2026-05" },
    { "pillar": "B", "topic": "SMC / Malaria Consortium — Wirksamkeit und Funding", "summary": "GiveWell-Grant 10,4 Mio. USD (Juni 2025) für Chad-Expansion 2026–27; Abdeckung 87–94 % (2018–2024); 2.000–7.000 USD pro abgewendetem Todesfall (Stand Dez. 2023). Coverage-Report Apr. 2026 dokumentiert Überbrückung einer PMI-Finanzierungslücke mit philanthropischen Mitteln.", "source": "GiveWell; Malaria Consortium SMC Coverage Report 2025", "source_date": "2026-04" },
    { "pillar": "B", "topic": "Neue Entwicklung: Malaria-Finanzierungskrise und Impfstoff-Skalierung", "summary": "Global Fund 8. Replenishment schloss mit 12,64 Mrd. USD (Ziel 18 Mrd.); US-Zusage von 6 auf 4,6 Mrd. USD gekürzt, Frankreich mehr als halbiert; 282 Mio. Malariafälle 2024 (leichter Anstieg). 25 afrikanische Länder impfen (Stand Jan. 2026), aber WHO meldet Finanzierungsengpässe bei Skalierung. Netto: stärkt den Fall für SMC-Spenden.", "source": "Global Fund; HRW; WHO; Gavi; JHU/IVAC", "source_date": "2026-02 bis 2026-05" },
    { "pillar": "C", "topic": "GovAI — Funding und Policy-Traktion", "summary": "Coefficient Giving (vormals Open Philanthropy) vergab 2,5 Mio. USD General Support (Listung 2026); GovAI-Personal war Vice-Chair bei Erstellung des EU-GPAI-Verhaltenskodex und berät JRC/EU AI Office. Keine akute Funding-Lücke belegt; marginaler Nutzen von Kleinspenden weiterhin schwer bezifferbar.", "source": "Granted-AI-Grant-Listungen; EU-Lobbyregister (LobbyFacts)", "source_date": "2026" },
    { "pillar": "C", "topic": "Neue Entwicklung: AI-Act-Durchsetzung ab 02.08.2026", "summary": "Ab 2. August 2026 setzt die EU-Kommission die GPAI-Pflichten des AI Act durch und kann Bußgelder verhängen; der GPAI-Verhaltenskodex (Juli 2025) strukturiert die Compliance. Erhöht Relevanz und Zeitkritikalität des AI-Governance-Felds.", "source": "Jones Day / EU-Kommission (digital-strategy.ec.europa.eu)", "source_date": "2025-08 / laufend 2026" },
    { "pillar": "D", "topic": "LEEP — Funding-Lücke 2026 geschlossen, starke Skalierung", "summary": "GWWC: unmittelbare Funding-Lücke für Paint-Programme 2026 gefüllt (Stand Nov. 2025). LEEP in 40 Ländern (76 % der LMIC-Geburten), Expansion auf 50 afrikanische Länder via Bloomberg-Initiative; Malawi-Wiederholungsstudie zeigt >50 % Rückgang des Bleifarben-Marktanteils. Wirksamkeit bestätigt, marginaler Nutzen zusätzlicher Kleinspenden derzeit unklarer.", "source": "Giving What We Can; leadelimination.org (2025 in Review)", "source_date": "2025-11 / 2026-02" },
    { "pillar": "D", "topic": "Neue Entwicklung: WHO Global Action Plan for Lead und Forschungsgelder", "summary": "WHO entwickelt gemäß WHA-Resolution 78.27 (2025) einen Global Action Plan for Lead plus Technical Package (Webinare März/Juni 2026); CGD und Coefficient Giving schreiben bis zu 5 Mio. USD Forschungsmittel aus (EoI bis 02.08.2026). Das Feld ist zunehmend weniger 'übersehen' — Prüfauftrag für Säule-D-Kriterium.", "source": "WHO; CGD-Blog", "source_date": "2026-06" }
  ],
  "rejected_findings": [
    { "query_or_topic": "Founders-Pledge-RFMF-Zahlen zu IGN und HKI", "reason": "geprüft, nicht relevant weil Datenstand 2020/2021 — als aktuelle Funding-Aussage unbrauchbar, nur historischer Kontext." },
    { "query_or_topic": "GiveWell 'Malaria Funding Gaps' (205 Mio. USD SMC-Lücke)", "reason": "geprüft, nicht relevant weil Publikationsstand November 2018 (Zeitraum 2018–2020), durch Replenishment-Daten 2026 überholt." },
    { "query_or_topic": "EA-Forum-Eintrag zu GovAI-Finanzierung", "reason": "geprüft, nicht relevant weil Stand Juli 2022; durch Coefficient-Giving-Grant (2026) ersetzt." },
    { "query_or_topic": "Kenia-Studie RTS,S-Coverage 2019–2022", "reason": "geprüft, nicht relevant weil historische Pilotdaten; durch Gavi-/WHO-Daten Jan.–Mai 2026 überholt." },
    { "query_or_topic": "GiveWell 'Basic Information'-Seite und Selbstbeschreibungen", "reason": "geprüft, nicht relevant weil Stand 2022 bzw. ohne neue Informationen zu Empfehlungen oder Lücken." },
    { "query_or_topic": "UIA-Yearbook-Profil IGN", "reason": "geprüft, nicht relevant weil reine Organisationsbeschreibung hinter Paywall, keine Funding-/Wirksamkeitsdaten." },
    { "query_or_topic": "KFF-Analyse US-FY2026-Budgetantrag", "reason": "geprüft, nur eingeschränkt relevant weil Budgetantrag statt verabschiedeter Haushalt; tatsächliche Effekte über Global-Fund-/PMI-Quellen besser belegt." }
  ],
  "delta_assessment": "Größtes Delta in Säule D: LEEPs unmittelbare 2026-Funding-Lücke ist laut GWWC (Nov. 2025, also vor der Sitzung) geschlossen; das Blei-Feld erhält über Bloomberg, WHO-Aktionsplan und CGD/Coefficient deutlich mehr Mittel — marginale Kosteneffektivität von Kleinspenden und 'übersehen'-Status sind in der Monatssitzung zu überprüfen. Säule B: Global-Fund-Replenishment blieb mit 12,64 Mrd. USD weit unter dem 18-Mrd.-Ziel; Kürzungen der US-, EU- und Frankreich-Beiträge sowie dokumentierte PMI-Einfrierung stärken tendenziell den Fall für SMC. Säule A: HKI bis Juni 2027 durch GiveWell finanziert (kurzfristige Dringlichkeit geringer); IGN-Funding-Lage nicht verifizierbar (Datenlücke); TaRL-Evidenz 2026 gestärkt, aber Trägerzuordnung 'Evidence Action' im Protokoll mutmaßlich fehlerhaft (Pratham/TaRL Africa). Säule C: keine widersprechende Evidenz; GovAI-Kernfinanzierung gesichert, AI-Act-Durchsetzung ab 02.08.2026 erhöht Feldrelevanz.",
  "convene": false,
  "convene_rationale": "Kein Kriterium eindeutig erfüllt: (a) Keine neue Evidenz widerspricht einer Empfehlung substantiell — alle Wirksamkeitsbefunde bestätigen oder stärken die Empfehlungen. (b) Die LEEP-Funding-Lücke wurde zwar geschlossen, aber bereits im November 2025, also vor der Sitzung vom 07.07.; es ist eine Korrektur der Informationsbasis, kein neues Ereignis, und LEEP skaliert weiter mit angekündigten neuen Fundraising-Phasen. (c) Die Global-Fund-Lücke ist gravierend, stärkt aber die bestehende SMC-Konsensempfehlung, statt ihr zu widersprechen. Demut-Kanon: Im Zweifel nicht einberufen — LEEP-Marginalnutzen, TaRL-Attributionskorrektur und IGN-Datenlücke sind in der regulären Monatssitzung prioritär zu behandeln.",
  "content_md": "«… vollständiges Wart-Dossier (Runden 1–6, Suchanfragen, verworfene Funde, Delta-Bewertung, Einberufungs-Entscheid) — im Rekord unter journal/2026-07-27/raw/wart-content.md wörtlich; hier aus Platzgründen gerafft …»",
  "costs": {
    "currency": "EUR",
    "total": 2.214,
    "fx_rate_usd_eur": 0.85,
    "model": "claude-fable-5",
    "input_tokens": 175210,
    "output_tokens": 14851,
    "web_search_requests": 11,
    "usd_tokens": 2.4947,
    "usd_web_search": 0.11,
    "usd_total": 2.6046
  },
  "actions_run_url": "https://github.com/noblecause-ai/NobleCause.ai/actions/runs/30255462425"
}
```

> **Hinweis zum `content_md`:** Im Rekord (O) steht hier der **vollständige** Dossier-Wortlaut (≈ ein
> 6-teiliges Markdown-Dokument in einer JSON-Zeile) plus die drei Dateien unter `raw/`. Für dieses
> Inventar ist er oben gerafft; der Wortlaut liegt unverändert in `origin/master:journal/2026-07-27/`.
> Die Kopf- und Entscheid-Felder (findings, convene, delta_assessment, costs, actions_run_url) sind
> vollständig.

### M — `master:journal/2026-07-27/entry.json` (Kommission, `5071194`)

```json
{
  "schema_version": 1,
  "date": "2026-07-27",
  "type": "commission",
  "commission_ref": "/commissions/2026-07-27/",
  "session_ref": null,
  "convene": true,
  "convene_rationale": "Sondersitzung außer der Reihe: Bestellung der Selbstdarstellungen der drei Sitzinhaber; zugleich Backend-Durchlauf vor Go-Live. Keine Beratungsfrage, keine Empfehlung.",
  "search_queries": [],
  "findings": [],
  "rejected_findings": [],
  "delta_assessment": "Bestell-Sondersitzung (commission-1): Selbstdarstellungs-Bestellung der drei Sitzmodelle über den regulären API-Mechanismus. Keine Beratungsfrage, keine Aggregation, keine Gremium-Empfehlung; zugleich Backend-Durchlauf vor Go-Live.",
  "content_md": "# Bestell-Sondersitzung — commission-1\n\n*Sondersitzung außer der Reihe, kein Beratungslauf. Zählt nicht als Sitzung; die Sitzungsnummerierung bleibt den Beratungen vorbehalten.*\n\n## Gegenstand\nDie drei Sitzmodelle bestellen ihr rundes Messingmedaillon selbst — getrennt befragt, ohne Kenntnis der anderen Bestellungen, mit dem identischen Rahmentext (§2 des Bestellverfahrens). Nachtragsbestellung, weil die Modelle längst einberufen sind (Ersteinberufung 2026-07-07).\n\n## Ablauf\nEin Lauf über den regulären API-Mechanismus (`gremium/run_commission.py`, `call_model`). Keine Aggregationsregel angewandt (keine Säulenfrage), kein Umdenken-Schritt. Rahmentext-Hash, Versuchszahl und Zeitstempel je Modell liegen in `/commissions/2026-07-27/commission.json`.\n\n## Nächster Schritt\nDer Wart prüft die drei Wortlaute gegen den Rahmen, **bevor** generiert wird; Ablehnungen bleiben mit Vermerk im Rekord (`models.json`, `warden_review`).",
  "costs": {
    "currency": "EUR",
    "total": null,
    "input_tokens": 2330,
    "output_tokens": 3084
  },
  "actions_run_url": null
}
```

**Strukturelle Unterschiede der beiden Köpfe:**

| Feld | O (Wart) | M (Kommission) |
|---|---|---|
| `type` | *(fehlt / Research)* | `"commission"` |
| `model` | `claude-fable-5` | `null` |
| `session_ref` | `"2026-07"` | `null` |
| `commission_ref` | *(fehlt)* | `/commissions/2026-07-27/` |
| `convene` | `false` | `true` |
| `search_queries` / `findings` | 11 / 9 | leer / leer |
| `raw/`-Dateien | 3 (prompt, content, response) | keine |
| `actions_run_url` | GitHub-Run 30255462425 | `null` |

---

## `schedule.json` — drei Fassungen (alle DIFF)

| Ref | `next_research` | `next_session` | `last_journal` |
|---|---|---|---|
| **O** (origin, Cron) | `2026-08-03T06:00:00Z` | **`2026-08-06T12:00:00Z`** | `/journal/2026-07-27/` |
| **M** (master lokal) | `2026-07-20T06:00:00Z` *(Vergangenheit)* | **`2026-08-08T12:00:00Z`** *(abweichend!)* | `/journal/2026-07-08c/` |
| **F** (feat) | `2026-07-27T06:00:00Z` *(Vergangenheit)* | **`2026-08-06T12:00:00Z`** | `/journal/2026-07-20/` |

Nur **O** ist aktuell (vom Cron fortgeschrieben). **M** trägt sogar ein **abweichendes `next_session`
(08-08 statt 08-06)** und das älteste `last_journal`. Für die *Anzeige* unschädlich (der Termin wird
aus dem Rhythmus berechnet, nicht gelesen) — aber beim Merge darf O nicht überschrieben werden.

---

## Konsequenzen / offene Entscheidungen (für Wart & Steward)

1. **ID-Kollision `journal/2026-07-27/` auflösen** — Wart-Research (O) *und* Kommission (M) können nicht
   dieselbe Adresse belegen. Kanon-Frage: bekommt die Kommission eine eigene ID (z. B. `2026-07-27b`
   oder ein `commission-…`-Schema), und bleibt der Wart-Research auf `2026-07-27`? Beide Wortläute
   liegen oben nebeneinander.
2. **Cron-Rekord nicht verlieren** — der Wart-Research vom 27.07. (`entry.json` + 3 `raw/`-Dateien) und
   die aktuelle `schedule.json` existieren **nur auf O**. Ein Merge, der lokal→origin schreibt, muss sie
   erhalten (nicht durch die Rekord-Stamm-Fassung zurückschreiben).
3. **Rekord-Stamm nicht verlieren** — die angereicherten Sessions (+254–264 Zeilen), `schema/**`,
   `run_commission.py`, `journal/2026-07-24`, die Kommission und die `+1`-Anreicherung der Journal-Köpfe
   existieren **nur lokal (M/F)**. Sie müssen in den zusammengeführten Stand.
4. **`schedule.json` gezielt setzen** — nicht mergen lassen, sondern die O-Fassung (Cron) als Wahrheit
   übernehmen; M/F-Fassungen sind veraltet (M zudem mit falschem `next_session`).
5. **`gremium/**`-Divergenz im Tabupfad prüfen, bevor gemergt wird:**
   - `prompts.py`: **M hat +30 Zeilen** ggü. O = F. (Lokaler master-Vorlauf; origin und feat gleich.)
   - `run_session.py`: **F hat +27 Zeilen** ggü. O = M. (feat-Vorlauf/-Rücklauf im Tabupfad.)
   - `reaggregate.py`: **F weicht ab** (+37/−1) ggü. O = M.
   - `run_commission.py`: **nur M** (+265). Auf O und F nicht vorhanden.
   Ein Merge feat→master bringt Fs `run_session.py`/`reaggregate.py` auf master; ein späterer
   →origin-Merge entscheidet über `prompts.py` und `run_commission.py`. **Guard beachten:** `gremium/**`
   ist auf `feat/*` Tabupfad — die feat-Divergenz dort ist erklärungsbedürftig und darf den
   Cron-Codestand (O) nicht rückwärts überschreiben.

---

*Methodik: `git ls-tree` (Bestand je Ref), `git diff --quiet`/`--stat` (Identität/Umfang je Paar),
`git show <ref>:<pfad>` (Wortlaut). Keine Arbeitskopie verändert, kein Merge, kein Push.*
