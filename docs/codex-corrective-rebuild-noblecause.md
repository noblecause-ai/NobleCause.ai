# Korrekturauftrag an Codex
## NobleCause.ai · Die Bühne ist das Produkt

**Ziel:** Die aktuelle Startseite visuell und interaktiv grundlegend neu bauen, ohne die bereits funktionierende Datenlogik zu verlieren.

**Produktiver Pfad:** `site/`  
**Build-Ausgabe:** `site/build/`  
**Arbeitszweig:** aktueller Branch `feat/immersive-homepage`

---

## 0. Lies dies als Korrektur, nicht als Detailrunde

Die aktuelle Implementierung ist technisch brauchbar, gestalterisch aber abgelehnt.

Sie hat erneut genau den Fehler produziert, den der Neuansatz vermeiden sollte:

- eine normale lange Scrollseite,
- große Textflächen und Dokumentkarten,
- helle Empfehlungskarten, die die Bildwelt überdecken,
- drei vollständige Modellspalten als eigene Inhaltssektion,
- das Vorzimmer als weiter unten liegendes Bild statt als betretener Raum,
- keine sichtbare Türöffnung,
- keine glaubhafte Kameraführung,
- die Zählmaschine ist nicht das Zentrum der Dramaturgie,
- die bestehende Ratssaal-Plate dient überwiegend als dunkler Hintergrund,
- die restlichen Routen wirken weiterhin wie eine andere Website.

Das ist kein Auftrag, diese Seite kosmetisch zu verbessern.

> **Baue die Präsentationsschicht der Startseite kontrolliert neu.**

Die bereits korrekte Datenarbeit soll möglichst erhalten bleiben.

---

# 1. Referenzhierarchie

Bei Konflikten gilt diese Reihenfolge:

1. **Das angehängte Ziel-Mockup** ist der verbindliche visuelle Vertrag.
2. Die vorhandenen Ratssaal- und Vorzimmer-Plates bestimmen Licht, Materialität und Raum.
3. Die publizierten Sitzungs- und Registrydaten bestimmen jede fachliche Aussage.
4. Die bestehende View-Model-, Registry-, Konsens-, Dissens- und Revisionslogik soll erhalten bleiben.
5. Frühere textliche Architekturvorgaben dürfen verworfen werden, wenn sie wieder zu einer linearen Dokumentseite führen.

Das Ziel-Mockup zeigt die entscheidende Komposition:

- Empfehlungen links,
- Vorzimmer links unten,
- Ratssaal als dominante Hauptfläche,
- drei Pulte und Zählmaschine sichtbar,
- Ablauf als integriertes Band unten,
- Archiv rechts,
- kurze Mechanismuserklärung oben,
- alles wirkt wie **ein einziges Instrument**, nicht wie gestapelte Sektionen.

Die aktuellen Screenshots sind negative Referenzen. Kopiere ihre Layoutlogik nicht.

---

# 2. Zielgruppe

Die frühere Persona „eine 80-Jährige muss alles in 30 Sekunden verstehen“ ist als Designsteuerung aufgehoben.

Barrierefreiheit, Klarheit und direkte Spendenlinks bleiben Qualitätsanforderungen. Sie sind aber nicht mehr die kreative Persona.

Die Kernzielgruppe ist:

> Ein digital offener, kritischer Spender, der KI nicht blind vertraut, aber bereit ist, ein transparentes Verfahren zu prüfen und sich von einer ungewöhnlichen, ernsthaften Inszenierung führen zu lassen.

Die Seite darf neugierig machen, Atmosphäre aufbauen und eine Mechanik erlebbar machen.

Sie darf nicht wie eine Seniorenbroschüre, Verwaltungsseite oder Standard-Charity-Landingpage wirken.

---

# 3. Was aus dem aktuellen Build erhalten bleibt

Erhalte, soweit fachlich korrekt und technisch sinnvoll:

- Datenladen aus den echten Sitzungen,
- Registryauflösung über `organization_id`,
- Spendenlinks ausschließlich aus `organizations.json`,
- Konsens- und Nicht-Konsenslogik,
- Vorbehalte,
- Revisionsvergleich zwischen Erst- und Schlussvotum,
- Korrekturhinweise,
- Kosten,
- bestehende Datentests,
- produktive Integration unter `site/`,
- Adapter-static-Build,
- bestehende Sitzungs- und Archivdaten.

Ändere diese Logik nur, wenn ein nachweislicher Fehler vorliegt.

---

# 4. Was neu gebaut werden muss

Ersetze die aktuelle visuelle Homepage-Komposition vollständig:

- große Introkarte,
- vier riesige helle Empfehlungskarten,
- lange unabhängige Inhaltssektionen,
- drei seitenhohe Modellspalten,
- rechte Sprungnavigation als gewöhnliches Inhaltsverzeichnis,
- Vorzimmer als spätes Banner,
- Szenencontroller, sofern er nur aktive Scrollsektionen markiert,
- Home-CSS, sofern es die aktuelle Dokumentstruktur erzwingt.

Die Datenkomponenten dürfen intern weiterverwendet werden. Ihre sichtbare Form wird neu komponiert.

---

# 5. Der verbindliche Desktop-Aufbau

## Eine Bühne, ein Viewport, mehrere Zustände

Auf Desktop besteht die Startseite aus einer **viewportfüllenden, sticky Bühne**.

Die Seite darf einen längeren Scrollweg besitzen, aber der Besucher sieht nicht nacheinander autonome Seitenabschnitte. Er sieht dieselbe Komposition, die sich verwandelt.

Die Hauptstruktur ist ungefähr:

```text
┌──────────────────┬────────────────────────────────────┬────────────────┐
│ EMPFEHLUNGEN     │                                    │ ARCHIV         │
│ kompakte Register│             RATSSAAL               │ Sitzungen      │
│                  │                                    │ monumentale Tür│
│                  │  drei Pulte      Zählmaschine      │                │
├──────────────────┤                                    │                │
│ VORZIMMER        │                                    │                │
│ Späher + Wart    │                                    │                │
├──────────────────┴────────────────────────────────────┴────────────────┤
│ FRAGE · BELEGE · ANTWORTEN · UMDENKEN · ZÄHLEN · VERÖFFENTLICHEN     │
└───────────────────────────────────────────────────────────────────────┘
```

Dies ist keine starre Pixelvorgabe, aber die räumliche Logik ist verbindlich.

## Flächenverhältnis

Bei einem Desktop-Viewport um 1440 × 900:

- der Ratssaal ist die dominante Fläche,
- mindestens etwa 60 bis 70 Prozent der zentralen Bühne bleiben als Bildraum wahrnehmbar,
- keine helle oder opake Textfläche darf den Saal großflächig überdecken,
- keine einzelne Textkarte soll mehr als ungefähr ein Fünftel des Viewports einnehmen,
- die Zählmaschine muss in den Zuständen `arrival`, `recommendations` und `count` sichtbar bleiben,
- die drei Pulte müssen im Zustand `initial` gleichzeitig sichtbar sein.

## Linke Zone

Oben:

- vier kompakte Empfehlungsregister,
- jeweils Säule, Organisation, Stimmenzahl und ruhiger direkter Link,
- Vorbehalt als kurze Zeile,
- bei Nicht-Konsens gleichwertige Mini-Einträge statt großer Karten.

Unten:

- ein dauerhaft erkennbares Fenster zum Vorzimmer,
- Späher und Wart sichtbar,
- beim Belegzustand wird dieses Fenster zum Portal und übernimmt die Hauptfläche.

## Mitte

- Ratssaal-Plate als echte Hauptbühne,
- drei Pulte räumlich markiert,
- Zählmaschine im Zentrum,
- nur kurze, an die Szene gebundene Texte,
- keine langen Protokollblöcke.

