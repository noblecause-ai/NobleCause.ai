> **Archiviert 2026-07-28 (CC) — überholter --SKIP-Bühnenspiel-Entwurf, nie Teil der Baseline.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# NobleCause.ai · OpenAI-Plan für das Bühnenspiel

**Zieldatei im Repository:** `docs/openai-buehnenspiel-plan--SKIP.md`  
**Phase:** Konzept und Architektur, noch keine Implementierung  
**Wichtig:** Dieser Plan wurde unabhängig erstellt. `docs/kimi-buehnenspiel-plan--SKIP.md` soll für die Umsetzung dieses Konzepts nicht als Quelle verwendet werden.

---

## 1. Leitidee: Drei Räume, eine wandernde Sitzung

Die Website soll sich nicht wie drei dekorierte Unterseiten anfühlen, sondern wie **ein Haus, durch das dieselbe öffentliche Sitzung wandert**.

Die drei echten Routen bleiben unverändert:

- `/` = The Study
- `/ratssaal/` = The Council
- `/archiv/` = The Archive
- plus die bestehenden englischen Gegenstücke

Jeder Raum folgt derselben Bühnen-Grammatik:

- **links:** die Ergebnis-Tafel
- **Mitte:** die Tür zum nächsten Raum
- **rechts:** ein Mondfenster als kalter Gegenpol
- **unten:** die Prozess-Röhre
- **dazwischen:** die jeweils raumspezifischen Akteure bzw. Arbeitsobjekte

Dadurch entsteht ein wiedererkennbares Theaterbild. Die Route wechselt, aber die Sitzung bleibt visuell dieselbe.

Die Bühne erklärt nicht alles gleichzeitig. Sie spielt eine kurze, klare Abfolge und kommt dann in einen stabilen **Lock-Zustand**, in dem der Besucher frei erkunden kann.

---

## 2. Was im ersten Moment zählt

Die erste Wahrnehmung ist immer räumlich, nicht textlich:

1. **Wo bin ich?**
2. **Was passiert hier?**
3. **Was ist das Ergebnis?**
4. **Wo geht es weiter?**

Darum gilt für alle drei Räume:

- Hintergrund zuerst
- raumspezifische zweite Ebene danach
- Ergebnisse danach
- Titel und Erklärung zuletzt

Die Ergebnisse erscheinen früh, aber nicht vor der Szene. Sie werden zum festen Orientierungspunkt und bleiben anschließend sichtbar.

---

## 3. Einheitliches Bühnenbild

### 3.1 Feste Anker

Jeder neue Raum-Plate wird bewusst für diese Geometrie komponiert:

```text
┌──────────────────────────────────────────────┐
│                                              │
│   ERGEBNIS-TAFEL       ZENTRALE TÜR    MOND  │
│                                              │
│        zweite Ebene / Akteure / Raumobjekte  │
│                                              │
│                                              │
├──────────────────────────────────────────────┤
│             PROZESS-RÖHRE                    │
└──────────────────────────────────────────────┘
```

Die Tür liegt **immer im sicheren zentralen Crop-Bereich**.

Die Tafel links und das Fenster rechts dürfen bei extremen Crops teilweise enger werden, ihre funktionalen Zonen müssen aber in Desktop und Mobil bewusst neu komponiert sein. Es wird nicht versucht, ein einziges 16:9-Bild für alle Seitenverhältnisse zu missbrauchen.

---

## 4. Die Ergebnis-Tafel: eine Konstante durch alle Räume

Die Ergebnisse sind eine echte HTML-Ebene, keine Schrift im Bild.

Sie liegen auf einer leeren Schieferfläche des jeweiligen Raum-Plates und werden aus der versiegelten Datenschicht gespeist.

### Beim Eintritt

Die leere Tafel ist bereits Teil des Bühnenbilds.

Nach dem Einfahren der zweiten Ebene werden die vier Ergebnisse eingeblendet:

- vier Bereichs-Embleme
- Organisationsname
- Stimmenzahl
- Vorbehalt, falls publiziert
- direkter Registry-Spendenlink

Keine neue Aggregation im Frontend.

### Während des Lock-Zustands

