# Bestellung Serie 5 — Archiv neu (geräumte Flanken) + Tür in Ebenen

**Von:** Opus 5 (Architekt) · **Für:** Afschin zum Copy/Paste in eine frische Bild-Session
**Stand:** 2026-07-27 · **Ablage der Ergebnisse:** `docs/` (Dateinamen siehe unten)

---

## Warum diese Bestellung

**Problem 1 — Verdopplung.** Der heutige Archiv-Plate (`scenes/archive-display.avif`) trägt in
beiden unteren Ecken bereits eine Anrichte mit Messingleuchte und aufgeschlagenem Buch. Genau
dieses Möbel fährt seit dem letzten Bau als Akteur ein. Die zweite Ebene kann nur wirken, wenn
die Kulisse an den Flanken **leer** ist. Bewegtes Möbel gehört in die zweite Ebene, gemaltes
Möbel in die Kulisse — nie beides dasselbe.

**Problem 2 — die Tür ist gemalt.** Der Raumwechsel ist heute eine Blende. Für den echten
Durchgang (Kamera fährt durch die Öffnung) braucht die Tür **Tiefe**, und Tiefe entsteht nur,
wenn Wand und Türflügel getrennte Ebenen sind.

**Der Trick, der die Bestellung klein hält:** Wir bestellen **nicht** den geschlossenen Raum.
Wir bestellen die Wand **mit offener Laibung** (P7) und die **Türflügel einzeln** (P8) — und
setzen den geschlossenen Zustand daraus selbst zusammen. Damit entfallen zwei Positionen, die
sonst pixelgenau deckungsgleich sein müssten (der alte „Tür offen"-Plate und seine
Registrierung). Deckungsgleichheit ist geschenkt, wenn beide Zustände aus denselben Pixeln
entstehen.

**Drei Bilder statt sechs.**

---

## Regeln (gelten für alle drei Positionen)

- **Ein Bild pro Anfrage.** Keine Raster, keine Vergleichstafeln, keine Beschriftungen.
- **Kein Text im Bild.**
- **Gleiche Welt wie die Beilagen:** Nacht, Nussbaum und dunkle Eiche, Messing, warmes
  Lampenlicht gegen kaltes Mondblau, gemalter Konzeptkunst-Stil, gleicher Schwarzpunkt.
