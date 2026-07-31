> **Kontext:** Zwei Reviews laufen gleichzeitig und **blind gegeneinander** — du siehst den Bericht des anderen nicht und fragst nicht danach. **Frische Session, kein Vorkontext:** wer seine eigene Baugeschichte im Kopf hat, prüft seine Erinnerung statt den Code. Du bist **Codex**.

Du prüfst eine Website vor ihrer ersten Veröffentlichung. Dies ist ein Review-Auftrag:
**du liest, misst und berichtest — du änderst nichts, committest nichts, pushst nichts.**

### 1 · Was das Projekt ist

**NobleCause.ai:** Drei KI-Modelle verschiedener Familien (Claude Opus, GPT, Gemini Pro)
prüfen dieselben Belege und empfehlen öffentlich, wo eine Spende voraussichtlich am meisten
bewirkt. Jede Sitzung wird vollständig und unverändert veröffentlicht. Vier Bereiche
(„Säulen"): Zukunft, Leid lindern, Große Gefahren, Was sonst übersehen wird.
Aggregationsregel: **zwei gleiche Nennungen ergeben eine Empfehlung.** Durch das System
fließt kein Geld; Spendenlinks führen direkt zu den Organisationen.

Technisch ein SvelteKit-Static-Build (`adapter-static`), inszeniert als drei nächtliche
Räume: **The Study** (Frage und Belege) → **The Council / Ratssaal** (Beratung) →
**The Archive** (das Protokoll). Dahinter ein Protokoll-Explorer (Sitzungen, Journal).
Deutsch ist Basissprache, Englisch liegt unter `/en/…` für die drei Räume.

Die Legitimation dieses Projekts ist **Nachprüfbarkeit**. Alles, was sie beschädigt, ist ein
schwerer Befund — auch wenn es hübsch aussieht.

### 2 · Nicht verhandelbar — hier gibt es nichts zu melden

Diese Entscheidungen stehen fest. Findings dagegen kosten nur Zeit:

- **§0:** Voller Inhalt ohne JavaScript und bei `prefers-reduced-motion`. Die Bühne
  verzögert und bewegt, sie **erzeugt und versteckt nie.**
- **Versiegelte Datennaht:** Das Frontend paraphrasiert nie. Sitzungs- und Journaltext
  stehen wörtlich. Der Renderer parst keine Prosa, nur strukturelle Signale. Prozessaussagen
  sind erlaubt („zwei gleiche Nennungen ergeben eine Empfehlung"), Ergebnisaussagen nie.
- **Kantenprinzip:** Bewegte Bühnenelemente sind `position: fixed`, kommen von der Kante
  herein, ziehen sich nur über `--retreat` zurück. Die Kulisse steht, bewegt wird die
  zweite Ebene.
- **Gestaltung:** Vignette statt Kasten. Gleiten und Licht statt Effekten. Schichtung statt
  Auswahl. Kein Weiß. Serifen für den Rekord, Versalien für die Ordnung. Dunkel ist
  Absicht, nicht Versehen.
- **Der Explorer ist kein vierter Raum** und bewegungslos.
- **Die Bildsprache steht.** Keine Vorschläge zu Motiven, Farbwelt oder Stil.
- **Der Rekord ist deutsch** und bleibt es, auch im englischen Zweig.

### 3 · Der Stand

- Branch `integration/go-live-0.4`, Tag `review-2026-08-01`, Commit `44f47cf`
- Worktree: `../nc-review-codex` — **arbeite nur dort**, nicht im Hauptbaum
- Build: **Node v20.20.2, npm 10.8.2** (wichtig: `rolldown` bringt native Bindings mit,
  eine andere Node-Version bricht den Build)
  ```
  npm ci
  rm -rf site/build site/.svelte-kit && npm run build
  npm run preview -- --port 4200
  ```
- Referenz-Screenshots liegen unter `docs/review/referenz-review-2026-08-01/`. Weicht dein Rendering
  davon ab, ist das selbst ein Befund — sag es, statt es zu übergehen.

Nichts ist bisher veröffentlicht. Alle URLs sind Permalinks auf den Rekord, sobald gepusht
wird — Adressfehler sind deshalb jetzt gratis und später teuer.

### 4 · Bekannt — bitte nicht melden

Diese Punkte stehen bereits auf der Liste:

- **erster Frame / LCP:** Plates laden sichtbar nach, beim Start steht kurz ein Rechteck
- **Explorer** hat keine visuelle Anbindung an die Bühne
- **Szenentext scheint hinter den Karten** im Abschnitt „Wie gezählt wurde" durch
- der Explorer ist **einsprachig deutsch**, auch aus dem englischen Zweig heraus
- Auslieferungs- und Cache-Parameter sind noch nicht gesetzt (kein Deploy erfolgt)
- `docs/` enthält unsortierte Arbeitsdokumente

### 5 · Dein Prüfumfang

Du prüfst, ob der Code hält, was der Rekord verspricht.

1. **Die Datennaht.** Paraphrasiert der Renderer irgendwo? Parst er Prosa statt
   struktureller Signale? Kann eine Anzeige vom publizierten Text abweichen?
   (`site/src/lib/server/content.js`, `homepage.js`, die Room-Komponenten)
2. **Die Aggregationslogik — hier bitte besonders genau.** Bildet sie „zwei gleiche
   Nennungen" korrekt ab, auch bei `conditional`, geändertem Votum, fehlendem Bereich,
   Dissens? **Hier saß schon einmal ein Fehler:** Organisationsnamen wurden per
   Zeichenkette verglichen, wodurch identische Organisationen als Dissens gewertet
   wurden. Der Korrekturhinweis dazu steht im Archiv. Sieh dir an, ob die heutige
   Auflösung über `organization_id` und `organizations.json` wirklich dicht ist.
3. **Zustandsführung der Bühne.** Türdurchgang (CSS-3D-Kamerafahrt, kein WebGL),
   `--retreat`, z-Order, Wiedereintritt ohne Neuladen. Speziell: das Archiv-Pult trägt
   `z-index: 4` und liegt damit vor dem Fluss — verdeckt es an irgendeinem Scrollstand
   oder Seitenverhältnis Rekordtext?
4. **Fehlerpfade.** Verhalten bei fehlenden Feldern, try/catch-Riegel, SSR/Client-Parität
   (Datumsformatierung ist UTC-fest — gilt das überall?), Prerender-Robustheit.
5. **`gremium/**` nur lesend:** Schlüsselbehandlung, Kostenzählung, Härtung. **Nichts
   ändern** — das ist geschützter Pfad.
6. **Die Szene und der Titelbereich** (`StageHero`, die `*Actors.svelte`) gehören
   ausdrücklich in deinen Umfang, nicht in Kimis.

### 6 · Wie du berichtest

Eine Datei: `docs/review/review-2026-08-01-<dein-name>.md`. Je Finding:

- **Ort:** Datei und Zeile, oder Route und Viewport
- **Beobachtet:** was passiert
- **Erwartet:** was stattdessen richtig wäre
- **Schwere:** `blockiert-go-live` · `punktversion` · `geschmack`

**Die Schwere-Einstufung ist Pflicht.** Ohne sie ist der Bericht eine Wunschliste und
kostet mehr Zeit, als er spart. Ordne streng ein: `blockiert-go-live` heißt, dass ein
Besucher Schaden nimmt oder der Rekord falsch dargestellt wird — nicht, dass es dich stört.

Wenn du unsicher bist, ob etwas Absicht ist: **melden mit der Einstufung `geschmack` und
einer Frage**, statt es zu übergehen oder als Fehler zu deklarieren.

Am Ende des Berichts drei Zeilen: **was du geprüft hast, was du nicht geprüft hast, und
worauf du beim nächsten Mal zuerst sehen würdest.** Der zweite Punkt ist der wichtigste —
eine ehrliche Lücke ist mehr wert als ein vollständig klingender Bericht.

### 7 · Grenzen

- **Nichts ändern.** Keine Datei bearbeiten, kein Commit, kein Push, kein Branch.
- **`gremium/**`, `sessions/**`, `journal/**`, `schedule.json`, `schema/**` sind geschützt**
  — lesen ja, anfassen nein.
- Nur im dir zugewiesenen Worktree arbeiten.
- Keine Vorschläge zur Bildsprache, Farbwelt oder zum Grundkonzept (siehe §2).
- Du siehst den Bericht des anderen Reviewers nicht und sollst nicht danach fragen.