## Rechte Zone

- monumentale Tür und Sitzungsarchiv,
- kompakte Register früherer Sitzungen,
- Uneinigkeit gleichwertig dargestellt,
- die Tür ist ein tatsächlicher Szenenanker, nicht nur ein Bild.

## Unteres Band

Sechs Stationen:

1. Frage
2. Belege sammeln
3. Drei Antworten
4. Gegenlesen und umdenken
5. Zählen
6. Veröffentlichen

Das Band ist Bestandteil der Raummechanik. Es darf nicht wie sechs SaaS-Featurekarten aussehen.

Geeignete Form:

- gravierte Messingsegmente,
- mechanische Laufbahn,
- kleine Symbole,
- aktive Station durch Licht, nicht durch eine gewöhnliche Tabfarbe.

---

# 6. Textbudget

Die Startseite erklärt, aber sie veröffentlicht nicht das gesamte Protokoll in voller Länge.

Pro Szenenzustand maximal:

- eine Überschrift,
- zwei kurze Sätze,
- eine primäre Aktion,
- wenige Datenlabels.

Das vollständige Protokoll liegt auf der Sitzungsseite oder in einem bewusst geöffneten Detailpanel.

## Was und warum

Der erste Zustand zeigt kompakt:

> **Wo hilft meine Spende am meisten?**

> Je ein KI-Modell von Anthropic, OpenAI und Google prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.

> Für Menschen heute, für unsere gemeinsame Zukunft, für große Gefahren und für Probleme, die leicht übersehen werden.

Klein:

> NobleCause nimmt kein Geld an. Spendenlinks führen direkt zu den Organisationen.

Die Ursprungsgeschichte darf als ein kurzer, optional öffnender Satz oder als kleines Protokollsiegel erscheinen. Sie darf den ersten Viewport nicht dominieren.

## Mechanismus

Der bevorzugte Satz bleibt sichtbar:

> **Drei Modelle antworten getrennt. Sie lesen einander. Sie dürfen umdenken. Ein einfaches Programm zählt nur die Nennungen.**

Darunter:

> **Nennen mindestens zwei dieselbe Organisation, wird sie empfohlen. Sonst bleiben alle Vorschläge gleichwertig nebeneinander.**

Diese Erklärung gehört als schmales Messingband oder Ratsschild in die Bühne, nicht in eine große Textkarte.

---

# 7. Verbindliche Szenen und Kameraführung

Implementiere acht diskrete Zustände. Der Scrollweg aktiviert diese Zustände innerhalb derselben sticky Bühne.

Der Controller setzt beispielsweise `data-scene` und CSS Custom Properties. Keine Szene darf als gewöhnliche Vollbreitensektion unter der vorherigen erscheinen.

## Szene 1 · `arrival`

- weiter Blick in den Ratssaal,
- Bild fast vollständig sichtbar,
- kurze Was-/Warum-Tafel,
- Empfehlungen links bereits erkennbar, aber noch ruhig,
- Archiv rechts dunkel,
- Vorzimmer links unten sichtbar,
- Mechanikband oben oder unten sichtbar.

Ziel: Das erste Bild muss der Zielreferenz ähneln, nicht dem aktuellen Intro-Screenshot.

## Szene 2 · `recommendations`

- Kamera nähert sich leicht der Mitte,
- linkes Empfehlungsregister wird aktiv,
- vier aktuelle Ergebnisse leuchten nacheinander oder gemeinsam ruhig auf,
- Zählmaschine bleibt sichtbar,
- keine großen Empfehlungskarten über dem Saal.

## Szene 3 · `door-opening`

- Kamera bewegt sich zur rechten beziehungsweise räumlich passenden Eingangstür,
- Türzustand: geschlossen → schmaler Lichtspalt → geöffnet,
- der Übergang muss im Browser sichtbar sein.

### Technische Umsetzung ohne zusätzliches Türbild

Falls kein offenes Tür-Asset existiert:

- baue zwei dunkle Türflügel als CSS-/SVG-Layer,
- platziere dahinter die Vorzimmer-Plate,
- starte mit einer schmalen vertikalen Clip- oder Maskenöffnung,
- erweitere die Öffnung im Szenenwechsel,
- warmes Licht erscheint ausschließlich im Spalt,
- danach übernimmt die Vorzimmer-Plate die Hauptbühne.

Nicht akzeptabel:

- sofortige harte Bildüberblendung ohne Türmoment,
- Vorzimmer einfach weiter unten anzeigen.

## Szene 4 · `antechamber`

- Vorzimmer füllt die zentrale Bühne,
- Schiefertafel bleibt als ruhige HTML-Fläche nutzbar,
- Späher und Wart sind sichtbar,
- höchstens kurze Labels:
  - „Der Späher sammelt Belege.“
  - „Der Wart ordnet das öffentliche Protokoll.“
- Frage oder Belegzugang auf der Tafel,
- keine langen Erklärblöcke.

## Szene 5 · `initial`

- Rückkehr durch die Tür in den Ratssaal,
- alle drei Pulte gleichzeitig sichtbar und gleichwertig beleuchtet,
- je Pult nur ein kompaktes Votumsregister,
- keine drei vollständigen seitenhohen Spalten,
- Auswahl eines Pults öffnet ein verankertes Detailblatt, ohne die Bühne zu ersetzen.

## Szene 6 · `revision`

Vor jedem durchgestrichenen Votum muss der Kontext sichtbar sein:

> Nach dem Gegenlesen änderten zwei Modelle ihre Empfehlung.

Dann kleine Revisionszettel an den betroffenen Pulten:

```text
Erstvotum
TaRL Africa

geändert zu
Helen Keller International
```

- altes Votum mit `<del>`,
- neues Votum klar,
- keine riesigen Papierkolumnen,
- eine Messingmarke oder Lichtbahn darf sichtbar von einer Spur zur anderen wechseln,
- vollständige Begründung nur auf Wunsch oder in der Sitzung.

## Szene 7 · `count`

- Kamera fährt sichtbar zur Zählmaschine,
- Maschine nimmt den Fokus der zentralen Fläche ein,
- drei Modellmarken laufen oder springen in datengetriebene Ausgabefächer,
- gleiche Nennungen landen gemeinsam,
- verschiedene bleiben getrennt,
- kein Gesicht, kein Bediener, keine künstliche Intelligenzmetapher.

Kurzer Satz:

> Das Programm zählt nur, wie oft dieselbe Organisation genannt wurde.

Bei Nicht-Konsens bleiben drei gleich helle Ausgänge sichtbar.

## Szene 8 · `archive`

- Kamera zieht leicht zurück,
- rechte Archivtür beziehungsweise das Register wird aktiv,
- aktuelle Sitzung wird als veröffentlicht markiert,
- frühere Sitzungen erscheinen kompakt,
- Kosten und Korrekturhinweis sind erreichbar,
- Link zum vollständigen Protokoll.

---

# 8. Konkretes Kameramodell

Verwende keine vage „Kamera“-Metapher. Implementiere pro Zustand konkrete Werte.

Beispielhafte Ausgangswerte, die du an die echten Plates anpassen sollst:

| Szene | Scale | Translate X | Translate Y | Fokus |
|---|---:|---:|---:|---|
| arrival | 1.00 | 0% | 0% | gesamter Saal |
| recommendations | 1.08 | 2% | 1% | Mitte + linkes Register |
| door-opening | 1.22 | -18% | 0% | Türbereich |
| antechamber | 1.00 | 0% | 0% | Vorzimmer-Plate |
| initial | 1.12 | 0% | 5% | drei Pulte |
| revision | 1.20 | 0% | 5% | Pulte + Lichtbahnen |
| count | 1.48 | 0% | 2% | Zählmaschine |
| archive | 1.08 | -8% | 0% | Saal + Archivzone |