Die Tafel bleibt vollständig stabil.

### Beim Verlassen per Scroll

Die Tafel komprimiert sich leicht, bleibt aber sichtbar, während zusätzlicher Erklärungstext in den freigewordenen Bühnenraum nachrückt.

### Während einer Türfahrt

Die Ergebnisse dürfen **nie verschwinden**.

Damit sie nicht perspektivisch grotesk mit der Kamera durch die Tür fliegen, wechseln sie kurz in einen kompakten „Reise-Zustand“:

- dieselben vier Ergebnisse
- kleinere Schrift
- gleiche Reihenfolge
- als schmale, messinggerahmte Schieferleiste im linken oberen Bildschirmbereich

Nach Ankunft im nächsten Raum expandiert diese Ebene wieder exakt auf dessen Tafelfläche.

Damit wird „dieselbe Sitzung reist durch das Haus“ visuell verständlich.

---

## 5. Eintrittssequenz und Szenen-Lock

### 5.1 Grundtiming

Ziel: ungefähr **1,5 bis 1,8 Sekunden**, bevor die Szene vollständig gelockt ist.

Keine lange Introanimation.

#### Beat 1 · Raum erscheint
`0–180 ms`

- Hintergrundbild sichtbar
- nur Raum, Tafel, Tür, Fenster
- Prozess-Röhre als leerer Rahmen sichtbar

#### Beat 2 · Zweite Ebene fährt ein
`180–900 ms`

- raumspezifische Elemente kommen auf klaren Schienen in Position
- keine federnden Animationen
- schwere, mechanische Ease-Kurve
- 40–70 px reale Bildschirmbewegung statt übertriebener Fahrten

#### Beat 3 · Ergebnisse erscheinen
`650–1150 ms`

- Tafelinhalte werden zeilenweise sichtbar
- kein „Typing“
- eher wie Licht, das über bereits vorhandene Schrift fällt

#### Beat 4 · Titel und Erklärung
`1000–1550 ms`

- kurze Überschrift
- maximal zwei kurze Erklärungssätze
- Prozess-Röhre füllt die für diesen Raum gültigen Stationen

#### Beat 5 · Lock
ab ca. `1550 ms`

Jetzt:

- Tür ist interaktiv
- Akteure reagieren auf Hover/Fokus
- Scrollen löst die Bühnen-Öffnung aus
- Tastaturbedienung vollständig aktiv

---

## 6. Was passiert, wenn jemand während des Aufbaus scrollt?

Es wird **nichts übersprungen**, aber die Seite blockiert den Browser nicht.

Keine `preventDefault`-Scrollsperre.

### Vorschlag: Intent Queue

Die Eintrittssequenz läuft immer vollständig in ihrer Reihenfolge.

Währenddessen:

- normales Scrollen bleibt möglich
- der Bühnenfortschritt selbst ist bis zum Lock geklemmt
- Scrollabsicht wird als Zielzustand gemerkt

Sobald der Lock erreicht ist:

- wenn der Nutzer noch im Eintrittsbereich steht: normaler Lock
- wenn bereits weiter gescrollt wurde: die Austrittsbeats laufen automatisch in verkürzter Form hintereinander ab
- kein Beat wird ausgelassen
- minimale sichtbare Dauer pro Austrittsbeat etwa 120–160 ms

Dadurch fühlt sich die Seite nicht blockierend an, aber die Dramaturgie bleibt vollständig.

Türklick oder Enter während des Aufbaus:

- wird angenommen
- Navigation wird vorgemerkt
- nach Ende der Eintrittssequenz beginnt sofort die Türfahrt

Der Nutzer muss nicht ein zweites Mal klicken.

---

## 7. Raum 1: The Study

### Funktion

Hier entstehen:

- Frage
- Belege
- öffentliches Arbeitsprotokoll

### Zweite Ebene

Zwei getrennte transparente Ebenen:

#### The Scout
kommt von links mit Tisch.

#### The Warden
kommt von rechts mit Tisch.

Beide:

- von hinten oder schräg hinten
- keine Gesichter im Licht
- ihre Tische sind Teil ihrer Ebene
- sie fahren nur einen kurzen Weg ein, wie Bühnenelemente auf Bodenschienen

