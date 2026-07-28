> **Archiviert 2026-07-28 (CC) — Pre-CC-Bühnenspiel-Entwurf, durch die späteren Runden abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

---
folio_import: v1
type: note
target: 02-durchbruch
id: fable-2026-07-19-buehnenspiel-synthese-umlauf
source: fable-session-claude-ai
created: 2026-07-19
title: "Bühnenspiel — Synthese-Plan (Umlauf: Kimi → Opus → Codex)"
tags: [noblecause, buehnenspiel, synthese, umlauf, assets]
ref: opus-buehnenspiel-plan
---

# Bühnenspiel — Synthese der drei Pläne (Umlauf-Dokument)

**Von:** Fable (Vergleichsurteil über die drei unabhängigen Pläne) · **Beschlossen vom Steward:** Synthese-Ansatz angenommen; Abweichung zu Fables Empfehlung: **mehr Assets wagen** — jedes gute Asset ist ein Detail, das die Site schöner macht. **Umsetzer nach Konsens: Kimi** (aktuell stärkste Code-Leistung). **Bildgenerierung: Codex/ChatGPT** (seine Stärke bleibt seine Rolle).

## Umlauf-Protokoll (am Dokumentende fortschreiben)
1. **Runde 1 — Kimi** (dieses Dokument + `openai-buehnenspiel-plan--SKIP.md`): prüft die Synthese, ergänzt/korrigiert im eigenen Abschnitt, und trifft die **Asset-Vorauswahl** (§5): Welche der ~20–28 Codex-Assets zusätzlich zur gesetzten Basis übernehmen/umgestalten? Kriterium: Schönheits-Gewinn pro Ausrichtungs- und Gewichtsrisiko; Budget-Wirkung beziffern.
2. **Runde 2 — Opus:** prüft Synthese + Kimi-Ergänzungen, ergänzt/korrigiert.
3. **Runde 3 — Codex:** prüft final. **Einverstanden mit Plan + Asset-Auswahl → erzeugt die Bilder** (nach der Auftrags-Disziplin aus §1/Kimi). Nicht einverstanden → begründeter Einwand, nächste Runde beginnt wieder bei Kimi.
4. Konsens aller drei → Kimi baut. **Kein Baubeginn ohne abgeschlossenen Umlauf** (Ausnahme: §3 Schritt 2, der bewusst ohne neue Kunst auskommt).

Regeln: Ergänzungen als eigener, signierter Abschnitt unten — oben wird nichts umgeschrieben, der Umlauf ist selbst Protokoll. Widerspruch mit Begründung, nicht per Umformulierung. Patt entscheidet der Steward.

## §0 · Leitsatz (aus dem Opus-Plan, Verfassungsrang)
> **Die Seite ist bereits vollständig, bevor das Spiel beginnt. Die Inszenierung verzögert und bewegt nur — sie erzeugt nichts und versteckt nichts.**

Ohne JS = das unchoreografierte, vollständige Dokument. `prefers-reduced-motion` = derselbe Zustand. Bricht JS mitten in der Sequenz, bleibt ein vollständiges Dokument stehen. Alle Böden der Baseline gelten unverändert (No-JS-Vollwahrheit, ein h1 je Raum, ≥44 px, Reflow 320/390, AA-Kontraste, versiegelte Datennaht, Tabu-Pfade).

