# gremium/ — die Beratungs- und Abstimmungspipeline

Führt eine Gremium-Sitzung als Batch-Lauf durch und schreibt das Protokoll
nach `../sessions/YYYY-MM/`. Kein Server, keine Datenbank: Der Orchestrator
(`run_session.py`) ist deterministisch. Modelle liefern Beratungsinhalt und
Voten; die Zählung bleibt vollständig im Code.

Der neue **Live-Rat 0.6** ist als ausgeschalteter Backend-Pilot vorbereitet:
fünf Stimmen, rotierender Vorsitz, fortlaufende Debatte und Ereignisrekord.
Er wird ausdrücklich mit `--live-council` aufgerufen und schreibt isolierte
Artefakte statt veröffentlichter Sitzungen. Im Standardmodus sperrt B4 echte
Modellaufrufe, solange die belegten Eingabe-Kostengrenzen fehlen. Der Steward
hat für den ersten Pilot ausdrücklich `--observe-costs` freigegeben:
[Kostenbeobachtung und Testergebnis](../docs/live-rat-kostenbeobachtung-2026-09-20.md).
Bedienung, Nachweise und
offene Schritte stehen in [der Backend-Abnahme](../docs/live-rat-backend-2026-09-20.md).
Die folgende Standardbeschreibung gilt weiterhin für den bisherigen Ablauf.

## Ablauf eines Laufs

Standardmodus:

1. **Runde 1:** Jedes Modell (3 Familien: Anthropic, OpenAI, Google) erhält
   Manifest + Fragestellung + Quellenliste (`sources.md`) und votiert
   unabhängig, mit Konfidenz und strukturiertem JSON-Abschluss.
2. **Runde 2 — Gegenlese:** Jedes Modell liest die Erstvoten der beiden anderen
   und gibt Schlussvotum + Dissens-Abschnitt ab. Das aktuelle Verfahren
   erzwingt noch keine namentlich adressierte Erwiderung; diese Form ist für
   Version 0.5 vorgesehen.
3. **Aggregation (deterministisch):** Nennen ≥2 Modelle für eine Säule
   dieselbe Organisation, ist das die Gremium-Empfehlung; sonst werden die
   Einzelvoten mit Attribution gelistet. Der Orchestrator urteilt nie selbst.
4. **Kurzfassung:** Zusammenfassung + Dissens-Highlights durch das konfigurierte
   Summarizer-Modell.
5. **Protokoll:** `session.json` (Schema: `../sessions/README.md`) plus alle
   Rohantworten unter `raw/`. Kosten werden aus den Usage-Daten der APIs und
   den Preisen in `config.json` berechnet.

Wart-geleiteter Modus (`--led-by-wart`, impliziert `--with-dossier`):

1. **Eröffnung durch den Wart (Fable):** eigener Call ohne Tools.
2. **Runde 0 — Scout-Dossier:** Opus mit Web-Suche liefert das Evidenz-Dossier.
3. **Runde 1:** Council votiert unabhängig.
4. **Moderation durch den Wart:** Fable schreibt Moderationsnotiz zur Gegenlese
   (wird in Runde-2-Prompt injiziert).
5. **Runde 2:** Council liefert Schlussvoten.
6. **Kurzfassung durch den Wart:** Summary/Dissens-Highlights via Fable.

## Vorbereitete Verfahrensschalter (standardmäßig aus)

`config.json` enthält Verfahrensschalter unter `features`. Alle stehen auf
`enabled: false`; ihr Vorhandensein ändert daher weder Wochenlauf noch Sitzung.