### Hover/Fokus

Scout:

> sammelt und prüft Belege

Warden:

> ordnet das öffentliche Protokoll

Keine Sprechblasen.

Name und Funktion erscheinen nahe der Figur als kleines Schild, nicht als großes Overlay.

### Tafel

Die vier aktuellen Empfehlungen erscheinen auf der großen Schiefertafel.

Die Frage selbst wird nicht mit den Ergebnissen vermischt. Sie erhält nach dem Lock eine eigene kurze, verständliche Zeile tiefer im Bühnenraum.

### Prozess-Röhre

Es erscheinen:

1. Frage
2. Belege

Die Kugeln rollen von rechts in ihre Fassungen.

Danach wird die Verbindung zwischen beiden sichtbar.

Kurzer Satz:

> Eine klare Frage. Dann werden die Belege gesammelt.

---

## 8. Raum 2: The Council

### Funktion

Hier passieren:

- drei getrennte Antworten
- Gegenlesen
- Umdenken
- Zählen

### Hintergrund

Der Saal bleibt weit und würdevoll.

Die Zählmaschine ist vorhanden, aber nicht das größte Objekt.

Sie darf an eine alte mechanische Kassen- oder Registriermaschine erinnern:

- Walzen
- kleine Zählwerke
- Papier-/Registermechanik
- Hebel
- drei Eingänge
- keine menschenähnlichen Eigenschaften

### Zweite Ebene

Nicht drei riesige Figuren.

Stattdessen drei einzelne **Council Stations**:

- Anthropic-Pult
- OpenAI-Pult
- Google-Pult

Jeweils als eigene transparente Ebene mit:

- Tisch/Pult
- Lampe
- Papier
- kleiner gesichtsloser Rückenfigur oder nur Arbeitsstation, abhängig vom bestehenden Stil

Sie fahren aus drei leicht unterschiedlichen Richtungen in eine stabile Dreiecksordnung.

Die drei Ebenen sind gleich groß und gleich hell.

### Hover/Fokus

Über jedem Pult erscheint:

- Anbieter
- Modellname aus den Daten
- „Erste Antwort ansehen“ bzw. entsprechender echter Link

Keine feste Pixelbeschriftung im Hintergrundbild.

Alle Labels hängen an den tatsächlichen DOM-Ankern der Pulte.

### Umdenken

Beim Lock kann ein dezenter Wechselzustand gezeigt werden:

- altes Votum sichtbar
- durchgestrichen
- neues Votum daneben/darunter

Erst nachdem der Satz sichtbar war:

> Sie lesen einander. Sie dürfen umdenken.

Damit ist das Durchstreichen erklärbar und wirkt nicht wie ein Fehler.

### Zählmaschine

Die Maschine ist Teil des Raums, aber erst beim Zähl-Schritt bekommt sie mehr Licht.

Sie urteilt nicht.

Klartext:

> Ein einfaches Programm zählt nur die Nennungen.

### Prozess-Röhre

Zu den vorhandenen zwei Kugeln kommen:

3. Drei Antworten
4. Umdenken
5. Zählen

Die Kugeln kommen einzeln, aber zügig.

---

## 9. Raum 3: The Archive

### Funktion

Hier wird aus Beratung ein dauerhaft öffentliches Protokoll.

### Zweite Ebene

Kein weiterer „Charakter“ nötig.

Stattdessen fährt ein **Publikationspult / Registertisch** aus dem unteren oder seitlichen Bühnenrand ein.

Darauf:

- das aktuelle Sitzungsdossier
- rotes Siegel
- Kostenangabe als echte HTML-Ebene
- Link zur vollständigen Sitzung

Zusätzlich darf genau eine Archivschublade oder ein Registerfach leicht hervortreten.

Das zeigt:

> Diese Sitzung wurde abgelegt und bleibt auffindbar.

Keine ganze Schrankwand animieren.

### Prozess-Röhre

Die letzte Kugel kommt hinzu:

6. Veröffentlichen

Danach ist die Röhre vollständig.

Kurzer Satz:

