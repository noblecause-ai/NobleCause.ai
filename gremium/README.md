# gremium/ — die Deliberations-Pipeline

Führt eine Gremium-Sitzung als Batch-Lauf durch und schreibt das Protokoll
nach `../sessions/YYYY-MM/`. Kein Server, kein Zustand: Der Orchestrator
(`run_session.py`) ist ein deterministisches Skript — kein LLM steuert den
Ablauf, Modelle liefern ausschließlich Voten.

## Ablauf eines Laufs

1. **Runde 1:** Jedes Modell (3 Familien: Anthropic, OpenAI, Google) erhält
   Manifest + Fragestellung + Quellenliste (`sources.md`) und votiert
   unabhängig, mit Konfidenz und strukturiertem JSON-Abschluss.
2. **Runde 2:** Jedes Modell liest die Erstvoten der beiden anderen und gibt
   Schlussvotum + Dissens-Abschnitt ab.
3. **Aggregation (deterministisch):** Nennen ≥2 Modelle für eine Säule
   dieselbe Organisation, ist das die Gremium-Empfehlung; sonst werden die
   Einzelvoten mit Attribution gelistet. Der Orchestrator urteilt nie selbst.
4. **Protokoll:** `session.json` (Schema: `../sessions/README.md`) plus alle
   Rohantworten unter `raw/`. Kosten werden aus den Usage-Daten der APIs und
   den Preisen in `config.json` berechnet.

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

Danach: Ergebnis prüfen, committen, pushen — die Site rendert die Sitzung
automatisch. Protokolle sind nach Veröffentlichung unveränderlich
(`run_session.py` verweigert das Überschreiben existierender Ordner).

## Dateien

| Datei | Zweck |
|---|---|
| `run_session.py` | Orchestrator (der gesamte Ablauf) |
| `prompts.py` | die wörtlichen Prompt-Vorlagen (werden mitveröffentlicht) |
| `sources.md` | Referenzquellen, die den Modellen mitgegeben werden |
| `config.json` | Modelle, Preise pro 1M Tokens, USD→EUR-Kurs, Output-Limit |

## Kadenz

v0 = manueller Lauf (`make session`), Ziel: monatlich. Ein GitHub-Actions-Cron
ist bewusst noch nicht eingerichtet — erst wenn sich die Kadenz bewährt hat.
