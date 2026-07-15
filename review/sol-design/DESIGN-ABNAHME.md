# Design-Abnahme — SOL-Build (PR #12)

Reine **Gestaltungs-/UX-Abnahme** des nachgebesserten Builds. Substanz, Daten,
Barrierefreiheit (AA+), no-JS, Datenschutz und die jargonfreie Antwortebene sind
**bereits geprüft und tragen** — hier nicht erneut bewertet. Grundlage: visuelle
Begutachtung im Browser (Desktop 1456 px, alle Sektionen gescrollt, Protokoll-Reiter
1+2 geöffnet). **Kein Merge, kein Deploy, keine Build-Änderung** — nur Befund.

## Urteil: **BEDINGT ABGENOMMEN**
Die Gestaltung trägt: die Licht-Metapher (helle Antwort im dunklen Saal), das
Stepper-Band, der begehbare Saal und die Kreide-Grammatik der Revision sind stimmig und
konsistent. Vor der finalen Freigabe sind **drei P1-Nachbesserungen** und einige
kleinere Feinschliffe fällig; ein Kartenzustand ist mit passender Sitzung gegenzuprüfen.

---

## Befunde je Leitfrage

### 1. Hero — 30-Sekunden-Regel, Licht, Kartenhierarchie
- ✅ **Licht trägt.** Die führende „lit-floor" (LEEP) glüht messingfarben/radial gegen
  den dunklen Saal — Antwort hell, Szene dunkel. Die Szene konkurriert nicht.
