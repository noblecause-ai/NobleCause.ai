# Auftrag an CC — Review-Umgebung für Kimi 3 und Codex vorbereiten

**Von:** Opus 5 (Architekt), 29. Juli 2026
**Wann:** nach dem Abschluss-Durchgang und nach dem Aufräumen des offenen Strangs,
**vor** Merge und Push. Der Stand muss eingefroren sein — ein Review auf einem dirty
Arbeitsbaum ist kein Review, weil kein Reviewer sagen kann, *was* er geprüft hat.

---

## 1 · Der eingefrorene Stand

1. Arbeitsbaum sauber: kein `git status`-Eintrag außer bewusst ignorierten Pfaden.
   Der offene Strang (`gremium/prompts.py`, `AGENTS.md`, Medien-Strang) ist vorher geklärt
   — nicht „für später liegengelassen".
2. Annotiertes Tag auf dem Review-Stand:
   `git tag -a review-2026-07-XX -m "Stand für UI- und Code-Review"`
3. Reproduzierbarer Build, im Briefing wörtlich dokumentiert: Node-Version, `npm ci`,
   `rm -rf site/build site/.svelte-kit && npm run build`, `npm run preview`.
   **Wichtig:** dieselbe Node-Version nennen, mit der du gebaut hast — `rolldown` bringt
   native Bindings mit, ein Versionssprung bricht den Build beim Reviewer.
4. Ein Referenz-Screenshot-Satz aus **deinem** Build: Study / Council / Archive / Explorer,
   je 1440 und 390, plus Ruhebild und Hover für Türen, Medaillons, 2b und den neuen
   Pult-Eingang. Zweck: „bei mir sieht das anders aus" von einem echten Finding
   unterscheidbar machen.

## 2 · Das Briefing (eine Datei, `docs/review-briefing-2026-07-XX.md`)

### 2.1 · Nicht verhandelbar — das ist kein Findings-Gebiet

Ein Reviewer ohne Kontext meldet sonst zuverlässig „warum kein helles Theme", „warum keine
Motion-Library", „warum wird der Rekord nicht zusammengefasst". Jede dieser Meldungen kostet
dich eine Antwortrunde. Schreib die Prämissen an den Anfang, nicht ans Ende:

- **§0:** voller Inhalt ohne JS und bei `prefers-reduced-motion`. Die Bühne verzögert und
  bewegt, sie erzeugt und versteckt nie.
- **Versiegelte Datennaht:** das Frontend paraphrasiert nie. Sitzungs- und Journaltext
  wörtlich. Prozessaussagen erlaubt, Ergebnisaussagen nie.
- **Kantenprinzip**, Vignette statt Kasten, kein Weiß, Serifen für den Rekord.
- **Explorer ist kein vierter Raum** und bewegungslos.
- Bildsprache und Farbwelt stehen. **Keine Gestaltungsvorschläge zur Bildsprache.**

### 2.2 · Bekannte offene Punkte — bitte nicht melden

Ohne diese Liste bekommst du zwanzig Findings zu Dingen, die längst auf der Liste stehen:

- linke Ergebnis-Tafel schneidet bei kurzem Viewport unten ab (in Arbeit)
- Routen-Inkonsistenz `/ratssaal/` · `/archiv/` gegen `/sessions/` · `/journal/` (in Arbeit)
- erster Frame / LCP: Plate lädt sichtbar nach (Punktversion)
- Explorer ohne visuelle Anbindung an die Bühne (Punktversion)
- Szenentext scheint hinter den 2b-Karten durch (Punktversion)
- 57 unsortierte Zeitstempel-Bilder in `docs/`
- nichts ist gepusht; Cache-/Auslieferungsparameter liegen beim Leitstand

### 2.3 · Prüfumfang, getrennt nach Reviewer

**Codex — Code und Substanz:**
- Datennaht: paraphrasiert der Renderer irgendwo? Parst er Prosa statt struktureller
  Signale? (`content.js`, `homepage.js`, die Room-Komponenten)
- Aggregationslogik: bildet sie „zwei gleiche Nennungen" korrekt ab — auch bei
  `conditional`, geändertem Votum, fehlendem Bereich? Der Korrekturhinweis vom 14.07.
  zeigt, dass hier schon einmal ein Fehler saß: Namensvergleich per Zeichenkette.
  **Genau dort noch einmal hinsehen.**
- Zustandsführung der Bühne: Türdurchgang, `--retreat`, z-Order, Wiedereintritt ohne
  Neuladen. Speziell der **neue `z-index: 4` am Pult** — verdeckt das Möbel an irgendeinem
  Scrollstand oder Seitenverhältnis Rekordtext?
- Fehlerpfade: try/catch-Riegel, Verhalten bei fehlenden Feldern, SSR/Client-Parität
  (`formatDate` ist UTC-fest — gilt das überall?)
- `gremium/**` nur lesend: Härtung, Schlüsselbehandlung, Kostenzählung.

**Kimi 3 — UI und Zugänglichkeit:**
- Tastaturpfad durch alle drei Räume und den Explorer. Reihenfolge, Fokussichtbarkeit,
  Fallen. **Bekannt und gemeldet:** das Pult ist der zweite Tab-Stopp, vor dem Hauptinhalt.
  Bewertung erwünscht, Reparaturvorschlag ohne `tabindex`-Flickerei.
- Kontrast gegen bewegte, dunkle Plates — nicht gegen `--bg`, sondern gegen das, was
  tatsächlich hinter dem Text liegt.
- Screenreader: Alt-Texte, `aria-label` am Pult-Eingang, `<time>`-Semantik,
  Landmarks, ob die Bühne als Dekoration erkennbar ist.
- Verständlichkeit ohne Vorwissen: Findet jemand in 30 Sekunden, **wo er spenden soll**
  und **warum diese Organisation**? Das ist der Kernpfad.
- 320 / 390 / 768 / 1440 / ultrawide.

> **Hinweis zur Besetzung:** Kimi 3 hat an Szene und Titelbereich selbst mitgebaut
> (`szene-kantenprinzip-fuer-kimi.md`, `titelbereich-neuordnung-fuer-kimi.md`). Für diese
> beiden Bereiche reviewt er seine eigene Arbeit — dort ist sein Urteil schwächer.
> Entweder diese Bereiche ausdrücklich Codex zuweisen, oder das Risiko benennen und
> in Kauf nehmen.

### 2.4 · Findings-Format

Jedes Finding: **Datei und Zeile oder Route und Viewport · beobachtet · erwartet · Schwere
(blockiert Go-Live / Punktversion / Geschmack)**. Ohne die Schwere-Einstufung ist die
Rückmeldung eine Wunschliste. Ablage: `docs/review/2026-07-XX-<reviewer>.md`,
eine Datei pro Reviewer, keine Sammelmails.

## 3 · Danach

Der Architekt sichtet beide Berichte, sortiert nach Schwere und legt fest, was vor dem Push
kommt und was in die Punktversion geht. **Erst danach Merge und Push.**
