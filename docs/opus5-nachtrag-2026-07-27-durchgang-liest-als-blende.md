# Nachtrag §6 — die Fahrt liest als Blende. Warum, und was zu ändern ist

**Von:** Opus 5 · **Stand:** 2026-07-27 · **Anlass:** Steward-Befund am Live-Blick:
„kein Durchgang durch die Tür, nur eine schnellere Blende."

**Der Bau ist nicht falsch.** Geometrie, Handoff und Flow sind bewiesen und bleiben. Was fehlt,
sind die **drei Größen, die aus einer Skalierung eine Fahrt machen.** Alle drei sind
Parameter, keine Umbauten.

---

## Ursache 1 (die wichtigste) · Die Wand fliegt nie am Betrachter vorbei

Eine Ebene passiert die Kamera genau dann, wenn der Kamerawagen die Strecke **`perspective`**
zurückgelegt hat. Steht `perspective` auf oder über der Fahrtstrecke von 1400, dann passiert die
Archiv-Wand den Betrachter **nie** — sie wird nur größer und wird am Ende weggeblendet.

**Größer werden ist Zoom. Vorbeiziehen ist Fahrt.** Das ist der ganze Unterschied, und er
erklärt den Befund vollständig.

**Änderung:** `perspective` auf **≈ 0,6 × Fahrtstrecke** (Richtwert **850** bei Strecke 1400).
Dann passiert die Wand bei ≈ 60 % der Fahrt den Betrachter, ihre Apertur ist zu diesem Zeitpunkt
längst über den Bildrand hinausgewachsen — und die **letzten 40 % der Fahrt sind reiner
Zielraum, der auf Cover 1,0 zuläuft.** Genau dieser Schwanz ist das Gefühl von „ich bin
hindurch".

Damit der Zielraum weiterhin exakt auf Cover 1,0 endet, ist seine Tiefe an das neue
`perspective` anzupassen — die harte Anforderung aus §6.3 bleibt unangetastet.

Die Wand in ihren letzten ≈ 15 % ausblenden **und** Blur hochziehen, während sie riesig am Rand
vorbeizieht. Sie ist dort nur noch Textur; scharf gezeichnet wird sie zum Fehler.

---

## Ursache 2 · Die Kamera zielt nicht auf die Tür

Steht `perspective-origin` auf `50% 50%`, fliegt die Kamera durch die **Bildmitte**. Die
Archiv-Tür sitzt aber bei **x ≈ 48,8 %, y ≈ 41 %** — deutlich über der Mitte. Die Wand teilt
sich dann nicht um die Öffnung, sondern schiebt sich schräg daran vorbei; die Öffnung wandert
während der Fahrt aus. Das liest als Zoom mit Drift, nicht als Durchtritt.

**Änderung:** `perspective-origin` auf den **gemessenen Mittelpunkt der Apertur** setzen —
Richtwert `48,8% 41%`, am gerenderten Plate nachmessen, nicht am Master.

---

## Ursache 3 · Der Auftakt ist wörtlich eine Blende

Der Start ist derzeit ein Dissolve von der geschlossenen Wand auf die Wand-mit-Loch. Das ist
eine Überblendung am Anfang einer Bewegung, die keine sein soll — und sie prägt den Eindruck,
weil sie das Erste ist, was man sieht.

**Änderung, sofort und billig:** Dissolve auf **≤ 100 ms** kürzen und **vollständig unter die
anlaufende Fahrt legen**, nicht davor. Der Wechsel darf nicht als eigener Schlag lesen.

**Änderung, richtig:** die gespreizten Flügel aus dem §3-Auf-Plate. Die geteilten Assets
(`door-leaf-left/right.avif`) liegen bereit. Das war ohnehin als Upgrade vorgesehen — es wird
jetzt Teil dieser Runde, weil der Auftakt den Gesamteindruck trägt.

---

## Zusatz, falls es danach noch flach bleibt

Erst umsetzen, wenn 1–3 sitzen — sonst ist nicht mehr unterscheidbar, was gewirkt hat:

- **Fahrtkurve:** spät beschleunigend, **nicht** ausklingend (`cubic-bezier(.5,0,.75,.4)`).
  Eine Kamera, die vor der Tür abbremst, liest wie ein Fehler.
- **Dauer:** 1,25 s ist eher kurz für eine Fahrt mit Schwanz. **1,5–1,6 s** probieren.
- **Türflügel bleiben stehen, während die Wand vorbeizieht** — sie sitzen 200 näher und müssen
  die Wand sichtbar früher verlassen. Wenn sie mit ihr gemeinsam verschwinden, fehlt die zweite
  Tiefenstufe und die Szene wirkt zweischichtig.
- **Schwellen-Bloom** im Moment des Durchtritts (0,9–1,25 s der alten Skala) — kaschiert, dass
  die ferne Ebene ein flaches Bild aus geringer Distanz ist.

---

## Abnahme — messbar, nicht nach Gefühl

Der Test, der „Fahrt" von „Blende" trennt, ist eine Frame-Reihe bei 0 / 25 / 50 / 65 / 80 / 100 %:

1. **Bei ≈ 65 %:** die Archiv-Wand ist **aus dem Bild** — keine Kante, kein Möbel, keine Regale
   mehr sichtbar. Nur noch Zielraum.
2. **Von 65 bis 100 %:** ausschließlich der Zielraum, der auf Cover 1,0 zuläuft. Diese Phase
   muss **existieren und sichtbar sein.**
3. **Über die ganze Fahrt:** die Apertur wächst **erkennbar schneller** als der Zielraum
   dahinter. Verhältnis der Wachstumsraten im Bericht nennen — das ist die Parallaxe, und ohne
   sie gibt es keinen Tiefeneindruck.
4. Handoff-Deckungsgleichheit unverändert bewiesen (§6.3).
5. `perspective-origin` liegt auf dem gemessenen Aperturmittelpunkt (Wert nennen).

**Punkt 1 und 2 sind der eigentliche Befund.** Wenn die Wand bis zum Schluss im Bild bleibt, ist
es eine Blende — egal wie gut alles andere gebaut ist.

---

## Commit

Der Commit-Umfang aus deinem Bericht (`door-passage.js`, `room-transitions.js`,
`(rooms)/+layout.svelte`) bleibt und wird gesetzt, **sobald die Fahrt live sitzt** — nicht
vorher. Guard mit, kein Push, Medien untracked.
