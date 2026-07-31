# Die Modelle bestellen ihre eigene Darstellung — Machbarkeit, Entwurf, Auflagen
## Dazu: Entscheide zu Runde D, die Council-Türmitte und das nie gebaute 2b

**Von:** Opus 5 (Architekt) · **Stand:** 2026-07-27
**Anlass:** Steward-Idee; zwei Richtungsentscheide von CC; zwei Steward-Befunde.

---

# Teil 1 · Die Idee: jedes Modell bestellt seine Darstellung

**Machbar — ja. Und es ist die bessere Antwort auf eine Lücke, die wir gerade erst gefunden
haben.** CC hat zu Recht festgestellt: die drei Modell-Medaillons aus meinem §7-Konzept
existieren nicht. Mein „kein neues Asset nötig" war falsch. Diese Idee füllt genau diese Lücke —
und zwar mit etwas, das inhaltlich weit mehr trägt als alles, was ich hätte spezifizieren können.

## 1.1 Der entscheidende Unterschied: bestellen, nicht erzeugen

Die Modelle **beschreiben** ihre Darstellung. Erzeugt wird sie von **einem** Generator, im
Hausstil, für alle drei gleich.

Das ist kein Kompromiss, sondern die einzig tragfähige Fassung — aus einem Grund, der im Kern
der Seite liegt:

**Ließe man jedes Modell sein Bild selbst erzeugen, könnte Claude nicht teilnehmen.** Anthropic
hat keine Bildgenerierung; OpenAI und Google haben sie. Zwei Familien bekämen ein Selbstbildnis,
eine bekäme einen Platzhalter — und die Grundprämisse der Seite, **drei Familien werden gleich
behandelt**, wäre an der sichtbarsten Stelle gebrochen. Dazu kämen drei unvereinbare Bildstile in
einem Raum, der von seiner Geschlossenheit lebt.

Beschreiben können alle drei gleich gut. **Der Text ist die Bestellung, das Bild ist ihre
Ausführung.** Damit ist auch die Datennaht sauber: die Bestellung ist Rekord und steht wörtlich,
das Bild ist eine abgeleitete Darstellung — dieselbe Trennung wie Klartext und Wortlaut.

## 1.2 Wann bestellt wird

Nicht pro Sitzung — **pro Modellidentität, bei der ersten Einberufung.** Die Darstellung hängt
am Modell (`claude-opus-5`, das jeweilige GPT, das jeweilige Gemini), nicht am Datum. Wechselt
die Besetzung oder die Version, wird neu bestellt; die alte Darstellung bleibt im Rekord stehen,
damit ältere Sitzungen weiter richtig aussehen.

Praktisch: eine kleine Registratur neben `organizations.json` — Modellkennung, Bestelltext
wörtlich, Datum der Einberufung, Pfad zum Asset, Version. Unter den Guard-Hook, wie die anderen
Rekord-Dateien.

## 1.3 Der Rahmen, den die Bestellung nicht verlassen darf

Die Freiheit liegt im **Motiv**, nicht in der Form. Fest vorgegeben:

- **Rundes Messingmedaillon**, fester Durchmesser, freigestellt auf Magenta, kein Text im Bild.
- **Hausstil:** Nacht, Nussbaum und dunkle Eiche, Messing, warmes Lampenlicht gegen kaltes
  Mondblau, gemalte Konzeptkunst, gleicher Schwarzpunkt.
- **Ein Gegenstand oder Zeichen, kein Gesicht und keine Figur.** Der Raum ist aus Möbeln,
  Instrumenten und Licht gebaut; ein Porträt bricht die Welt. Und ein Modell, das sich ein
  Gesicht gibt, behauptet etwas, das die Seite nirgends behauptet.
- **Keine Firmenlogos, keine Wortmarken, keine Markenfarben.** Nicht nur rechtlich — die Seite
  zeigt Modelle als Stimmen, nicht als Produkte.
- **Gleiche Bedingungen für alle drei:** derselbe Rahmentext, dieselbe Zeichenzahl, dieselbe
  Anzahl Versuche, derselbe Generator. Wer mehr Versuche bekommt, bekommt ein besseres Bild —
  und die Ungleichheit wäre sichtbar.

## 1.4 Was ich für eine Wart-Vorlage halte

Das ist **keine reine Bauentscheidung.** Die Bestelltexte werden Teil des Rekords, und die Seite
zeigt künftig, wie Modelle sich selbst darstellen wollten. Das berührt Kanon IV und die
Datennaht — also den Wart.

Zu klären wären: Ist der Bestelltext Rekord (wörtlich, unveränderlich) oder Beiwerk? Wird er
öffentlich gezeigt oder nur das Bild? Und wer entscheidet bei einer Bestellung, die den Rahmen
verlässt — Ablehnung mit Vermerk, oder Nachbestellung? **Ich schreibe die Vorlage, wenn du
willst; gebaut wird erst nach dem Entscheid.**

## 1.5 Was das für §7 bedeutet

**§7 wartet auf diese Assets** — und wird dadurch besser. Drei Medaillons, die die Modelle selbst
bestellt haben, kreisen um die Zählmaschine, während gezählt wird. Das ist die Bewegung, die ich
beschrieben habe, mit einem Inhalt, den ich nicht hatte.

---

# Teil 2 · Entscheide zu Runde D

## 2.1 §8 Zählmaschine → **Weg 1** (Plakette + Aufwach-Licht jetzt, Ruck nachrüstbar)