> Das Ergebnis und der ganze Weg dorthin werden veröffentlicht.

### Ausgang

Die zentrale Tür führt zurück zu The Study.

Damit entsteht ein Rundgang:

```text
Study → Council → Archive → Study
```

---

## 10. Raum-Topologie und Navigation

### Primäre Navigation

Nur die zentrale Tür ist der vorwärts gerichtete dramatische Weg:

- Study → Council
- Council → Archive
- Archive → Study

### Rückweg

Zusätzlich:

- Council: „Zurück ins Vorzimmer“
- Archive: „Zurück zum Rat“

Diese sind echte Links auf die vorherige logische Route.

Nicht `history.back()` als alleinige Logik.

Damit funktionieren auch Direktaufrufe stabil.

Der Browser-Zurück-Button bleibt selbstverständlich nativ und unangetastet.

### Direkte Sprünge

Keine große permanente Raumnavigation mitten in der Bühne.

Aber es gibt eine kleine, ruhige Utility-Navigation außerhalb der Dramaturgie:

- Vorzimmer
- Rat
- Archiv

Sie ist:

- tastaturzugänglich
- im No-JS-Zustand sichtbar
- visuell sekundär

Damit bleibt die Site praktisch, ohne das Bühnenspiel zu zerstören.

---

## 11. Die zentrale Tür als echte Portal-Ebene

Die Tür darf nicht nur Teil eines flachen Hintergrundbilds sein.

### Bildarchitektur

Jeder Raum besteht aus:

1. Base Plate mit zentralem Türrahmen und dunkler Öffnung
2. separater geschlossener Tür-Ebene
3. optionaler „leicht geöffnet“-Tür-Ebene
4. dahinter eine maskierte Vorschau des nächsten Raum-Plates

Dadurch kann die Tür unabhängig vom Hintergrund reagieren.

### Hover Desktop

Tür:

- öffnet sich ungefähr 8–12 Grad visuell
- warmer Lichtspalt
- hinter der Öffnung ist bereits ein kleiner echter Ausschnitt des nächsten Raums sichtbar
- keine Vollbildanimation

Daneben/unterhalb:

> Zum Ratssaal  
> Zum Archiv  
> Zurück ins Vorzimmer

je nach Raum.

### Fokus Tastatur

`:focus-visible` erzeugt denselben Vorschauzustand.

Keine Information nur per Hover.

### Mobile

Es gibt kein Hover.

Die Tür zeigt immer einen sehr subtilen Lichtsaum und ein kleines Ziel-Label.

Tap:

- startet direkt die Türfahrt
- die Vorschau wird während der ersten 250–350 ms sichtbar
- danach geht die Kamera durch die Tür

Kein Double-Tap und keine versteckte Geste.

---

## 12. Türfahrt / Kamera-Choreografie

Ziel: kein Crossfade zwischen Webseiten, sondern ein kurzer räumlicher Übergang.

Gesamtdauer etwa **1,1–1,5 Sekunden**.

### Phase 1 · Bühne räumt sich
`0–300 ms`

- zweite Ebene fährt 10–20 % zurück
- Erklärungstext zieht sich zurück
- Ergebnis-Tafel kollabiert in ihren Reise-Zustand
- Prozess-Röhre bleibt sichtbar

### Phase 2 · Portal öffnet
`220–500 ms`

- Tür öffnet
- nächster Raum liegt sichtbar dahinter
- Licht und Farbtemperatur des Zielraums sickern in den aktuellen Raum

### Phase 3 · Durchgang
`450–950 ms`

- Kamera bewegt sich geradlinig auf die zentrale Tür zu
- kein seitliches Schwenken
- Portal füllt zunehmend den Viewport

### Phase 4 · nativer Routenwechsel
ungefähr bei `70–80 %` Portalfüllung

Die bestehende Route wird normal navigiert.

Die vorhandene View-Transition wird benutzt, nicht ersetzt.

Shared-Elemente:

- Ergebnis-Reiseleiste
- Prozess-Röhre
- Portalfläche

### Phase 5 · Ankunft
`0–600 ms` auf Zielroute

