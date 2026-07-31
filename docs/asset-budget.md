# Asset-Budget — Bestell-Gate (B3/D)

Stand: 2026-07-19, Branch `feat/council-rooms`. **Regel: Codex erzeugt nur, was hier eine
Zeile hat.** Deckel §4: initiale Last je Raum **Desktop ≤ 1,2 MB / Mobil ≤ 900 KB** —
**plus zweite Dimension (Nachtrag A): dekodierte Fläche ≤ 4 MP je Raum im Ruhezustand,
≤ 6 MP im Übergangs-Peak.** Stage-JS ≤ 10 KB gzip (gemessen: 2,1 KB ✓).
**Überschreitung ⇒ tauschen/dimensionieren, nicht hoffen.**

Format-Regel (Nachtrag A1): jedes Derivat wird als **AVIF und WebP encodiert, die
kleinere Fassung wird eingecheckt** (Encoder lokal: `avifenc -s 6 -q 55` vs `cwebp -q 80`,
Muster `/tmp/nc-reencode.sh`; keine Build-Dependency). Bisheriger Befund: AVIF gewann
überall (21/21). PNG nur als C2PA-Master in der Provenienz, nie im Deploy-Pfad.

## 1 · Grundlast heute (AVIF-Stand, gemessen per CDP Network, Cache aus, 2026-07-19)

„Grundlast" = alles außer der Raum-Plate: prerendered HTML (das §0-Dokument), JS, CSS,
10 Embleme (6 Prozess + 4 Bereich), Türbilder/Sonstiges. Messzeilen: checks.txt A1/A3.

| Raum | Viewport | Gesamt | Plate | Grundlast |
|---|---|---|---|---|
| `/` Study | Desktop | 350 | 57 | **293** (inkl. 23 Tür-Karten + ~10 favicon/manifest) |
| `/ratssaal/` | Desktop | 365 | 104 | **261** |
| `/archiv/` | Desktop | 442 | 183 | **259** |
| `/` Study | Mobil | 291 | 31 (800-px-Stufe) | **260** |
| `/ratssaal/` | Mobil | 365 | 104¹ | **261** |
| `/archiv/` | Mobil | 314 | 55 (800-px-Stufe) | **259** |

Alle Angaben KB (encodedDataLength). ¹ Council hat heute keine eigene Mobil-Plate
(Platzhalter-Slot), es wird die Desktop-Plate ausgeliefert.

Zerlegung der gemeinsamen Grundlast ≈ 260 KB: HTML 121 (§0, nicht verhandelbar) +
JS 49 + CSS 8 + **10 Embleme 81** (war 294 als JPEG — der A1-Tausch ist bereits
erledigt und eingecheckt).

**Verfügbares Asset-Budget je Raum: Desktop ~940 KB, Mobil ~640 KB.**
(Vor A1 waren es ~600–730 / ~430 — der Engpass ist aufgelöst.)

## 2 · Der aufgelöste Widerspruch: 1050 gemessen vs. 550–750 geschätzt

Die Runde-1-Schätzung bezog sich auf die Bildlast des Zielzustands, die Messung auf den
Gesamttransfer des Ist-Zustands; drei Befunde trugen die Differenz (Grundlast existierte
in der Schätzung nicht · Archiv-Plate Ausreißer 579 KB · Study-Türbilder additiv).
**Auflösung durch A1 (gemessen, nicht projiziert):** Archiv-Plate 579→183 KB,
Embleme 294→81 KB, alle sechs Routen-Initialwerte ≤ 37 % der Deckel. Der Widerspruch
besteht nicht mehr; die Auflage für die neue Archiv-Plate bleibt (§5).

## 3 · Asset-Tabelle (Katalog Umlauf §6: 19 Aufträge + 6 sips-Crops)

KB = Planwert AVIF, begründet aus heutigen Derivaten (Plates 1600w: 57–183 KB;
Portrait 800×1200: 31–55 KB; Tür 480×640: 10–13 KB; Emblem 320²: 8–9 KB).
Cutouts haben keine Alpha-Referenz im Repo — konservativ aus der WebP-Schätzung der
Vorrunde; A1-Regel + **Nachmessung Pflicht** (bricht eine Serie das Budget, wird
getauscht, nicht gehofft). MP = dekodierte Fläche der kleinsten sinnvollen
Master-Dimension (Auflage, §5).

