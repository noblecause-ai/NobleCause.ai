# Codex-Serie 4 — Fensterblick als eigene Ebene (Study)

**Von:** Opus 5 (Architekt) · **Datum:** 2026-07-24
**Anlass:** Phase 0 (Ruhebild-Parallaxe) ist gebaut, gemessen und **wirkungslos** — nicht
falsch eingestellt, sondern konstruktiv verdeckt. Diese Serie beschafft die eine Ebene, die
fehlt, damit Tiefe im Ruhebild überhaupt lesbar werden kann.
**Bestelldisziplin:** analog `docs/codex-serie-2-council.md` (gleiche Welt, gleiches Licht,
Cutout mit Alpha, Plate ohne einfahrende Elemente).

---

## 1 · Der Befund, der die Bestellung auslöst

Parallaxe liest nur gegen eine **stehende Referenz**. Die Study hat genau eine Blende — das
Mondfenster. Deren Inhalt ist aber die einzige Ebene, die überhaupt unabhängig existiert,
und sie ist gleichzeitig der schlechteste Träger:

- `opacity: 0.5`, `mix-blend-mode: screen` → kontrastarm
- **schon in Eigenbewegung:** `.drift-x` ±12 % der Ebenenbreite, `.drift-y` ±6 % der Höhe →
  bei 241 × 446 px sind das **±29 px / ±27 px**
- der Parallaxe-Versatz aus Phase 0 beträgt gemessen **3,00 px / 1,80 px volle Spanne** →
  Verhältnis **1 : 19**. Unsichtbar durch Überdeckung, nicht durch Feinjustierung.

Alle anderen Kandidaten fallen aus einem gemeinsamen Grund weg: Scout und Warden haben
**gebackenen Bodenkontakt und eigene Lichtpfützen** (Schreibtischlampen). Bewegt man die
Figuren, rutschen sie über die gemalte Diele; bewegt man statt dessen die Wand, rutscht die
Diele unter den Figuren weg. Derselbe Fehler mit umgekehrtem Vorzeichen.

Der richtige Träger wäre der **Mond**: harte Kante, hoher Kontrast, hinter feststehenden
Fenstersprossen. Er ist im Plate gebacken und deshalb heute nicht bewegbar.

## 2 · Was bestellt wird — zwei Assets

**Asset A — „Blick nach draußen"**
Nachthimmel mit Mond und Wolken, wie er durch das Study-Fenster zu sehen ist.
- **Ohne** Fensterrahmen, **ohne** Sprossen, **ohne** Glasreflexe — nur der Außenraum.
- **Mindestens 1,5× die Fensteröffnung in beiden Achsen.** Er wird verschoben; überall dort,
  wo er zu klein ist, liegt am Rand ein Loch. Bildwichtiges (der Mond) gehört in die mittleren
  60 %, nie an den Rand.
- Gleiche Nacht, gleiche Farbtemperatur, gleiche Mondposition wie im heutigen Plate — er soll
  in Ruhelage deckungsgleich wirken.
- Deckend (kein Alpha nötig), Querformat.

**Asset B — „Fenstersprossen + Rahmen"**
Nur das Gitter und der innere Rahmen des Fensters, **transparenter Grund (Alpha)**.
- Exakt die Geometrie des Fensters im heutigen Plate — es wird deckungsgleich darüber gelegt.
- Mit Glasreflex und Lichtabfall der Vorlage, damit der Übergang nicht flach wirkt.
- Alpha-Kanal echt; Chroma-Grün nur als Fallback (Präzedenz: der Magenta-Key-Unfall bei den
  Akteur-Cutouts, siehe Fußlinien-Messung in Paket 1 — der ausgelieferte Wert wich vom Master
  ab und musste am gerenderten AVIF nachgemessen werden).

## 3 · Warum diese Zerlegung und nicht ein Alpha-Loch im Plate

Naheliegend wäre: Plate mit ausgeschnittener Glasfläche, Himmel dahinter. Das verlangt vom
Generator einen **feinen Alpha-Schnitt um jede Scheibe** — fehleranfällig, und ein 1-px-Fehler
am Sprossenrand ist in jeder Fassung sichtbar. Die Zerlegung A + B kehrt das um: das Plate
bleibt **unverändert**, die beiden neuen Ebenen liegen darüber, und der Alpha-Schnitt fällt
auf ein kleines, geometrisch einfaches Gitter (B) statt auf ein Vollbild.

Nebeneffekt: Das heutige Plate bleibt der Fallback. Ohne Zeiger, ohne JS und bei
Reduced-Motion können A und B ungemountet bleiben — dann ist das Bild exakt das heutige.

## 4 · Wie es danach verbaut wird (für CC, nach Lieferung)

Reihenfolge im Stapel, alle als Ebenen der fixen Bühne (dasselbe Muster wie `.clouds`):

```
Plate (unverändert)  →  A: Himmel (verschiebbar)  →  B: Sprossen (fest)  →  Akteure  →  DOM
```

- **A** hängt an `--px`/`--py` mit **±6 bis 10 px** (Startwert ±8 px, Y ~60 % von X). Das ist
  die Amplitude, bei der Aperturparallaxe liest — sie darf hier so groß sein, weil die
  Referenz (B) hart und feststehend ist.
- **B** bewegt sich nie.
- **Die Fenstergeometrie wird wie der Tür-Hotspot hergeleitet** — aus derselben
  `object-fit: cover`-Mathematik, zwei Aspect-Ratio-Zweige (`StudyRoom.svelte`, ~Z. 256–275).
  Beide Zweige einzeln nachweisen, nicht einen analytisch aus dem anderen ableiten.
- **Der Wolken-Eigendrift zieht auf A um** (oder entfällt). Bleibt er auf einer separaten
  Ebene, kehrt genau das Überdeckungsproblem aus §1 zurück.
- Der Parallaxe-Listener aus Phase 0 (`stage.js`, `installParallax`) ist korrekt gebaut und
  wird **unverändert wiederverwendet** — rAF-gedrosselt, nur bei `pointer: fine` und
  ohne Reduced-Motion, weiches Ausklingen beim Verlassen des Fensters.

**Abnahme:** Ruhelage pixelgleich mit heute · bei Zeiger am Anschlag kein Loch am Rand von A ·
B sitzt deckungsgleich auf dem gemalten Fenster in **beiden** Aspect-Ratio-Zweigen · kein
Layout-Thrash · Reduced-Motion/No-JS/Touch = heutiges Bild.

## 5 · Was diese Serie NICHT ist

Nicht die Portal-Serie. Der Durchflug braucht weiterhin die Assets aus §A6 des
Review-Dokuments (Wand-Plate mit Alpha-Türöffnung, Türblatt-Cutout, Laibung, hochauflösendes
Zielraum-Plate). Die beiden Bestellungen sind unabhängig und können parallel laufen — Serie 4
wirkt im Ruhebild, §A6 im Übergang.
