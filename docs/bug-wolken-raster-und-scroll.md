# Bug — Wolkenebene: sichtbares Schachbrett-Raster + scrollt mit statt fix

**Gemeldet:** Steward · 2026-07-23 · **Betrifft:** The Study, zweite Ebene (Wolkenzug)
**Schwere:** sichtbarer Darstellungsfehler auf der Startseite — vor Go-Live zu beheben.
**Bewertung:** kein Umsetzungsfehler von Kimi, sondern ein durchgereichter Asset-Mangel
plus eine Positionierungs-Regel. Der Steward hatte gegen die Nachbestellung entschieden
(„Neugenerierung ist billig") — die Wolke wurde dennoch mit dem defekten Master
integriert. Das ist der Auslöser für Befund 1.

## Symptom
Über der statischen Vorzimmer-Szene liegt im Fensterbereich (und darüber hinaus) ein
sichtbares graues **Schachbrett-Raster**; beim Scrollen wandert dieses Raster **nach
oben aus dem Bild**, während das gemalte Hintergrundbild stehen bleibt. (Screenshot beim
Steward.)

## Befund 1 — Schachbrett ist ins Bild gemalt (kein Alphakanal)
`static/media/ambient/clouds-study.avif` ist **`mode=RGB`, KEIN Alphakanal**
(384×512). Das „Transparenz"-Schachbrett steckt als graue Pixel im Bild — genau der
Mangel, den das Serie-1b-Gate für alle Cutouts und die Wolke gemessen hat
(`docs/review/serie-1b-gate/`).

In `StudyActors.svelte` wird das Bild mit `mix-blend-mode: screen; opacity: 0.5`
gelegt. `screen` schluckt die dunklen Kacheln weitgehend, aber die **hellen Kacheln
bleiben sichtbar** — sie leuchten als Raster über der Szene. Ohne echten Alphakanal kann
kein Blend-Modus das sauber lösen.

**Ursache:** Der defekte Master wurde eingebaut, statt ihn nach dem Gate-Befund zu
ersetzen. Die Entscheidung Retusche vs. Neugenerierung (siehe
`prompt-kimi-serie-1b.md` und die Steward-Freigabe „Neugenerierung ist ausdrücklich
erlaubt, billiger als Rumwerkeln") steht noch aus — der Einbau kam ihr zuvor.

**Fix:** Kein Blend-Trick. Die Wolkenebene braucht einen **echten Alphakanal**. Zwei
Wege, Entscheidung liegt bei dir (Kimi):
1. Neu generieren mit sauberem, transparentem Hintergrund (Freigabe liegt vor), oder
2. den vorhandenen Master freistellen — bei der Wolke günstig, da der Motivinhalt hell
   auf flachem Schachbrett liegt (das Gate hielt das für machbar).
Bis dahin: **Wolkenebene deaktivieren**, nicht defekt ausliefern.

## Befund 2 — Ebene scrollt mit, statt an der fixen Szene zu haften
Das Hintergrundbild `.room-bg` (StageHero) ist `position: fixed; inset: 0; z-index: 0`
— es bleibt beim Scrollen stehen. Die Wolkenebene sitzt aber in `.scene2`
(StudyActors), und die ist `position: absolute; inset: 0` **relativ zum `.room-hero`**,
der mit dem Inhalt wegscrollt (`min-height: 100svh`). Folge: Die Wolke scrollt nach
oben aus dem Bild, während die gemalte Szene liegen bleibt — die Ambient-Bewegung löst
sich vom Fenster, auf das sie gehört.

**Fix:** Die Wolkenebene (bzw. die ganze `.scene2`-Bildebene) muss demselben
Positionierungs-Regime folgen wie `.room-bg` — **fix zur Szene, nicht zum scrollenden
Hero**. Sie gehört visuell in die fixe Bildebene (z-index 0), nicht in den Fluss.
Prüfen, dass sie damit weiterhin **unter** Tafel/Text (z-index ≥ 2) und dem Tür-Hotspot
liegt.

## Randbedingungen für den Fix (unverändert gültig)
- `prefers-reduced-motion`: Ebene steht still (ist bereits so verdrahtet — beibehalten).
- Ohne JS / No-JS-Boden: kein Regression; die Ambient-Ebene ist reine Zugabe.
- §4-Budget: die 384×512-Ebene (0,20 MP) zählt mit; nach dem Fix nachmessen.
- Der Effekt darf beim ersten Hinsehen nicht auffallen (Steward-Regel) — nach dem Fix
  Deckkraft/Drift gegenprüfen.

## Abnahme
Screenshot bei ~1440 px und bei 390 px, jeweils oben und nach ~600 px Scroll: kein
Raster sichtbar, Wolke haftet am Fenster, bewegt sich nur durch die Drift. Bei
Reduced-Motion: Standbild, kein Raster.

## NACHTRAG (2026-07-24) — Bewegung unsichtbar: Perzeptibilität anheben

Steward-Befund: „sehe beim besten willen keine wolkenbewegung." Zwei Ursachen, in
Reihenfolge prüfen:

1. **Reduced-Motion beim Betrachter** (macOS „Bewegung reduzieren" / Browser). Dann ist
   das Standbild korrekt — kein Fix nötig, nur bestätigen. Falls der Steward Bewegung
   TROTZ reduced-motion will, wäre das eine bewusste Ausnahme von §0 und separat zu
   entscheiden (Default bleibt: still).
2. **Zu langsam + zu faint** (wenn reduced-motion aus ist). Rechnung: 48 s für ±8 % im
   ~224 px-Fenster = **0,75 px/s** — unter der Wahrnehmungsschwelle. Tuning, bis die
   Bewegung bei ruhigem Hinsehen (3–5 s) sanft sichtbar ist, aber nicht von der Tafel
   ablenkt:
   - **x-Drift-Periode kürzen** (Startwert ~24–28 s statt 48 s), **y länger lassen**
     (teilerfremd, damit kein Pendeln entsteht — z. B. 24 s × 41 s).
   - **Amplitude leicht erhöhen** (±8 % → ~±12 %); Overscan im `.clouds img` entsprechend
     nachziehen (aktuell 120 %/112 %), damit die Ränder nie ins Fenster laufen.
   - **Sichtbarkeit prüfen**: opacity 0,5 → ~0,6 testen; erst sicherstellen, dass die
     freigestellte Wolke überhaupt gegen das Fenster liest (Standbild-Screenshot der
     Fensterzone), dann Bewegung tunen — sonst tunt man eine unsichtbare Ebene.
   - Danach gegen die Steward-Regel gegenprüfen: bei erster flüchtiger Sicht ruhig, beim
     Verweilen lebendig. Kurze Frame-Sequenz (t0/t+2s/t+4s) zur Abnahme.
