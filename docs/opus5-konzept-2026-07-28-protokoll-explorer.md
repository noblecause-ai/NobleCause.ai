# Konzept — Der Protokoll-Explorer

**Von:** Opus 5 (Architekt) · **Stand:** 2026-07-28
**Gegenstand:** `/sessions`, `/sessions/[id]`, `/journal`, `/journal/[id]`, `/manifest` — die
letzte große Designlücke vor Go-Live. Enthält 2b („Wie gezählt wurde").

---

## 1 · Was der Explorer ist, und was er nicht ist

**Die Räume erzählen den Vorgang. Der Explorer hält den Rekord.**

Daraus folgt fast alles Weitere. Ein Raum darf verzögern, damit man ankommt; ein Protokoll darf
das nie — wer hier ist, will lesen. Die Räume arbeiten mit Bewegung, der Explorer mit **Ruhe**.
Gleiche Welt, gleiche Farben, gleiche Schrift — aber die Bühne steht still.

**Er ist kein vierter Raum.** Die Türfahrt bedeutet „ein anderer Ort". Der Rekord ist kein
anderer Ort, sondern eine andere **Tiefe** — die Schicht unter dem Klartext. Ihn mit derselben
Kamerafahrt zu betreten, würde diese Unterscheidung einebnen.

---

## 2 · Der Übergang: man setzt sich hin

Steward-Idee, übernommen. Der Explorer wird über den **Lesetisch im Archiv** betreten:

Der Tisch mit der Leuchte fährt heran und füllt den unteren Bildrand, das Licht der Lampe
weitet sich, der Raum dahinter sinkt in Unschärfe und Dunkel — und auf der Tischfläche liegt der
Rekord. Keine Kamerafahrt, keine Tür, **kein Ortswechsel: ein Perspektivwechsel.** Rund 0,8 s,
kürzer als die Türfahrt, weil dahinter Text wartet und nicht ein Anblick.

Zurück ist die Umkehrung: der Tisch weicht, der Raum kommt zurück.

**§0 unverändert:** ohne JS und bei `prefers-reduced-motion` ist es ein normaler Link auf eine
vollständig vorgerenderte Seite. Der Tisch ist Zierde, nie Zugang.

**Asset:** der vorhandene Pult-Cutout (`actors/pult-lamp`) reicht als Nahansicht vermutlich nicht
— das entscheidet CC am gerenderten Bild. Trägt er nicht, ist das eine Bestellung und kein
Kompromiss.

---

## 3 · Drei Schichten, jede mit einer Adresse

Das ist das tragende Prinzip, und es löst zugleich die §0-Frage, an der 2b hängen geblieben ist.

| Schicht | Was | Adresse |
|---|---|---|
| **Übersicht** | alle Sitzungen, neueste zuerst; je Sitzung Datum, Nummer, die vier Bereiche mit Zählstand und genannter Organisation | `/sessions` |
| **Eine Sitzung** | die vier Bereiche; je Bereich die drei Voten (Erst- und Schlussvotum, Änderungen und Vorbehalte gekennzeichnet), der Zählstand, der Dissens, die Kosten | `/sessions/[id]` |
| **Wortlaut** | der ungekürzte Text eines Modells | `/sessions/[id]#[modell]-[bereich]` |

**Jede Ansicht hat eine Adresse.** Filter sind Links, keine Schaltzustände: `/sessions?bereich=zukunft`,
`?modell=gpt`, `?org=hki`. Damit ist jede Ansicht teilbar, im Verlauf auffindbar, ohne JS
erreichbar — und **2b wird baubar**, denn die Auswahl eines Bereichs erzeugt keinen Inhalt mehr,
sie **adressiert** ihn.

Die vollständige Liste aller vier Bereiche ist immer der Inhalt. Der Zählstrang aus 2b (Pulte →
Trichter → Trommel) ist eine **Bühne darüber**, die den adressierten Bereich hervorhebt. Ohne JS
sieht man die Liste. Das war die ganze Blockade, und sie löst sich in der Adressierung auf.

---

## 4 · Gestalt

- **Kein Weiß.** Der Rekord liegt auf gealtertem Papier im Lampenlicht — warmer, dunkler Ton,
  Text hell darauf. Wer aus dem Archiv kommt, soll nicht geblendet werden.
- **Keine Kästen, keine Karten.** Vignetten und Linien, wie überall. Ein Votum ist ein Absatz mit
  Kopfzeile, kein Kärtchen.
- **Ein Lichtkegel.** Die Lampe des Tisches ist die einzige Lichtquelle; die Ränder der Seite
  dunkeln ab. Das ersetzt jede Rahmung.
- **Serifen für den Rekord, Versalien für die Ordnung** — die Schriftrollen der Räume, unverändert.
- **Die Medaillons ordnen die Voten.** Jedes Votum trägt das Medaillon seines Modells und den
  Modellnamen. Hier — und nur hier — stehen auch **Motiv und Begründung** der Selbstdarstellung,
  eine Ebene unter dem Medaillon. Das ist der Ort, den ich beim Bestellverfahren dafür
  vorgemerkt habe.
- **Bewegung: keine.** Kein Einfahren, kein Kreisen, kein Parallax. Nur der Eintritt bewegt sich.

---

## 5 · Was der Explorer über den Rekord sagen darf

Die versiegelte Datennaht gilt hier strenger als irgendwo sonst, weil hier der Wortlaut steht.

- **Wörtlich ist wörtlich.** Kein Kürzen, kein Zusammenfassen, kein „im Wesentlichen".
- **Strukturelle Signale dürfen dargestellt werden:** Zählstand, `conditional`, geändertes Votum
  zwischen den Runden, Dissens, Kosten, Suchanfragen. Das sind Felder, keine Deutungen.
- **Prozessaussagen sind erlaubt** — „zwei gleiche Nennungen ergeben eine Empfehlung" —, weil sie
  die Regel beschreiben und kein Ergebnis. Dieselbe Kategorie wie die Plakette an der
  Zählmaschine.
- **Ablehnungen und Vermerke bleiben sichtbar.** Der Rekord zeigt auch, was schiefging: der
  Bootstrap-Vermerk, `nachtragsbestellung`, `within_limits: false`, wer eine Bestellung
  angenommen hat. Ein Protokoll, das nur die guten Teile zeigt, ist keins.

---

## 6 · Journal und Kommissionen

Dasselbe Muster, kleinere Ausgabe. `/journal` als Zeitleiste der Läufe — Datum, Modell,
einberufen ja/nein mit Begründung, Befunde. `/journal/[id]` mit dem vollen Eintrag. Die
Bestell-Kommission (`commission-1`) erscheint dort als eigener Typ, **nicht** als Sitzung
gezählt — so, wie der Wart es entschieden hat.

---

## 7 · Reihenfolge des Baus

1. **Übersicht und Sitzungsseite** in der neuen Gestalt, ohne Übergang, ohne 2b. Das allein
   schließt die Designlücke und ist ausliefbar.
2. **Adressierbare Filter** (Bereich, Modell, Organisation) — Links, kein Zustand.
3. **Journal und Kommissionen** nach demselben Muster.
4. **2b, der Zählstrang** als Bühne über der Liste.
5. **Der Lesetisch-Übergang** — zuletzt, weil er Zierde ist und nichts blockiert.

**Nach Schritt 1 ist Go-Live möglich.** Alles danach ist Ausbau und kann in einer Punktversion
nachkommen, ohne dass jemand eine unfertige Seite sieht. Das ist die Grenze, die ich empfehle,
wenn der Gesamtrelease drängt.

---

## 8 · Abnahme

Vollständig ohne JS bedienbar, jede Ansicht adressierbar und teilbar · kein Wortlaut gekürzt ·
kein weißer Hintergrund · Tastaturbedienung und Fokusreihenfolge geprüft · Kontrast gemessen,
nicht geschätzt · mobil 390 ohne Overflow · reduced-motion geprüft · Vorstufe vor jeder visuellen
Aussage (frischer Build, Konsole sauber, Handler feuert).
