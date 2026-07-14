# audit/recommendation.md — Behalten / Härten / Ersetzen

Zahlen statt Meinung. Basis: `findings.md` (22 kalibrierte Funde), `tests/golden/`
(10 grün), Schema-Validierung (alle realen Dateien valide).

## Funde je Schweregrad
| kritisch | hoch | mittel | niedrig | Summe |
|---|---|---|---|---|
| 2 | 6 | 9 | 5 | 22 |

**Verteilung der schweren Funde (kritisch+hoch = 8):**
- `run_wart.py`: **2 kritisch** (K1 fallback_from_markdown, K2 latest_session) + **1 hoch** (H6 convene→Termin) = 3
- `run_session.py`: **5 hoch** (H1 stiller Parse-Drop, H2 innere Keys, H3 config, H4 call_model-Abbruch, H5 Budget) = 5
- **Aggregator-Kern (`aggregate_recommendations`): 0 kritisch, 0 hoch.** Verifiziert:
  zählt, urteilt nicht. Nur N1 (latent, ≥4 Modelle) + M3 (confidence-Range).

## Modul-Einordnung
| Modul | Verdikt | Begründung | Aufwand | Risiko |
|---|---|---|---|---|
| `aggregate_recommendations` (Kern) | **BEHALTEN** | Constitution sauber (zählt, kein LLM im Zählweg); jetzt golden gegen alle 3 realen Sitzungen | — | niedrig |
| `organizations.py` | **BEHALTEN** | deterministische Auflösung, Kollisions-Check; nur M9 (Load-Schema) | S | niedrig |
| `reaggregate.py`, `preflight.py`, `envtools.py` | **BEHALTEN** | P0.0-Code, keine schweren Funde | — | niedrig |
| `donation_canary.py` | **HÄRTEN (leicht)** | M7 Bare-Domain-Lücke (latent, geld-nah) | S | niedrig |
| `config.json` + Config-Zugriff | **HÄRTEN** | H3/M8/M9: Schema + Validierung beim Laden (lauter Fehler statt KeyError/Preis-Drift) | S–M | niedrig |
| `run_session.py` (ohne Kern) | **HÄRTEN** | H1/H2/H4/H5 + M2–M5: Validierungs-/Fehlerpfad-Schicht; Struktur (deterministischer Ablauf) trägt | M | mittel |
| `run_wart.py` | **HÄRTEN (vorrangig)** | Cluster der kritischen Funde: K1 `fallback_from_markdown` streichen (statt raten laut abbrechen), K2 latest_session nach `number` sortieren, H6 convene-Governance entscheiden, M1 UTC | M | mittel |
| `prompts.py` | **n/a** | redaktionell, tabu (Content-Kaskade) | — | — |

Kein Modul erhält **ERSETZEN**: die schweren Funde sind benannt und lokal fixbar;
keine Struktur ist so tief von der Signatur durchsetzt, dass Neuschreiben nötig wäre.

## Testabdeckung kritischer Pfad (vorher → nachher)
Kritischer Pfad = {Aggregation (Geld+Verfassung), Determinismus (Sitzungswahl/
Zeitplan), Wart-Research→Journal}.

| Teilpfad | Vorher | Nachher (dieser Audit) |
|---|---|---|
| Aggregation end-to-end gegen die 3 realen Sitzungen | **0 %** (nur 9 synthetische Unit-Tests auf die Logik) | **~90 %** (10 Golden-Tests reproduzieren Konsens/Dissens/Konvergenz/konditional/`donation_url` je Säule aus den Rohvoten; nur der ≥4-Modell-Tiebreak N1 nicht in den Daten) |
| Determinismus-Funktionen | **0 %** | **3 von 4 gepinnt** (`resolve_session_id`, `prior_session`, `advance_schedule`); `latest_session` nicht — der Bug K2 verhindert einen deterministischen Test (dokumentiert) |
| Wart-Research→Journal (`run_wart`, `fallback_from_markdown`, convene) | **0 %** | **0 %** — hier leben beide kritischen Funde; ungetestet |

## Rewrite: JA / NEIN — **NEIN.**
Begründung (Zahlen):
1. Der **constitutionelle Kern zählt sauber** — 0 kritische/hohe Funde im Aggregator,
   verifiziert und jetzt golden-getestet. Ein Rewrite würde genau diesen bereits
   abgesicherten Kern neu riskieren.
2. Von 22 Funden sind nur **2 kritisch**, **beide im selben ~346-Zeilen-Modul
   (`run_wart.py`)** und **beide mit klarem, lokalem Fix** (fallback streichen; Sort
   nach `number`). Das ist gezielte Härtung, kein Strukturversagen.
3. Die 6 hohen Funde sind großteils **eine fehlende Validierungs-/Fehlerpfad-Schicht**
   (Schema-Check beim Laden/Schreiben, lauter Abbruch statt stiller Drop) — additiv
   einbaubar, ohne die Ablauflogik umzuschreiben.
4. Das **Golden-Netz** macht jede künftige Härtung verantwortbar: jede Änderung, die
   eine der drei publizierten Sitzungen anders ausgäbe, wird rot.

**Empfohlene Reihenfolge der Härtung (separater Auftrag, nicht dieser Lauf):**
(1) `run_wart` K1+K2 + H6-Governance-Entscheid; (2) Schema-Validierung beim
Schreiben (`schema/*.json`) → H1/H2/H3/M9; (3) Budget-Enforcement H5; (4) Canary
M7 + Kosten/`kosten.json`-Vereinheitlichung. Danach die Datenvertrag-Naht (Version-
Bump, Modell-Identität) vor dem Frontend-Anschluss.
