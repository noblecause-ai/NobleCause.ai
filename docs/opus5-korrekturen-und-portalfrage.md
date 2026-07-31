# Fünf Korrekturen + die Portalfrage

**Für:** CC (1–5) und den Steward (6) · **Von:** Opus 5 · **2026-07-27**

**Commits:** Zwei getrennte Commits, Archiv zuerst, dann Council-Tür. Sie sind unabhängig, die
Historie bleibt lesbar. **Freigegeben, setz sie.** Die Korrekturen unten kommen danach.

---

## 1 · Ratssaal: der Hintergrund wechselt beim Hover mitsamt dem Raum

**Ursache, gemessen:** `hall-door-open-display.avif` ist eine **separate Generation**, nicht eine
lokale Änderung. Außerhalb der Türzone weicht sie im Mittel um **5,86** ab, **17,96 % der Pixel
über 8**. Der 0,55-s-Crossfade blendet also den halben Raum um.

**Fix:** Genau das, was du beim Archiv gerade gemacht hast — nur die Tür-Region gefedert in das
geschlossene Plate komponieren, statt das ganze Master zu verwenden. Beim Archiv kamst du damit
auf 1,06 / 0,30 %. Dasselbe Verfahren auf `hall-*` anwenden, Zielwert Study-Niveau
(< 1 mittlere Differenz, < 1 % der Pixel > 8). Study prüfen und, wenn nötig, gleich mitziehen
(dort sind es 0,78 / 0,65 % — grenzwertig, aber unauffällig).

## 2 · Ratssaal: Sitz-Beschriftung über die Pulte

Wie bei Scout und Warden. `.pult-figure figcaption` sitzt heute bei `bottom: 17.5%`, also
darunter. Anker an die **Oberkante des Pults**, Versatz nach oben, `z-index` über dem Bild
(dieselbe Falle wie bei den Akteuren: `.actor img` trug `z-index: 1` und stach durch den Text),
Vignette statt Kasten. Höhenbudget wie bei den Akteur-Plaketten: erst Zeilen zusammenziehen,
dann kürzen — nichts verkleinern, was Wiedererkennung trägt.

## 3 · Archiv: nicht zwei gleiche Möbel

Zwei identische Karteikästen sind der Fehler, nicht die Kästen selbst. Neu:

- **unten links: das Pult mit der Leuchte** — das Möbel, das im Plate hinten rechts steht
  (Referenz: `ref-archiv-pult-mit-leuchte.png`). Es bringt eine warme Lichtquelle mit, die
  einfährt; das ist der Gewinn gegenüber einem stummen Schrank.
- **unten rechts: der Karteikasten** (`register.avif`, schon gekeyt) — bleibt, aber nur einmal.

Zwei verschiedene Objekte, asymmetrisch, Mitte frei. Dass dasselbe Möbel auch im Plate steht,
ist unschädlich — das Einfahrende ist näher, größer und an der anderen Ecke; im Vorzimmer stehen
ebenfalls zwei Schreibtische.

**Ein Bild zu bestellen** (Referenz beilegen):

