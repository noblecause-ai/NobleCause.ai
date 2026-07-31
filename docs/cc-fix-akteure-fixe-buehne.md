# Fix an CC — Akteure als fixe Bühne (Fehler 1: scrollen zur Decke)

**Befund (am Code lokalisiert):** In `site/src/lib/components/rooms/StudyActors.svelte`
ist `.scene2` (Zeile ~81) `position: absolute; inset: 0` und `.rail` (Zeile ~195/457)
ebenfalls `position: absolute` — beide sitzen in `.room-hero`, und das scrollt
(`min-height: 100svh`, normaler Fluss). Folge: Die Akteure gleiten korrekt seitlich ein,
scrollen dann aber **mit dem Inhalt nach oben aus dem Bild** ("bis zur Decke") — und der
Warden schwebt dabei über dem Boden. Wolke (`.clouds`) und Tür-Schimmer wurden einzeln auf
`position: fixed` gesetzt, die Akteur-Schienen **nicht**. Das ist der ganze Fehler.

## Fix
`.rail` auf `position: fixed` heben — dieselbe fixe Bühnen-Ebene wie `.room-bg` und
`.clouds`. Dann ist die **einzige** Scroll-Reaktion das seitliche Ausweichen über
`--retreat`; die Bodenlinie bleibt fest, nichts scrollt nach oben.

Konkret:
- Beide `.rail`-Regeln (Basis ~Zeile 195 und die Breakpoint-Blöcke ~457/512):
  `position: absolute` → `position: fixed`. Die `bottom`/`left`-Werte sind bereits
  svh/vw (viewport-relativ), passen also unverändert zu `fixed`.
- **Voraussetzung geprüft:** kein Vorfahre von `.rail` trägt `transform`/`filter`
  (`.scene2`, `.room-hero` sind transform-frei) — `fixed` bleibt viewport-verankert.
- `--retreat`-Scrub in `stage.js` (~Zeile 177) unverändert lassen — er liefert weiter den
  Seitwärts-Wert (Desktop: `translateX(--retreat * --side * 13vw)`).
- Kontaktschatten/Fußlinie bleiben auf der Diele; **Warden auf dieselbe Fußlinie wie der
  Scout** setzen (Scout-Fußlinie 82 % der Box, gemessen) — er sitzt aktuell zu hoch.

## Abnahme
Bei ~1440 px und 390 px langsam durchscrollen: Akteure bleiben auf Bodenhöhe, weichen nur
zur Seite (Desktop) bzw. zurück nach unten (Mobil, dorthin, wo sie einfuhren), erreichen
**nie** die Decke. No-JS/reduced-motion: Ruheposition unverändert (voller Zustand).

## Gilt auch für die Council-Pulte
Die Pulte nutzen dieselbe `.rail`-Mechanik — falls sie eine eigene Ebene/Klasse haben,
denselben `position: fixed`-Fix anwenden, sonst erben sie ihn.