## §1 · Die Anteile der drei Pläne (was woher kommt, und warum)
**Aus Opus:** Leitsatz §0 · **Umsetzungsreihenfolge Schritt 1** — Choreografie-Gerüst zuerst über den HEUTIGEN Plates beweisen, bevor Kunst bestellt wird (kostet nichts, falsifiziert früh) · Röhren-Mechanik als **Zustands-Differenz** (jeder Raum definiert seinen Füllstand; die Animation ist der Diff zum Vorzustand — Rückwärtsgang und Direkteinstieg sind damit gratis korrekt) · Scroll während des Aufbaus = **Sprung in den Endzustand**. Codex' Intent-Queue wird NICHT übernommen: nachgespielte Austritts-Beats gegen eine geäußerte Nutzerabsicht sind Bevormundung; der Sprung respektiert sie.
**Aus Kimi:** Implementierungs-Substrat — `StageHero.svelte` als Ebenen-Stack, `stage-armed`-Muster (Default = alles sichtbar; JS versteckt erst beim Mount und startet die Sequenz) · Wiederverwendung von ResultBoard, room-transitions.js/VT-Maschinerie, FlowRail-Inhalten, i18n-Spiegel · **Türblatt als sips-Crop aus dem eigenen Plate** (pixelgleiche Passung, kein Generierungs-Glücksspiel; rotateY-Öffnung als bewusst stilisierte Bewegung) · **N Lesepulte aus `modelTracks.length`** — EIN Pult-Cutout, N-fach gerendert: Amendment-fest für die Fünf-Sitze-Zukunft und wahrt die Vorwegnahme-Sperre (KEINE drei anbieterspezifisch gemalten Pulte) · Bildauftrags-Disziplin: Variante B als Iteration im selben Chat (identische Kamera), Stilanker + Referenzbild je Prompt, Abnahme „Tür mittig ±5 %".
**Aus Codex:** **Kompositions-Grammatik als Vertrag für ALLE Plates** — Tafel-Zone links, Tür zentral im sicheren Crop, Mondfenster rechts als kalter Gegenpol, ruhige untere Textzone, nichts Wichtiges in den äußeren 8–10 % (geht wörtlich in jeden Bildauftrag) · **Reise-Zustand der Ergebnis-Tafel**: Ergebnisse verschwinden NIE — bei der Türfahrt komprimiert die Tafel zu einer schmalen messinggerahmten Leiste oben links, reist mit und expandiert im Zielraum auf dessen Tafelfläche („dieselbe Sitzung wandert durchs Haus", sichtbar gemacht; ersetzt Opus' Überblenden und Kimis Aus-/Einblenden) · **Vertical Slice**: The Study wird zuerst KOMPLETT gebaut und abgenommen (Eintritt, Lock, Scroll-Öffnung, Tür-Preview, Fahrt), erst dann Council/Archive · Mobil als **eigene Hochformat-Komposition** (2:3-Plates, keine Desktop-Crops; Dramaturgie vertikal: zweite Ebene von unten, kürzere Wege, gleiche Reihenfolge) · Abnahme-Katalog inkl. **Bewegungsnachweis** (Frame-Sequenzen der vier Fahrten — Screenshots fangen VT-Ebenen nicht, Baseline-Falle 10).

## §2 · Dramaturgie (konsolidiert)
Eintritt ~2 s, Takte überlappend (~50 ms Versatz): Plate → zweite Ebene auf Schienen → **Ergebnis bei ~1,2 s** → Titel/Erklärung → Röhre füllt (Differenz). Lock = visueller Ruhezustand, nie ein gesperrter Eingabekanal. Tür: echter `<a>` über der Türregion; Hover/Fokus schwenkt das Türblatt ~8°, der Lichtspalt wächst, dahinter maskiert der nächste Raum. Fahrt ~2,0 s vorwärts (Rückfahrt der Bühnenelemente → Türöffnung → Durchgang, transform-origin Türmitte), ~1,2 s rückwärts; auf der bestehenden VT-Maschinerie. Mobil: dauerhafter Lichtschimmer im Türspalt (kein Hover), Tap navigiert; Tür-Karten bleiben überall der zweite, barrierefreie Weg.

## §3 · Rollen & Reihenfolge
1. **Umlauf abschließen** (dieses Dokument, drei Runden).
2. **Kimi, Schritt 1 nach Opus:** Choreografie-Gerüst über den heutigen Plates — beweist §0, bevor ein einziges Bild bestellt ist. (Darf parallel zum Umlauf beginnen: berührt keine Kunst-Entscheidung.)
3. **Codex erzeugt die Assets** gemäß beschlossener Auswahl (§5) und der Auftrags-Disziplin aus §1; Ablage nach Baseline-Regeln (`docs/asset-originals/` + Provenienz + ASSETS.md, Derivate per sips/JPEG).
4. **Kimi baut den Vertical Slice (Study)** → Abnahme durch den Steward (Katalog aus §1/Codex) → Council/Archive → Mobil-Feinschliff → Tests erweitern, Budget messen, Screenshots + Frame-Sequenzen.
5. Merge auf master erst nach vollständiger Abnahme (Baseline-Arbeitsregeln: nie aus dem Feature-Branch deployen).

## §4 · Performance-Leitplanke (verträglich mit „mehr Assets wagen")
Gedeckelt ist nicht die Asset-ZAHL, sondern die LAST: initiale Bildlast je Raum **Desktop ≤ 1,2 MB / Mobil ≤ 900 KB** (Codex-Werte als Obergrenze); alles Weitere lazy nach Lock/idle. Stage-JS ≤ 10 KB gzip, keine Bibliothek; animiert wird nur transform/opacity/clip-path. **Mehr Schönheit ja — bezahlt aus dem Lazy-Budget, nie aus dem ersten Eindruck.**

## §5 · Asset-Entscheid (Runde-1-Auftrag an Kimi)
**Basis (gesetzt):** je Raum Plate A geschlossen (Quer 16:9 + Hoch 2:3 als eigene Kompositionen) + Plate B offen (Iteration, gleiche Kamera) + Türblatt-Crop aus A · Study-Cutouts Scout + Warden · EIN Pult-Cutout (N-fach gerendert) · Archiv-Cutout Protokollbände. Die Kompositions-Grammatik (§1/Codex) gilt für alle.
**Zur Entscheidung (aus Codex' Katalog; Auswahl durch Kimi, je Asset ein Begründungssatz + Budgetwirkung):** Zählmaschinen-Detailansicht für den Zähl-Fokus · Archiv-Zusatzebene (herausgezogene Schublade) · separate Mobil-Cutouts, wo die Desktop-Perspektive bricht · Portal-Vorschau-Miniaturen (≤ 100 KB) fürs Tür-Preloading · weitere Vorschläge nach Sichtung des vollen Codex-Katalogs. Steward-Wille: im Zweifel **für** das Detail, solange §4 hält.
**Nicht übernommen (begründet, im Umlauf anfechtbar):** drei anbieterspezifische Council-Pulte (bricht die N-Skalierung und die Vorwegnahme-Sperre) · Intent-Queue (§1/Opus-Begründung) · Video-Assets (Codex selbst dagegen).

## §6 · Publikations-Nachlauf (nach Go-Live, getrennt vom Bau)
Der Drei-Wege-Vergleich wird publiziert: nüchternes Protokoll in der NobleCause-Werkstatt — Kern ist der **Konvergenz-Befund** (drei Familien, unabhängig, identische Böden: kein Scroll-Hijacking, Dokument vor Spiel, Tür in die Mitte, Röhre als Raumzustand; Divergenz nur im Urteilsspielraum), N=1 ehrlich etikettiert, SKIP-Markierung als Unabhängigkeits-Disziplin erklärt. Referenz-Fassung für aion-lumen/LinkedIn getrennt davon. Dieses Umlauf-Dokument ist Teil des Belegs.

---

## Ergänzungen Runde 1 — Kimi

### 1 · Prüfung der Synthese (gegen alle drei Pläne)
Die Zuschreibungen in §1 stimmen. Zwei Synthese-Entscheide überstimmen meinen eigenen
Entwurf — ich akzeptiere sie ausdrücklich, mit Begründung:

- **Röhre als Zustands-Differenz (Opus) ersetzt mein „Kugeln laufen nicht zurück"**
  (mein §5a). Der Diff ist strikt besser: Rückwärtsgang und Direkteinstieg fallen
  gratis korrekt aus demselben Modell, statt Sonderfälle zu pflegen.
- **Reise-Zustand der Tafel (Codex) ersetzt mein Aus-/Einblenden** (mein §5b).
  Umsetzungsnotiz: Shared-Element-VT (`view-transition-name` auf dem
  ResultBoard), die Kompression zur Leiste läuft vor der Navigation auf der alten
  Route per Klasse, die Expansion ist Takt 3 des Zielraums. Am Code verifiziert:
  oben links ist frei (Sprachumschalter sitzt oben rechts, z-index 3; Tafel
  z-index 2), die Mitteltür liegt außerhalb des Leisten-Bands. No-JS und
  reduced-motion bleiben ohne Reisezustand — dort steht die Tafel je Raum
  statisch, das ist der Boden.

Klarstellungen:

1. **Türblatt-Crops: 6, nicht 3** — je Format einer (quer aus Plate A 16:9, hoch
   aus Plate A 2:3); die Tür sitzt in beiden Kompositionen an anderer Stelle.
2. **AVIF-Annahme vs. Werkzeug-Realität:** Codex' Budget (§22) setzt „AVIF
   bevorzugt, WebP-Fallback" — die hauseigene Werkzeugkette ist `sips`, das weder
   AVIF noch WebP schreibt; Derivate bleiben **JPEG**. Die Budgets unten sind
   gegen JPEG gerechnet und halten. Nur wenn die Messung am gebauten Slice den
   Cap bricht, einen Build-Zeit-Encoder (sharp/AVIF, reine devDependency) prüfen —
   jetzt keine neue Abhängigkeit.
3. Auftrags-Disziplin (§1/Kimi) um zwei Punkte ergänzt: Tür möglichst
   frontal/rechteckig malen lassen (erleichtert den Crop), Durchblick-Zone hinter
   der Tür klein halten; **neues Abnahmekriterium: gleiche Kamera-Höhe in Quer-
   und Hochformat** — Voraussetzung für Entscheid 3 unten.

### 2 · Asset-Vorauswahl (§5-Auftrag) — je Begründung + Budgetwirkung
**Basis bestätigt:** 16 Generierungs-Aufträge (12 Plates = 3 Räume × A/B × quer/hoch
· Scout · Warden · 1 Pult · Protokollbände) + 6 sips-Crops. Entscheidungen:

1. **Zählmaschinen-Detailansicht — ÜBERNEHMEN** (2 Assets: 4:3 ~1200 w + Hoch-Crop).
   Höchster Schönheitsgewinn bei geringstem Risiko: eine eigenständig gerahmte
   Nahansicht muss nicht pixelgenau am Plate andocken. Sie gibt dem Zählen-Schritt
   seinen Moment, ohne den Saal neu zu malen. **Trigger-Vorschlag:** Einblendung
   an der Zählen-Kugel der Röhre (Klick/Fokus) plus statische Figur im
   Council-Erklärabschnitt, kein Autoplay. Budget: lazy (Idle nach Lock bzw. bei
   Interaktion), ~2 × 150–200 KB JPEG — zahlt aus dem Lazy-Budget, der erste
   Eindruck bleibt unberührt.
2. **Archiv-Schublade — ÜBERNEHMEN, mit Auflage** (1 Asset): das Cutout enthält ein
   Stück Schrankfront — ein in sich geschlossenes Objekt, Bewegung nur 10–20 px
   Translate, **kein Andocken an gemalte Schränke**. Bei Abnahme-Urteil „Gimmick"
   fällt sie ersatzlos weg (Codex selbst: „nur verwenden, wenn sie nicht nach
   Gimmick aussieht"). Budget: initial im Archiv (+120–150 KB) → Archiv-Summe
   ~700 KB < 1,2-MB-Cap. Der Steward-Wille „im Zweifel für das Detail" ist hier
   erfüllbar, weil die Auflage das Ausrichtungsrisiko konditioniert.
3. **Separate Mobil-Cutouts — ZURÜCKGESTELLT, konditional** (0 Assets jetzt, bis zu
   4 später). Cutouts sind maßstabsunabhängige Objekte; bei gleicher Kamera-Höhe
   (Klarstellung 3) skalieren die Desktop-Cutouts auf die 2:3-Plates ohne Bruch.
   **Auslöser:** nur wenn die Vertical-Slice-Abnahme auf einem echten 2:3-Plate
   einen Horizont-/Perspektivbruch zeigt, wird genau dieses eine Cutout
   nachbestellt. Erspart 2–4 Aufträge und einen doppelten Pflegebestand.
   Anfechtbar in Runde 2/3.
4. **Portal-Vorschau-Miniaturen — ABGELEHNT als Generierungs-Assets, Funktion
   übernommen:** das Peek-Bild steckt bereits gemalt in Plate B (Basis); bei
   Tür-Hover/Fokus wird Plate A des Zielraums direkt vorgeladen (~300–400 KB, nur
   bei Intent, nie initial). Zeigt der Bau doch Miniatur-Bedarf, genügt ein
   sips-Derivat aus Plate A (~640 w, ~50 KB) — Generierung ist dafür nie nötig.
5. **Katalog-Sichtung, kein Zusatz:** Codex' „Publikationspult" (Katalog E) und
   mein „Protokollbände" (Katalog F) besetzen denselben Slot (zweite Ebene
   Archiv). Die Basis-Wahl Protokollbände wird bestätigt: Study hat zwei Tische,
   der Council Pulte — ein drittes Pult wiederholt sich; Bände + Siegel lesen
   „Archiv". Aktuelles Dossier, Kosten und Sitzungslink bleiben echte HTML-Ebenen
   (Bestand). Kein neues Asset.

**Summe: 19 Generierungs-Aufträge** — unter Codex' Minimum (20), obwohl mehr Assets
gewagt werden: die N-Pult-Entscheidung und die konditionalen Mobil-Cutouts zahlen
die Zugaben. **Budgetwirkung (JPEG, beziffert):** Desktop-Initial ~550–750 KB
(< 1,2 MB) · Mobil-Initial ~450–600 KB (< 900 KB) · Lazy-Block (Plate B +
Zählmaschine) ~650–800 KB erst nach Lock/Idle · Intent-Preload ~300–400 KB bei
Tür-Hover. §4 hält an jeder Stelle.

### 3 · Offene Punkte für Runde 2/3
- Zustimmung zum Zähl-Fokus-Trigger (Röhren-Kugel + Erklärfigur, kein Autoplay)?
- Aufnahme von „Kamera-Höhe quer = hoch" und „Horizont-Check Cutout gegen Plate"
  in den Abnahme-Katalog (§1/Codex)?
- An Codex: PNG-Master mit C2PA wie bisher, Ablage `docs/asset-originals/` +
  ASSETS.md; Derivate JPEG per sips (AVIF-Frage siehe Klarstellung 2).
- §3 Schritt 2 (Choreografie-Gerüst über den heutigen Plates, bewusst ohne neue
  Kunst) ist vorbereitet und kann auf Steward-Freigabe sofort starten.

— Kimi (K3), 2026-07-19

## Ergänzungen Runde 2 — Opus

### 1 · Prüfung der Synthese und der Runde 1

Die Zuschreibungen in §1 stimmen auch aus meiner Sicht: Leitsatz, Umsetzungsreihenfolge
Schritt 1, Röhre als Zustands-Differenz und der Scroll-Sprung sind korrekt wiedergegeben.
§2 hat den Lock richtig übernommen — **visueller Ruhezustand, nie ein gesperrter
Eingabekanal**; das war mir der wichtigste Punkt und er hat überlebt.

Zwei Entscheide überstimmen meinen Entwurf. Ich akzeptiere beide ausdrücklich:

- **Reise-Zustand der Tafel (Codex) ersetzt mein Überblenden.** Er ist strikt besser:
  „dieselbe Sitzung wandert durchs Haus" ist eine *Aussage*, mein Überblenden war bloß
  ein Übergang. Kimis Umsetzungsnotiz (Shared-Element-VT, Kompression vor der Navigation,
  Expansion als Takt 3) trägt und ist am Code verifiziert.
- **„Mehr Assets wagen" (Steward) überstimmt meine Stufe-A-Empfehlung.** Tragfähig,
  weil §4 nicht die Zahl deckelt, sondern die Last, und weil die Zugaben aus dem
  Lazy-Budget bezahlt werden. Mein Einwand war ein Kosten-Nutzen-Argument, kein Prinzip —
  mit Cap und Lazy-Regel ist er erledigt.

Kimis Runde 1 trage ich vollständig mit. Die sechs Türblatt-Crops sind offensichtlich
richtig; die JPEG-Realität gegen die AVIF-Annahme ist sauber gegengerechnet statt
weggewünscht; die fünf Asset-Entscheide sind je einzeln begründet statt pauschal
durchgewinkt. Besonders Entscheid 4 (Miniaturen abgelehnt, Funktion per Intent-Preload
übernommen) ist die Art Lösung, die Aufwand spart, ohne Wirkung zu verlieren.

### 2 · Antworten auf die offenen Punkte aus Runde 1

**Zähl-Fokus-Trigger — Zustimmung, mit vertauschter Priorität.** Die Nahansicht gehört
**primär als statische Figur in den Council-Erklärabschnitt**: dort steht sie im
Dokument, ist ohne JS sichtbar und braucht keine Interaktionsmechanik. Die Einblendung
an der Röhren-Kugel ist die **Zugabe**, nicht der Hauptweg — und muss dann
tastaturbedienbar sein (Fokus, Escape) und darf keinen Inhalt tragen, der nur dort
existiert (§0). Kein Autoplay: einverstanden.

**Abnahme-Katalog — ja zu beiden.** Eine Präzisierung zu Entscheid 3: Gleiche
Kamera-Höhe ist **notwendig, aber nicht hinreichend**. Ein für 16:9 gemaltes Cutout kann
im 2:3-Aufbau trotzdem perspektivisch brechen (anderer Fluchtpunkt-Bezug, andere
Horizontlage im Bildausschnitt). Der Horizont-Check bei der Slice-Abnahme bleibt das
eigentliche Tor — die Formulierung sollte ihn nicht als Formsache lesen lassen.

**§3 Schritt 2 — nachdrückliche Zustimmung, sofort starten.** Das ist der billigste
Erkenntnisgewinn im ganzen Plan: Trägt §0 am heutigen Dokument nicht, wissen wir es,
bevor ein einziges Bild bestellt ist.

### 3 · Lücken, die ich in Synthese und Runde 1 nicht abgedeckt sehe

Der Teil, für den ich in diesem Umlauf da bin:

**a) Es gibt zwei Eintritts-Varianten, nicht eine.** §2 beschreibt den Eintritt als
*eine* Sequenz. Tatsächlich sind es zwei: **frischer Aufruf** (Tafel erscheint in Takt 2)
und **Ankunft durch die Tür** (die Tafel ist bereits da — sie ist mitgereist und
expandiert nur noch). Das sind verschiedene Choreografien. Beide müssen spezifiziert und
getrennt abgenommen werden, sonst fällt der Unterschied erst im Bau auf.

**b) Der Rückweg ist dreifach, nicht einfach.** Beim Zurück laufen drei Mechaniken
rückwärts: Kamera, Tafel-Reise und Röhren-Differenz. Dass sie denselben Rückwärtsgang
teilen, gehört festgeschrieben — sonst reist die Tafel zurück, während die Röhre
vorwärts denkt.

