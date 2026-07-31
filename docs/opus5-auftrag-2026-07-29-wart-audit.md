# Auftrag an CC — Audit der Automatik vor Go-Live

**Von:** Opus 5 (Architekt), 29. Juli 2026
**Dringlichkeit:** höchste. `schedule.json` sagt `next_session: 2026-08-06T12:00:00Z` —
**in acht Tagen.** Die Seite verspricht diesen Termin sichtbar im Ratssaal.
**Diagnose only. Nichts an der Automatik ändern** ohne Rückmeldung an den Steward — er hat
das Secret-Thema bereits zweimal angefasst, das zweite Mal mit langem Debugging.

---

## Der Anlass

- `origin/master` = `57c3416` („journal: Wart-Eintrag 2026-07-20")
- lokaler `master` = `5071194` (Rekord-Stamm + Kommission)

Der **27. Juli war ein Montag**. `wart.yml` läuft `cron: '0 6 * * 1'`. Wäre der Lauf
durchgegangen und hätte etwas gefunden, stünde `origin/master` weiter. Tut es nicht.
Der lokale Journal-Eintrag `2026-07-27` ist der **Kommissionslauf**, nicht der Wart —
der letzte echte Research-Lauf bleibt der 20. Juli.

Drei Erklärungen sind möglich, und sie führen zu völlig verschiedenen Konsequenzen:

1. Der Lauf **fiel aus** (Workflow deaktiviert, Secret fehlt, Abbruch) → Issue mit Label
   `ci-failure:wart` müsste offen sein.
2. Der Lauf **lief und fand nichts** → `git diff --staged --quiet` griff, „Keine Änderungen
   zum Committen", exit 0, kein Commit, **kein Issue**. Dann ist alles in Ordnung — aber
   dann fehlt auch ein Journal-Eintrag, den es nach Kanon geben müsste.
3. Der Lauf **lief und scheiterte still** → Artefakt `wart-raw-*` vorhanden.

## Was zu prüfen ist

```
gh run list --workflow=wart.yml --limit 10
gh run list --workflow=session.yml --limit 10
gh issue list --label "ci-failure:wart" --state all
gh secret list                       # nur Namen, nie Werte
gh api repos/:owner/:repo --jq .default_branch
```

Berichte zu jedem Punkt **mit Zeitstempel und Ergebnis**:

1. **Ist der Lauf vom 27.07. gestartet?** Wenn ja: Status, Dauer, Log-Ende. Wenn nein:
   ist `wart.yml` in der Actions-Oberfläche deaktiviert?
   *Hintergrund:* GitHub schaltet `schedule`-Trigger nach **60 Tagen ohne
   Repository-Aktivität** automatisch ab. Letzte Aktivität auf `origin` war der 20. Juli —
   noch nicht kritisch, aber der Mechanismus ist real und trifft ein Projekt, das
   monatelang nur lokal arbeitet. **Das ist ein Argument dafür, endlich zu pushen.**
2. **Sind alle drei Secrets gesetzt?** `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`,
   `GEMINI_API_KEY`. `session.yml:65–76` fordert alle drei; `run_session.py:644` bricht
   sonst ab. `wart.yml` braucht nur den Anthropic-Key — eine fehlende OpenAI-/Gemini-Key
   würde den Wart also **nicht**, die Sitzung am 6. August aber **sehr wohl** stoppen.
   Nur Namen berichten, nie Werte, nie Längen im Klartext-Kanal.
3. **Welcher Branch ist Default?** `wart.yml` und `session.yml` laufen per `schedule` nur
   vom Default-Branch. `actions/checkout@v5` steht ohne `ref:` — der Lauf arbeitet also auf
   dem Default-Stand. Liegt die `envtools.py`-Härtung (`load_env`, `require_keys`) dort?
   `gremium/**` ist auf `feat/*` Tabupfad und **kann von dort nie committet worden sein** —
   wenn die Härtung nur lokal existiert, läuft der Cron die alte Fassung.
4. **Läuft `session.yml` täglich sauber durch?** `cron: '0 12 * * *'`, also jeden Tag.
   Wenn die täglichen Läufe seit Wochen scheitern, merkt es niemand, bis der 6. August
   kommt. Status der letzten zehn Läufe.
5. **`schedule.json`:** Der Wart committet die Datei auf `master`; auf `feat/council-rooms`
   ist sie seit `72c78d5` untracked. **Beim Merge feat→master prüfen, dass die vom Cron
   geschriebene Fassung nicht überschrieben wird.** Aktuell steht dort
   `next_research: 2026-07-27T06:00:00Z` — ein Datum in der Vergangenheit. Das ist für die
   Anzeige unschädlich (der Wart-Termin wird aus dem Rhythmus berechnet, nicht gelesen),
   aber es ist ein Symptom: **die Datei wurde seit dem 20. Juli nicht mehr fortgeschrieben.**

## Was NICHT zu tun ist

- Keine Änderung an `gremium/**`, `wart.yml`, `session.yml`, `prompts.py`.
- Kein Preflight nachbauen — `envtools.py` ist bereits die stärkere Fassung, ein dritter
  wäre die schwächste (siehe `noblecause-raumuebergang-entscheid-2026-07-24.md`).
- Keine Secrets anlegen, rotieren oder ausgeben.
- Kein `workflow_dispatch`-Testlauf ohne Freigabe des Stewards — ein Wart-Lauf schreibt
  Rekord und kostet Geld.

## Ergebnis

Ein Bericht mit einem von drei Sätzen am Anfang:

- **„Die Automatik läuft, der 6. August ist gedeckt."** — dann Punkt 1 abgehakt.
- **„Die Automatik läuft, aber X fehlt."** — dann X als eigener Auftrag, vor Go-Live.
- **„Die Automatik läuft nicht."** — dann geht die Seite **nicht** live, bevor das steht.
  Eine Seite, die einen Sitzungstermin verspricht und ihn nicht hält, beschädigt genau das,
  wovon sie lebt.
