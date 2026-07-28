> **Archiviert 2026-07-28 (CC) — Codex-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# Codex-Auftrag: Prozess-Embleme und Säulenbilder sauber integrieren

Arbeite im bestehenden NobleCause.ai-Repository auf dem aktuellen Branch.

Claude Code hat den Stand inzwischen bereinigt und verändert. **Nichts aus früheren Plänen blind übernehmen.** Untersuche zuerst den tatsächlichen Repositoryzustand, die letzten Änderungen und die aktuell produktive Startseite.

## Verbindlicher Zwei-Phasen-Ablauf

### Phase 1: Recherche und Plan, noch keine Implementierung

Lies mindestens:

- `AGENTS.md`
- `docs/handoff-notes-for-codex.md`
- `docs/codex-analysis.md`
- den aktuellsten Build-/Release-Bericht unter `docs/`
- `site/static/media/ASSETS.md`
- `git status`
- die letzten relevanten Commits und Diffs
- die aktuellen Homepage-Komponenten, Styles und Szenensteuerung
- alle neu unter `docs/` abgelegten Bilddateien

Prüfe insbesondere:

1. Welche Änderungen Claude Code zuletzt vorgenommen hat.
2. Welche Komponenten aktuell die vier Säulen und die sechs Prozessschritte rendern.
3. Welche Assetstruktur und Provenienzregeln jetzt tatsächlich gelten.
4. Welche vier neuen Säulenbilder in `docs/` liegen und welches Bild zu welchem Bereich gehört.
5. Ob es bereits ältere oder doppelte Embleme gibt, die später entfernt werden können.
6. Welche Bildgrößen, Crops und Dateiformate die vorhandene UI wirklich benötigt.
7. Wo die Bildzeichen bei ihrer ersten Erwähnung oben auf der Seite erscheinen müssen, damit die visuelle Sprache sofort erklärt wird.
8. Ob Codex in dieser Umgebung hochwertige Bilder erzeugen kann. **Keine minderwertigen SVG-/CSS-Ersatzbilder bauen.**

Erzeuge danach ausschließlich:

`docs/process-emblems-integration-plan.md`

Der Plan enthält:

- verifizierten Ist-Zustand
- aktuelle betroffene Dateien
- Mapping der vier Säulenbilder aus `docs/`
- vorgeschlagene endgültige Dateinamen und Zielpfade
- Plan für Originale, Webderivate, Hashes und `ASSETS.md`
- genaue visuelle Spezifikation der sechs Prozess-Embleme
- geplante UI-Integration
- geplante Wiederholung der Bildzeichen bei der ersten sprachlichen Erklärung
- Cleanup-Liste
- Test- und Screenshotplan
- klare Aussage, ob Codex die sechs Bilder selbst hochwertig erzeugen kann
- falls nein: sechs endgültige Bildprompts und eine Liste der fehlenden Dateien

**In Phase 1 keine produktiven Dateien, Bilder oder Styles verändern.**  
Danach stoppen und auf meine ausdrückliche Nachricht **`FREIGABE`** warten.

---

## Phase 2: Erst nach `FREIGABE`

Nach der Freigabe den geprüften Plan umsetzen.

# A. Vier Säulenbilder aus `docs/`

Ordne die Bilder nach ihrem Inhalt zu:

1. **Zukunft**  
   Rakete als klares Zukunftszeichen.

2. **Leid lindern**  
   Eine gebende und eine empfangende Hand.

3. **Große Gefahren**  
   Vereinfachter Atompilz.

4. **Was sonst übersehen wird**  
   Steinbogenbrücke mit groß herausfallendem tragendem Stein; ein Auto fährt über die gefährdete Brücke.

Regeln:

- nicht anhand zufälliger aktueller Dateinamen zuordnen, sondern Bildinhalt prüfen
- semantisch und konsistent umbenennen
- in die vorhandene produktive Assetstruktur unter `site/static/media/` einordnen
- bestehende Konventionen des Repositories respektieren
- Originalbytes und Provenienz dokumentieren
- SHA-256, Maße, Größe, Quelle und Derivate in `site/static/media/ASSETS.md`
- Arbeitskopien unter `docs/` erst nach erfolgreicher Prüfung entfernen
- alte, eindeutig unreferenzierte Säulenbilder nach Prüfung entfernen

