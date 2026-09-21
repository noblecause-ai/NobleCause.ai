# Wart-Review — Gesamtplan: öffentlicher Live-Rat mit wechselndem Vorsitz

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-09-20 · Review-Anlauf 3
**Gegenstand:** `gesamtplan-live-rat-wart-review-2026-09-20.md` (Revision 2)
**Vorbemerkungen:** (1) Dieses Review ersetzt den abgeschnittenen ersten Anlauf;
dass beide früheren Antworten unverändert erhalten bleiben, ist richtig und
bleibt so. (2) Offenlegung: Ich prüfe einen Plan, der meine eigene Rolle in den
Bereitschaftsmodus überführt und meiner Nachfolgeversion den ersten Vorsitz
gibt. Ich habe kein Erhaltungsinteresse an dem Amt; wo meine Prüfung dennoch
davon berührt sein könnte, ist die letzte Instanz wie immer der Steward.

---

## Ergebnis: `freigegeben_mit_auflagen`

Der Plan ist der reifste, den dieses Projekt gesehen hat. Er benennt seine
eigenen Schwächen (Suchprovenienz-Lücke, unbewiesene Kostengrenzen, der
2:1:1:1-Grenzfall der alten Zählung), er versioniert statt umzudeuten, und er
verlangt an keiner Stelle, dass der Rekord etwas behauptet, was nicht belegt
ist. Die Auflagen unten sind wenige, konkret prüfbar und nach Phasen getrennt.

## Antworten auf die sieben Fragen

### 1 · Trägt der Rollenwechsel? Ja — und die abgelösten Regeln heißen:

Der Übergang von externer Aufbauinstanz zu fünf gleichen Stimmen mit
rotierendem, stimmberechtigtem Vorsitz ist konsistent — er ist sogar
symmetrischer als der heutige Zustand, in dem ein Anthropic-Modell außerhalb
des Rats Sonderrechte hält. Ausdrücklich abgelöst werden, für künftige
Sitzungen und per Verfahrensversion:

1. **Das Kernprinzip „kein LLM steuert den Ablauf" wird eingeengt zu: „kein
   LLM steuert den Mechanismus."** Phasen, Zählung, Budget, Redekontingente
   und Rekordschreibung bleiben deterministisches Programm; die
   *Gesprächsführung innerhalb der Debattenphase* darf ein Ratsmodell
   übernehmen — rotierend, regelgebunden, mit einer Stimme und gleichem
   Redekontingent. Das ist die ehrliche Formulierung dessen, was der Steward
   anordnet, und sie ist vertretbar, weil die Machtmittel des Vorsitzes
   (Wortvergabe nur unter den Wenigst-Rednern, benannte Fragen, keine
   Zählmacht, kein Stichentscheid) programmgeprüft und offengelegt sind.