Die tatsächlichen Werte müssen visuell anhand der Screenshots abgestimmt werden.

Nutze:

- `transform-origin`,
- CSS Custom Properties,
- `scale` und `translate`,
- Opacity,
- Clip-Path oder Masken,
- kontrollierte Vignetten.

Keine WebGL- oder Canvas-Kamera.

---

# 9. Informationsdarstellung an den Pulten

Die aktuellen drei langen Modellspalten sind nicht akzeptabel.

Stattdessen:

- jedes Pult besitzt ein kleines verankertes Protokollschild,
- im Zustand `initial` zeigt es nur die vier Organisationsnamen kompakt,
- im Zustand `revision` zeigt es nur Änderungen,
- Fokus oder Klick öffnet ein größeres Detailblatt,
- das Detailblatt ist schließbar und blockiert nicht den gesamten Saal,
- alle drei Pulte bleiben im Raum erkennbar.

Die Bühne erzählt zuerst. Das vollständige Dokument steht zweitrangig zur Verfügung.

---

# 10. Empfehlungen links

Die vier Empfehlungen werden als kompaktes Register gebaut, nicht als 2×2-Kartenwand.

Jede Zeile enthält:

- kleines Symbolbild oder Säulenzeichen,
- Säulenname,
- Organisationsname,
- „3 von 3“, „2 von 3“ oder „keine zwei gleich“,
- ruhigen direkten Link.

Bei Fokus/Klick kann sich eine Zeile innerhalb des Registers erweitern und Registrybeschreibung, Vorbehalt oder alternative Nennungen zeigen.

Im Ruhezustand bleibt das Register kompakt.

Kein großer allgemeiner Button „Hier spenden“, der eine einzelne Organisation suggeriert. Jede Säule besitzt ihren eigenen direkten Link.

---

# 11. Restliche Website einbinden

Die neue Startseite darf nicht in eine optisch fremde alte Website führen.

Baue deshalb eine gemeinsame visuelle Hülle für alle Routen:

- einheitlicher Header,
- gleiche Messing-/Mondblau-Tokens,
- gleiche Typografie,
- gleiche Fokuszustände,
- gleiche Navigation,
- ruhige Hintergrundtexturen,
- Dokumentseiten wirken wie Archivblätter, Protokollbände oder Lesepulte desselben Hauses.

Mindestens folgende Routen müssen visuell eingebunden werden:

- `/idee/`
- `/manifest/`
- `/sessions/`
- `/sessions/[id]/`
- `/journal/`
- `/journal/[id]/`
- `/impressum/`

Dies ist kein vollständiges inhaltliches Redesign jeder Route. Es ist eine gemeinsame Art Direction und Shell, damit die Site wie ein Produkt wirkt.

Die Startseite bleibt full-bleed. Dokumentrouten dürfen lesbare Archivseiten sein.

---

# 12. No-JS-Fallback richtig lösen

Der No-JS-Fallback darf nicht länger die sichtbare Standardarchitektur diktieren.

Baue zwei Präsentationsmodi derselben Daten:

## Enhanced Mode

- sticky Bühne,
- Szenen,
- Türportal,
- Kameraführung,
- kompakte Register.

## Fallback Mode

- kompakte lineare Zusammenfassung,
- aktuelle Empfehlungen,
- direkte Links,
- Mechanismuserklärung,
- Link zur vollständigen Sitzung.

Technische Empfehlung:

- SSR rendert Bühne und Fallback,
- ein sehr früher Inline-Check setzt `document.documentElement.classList.add('js')`,
- bei erfolgreicher Initialisierung zusätzlich `stage-ready`,
- Fallback bleibt sichtbar, solange die Bühne nicht bereit ist,
- nach `stage-ready` wird der Fallback mit `hidden` oder äquivalenter zugänglicher Semantik entfernt,
- bei deaktiviertem oder fehlerhaftem JS bleibt der Fallback sichtbar.

