# Auftrag: The Archive einbauen

**Für:** CC · **Von:** Opus 5 · **2026-07-27**
Vier gelieferte Assets, ein vorhandenes Plate, eine Montage im Haus. **Keine weitere
Codex-Runde nötig.**

## 1 · Assets einsortieren

| Quelle in `docs/` | Ziel | Bemerkung |
|---|---|---|
| `ChatGPT Image 27. Juli 2026, 04_00_37.png` | `scenes/archive-display.avif` | Plate quer, ersetzt die alte Kulisse |
| `…04_40_10.png` | `scenes/archive-portrait-display.avif` + `-800.avif` | Plate hoch; 800er ist ein Export |
| `…04_42_32.png` | `actors/register.avif` | **Magenta → Alpha keyen** |
| `…04_44_44.png` | `ambient/window-frame-study.avif` | **Magenta → Alpha keyen** |
| `…04_45_58.png` | `ambient/window-sky-study.avif` | deckend, kein Key |

**Keying:** Der gelieferte Master ist RGB auf `#FF00FF`. Beim Ausschlüsseln entstehen
Magenta-Säume an weichen Kanten — Kantensaum entfernen, nicht nur Farbe auf transparent
setzen. Und: **Geometrie am gerenderten AVIF messen, nicht am Master.** Beim Scout wich der
Master um ~3 % ab; das hat dich in Paket 1 einen Korrekturlauf gekostet.

`ambient/window-*` werden **nur abgelegt**, nicht verbaut — das ist Serie 4 und liegt nach dem
Go-Live (`docs/codex-serie-4-fensterblick.md`).

**Hinweis zum Medien-Strang:** Diese Dateien gehören in denselben untracked-Medien-Komplex,
den du beim Council gemeldet hast. Nicht dein Auftrag, aber sie vergrößern ihn.

## 2 · Tür-offen-Plate selbst montieren

**Kein Generator.** Vorlage ist `scenes/antechamber-door-open-display.avif` im Vergleich zum
geschlossenen Plate: es ist **dieselbe frontale Tür, die Flügel eine Handbreit aufgezogen** —
schmaler warmer Lichtspalt in der Mittelfuge, Lichtpfütze auf der Diele, ein Schimmer an der
oberen Laibung. Sonst pixelgleich. Genau deshalb funktioniert die Überblendung.

Dasselbe aus `archive-display.avif` bauen → `scenes/archive-door-open-display.avif`.
**Abnahme: außerhalb der Türöffnung Pixel-Differenz null.**

## 3 · Den Raum bauen

**Tür-Hotspot, Archiv-eigene Werte.** Die Tür im Archiv-Plate ist kleiner als in Study und
Council (grob x 42–56 %, y 18–63 % statt 40–60 / 17–82). **Nicht nachbestellen** — miss die
Türkanten am Plate und rechne die zwei Aspect-Ratio-Zweige wie in `StudyRoom.svelte`
(~Z. 256–275) neu. Die Türblende liest ihr Rechteck beim Klick aus `getBoundingClientRect()`
und passt sich von selbst an; identische Geometrie über alle Räume war meine Vorliebe, keine
Anforderung.
Dazu der Crossfade auf das Tür-offen-Plate wie in `StageHero` (`.room-bg-open`), inklusive der
0,14-s-Regel unter `stage-clearing`.

**`ArchiveActors.svelte`** nach dem Muster von `CouncilActors.svelte`: `register.avif` mehrfach
platziert wie das Lesepult, auf `.rail`-Schienen, **`position: fixed`** (Paket 1), von der
**unteren Kante** einfahrend, Rückzug über `--retreat` nach unten. Fußlinie am gerenderten
AVIF messen.

**Mobil:** eigener `.door-shimmer` für das Hochformat-Plate; die Study-Koordinaten passen nicht.

**Zeitschicht:** Die Archiv-Zeile trägt **keine Zukunft** — nur die Vergangenheit mit Datum
(`home.archive[].date`, §4.2 des Zeitschicht-Konzepts). Prüfen, ob die Daten am Regal schon
sichtbar sind.

## 4 · Ein Vorbehalt, den nur der Einbau klärt

Der Karteikasten liest **fotografisch**, die Plates und die Akteur-Cutouts sind gemalt. Ob die
Rauminszenierung das absorbiert, zeigt sich erst in der Szene. Falls nicht: malerischer
Durchgang, keine Neubestellung. Bitte einen Frame davon mitschicken.

## 5 · Abnahme

Türblende landet auf der gemalten Tür (Frame bei ~150 ms) · Register scrollen nicht zur Decke,
weichen nur nach unten · Tür-offen außerhalb der Öffnung pixelgleich · Reflow 320/390 ·
No-JS und Reduced-Motion voller Zustand · Build warnungsfrei, Tests grün, Preview neu.