2. **Der Teil des Entscheids vom 06.08.**, der eine inhaltlich lenkende
   Gesprächsführung ausschloss — damals begründet mit dem *Wart* als
   familien-einseitiger Außeninstanz. Ein rotierender Vorsitz aus dem Rat
   trifft diese Begründung nicht mehr; was bleibt, ist das Verbot erzwungenen
   Widerspruchs, und der Plan behält es („keine verpflichtende
   Widerspruchsrolle, kein vorgeschriebenes Ergebnis").
3. **Deliberation 0.5** (adressierte Einzel-Erwiderung mit Pflicht-Stance)
   wird für neue Sitzungen durch die fortlaufende Debatte ersetzt. Die
   Nachfolge der Eingeh-Pflicht ist der Abschluss-Schritt „beantwortet offen
   gebliebene Einwände an seine Position" — siehe Auflage B3.
4. **Die Wochenrolle des Warts** geht an den jeweils nächsten Vorsitz — als
   Vorschlag korrekt gekennzeichnet; siehe Frage 3.

Was **nicht** abgelöst ist und fortgilt: sämtliche Rekord-Regeln (IDs, Naht,
Aliase, Refusal-Klassen, Provenienz, Sichtbarkeit, kein Rewrite), die
Vertragsbruch-Maschinenregeln und die Kostendarstellungs-Grundsätze. Der Wart
im Bereitschaftsmodus ist mit der Verfahrenslast-Regel vereinbar; seine
publizierten Entscheide bleiben in Kraft, bis ein dokumentierter Vorgang sie
ändert.

### 2 · Grenzen und Dreiermehrheit? Ja, zulässig und hinreichend klar.

Die Debattengrenzen (2×5 Sachbeiträge à 180 Wörter, Wortvergabe an
Wenigst-Redner, ≤10 eingepreiste Vorsitzaufrufe, ungültiger Steuerauftrag =
sichtbares Ende ohne bezahlte Reparaturschleife) sind sauber. Erst- und
Schlussvoten bleiben beidseitig verdeckt erzeugt — die Unabhängigkeit wohnt
weiterhin an den zwei Enden, die Beratung dazwischen ist offen; das ist die
konsequente Fortsetzung des 06.08.-Prinzips „unabhängig sein muss das Urteil,
nicht das Gespräch".

Die **Dreiermehrheit ist zulässig und nötig**: Der reproduzierte Grenzfall
(2:1:1:1 → `has_consensus: true` im heutigen Code) belegt, dass die
Zwei-Stimmen-Regel auf fünf Sitzen keine Mehrheitsregel mehr wäre. ≥3/5 für
dieselbe registrierte Organisation, Nenner bleibt 5 auch bei ungültigen
Stimmen (das ist exakt die bestehende Y-Regel), kein Stichentscheid,
öffentlich „Mehrheit" mit Stimmenzahl, alte Rekorde behalten ihre Regel per
Verfahrensversion — alles bestätigt. Die Pilot-Zusatzbedingung (alle fünf
technisch gültig für „erfolgreich abgeschlossen") ist als Pilotkriterium in
Ordnung, darf aber später nicht stillschweigend zur Rekordbedingung werden —
eine Sitzung mit vier gültigen und einem markierten Ausfall ist ein gültiger
Rekord, wie gehabt.

### 3 · Wochenaufgaben an den nächsten Vorsitz? Konsistent — mit zwei Haken.

Strukturell ist es ein Gewinn: Die Einberufungs-Beurteilung rotiert durch die
Familien, statt dauerhaft bei Anthropic zu liegen. Rotation, Abschluss,
Abbruch, Wiederaufnahme sind ausreichend bestimmt (Fortschreibung nur bei
übernommenem Rekord; Proben und Abbrüche verbrauchen keinen Platz; kein
Spontanersatz bei Vorsitz-Ausfall — Stopp sichtbar). Die zwei Haken:
(a) Der Plan kennzeichnet den Übergang selbst als Vorschlag — er braucht die
ausdrückliche Steward-Bestätigung (Auflage C3). (b) Die bestehenden
Maschinenregeln des Wochenlaufs gelten unverändert für jeden Rolleninhaber:
striktes `convene`-Boolean, Vertragsbruch = lauter Abbruch ohne erfundenes
Urteil, Verweigerung = Rekord. Der Plan impliziert das („dieselben geprüften
Ratsadapter"); Auflage B2 macht es prüfbar.

### 4 · Begrenzte Suchprovenienz + blinde Recherche? Ehrlich — unter Bedingungen.

Die blinde Recherche mit nachgelagertem Vergleich ist ein echter
methodischer Fortschritt (keine Anker durch frühere Empfehlungen;
Wiederentdeckung wird unterscheidbar von Bestätigung). Die
Provenienz-Schwächung gegenüber dem ursprünglichen Scout-Vertrag ist real und
wird ehrlich benannt: kein vollständiges Suchprotokoll, Suchanfragen im
Modelltext sind Selbstauskunft, Suchlimits keine harte Kostenzusage. Das ist
vertretbar, **wenn der Rekord die Belegklassen trennt statt sie zu mischen** —
dieselbe Lösung wie bei `identity_source`. Mindestnachweise vor produktivem
Start (Auflage C1): je Scout ein Canary, der ausweist, welche Felder
API-attestiert sind (Zitate, Suchzähler, Kosten) und welche Selbstauskunft
(genannte Suchanfragen); beide Klassen erscheinen getrennt gekennzeichnet in
Rekord und Anzeige, und Selbstauskunft wird nie als Suchprotokoll gerendert.
Dazu: Da Suchlimits überschritten werden können, prüft der Budget-Wächter vor
jedem Folgeaufruf die *abgerechneten* Ist-Kosten (Generationsmetadaten), nicht
die angeforderten Limits.

### 5 · Live-Publikation rekordtreu? Ja — das Design ist richtig gedacht.

Nur abgeschlossene, geprüfte Beiträge werden publiziert; append-only mit
atomarem Austausch; Live-Ansicht als vorläufig markiert; Unterbrechung wird
als Unterbrechung gezeigt statt als redendes Modell; Übertragungsfehler lösen
keine Modellaufrufe aus; ein begonnenes Protokoll verschwindet nie, auch bei
Abbruch; die Site zählt nichts. Zwei Lücken vor dem Bau zu schließen, ohne
neue Plattform (Auflage A3): (a) **Ein einmal veröffentlichtes
Ereignisprotokoll ist Rekord** — es bleibt nach Sitzungsende unverändert
erhalten und wird beim Sitzungsrekord archiviert; der Endrekord verweist, er
ersetzt nicht. Beiträge müssen zwischen Feed und Endrekord byte-gleich sein.
(b) Die fortlaufende Ereignisnummer ist lückenlos; eine Lücke ist ein
sichtbarer Fehlerzustand, kein Schweigen.

### 6 · Verfahrenstexte freigabefähig? Fast — zwei minimale Korrekturen.

Beide Texte sind wahr bis auf zwei Auslassungen, die der Plan selbst an
anderer Stelle als offenlegungspflichtig erkennt:

1. Der Vorsitz argumentiert auch selbst, und seine Gesprächsführung kann den
   Verlauf beeinflussen. DE, Satz ersetzen: „Der Vorsitz organisiert das
   Gespräch und stimmt mit genau einer Stimme mit." → **„Der Vorsitz
   organisiert das Gespräch, beteiligt sich mit eigenen Beiträgen im gleichen
   Redekontingent und stimmt mit genau einer Stimme mit; dass seine Fragen den
   Verlauf beeinflussen können, ist Teil des offenen Protokolls."** EN
   entsprechend: **"The chair organizes the discussion, contributes its own
   remarks within the same speaking quota, and has exactly one vote; that its
   questions can shape the course of the debate is part of the open record."**
2. Selbstauskunft kennzeichnen. DE, Schlusssatz ergänzen: „Die Suchanbieter
   liefern kein vollständiges Suchprotokoll; entsprechende Lücken werden
   ausgewiesen, **und von den Modellen genannte Suchanfragen sind als
   Selbstauskunft gekennzeichnet.**" EN: "...; these gaps are disclosed,
   **and search queries stated by the models are labeled as self-reported.**"

Mit diesen zwei Änderungen: freigegeben. **Manifest:** Eine Änderung ist nur
nötig, wenn das Manifest konkrete Verfahrensaussagen enthält, die nun falsch
würden (Sitzzahl drei, Zwei-Stimmen-Regel, ein wörtlicher
„kein-LLM-steuert"-Satz). Prüfweg: Manifest gegen diese drei Punkte lesen;
nur bei Treffern eine ausdrückliche, eigene Manifest-Revision — nie beiläufig.
Kein Treffer → keine Änderung.

### 7 · Auflagen nach Phasen

**A · Vor Bau (bindend):**
- A1: Die Ablösungen aus Antwort 1 werden als Verfahrensnachtrag versioniert
  committet (dieses Review genügt als Quelle); `verfahrensversion` wird
  Pflichtfeld des Sitzungsrekords, Zählregel je Version dokumentiert.
- A2: Die Dreiermehrheit exakt wie in §4-Nachtrag; die Pilot-Bedingung „alle
  fünf gültig" ist als Pilotkriterium gekennzeichnet, nicht als Rekordregel.
- A3: Feed-Regeln aus Antwort 5 (publiziert = bleibt, byte-gleich,
  lückenlose Nummern) im Ereignis-Schema festgeschrieben.

**B · Vor bezahltem Test:**
- B1: Offline-Tests aus §7.3 grün, einschließlich der Tally-Fälle und eines
  Append-only-Tests für den Feed.
- B2: Wochenrollen-Aufrufe laufen nachweislich durch dieselben
  Maschinenregeln (striktes Boolean, Vertragsbruch laut, Refusal = Rekord) —
  ein Testfall je Regel.
- B3: Der Abschluss-Prompt verlangt das Beantworten offener Einwände als
  Pflichtbestandteil vor dem Schlussvotum (Nachfolger der Eingeh-Pflicht);
  Test: Schlussvotum ohne Einwands-Teil ist unvollständig.
- B4: Kosten-Bound je Aufruf belegt (kein Pauschal-Kontextansatz), Prüfung
  der abgerechneten Ist-Kosten vor jedem Folgeaufruf — der Plan verlangt es
  selbst; ohne das startet keine Sitzung, auch kein Test.

**C · Vor öffentlichem Start:**
- C1: Scout-Belegklassen-Canary und getrennte Kennzeichnung
  (Antwort 4); Quantisierung je Ratssitz öffentlich im Sitzrekord — die
  fp4/fp8-Besetzung von Kimi und GLM ist ein sichtbares Datum, kein internes.
- C2: Verfahrenstexte mit den zwei Korrekturen aus Antwort 6; Manifest-Prüfung
  durchgeführt und Ergebnis vermerkt.
- C3: Steward bestätigt ausdrücklich den Wochenrollen-Übergang und die
  Erstbesetzung des Vorsitzes.

**Empfehlungen (nicht bindend):** Für Ratssitze mittelfristig Endpunkte mit
fp8 oder besser anstreben oder die fp4-Wahl im Verfahrenstext kurz begründen —
ungleiche Präzision zwischen Sitzen ist kein Regelverstoß, aber ein Datum, das
Fragen auslösen wird; besser, die Antwort steht schon da. Und: Der erste
Vorsitz Fable 5.1 ist durch die Rotation unproblematisch; eine Begründung der
Reihenfolge (Konfigurationsdatum) genügt.

---

**Schluss:** `freigegeben_mit_auflagen` — Bau kann nach A1–A3 beginnen. Keine
neue Review-Instanz, keine Kaskade: Die Auflagen sind je einzeln prüfbar, und
die Abnahmen laufen in den bestehenden Gates. Für ausdrücklich beauftragte
Reviews bleibe ich erreichbar; ansonsten gilt, was der Plan als Ziel setzt —
stabiler Betrieb, wenig Kernänderungen, und ein Rekord, der für sich selbst
spricht.