| # | Asset | Raum | Format/Dimension | KB (Plan) | MP | Initial/Lazy |
|---|---|---|---|---|---|---|
| 1 | Study Plate A Desktop | Study | AVIF 1600×900 | 120 | 1,44 | **Initial** |
| 2 | Study Plate B Desktop | Study | AVIF 1600×900 | 120 | 1,44 | Lazy (Peek) |
| 3 | Study Plate A Mobil | Study | AVIF 800×1200 | 60 | 0,96 | **Initial** |
| 4 | Study Plate B Mobil | Study | AVIF 800×1200 | 60 | 0,96 | Lazy |
| 5 | Scout Cutout | Study | AVIF/WebP Alpha ≤600×900 | 90 | 0,54 | **Initial** (Einfahr-Ebene) |
| 6 | Warden Cutout | Study | AVIF/WebP Alpha ≤600×900 | 90 | 0,54 | **Initial** |
| 7 | Council Plate A Desktop | Council | AVIF 1600×900 | 150 | 1,44 | **Initial** |
| 8 | Council Plate B Desktop | Council | AVIF 1600×900 | 150 | 1,44 | Lazy |
| 9 | Council Plate A Mobil | Council | AVIF 800×1200 | 70 | 0,96 | **Initial** |
| 10 | Council Plate B Mobil | Council | AVIF 800×1200 | 70 | 0,96 | Lazy |
| 11 | Neutrales Pult-Cutout | Council | AVIF/WebP Alpha ≤600×900 | 80 | 0,54 | **Initial** (1 Bitmap, N-fach gerendert) |
| 12 | Zählmaschinen-Detail Desktop | Council | AVIF 1200×900 | 110 | 1,08 | Lazy (Trigger/Idle) |
| 13 | Zählmaschinen-Detail Mobil | Council | AVIF 800×1000 | 60 | 0,80 | Lazy |
| 14 | Archive Plate A Desktop | Archiv | AVIF 1600×900 | 200 (Auflage ≤ 220; heute 183 belegt) | 1,44 | **Initial** |
| 15 | Archive Plate B Desktop | Archiv | AVIF 1600×900 | 200 | 1,44 | Lazy |
| 16 | Archive Plate A Mobil | Archiv | AVIF 800×1200 | 80 | 0,96 | **Initial** |
| 17 | Archive Plate B Mobil | Archiv | AVIF 800×1200 | 80 | 0,96 | Lazy |
| 18 | Protokollbände-Cutout | Archiv | AVIF/WebP Alpha ≤600×900 | 90 | 0,54 | **Initial** (zweite Ebene) |
| 19 | Archivschublade-Cutout | Archiv | AVIF/WebP Alpha ≤600×900 | 100 | 0,54 | **Initial** (konditional, Auflage Runde 1) |
| C1–C6 | Tür-Crops (sips aus Plates, 3 Räume × quer/hoch) | alle | AVIF 640w | 20 quer / 15 hoch | 0,23 q / 0,55 h | Lazy (below-fold, Lock-Interaktion) |

Kein Generierungs-Auftrag: Portal-Vorschau-Miniaturen (sips-Derivat aus Plate A,
~50 KB, nie initial) · separate Mobil-Cutouts erst nach dem Horizont-/Perspektivtest
(bis dahin zählen die Desktop-Cutouts auch mobil — die Summen unten rechnen genau so,
Worst Case).

## 4 · Raum-Summen gegen die Deckel

### KB (Initial = Grundlast + Initial-Zeilen; Study-Desktop um ersetzte Tür-Karten 23 KB bereinigt ⇒ 270)

| Raum | Rechnung (KB) | Summe | Deckel | Stand |
|---|---|---|---|---|
| Study Desktop | 270 + 120 + 90 + 90 | **570** | 1200 | 48 % ✓ |
| Council Desktop | 261 + 150 + 80 | **491** | 1200 | 41 % ✓ |
| Archiv Desktop | 259 + 200 + 90 + 100 | **649** | 1200 | 54 % ✓ |
| Study Mobil | 260 + 60 + 90 + 90 (Desktop-Cutouts, Worst Case) | **500** | 900 | 56 % ✓ |
| Council Mobil | 261 + 70 + 80 | **411** | 900 | 46 % ✓ |
| Archiv Mobil | 259 + 80 + 90 + 100 | **529** | 900 | 59 % ✓ |

### MP (Ruhe; nur initial Geladenes, dedupliziert je URL — Messmethode `/tmp/nc-mp.mjs`)

Ruhe-Ziel je Raum: **≤ 3,4 MP** (nicht 4,0 ausnutzen — Begründung: realistischer
Übergangs-Peak = Ruhe_neu + 2 VT-Root-Snapshots à 1,30 MP muss ≤ 6,0 bleiben).

| Raum | Rechnung (MP) | Summe | Ziel | Stand |
|---|---|---|---|---|
| Study Desktop | 1,44 Plate + 0,60 Röhre-6 + 0,54 Scout + 0,54 Warden | **3,12** | 3,4 | 92 % ✓ |
| Council Desktop | 1,44 + 0,60 Röhre + 0,40 Pillar-4 + 0,54 Pult | **2,98** | 3,4 | 88 % ✓ |
| Archiv Desktop | 1,44 + 0,60 + 0,54 Bände + 0,54 Schublade | **3,12** | 3,4 | 92 % ✓ |
| Study Mobil | 0,96 + 0,60 + 0,54 + 0,54 | **2,64** | 3,4 | 78 % ✓ |
| Council Mobil | 0,96 + 0,60 + 0,40 + 0,54 | **2,50** | 3,4 | 74 % ✓ |
| Archiv Mobil | 0,96 + 0,60 + 0,54 + 0,54 | **2,64** | 3,4 | 78 % ✓ |

