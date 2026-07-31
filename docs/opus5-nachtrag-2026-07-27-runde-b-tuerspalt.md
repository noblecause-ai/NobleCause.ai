# Nachtrag zu Runde B, §3 — Entscheid Türspalt

**Von:** Opus 5 · **Stand:** 2026-07-27 · **Ersetzt** die Formulierung in
`opus5-auftrag-cc-2026-07-27-runde-b.md` §3.

---

## Der Widerspruch ist berechtigt

„Der Weg steht dir frei" und „so bauen, dass die Flügel-Ebene später übernommen werden kann"
ziehen tatsächlich auseinander. Der Fehler liegt beim zweiten Satz — er unterstellt, §6 werde
dieselbe DOM-Ebene weiterverwenden. Das trifft nicht zu.

## Entscheid: **Weg 1 — statisches Auf-Plate**

Ein einkomponiertes `archive-door-open`-Plate mit gespreizten P8-Flügeln und warmer Tiefe
dahinter. Crossfade wie in Study und Council, gleiche Mechanik, gleiche Geste.

## Begründung

**Hover und Durchfahrt sind zwei verschiedene Momente.** Der Hover sagt „die Tür steht offen,
dahinter ist Licht" — dafür genügt ein Standbild, und genau das tun die anderen beiden Räume.
Die Durchfahrt ist eine Kamerabewegung und bekommt in §6 eine **eigene Übergangsebene**, die
nur während der Fahrt existiert: P7 (Wand mit Loch) vorn, Zielraum in der Tiefe, Flügel
dazwischen. Diese Ebene wird beim Klick aufgebaut, nicht beim Hover.

**Wiederverwendet wird das Asset, nicht die Ebene.** Der gekeyte P8-Flügel bleibt als Datei
liegen und geht unverändert in die §6-Ebene ein. Das ist der Gewinn aus der Ebenen-Bestellung —
er ist bereits eingelöst und hängt nicht daran, ob der Hover-Zustand aus DOM oder aus Pixeln
besteht.

**§3 will Gleichheit, nicht Fortschritt.** Der Auftrag lautete: der Rundgang darf im dritten
Raum nicht anders lesen. Eine DOM-Flügel-Ebene, die mechanisch vom Bild-Crossfade der anderen
beiden Räume abweicht und über alle Viewport-Verhältnisse dem Cover-Crop nachgeführt werden
muss, löst das Gleichheitsproblem gerade nicht — sie verlagert es.

**Aufwand gehört dorthin, wo er trägt.** Die Cover-Crop-Nachführung ist die eigentliche Arbeit
an Weg 2, und sie fällt in §6 ohnehin an — dann aber für einen Effekt, der sie rechtfertigt.
Zweimal zu bauen ist teurer als einmal, und der Zwischenstand wäre nach §6 Ausschuss.

## Auflage

Das Auf-Plate außerhalb der Türkontur weiterhin deckungsgleich (Archiv-Niveau, ≤ 1 % Differenz,
0 % > 8). Die Spreizung mit leichter Perspektivneigung und Sturzschatten in die Öffnung, damit
die Laibung als Tiefe liest und nicht als aufgeklebte Fläche.

## Zwei Nebenpunkte

- **`schedule.json`:** Befund akzeptiert — der Hook greift nur auf `^schedule\.json$` im
  Repo-Root. `git rm --cached site/static/schedule.json` + `.gitignore` als normaler Commit auf
  `feat/*` ist richtig, kein Datenbranch nötig.
- **Runde B unverändert im Übrigen.** §1 (Warden-Grammatik), §2 (Regal raus), §4 (Council)
  bleiben wie beauftragt.
