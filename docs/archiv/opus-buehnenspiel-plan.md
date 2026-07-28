> **Archiviert 2026-07-28 (CC) — Pre-CC-Bühnenspiel-Entwurf, durch die späteren Runden abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# Bühnenspiel — Entwurf (Opus)

**Von:** Claude Opus (Cowork-Session) · **Datum:** 2026-07-19
**Grundlage:** Bühnenspiel-Direktive + `docs/handover-baseline.md` (IST-Zustand)
**Status:** Plan, unabhängig erstellt. Kein Code, kein Blick in fremde Pläne.

---

## 0 · Das Leitprinzip: Choreografie über einem fertigen Dokument

Der wichtigste Satz dieses Entwurfs, und alles andere folgt daraus:

> **Die Seite ist bereits vollständig, bevor das Spiel beginnt. Die Inszenierung
> verzögert und bewegt nur — sie erzeugt nichts und versteckt nichts.**

Das HTML, das der Server ausliefert, **ist der Endzustand**: alle Ergebnisse, alle
Spendenlinks, alle Erklärungen, die Röhre im korrekten Stand, die Türen als echte
Links. Das JavaScript setzt anschließend Startwerte (`transform`, `opacity`) und gibt
sie in einer Reihenfolge wieder frei.

Warum das die Architektur trägt:

- **Ohne JS** ist der Fallback kein zweiter Bau — es ist schlicht das unchoreografierte
  Dokument. Nichts zu pflegen, nichts, das auseinanderdriften kann. (Der frühere
  Doppelbau „sichtbarer Fallback + versteckte Bühne" entfällt ersatzlos.)
- **`prefers-reduced-motion`** ist derselbe Zustand: Choreografie wird gar nicht erst
  angewandt.
- **Bricht das JS mitten in der Sequenz**, bleibt ein vollständiges Dokument stehen,
  kein halb aufgebautes Bühnenbild.
- Der ehrliche No-JS-Test aus dem Bestand prüft weiterhin genau das Richtige.

Das ist die Umkehrung des naheliegenden Wegs (Elemente per JS einfügen) — und der
einzige, der die hart erkämpften Böden nicht gefährdet.

---

## 1 · Was ich anders vorschlage als die Direktive

Zwei Punkte, an denen ich begründet abweiche. Beide sind vom Steward überstimmbar.

### 1.1 Kein echter Scroll-Lock — ein *visueller* Lock

Die Direktive spricht vom „Szenen-Lock", der durch Scrollen verlassen wird. Ein
tatsächliches Sperren des Scrollens (`preventDefault`, Scroll-Hijacking) würde ich
**nicht** bauen: Es bricht Tastaturnavigation, Screenreader-Fluss, Trackpad-Erwartung
und ist die häufigste Beschwerde an solchen Seiten.

Stattdessen: Die Bühne füllt den Viewport (`100svh`), der Aufbau läuft, und **Scrollen
ist jederzeit erlaubt**. Der „Lock" ist der Zustand, in dem die Szene steht und nichts
weiter passiert — nicht ein gesperrter Eingabekanal. Das Ergebnis fühlt sich identisch
an, ohne den Nutzer festzuhalten.

### 1.2 „Während des Aufbaus gescrollt" → Choreografie springt ans Ende

Kein Überspringen aus Ungeduld (das ist entschieden). Aber wer scrollt, hat eine
Absicht geäußert, und gegen Nutzereingaben zu arbeiten ist etwas anderes als Geduld
einzufordern. Vorschlag: **Bei Scroll-Eingabe während des Aufbaus springt die
Choreografie sofort in den Endzustand** und der Scroll läuft normal weiter. Die
Sequenz wird nicht abgekürzt — sie wird *abgeschlossen*.

---

## 2 · Die Dramaturgie

### 2.1 Eintritt (alle Räume, gleiche Grammatik)

| Takt | Was | Dauer | Warum |
|---|---|---|---|
| 0 | **Bühnenbild** blendet auf (Plate) | 0 → 400 ms | Der Raum entsteht |
| 1 | **Zweite Ebene** fährt auf Schienen ein | 350 → 900 ms | Die Beteiligten treten auf |
| 2 | **Ergebnis** erscheint auf der Tafel | 800 → 1200 ms | Die Antwort — früh, nicht am Ende |
| 3 | **Titel / Erklärtext** setzt sich | 1100 → 1500 ms | Die Einordnung |
| 4 | **Röhre** füllt sich (Kugeln laufen ein) | 1300 → 1900 ms | Wo wir im Verfahren stehen |

Gesamt **unter zwei Sekunden**. Das Ergebnis steht bei ~1,2 s — die Geduld, die
verlangt wird, bleibt zumutbar, und die 30-Sekunden-Regel bricht nicht.

Takte überlappen bewusst (jeweils ~50 ms Versatz statt harter Kette): Das wirkt wie
ein Atemzug, nicht wie eine Abarbeitung.

### 2.2 Die zweite Ebene je Raum — gleiche Grammatik, eigener Inhalt

„Die Beteiligten dieses Raums treten auf":

- **The Study:** The Scout von links, The Warden von rechts, je mit Tisch und Lampe.
- **The Council:** die **drei Lesepulte fahren von unten in den Ring** und nehmen
  ihre Plätze ein — drei Lichter gehen nacheinander an. Das dramatisiert genau die
  Kernaussage des Raums: *drei Stimmen, getrennt, gleichrangig.*
- **The Archive:** die **Registerfächer füllen sich** (Sitzungen laufen von unten in
  die Regale). Das Archiv wächst, während man es betritt.

### 2.3 Die Tür

Die Tür liegt zentriert im Plate. Darüber liegt als eigene Ebene ein **Türblatt**
(freigestelltes Bild). Dahinter, maskiert auf die Türöffnung, das **Plate des nächsten
Raums**.

- **Ruhe:** Türblatt geschlossen, ein schmaler warmer Lichtspalt.
- **Mouseover/Fokus:** Das Türblatt schwenkt ~8° auf, die Maske gibt mehr des nächsten
  Raums frei, der Lichtspalt wächst. ~250 ms, weich.
- **Klick:** siehe 2.4.

Die Tür ist ein **echter `<a href>`** über der Türregion — damit ohne JS navigierbar,
tastaturbedienbar, mit sichtbarem Fokusring. Das Türblatt-Schwenken ist die Zugabe.

### 2.4 Der Übergang — „durch die Tür"

Ich lese die Direktive als *Hineingehen*, nicht als Herauszoomen:

1. **Rückfahrt** (0 → 300 ms): Die Schienen-Elemente ziehen sich zurück, die Röhre
   weicht zur Seite — die Bühne räumt.
2. **Türöffnung** (250 → 700 ms): Das Türblatt schwingt ganz auf.
3. **Durchgang** (600 → 1800 ms): Die aktuelle Szene skaliert auf den Türrahmen zu
   (`transform-origin` = Türmitte, Scale → ~1,35, sanftes Abdunkeln), während die
   Türöffnung als Blende aufreißt und den nächsten Raum freigibt.
4. **Ankunft** (ab 1600 ms): Im neuen Raum läuft §2.1 ab Takt 0 — Bühnenbild, zweite
   Ebene, Ergebnis, Text, Röhre.

Zusammen ~2,0 s vorwärts, ~1,2 s rückwärts (Zurück ist Orientierung, nicht Erlebnis).
Technisch auf der bestehenden View-Transitions-Maschinerie, die im Bestand nachweislich
läuft — kein Neubau.

**Ergebnisse während des Durchgangs:** Sie bleiben **nicht** starr stehen (das wirkt,
als klebte ein Zettel auf der Kamera). Sie reisen die ersten ~300 ms mit, blenden dann
über und setzen sich im Zielraum neu — als würde die Antwort mitgetragen.

### 2.5 Verlassen des Locks durch Scrollen

Die Schienen-Elemente ziehen sich beim ersten Scrollen ein Stück zurück (nicht ganz —
sie bleiben als Bühnenrand sichtbar), die Röhre schiebt zur Seite, der Inhalt rückt
nach. Rein scroll-gekoppelt über eine einzige CSS-Variable, kein Zustandsautomat.

---

## 3 · Die Prozess-Röhre

**Kernidee: Der Röhrenstand ist eine Eigenschaft des Raums, keine Erinnerung an den
Weg.**

Alle sechs Kugeln liegen immer im DOM. Jeder Raum definiert, welche gefüllt sind:

| Raum | Gefüllt | Blass |
|---|---|---|
| The Study | Frage, Belege | Drei Antworten, Umdenken, Zählen, Veröffentlichen |
| The Council | + Drei Antworten, Umdenken, Zählen | Veröffentlichen |
| The Archive | alle sechs | — |

Daraus folgt gratis:

- **Direkteinstieg** auf `/ratssaal/` zeigt sofort den richtigen Stand — ohne dass die
  Seite wissen müsste, wie jemand hereinkam.
- **Rückwärts** ist symmetrisch: Die Kugeln, die im Zielraum blass sind, laufen beim
  Rückweg aus der Röhre heraus. Kein Sonderfall, nur derselbe Zustandsvergleich.
- **Ohne JS** steht der korrekte Stand statisch da (gefüllt/blass als CSS-Klasse),
  ohne Animation.

Die Einlaufanimation ist die *Differenz* zwischen dem vorigen und dem aktuellen Stand:
Was neu gefüllt ist, rollt herein; was verloren geht, rollt hinaus. Beim Direkteinstieg
gibt es keine Differenz — die gefüllten Kugeln blenden einfach auf.

Jede Kugel trägt ihr Emblem, ihren Namen und ihren Erklärsatz. Die Röhre ist damit
gleichzeitig Fortschrittsanzeige *und* die Erklärung des Verfahrens.

---

## 4 · Mobil — dieselbe Erzählung, andere Physik

Auf dem Hochformat gibt es kein Links und Rechts, aus dem Akteure einfahren könnten.
Also wird die Dramaturgie **vertikal**, nicht geschrumpft:

| Takt | Mobil |
|---|---|
| 0 | Bühnenbild (Hochformat-Plate) blendet auf |
| 1 | Zweite Ebene steigt **von unten** ins Bild (statt von den Seiten) |
| 2 | Ergebnis-Tafel schiebt sich von oben ein und rastet |
| 3 | Titel/Text |
| 4 | Röhre füllt sich (bleibt horizontal — funktioniert unverändert) |

- **Kein Hover** → der Tür-Spalt zeigt dauerhaft einen schmalen Lichtschimmer;
  Antippen navigiert (kein Tap-and-Hold-Vorschau, das ist auf Mobil unentdeckbar).
- Die Ergebnis-Tafel **scrollt mit** (kein `fixed` — dafür ist zu wenig Platz), bleibt
  aber der erste Block nach dem Bühnenbild.
- Bewegungsumfang halbiert: kürzere Wege, gleiche Reihenfolge. Die Erzählung bleibt
  erkennbar, ohne dass etwas quer läuft.

---

## 5 · Assets — zwei Ausbaustufen

### Stufe A — schlank (Empfehlung für den ersten Bau)

Pro Raum **2 Bilder**:
1. **Raum-Plate** mit zentrierter Tür, allen Möbeln und Akteuren **bereits im Bild**
   (Quer + Hoch = 2 Dateien).
2. **Türblatt** freigestellt (transparentes PNG), passend zur Türöffnung des Plates.

„Einfahren" wird dann als **Parallax/Aufblenden** der Bildebenen gelöst statt als echte
Sprites. Wirkt ruhig, kostet wenig, kann nie fehlausgerichtet sein.
**Summe: 3 Räume × (2 Plates + 1 Türblatt) = 9 Dateien.**

### Stufe B — volle Bühne (falls die Wirkung nicht reicht)

Zusätzlich pro Raum **freigestellte Sprites** für die zweite Ebene:
- Study: Scout+Tisch, Warden+Tisch (2)
- Council: drei Lesepulte (1 Sprite-Satz)
- Archive: Registerreihen (1 Sprite-Satz)

Dafür müssen die Plates **ohne** diese Elemente erzeugt werden (leerer Raum), damit die
Sprites einfahren können. **Summe: +4 Dateien, und alle Plates in leerer Fassung.**

Ich würde mit **Stufe A** starten und Stufe B nur nachziehen, wenn der Aufbau zu
statisch wirkt. Der Unterschied ist spürbar, aber nicht so groß wie der Aufwand — und
Stufe A hat kein Ausrichtungsrisiko.

### Bildaufträge (ChatGPT), gemeinsame Vorgabe

> Gemalte Konzeptkunst wie die bestehenden NobleCause-Räume: dunkles Holz, Messing,
> Bernstein-/Lampenlicht gegen kühles Mondblau, matt, ernst. **Kein Text, keine
> Buchstaben, keine Zahlen im Bild.** Die **Tür sitzt zentriert** und ist sauber
> freistellbar (klare Kante, kein Objekt davor). Ruhige, dunkle Zonen links (Tafel)
> und unten (Text) freihalten. Zwei Fassungen je Raum: **Quer 16:9** und **Hoch 2:3**,
> identische Bildwelt.

- **The Study:** Studierzimmer. Zentrierte Doppeltür, große Schiefertafel links,
  hohes Fenster mit Mond rechts, zwei Schreibtische mit Lampen (Scout links, Warden
  rechts).
- **The Council:** Runde Kammer auf Augenhöhe (kein Amphitheater). Zentrierte Tür
  hinten, davor die messingfarbene Zählmaschine auf niedrigem Podest, drum herum drei
  gleiche beleuchtete Lesepulte. Unteres Drittel ruhiger Steinboden.
- **The Archive:** Archivsaal. Zentrierte Tür, hohe Registerregale mit beschrifteten
  (aber textlosen) Schachteln, warmes Lampenlicht, ruhige dunkle Spalte links.
- **Türblätter (3):** je ein freigestelltes Türblatt passend zur Öffnung des Plates,
  transparenter Hintergrund, leicht geöffnete und geschlossene Fassung optional.

---

## 6 · Raum-Topologie

**Rundgang als Erzählung, Karten als Freiheit.**

- Die **In-Szene-Tür** führt immer eine Station weiter: Study → Council → Archive →
  Study. Ein Raum, eine Vorwärtstür — das macht die Tür bedeutungsvoll.
- Die **Tür-Karten** (Bestand) bleiben und erlauben jeden Sprung. Sie sind zugleich
  der barrierefreie und der No-JS-Weg.

Damit ist die Inszenierung linear, die Navigation aber frei — niemand muss durch drei
Räume klicken, um ins Archiv zu kommen.

---

## 7 · Böden (unverhandelbar, hier konkret)

- **Ohne JS:** vollständiges Dokument, Röhre im korrekten Stand, Türen als Links,
  Ergebnisse und Spendenlinks da. Der bestehende ehrliche No-JS-Test wird um den
  Röhrenstand je Raum erweitert.
- **`prefers-reduced-motion`:** keine Choreografie, kein Übergang, kein Türschwenk.
  Sofortiger Endzustand, sofortiger Raumwechsel.
- **A11y:** genau ein wirksames `h1` je Raum; Türen und Kugeln sind echte
  Links/Buttons mit sichtbarem Fokus; Tap ≥ 44 px; Reflow 320/390 ohne Overflow;
  Akteur-Namen sind nicht nur Hover — sie stehen als Text unter/neben der Figur (Hover
  hebt nur hervor). **Keine Information existiert ausschließlich im Hover-Zustand.**
- **Datennaht:** unberührt. Ergebnisse, Zählstände, Revisionen kommen gelesen aus den
  publizierten Daten; Spendenlinks nur aus der Registry; nichts wird neu gezählt.
- **Tabu-Pfade:** unangetastet. Nur `site/` + `docs/`.

---

## 8 · Technik & Budget

- Choreografie ausschließlich über `transform` und `opacity` (Compositor), gesteuert
  von einer Handvoll CSS-Custom-Properties. Kein Layout-Thrashing.
- Ein kleines Modul (`stage.js`), Ziel **< 8 KB gzip**, ohne Bibliothek. Übergänge über
  die vorhandene View-Transitions-Maschinerie.
- `IntersectionObserver` nur für den Eintritts-Trigger, kein Scroll-Zustandsautomat.
- Bilder: pro Raum Plate (quer *oder* hoch, per `<picture>`) + Türblatt + maskiertes
  Nachbar-Plate. **Initiale Übertragung Ziel < 600 KB**; Nachbar-Plates lazy.
- Türblatt und Maske in `%` des Plates — die Vollbild-/`cover`-Frage ist damit
  entkoppelt, weil die Tür **zentriert** liegt und jeden Crop überlebt.

---

## 9 · Risiken, ehrlich

| Risiko | Gegenmittel |
|---|---|
| Der Aufbau verzögert die Antwort | Ergebnis in Takt 2 (~1,2 s); im DOM sofort vorhanden; Scroll springt ans Ende |
| Türblatt sitzt nicht exakt auf der Öffnung | Stufe A: Türblatt aus demselben Bild abgeleitet; %-Verankerung, visuelle Abnahme je Breakpoint |
| Drei Räume × zwei Formate × Ebenen = Gewicht | Nachbar-Plates lazy, Derivate optimiert, Budget gemessen statt geschätzt |
| Choreografie bricht auf schwachen Geräten | Nur Transform/Opacity; bei erkannt niedriger Bildrate Sequenz verkürzen (nicht abbrechen) |
| Mobiler Türspalt wird nicht entdeckt | Dauerhafter Lichtschimmer + Tür-Karten bleiben sichtbar |

---

## 10 · Umsetzungsreihenfolge

1. Choreografie-Gerüst über dem **bestehenden** Dokument (noch mit heutigen Plates) —
   beweist das Leitprinzip aus §0, bevor Kunst bestellt wird.
2. Röhre als Raum-Zustand (inkl. No-JS-Stand und Rückwärts-Differenz).
3. Tür als eigene Ebene mit Schwenk und maskiertem Nachbarblick.
4. Übergang auf die bestehende View-Transitions-Maschinerie setzen.
5. Mobil-Dramaturgie.
6. Neue Plates + Türblätter einsetzen (Stufe A).
7. Tests ehrlich nachziehen, Budget messen, Screenshots.

Schritt 1 ist bewusst zuerst: Wenn das Leitprinzip trägt, ist alles Weitere Fleiß.
Wenn nicht, hat es noch nichts gekostet.

---

## 11 · Die eine Frage, an der ich diesen Entwurf messe

> **Bleibt die Seite vollständig, wenn man ihr das Spiel wegnimmt?**

Wenn ja, ist die Inszenierung ein Geschenk. Wenn nein, ist sie eine Geisel.