Die neue Szene startet zunächst enger auf dem Portal und zieht dann sanft auf das komplette Bühnenbild zurück.

Danach beginnt die normale Eintrittsreihenfolge des Zielraums.

So fühlt sich die Bewegung wie **durch eine Tür gehen und im nächsten Raum zurücktreten** an.

---

## 13. Ergebnisse während der Türfahrt

Nie ausblenden.

Ablauf:

```text
Tafel groß
→ kompakte Reiseleiste
→ Türfahrt
→ Reiseleiste
→ Tafel groß im neuen Raum
```

Die Inhalte bleiben identisch.

Damit wird auch psychologisch klar:

> Die Empfehlung verändert sich nicht, nur weil ich den Raum wechsle.

---

## 14. Prozess-Röhre

### Bildidee

Keine klassische Stepper-Navigation.

Eine horizontale Messing-/Glasröhre mit sechs Fassungen.

Die vorhandenen sechs Prozess-Embleme sind die Kugeln.

#### Study
gefüllt: 1, 2

#### Council
gefüllt: 1, 2, 3, 4, 5

#### Archive
gefüllt: 1–6

Die Kugeln rollen sichtbar von rechts ein.

Verbindungsstücke leuchten erst, wenn beide angrenzenden Schritte vorhanden sind.

### Relevanz statt Volltext

Im gelockten Zustand:

- alle erreichten Kugeln sichtbar
- nur der aktive/zuletzt hinzugekommene Schritt trägt einen kurzen Satz
- ältere Schritte bleiben als Emblem + kurzer Name

So bleibt die Röhre lesbar.

### Beim Scrollen

Wenn zusätzlicher Text nachrückt:

- die Röhre darf sich auf Desktop an den unteren/seitlichen Rand schieben
- sie bleibt sichtbar, verliert aber ihre dominante Breite

### Rückwärts

Beim logischen Rückweg:

#### Archive → Council
Kugel 6 rollt wieder nach rechts aus der Röhre.

#### Council → Study
Kugeln 5, 4, 3 rollen in dieser Reihenfolge zurück.

Die verbleibenden Kugeln bleiben stabil.

Keine neue fachliche Berechnung, nur Darstellung des Raumzustands.

### Direktaufruf

Bei direktem `/ratssaal/`:

- HTML enthält sofort den korrekten Stand 1–5
- visuell dürfen die fünf Kugeln beim Eintritt zügig mit ca. 70–100 ms Versatz einlaufen

Bei `/archiv/` entsprechend 1–6.

No-JS zeigt den korrekten statischen Stand sofort.

---

## 15. Scrollen nach dem Lock

Die Seite darf nach dem Bühnenspiel nicht zu einer zweiten völlig anderen Website werden.

### Scroll-Öffnung

Erster bewusster Scroll nach unten:

- Akteure/zweite Ebene ziehen sich leicht zurück
- zentrale Tür bleibt sichtbar, wird aber ruhiger
- Ergebnis-Tafel wird kompakter
- Prozess-Röhre wandert an den Rand
- zusätzlicher Text kommt in den frei gewordenen Raum

Der Hintergrund bleibt derselbe Raum.

Keine abrupten weißen Dokumentsektionen.

### Inhalt darunter

Study:

- Was ist NobleCause?
- kurze Ursprungsgeschichte
- aktuelle Frage
- Belegzugang

Council:

- drei Voten
- sichtbare Änderungen
- vollständige Erklärung der Zählregel
- Zugang zum Sitzungsprotokoll

Archive:

- frühere Sitzungen
- Kosten
- Korrekturhinweis
- vollständige Sitzung

Das Bühnenspiel ist der Einstieg, die darunterliegende Dokumentebene die überprüfbare Tiefe.

---

## 16. Mobile: gleiche Dramaturgie, eigene Komposition

Mobil wird nicht der Desktop verkleinert.

### Portrait-Bühnenbild

Eigene 2:3- oder 9:16-nahe Plates pro Raum.

Gleiche Anker:

- Ergebnis-Tafel oben/links bzw. oberes Drittel
- zentrale Tür im sicheren mittleren Bereich
- Mondfenster rechts/oben
- Prozess-Röhre unten

