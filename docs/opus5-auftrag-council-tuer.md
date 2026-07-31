# Auftrag: Tür-Hotspot im Ratssaal (Council → Archive)

**Für:** CC · **Von:** Opus 5 · **2026-07-27** · Ein File, zwei Ergänzungen.

## Befund

`CouncilRoom.svelte` trägt `sceneOpen="/media/scenes/hall-door-open-display.avif"` (Z. 71),
aber **keinen `.door-hotspot`**. Study und Archive haben einen, der Ratssaal nicht. Folgen:

- Die gemalte Tür im Ratssaal ist nicht klickbar — der Weg ins Archiv läuft nur über die
  Galerie-Karte.
- Das Tür-offen-Plate ist praktisch toter Ballast: `.room-bg-open` wird in `StageHero` über
  `:has(.door-hotspot:hover)` bzw. `:has(…:focus-visible)` sichtbar. Ohne Hotspot öffnet sich
  die Tür nie beim Hovern; sie blitzt nur noch unter `html.stage-clearing` auf, also erst
  *nach* dem Klick auf eine Karte.

Alles Übrige ist vorhanden: `ORDERS` in `room-transitions.js` enthält `/ratssaal/` → `/archiv/`,
der Klick-Handler matcht `.door-hotspot[href]`, und `t.council.doors` führt den `/archiv/`-
Eintrag bereits (Label „The Archive").

## 1 · Markup

Im `overlay`-Snippet von `CouncilRoom.svelte`, analog zu `StudyRoom.svelte` (~Z. 78–86): den
`/archiv/`-Eintrag aus `t.council.doors` ziehen und

```svelte
<a class="door-hotspot" href={archiveDoor.href}
   aria-label="{archiveDoor.sub}: {archiveDoor.label}"
   title="{archiveDoor.sub}: {archiveDoor.label}"
   onclick={setDoorOrigin}></a>
```

`setDoorOrigin` wie in `StudyRoom` (setzt `--vt-origin`).

## 2 · CSS — Ratssaal-eigene Werte

Gemessen am Plate (`hall-display.avif`, 1672 × 941): Türzone inkl. Laibung
**x 43,5 %–57,9 %, y 18,3 %–65,9 %**. Unterkante bewusst bei 66 %, **nicht** tiefer — sonst
liegt der Hotspot über der Zählmaschine auf ihrem Sockel und schluckt sie.

Alle Räume nutzen `bgPos="center top"`, also gelten dieselben zwei Umrechnungen wie in
`StudyRoom`/`ArchiveRoom` (an StudyRooms Bestandswerten nachgerechnet, sie reproduzieren exakt):

```
Zweig A (max-aspect-ratio 16/9, Bild füllt die Höhe, horizontal zentriert):
  left   = 50vw − 88.89svh + f0·177.78svh      top    = g0·100svh
  width  = (f1−f0)·177.78svh                   height = (g1−g0)·100svh

Zweig B (min-aspect-ratio 16/9, Bild füllt die Breite, Crop ab top):
  left   = f0·100vw                            top    = g0·56.25vw
  width  = (f1−f0)·100vw                       height = (g1−g0)·56.25vw
```

Daraus:

```css
@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
  .door-hotspot {
    left: calc(50vw - 11.56svh);
    top: 18.3svh;
    width: 25.6svh;
    height: 47.6svh;
  }
}
@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
  .door-hotspot {
    left: 43.5vw;
    top: 10.29vw;
    width: 14.4vw;
    height: 26.78vw;
  }
}
```

Der Basis-Block (`display: none`, ab 1200 px `position: absolute` + `pointer-events: auto` +
`:focus-visible`-Outline) übernimmst du unverändert aus `ArchiveRoom.svelte`.

**Meine Werte sind visuell abgelesen — bitte die Türkanten am Plate nachmessen und korrigieren,
wenn sie abweichen.** Die Umrechnungen stimmen, die vier Prozentzahlen sind der weiche Teil.

## 3 · Eine Prämisse von mir war falsch

Ich habe zweimal geschrieben, die Türzone müsse in allen drei Räumen dieselbe sein, und das dann
für das Archiv als Ausnahme freigegeben. **Sie war nie dieselbe.** Study 40–60 % × 17–82 %,
Ratssaal 43,5–57,9 % × 18,3–65,9 %, Archiv (deine Messung) 43–54,5 % × 19,5–62,5 %. Jedes Plate
hat seine eigene Tür. Per-Raum-Geometrie ist keine Konzession, sondern der Normalfall — und
unschädlich, weil die Türblende ihr Rechteck beim Klick aus `getBoundingClientRect()` liest.

## 4 · Abnahme

1. **1440 px und 1280 px:** Hover über die gemalte Tür öffnet sie (Crossfade auf
   `hall-door-open-display.avif`); der Hotspot deckt die Tür und **nicht** die Zählmaschine.
2. Klick → Türfahrt ins Archiv, Blende zieht den Archivraum aus der Türkontur auf; Frame bei
   ~150 ms einfrieren.
3. Tastatur: Tab erreicht den Hotspot, `:focus-visible`-Outline sichtbar, Enter löst die Fahrt
   aus (der Handler setzt `--vt-origin` auf die Kartenmitte).
4. Beide Aspect-Ratio-Zweige geprüft (schmaler und breiter als 16:9).
5. `< 1200 px`: Hotspot `display: none`, Weg läuft über die Galerie — unverändert.
6. Reflow 320/390, No-JS und Reduced-Motion unverändert, Build warnungsfrei, Tests grün.
