# Briefing für den frischen CC — NobleCause.ai Bühnenspiel

**Erstellt:** 2026-07-24 von Opus 5 (Architekt/Review) · **Für:** Claude Code (Bau, Opus 5)
**Lies dieses Dokument zuerst, dann §2 in dieser Reihenfolge. Nichts anderes vorab.**

---

## 1 · Wer du bist und wie hier gearbeitet wird

- **Du = Bau.** Du sitzt direkt am Repo: `npm run build`, `vite preview`, CDP-Reflow-Messung,
  pre-commit-Hook. Du schreibst Code.
- **Opus 5 (Cowork-Session) = Architekt + Review.** Schreibt Pläne, prüft deinen Diff gegen
  die Abnahmekriterien. Nicht dein Konkurrent — dein Gegenleser.
- **Fable (claude-fable-5) = Wart:** Governance, Klartext-Freigaben, Journal.
- **Codex/ChatGPT = Bilder** (Serien-Aufträge, Kontaktbogen-Gates).
- **Steward = Afschin**, letzte Instanz. Deutsch, knapp, sachlich. Er ist Informatiker
  (20 J. IT-Beratung, 10 J. SAP BI): Tools und Architektur wählst du selbst, **legst sie ihm
  aber als Plan vor und begründest sie**, bevor du baust. Eigene Fehler offen benennen — das
  zählt hier mehr als eine glatte Meldung.
- **Kimi wurde der Bauauftrag entzogen** (Qualität). Falls er wieder verfügbar ist, darf er
  deinen Code **bewerten**, nicht bauen.

**Rückmeldung an den Review:** Wenn ein Paket steht, meldest du den **Diff** plus die
Messwerte aus dem jeweiligen Abnahmeblock. Nicht „ist gebaut", sondern was du gemessen hast.

## 2 · Leseordnung (kurz halten, nicht alles lesen)

1. `docs/HANDOVER-2026-07-24-opus5.md` — der Gesamteinstieg, Zustand je Raum
2. `AGENTS.md` — harte Grenzen und Sauberkeitsregeln
3. `docs/szene-kantenprinzip-fuer-kimi.md` — das Kompositionsgesetz (inkl. Nachtrag 24.07.)
4. `docs/cc-fix-akteure-fixe-buehne.md` — dein erstes Arbeitspaket
5. `docs/opus5-review-raumuebergang-2026-07-24.md` — dein zweites Arbeitspaket (§B) und die
   Korrekturen am WebGL-Plan (§A), falls das Portal später kommt
6. Nur bei Bedarf: `docs/buehnenspiel-gesamtbild-fuer-kimi.md` (Vision),
   `docs/raum-content-final-fuer-kimi.md` und `docs/titelbereich-neuordnung-fuer-kimi.md`
   (Copy/Reihenfolge — nur lesen, wenn du Content anfasst)

Alles andere in `docs/` ist Historie (Kimi-, Codex-, Fable-Berichte). Nicht durcharbeiten.

## 3 · Verfassungsrang — nie brechen

- **§0:** Die Seite ist **vollständig, bevor das Spiel beginnt.** No-JS und
  `prefers-reduced-motion: reduce` zeigen denselben vollen Zustand. Inszenierung **verzögert
  und bewegt nur** — sie erzeugt und versteckt nie Inhalt. Jeder Anfangszustand lebt
  ausschließlich unter `html.stage-armed` (JS-gesetzt) und nur ohne Reduced-Motion.