### The Study mobil

- Scout und Warden fahren aus den unteren seitlichen Bereichen ein
- Tische kleiner, keine Überdeckung der Tafel
- Ergebnis-Tafel nutzt das obere Drittel
- Tür bleibt in der Mittelachse sichtbar

### Council mobil

- weite vertikale Saalansicht
- drei Pulte als Dreieck
- Maschine klein in der Mitte
- viel dunkler Steinboden im unteren Bereich für kurze Erklärung
- bei Zähl-Fokus wird nicht das ganze Bild gezoomt, sondern eine eigene Maschinen-Nahansicht eingeblendet

### Archive mobil

- zentraler Archivschrank / Register
- Tür mittig
- Ergebnis-Tafel als integrierte dunkle Fläche
- Publikationspult fährt von unten ein

### Ergebnisse mobil

Nach ihrer Enthüllung bleiben alle vier sichtbar in einer kompakten 2×2-Tafel.

Nicht als horizontales Karussell.

Keine Empfehlung wird hinter einem Swipe versteckt.

### Prozess-Röhre mobil

Sechs 44px-Fassungen passen als horizontale Leiste.

Nur beim aktiven Schritt erscheint eine kurze Textzeile darüber.

Die Röhre bleibt tappbar, ist aber nicht als Skip-Navigation gedacht.

---

## 17. No-JS-Grundzustand

Ohne JavaScript keine Bühne erzwingen.

Jede Route rendert normales, vollständiges HTML.

Reihenfolge:

1. Raum-Kopfbild
2. h1
3. vier Ergebnisse
4. direkter Spendenweg
5. kurzer Mechanismussatz
6. korrekter Prozessstand
7. raumspezifischer Inhalt
8. Tür als normaler Link
9. Utility-Navigation
10. vollständige Dokumenttiefe

Keine Inhalte sind nur in Layern vorhanden.

Mit JavaScript wird genau dieses HTML progressiv in die Bühne gesetzt.

---

## 18. `prefers-reduced-motion`

Bei `reduce`:

- keine Einfahrten
- keine Türrotation
- keine Kamerafahrt
- keine Kugelbewegung
- keine Scroll-Choreografie

Der Raum erscheint sofort im gelockten Endzustand.

Türnavigation erfolgt mit einer kurzen oder keiner Überblendung.

Die visuelle Hierarchie bleibt identisch.

---

## 19. Zweite Ebene je Raum

Zusammenfassung:

### Study
**Scout + Tisch** und **Warden + Tisch** als zwei getrennte Ebenen.

### Council
**Drei Council Stations** als drei getrennte Ebenen.

Grund:

- gleiche Rangordnung
- einzelne Hover-/Fokus-Anker
- saubere Einfahrbewegung
- Modellnamen sitzen am tatsächlichen Objekt statt an Bildkoordinaten

### Archive
**Publikationspult mit aktuellem Dossier und rotem Siegel** als eine Ebene.

Optional eine zweite kleine Ebene:

- einzelne leicht herausgezogene Archivschublade

Nur verwenden, wenn sie nicht nach Gimmick aussieht.

---

## 20. Asset-Plan

Keine Videos und keine GIFs nötig.

CSS- und View-Transition-Bewegung ist für diese Bühne besser:

- leichter
- schärfer
- reduced-motion-freundlich
- besser synchronisierbar
- keine Codec-/Autoplay-Probleme

### A. Base Plates

#### Desktop
3 × `16:9`, mindestens 1920×1080 Master:

1. Study, leeres Set
2. Council, leeres Set
3. Archive, leeres Set

Gemeinsam:

- zentrale leere Türöffnung / Türrahmen
- leere Schiefertafel links
- Mondfenster rechts
- keine Beschriftung
- keine zweite Ebene
- sichere zentrale Cropzone

#### Mobile
3 × `2:3`, mindestens 1024×1536:

1. Study
2. Council
3. Archive

Nicht bloß Crops der Desktopbilder.

**Summe Base Plates: 6**

### B. Tür-Ebenen

Pro Raum:

