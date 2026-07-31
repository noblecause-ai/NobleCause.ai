# Szene-Prinzip: kantenverankerte Rahmen-Props (für Kimi)

**Steward-Vorgabe, 2026-07-24.** Formalisiert die bestehende Schienen-Mechanik
(`--retreat`/`--side` in `StudyActors.svelte`) als generelle Kompositions- und
Bewegungsregel für alle Räume.

## Kernregel
Jedes **bewegliche** Element der zweiten Ebene — die Akteure (Scout/Warden, Pulte,
Registerfächer) und optional einzelne kleinere Rahmen-Props (eine Pflanze, eine Kommode,
ein Lämpchen) — **berührt/schneidet immer einen Viewport-Rand.** Nie frei in der
Bildmitte.

**Warum:** So umrahmen die Props die Szene von den Rändern und halten die **Mitte frei für
Inhalt** (reisende Tafel, Text, Röhre). Und weil sie an der Kante sitzen, ist ihre
Bewegung ein sauberes **Hinein-/Hinausgleiten über die Kante** — kein Schrumpfen, kein
Verschwinden mitten im Bild.

## Drei Bewegungszustände
1. **Einfahren (Ankunft):** Der Hintergrund (Plate) **steht still.** Nur die Rand-Props
   gleiten von ihrer Kante herein. Danach Lock — die Szene ruht.
2. **Ausfahren (= Raumwechsel):** Die Props gleiten über ihre Kanten **hinaus**, und der
   Raum wechselt (Türfahrt). Das Hinausgleiten IST der Wechsel, kein separater Effekt.
3. **Scrollen:** Die Props fahren **teilweise** zu ihrer Kante zurück — **nur falls nötig**,
   um Platz für den scrollenden Inhalt zu schaffen. Scroll-Scrub (`--retreat`), kein harter
   Zustandsautomat.

## Konsequenzen für die Umsetzung
- Akteure sind an ihrer Kante verankert und verlassen die Szene über **genau diese Kante**
  (`--side`): Scout **links**, Warden **rechts**, Council-Pulte von **unten**,
  Archiv-Register von **unten**.
- **Der neue sitzende Scout wird links verankert** eingebaut — ein Teil (Figur/Stuhl) liegt
  an bzw. über der linken Viewport-Kante, damit der Rückzug/Austritt nach links sauber über
  den Rand läuft. Beim Positionieren nicht zentrieren, sondern an die Kante schieben.
- **Reduced-motion / No-JS:** alle Props stehen an ihrer Ruheposition (gerahmt), nichts
  bewegt sich — voller Zustand (§0).
- **Optionale Rand-Props als eigene Ebene:** Eine gemalte Pflanze/Lampe kann aus dem Plate
  als eigene kantenverankerte Ebene gelöst werden, **wenn** sie beim Scrollen mitweichen
  soll. Nur wo es den Inhalt spürbar entlastet — nicht als Selbstzweck. Jede zusätzliche
  Ebene zählt ins §4-Budget; im Zweifel bleibt der Prop im Plate (statisch).

## NACHTRAG (2026-07-24, nach dem Study-Einbau) — fixe Bühne + Tafel als Asset

### 1. Kein vertikales Mitscrollen — nur seitliches Ausweichen (Kernkorrektur, Bug)
Die zweite Ebene (Akteure, Tafel, Wolken) darf **nicht mit dem Text nach oben scrollen.**
Sie ist eine **fixe Bühne** — `position: fixed`, dieselbe Ebene wie `.room-bg` und
`.clouds`: Füße und Fundamente bleiben auf der gemalten Diele, egal wie weit man scrollt.
Der **einzige** Scroll-Effekt ist das **seitliche Ausweichen** (`--retreat`/`--side`).
*Grund:* Der mitscrollende Warden hob mit dem Text ab und „schwebte 3 Meter über dem
Boden" — das bricht das Bühnenbild. → Akteur-Rails (Scout/Warden) auf `position: fixed`
wie die schon gefixten Wolken; Bodenlinie fest; Scroll steuert nur die Seitwärts-Drift.

### 2. Warden auf dieselbe Bodenlinie wie Scout
Beide stehen auf **derselben Ebene** (gleiche Fußlinie). Aktuell sitzt der Warden zu hoch.
Scout-Fußlinie ist 82 % der Box (gemessen) — Warden auf dieselbe Diele setzen, damit beide
auf dem Boden stehen, nicht in der Luft.

### 3. Die Ergebnis-Tafel ist auch ein kantenverankertes Asset (Ecke oben-links)
Die Tafel wird behandelt wie ein Akteur: ein **Asset, das aus der oberen-linken Ecke
hereingleitet** (kurzer Versatz wie die Akteur-Beats, nicht nur Auf-Blenden) und in
**jeder Szene an derselben Stelle** sitzt. Sie bleibt **fix** (scrollt nicht mit) und reist
beim Raumwechsel weiter (VT-Shared-Element `board` — schon vorhanden).
- **Study-Maße:** etwas **breiter, dafür kürzer** — eine querformatige Plakette **oben,
  oberhalb des Scout**, statt eines hohen Panels.

### 4. Das löst zugleich den gemeldeten Tafel-Scout-Konflikt
Mit der breiteren, **kürzeren** Tafel **oben** und dem Scout **tief unten-links darunter**
sind beide **vertikal getrennt** — der Scout kann jetzt **wirklich an der linken Kante**
verankert werden (er sitzt unter der Tafel, nicht hinter ihr). Die bisherige
Desktop-Ausnahme („Scout zu ~95 % hinter der Tafel") entfällt damit: nicht mehr hinter der
Wand, sondern unter der Plakette. Reduced-motion/No-JS unverändert: alles an Ruheposition.

## Für die Bildbestellung (Codex)
Bewegliche Cutouts werden **vollständig und unbeschnitten** geliefert (transparenter
Grund) — die Kantenverankerung macht der Umsetzer per Platzierung, nicht der Generator.
Der Cutout muss aber **lesen, wenn ein Teil vom Rand beschnitten wird** (z. B. der Scout,
dessen linke Seite an der Kante sitzt): keine bildwichtigen Details ganz außen, die beim
Anschnitt verloren gingen.
