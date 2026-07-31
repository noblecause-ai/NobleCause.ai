# Phase 0 — Ruhebild-Parallaxe (Bauauftrag)

**Von:** Opus 5 (Architekt/Review) · **Für:** CC (Bau) · **Datum:** 2026-07-24
**Voraussetzung:** Paket 1 (Akteur-Fix) und Paket 2 (Tür-Gegenprobe) sind committet.
**Steward-Entscheid:** Gegenprobe bleibt der Übergang; Phase 0 kommt als Ruhebild-Tiefe dazu.
Phase 1 (echter Durchflug) bleibt nach dem Go-Live, weil sie an der Codex-Serie hängt.

---

## §0 · Revision meiner eigenen Empfehlung

In `opus5-review-raumuebergang-2026-07-24.md` §A3 habe ich Phase 0 als
„`perspective` + `translateZ` auf den vorhandenen `<img>`" beschrieben. **Das nehme ich
zurück.** Nach Paket 1 ist es der falsche Weg, aus zwei Gründen:

1. **`perspective` auf einem Vorfahren bricht `position: fixed`** (§A5). Seit Paket 1 hängt
   die *gesamte* Bühne daran. Ein gemeinsamer 3D-Container würde bedeuten, alle Ebenen von
   `fixed` auf `absolute` umzubauen — also genau den Fix rückgängig zu machen, den wir
   gerade nachgewiesen haben.
2. **Echte Perspektive skaliert die Ebenen** (ein Element bei `translateZ(-d)` erscheint um
   `p/(p+d)` kleiner und muss gegenskaliert werden). Jede Skalierung des Plates **verschiebt
   den `object-fit: cover`-Ausschnitt** — und daraus ist die Tür-Hotspot-Geometrie in
   `StudyRoom.svelte` hergeleitet. Wir würden die Türkoordinaten verschieben, an denen
   Paket 2 hängt.

**Echte Perspektive braucht man erst, wenn die Kamera durch die Szene fährt** — also in
Phase 1. Für das Ruhebild leistet **differenzielle Translation** dasselbe fürs Auge, ohne
einen der beiden Fallstricke. Das ist Phase 0.

## §1 · Was gebaut wird

Ein **Pointer-getriebener Tiefen-Versatz**: Bewegt sich der Zeiger, verschieben sich die
Bildebenen unterschiedlich weit. Nähere Ebenen weiter, fernere weniger. Kein neuer
Renderer, keine Dependency, keine Strukturänderung — nur eine zusätzliche Transform-
Komponente auf Ebenen, die **bereits** `position: fixed` sind.

**Kein `perspective`, kein `translateZ`, kein neuer Wrapper.** Wer später Phase 1 baut,
findet diese Ebene unverändert vor und ersetzt sie dort, wo die Kamera wirklich fährt.

## §2 · Mechanik

Ein Listener schreibt zwei normalisierte Werte auf `:root`:

```js
// --px / --py: -1 .. +1, Zeigerposition relativ zur Viewportmitte.
// rAF-gedrosselt, passive, nur eine Schreiboperation pro Frame.
// Nur montiert bei: pointer:fine (kein Touch) UND no-preference (Reduced-Motion aus).
```

Jede Ebene bekommt ihren eigenen Faktor. Die Transform-Komponente wird **an die vorhandene
angehängt**, nicht ersetzt — die `--retreat`-Scrub-Mechanik bleibt unangetastet:

```css
.rail {
  transform:
    translateX(calc(var(--retreat, 0) * var(--side, 1) * 13vw))   /* Bestand */
    translate(calc(var(--px, 0) * var(--depth-x)), calc(var(--py, 0) * var(--depth-y)));
}
```

**Tiefenstaffelung Study** (Startwerte, vom Auge nachzujustieren):

| Ebene | Verhältnis | Amplitude Start (Desktop) |
|---|---|---|
| Wolken (durchs Fenster, am fernsten) | am wenigsten | ±1,5 px |
| Plate / Wand (Referenz) | wenig | ±4 px |
| Tür-Hotspot-Ebene | **identisch zum Plate** | ±4 px |
| Akteure (Scout/Warden, am nächsten) | am meisten | ±14 px |

Die Y-Amplitude durchweg ~60 % der X-Amplitude (Zeiger bewegt sich horizontal mehr).

## §3 · Zwei harte Regeln

**R1 — Der Tür-Hotspot bewegt sich exakt wie das Plate.** Dieselbe Variable, derselbe
Faktor. Sonst driftet die Klickfläche von der gemalten Tür weg. Der Portal-Blende schadet
das nicht: `--door-*` wird beim Klick aus `getBoundingClientRect()` gelesen und enthält den
Transform bereits — die Geometrie korrigiert sich selbst, **solange R1 gilt**.

**R2 — Das Plate darf keine Kante freilegen.** Bei ±4 px Versatz kann am Rand ein Streifen
Hintergrund erscheinen. Falls sichtbar: **konstantes** `scale(1.015)` auf das Plate — und
dann **zwingend dieselbe Skalierung auf die Hotspot-Ebene** (R1 gilt für Skalierung genauso,
sonst verschiebt sich der Cover-Ausschnitt gegen den Hotspot). Kein animiertes Skalieren.

## §4 · Degradation (zuerst bauen, nicht zuletzt)

Der Listener wird **nicht montiert** bei: `prefers-reduced-motion: reduce` · `pointer:coarse`
(Touch) · kein JS. Dann bleiben `--px`/`--py` ungesetzt, die `var(…, 0)`-Fallbacks greifen,
und die Transform-Komponente ist die Identität — **das Bild ist pixelgleich mit heute.**
Das ist die erste Prüfung, nicht die letzte.

Mobil bekommt bewusst nichts: es gibt dort keinen Zeiger, und der Tür-Hotspot existiert
ohnehin erst ab 1200 px.

## §5 · Abnahme

1. **Degradation zuerst:** Reduced-Motion und No-JS liefern exakt das heutige Bild
   (Screenshot-Vergleich, nicht Augenmaß).
2. **Regression Paket 1:** 700 px durchscrollen bei 1440 und 390 — Akteure bewegen sich
   weiterhin 0 px vertikal. Die Parallaxe darf die fixe Bühne nicht wieder lösen.
3. **Regression Paket 2 (der eigentliche Kopplungstest):** Zeiger in eine Ecke bewegen, so
   dass die Parallaxe am Anschlag steht, **dann** die Tür klicken. Die Blende muss weiterhin
   auf der gemalten Tür sitzen, nicht daneben. Frame bei ~12 ms einfrieren.
4. **Kein Layout-Thrash:** Während der Zeigerbewegung nur Compositing — kein Layout/Paint in
   den DevTools-Performance-Frames. Eine Schreiboperation pro rAF, nicht pro `pointermove`.
5. `npm run build` warnungsfrei, Testsuite grün, Preview neu gestartet.
6. **Urteil des Stewards:** Trägt die Tiefe? Amplituden sind Stellschrauben — lieber zu
   dezent starten und hochdrehen als umgekehrt.

## §6 · Was Phase 0 NICHT ist

Kein Durchflug, keine Verdeckung zwischen Ebenen, keine Tiefenschärfe. Wenn das Ruhebild
trägt, ist die Frage für Phase 1 nur noch: reicht die Blende für den Wechsel, oder muss die
Kamera wirklich fahren. Die Antwort darauf kostet die Codex-Serie aus §A6 des Review-
Dokuments — nicht vorher bestellen.