- **`two_scouts`:** Verlangt bei Aktivierung genau zwei Einträge in
  `config.scouts`, aus zwei verschiedenen Familien; mindestens eine Familie
  muss außerhalb des Rates liegen und kein Scout darf zugleich Wart sein.
  Beide erhalten denselben Auftrag. Beide Wortlaute, Ausfälle und ein exakter
  (nicht semantisch geratener) Divergenzausweis werden veröffentlicht. Ein
  gültiges Dossier kann den Ausfall des anderen Scouts auffangen; fallen beide
  aus, entsteht ein sichtbarer Refusal-Rekord ohne Wart-Entscheid. Als zweiter
  Provider ist der bestehende Google-Zugang vorbereitet: Der Adapter nutzt
  Gemini Search Grounding und übernimmt nur tatsächlich gemeldete Suchqueries
  in Nutzung und Rekord. Die konkrete Scout-Besetzung bleibt bis zum
  Steward-Entscheid unkonfiguriert.
- **`deliberation_0_5`:** Fügt nach den unabhängigen Erstvoten eine adressierte
  Erwiderung ein. Jedes Modell muss genau eine überprüfbare Behauptung eines
  anderen, durch Modell-ID benannten Teilnehmers stützen, bestreiten oder
  präzisieren. Die Haltung wird als `support | dispute | refine` geführt. Nur
  strukturierte Felder werden an das Zielmodell weitergegeben; ungültige oder
  ausgefallene Erwiderungen bleiben sichtbar, verhindern aber nicht die
  Schlussvoten. Für die Empfehlung zählt weiterhin ausschließlich die
  deterministische Aggregation der strukturierten Schlussvoten.
- **`three_scouts`:** Drei voneinander unabhängige, zunächst blinde Recherchen;
  Besetzung und Herkunftsnachweise siehe [Scout-Adapter](../docs/scout-adapter-2026-09-20.md).
- **`live_council`:** Bereitet die Wochenrolle des nächsten Vorsitzes vor.
  Der Sitzungspilot benötigt weiterhin ausdrücklich `--live-council`; das
  bloße Einschalten aktiviert keinen öffentlichen Sitzungslauf. Verfahren:
  [Nachtrag 0.6](../docs/verfahren-0.6.md).

Vor der ersten echten Aktivierung sind Steward-Freigabe, synthetische Abnahme,
eine veröffentlichte DE/EN-Verfahrenserklärung und ein ausdrücklich genehmigter
Kostenrahmen erforderlich. Alte Sitzungs- und Journalrekorde werden dadurch
nicht verändert.

## Benutzung

```bash
make install                      # einmalig: pip-Abhängigkeiten
export ANTHROPIC_API_KEY=…        # oder in gremium/.env (gitignored)
export OPENAI_API_KEY=…
export GEMINI_API_KEY=…

make session \
  QUESTION="Welche drei Interventionen bieten 2026 pro 1'000 € die höchste erwartbare Wirkung je Säule?" \
  TITLE="Eröffnungsfrage: Wirkung pro 1'000 €"
```

Direktaufruf mit Optionen:

```bash
python3 run_session.py \
  --session-id 2026-07c \
  --number 3 \
  --title "Gründungssitzung: Auflösung des Säule-A-Dissens" \
  --question "..." \
  --with-dossier
```

Wart-Leitung:

```bash
python3 run_session.py \
  --led-by-wart \
  --session-id 2026-07c \
  --number 3 \
  --title "Gründungssitzung: Auflösung des Säule-A-Dissens" \
  --question "..."
```

Wichtige Flags:
- `--with-dossier`: aktiviert Runde 0 (Scout-Dossier mit Web-Suche).
- `--led-by-wart`: aktiviert Eröffnung + Moderation + Wart-Summary und setzt
  automatisch `--with-dossier`.
- `--budget-cap`: Budgetdeckel in EUR (Default `15.0`), Zwischenkosten werden
  nach jedem Schritt geprüft.

Danach: Ergebnis prüfen, committen, pushen — die Site rendert die Sitzung
automatisch. Protokolle sind nach Veröffentlichung unveränderlich
(`run_session.py` verweigert das Überschreiben existierender Ordner).
Korrekturhinweise sind additiv; deterministische Backfills abgeleiteter
Strukturfelder benötigen Steward-Freigabe und dürfen Rohvoten oder Prosa nicht
ändern.

