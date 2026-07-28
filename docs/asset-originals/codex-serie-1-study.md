# Bestellung Serie 1 · The Study (Aufträge 1–6) — an Codex

**Status: BEREIT, NICHT AUSGELÖST.** Gates: Slice-Abnahme C 11/11 ✓ (checks.txt,
2026-07-19) · asset-budget.md unter beiden Deckeln ✓. Auslösung ausschließlich durch
den Steward. Danach: §5-Disziplin — Serie 1 komplett, **Mini-Kontaktbogen als Gate**,
erst dann Serie 2.

Dieses Dokument ist der vollständige Auftrag; es interpretiert den Umlauf
(`docs/fable-2026-07-19-buehnenspiel-synthese-umlauf--mit-runde3-codex.md`, §5/§6)
nicht neu, sondern macht ihn bestellbar. Bei Konflikt gilt der Umlauf.

## 0 · Gemeinsame Vorgaben (gelten für alle 6 Aufträge)

**Stimmung/Stil:** gemalte Konzeptkunst, kein Fotorealismus — warmes Bernstein/Messing
(Kerzen, Lampen, Messingarmaturen) gegen kaltes Mondblau (Fenster, Nacht). Stilreferenz:
die vorhandenen Plates `docs/asset-originals/media/provenance/vorraum.png` und
`ratssaal.png` (C2PA-Master der aktuellen Szenen) — bitte als Referenz einlesen;
die Serie muss wie dieselbe Welt wirken, eine Zeit später am selben Ort.

**Kompositions-Grammatik (verbindlich, Umlauf §5):**
- zentrale Tür: Mittelpunkt max. ±5 % von der horizontalen Bildmitte,
- Tafelzone links (dunkle Schieferfläche, frei — das Frontend legt später Text darauf),
- Mondfenster rechts (kalter Gegenpol),
- ruhige, dunkle untere Textzone (unteres Drittel frei von Motiv-Details),
- nichts Wichtiges in den äußeren 8–10 % oben/unten (cover-Crop-Reserve),
- **kein Text, keine Buchstaben, keine Ziffern, keine lesbaren Buchrücken/Schilder.**

**Tür (Auflage):** möglichst frontal, klare rechteckige Kontur, keine starke
perspektivische Verzerrung, genug sichtbarer Rahmen ringsum für einen sauberen
`sips`-Crop (das Türblatt wird später als eigenes Anzeige-Derivat ausgeschnitten).

**Kamera A↔B:** exakt gleiche Kamera, Brennweite, Kamerahöhe, Fluchtpunkt,
Objektpositionen — **nur der definierte Türzustand ändert sich** (A geschlossen,
B offen). Quer↔Hoch: gleiche gedachte Kamerahöhe und Raumgeometrie, aber
**eigenständige Komposition, kein Crop**.

**Technik je Auftrag:**
- Master: PNG mit C2PA, Ablage `docs/asset-originals/media/provenance/` (nie im
  Deploy-Pfad), dazu ASSETS.md-Eintrag (Rolle, Prompt, Datum, Quelle, C2PA-Hinweis).
- Derivate (durch Umsetzer, nicht durch Codex): AVIF + WebP, kleinere Fassung wird
  eingecheckt (`avifenc -s 6 -q 55` vs `cwebp -q 80`).
- Budget-Auflagen aus `docs/asset-budget.md` (Tabelle §3): siehe je Auftrag.

## 1 · Study Plate A — Desktop, geschlossen (16:9)

- **Motiv:** The Study — das stille Vorzimmer des Hauses, in dem die Antwort dieser
  Sitzung bereits wartet. Studierzimmer-Atmosphäre: dunkles Holz, wenige warme
  Lichtquellen, gesammelte Stille vor der Beratung. Die **große geschlossene Tür in
  der Bildmitte** (dahinter: The Council), links die **leere dunkle Tafel** an der
  Wand, rechts das **Mondfenster**. Zwei schmale, leere Tische/Pulte flankieren die
  Mitte im unteren Halbfeld (Plätze der Akteure — unbesetzt, die Figuren kommen als
  eigene Cutouts dazu).
- **Format:** Master 1920×1080 → Derivat 1600×900. Auflage: ≤ 120 KB (Plan), MP 1,44.
- **Fokus:** die Tür trägt die Komposition; Tafel- und Fensterzone bleiben lesbar,
  aber ruhig.