Empfohlene semantische Namen, sofern sie zur aktuellen Konvention passen:

- `pillar-future`
- `pillar-relieve-suffering`
- `pillar-major-risks`
- `pillar-overlooked`

# B. Sechs Prozess-Embleme

Alle sechs Embleme gehören sichtbar zur bestehenden Ratssaalwelt:

- Messingrelief auf sehr dunklem Stein oder Schiefer
- matt, ernst, kein Hochglanz
- warmes Bernsteinlicht gegen kaltes Dunkel
- quadratisch
- kein Text und keine Buchstaben
- ein starkes Hauptmotiv
- bei ungefähr 32 px noch eindeutig erkennbar
- keine komplexe Miniaturszene
- stilistisch untereinander konsistent

## 1. Frage

**Motiv:** Feder über einem leeren Blatt, darauf ein deutliches eingraviertes Fragezeichen.

Bedeutung: Die Frage wird bewusst und präzise formuliert.

## 2. Belege sammeln

**Motiv:** Lupe über wenigen sauber geordneten Dokumenten.

Bedeutung: Belege werden gesammelt und geprüft.

Nicht als chaotischer Papierstapel darstellen.

## 3. Drei Antworten

**Motiv:** Drei beleuchtete Pulte in klarer Dreiecksordnung, auf jedem genau ein Blatt.

Bedeutung: Drei getrennte und gleichwertige Antworten.

Regeln:

- stark vereinfachen
- keine Personen nötig
- die Dreizahl muss auch klein klar bleiben
- wenn der erste Entwurf bei 32 px nicht eindeutig ist, eine zweite reduzierte Variante erzeugen und vergleichen

## 4. Gegenlesen und Umdenken

**Motiv:** Seitliches Kopfprofil oder stilisiertes Gehirn mit einem klaren Wendepfeil beziehungsweise einer sichtbar geänderten Gedankenbahn.

Bedeutung: Die Modelle lesen die anderen Antworten, wägen neu ab und dürfen ihre Meinung ändern.

Regeln:

- kein Buch, keine Dokumente, damit es nicht mit „Belege“ verwechselt wird
- nicht medizinisch oder anatomisch
- keine Chatblasen
- der Richtungswechsel muss der klare Sinnträger sein

## 5. Zählen

**Motiv:** Die tatsächliche mechanische Zählmaschine aus den bestehenden Ratssaal-/Maschinenszenen, als stark vereinfachtes Emblem.

Bedeutung: Ein Programm zählt nur die Nennungen.

Regeln:

- kein generischer Abakus
- vorhandene Maschine als visuelle Referenz verwenden
- erkennbare Trommeln/Zählwerk und drei Zuflüsse oder Marken
- keine Intelligenz, kein Gesicht, niemand bedient sie

## 6. Veröffentlichen

**Motiv:** Offenes offizielles Protokoll oder ausgerollte Schriftrolle mit deutlich erkennbarem Siegel.

Bedeutung: Das Ergebnis wird protokolliert und öffentlich gemacht.

Nicht wie ein privater Brief darstellen.

## Bildgenerierung

Falls hochwertige Bildgenerierung verfügbar ist:

- alle sechs Embleme selbst erzeugen
- mindestens eine hochauflösende Originalfassung pro Motiv
- vor Integration jedes Motiv testweise auf 32 px verkleinern
- schwache oder verwechselbare Motive neu erzeugen
- keine provisorischen Platzhalter integrieren

Falls keine hochwertige Bildgenerierung verfügbar ist:

- nicht improvisieren
- nach Phase 1 stoppen
- die sechs finalen Prompts im Plan ausgeben
- auf die von mir gelieferten Bilder warten

# C. Visuelle Sprache auf der Seite erklären

Auf der obersten Ebene keine unerklärte Protokollsprache verwenden.

Nicht ohne Übersetzung:

- „Säule A“
- „Dissens“
- „Evidenz“
- ähnliche interne Begriffe

Stattdessen zuerst Alltagssprache:

- **Zukunft**
- **Leid lindern**
- **Große Gefahren**
- **Was sonst übersehen wird**
- **noch keine Einigkeit**
- **Belege**

Die vier Säulenzeichen müssen bereits bei ihrer ersten sprachlichen Erwähnung sichtbar danebenstehen. Dasselbe gilt für die sechs Prozesszeichen bei der ersten Erklärung des Ablaufs.

Damit entsteht eine konsistente Bildwiedererkennung über:

- Einführung
- Empfehlungsregister
- Prozessnavigation
- Szenenzustände
- Archiv- und Sitzungsansichten, wo passend

Die Bilder erklären Begriffe, ersetzen aber nicht zugänglichen Text.

# D. Integration

- bisherige Buchstaben-Medaillons A–D durch die vier neuen Säulenbilder ersetzen
- bisherige Nummernkreise beziehungsweise generische Prozesssymbole durch die sechs neuen Prozessbilder ersetzen
- Bildzeichen in der ersten Erklärung oben auf der Seite ergänzen
- vorhandene Datenlogik nicht verändern
- keine fachlichen Inhalte erfinden
- Alt-Texte und zugängliche Namen aus dem sichtbaren Begriff ableiten
- Bilder dürfen nicht wie fremde Kacheln wirken
- Zuschnitt, Rahmen, Vignette und Licht an die gemalte Bühne anpassen
- aktive Prozesszustände über Licht/Rahmen markieren, nicht durch Austausch des Motivs
- mobile Fassung bewusst komponieren und nicht nur verkleinern

# E. Cleanup

Nach erfolgreicher Integration:

- doppelte und unreferenzierte alte Embleme entfernen
- tote Imports und alte CSS-Platzhalter entfernen
- keine geschützten Datenpfade verändern:
  - `sessions/**`
  - `journal/**`
  - `schedule.json`
  - `gremium/**`
  - `schema/**`
  - `prompts.py`
- keinen zweiten Prototyp oder Buildpfad anlegen
- `sol-build/` als historische Referenz belassen, sofern die aktuellen Repo-Regeln nichts anderes sagen

# F. Prüfung

Mindestens:

```bash
cd site
npm ci
npm test
npm run build
npm run preview
```

Prüfe die produktive Ausgabe aus `site/build/`.

Viewports:

- 1440 × 900
- 1024 × 768
- 390 × 844
- 320 × 700

Zusätzlich:

- 32-px-Lesbarkeit aller zehn Embleme
- 200-%-Zoom
- No-JS
- Reduced Motion
- Tastatur
- Hash-Navigation und Browser-Zurück
- keine horizontalen Überläufe
- keine gebrochenen Bildpfade
- keine unnötigen Mehrfachdownloads
- alle internen und externen Links

Erzeuge finale Screenshots unter:

`docs/review/final-emblems/`

Mindestens:

- Desktop Ankunft
- Desktop Empfehlungen
- Desktop Prozessnavigation
- Desktop Vorzimmer
- Desktop Zählung
- Mobile Einführung
- Mobile Empfehlungen
- Mobile Prozessnavigation
- 32-px-Vergleich aller Embleme

# G. Abschlussbericht

Aktualisiere oder erzeuge:

`docs/codex-emblems-integration-report.md`

Inhalt:

1. recherchierter Ausgangszustand
2. freigegebener Plan
3. erzeugte beziehungsweise übernommene Bilder
4. altes → neues Dateinamen-Mapping
5. endgültige Zielpfade
6. 32-px-Lesbarkeitstest
7. UI-Integration
8. sprachliche Übersetzungen auf der obersten Ebene
9. entfernte Altdateien
10. ausgeführte Befehle und Exit-Codes
11. Test- und Buildresultate
12. geprüfte Viewports
13. verbleibende Risiken
14. Status:
   - `READY FOR REVIEW`
   - `READY FOR MERGE`
   - oder `NOT READY`

Kein Merge und kein Deployment ohne separate Freigabe.