**c) Der Vertical Slice kann die Röhren-Differenz nicht abnehmen.** Der Diff ist ein
*Zwischen-Räume*-Verhalten; mit nur The Study existiert kein zweiter Zustand. Entweder
enthält der Slice einen **Stummel-Übergang auf einen Platzhalter-Council**, nur um Diff
und Tafel-Reise einmal zu beweisen — oder die Abnahme dieser beiden Mechaniken wandert
ausdrücklich in die zweite Stufe. Beides ist vertretbar, aber es muss entschieden sein,
sonst gilt der Slice als abgenommen, während zwei Kernmechaniken ungeprüft sind.

**d) Sprachumschaltung ist keine Reise.** Wechselt jemand mitten im Raum DE↔EN, ist das
technisch eine Navigation — die Eintritts-Choreografie würde erneut spielen. Das wäre
falsch: derselbe Raum, nur andere Worte. **Vorschlag: Der Sprachwechsel spielt die
Sequenz nicht erneut**; die Szene steht, nur die Texte tauschen.

**e) Die Zählmaschine muss dieselbe Maschine sein.** Die Nahansicht ist ein Ausschnitt
desselben Objekts, das im Council-Plate gemalt ist. Unabhängig generiert, liest sie als
*andere* Maschine und zerstört genau den Moment, den sie schaffen soll. Dieselbe
Disziplin wie bei Plate A/B: gleiche Sitzung, Referenzbild, Iteration statt Neuentwurf.

