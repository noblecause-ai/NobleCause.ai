> **Archiviert 2026-07-28 (CC) — überholter --SKIP-Bühnenspiel-Entwurf, nie Teil der Baseline.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

> **SKIP — Kimi-eigener Entwurf für ein künftiges Konzept.**
> Diese Datei ist NICHT Teil der Übergabe-Baseline (`docs/handover-baseline.md`).
> Für den Drei-Wege-Vergleich: überspringen — sie enthält einen Lösungsweg, keinen Ist-Zustand.
> Original: Phase-1-Plan vom 19.07.2026, unverändert kopiert.

# Bühnenspiel — Phase 1: Analyse, Vorschläge, Bildaufträge (noch nichts gebaut)

Rahmen: nur `site/` + `docs/`, Tabu-Pfade unberührt (`content.js`/`homepage.js` werden
nicht editiert), Datennaht/keine Re-Aggregation, No-JS-Vollwahrheit, A11y, DE+EN,
kein Commit. Dieser Plan enthält die verbindlichen Vorschläge + die präzisen
Bildaufträge. **Bau erst nach „los".**

## 1. Befund am Bestand (verifiziert)

- **Die drei docs-Bilder für die alte Mobil-Fassung taugen NICHT** (gesichtet):
  `20_35_45 (1)` = Study-Portrait (Figur eingezeichnet, keine Tür sichtbar),
  `20_35_45 (2)` = Council-Portrait (Zählmaschine mittig, keine Tür),
  `20_35_46 (3)` = Archiv-Portrait (Karteischrank, keine Tür). Alle drei haben
  **keine zentrierte Tür** und Figuren fest eingebrannt — für das Bühnenspiel
  unbrauchbar. Ebenso ungeeignet: `19_49_56`/`19_50_47` (Study-Landschaft mit
  Figuren, Tür am rechten Rand) und `21_44_02` (sehr dunkle Council-Luftansicht).
  → **Neue Kunst zwingend** (Aufträge in §7). Die sechs Dateien bleiben ungenutzt
  in `docs/` (Provenienz), kein Löschen.
- **Kein vorhandener Plate hat eine zentrierte Tür** — der aktuelle Hotspot liegt
  bei x 86–99 % (rechter Rand), deshalb nur ab Seitenverhältnis ≥2,1 sichtbar.
  Bestätigt den Ausgangsbefund: Randtür stirbt im Crop, Mitteltür überlebt jeden.
