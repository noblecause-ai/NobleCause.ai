# Konzept + Auftrag — §6 Echter Türdurchgang, §7 Sitze um die Zählmaschine

**Von:** Opus 5 (Architekt) · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Vorlauf:** Runde B erledigt (`a9ec155`, `00b0d1c`, `3fd11e2`, `72c78d5`).
**Arbeitsweise:** Plan → Freigabe → Bau → Browser-Verifikation → Bericht.
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

Beide Teile stehen in **einem** Dokument, weil sie sich eine Ebene und eine Tiefenlogik teilen.
Gebaut wird trotzdem nacheinander: erst §6, dann §7 auf dem, was §6 hinterlässt.

---

## 0 · Zur Referenz

Die Vorlage (`motionsites.ai/?prompt=dreamcore-landing`) ließ sich nur als Standbild sichten —
die Vorschau hinter dem Modal ist ein Bild, die Bewegung liegt hinter der Paywall. Das Prinzip
ist am Standbild aber eindeutig ablesbar und deckt sich mit Afschins Beschreibung: **eine Öffnung
in einer nahen Ebene, dahinter eine ferne Ebene, und die Kamera fährt hindurch.** Die Öffnung
wächst über den Bildrand hinaus, die Ferne wächst kaum — danach ist man drin.

Das ist kein 3D-Effekt, sondern **Parallaxe mit korrekter Perspektive**: nahe Ebenen wachsen
schnell, ferne langsam. Genau das leistet `perspective` + `translateZ` im Browser von selbst,
sobald man **die Kamera** bewegt statt der Ebenen.

---

# §6 · Der echte Türdurchgang

## 6.1 Der Kern

Eine **Übergangsebene**, die beim **Klick** entsteht und nach der Fahrt wieder verschwindet.
`position: fixed; inset: 0`, eigener Stacking-Kontext, `pointer-events: none`, über allem.

Darin ein Kamerawagen und drei Ebenen im Tiefenraum:

| Ebene | Tiefe | Inhalt |
|---|---|---|
| **nah** | `z = 0` | P7 — die Wand des Ausgangsraums, mit **Loch** an der Türstelle (Alpha) |
| **mitte** | `z ≈ −200` | P8 — die beiden Türflügel, gekeyt (das Asset aus Runde B) |
| **fern** | `z ≈ −1400` | das **Plate des Zielraums** |

Der Elternknoten trägt `perspective`. Jede Ebene wird mit `(P + D) / P` gegenskaliert, damit sie
im Ruhezustand **exakt so aussieht wie heute** — die Tiefe ist zu Beginn unsichtbar. Animiert
wird dann **nur eine einzige Größe:** `translateZ` des Kamerawagens, von 0 nach vorn. Die nahe
Wand wächst schnell und schiebt sich am Betrachter vorbei, der Zielraum wächst kaum. Kein
Rechnen pro Ebene, keine Skalierungs-Keyframes, keine Bibliothek.

**Das ist der ganze Trick.** Er ist deshalb billig, weil der Browser die Perspektivteilung macht.

## 6.2 Der Takt

Drei Schläge, überlappend, zusammen ≈ 1,25 s:

1. **Flügel öffnen** (0 → 0,45 s) — P8 spreizt zur Laibung, leichte Perspektivneigung.
   Dieselbe Geste wie das statische Auf-Plate aus §3, nur jetzt bewegt.
2. **Fahrt** (0,25 → 1,15 s) — Kamera nach vorn. Beginnt, während die Flügel noch aufgehen;
   getrennte Schläge lesen zäh.
3. **Schwelle** (0,9 → 1,25 s) — kurzer warmer Bloom an der Laibung im Moment des Durchtritts,
   dazu ein leichter Blur-Anstieg **auf der nahen Ebene**, während sie am Rand vorbeizieht.

Der Bloom und der Blur sind nicht Zierrat: sie kaschieren, dass die ferne Ebene ein flaches Bild
ist, das man aus zu geringer Distanz sieht. **Ohne sie liest die Fahrt als Zoom in eine Tapete.**

Kurve: langsam anlaufend, spät beschleunigend (`cubic-bezier(.5,0,.75,.4)`), **nicht** ausklingend.
Eine Kamera, die vor der Tür abbremst, liest wie ein Fehler.

