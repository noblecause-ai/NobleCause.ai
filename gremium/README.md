# gremium/ — die Deliberations-Pipeline

Führt eine Gremium-Sitzung als Batch-Lauf durch und schreibt das Protokoll
nach `../sessions/YYYY-MM/`. Kein Server, kein Zustand: Der Orchestrator
(`run_session.py`) ist ein deterministisches Skript — kein LLM steuert den
Ablauf, Modelle liefern ausschließlich Voten.

## Ablauf eines Laufs

Standardmodus:

1. **Runde 1:** Jedes Modell (3 Familien: Anthropic, OpenAI, Google) erhält
   Manifest + Fragestellung + Quellenliste (`sources.md`) und votiert
   unabhängig, mit Konfidenz und strukturiertem JSON-Abschluss.
2. **Runde 2:** Jedes Modell liest die Erstvoten der beiden anderen und gibt
   Schlussvotum + Dissens-Abschnitt ab.
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
2. **Runde 0 — Wart-Dossier:** Fable mit Web-Suche liefert Evidenz-Dossier.
3. **Runde 1:** Council votiert unabhängig.
4. **Moderation durch den Wart:** Fable schreibt Moderationsnotiz zur Gegenlese
   (wird in Runde-2-Prompt injiziert).
5. **Runde 2:** Council liefert Schlussvoten.
6. **Kurzfassung durch den Wart:** Summary/Dissens-Highlights via Fable.

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
- `--with-dossier`: aktiviert Runde 0 (Wart-Dossier mit Web-Suche).
- `--led-by-wart`: aktiviert Eröffnung + Moderation + Wart-Summary und setzt
  automatisch `--with-dossier`.
- `--budget-cap`: Budgetdeckel in EUR (Default `15.0`), Zwischenkosten werden
  nach jedem Schritt geprüft.

Danach: Ergebnis prüfen, committen, pushen — die Site rendert die Sitzung
automatisch. Protokolle sind nach Veröffentlichung unveränderlich
(`run_session.py` verweigert das Überschreiben existierender Ordner).

## Dateien

| Datei | Zweck |
|---|---|
| `run_session.py` | Orchestrator (der gesamte Ablauf) |
| `run_wart.py` | wöchentlicher Wart-Research-Lauf (Journal + schedule) |
| `prompts.py` | die wörtlichen Prompt-Vorlagen (werden mitveröffentlicht) |
| `sources.md` | Referenzquellen, die den Modellen mitgegeben werden |
| `config.json` | Modelle, Preise pro 1M Tokens, USD→EUR-Kurs, Output-Limit |

## Kadenz

- **Sitzungen:** manuell (`make session` oder `run_session.py`), Ziel:
  monatlich bzw. ad hoc bei Bedarf.
- **Wart-Research:** wöchentlicher Cron ist aktiv über
  `.github/workflows/wart.yml` (Mo, 06:00 UTC), ruft `run_wart.py` auf und
  committed Journal + `schedule.json`.
