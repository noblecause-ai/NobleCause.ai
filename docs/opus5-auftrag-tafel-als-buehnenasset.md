# Die Ergebnis-Tafel als Bühnen-Asset — Analyse und Bauauftrag

**Von:** Opus 5 (Architekt/Review) · **Für:** CC (Bau) · **Datum:** 2026-07-27
**Anlass, Steward:** Die Tafel wirkt gröber als der Rest, und sie ist beim Szenenübergang das
einzige bleibende Element und behindert damit den Effekt. Vorschlag: dieselbe Behandlung wie
die Scout-/Warden-Plaketten — transparent, an immer derselben Stelle, ein- und ausfahrend wie
jedes andere Asset.

---

## §1 · Zwei Beobachtungen, ein Befund

**Die Behandlung.** `.result-board` trägt einen opaken Grund und einen Goldrahmen — die
Formsprache, die `StageHero.svelte` für den Kopf ausdrücklich verworfen hat („Schwebende
Plakette: weiche Vignette statt opaker Kasten"). Die Akteur-Plaketten folgen inzwischen der
Vignette. Die Tafel ist das letzte Element im alten Duktus.

**Die Masse.** Ab 1200 px ist die Tafel `position: fixed; top: 15.5rem; left: 1.25rem;
width: 22rem` — eine hohe Spalte über die halbe Bildhöhe. Das ist derselbe Befund noch einmal:
Der Nachtrag im Kantenprinzip (24.07., §3) fordert die Tafel längst **„etwas breiter, dafür
kürzer — eine querformatige Plakette oben"**. Dieser Umbau ist **nie gebaut worden.** Er ist
zugleich die Vorbedingung dafür, den Scout an die linke Viewport-Kante zu verankern (Nachtrag
§4); solange die Tafel die linke Spalte hält, ist die alte Ausnahme „Scout an der Tafelkante"
in Kraft.

→ „Wirkt gröber" ist beides: der Rahmen **und** die Masse. Wer nur den Rahmen wegnimmt, löst
die Hälfte.

## §2 · Warum die Tafel den Übergang behindert — die exakte Ursache

`.result-board` trägt `view-transition-name: board`. Ein benanntes Element bildet in der
View-Transition eine **eigene Gruppe** und liegt damit **außerhalb des Root-Snapshots** — also
außerhalb der Türblende, die den Zielraum aus der Türkontur aufzieht. Deshalb ist die Tafel
das einzige Element, das an der Blende nicht teilnimmt: sie steht als hartkantiger Block
darüber, während der Raum durch die Tür wächst.

Das ist kein Stilproblem, das ist die Mechanik. Und es war Absicht — die „reisende Tafel" ist
ein Bild aus der Gründungsvision (`docs/buehnenspiel-gesamtbild-fuer-kimi.md`: „die Antwort
erscheint auf einer reisenden Tafel"). Wer sie ein- und ausfahren lässt, **überschreibt ein
Vision-Element**, nicht nur eine CSS-Zeile. Das gehört bewusst entschieden, nicht nebenbei.

## §3 · Drei Wege

> **ENTSCHIEDEN (Steward, 2026-07-27): Weg A — nur die Vignette**, und **zusammen mit der
> Zeitschicht in einem Commit** (beide fassen `ResultBoard.svelte` an; die Zeitschicht setzt
> die Datenzeile, Weg A die Haut).
> **Bewusst in Kauf genommen:** Die Übergangs-Behinderung aus §2 bleibt — die Tafel trägt
> weiter `view-transition-name: board` und nimmt an der Türblende nicht teil. Weg B bleibt als
> Nachtrag von zwei Zeilen jederzeit verfügbar, ohne dass Weg A dafür zurückgebaut werden muss.
> **§4 (Kontrast) gilt unverändert und ist bei Weg A das Hauptrisiko** — die Vignette ist die
> ganze Änderung, also hängt die Lesbarkeit der Antwort allein an ihr.

**A — nur die Vignette.** Rahmen und Deckgrund raus, Scrim wie `.room-plaque`, `text-shadow`.
Löst „gröber", **nicht** die Übergangs-Behinderung. Kleinster Eingriff.

**B — Vignette + Shared Element nur während der Türfahrt aussetzen.** *(Empfehlung.)*
`view-transition-name: none` auf `.result-board`, solange `html[data-portal]` gesetzt ist.
Dann ist die Tafel bei der Türfahrt Teil des Root-Snapshots und wird von der Blende **mit
aufgezogen** — genau der Effekt, den der Steward will. Bei allen anderen Navigationen
(Sprachwechsel, Back/Forward) reist sie weiter wie vorgesehen. Die Vision bleibt intakt, die
Behinderung verschwindet. Zwei Zeilen CSS plus die Vignette.

**C — Vignette + echtes Bühnen-Asset + Nachtrag-Umbau.** Kein `view-transition-name` mehr; die
Tafel fährt über ihre Kante hinaus und wieder herein wie die Akteure (`--retreat`-Mechanik
existiert), dazu der ausstehende Umbau auf „breiter, kürzer, oben". Das ist die wörtliche
Fassung des Steward-Wunsches und räumt zugleich die linke Spalte für den Scout. **Größter
Eingriff, größtes Review** — und er überschreibt die reisende Tafel.

## §4 · Die harte Randbedingung: Kontrast

Die Tafel trägt **die Antwort und die Spendenlinks** — das ist der Zweck der Seite. Hier ist
Lesbarkeit **Boden, nicht Geschmack.** Für Kopf und Akteur-Plaketten genügt eine Vignette,
weil sie große Schrift über den dunkelsten Bildzonen tragen; die Tafel hat kleine Schrift,
Links und **sie steht in allen drei Räumen an derselben Stelle** — auch im Ratssaal und im
Archiv, deren Plates dort heller sind.

Verbindlich:
- Kontrast von **Organisationsnamen und Spendenlinks gegen die tatsächlich gerenderten Pixel**
  messen, nicht gegen Nominalfarben, und zwar **in allen drei Räumen** an der Tafelposition.
- Reicht der Scrim nicht: Scrim verstärken oder eine zweite, sehr flache Lage hinter dem
  Textblock — **nicht** die Schrift vergrößern. Wirkung ist Pflicht, aber die Antwort muss
  lesbar sein; das ist die eine Stelle, an der die Randbedingung gewinnt.
- `backdrop-filter: blur()` ist eine Option, aber kein Default: teuer, im
  View-Transition-Snapshot unzuverlässig, braucht Fallback. Nur wenn der Scrim scheitert.

## §5 · Drei Anschlüsse, die mitkippen

1. **Der interne Scroll.** Die Tafel scrollt bei niedrigen Viewports in sich
   (`scrollbar-width: thin`). Ohne Rahmen fehlt die Kante, die dem Auge sagt, dass hier
   abgeschnitten wird. Ersatz: eine weiche Maske (`mask-image`) an der Unterkante statt einer
   Scrollleiste — sonst wirkt abgeschnittener Text wie fehlender Text.
2. **Die Textspalte weicht der Tafel aus.** `.room-section` trägt ab 1200 px
   `margin-left: max(calc(50% - 35rem), 25.5rem)` — hart auf die 22 rem plus Abstand gerechnet.
   Jede Formänderung (Weg C) muss diesen Wert mitziehen, sonst kollidiert der Fließtext.
3. **Unter 1200 px** fließt die Tafel in `main` mit dem Scrim dahinter. Die Vignette darf dort
   nicht doppelt auftragen (Scrim + Vignette = Matsch) und nicht zu wenig (Text über Bild).
   Eigener Nachweis bei 390 px.

## §6 · Abnahme

1. **Kontrast** in allen drei Räumen an der Tafelposition gemessen, Werte im Bericht.
2. **Türfahrt:** Frame bei ~150 ms — die Tafel wird von der Blende aufgezogen (Weg B/C) bzw.
   die Behinderung ist unverändert dokumentiert (Weg A). Kopf (`masthead`) bleibt stabil.
3. **Sprachwechsel und Back/Forward** (Weg B): Tafel reist weiter wie bisher.
4. Niedrige Viewports: 1280 × 720 und 1440 × 700 — Akteur-Plaketten weiterhin vollständig über
   der Kopflinie, keine Kollision mit der Tafel; bei 1280 klärte der Scout zuletzt nur 10 px.
5. Interner Scroll: abgeschnittener Text ist als abgeschnitten erkennbar.
6. Reflow 320/390, No-JS und Reduced-Motion unverändert vollständig, Build warnungsfrei,
   Testsuite grün, Preview neu gestartet.

## §7 · Reihenfolge

Weg B ist in einem Durchgang mit der Vignette machbar und lässt sich isoliert abnehmen.
Weg C sollte **nicht** in denselben Commit wie die Zeitschicht — er ändert Form, Position und
Choreografie der Tafel gleichzeitig, und die Zeitschicht setzt gerade eine neue Datenzeile in
dieselbe Tafel. Erst Zeitschicht abnehmen, dann C.