> Erzeuge genau EIN Bild, mindestens 1024 px hoch. Keine Montage, kein Text.
> Ein Archivpult aus dunklem Nussbaumholz mit Schubladen und Messinggriffen, darauf eine
> **brennende Messing-Schreibtischleuchte mit Schirm** und ein **aufgeschlagener Foliant auf
> einem Pultständer**, schräg von vorn gesehen. Wie im beigelegten Bild, dasselbe Möbel.
> Freigestellt vor FLÄCHIGEM MAGENTA (#FF00FF), formatfüllend, kein Boden, kein Schatten,
> keine Umgebung. Das Licht der Leuchte darf auf Pult und Folianten fallen — aber nicht auf
> den Magenta-Grund.

## 4 · Die Protokollseiten sind ein eigenes Paket

`/sessions`, `/sessions/[id]`, `/journal`, `/journal/[id]` liegen außerhalb der
`(rooms)`-Gruppe und tragen noch das alte Dokumentlayout. Der Sprung vom inszenierten Raum in
eine schlichte Textseite ist der härteste Bruch, den die Seite hat — und er trifft genau die
Nutzer, die *genau hinsehen* wollen.

**Das entwerfe ich hier nicht.** Es ist ein eigenes Gestaltungsproblem — ein Explorer über die
Protokolle, mit Überblick, Filter nach Bereich und Sitzung, und dem Wortlaut eine Ebene
darunter. Es braucht eine eigene Runde und sollte **nicht** in die laufenden Korrekturen
gemischt werden. Nur die Einordnung: **es ist die letzte große Designlücke vor dem Go-Live**,
größer als alles, was in den Räumen noch offen ist.

## 5 · Study: was durch den Türspalt zu sehen ist, ist nicht der Ratssaal

Richtig beobachtet. Durch den Spalt gehört ein Hauch des Zielraums — Rundsaal, warmes
Lampenlicht, ein Schimmer Messing. Zwei Wege, und der zweite ist der bessere:

- **kurzfristig:** die Farbtemperatur im Spalt an das Ratssaal-Licht angleichen (Tonwertkorrektur
  auf der Spaltregion). Billig, macht den Widerspruch leiser statt ihn zu lösen.
- **richtig:** Es löst sich von selbst, sobald der echte Durchgang gebaut ist — dann liegt
  hinter der Tür wirklich das Ziel-Plate und nicht ein gemalter Ersatz. Siehe §6.

Ich würde es **nicht** einzeln nachbestellen, sondern an §6 hängen.

---

## 6 · Der echte Durchgang — Sachstand und ein Befund, der die Rechnung ändert

**Wir haben nie dagegen entschieden.** Der Steward hat am 24.07. WebGL beschlossen; ich habe die
`clip-path`-Blende als **Gegenprobe vor** dem 3D-Bau vorgeschlagen. Die Gegenprobe wurde gebaut,
sie trug — und Phase 1 ist danach nie wieder aufgerufen worden, weil sie an den Assets aus §A6
des Review-Dokuments hing und **ich diese drei nie bestellt habe**, während Serie 3 und 4
rausgingen. Kein Beschluss, ein Versäumnis.

**Technisch:** möglich, und ohne Three.js. `perspective` + `translateZ` auf einer eigenen
Übergangsebene genügt für eine Kamerafahrt. Meine Rücknahme von CSS-3D galt dem *Ruhebild* —
dort bricht `perspective` die fixe Bühne und Plate-Skalierung verschiebt den Cover-Ausschnitt,
aus dem die Hotspot-Geometrie kommt. Für eine **Sekunde Fahrt** greift beides nicht: die Bühne
wird dabei abgebaut, der Hotspot ist irrelevant, und die Übergangsebene ist ein Overlay im
persistenten Layout (§A1), nicht die Scroll-Bühne. Die VT muss während der Fahrt aus sein
(§A2) — dieselbe Mechanik, die du für die Blende schon hast.

**Und der Befund:** Die §A6-Assets braucht es vermutlich **gar nicht als Bestellung.** Was
gebraucht wird, ist
1. das **Wand-Plate mit Loch** — das vorhandene Plate mit Alpha in der Türöffnung,
2. das **Türblatt als eigene Ebene** — dieselbe Region, herausgeschnitten,
3. das **Ziel-Plate in hoher Auflösung** — existiert.

Punkt 1 und 2 sind **Maskierarbeit am vorhandenen Plate**, keine Generierung. Die Türgeometrie
ist in allen drei Räumen gemessen. Damit fällt die externe Lieferzeit weg — also genau der Grund,
aus dem Phase 1 liegengeblieben ist.

**Spike, bevor irgendetwas geplant wird (klein, aussagekräftig):** Schneide im Study-Plate die
beiden Türflügel entlang der Laibung heraus und sieh nach, ob die zurückbleibende Öffnung sauber
liest — Laibung, Sturzschatten und Schwelle müssen stehenbleiben, sie sind heute auf die Flügel
gemalt. Trägt der Schnitt, ist Phase 1 in Reichweite; trägt er nicht, brauchen wir doch ein
Wand-Plate vom Generator, und dann wissen wir es für einen Preis von einer Stunde.

## 7 · Rotierende Sitze um die Zählmaschine — machbar, mit zwei Ehrlichkeiten

Semantisch die stärkste Idee dieser Runde: drei Stimmen, die den Zähler umkreisen, ist genau
das, was im Ratssaal geschieht.

**Erstens:** Die Pulte sind flache Cutouts aus **einem** Blickwinkel. Eine echte Rotation würde
sie von der Seite und von hinten zeigen — das kann ein flaches Bild nicht. Was geht, ist eine
**Billboard-Ellipse**: sie laufen auf einer perspektivisch verkürzten Bahn um die Maschine,
bleiben zur Kamera gedreht, und Tiefe zeigt sich über Größe, Helligkeit und Verdeckung. Das
liest als Umkreisen, nicht als Drehen — und es ist genau das, was die Vorlage tut.

**Zweitens:** Die Bahn führt durch die Bildmitte, die das Kantenprinzip für Inhalt freihält.
Auflösbar, aber nur so: Die Umkreisung läuft **im Hero-Band und nur im Ruhezustand**, bevor die
Tafel einfährt; sobald gescrollt wird, ziehen die Pulte auf ihre Randpositionen und die Mitte
gehört wieder dem Inhalt. Das ist eine Erweiterung des Kantenprinzips, keine Verletzung — aber
sie gehört ausdrücklich entschieden, nicht nebenbei gebaut.

**Reihenfolge:** Erst der Spike aus §6. Die Umkreisung und der Durchgang teilen dieselbe
Übergangsebene und dieselbe Tiefenlogik; sie zweimal zu bauen wäre Verschwendung.