## Dateien

| Datei | Zweck |
|---|---|
| `run_session.py` | Orchestrator (der gesamte Ablauf) |
| `run_wart.py` | Wochenlauf: Scout-Recherche, Wart-Entscheid, Journal + schedule |
| `run_commission.py` | getrennte Modellbestellung außerhalb einer Sitzung |
| `reaggregate.py` | freigabepflichtige, deterministische Rekordkorrekturen aus Rohvoten |
| `prompts.py` | die wörtlichen Prompt-Vorlagen (werden mitveröffentlicht) |
| `sources.md` | Referenzquellen, die den Modellen mitgegeben werden |
| `config.json` | getrennte Ämter, stärkstes produktionsreifes Ratsmodell je Familie, Preise, USD→EUR-Kurs |

## Kadenz

- **Sitzungen:** manuell (`make session` oder `run_session.py`), Ziel:
  monatlich bzw. ad hoc bei Bedarf.
- **Scout/Wart:** wöchentlicher Cron ist aktiv über
  `.github/workflows/wart.yml` (Mo, 06:00 UTC), ruft `run_wart.py` auf und
  lässt erst den Scout recherchieren, dann den Wart entscheiden und committed
  Journal + `schedule.json`.

## Secrets & CI

Drei API-Keys treiben die Pipeline. Sie kommen aus **zwei getrennten Quellen** —
das ist Absicht, nicht Zufall:

| Key | Lokal | In CI (GitHub Actions) | Geprüft von |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | `gremium/.env` (gitignored) | Repo-Secret | wart, session, preflight |
| `OPENAI_API_KEY` | `gremium/.env` | Repo-Secret | session, preflight |
| `GEMINI_API_KEY` | `gremium/.env` | Repo-Secret | session, preflight |

**Warum der `.env`-Fallback in CI aus ist.** `envtools.load_env()` ist ein
No-op, sobald `CI=true` (GitHub Actions setzt das automatisch). In CI ist die
Actions-Secret-Umgebung die **einzige** Quelle der Wahrheit. Früher fiel eine
lokal-gefüllte, in CI leere Key-Lage nicht auf → der erste geplante Lauf starb an
`401 invalid x-api-key`. Jetzt: kein stiller `.env`-Fallback in CI, und
`envtools.require_keys(...)` bricht **vor** dem ersten API-Call hart ab (`exit 1`,
klare Meldung, nur Zeichenzahl — nie der Wert), wenn ein Key fehlt oder leer ist.

**google-genai-Fallstrick.** Das SDK liest `GOOGLE_API_KEY` bevorzugt, sonst
`GEMINI_API_KEY` (beide gesetzt → Warnung, `GOOGLE_API_KEY` gewinnt). Projekt-
Konvention und Secret-Name ist **`GEMINI_API_KEY`**. Nicht beide setzen.

**Canary (`preflight.py` / `preflight.yml`).** Läuft täglich 05:30 UTC und macht
pro Anbieter einen minimalen Live-Call — fängt einen abgelaufenen/rotierten Key,
bevor ein echter Lauf daran scheitert. Manuell triggern: GitHub → Actions →
„Preflight — Key-Canary" → **Run workflow** (`workflow_dispatch`). Rot = ein Key
fehlt/leer oder ein Anbieter nicht erreichbar.

**Fehlersichtbarkeit.** `wart.yml`, `session.yml` und `preflight.yml` haben je einen
`if: failure()`-Step, der ein Issue mit Run-URL + Log-Auszug anlegt (Label
`ci-failure:<workflow>`) bzw. ein offenes Issue gleichen Labels aktualisiert —
kein Duplikat-Spam.

**Secrets setzen:** Repo → Settings → Secrets and variables → Actions → New
repository secret. `GITHUB_TOKEN` wird von Actions automatisch bereitgestellt
(nicht manuell setzen).
