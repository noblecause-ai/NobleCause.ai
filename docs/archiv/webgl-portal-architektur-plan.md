> **Archiviert 2026-07-28 (CC) — WebGL/Three.js-Entscheid (2026-07-24) später verworfen; Türdurchgang in CSS-3D gebaut (Runde C).** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# WebGL-Portal — Architektur-Plan (Entscheidung: Three.js)

**Steward-Entscheid 2026-07-24:** Der „durch die Tür"-Übergang wird mit **WebGL/Three.js**
gebaut (echte Tiefe wie die MotionSites-Vorlage), **nicht** als 2D-Zoom.
**Für:** CC (Umsetzung), zur Freigabe durch den Steward, bevor gebaut wird.

## 0 · Leitprinzip (nicht verhandelbar)
WebGL ist eine **reine Enhancement-Ebene ÜBER dem fertigen 2D-Boden.** Der heutige
Zustand — No-JS, reduced-motion, schwaches Gerät, kein WebGL — **bleibt exakt die 2D-Site
von jetzt.** §0 (die Seite ist vollständig, bevor das Spiel beginnt) behält Verfassungsrang.
Wir holen den Wow-Effekt, ohne den Boden zu opfern. Der Canvas wird nur auf fähigen
Geräten **nach dem ersten Paint** lazy dazugeladen.

## 1 · Was WebGL rendert — und was NICHT
- **Canvas = nur Kulisse/Atmosphäre:** die Raum-Ebenen als 2.5D-Planes mit Parallaxe und
  der Tür-Durchflug. Reine Optik.
- **Inhalt bleibt DOM:** Ergebnis-Tafel, Texte, Spendenlinks, Türlinks — alles liegt über
  dem Canvas, klickbar und zugänglich. Der Canvas trägt nie Inhalt (§0), er ist die
  bewegte Leinwand dahinter.
- **Asset-Reuse:** Plate (Hintergrund), Tür(-Crop), Akteur-Cutouts, Wolke sind **exakt die
  Depth-Layer** der 2.5D-Szene. Kein neues Kunstkonzept — nur andere Z-Anordnung.

## 2 · Die Portal-Technik (der Kern)
**2.5D-Layered-Dolly:**
- Die Ebenen des aktuellen Raums liegen auf verschiedenen Z: Wand/Plate hinten · Tür in der
  Mitte · Akteure vorn · Wolke im Fensterausschnitt. Kamera in Ruhe = die **heutige
  Komposition** (der Canvas sieht im Stand aus wie das 2D-Bild).
- **Pointer/Scroll → Parallaxe:** leichte Kameraversätze erzeugen Tiefe zwischen den Layern.
- **Tür-Klick → Dolly:** die Kamera fährt in die **Türmitte** hinein; hinter der Tür-Plane
  liegt das **Plate des Zielraums** (tiefer in Z). Die Tür wächst, der Zielraum füllt das
  Bild; an der Schwelle → echte Navigation (URL/DOM wechselt darunter, VT optional).
- **Phase-2-Option:** echter Stencil-Portal (Zielraum nur innerhalb der Türkontur
  gerendert) — nur falls der Dolly nicht überzeugt.

## 3 · Degradation (hart, zuerst bauen)
Vor dem Mount Feature-Detection. Canvas wird **nicht** gemountet bei:
kein WebGL · `prefers-reduced-motion: reduce` · `navigator.connection.saveData` · kein JS.
Dann steht die heutige 2D-CSS-Site als voller Zustand. Die Degradation ist die **erste**
Akzeptanzprüfung, nicht die letzte.

## 4 · Bibliothek & Bundle
- `three` als dependency; das WebGL-Modul in einem **eigenen lazy-Chunk** (dynamic
  `import()` in `onMount`, nach dem 2D-Paint). **Kein three im initialen Bundle** — die
  30-Sekunden-Regel und der erste Eindruck hängen nie an der 3D-Ebene.
- Nur `transform`/Shader auf der GPU; kein Layout-Thrash im DOM.

## 5 · Phasen (Risiko gestaffelt, Study zuerst)
- **Phase 0 — Spike (Study):** Canvas über dem Study-Hero, die 4 Ebenen als Planes,
  Ruhebild deckungsgleich mit dem heutigen 2D-Bild, Pointer-Parallaxe. Beweist
  Enhancement + Degradation. **Noch kein Portal.** Abnahme: sieht im Stand identisch aus,
  degradiert sauber, kostet nichts vor First Paint.
- **Phase 1 — Portal Study→Council:** Dolly durch die Tür in das Council-Plate. Der eine
  Wow-Moment. Abnahme gegen die Vorlage.
- **Phase 2 — Ausrollen:** Council/Archive, Feinschliff, evtl. Stencil.

## 6 · Asset-Konsequenz (wichtig für Phase 1)
Für echte Tiefe muss der **Hintergrund-Plate ohne die separat gelagerten Vorderelemente**
vorliegen (Tür/Akteure liegen als eigene Planes davor) — sonst doppeln sie sich. Und
**hinter der Tür-Plane braucht der Hintergrund Inhalt** (kein Loch), wenn die Tür als
eigene Ebene davorsteht. Study: Akteure sind schon separat, Tür-Crop existiert. Zu prüfen:
ob der Plate-Hintergrund hinter der Tür „gefüllt" genug ist oder ein minimaler Nachzug
nötig wird. Für Phase 0 (nur Parallaxe) genügt das heutige Material.

## 7 · Risiken, ehrlich
- **Größter Aufwand des Projekts** — Three.js-Szene, Kamera, Layer-Kalibrierung je Raum.
  Deshalb Study-Spike zuerst: beweisen, bevor wir ausrollen.
- reduced-motion muss den Canvas **komplett** abschalten, nicht nur dämpfen.
- Der Canvas darf die DOM-Interaktion nie blockieren (pointer-events, Fokusreihenfolge).
- Perf auf Mittelklasse-Mobil: notfalls Mobil = 2D-Boden (Canvas nur Desktop), als
  konservativer Startpunkt.

## 8 · Was CC zuerst tut
Phase 0 als isolierter Spike, hinter Feature-Flag, **ohne** den bestehenden 2D-Pfad zu
verändern (der bleibt der Fallback). Erst wenn Phase 0 abgenommen ist, Phase 1.