1. geschlossene Tür, freigestellt
2. leicht geöffnete Tür, freigestellt

Möglichst identische Perspektive.

- Study-Tür → Council
- Council-Tür → Archive
- Archive-Tür → Study

Die eigentliche offene Fläche zeigt dynamisch einen Crop des nächsten Raum-Plates.

**Summe Tür-Assets: 6**

Falls technisch sauberer, kann die „leicht geöffnet“-Variante durch CSS/Perspektivtransformation der geschlossenen Ebene ersetzt werden. Dann nur 3 Assets.

### C. Study-Akteure

1. Scout + Tisch, freigestellt
2. Warden + Tisch, freigestellt

Hohe Auflösung, Alpha.

Wenn dieselben Perspektiven mobil nicht sauber funktionieren:

- zusätzlich 2 mobile Varianten

**Summe: 2–4**

### D. Council Stations

1. Anthropic-Pult
2. OpenAI-Pult
3. Google-Pult

Freigestellt, identische visuelle Gewichtung.

Jeweils:

- Tisch/Pult
- Lampe
- Papier
- optional kleine gesichtslose Rückenfigur

Wenn mobile Perspektive separat nötig:

- weitere drei Portraitvarianten

**Summe: 3–6**

### E. Archive-Ebene

1. Publikationspult mit aktuellem Dossier
2. optional herausgezogene Schublade

Mobile Variante nur falls perspektivisch nötig.

**Summe: 1–4**

### F. Zählmaschine

Zwei Darstellungen:

1. kleine Maschine im Council-Base-Plate
2. eigene Detailansicht für den Zähl-Fokus

Detailmotiv:

- alte Registrier-/Kassenmechanik
- Walzen
- Zahnräder
- Papierstreifen ohne lesbaren Text
- drei Eingänge
- sichtbares Sortieren/Zählen
- nicht größer oder wichtiger als der Rat selbst

Desktop 4:3 oder 1:1 und mobile Portrait-Crop.

**Summe: 2**

### G. Bereits vorhandene Assets weiterverwenden

- vier farbige Bereichs-Embleme
- sechs Prozess-Embleme
- vorhandene Provenienz-Originale als Stilreferenz

Keine Neugestaltung ohne Not.

### Gesamt neuer Bildbedarf

Je nach Wiederverwendbarkeit:

- Minimum: ca. **20 Assets**
- Maximum mit separaten Mobile-Overlays: ca. **28 Assets**

Davon sind nur sechs große Vollflächenbilder.

Der Rest sind kleine transparente Ebenen.

---

## 21. Asset-Komposition und Textzonen

Alle Plates müssen absichtlich für HTML-Overlay komponiert werden.

### Tafel
große ruhige dunkle Fläche links.

### Titelzone
oberes mittleres Drittel, wenig Detail.

### Tür
Mitte, niemals nahe Rand.

### Mondfenster
rechts, dient als Lichtanker, nicht als Textzone.

### Untere Textzone
ruhiger Boden / dunkle Architektur.

Kein wichtiges Motiv in den letzten 8–10 % der oberen und unteren Bildkante.

Damit können 9:16-Geräte sicher erweitert oder beschnitten werden.

---

## 22. Performance-Budget

### Initialer Raum

Ziel:

- Base Plate Desktop: `≤ 500 KB`
- Base Plate Mobile: `≤ 350 KB`
- sichtbare zweite Ebenen zusammen: `≤ 350 KB`
- Tür-Layer: `≤ 120 KB`
- Embleme im ersten Paint zusammen: `≤ 150 KB`

**Initiale Bildlast Ziel:**

- Desktop `≤ 1.2 MB`
- Mobile `≤ 900 KB`

AVIF bevorzugt, WebP-Fallback.

Originale mit Provenienz bleiben außerhalb des produktiven rsync-Pfads, sofern das bestehende Assetkonzept das so vorsieht.

### Nächster Raum

Vor Lock:

- nichts Großes vorladen

Nach Lock oder bei Idle:

- nur kleine Portal-Vorschau `≤ 100 KB`

Bei Tür-Hover/Fokus:

- nächstes Base Plate priorisiert vorladen

Bei Türklick:

- volle Zielroute darf aus Cache kommen, Navigation funktioniert aber auch ohne Prefetch.

### JavaScript

Kein Animationsframework.

Zusätzlicher Stage-Controller:

- Ziel `≤ 20 KB gzip`

### CSS

Zusätzliche Bühnenregeln:

- Ziel `≤ 35–40 KB gzip`

Keine WebGL-/Canvas-Pflicht.

---

## 23. Technisches Zustandsmodell

Die Datenlogik bleibt versiegelt.

Die Präsentation bekommt nur einen kleinen Szenenzustand:

```text
room:
  study | council | archive

entry:
  background
  secondary
  results
  explanation
  locked

interaction:
  idle
  actorFocus
  doorPreview
  leavingByScroll
  leavingByDoor

motion:
  full
  reduced
```

Kein Zustand berechnet Empfehlungen.

Der Raumstatus bestimmt nur:

- welche Layer sichtbar sind
- wie viele Prozesskugeln gefüllt sind
- welche nächste Route hinter der Tür liegt

---

## 24. Was bewusst NICHT gemacht wird

- keine einzige riesige One-Page-Scrollstory
- keine künstliche History-Manipulation
- keine JS-Router-Ersatznavigation
- kein WebGL
- keine Chatblasen
- keine langen Textkarten über dem ganzen Hintergrund
- keine animierten Modellgesichter
- keine neu berechneten Ergebnisse
- kein Überspringen der Eintrittsbeats
- kein Video als notwendige Navigation
- kein Hover-only-Inhalt
- kein Desktop-Crop als mobile Lösung

---

## 25. Abnahmescreenshots und Bewegungsnachweis

Vor Freigabe braucht jeder Raum:

### Desktop
1. Hintergrund allein
2. zweite Ebene eingefahren
3. Lock-Zustand
4. Tür-Preview
5. Scroll-Öffnung

### Mobile
1. Eintritt
2. Lock
3. Türfahrt-Start
4. Scroll-Öffnung

Zusätzlich:

- Council Zähl-Fokus
- Archive vollständige Röhre
- Rückwärtszustand
- No-JS
- Reduced Motion

Ein statischer Screenshot reicht für Türfahrten nicht.

Für die Abnahme zusätzlich kurze lokale Screen-Recordings oder Frame-Sequenzen von:

- Study → Council
- Council → Archive
- Archive → Study
- Archive → Council rückwärts

---

## 26. Prioritäten für die Umsetzung

### Phase 1
Repository-Research auf der sauberen Baseline.

Keine Codeänderung.

### Phase 2
Asset-Geometrie und Raum-Plates final festlegen.

Vor Implementierung mindestens je ein Desktop- und Mobile-Wireframe pro Raum.

### Phase 3
No-JS-/Reduced-Motion-Grundzustand unverändert absichern.

### Phase 4
Study vollständig als vertikaler Slice bauen:

- Eintritt
- Lock
- Scroll-Öffnung
- Tür-Preview
- Türfahrt

Erst wenn dieser eine Raum überzeugt, die Mechanik auf Council und Archive übertragen.

### Phase 5
Council + Röhre + Rückwärtslogik.

### Phase 6
Archive + Rundgang.

### Phase 7
Mobile eigenständig feinabstimmen.

### Phase 8
Performance, A11y, DE/EN, Direktaufrufe, Browser Back/Forward.

---

## 27. Entscheidender Unterschied zu den bisherigen Versuchen

Bisher wurde Atmosphäre häufig **auf eine Inhaltsseite gelegt**.

Dieser Plan dreht es um:

> Die Bühne ist die primäre Benutzeroberfläche.  
> Das vollständige Dokument ist ihr belastbarer Boden.

Die drei echten Routen bleiben echte Webseiten.

Aber innerhalb jedes Raums verhält sich die Oberfläche wie ein kleines Bühnenstück mit wiederkehrenden Regeln:

- Raum
- Akteur
- Ergebnis
- Erklärung
- Tür
- nächster Raum

Damit entsteht nicht wieder eine lange Scrollseite mit schönen Hintergründen, sondern ein konsistentes räumliches System.