Kein doppelter Fokusinhalt im aktiven Enhanced Mode.

---

# 13. Mobile

Mobil muss klar und atmosphärisch sein, aber nicht die Desktopbühne simulieren.

Verwende:

- ein Ratssaal-Kopfbild,
- kompakte Empfehlungsregister direkt darunter,
- eine horizontale oder schrittweise Szenennavigation,
- Vorzimmer als bewusstes Raumfenster,
- Pulte als kleine auswählbare Register,
- Zählmaschine als eigener visueller Zustand,
- Archiv als Türabschluss.

Auch mobil keine riesigen hellen Karten und keine endlosen Modellspalten.

Volltexte liegen auf der Sitzungsseite oder in Details.

---

# 14. Bewegung

Die Bewegung ist ruhig und mechanisch.

Erlaubt:

- sanfte Kameraannäherung,
- gezielte Lichtfokussierung,
- Türflügel öffnen,
- Clip-Reveal zum Vorzimmer,
- Messingmarken wechseln eine Spur,
- Zählwerk bewegt sich kurz,
- Register schieben sich wenige Pixel ein.

Verboten:

- permanente Zahnradrotation,
- Partikeleffekte,
- federnde Animationen,
- Cursorverfolgung,
- aggressive Parallaxe,
- Scrolljacking,
- große Animationsbibliothek.

Bei `prefers-reduced-motion` werden die Zustände ohne Kamerafahrt direkt überblendet.

---

# 15. Visueller Abnahmevertrag

Die Umsetzung gilt nicht als fertig, solange nicht für jeden Zustand ein Screenshot erzeugt und geprüft wurde.

Erzeuge unter `docs/review/corrective-home/`:

1. `01-arrival.png`
2. `02-recommendations.png`
3. `03-door-opening.png`
4. `04-antechamber.png`
5. `05-three-lecterns.png`
6. `06-revision.png`
7. `07-counting-machine.png`
8. `08-archive.png`
9. `09-mobile.png`
10. `10-nojs.png`

Verwende die produktive Preview-Ausgabe.

Jeder Desktop-Screenshot muss folgende Kriterien erfüllen:

- dieselbe Bühnenkomposition bleibt erkennbar,
- Ratssaal beziehungsweise Vorzimmer ist die dominante visuelle Fläche,
- keine Wand aus hellen Karten,
- kein langer Textblock verdeckt den Hintergrund,
- aktiver Zustand ist durch Licht, Fokus und Raum verständlich,
- die Zählmaschine ist im passenden Zustand frei sichtbar,
- das Vorzimmer übernimmt im passenden Zustand die Hauptfläche,
- die Türöffnung ist als eigener Zustand sichtbar,
- das Ergebnisregister bleibt kompakt,
- das Archiv ist Teil der Raumarchitektur.

Vergleiche `01-arrival.png` ausdrücklich mit dem angehängten Ziel-Mockup.

Falls die Ähnlichkeit nur in Farben besteht, aber nicht in Komposition und Informationsdichte, ist die Umsetzung nicht abgenommen.

---

# 16. Technische Prüfung

Erhalte die bestehenden Datentests und ergänze bei Bedarf nur presentation-nahe Tests.

Führe aus:

```bash
cd site
npm ci
npm test
npm run build
npm run preview -- --host 127.0.0.1
```

Prüfe:

- Desktop 1440 × 900,
- Desktop 1024 × 768,
- Mobil 390 × 844,
- Mobil 320 × 700,
- 200 Prozent Zoom,
- Tastatur,
- Hash-Navigation,
- Browser-Zurück,
- Reduced Motion,
- JavaScript deaktiviert.

Berichte nur tatsächlich ausgeführte Prüfungen.

---

# 17. Dateien und Grenzen

Arbeite im produktiven Pfad `site/`.

Behalte die bestehende Datenlogik, sofern korrekt.

Ändere nicht:

- `sessions/**`
- `journal/**`
- `schedule.json`
- `gremium/**`
- `schema/**`