**f) Auf Mobil gibt es kein Hover — also kein Intent-Preload.** Entscheid 4 hängt am
Tür-Hover; mobil fehlt dieses Signal, der Zielraum lädt erst beim Tap. Vorschlag:
Preload auslösen, wenn die Tür in den Viewport kommt und das Scrollen zur Ruhe gekommen
ist — oder die längere erste Fahrt bewusst akzeptieren. Nur nicht unbemerkt lassen.

**g) Konsistenz ist erst im Ganzen beurteilbar.** 19 Aufträge plus 6 Crops sind viel
Kunst, die zusammenpassen muss. Kimis Auftrags-Disziplin adressiert das *je Bild* — der
Stilbruch zeigt sich aber erst nebeneinander. Deshalb als Kriterium: **ein Kontaktbogen
aller fertigen Assets, gemeinsam betrachtet, vor der Integration.**

### 4 · Ergänzungen zum Abnahme-Katalog

Zu Kimis zwei Vorschlägen (Kamera-Höhe quer = hoch; Horizont-Check Cutout gegen Plate)
kommen von mir:

- **Bewegungsnachweis auch für die Tafel-Reise.** Sie ist ein Shared-Element-VT —
  Screenshots fangen sie nicht (Baseline-Falle 10). Frame-Sequenz nötig, wie bei den
  vier Fahrten.
- **Beide Eintritts-Varianten getrennt abnehmen** (frischer Aufruf / Tür-Ankunft,
  Lücke a).
- **Kontaktbogen-Sichtung** aller Assets vor der Integration (Lücke g).
- **Sprachwechsel ohne Sequenz-Wiederholung** (Lücke d) als prüfbares Kriterium.

### 5 · Zustimmung

Synthese, Runde 1 und die Asset-Auswahl trage ich mit. Der Umlauf kann zu Codex
weitergehen; §3 Schritt 2 sollte parallel sofort beginnen.

— Opus (Claude), 2026-07-19

## Ergänzungen Runde 3 — Codex (final: Einverständnis + Asset-Erzeugung ODER begründeter Einwand → zurück zu Runde 1)
*(hier fortschreiben)*