- **Wirkung ist Pflicht, nicht Kür.** Die Seite soll beeindrucken — sie ist die Auslage des
  Protokolls, und der Wow-Effekt ist ein **Muss**. Zielgruppe ist, wer **genau hinsehen**
  will *und* wer **schnell Überblick** braucht; beides bedient dieselbe Seite über
  **Schichtung** (Klartext vorn, Rekord dahinter), nie über Vergrößerung oder Reduktion.
  **Lesbarkeit ist Randbedingung, nie Gestaltungsziel.** Kollidieren Wirkung und Lesbarkeit,
  wird die Schichtung geändert — nicht die Wirkung heruntergefahren.
  → **Zurückgezogen (Steward-Klarstellung 2026-07-24): der „80-Jährige" als
  Gestaltungsleitbild.** Dieser Weg wurde einmal zu Ende gegangen und endete bei Großtext
  ohne Charme. Er darf nicht als Argument gegen Gestaltung wiederkehren — auch nicht in
  abgeschwächter Form („kostet Aufmerksamkeitsbudget"). Wer hier spendet, kommt nicht trotz,
  sondern wegen der Machart.
- **Versiegelte Datennaht:** Das Frontend paraphrasiert nie. Sitzungsabhängiger Text kommt
  aus den Daten, feste Copy aus `lib/i18n/de.js`/`en.js` (Spiegel — beide oder keine).
- **Kanten-/Bühnenprinzip:** Bewegliche Elemente sind viewport-kantenverankert und
  `position: fixed`. Sie scrollen **nicht** vertikal mit; der einzige Scroll-Effekt ist das
  seitliche bzw. vertikale Ausweichen über `--retreat`.
- **Tabu-Pfade** (`AGENTS.md`): `sessions/**`, `journal/**`, `schema/**`, `gremium/**`,
  `schedule.json`, `**/prompts.py`. Ein `pre-commit`-Hook blockt Commits, die diese Pfade auf
  `feat/*` berühren. **Nie mit `--no-verify` umgehen.** Scheint eine Aufgabe das zu
  verlangen: **stoppen und melden.**
- **Nie Push auf `master`, nie Merge ohne ausdrückliche Freigabe. Kein Commit ohne
  Steward-Freigabe.**
- **Was zweimal verschoben wurde, wird beim dritten Mal sperrend.** (Präzedenz: der
  320-px-Reflow-Nachweis.)

## 4 · Git-Stand (verifiziert 2026-07-24)

```
Branch:        feat/council-rooms      (Wegwerf-Präsentationsbranch)
Trunk:         master                  (nicht main!)
HEAD:          f3e67ed  data: Klartext-Schicht Bootstrap — drei Bestandssitzungen
Uncommitted:   139 Einträge            = die gesamte Frontend-Arbeit, bewusst uncommittet
```

Die 139 Einträge werden später zu sauberen Einheiten gesquasht. Committe nicht ungefragt
dazwischen. Datenpublikationen laufen auf einem Nicht-`feat/*`-Branch.

Git-Identität in diesem Repo dauerhaft setzen, falls noch nicht geschehen:
`git config user.email 105276395+AfshinMirhamed@users.noreply.github.com`

## 5 · Codestand, den ich am Code verifiziert habe (nicht vermutet)

Damit du nicht suchst — Stand `site/src/`:

- **Bühnen-Mechanik:** `lib/stage.js` (Eintrittsmodi `fresh`/`arrival`/`language`,
  `--retreat`-Scroll-Scrub, Lock + Watchdog, Tür-Preload) und `lib/room-transitions.js`
  (Klick-Handler, Räum-Beat 480 ms, View-Transition, Röhren-Diff). **Das sind die einzigen
  Stellen mit Navigationslogik** — keine Teilmechanik bekommt eigene.
- **`StudyActors.svelte`: der Akteur-Fix ist NOCH NICHT drin.** `.scene2` (Z. 82) und die
  `.rail`-Basisregel (Z. ~196) stehen weiterhin auf `position: absolute`. Die Wolken
  (`.clouds`) und der mobile `.door-shimmer` (Z. ~136) sind bereits `fixed` — daran siehst
  du das Zielmuster.
- **Die Tafel-Neuordnung aus dem Kantenprinzip-Nachtrag §3 ist NOCH NICHT gebaut.**
  `ResultBoard.svelte` ist ab 1200 px weiterhin ein **hohes** Panel:
  `position: fixed; top: 15.5rem; left: 1.25rem; width: 22rem`. Der Nachtrag verlangt
  **breiter und kürzer, oben** als querformatige Plakette.
  → **Abhängigkeit, die im Handover untergeht:** Der Scout steht auf Desktop noch an der
  alten Ausnahmeposition (`.rail.scout { left: calc(23.5rem + 18svh) }` — „hinter der
  Tafel"). Ihn an die **linke Viewport-Kante** zu ziehen (Nachtrag §4) geht erst, **nachdem**
  die Tafel breit/kurz nach oben gewandert ist. Der `position: fixed`-Fix aus Paket 1 ist
  davon unabhängig und kann sofort landen.
- **Tür-Hotspot** (`StudyRoom.svelte`, Z. ~244 ff.): existiert erst **ab 1200 px**, Geometrie
  in zwei Aspect-Ratio-Zweigen exakt aus der Cover-Crop-Mathematik der Plate abgeleitet.
  Unterhalb 1200 px ist die Tür die `.door-gallery`-Karte im Fluss. Jeder Portal-Effekt ist
  damit von Haus aus ein Desktop-Effekt.
- **Shared Elements der View-Transition:** `board` (ResultBoard) und `masthead`
  (`.stable-head` im StageHero). Gruppenregeln stehen in `routes/(rooms)/+layout.svelte`.

## 6 · Deine Arbeitspakete, in dieser Reihenfolge

**Paket 1 — Akteur-Fix.** `docs/cc-fix-akteure-fixe-buehne.md`. `.rail` auf
`position: fixed`, Warden auf die Scout-Fußlinie (82 % der Box). Der schnellste sichtbare
Gewinn. Die Scout-Kantenverankerung gehört **nicht** hierher (siehe §5, Abhängigkeit).

**Paket 2 — Tür-Gegenprobe.** `docs/opus5-review-raumuebergang-2026-07-24.md` §B. Der
Zielraum wird per `clip-path` aus der Türkontur aufgezogen, statt den ganzen Frame zu
ersetzen. Enthält den fertigen CSS-Block, das JS-Wiring und einen §0-Nebenfix in
`room-transitions.js` (Watchdog gegen dauerhaft ausgeräumte Bühne). Ergebnis geht an den
Steward, bevor über 3D entschieden wird.

**Paket 3 — Council verifizieren.** Kimi berichtete den Einbau der neuen Saal-Plates; der
Steward sah noch alte Hintergründe. Wahrscheinlichster Grund: **stale `vite preview`-Cache**.
**Erst frisch bauen und den Preview neu starten, dann urteilen — nichts neu bauen, bevor das
geprüft ist.**

**Später (nicht jetzt):** Archive Serie 3 (Bilder noch nicht geliefert), EN-Klartext,
Tafel-Neuordnung + Scout an die Kante, echtes-Gerät-Mobiltest, squash/merge auf `master`.
Das WebGL-Portal steht bis nach dem Go-Live zurück; falls es kommt, gelten §A1–A7 des
Review-Dokuments (u. a.: 3D-Ebene ins persistente Layout, VT und Live-Durchflug schließen
sich aus, CSS-3D vor Three.js, `perspective` bricht `position: fixed`).

## 7 · Verifikation — gilt für jedes Paket

- `npm run build` in `site/` **warnungsfrei**; Testsuite grün (zuletzt 21/21).
- **Nach jedem Build den Preview neu starten.** `vite preview`/sirv cached Assets im
  Speicher — sonst misst und siehst du den alten Stand. Das ist die bekannteste Falle in
  diesem Projekt und hat schon einmal einen falschen Befund erzeugt.
- Reflow bei **320 und 390 px** per CDP-Emulation (`mobile: true`), alle 6 Raum-Routen,
  kein horizontaler Overflow. Desktop-Gegenprobe bei 1440 px.
- **No-JS und `prefers-reduced-motion: reduce` = voller Ruhezustand**, bitidentisch mit dem
  JS-Endzustand. Das ist die **erste** Prüfung, nicht die letzte.
- Beim Durchscrollen bleiben Akteure auf Bodenhöhe und weichen nur aus — sie erreichen nie
  die Decke.
- Kein Commit ohne Steward-Freigabe.

---

### Kickoff-Prompt (zum Einfügen in die frische CC-Session)

> Du bist CC (Bau) für NobleCause.ai, Branch `feat/council-rooms`, Repo
> `~/Projects/NobleCause.ai`. Lies zuerst `docs/cc-briefing-2026-07-24.md` vollständig, dann
> die dort in §2 genannten Dokumente in der angegebenen Reihenfolge. Baue noch nichts.
> Melde mir danach: (a) dein Verständnis von §0 und dem Kantenprinzip in drei Sätzen,
> (b) deinen Plan für Paket 1 (Akteur-Fix) mit den konkreten Zeilen, die du änderst,
> (c) alles, was dir im Briefing widersprüchlich oder unvollständig vorkommt.
> Erst nach meiner Freigabe änderst du Code. Antworte deutsch, knapp, sachlich.