- **Freistellung = flächiges Magenta (#FF00FF)**, kein Alpha, kein Schatten, keine Vignette.
- **Master-Format**, keine gerundeten Ecken, kein Rahmen.

**Beilage für alle drei:** der heutige Archiv-Plate
(`site/static/media/scenes/archive-display.avif`, als PNG exportiert). Er ist die verbindliche
Vorlage für Architektur, Kamera, Licht und Türposition.

---

## P7 · Archiv-Wand mit offener Türlaibung · quer 16:9

**Datei:** `docs/P7_archiv_wand_laibung_16x9.png`

> Beigefügtes Bild ist die verbindliche Vorlage. Erzeuge **denselben Raum, denselben
> Kamerastandpunkt, dasselbe Licht** — ein nächtliches Archiv in dunkler Eiche und Nussbaum mit
> Registerschränken, Karteikästen, Protokollbänden und einer Leiter, warmes Lampenlicht gegen
> kaltes Mondblau von links, gemalter Konzeptkunst-Stil. Zwei Änderungen:
>
> **1. Die beiden unteren Ecken werden geräumt.** Die niedrigen Anrichten mit Messingleuchte
> und aufgeschlagenem Buch im linken und rechten Vordergrund entfallen ersatzlos. An ihrer
> Stelle: durchlaufende Wandvertäfelung mit Sockelleiste und Steinboden, so ruhig wie möglich.
> Das **untere Bilddrittel bleibt links und rechts leer** — dort steht später Möbel, das
> hereinfährt. Die Regale und Registerschränke **darüber** bleiben und rahmen weiter.
>
> **2. Die Türflügel fehlen.** Wo in der Vorlage die zweiflügelige Tür steht, ist die Öffnung
> **flächig magenta (#FF00FF)** ausgefüllt — eine saubere, harte Kante, kein Verlauf, kein
> Schimmer, keine Andeutung eines dahinterliegenden Raums. **Türrahmen, Laibung, Sturz mit
> Bekrönung, die beiden Wandleuchten links und rechts und die Schwelle am Boden bleiben
> vollständig erhalten** und sind so gemalt, dass die Laibung als **kurzer Tunnel** liest: die
> seitlichen Wangen leicht angeschnitten sichtbar, der Sturzschatten fällt in die Öffnung.
>
> Die magentafarbene Öffnung liegt bei **43 % bis 54,5 % der Bildbreite** und **19,5 % bis
> 62,5 % der Bildhöhe** — wie in der Vorlage. Die Bildmitte davor bleibt frei.
>
> 16:9 quer, kein Text, kein Rahmen.

**Abnahme:** Ecken leer · Öffnung sauber magenta ohne Verlauf · Laibung/Sturz/Schwelle stehen ·
Türzone innerhalb ±1 % der Vorgabe.

---

## P8 · Türflügel, freigestellt · quer

**Datei:** `docs/P8_archiv_tuerfluegel_magenta.png`

> Eine **zweiflügelige Tür, geschlossen**, aus dunkler, schwerer Eiche mit Nussbaumfüllungen,
> Messingbeschlägen und zwei langen Messinggriffen in der Mitte — dieselbe Tür wie im
> beigefügten Bild, dieselbe Schnitzerei in den Kassetten, dieselbe Alterung, dasselbe warme
> Streiflicht von links oben.
>
> **Nur die beiden Türblätter**, frontal, ohne Perspektivverzerrung. **Kein Rahmen, keine
> Laibung, kein Sturz, keine Wand, kein Boden, kein Schatten, keine Umgebung** — alles außerhalb
> der Türblätter ist **flächiges Magenta (#FF00FF)**.
>
> Die Türblätter füllen das Bild vollständig aus: Oberkante, Unterkante und beide Außenkanten
> berühren den Bildrand. Seitenverhältnis der Türfläche **etwa 1 : 1,9** (breit zu hoch).
>
> Kein Text.

**Abnahme:** exakt zwei Flügel · Trennfuge mittig · Magenta sauber bis an die Kante · Lichtrichtung
wie die Vorlage.

**Hinweis:** Kleine Maßabweichungen sind unkritisch — die Flügel werden beim Einbau auf die
Öffnung aus P7 skaliert.

---

## P9 · Archiv-Plate hoch · 2:3

**Datei:** `docs/P9_archiv_hoch_2x3.png`

> Derselbe Raum wie im beigefügten Bild als **Hochformat-Komposition** — nicht als Beschnitt,
> sondern als eigene Ansicht: die zweiflügelige Tür etwa mittig, Registerschränke und
> Bücherwände rahmen links und rechts, ein vertikaler Streifen in der Bildmitte bleibt frei.
> Die Tür ist hier **geschlossen und gemalt** (keine Freistellung, kein Magenta).
>
> **Die unteren Bildecken bleiben leer** — durchlaufende Vertäfelung, Sockelleiste, Steinboden,
> keine Anrichten, keine Leuchten, keine Karteikästen im Vordergrund.
>
> Nacht, dunkle Eiche und Nussbaum, Messing, warmes Lampenlicht gegen kaltes Mondblau, gemalter
> Konzeptkunst-Stil, gleicher Schwarzpunkt wie die Vorlage. 2:3 hoch, kein Text, kein Rahmen.

**Abnahme:** untere Ecken leer · Mittelstreifen frei · gleiche Welt wie P7.

---

## Was danach passiert (kein Bestellumfang — zur Einordnung)

1. Keying von P8 (Magenta → Alpha, v5-Kette), P7 bekommt die Öffnung als Alpha-Loch.
2. Der **geschlossene** Archiv-Plate entsteht als Komposit P7 + P8 → ersetzt
   `scenes/archive-display.avif`.
3. Der **offene** Zustand braucht kein eigenes Bild mehr: P7 mit dem Zielraum-Plate dahinter.
4. Trägt die Zerlegung, wird für **Study und Council dieselbe Bestellung** aufgegeben (je P7/P8).
   Erst dann ist der echte Durchgang in allen drei Räumen möglich.

**Bis dahin bleibt die Blende in Study und Council unverändert in Betrieb.**