## 6.3 Die einzige harte Anforderung: der Übergabemoment

Das **letzte Bild der Fahrt** und das **erste Bild des Zielraums** müssen deckungsgleich sein.
Ist der Zielraum am Ende der Fahrt bei Skalierung 1,0 und in Ruheposition, ist die Übergabe
unsichtbar. Weicht er ab, springt es — und der ganze Effekt ist verloren.

Daraus folgt zwingend:

- **Vor dem ersten Frame:** Zielroute prefetchen **und** das Ziel-Plate `img.decode()`.
  Erst dann startet die Fahrt. Wartedeckel **300 ms**, danach startet sie ohnehin (lieber ein
  kurzes Nachladen als ein hängender Klick).
- **Die ferne Ebene ist dasselbe Bild in derselben Ausschnittslogik** wie das Ziel-Plate im
  Zielraum (`cover`, gleicher Fokuspunkt). Nicht „ein Bild vom Zielraum", sondern **das** Bild.
- **View Transitions während der Fahrt aus.** Die Übergangsebene *ist* der Übergang.
- Am Ende: Navigation abgeschlossen, Zielraum steht, **dann** Ebene abbauen — nicht umgekehrt.
- Die Eintrittschoreografie des Zielraums (`stage-armed`/`stage-play`) läuft **nach** der
  Übergabe an, nicht während der Fahrt. Sonst fahren die Möbel während der Kamerafahrt ein.

## 6.4 Ruhezustand und Anschluss an §3

Im Ruhezustand bleibt alles wie heute: das statische Auf-Plate beim Hover, der Türhotspot, die
Portalblende als Fallback. Die Übergangsebene entsteht erst beim Klick.

Der Wechsel vom „warmen Tiefe"-Hintergrund des Auf-Plates auf das echte Ziel-Plate wird in den
ersten **200 ms** übergeblendet — zu diesem Zeitpunkt ist die Öffnung noch klein und das Auge
folgt der Bewegung. Ein harter Schnitt an dieser Stelle ist sichtbar, eine kurze Blende nicht.

## 6.5 §0-Verfassung

- **Kein JS:** normaler Link, normale Navigation. Die Ebene existiert nicht.
- **`prefers-reduced-motion`:** keine Fahrt, harter Schnitt zum Zielraum.
- Die Ebene **erzeugt und versteckt nichts** — sie liegt über einer Navigation, die ohnehin
  stattfindet. Sie verzögert um ≈ 1,25 s; das ist ihre einzige Wirkung auf den Inhalt.
- **Nur Desktop ≥ 1200 px**, wie der Türhotspot. Mobil bleibt unverändert.

## 6.6 Umfang: erst ein Durchgang, nicht drei

**Phase 1 ist ausschließlich Archiv → Study.** Nur dort liegen P7 (Wand mit Loch) und der
gekeyte P8-Flügel vor. Study und Council haben ihre Türen gemalt im Plate — dort ist der
Durchgang ohne die gleiche Bestellung nicht baubar.

**Trägt Phase 1, bestelle ich P7/P8 für Study und Council nach** (dieselben zwei Prompts,
anderer Raum). Bis dahin laufen die beiden anderen Türen unverändert mit der Blende. Ein Raum
mit echtem Durchgang und zwei mit Blende ist für die Dauer einer Bestellung vertretbar.

**Kein WebGL, kein Three.js.** Falls sich beim Bau zeigt, dass es ohne nicht geht: abbrechen und
berichten, nicht ausweichen.

## 6.7 Abnahme

- Übergabe ohne sichtbaren Sprung (Frame vor/nach der Navigation vergleichen).
- Außerhalb der Türkontur keine Bewegung, bis die Fahrt beginnt.
- Kein Layout-Shift, keine Scrollbar, kein Flackern beim Abbau der Ebene.
- Nur `transform`, `opacity`, `filter` — nichts, was Layout auslöst.
- 60 fps auf dem Entwicklungsgerät; wenn nicht, Ursache benennen statt Dauer verkürzen.
- Doppelklick, Klick während der Fahrt, Zurück-Taste mitten in der Fahrt: kein hängender Zustand.
- reduced-motion und No-JS geprüft.

---