- **Ruhige Zonen:** Tafelfläche links (vollständig frei), unteres Drittel (Textzone),
  keine Details in den äußeren 8–10 % oben/unten.

## 2 · Study Plate B — Desktop, offen (Iteration von 1)

- **Motiv:** identischer Raum, identische Kamera — die Tür steht jetzt **einen Spalt
  offen**: kontrollierter Durchblick in den nächsten Raum (warmer, kaum sichtbarer
  Andeutungsraum Richtung Council — **nicht bilddominant**, kein zweites Bühnenbild).
- **Format/Auflagen:** wie Auftrag 1.
- **Zweck:** Lock-Zustand/Tür-Peek (Mouseover) und Peek hinter der Tür-Ebene.

## 3 · Study Plate A — Mobil, geschlossen (2:3, eigene Komposition)

- **Motiv:** derselbe Raum, dieselbe Raumgeometrie und Kamerahöhe, aber als
  **eigenständige Hochformat-Komposition** gedacht (Dramaturgie vertikal: Tür mittig,
  Tafelzone oberhalb/links angedeutet, Mondfenster rechts; Akteurs-Tische kompakter,
  ruhige Zone unten großzügiger). **Kein Crop des Querformats.**
- **Format:** Master 1080×1620 → Derivat 800×1200. Auflage: ≤ 60 KB (Plan), MP 0,96.

## 4 · Study Plate B — Mobil, offen (Iteration von 3)

- Wie Auftrag 3, nur der Türzustand ändert sich (Spalt, kontrollierter Durchblick).
- **Format/Auflagen:** wie Auftrag 3.

## 5 · Scout-Cutout — Figur + Tisch, freigestellt (Alpha)

- **Motiv:** **The Scout** — der aufmerksame Sammler des Gremiums: eine eher junge,
  bewegliche Gestalt in schlichtem, reisetauglichem Gewand; Attribute der Suche
  (z. B. Kartenrohr, kleines Fernrohr oder Satchel — dezent, kein Steampunk-Übermaß).
  Dazu **ihr schmaler Stehtisch** mit wenigen Papieren/Karten. Ganzkörper mit Tisch,
  Standfigur, Blick leicht nach **rechts** (zur Raummitte — sie fährt von links ein).
- **Stil:** dieselbe gemalte Konzeptkunst wie die Plates; warme Messing-Akzente.
  Figur ohne Umgebung, sauberer Alpha-Kanal (kein Schattenklecks außer einem
  bodenständigen, weichen Kontaktschatten).
- **Format:** Master ~1200×1800 (Alpha) → Derivat ≤ 600×900. Auflage: ≤ 90 KB
  (Plan, AVIF/WebP kleinere Fassung), MP 0,54.
- **Horizont-Auflage:** Augenhöhe der Figur und Tischoberkante als %-Werte der
  Bildhöhe im ASSETS.md-Eintrag vermerken (wird gegen den tatsächlichen Horizont des
  finalen Plates geprüft — Umlauf §5/Kamera).

## 6 · Warden-Cutout — Figur + Tisch, freigestellt (Alpha)

- **Motiv:** **The Warden** — der stille Hüter des Protokolls: eine ältere, ruhige
  Gestalt in würdevollem, dunklem Gewand; Attribute des Bewahrens (z. B. gebundener
  Journalband, Siegel oder kleine Lampe). Dazu **sein schwererer Schreibtisch** mit
  aufgeschlagenem Band. Ganzkörper mit Tisch, Standfigur, Blick leicht nach **links**
  (er fährt von rechts ein).
- **Stil/Format/Auflagen:** wie Auftrag 5 (kühlerer Akzent erlaubt — Mondblau am
  Saum statt Messing).

## 7 · Abnahme-Gate nach Serie 1: Mini-Kontaktbogen

Alle 6 Master gemeinsam auf einem Kontaktbogen prüfen (Umlauf §7): Farbtemperatur,
Schwarzpunkt, Messingfarbton, Mondblau, Pinsel-/Konzeptkunststil, Perspektive,
Türgröße, Tafelgröße, Fensterwirkung, Detailgrad, relative visuelle Gewichte.
**Ein einzelnes schönes Bild reicht nicht — der Satz muss als eine Welt wirken.**
Zusätzlich für diese Serie: Tür-Crop-Test per `sips` (saubere Kontur aus Plate A,
quer + hoch) und Horizont-Abgleich der Cutouts gegen Plate A. Erst nach diesem Gate
werden Derivate erzeugt und Serie 2 (Council) ausgelöst.