- ⚠️ **Die Empfehlung gewinnt aber NICHT den ersten Blick.** Über ihr stehen jetzt drei
  Textblöcke: das neue `<h1>` (großer Serif-Seitentitel „Öffentliche Beratung, wohin
  Spenden am wirksamsten fließen"), die Kontextzeile und die Trust-Zeile. Der Erstblick
  landet auf der **Tagline**, nicht auf LEEP / „Hier direkt spenden". Das schwächt die
  30-Sekunden-Regel. (Nebeneffekt der F6-Nachbesserung — echtes `<h1>` war a11y-richtig,
  hat aber Gewicht über die Empfehlung gelegt.)
- ✅ Die führende Karte (D/LEEP) trägt einen Messing-Fokusrahmen — das Hierarchie-Signal
  im Vierer-Grid ist vorhanden.
- ⚠️ **Karten-Höhen stark ungleich:** Karte A (Vorbehalts-Box **plus** Revision) ist rund
  doppelt so hoch wie B/C/D und überstrahlt die fokussierte Karte D optisch (siehe 4/5).

### 2. Stepper-Band — ✅ harmoniert
Nummerierte Messing-Knoten auf einer Verbindungslinie, Serif-Überschrift, transparent
auf dem dunklen Feld. Kein fremdes UI-Panel, sondern integrierte Typografie im Duktus
der Seite. **Keine Nachbesserung.**

### 3. Ratssaal als begehbare Kür — ✅ überwiegend gut
Glühende Messing-Hotspots (Claude Opus / GPT / Gemini / zentrale Zählmaschine mit
Zahnrädern / Tür), Metapher durch die Einleitung klar erklärt („Jedes Pult = eine
Antwort, die Maschine zählt nur"). Der Saal liegt **unter** dem Primärpfad und hält den
Spender nicht auf. Der Vorraum („Späher und Wart") ist stimmungsvoll komponiert.
- ◦ **Kleiner Feinschliff:** die Hotspots sind auf dem großen Bild recht klein/subtil —
  Erstbesucher erkennen die Klickbarkeit evtl. spät. Etwas stärkere Affordanz (dezenter
  Puls oder Rahmen beim Hover/Fokus) würde einladen, ohne aufdringlich zu werden. Optional.

### 4. Drei Kartenzustände — teils geprüft
- ✅ *Einig* (B/C/D „Empfehlung") und *einig mit Vorbehalt* (A „Einigkeit mit Vorbehalt")
  teilen dieselbe Kartenform; der Vorbehalt ist eine neutrale, gerahmte Box — **kein
  Fehlerfall-Look** (kein Rot, kein Warnsymbol). Gut.
- ⚠️ *Mit Vorbehalt* trägt jedoch spürbar **mehr Gewicht** (Box + Revision → doppelte
  Höhe) als schlichte Einigkeit — mild ungleich; hängt an der Kartenhöhe (siehe 1/5).
- ◦ **In Sitzung 3 nicht prüfbar:** alle vier Säulen sind einig; der Zustand *keine
  Einigung* (split-votes) kommt hier nicht vor. Laut Markup nutzt er dieselbe
  `recommendation-card`-Hülle (gut). **Empfehlung:** vor der finalen Freigabe mit einer
  Nicht-Konsens-Sitzung (z. B. 2026-07, Säule A) visuell gegenprüfen, ob er gleichwertig
  wirkt und nicht wie ein leerer/kaputter Zustand.

### 5. Kreide-Grammatik der Revision — ✅ konsistent
Karte **und** Protokoll sprechen dieselbe Sprache: „before" handschriftlich
durchgestrichen (Bradley Hand), „after" fett. Auf Tafel und im Protokoll liest sich das
als eine Grammatik.
- ⚠️ **Redundanz im Protokoll:** die neue Org erscheint **doppelt** — als fettes `<ins>`
  (mit „nach dem Gegenlesen geändert") **und** direkt darunter nochmals als
  Zeilen-Überschrift. Eine davon streichen.
- ⚠️ **Revision in Karte A doppelt gelistet** — einmal je Modell identisch gestapelt
  („TaRL Africa → HKI (GPT)" und „TaRL Africa → HKI (Gemini Pro)"). Zusammenfassen zu
  „GPT & Gemini Pro: TaRL Africa → Helen Keller International".
- ◦ Die Kreide-Durchstreichung ist sehr **blass/klein** — Legibilität leicht anheben.

### Zusätzlicher Gestaltungsfund (Rendering-Polish)
Der verbatim gerenderte `dissent_md` zeigt **literale `**`-Markdown-Sternchen**
(„**Claude Opus:** **Säule A — …"). `build.py` escaped den Text, rendert aber kein
Markdown → die Formatierung wirkt **kaputt**. Das ist Gestaltung, nicht Sprache/Substanz.
**Nachbesserung:** `dissent_md` als Markdown rendern (oder die `**` entfernen), damit
keine rohen Sternchen erscheinen.

---

## Priorisierte Gestaltungs-Nachbesserungen
**P1 — vor finaler Freigabe**
1. **Hero-Hierarchie / 30-Sek-Regel:** Intro verschlanken, damit die lit-floor + Spenden-
   Button den Erstblick gewinnen (kürzeres/kleineres `<h1>`, näher an die Marke; ggf.
   Kontext-/Trust-Zeile straffen oder die lit-floor höher/prominenter).
2. **Rohe `**`-Sternchen** im Dissens-Text beheben (Markdown rendern statt escapen).
3. **Revision entdoppeln** — Protokoll (Org nur einmal) und Karte (Modelle
   zusammenfassen); reduziert zugleich die Überhöhe von Karte A.

**P2 — Feinschliff**
4. **Kartenhöhen angleichen** (Vorbehalts-/Revisions-Karten nicht doppelt so hoch wie
   schlichte Einigkeit), damit die fokussierte Karte D die stärkste bleibt.
5. **Kreide-Durchstreichung** legibler (etwas kräftiger/größer).

**P3 — optional**
6. **Hotspot-Affordanz** im Saal (dezenter Puls/Rahmen), damit die Klickbarkeit früher
   lesbar ist.

**Gegenprüfung (Daten, nicht Gestaltung):** *keine-Einigung*-Kartenzustand mit einer
Nicht-Konsens-Sitzung visuell bestätigen.

## Nicht Gegenstand dieser Abnahme
WCAG-Kontrast (AA+ geprüft), no-JS-Fallback (belegt), Datenschutz (0 Tracker),
Datenkorrektheit (echte Sitzung 3), Fachsprache auf der Antwortebene (jargonfrei).
Die Fachvokabular-Sichtbarkeit im **verbatim** Protokoll-/Dissens-Text ist publizierter
Text (Content-Kaskade), kein Gestaltungsfehler.

## Empfehlung
Nach den drei P1-Punkten + Gegenprüfung des Nicht-Konsens-Zustands ist der Build aus
Design-Sicht freigabereif. Umsetzung ist ein eigener Auftrag (nicht Teil dieser Abnahme).