# §7 · Die Sitze um die Zählmaschine

**Erst bauen, wenn §6 steht.** Was §7 braucht, entsteht in §6.

## 7.1 Was umkreist

Vorschlag: **die drei Modell-Embleme** — die runden Messingmedaillons, die es bereits gibt.

Begründung: Runde Objekte sind **richtungslos** und damit als Billboard ehrlich; ein Stuhl,
der auf der Rückseite der Ellipse steht, müsste seine Rückseite zeigen, und ein frontaler Stuhl
an dieser Stelle ist ein sichtbarer Fehler. Runde Medaillons haben das Problem nicht — und sie
sind inhaltlich das Richtige: **drei Stimmen kreisen um die Zählung.** Die Vorlage arbeitet
ebenfalls mit Kreisen. Kein neues Asset nötig.

**Alternative, falls du wirklich Sitzmöbel willst:** zwei Ansichten pro Sitz bestellen (Vorder-
und Rückansicht auf Magenta), Umschlag an den Scheiteln der Ellipse. Machbar, aber eine
Bestellung und ein sichtbarer Umschlagmoment. **Steward entscheidet.**

## 7.2 Bewegung

Eine **Billboard-Ellipse** um die Zählmaschine: Winkel θ pro Objekt, `x = cx + a·cos θ`,
`y = cy + b·sin θ`, b deutlich kleiner als a (flache Ellipse, Aufsicht von leicht oben).

Aus θ folgt die **Tiefe** `d = (sin θ + 1) / 2`, und aus d alles Weitere:

- Skalierung ≈ 0,62 → 1,0
- Helligkeit und ein Hauch Blur nach hinten
- **`z-index`**, damit die Hälfte hinter der Zählmaschine **wirklich dahinter** liegt

Genau diese Ableitung d → Skalierung/Helligkeit/Stapelung ist die **Tiefenlogik, die §6
hinterlässt.** Sie wird einmal geschrieben und zweimal benutzt — nicht zweimal geschrieben.

## 7.3 Der Einflug

Nach dem Eintrittstakt des Ratssaals (die Pulte stehen), fliegen die drei Objekte von **außerhalb
des Bildrands** ein und **setzen sich** auf ihre Bahnpunkte — Ankunft mit leichtem Überschwingen,
dann geht die Bahn ins ruhige Kreisen über. Das ist die Geste aus der Vorlage.

**Kein Blinken, kein Puls, kein Aufleuchten beim Ankommen.** Die Räume arbeiten mit Gleiten und
Licht, nicht mit Effekten.

## 7.4 Ruhe und Rückzug

Das Kreisen läuft **nur im Ruhezustand** (Hero-Band, kein Scroll). Auf `--retreat` weitet sich
die Ellipse und die Objekte weichen an die Ränder — dieselbe Scrub wie bei allen anderen
Bühnenelementen, kein zweiter Mechanismus.

Eine Umdrehung **langsam** — Richtwert 40–60 s. Alles Schnellere zieht Aufmerksamkeit von der
Tafel ab, und die Tafel ist der Zweck der Seite.

## 7.5 §0-Verfassung

Ruhepositionen stehen im prärenderten HTML. `prefers-reduced-motion` und No-JS: die Objekte
stehen still an ihren Bahnpunkten, kein Einflug, kein Kreisen. Eine rAF-Schleife, die bei
`hidden`/außerhalb des Viewports pausiert — nicht drei Schleifen.

## 7.6 Abnahme

Objekte hinter der Maschine liegen sichtbar dahinter; kein Flackern der Stapelreihenfolge an den
Scheiteln; kein Overflow, keine Scrollbar; die Tafel bleibt frei; CPU im Ruhezustand niedrig
(eine Schleife, pausiert außer Sicht); reduced-motion und No-JS geprüft.

---

## Reihenfolge

1. **§6 Phase 1** — Archiv → Study. Bericht mit Frames vor/nach der Übergabe.
2. **Entscheid**: trägt es? Dann Bestellung P7/P8 für Study und Council.
3. **§7** auf der Tiefenlogik aus §6.
4. Danach: **Protokollseiten** — die letzte große Designlücke vor Go-Live.

Unverändert offen und nicht Teil dieser Runden: der gebündelte **Medien-Strang**.