CCs Befund ist richtig und mein Auftrag war an dieser Stelle blind: die Maschine ist flach ins
Plate gemalt, ein wörtliches Vorrücken der Zählglieder braucht ein Cutout, das es nicht gibt.

**Bauen: Hotspot, warmes Aufwach-Licht im `.lamp`-Muster, Hover-Plakette mit der
Aggregationsregel, i18n, §0-sicher.** Das löst den Steward-Befund vollständig — die Maschine
antwortet.

**Weg 3 (Ruck approximieren) ausdrücklich nicht.** Ein „subtiler Maschinen-Ruck" ohne trennbare
Ebene kann nur die ganze Kulisse bewegen. Die Räume haben eine Regel — **bewegt wird die zweite
Ebene, die Kulisse steht** — und die wird für einen Näherungseffekt nicht gebrochen.

Das Trommel-Cutout kommt mit der nächsten Bestellung (siehe 2.3). Der Ruck wird dann
nachgerüstet, ohne die Plakette anzufassen.

## 2.2 §7 Medaillons → **Weg 1** (zurückstellen)

Keine Platzhalter. Die Assets entstehen jetzt aus Teil 1 dieses Dokuments, und eine
Platzhalter-Bahn mit falscher Verdeckung müsste zweimal gebaut und einmal weggeworfen werden.

**Ausnahme, falls du sie willst:** die reine Bahn-Mechanik (rAF, Einflug, `--retreat`) ist
asset-unabhängig und könnte vorgezogen werden. Ich empfehle es nicht — die Verdeckung ist der
Punkt, an dem die Bahn steht oder fällt, und die lässt sich ohne Cutout nicht beurteilen.

## 2.3 Zwei Bestellungen, die jetzt fällig werden

1. **Zählmaschine als Vordergrund-Cutout**, freigestellt auf Magenta, aus dem Council-Plate
   heraus gedacht (gleiche Ansicht, gleiches Licht) — löst **beides**: den literalen Ruck in §8
   und die echte Verdeckung in §7.
2. **Drei Medaillons** nach den Bestelltexten der Modelle (Teil 1) — nach dem Wart-Entscheid.

Ob (1) generiert oder aus dem Plate geschnitten wird, prüft CC zuerst: der Freischnitt hat bei
den Türen zweimal getragen. CCs Befund „keytet nicht sauber gegen Dunkel" betrifft das
Magenta-Keying; ein **Freischnitt entlang der Kontur** ist etwas anderes und sollte vor der
Bestellung versucht werden. Trägt er, ist die Bestellung gespart.

---

# Teil 3 · Zwei Steward-Befunde

## 3.1 Die Council-Tür öffnet nicht mittig — vermutlich ein Fehler in allen drei Räumen

Der Verdacht: `perspective-origin` steht als **feste Prozentzahl des Viewports**, die
Aperturmitte wandert aber mit dem **Cover-Crop**. Sobald das Seitenverhältnis vom Messfall
abweicht, zielt die Kamera neben die Tür — im Council am sichtbarsten, weil dort zwischen
gemessener Hotspot-Mitte (50,7 % / 42,1 %) und gesetztem Origin (50,5 % / 48 %) ohnehin schon
sechs Punkte in y klaffen.

**Auftrag:** `perspective-origin` **zur Laufzeit aus derselben Cover-Rechnung** ableiten, aus der
auch der Hotspot seine Position bekommt — nicht als Konstante pflegen. Eine Quelle, wie beim
Ruhe-Stapel.

**Abnahme:** in allen drei Räumen bei 16:9, 21:9 und einem hohen schmalen Fenster liegt die
Fahrtachse auf der Türmitte; Abweichung in Prozentpunkten je Fall im Bericht.

## 3.2 „Wie gezählt wurde" — 2b ist nie gebaut worden

Der Entwurf (Pulte → Trichter → Trommel, ein Bereich im Fokus) ist die richtige Idee: er
**erzählt den Vorgang**, statt ihn zu tabellieren. Die heutige Liste ist der Zählstand, nicht
die Zählung.

Der Grund, warum er liegen blieb, steht in der Anmerkung des Entwurfs selbst: *„nur ein Bereich
zugleich — braucht Auswahl, §0-kritischer."* Inhalt, der erst nach einem Klick erscheint,
verletzt die Verfassung.

**Die Auflösung ist dieselbe wie überall auf dieser Seite: Schichtung.** Die vollständige Liste
aller vier Bereiche bleibt der Inhalt und steht ohne JS vollständig da. Der Zählstrang ist eine
**Bühne darüber**, die einen Bereich hervorhebt — sie erzeugt nichts, sie betont. Ohne JS und
bei `prefers-reduced-motion` sieht man die Liste, wie heute. Damit ist 2b baubar, ohne §0 auch
nur zu streifen.

**Das ist ein eigenes Paket** und gehört zum Protokoll-Explorer, nicht in Runde D — dieselbe
Frage („wie zeigt man den Vorgang, ohne den Wortlaut zu verlassen"), dieselbe Runde.

---

# Reihenfolge

1. §8 nach Weg 1 → Commit.
2. §3.1 Türmitte, alle drei Räume → Commit.
3. Freischnitt-Versuch Zählmaschine; trägt er nicht → Bestellung.
4. Wart-Vorlage zur Selbstdarstellung → Entscheid → Bestelltexte der Modelle → drei Medaillons.
5. §7 auf den echten Assets.
6. **Protokoll-Explorer inkl. 2b** — die letzte große Designlücke vor Go-Live.
7. Vor Go-Live: der gebündelte **Medien-Strang**.