- **Erbbare Substanz:** fixe Bildebene + Scrim-Architektur (`RoomHero`, Layout),
  `ResultBoard` (fix ≥1200 px, im Fluss darunter — ist bereits „die Tafel links"),
  `FlowRail`-Texte/Embleme (Röhren-Inhalt liegt fertig in `t.study.flow`),
  `room-transitions.js` (VT-Maschinerie, `--vt-origin`, nav-dir, reduced-motion-
  Ausstieg), Tür-Karten (`Door.svelte`), i18n-Spiegel, 16 grüne Build-Tests.
- **Werkzeuge:** `sips` vorhanden (kein WebP — Derivate bleiben JPEG, wie bisher);
  CDP-Verifikationswerkzeuge in `/tmp` intakt.

## 2. Architektur des Bühnenspiels

Neue Komponente **`StageHero.svelte`** (ersetzt `RoomHero` in den drei Räumen) —
Ebenen-Stack im 100svh-Hero, alle Ebenen `position:absolute` über dem fixen Plate:

```
Ebene 0  Plate GESCHLOSSENE Tür (fix, object-fit:cover)      — immer da
Ebene 1  Plate OFFENE Tür (gleiche Datei-Familie, absolut,   — hover/focus/ride
         clip-path um die Türöffnung, opacity 0 → 1)
Ebene 2  TÜRBLATT als eigene animierbare Ebene = der Link    — rotateY am Ansatz
Ebene 3  Akteure/Zweite Ebene (Slide-in auf Schienen)        — raumspezifisch
Ebene 4  Ergebnis-Tafel (ResultBoard, unverändert)           — Sequenz-Schritt 3
Ebene 5  Prozess-Röhre (neu: StageTube.svelte)               — unten im Hero
Ebene 6  Plakette (eyebrow/h1/lead, wie bisher)              — Sequenz-Schritt 4
```

**Eintritts-Sequenz (CSS-Animationen, verzögert gestaffelt, ~2,4 s gesamt):**
1. Plate (sofort) → 2. zweite Ebene fährt ein (Study: Scout von links, Warden von
   rechts; ~0,7 s, ease-out) → 3. Tafel blendet ein → 4. Plakette blendet auf →
   5. Röhren-Kugeln laufen von rechts ein (gestaffelt, mit Pfeil).
Muster: **Default = alles sichtbar** (No-JS-Boden); JS setzt beim Mount die Klasse
`stage-armed`, die die Ausgangszustände erst versteckt und die Animationen startet.
Kein Scroll-Trap, kein JS-Zwang.

**Vorschlag Tafel-Frage (Pflichtfeld „mit oder ohne sichtbare Tafel-Fläche"):**
**MIT.** Der neue Study-Plate bekommt links eine gemalte, leere Schiefertafel;
das `ResultBoard`-Panel liegt bei Sequenz-Schritt 3 als eigenes CSS-Panel darüber
(wie in K3 bewährt: nicht pixelgekettet, rem-basiert, ab 1200 px fix → „bleibt bis
zuletzt stabil" und „in jedem Raum immer sichtbar" ist damit identitätsstiftend
erfüllt: dieselbe Tafel in allen drei Räumen). Die gemalte Tafel ist Atmosphäre,
das Panel die Antwort — keine Doppelung des Inhalts.

**Lock / Unlock:** Der „Lock" ist rein visuell (Hero = 100svh). Scroll-Intent
(scrollY > ~48 px) setzt `.stage-unlocked` per Listener (beidseitig toggelnd):
Akteure/Zweite Ebene fahren ~30 % zurück Richtung Einfahrts-Seite, Röhre schiebt
zur Seite/unter den Textrand, Plakette legt sich ruhiger. **Scrollen WÄHREND des
Aufbaus (Definitionspflicht):** Scroll-Intent vor Sequenz-Ende springt alle laufenden
Animationen in ihren Endzustand (`stage-skip`: `animation-duration:0.01ms`) und
unlockt sofort — die Sequenz ist nicht abkürzbar per Knopf, aber niemand wird
gefangen; Geduldige sehen sie vollständig.

**Tür-Hover (gelockt):** Türblatt-Link bekommt `:hover`/`:focus-visible` →
`transform: perspective(900px) rotateY(-55deg)` (Ansatz links), darunter blendet
Ebene 1 (offener Plate mit gemaltem Durchblick in die nächste Szene) weich ein.
Im Council zeigt Ebene 1 den Archiv-Streifen (gemalt, s. Bildauftrag). Kein JS
nötig — reines CSS auf dem Link selbst.

**Türfahrt (Klick, mit VT-API + no-preference):** Drei Phasen, ~1,8 s gesamt:
1. Rückfahrt der Seitenelemente + Tafel-Fade (~300 ms, WAAPI im onNavigate-Hook),
2. Tür öffnet sich voll (`rotateY(-75deg)`) + Ebene 1 voll sichtbar (~350 ms),
3. `startViewTransition`: alte Seite skaliert ~2,6 mit `transform-origin` auf der
   Türmitte (≈ 50 % 45 % — zentrierte Tür macht `--vt-origin` hier überflüssig),
   neue Seite von 1,12 → 1 einblendend (~1,1 s). Fühlt sich an wie Hindurchgehen:
   Rückzug → Öffnen → Durchschreiten. Back-Navigation: dieselben Keyframes kürzer
   (1,2 s, Richtung umgekehrt). Ohne VT-API/reduced-motion: sofortiger Wechsel.

## 3. Vorschläge zu den Pflichtfragen

**(1) MOBIL — reduzierte eigene Fassung, kein geschrumpfter Desktop:**
- Portrait-Plates (2:3) mit zentrierter Tür; Ebene 2 (Akteure/Pulte) fährt mit
  ~40 % kürzerem Weg ein, dieselbe Reihenfolge, dieselben Zeiten (kürzer wirkt
  mobil hektisch).
- Tafel: im Hero NICHT überlagert — sie ist das erste Element im Fluss direkt
  unter dem Hero (K3-Verhalten, ein Scrollzug entfernt); die gemalte Tafel links
  trägt die Stimmung. Desktop trägt „immer sichtbar" wörtlich (fix), mobil trägt
  es „sofort griffbereit" — ehrliche Reduktion statt gequetschter Mini-Tafel.
- Röhre: eine Zeile Chips (Emblem + Kurzname, horizontal, umbrechend) — die
  Erklärungssätze leben mobil im FlowRail-Abschnitt unter dem Hero.
- Peek/Hover gibt es an Touch nicht: die Tür ist dort schlichter Link; die Fahrt
  (Öffnen + Zoom) spielt nach Tap identisch.

**(2) BODEN ohne JS / reduced-motion:** Statisch trägt: Plate (geschlossene Tür),
Tür-Link geschlossen aber klickbar (Ebene 2 ist ein echter `<a>`), Akteure/Zweite
Ebene SICHTBAR mit dauerhaft eingeblendetem Namen/Funktion, Tafel mit allen
Ergebnissen + Spendenlinks, Röhre mit dem vollen raum-eigenen Kugelstand,
Plakette, danach der gesamte bisherige Inhalt (FlowRail, Dossiers, Voten, Türen).
Reduced-motion mit JS: `stage-armed` wird nie gesetzt, Übergänge sofort — der
Boden ist identisch zum No-JS-Zustand.

**(3) TÜR ALS EBENE — Konsequenz für die Bilder:** Pro Raum ZWEI Varianten
desselben Plates (im Chat iteriert, nicht neu gewürfelt): **A geschlossen**,
**B offen** (Türblatt angelehnt, Öffnung zeigt warmen Lichtaustritt + angedeutete
nächste Szene). Das Türblatt schneiden wir selbst als Rechteck-Crop aus Plate A
(`sips`, %-Koordinaten nach Vermessung) — pixelgleiche Passung ohne
Generierungs-Risiko; Transparenz-Cutout von ChatGPT wird NICHT benötigt.
Ebene 1 zeigt Plate B nur in der Türzone (`clip-path: inset(...)`, %-vermessen).

**(4) ZWEITE EBENE je Raum:** Study: **The Scout** (links, Stehpult mit Laterne)
+ **The Warden** (rechts, Schreibtisch mit Hauptbuch) — zwei Cutouts, Blick
nach innen. Council: **N Lesepulte** — EIN Pult-Cutout, N-mal gerendert
(N = `modelTracks.length`, leichte Staffelung per `nth-child`: Skala/X-Versatz) —
generisch skalierbar statt drei festgemalter Pulte (Amendment-konform).
Archiv: **die Protokolle** — Cutout „Stapel gebundener Protokollbände mit Siegel
auf kleinem Karteischrank" (die Aufzeichnungen nehmen ihre Plätze ein — dieselbe
Grammatik). Hover/Fokus auf Ebene-3-Elemente blendet Name+Funktion ein
(neue i18n-Keys; Buttons mit `aria-expanded`, No-JS: dauerhaft sichtbar).

**(5a) Röhre rückwärts:** Kugeln laufen **nicht** zurück. Jeder Raum hat einen
definierten Füllstand (akkumulierend: Study 2 — Frage, Belege; Council 5 — +Drei
Antworten, Umdenken, Zählen; Archiv 6 — +Veröffentlichen). Beim Rückwärtsgehen
steht die Zielröhre bereits gefüllt da (ihre Sequenz spielt nur beim Vorwärts-
Eintritt; bei Back-Navigation statisch gefüllt — kürzer, ruhiger).
**(5b) Ergebnisse während der Fahrt:** Tafel fadet in Phase 1 kurz aus (~250 ms)
und im neuen Raum bei dessen Schritt 3 wieder ein. „Immer sichtbar" gilt für die
Zustände, die 2-s-Kamera ist Übergang — bewusst so gewählt, weil eine starr
mitgezogene Tafel den Raumwechsel verwässert.
**(5c) Topologie:** Ring vorwärts über die Mitteltür: Study→Council→Archiv→Study
(Archiv-Mitteltür führt zurück ins Study — Vorgabe). Die bestehenden Tür-Karten
unter jedem Raum bleiben unverändert (Direktsprünge Study→Archiv, Council→Archiv,
alle Rückwege, No-JS-Träger, Auffindbarkeit).

**(6) Performance-Budget:** Initial je Raum ≤ **1,0 MB** (Plate A ≤ 320 kB JPEG
q≈60 bei 1600×686 bzw. 1024×1536 ≤ 300 kB, Türblatt-Crop ≤ 60 kB, 1–2 Cutouts
≤ 180 kB, Röhren-Embleme vorhanden); Plate B nachgeladen bei Lock/idle
(`requestIdleCallback`, ≤ 320 kB) → gesamt ≤ 1,4 MB/Raum. Nur `transform`/
`opacity`/`clip-path` animiert (Kompositor), keine Layout-Animationen; VT-Zeiten
≤ 1,1 s je Phase. Gemessen per CDP (Ladegrößen + Laufzeit wie bisher).

## 4. No-JS-/A11y-Vertrag (unverändert hart)

Ein wirksames h1 je Raum (bleibt), Tür-Link ≥44 px + sichtbarer Fokus + aria-label
(„Durch die große Tür: The Council" o. ä.), Ebene-3-Elemente tastaturerreichbar
(Buttons), Kontraste AA auf Scrim/Panel, Reflow 320/390, Sprachumschalter fix
(bleibt), Historie über echte URLs (Direkteinstieg spielt die Raumsequenz mit
korrektem Röhrenstand — jeder Raum rendert seinen Füllstand autark aus der Route).

## 5. Umsetzungsskizze (nach „los")

1. **Zuerst Bilder:** Aufträge §7 an Afschin → eintreffende PNGs nach
   `docs/asset-originals/media/provenance/` + Derivate per `sips` (Plates,
   Türblatt-Crops nach Vermessung, Cutouts) + `ASSETS.md` fortschreiben.
   Interim zum Bauen: provisorische Stand-ins aus vorhandenen Plates
   (zerschnittene Crops), werden 1:1 ersetzt — Markup/CSS ändert sich nicht.
2. `StageHero.svelte` + `StageTube.svelte` neu; `RoomHero` bleibt (Archiv nutzt
   denselben StageHero wie alle); Räume auf StageHero umstellen.
3. `room-transitions.js`: Drei-Phasen-Fahrt (Retreat→Open→VT) für Mitteltür-Klicks
   (Klasse `stage-door`), Tür-Karten behalten die bisherige 2-s-Fahrt.
4. i18n: `stage.actors` (Name/Funktion), Röhren-Kurznamen, Tür-aria-Labels (DE+EN).
5. Tests: Röhren-Füllstand je Raum (akkumuliert), Mitteltür-Link + aria-label,
   Akteure benannt (Study), N Pulte aus Daten (Council), Protokoll-Ebene (Archiv),
   Boden-Assertions (No-JS trägt alles), h1=1, EN-Spiegel, neue Assets im Deploy.
6. Verifikation: Build warnungsfrei, 16+X Tests grün, CDP-Screenshots
   (Sequenz-Endstand je Raum Desktop/Mobil, Hover-Peek, Unlocked, EN, No-JS,
   reduced-motion, 320/390, 900–1200-Band), Fahrt-Zeitmessung, Zurück-Button.

## 6. Was NICHT angefasst wird

Datenschicht (`content.js`, `homepage.js`), `ResultBoard`-Datenlogik, Tür-Karten,
FlowRail-Inhaltsabschnitt unter dem Hero (bleibt als vollständige Erklärung),
Layout-Scrim/Ausweich-Spalte, Sitzungs-/Archiv-Inhalte, die 16 bestehenden Tests
(werden erweitert, nicht umgeschrieben — Ausnahme: neue Asset-Namen).

## 7. BILDAUFTRÄGE AN CHATGPT (direkt versandfertig)

Stilanker für ALLE Aufträge (jedem Prompt beilegen + je eines der vorhandenen
Plates als Referenzbild anhängen): „Gemalte Konzeptkunst, nächtlich, warmes
Bernstein/Messing-Lampenlicht gegen kaltes Mondblau, gleiche Bildwelt wie das
Referenzbild. KEINE Personen, KEIN Text, KEINE Wasserzeichen. Ruhige, dunkle
Zonen für UI-Overlays: linke Drittelzone (Tafel), untere Mitte (Titel), unterer
Rand (Leiste)."

**A1/A2 — Study-Bühne (Querformat 1915×821 + Hochformat 1024×1536):**
„Studierzimmer-Vorzimmer in der Bildwelt des Referenzbilds. Auf der Rückwand
MITTIG eine große geschlossene hölzerne Doppeltür (das kompositorische Zentrum,
von beiden Seiten gleich viel Raum). Links eine große LEERE dunkle Schiefertafel
im Holzrahmen, rechts ein hohes Fenster mit Vollmond. Zwei leere Schreibtische
mit ausgeschalteten Lampen links und rechts des Raums (Platz für spätere Figuren).
Variante A: Tür geschlossen."
Dann im selben Chat: „Identische Komposition, dieselbe Kamera: die Doppeltür
steht einen Spalt offen, warmes goldenes Licht tritt heraus, im Türspalt schemenhaft
eine runde Maschinenhalle mit Kerzen." (Variante B; im Hochformat wiederholen.)

**B1/B2 — Council-Bühne (Quer + Hoch):** „Runder nächtlicher Ratssaal (Referenz):
kreisende Steintribünen, zentral vorn die Messing-Zählmaschine. In der hinteren
Wand MITTIG eine schlichte einflügelige Holztür. Links ruhige dunkle Wandzone
(für Tafel-Overlay), rechts hohe gotische Fenster mit Mondblau. Kerzenlicht.
Variante A: Tür geschlossen." Iteration: „Dieselbe Kamera: die Tür steht einen
Spalt offen — dahinter ein kühler, schmaler Archivgang mit Karteischränken und
einer einzigen warmen Lampe, als schmaler Lichtstreif sichtbar." (Variante B.)

**C1/C2 — Archiv-Bühne (Quer + Hoch):** „Nächtliches Archiv (Referenz): hohe
Regale und Karteischränke, Staub im Lampenlicht. Auf der Rückwand MITTIG eine
ältere Holztür mit Messingschild. Links freie dunkle Wandzone, rechts kleines
hohes Fenster mit Mond. Variante A geschlossen; Iteration B: Tür einen Spalt
offen — dahinter das warme Vorzimmer mit der großen Schiefertafel angedeutet."

**D — Akteur-Cutouts (transparente PNGs, je ~900×1400):**
„Volle Figur + Möbel als freigestelltes Element auf transparentem Grund, gemalter
Stil der Referenz, Blickrichtung nach rechts: THE SCOUT — jüngere Person mit
Satteltasche und Stab-Laterne an einem hohen Stehpult mit Karten und Papieren,
warmer Laternenschein von links." / „Blickrichtung nach links: THE WARDEN —
ältere Person mit Schlüsselbund am Gürtel an einem Schreibtisch mit aufgeschlagenem
Hauptbuch und grüner Bankers-Lampe, warmes Licht von rechts."

**E — Pult-Cutout (transparent, ~800×1100):** „Ein hölzernes Lesepult mit
aufgeschlagenem Folianten und kleiner Kerze, Dreiviertelansicht, freigestellt auf
transparentem Grund, Stil der Referenz." (Wird N-mal gerendert.)

**F — Archiv-Cutout (transparent, ~900×1100):** „Kleiner Karteischrank mit einem
Stapel gebundener Protokollbände, Wachssiegel und Messing-Lämpchen, freigestellt
auf transparentem Grund, Stil der Referenz."

Hinweise für die Generierung: Varianten B UNBEDINGT als Iteration auf Variante A
im selben Chat (Kamera/Horizont müssen identisch bleiben — sonst flackert der
Hover). Tür rechteckig und möglichst perspektivisch frontal (erleichtert den
Crop). Durchblick-Zonen hinter den Türen klein halten (schmaler Streif genügt).

## 8. Offen gemeldet

- Die Türblatt-Drehung (`rotateY`) über einem rechteckigen Crop ist eine
  stilisierte Öffnung (Ansatz links, Perspektive via `perspective()`); ein echtes
  3D-Scharnier mit sichtbarer Türkante wäre nur mit modelliertem Cutout möglich —
  bewusst einfach gehalten, Stilbruch-Risiko gering (dunkle Szene, kurze Fahrt).
- ChatGPT-Konsistenz zwischen Quer- und Hochformat ist erfahrungsgemäß gut, aber
  nicht garantiert; Abnahme-Kriterium: Tür mittig ±5 %, Tafelzone links ruhig.
- `20_35_46 (3)` (Archiv-Portrait) wäre als statischer Archiv-Plate denkbar, hat
  aber keine Tür → verworfen, alle drei Räume bekommen einheitlich neue Plates.