**Peak (Übergang, zwei Modelle — dieselbe Modellfrage wie der A2-Befund):**
realistisch (altes Dokument gibt Dekodierungen frei): Ruhe_neu 3,12 + 2 Snapshots 2,60
= **5,72 ≤ 6 ✓**. Streng (altes Set bleibt komplett resident + neue Plate):
3,12 + 1,44 + 2,60 = **7,16 > 6 ✗** — dominiert von den beiden Viewport-Snapshots
(2,6 MP, inhärent für jede Root-VT bei 1440×900, nicht reduzierbar). Kein neuer
Befund: die Modell-Frage ist mit A2 an den Steward gemeldet (checks.txt, Zeile 93)
und bleibt dort zur Entscheidung offen; diese Tabelle hält das realistische Modell ein.

## 5 · Gate-Befunde — alte ROTs aufgelöst, neue Auflagen gesetzt

1. **ERLEDIGT — PNG-Cutout-ROT:** die Formatfrage ist durch die A1-Regel beantwortet
   (AVIF/WebP, je kleinere Fassung einchecken; Alpha unterstützen beide). PNG bleibt
   ausschließlich C2PA-Master in `docs/asset-originals/media/provenance/`.
2. **ERLEDIGT — Mobil-ROT Study 931 / Archiv 946:** die geforderten Tausch-Aktionen
   sind in A1/A3 ausgeführt und gemessen (Embleme 294→81 KB = Grundlast −213;
   800-px-Mobil-Stufe; Archiv-Plate 579→183). Neue Mobil-Summen 46–59 %.
3. **BESTÄTIGT — Archiv-Plate-Auflage:** ≤ 220 KB Desktop (heute 183 belegt, dass das
   Motivniveau das hält), ≤ 80 KB Mobil.
4. **NEU — MP-Auflagen für die Bestellung:** Plates 1600×900 (1,44 MP) bzw. 800×1200
   (0,96 MP), kein 1920w im Deploy-Pfad · Cutouts ≤ 600×900 (0,54 MP) · Tür-Crops
   `loading="lazy"` (below-fold; das Lock-Preloading holt sie bei Annäherung) ·
   Ruhe-Ziel ≤ 3,4 MP je Raum als Gate-Wert (Peak-Begründung oben).
5. **Regel bleibt:** kein weiteres Initial-Asset in einem Raum ohne gleichzeitigen
   Tausch — trotz komfortabler KB-Puffer (41–59 %) bindet die MP-Spalte (74–92 %).

*Nachmessung Pflicht: jede integrierte Asset-Serie wird per CDP nachgemessen
(KB: Muster `/tmp/nc-b3-groundload.mjs`; MP: `/tmp/nc-mp.mjs`).*

## 6 · Nachtrag 20.07.2026 — Serie 1c eingebaut, MP-Modell korrigiert

**Einbau (Study, zweite Ebene):** `actors/scout.avif` + `actors/warden.avif` je
540×810 Alpha (0,44 MP, 25/20 KB — Budget-Zeilen 5/6 mit Reserve eingehalten) und
**neue Zeile** `ambient/clouds-study.avif` 384×512 (0,20 MP, 11 KB, Lazy/Ambient —
Wolkenzug im Mondfenster, bei reduced-motion/no-JS statisch bzw. das gemalte
Plate-Bild). Wolken-Zeile in §3 ergänzen: „20 · Wolkenzug Study · AVIF 384×512 ·
11 KB · 0,20 MP · Lazy (Ambient)".

**MP-Modell korrigiert (Messung schlägt Modell):** die Nachmessung zeigte Ruhe
4,52 MP statt der gerechneten 3,12 — das Modell hatte Tür-Karten (0,54 MP) und
die vier Tafel-Pfeiler (0,41 MP) nie mitgezählt; die reale Seite lag vor dem
Einbau bereits bei ~3,0 MP. Korrektur durch Dimensionierung (Regel §5.5):
Wolke auf 384×512, Akteure auf 540×810, **Embleme 320²→160²** (1,02→0,26 MP,
Anzeige ≤ 64 px ⇒ DPR2 gedeckt; KB 83→30 als Nebengewinn; `process-three-answers`
als .webp). Gemessener Endstand: **Ruhe Desktop 3,31 MP ✓, Mobil 1,56 MP ✓**;
KB (B3-Protokoll): Study Desktop 445 KB / Mobil 299 KB — alle Deckel grün.
Belege: `docs/review/serie-1c-gate/checks.txt`.

**Lektion fürs Modell:** die MP-Spalte ab jetzt aus der Messung fortschreiben
(alle `<img>`-URLs dedupliziert), nicht aus der Bestell-Tabelle — die Tabelle
zählt nur, was bestellt wurde, nicht, was die Seite lädt.
