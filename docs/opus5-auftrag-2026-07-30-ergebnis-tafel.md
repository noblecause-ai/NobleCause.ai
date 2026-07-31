# Auftrag an CC — Ergebnis-Tafel: Raumzuteilung bei kurzen Viewports

**Von:** Opus 5 (Architekt), 30. Juli 2026
**Betrifft:** Übergabe 30.07. §4 Punkt 1 · `ResultBoard.svelte`
**Vorgehen:** erst messen, dann dem Steward Zahlen vorlegen, dann bauen. **Nicht sofort
umbauen.**

---

## 1 · Richtigstellung des Befunds

Der Architekt hat gemeldet, der vierte Eintrag der Tafel sei „nicht erreichbar". **Das war
zu scharf.** Am Code nachgesehen: die Tafel trägt `max-height: calc(100svh - 24rem)` und
`overflow-y: auto` — sie ist scrollbar, der Inhalt ist erreichbar. Der weiche Rand unten ist
eine `mask-image` von `0.9rem` und als Scroll-Andeutung gedacht, kein Rendering-Fehler.

**Der Befund bleibt trotzdem gültig, nur anders begründet:**

1. **Die Raumzuteilung ist für hohe Schirme kalibriert.** `top: 15.5rem` plus die Reserve
   von `24rem` nehmen der Tafel bei einem 800-px-Fenster über die Hälfte der Höhe. Was übrig
   bleibt, trägt die vier Einträge samt Kopfzeile nicht — also scrollt sie fast immer.
2. **Die Scrollbarkeit ist nicht erkennbar.** Ein 0,9-rem-Verlauf liest sich als
   Gestaltungsdetail, nicht als „hier geht es weiter". Wer ihn nicht als Andeutung erkennt,
   sieht drei Empfehlungen und hält das für alle.
3. **Ein scrollender Container in der fixen Bühne ist eine Falle.** Steht der Mauszeiger
   über der Tafel, scrollt das Rad die Tafel statt der Seite. Der Nutzer wollte
   weiterlesen und bekommt eine Bewegung, die er nicht angefordert hat.

**Das Gewicht der Sache:** Die Tafel trägt die vier Spendenlinks — den einzigen
Handlungspfad der Seite. Ein Weg, der nur über eine unerkannte Scrollgeste erreichbar ist,
ist praktisch keiner.

---

## 2 · Schritt 1 — messen, nicht schätzen

Frischer Build, dann bei **1440×900, 1440×800, 1366×768 und 1280×720** je erheben:

- die tatsächliche Inhaltshöhe der Tafel (`scrollHeight`)
- die verfügbare Höhe (`clientHeight`, also was `max-height` übrig lässt)
- die Differenz — **wie viele Pixel fehlen wirklich?**
- ob der vierte Eintrag samt Spendenlink ohne Scrollen sichtbar ist (ja/nein)
- dasselbe für die drei Räume, falls sich die Tafel je Raum unterscheidet

**Das Ergebnis als kleine Tabelle in den Bericht.** Erst danach wird entschieden, wie viel
Platz zurückgewonnen werden muss — 40 fehlende Pixel sind eine andere Aufgabe als 200.

---

## 3 · Schritt 2 — Raum zurückgewinnen, in dieser Rangfolge

Die Vorgabe ist ein Ziel, kein Verfahren: **bei 1280×720 stehen alle vier Einträge samt
Spendenlink ohne Scrollen.** Wie du dorthin kommst, ist deine Entscheidung — aber in dieser
Reihenfolge, weil sie von „kostet nichts" zu „kostet Substanz" geht:

1. **Die Reserve prüfen.** `top: 15.5rem` und `− 24rem` sind großzügig. Miss, was oben und
   unten tatsächlich belegt ist, und gib der Tafel zurück, was niemand braucht. Das ist der
   billigste Platz.
2. **Die vorhandene Kompaktierung schärfen.** Es gibt bereits einen Block für
   `max-height: 740px`. Er greift zu spät und zu schwach — Schwelle und Wirkung anpassen,
   statt einen zweiten Mechanismus danebenzustellen.
3. **Zeilen einsparen, nicht Inhalt.** Der Spendenlink steht heute als eigene Zeile unter
   dem Organisationsnamen — vier Einträge, vier zusätzliche Zeilen. Ob Name und Link bei
   knapper Höhe zusammenfallen dürfen, ist eine Gestaltungsfrage: **vorlegen, nicht
   entscheiden.** Wenn du hier landest, schreib in den Bericht, wie viele Pixel es brächte,
   und lass den Steward wählen.

**Was nicht passieren darf, unabhängig vom Weg:**

- **Kein Eintrag verschwindet, keiner wird gekürzt.** Vier Säulen, vier Zeilen — auch die
  ohne Konsens („keine Einigung"). §0: die Bühne versteckt nie.
- **Kein Spendenlink fällt weg.** Wenn irgendetwas weichen muss, dann nicht er.
- **Der Zählstand bleibt** („3 von 3") — er ist der Beleg, ohne ihn ist die Empfehlung eine
  Behauptung.
- **Keine Bewegung, keine Animation.** Das ist eine Layoutfrage.

---

## 4 · Wenn Scrollen unvermeidbar bleibt

Falls die Messung zeigt, dass es bei sehr kurzen Fenstern nicht ohne geht, muss der Zustand
wenigstens ehrlich sein:

- **Die Scrollbarkeit muss erkennbar sein**, nicht angedeutet. Ein 0,9-rem-Verlauf reicht
  dafür nicht.
- **Das Rad-Verhalten prüfen:** `overscroll-behavior` so setzen, dass die Seite weiterscrollt,
  wenn die Tafel am Ende ist — nicht in ihr hängenbleibt.
- **Tastatur:** ein scrollbarer Bereich muss per Tastatur erreichbar und bedienbar sein,
  sonst ist der vierte Spendenlink ohne Maus unerreichbar. Das ist der härtere Fall als die
  Sichtbarkeit.

---

## 5 · Abnahme

Frischer Build vorweg, dann je Punkt ein Beleg:

1. Die Messtabelle aus §2, vorher und nachher.
2. Bei **1280×720**: alle vier Einträge mit Spendenlink ohne Scrollen sichtbar. Screenshot.
3. Bei **1440×900**: unverändert gut, keine Regression durch die Kompaktierung. Screenshot.
4. **390 px**: die Tafel steht dort anders — belegen, dass sich nichts verschlechtert hat.
5. Alle vier Säulen vorhanden, inklusive einer ohne Konsens; alle vier Spendenlinks
   klickbar; Zählstände unverändert.
6. **Tastatur:** Tab erreicht alle vier Spendenlinks, auch den vierten.
7. `reduce` und ohne JS: unverändert vollständig.
8. Die Tafel steht in **allen drei Räumen** — alle drei prüfen, nicht nur die Study.

Committen erst auf Freigabe. Wenn du bei §3 Punkt 3 landest, **stopp vor dem Bauen** und
leg die Zahlen vor.