Baue keinen neuen Prototypordner.

Keine neue Runtime-Abhängigkeit, außer sie ist technisch zwingend und vorher begründet.

---

# 18. Arbeitsreihenfolge

1. Aktuellen Build und Komponentenstruktur prüfen.
2. Daten-/View-Model-Schicht markieren, die erhalten bleibt.
3. Alte sichtbare Home-Komposition entfernen oder aus dem aktiven Renderpfad nehmen.
4. Gemeinsame Stage-Geometrie bauen.
5. `arrival` visuell fertigstellen und Screenshot prüfen.
6. Empfehlungregister integrieren.
7. Türportal und Vorzimmerübergang bauen.
8. Pulte und kompakte Votumsregister bauen.
9. Revision als räumlichen Vorgang bauen.
10. Zählmaschine fokussieren und datengetriebene Ausgänge bauen.
11. Archivzone bauen.
12. Gemeinsame Shell für restliche Routen integrieren.
13. Mobile Komposition bauen.
14. No-JS-Fallback isolieren.
15. Alle zehn Screenshots erzeugen.
16. Screenshots gegen den visuellen Vertrag prüfen und iterieren.
17. Tests, Build und manuelle Abnahme durchführen.
18. Abschlussbericht schreiben.

Gehe nicht direkt von Schritt 4 zu einem „fertig“-Bericht. Die Screenshotschleife ist Teil des Auftrags.

---

# 19. Abschlussbericht

Aktualisiere oder ersetze den bisherigen Buildbericht durch:

`docs/codex-corrective-build-report.md`

Der Bericht enthält:

1. Welche Datenlogik erhalten blieb.
2. Welche Präsentationskomponenten entfernt oder ersetzt wurden.
3. Aufbau der festen Bühne.
4. Technische Umsetzung der Kamerazustände.
5. Technische Umsetzung der Türöffnung.
6. Technische Umsetzung des Vorzimmerwechsels.
7. Technische Umsetzung der Zählmaschine.
8. Darstellung von Revisionen und Kontext.
9. Einbindung der übrigen Routen.
10. Mobile und No-JS-Modus.
11. Liste aller Screenshots.
12. Ausgeführte Befehle und Exit-Codes.
13. Tatsächlich geprüfte Viewports und Interaktionen.
14. Verbleibende Probleme.
15. Produktiver Buildpfad.

---

# 20. Definition of Done

Der Auftrag ist erst abgeschlossen, wenn:

- die Startseite wie ein einziges räumliches Instrument wirkt,
- der Ratssaal nicht von Textflächen verschluckt wird,
- Empfehlungen links kompakt integriert sind,
- das Vorzimmer dauerhaft räumlich verankert ist,
- die Tür sichtbar geöffnet wird,
- das Vorzimmer die Hauptbühne übernimmt,
- die Rückkehr in den Ratssaal sichtbar ist,
- drei Pulte gleichzeitig als gleichwertige Orte erfahrbar sind,
- Meinungsänderungen erst nach klarer Erklärung erscheinen,
- die Revision räumlich und typografisch nachvollziehbar ist,
- die Zählmaschine sichtbar fokussiert wird,
- Konsens und Nicht-Konsens datengetrieben dargestellt werden,
- Archiv und frühere Sitzungen Teil der Bühne sind,
- die restlichen Routen dieselbe visuelle Welt teilen,
- No-JS als Fallback existiert, aber nicht das Enhanced Design diktiert,
- die zehn Abnahmescreenshots vorliegen,
- der produktive Build erfolgreich ist.

Die zentrale Frage lautet diesmal nicht nur:

> Trägt die Szene den Zweck?

Sondern ebenso:

> **Ist die Szene tatsächlich die Benutzeroberfläche, oder liegt wieder nur Text vor einem dunklen Bild?**

Beginne jetzt mit dem kontrollierten Neuaufbau der Präsentationsschicht.
