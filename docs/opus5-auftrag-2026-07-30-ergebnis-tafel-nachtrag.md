# Nachtrag — Ergebnis-Tafel: Steward-Entscheid und Schritt 2

**Von:** Opus 5 (Architekt), 30. Juli 2026
**Zu:** `docs/opus5-auftrag-2026-07-30-ergebnis-tafel.md`
**Grundlage:** deine Messung — 593 px Inhalt gegen 492/392/360/312 px verfügbar.

---

## 1 · Steward-Entscheid

**Internes Scrollen entfällt. Die vier Einträge stehen vollständig, ohne Scrollgeste.**

Damit ist §4 des Auftrags (Scrollbarkeit erkennbar machen) gestrichen — nicht verschoben.
Der Steward nennt als erlaubte Mittel ausdrücklich: **kleinerer Schriftgrad, zwei Spalten,
und in die Waagerechte gehen.**

Deine Rangfolge aus §3 ist damit überholt. Der begrenzende Faktor war die Annahme, die Tafel
bleibe eine schmale, einspaltige Liste — genau die steht jetzt zur Disposition. Dass §3.1
und §3.2 zusammen nur ~30 px liefern, ist deshalb kein Ergebnis mehr, sondern der Beleg,
dass am Zuschnitt gearbeitet werden muss statt an den Abständen.

---

## 2 · Der Rechenrahmen

Aus deiner Messung: der Kopf der Tafel (Titel + Sitzungszeile) belegt rund 120 px, die vier
Einträge rund 473 px — also **rund 118 px je Eintrag**. Dort liegt die Masse, und dort ist
der Hebel.

Zielmarke: **1280 × 720, alle vier Einträge samt Spendenlink ohne Scrollen.** Verfügbar sind
dort 312 px, davon 120 px Kopf → **die vier Einträge müssen in rund 190 px passen, also
knapp 48 px je Eintrag.** Das ist mit Abständen nicht zu holen, mit einem anderen Zuschnitt
schon.

---

## 3 · Drei Varianten — bauen, messen, zeigen

Baue alle drei als umschaltbare Fassungen (temporär, nicht zum Committen) und liefere je
**Screenshot bei 1280×720 und 1440×900** plus die Zahlen. Der Steward wählt am Bild.

**A · Dichte und Schriftgrad** — eine Spalte, alles bleibt wo es ist, nur kompakter.
Emblem kleiner, Zeilenabstände enger, Schriftgrade eine Stufe runter.
Frage an die Messung: **wie weit kommt man damit allein, und wie klein wird der
Organisationsname dabei?**

**B · Ein Eintrag, eine Zeile** — die Waagerechte. Emblem links, daneben Bereich, Name,
Zählstand und Spendenweg in *einer* Zeile statt in dreien. Das ist rechnerisch der stärkste
Einzelhebel: von ~118 px auf ~50 px je Eintrag. Setzt voraus, dass die Tafel etwas breiter
werden darf.

**C · Zwei Spalten** — 2 × 2 Raster. Halbiert die Zeilenzahl, verdoppelt aber den
Breitenbedarf; bei halber Spaltenbreite brechen lange Namen mehrzeilig und fressen einen
Teil des Gewinns zurück. **Miss das, statt es zu schätzen** — „Lead Exposure Elimination
Project (LEEP)" ist der Worst Case.

Kombinationen sind erlaubt und vermutlich die Antwort (A+B oder A+C).

---

## 4 · Die Messung, die vor allem anderen kommt: wie viel Breite ist da?

B und C brauchen Breite, und die Tafel steht heute bei `left: 1.25rem`, `width: 22rem`.
Der Kommentar in `+layout.svelte` sagt, die Textspalte weiche ihr aus — **wie viel Luft
zwischen Tafel-Rechtskante und linker Kante der Fluss-Spalte tatsächlich ist, weiß niemand.**

Erhebe bei **1280, 1440 und 1920** je:

- rechte Kante der Tafel, linke Kante der Fluss-Spalte, der Abstand dazwischen
- wie viel breiter die Tafel werden könnte, bevor die Fluss-Spalte weiter ausweichen muss
- was mit der Fluss-Spalte passiert, wenn sie ausweicht — und ab welcher Breite sie zu
  schmal für den Rekordtext wird

**Diese Zahl entscheidet, ob C bei 1280 überhaupt in Frage kommt.** Wenn die Tafel dort
nicht breiter werden kann, ohne den Rekord zu quetschen, ist C eine Variante für breite
Schirme und B die Antwort für schmale.

---

## 5 · Randbedingungen — gelten für alle Varianten

- **Vier Säulen, vier Einträge**, in der Reihenfolge Zukunft · Leid lindern · Große Gefahren
  · Was sonst übersehen wird. Auch Säulen ohne Konsens („keine Einigung") bleiben stehen.
- **Bei zwei Spalten: zeilenweise füllen** (Z L oben, G W unten), nicht spaltenweise. Sonst
  liest sich die Reihenfolge als Z G / L W und die Ordnung der Säulen ist zerstört.
- **Jeder Spendenweg bleibt** und behält ein Tippziel von mindestens 44 px. Wenn Name und
  Spendenweg zusammenfallen, muss erkennbar bleiben, dass es ein externer Link ist.
- **Der Zählstand bleibt** („3 von 3") — er ist der Beleg.
- **Schriftgrad hat eine Untergrenze.** Der Organisationsname trägt den Namen, den jemand
  im Spendenformular wiedererkennen muss; die Versalienzeile ist bereits klein. Nenne für
  jede Variante die kleinste verwendete Größe, damit der Steward sie beurteilen kann.
  Lesbarkeit ist Randbedingung, nicht Gestaltungsziel — aber sie ist eine.
- **Keine Bewegung.** Layoutfrage.
- **Die Tafel ist eine Instanz für alle drei Räume.** Jede Variante in Study, Council und
  Archiv ansehen, nicht nur in der Study.
- **Mobil (< 1200 px) bleibt wie es ist** — dort steht die Tafel im Fluss und hat kein
  Höhenproblem. Keine Variante darf dort etwas verändern.

---

## 6 · Ablauf

1. Breitenmessung aus §4 — **zuerst**, sie schränkt die Varianten ein.
2. A, B, C bauen, messen, Screenshots bei 1280×720 und 1440×900.
3. Bericht mit Zahlen und Bildern. **Stopp.** Der Steward wählt.
4. Erst danach die gewählte Fassung sauber ausbauen, alle drei Räume, Abnahme nach §5 des
   Hauptauftrags (ohne dessen §4).

Nichts committen. Die drei Varianten sind Wegwerf-Arbeit; nur die gewählte wird sauber
gebaut.
