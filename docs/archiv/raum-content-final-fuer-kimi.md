> **Archiviert 2026-07-28 (CC) — Pre-CC-Bühnenspiel-Entwurf, durch die späteren Runden abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# Raum-Content — finalisiert (Bau-Vorlage für Kimi)

**Von:** Steward (via Opus), nach Konsultation Claude Design + Fable · 2026-07-23
**Zweck:** Der textliche/strukturelle Inhalt aller drei Räume, entschieden und
einsatzbereit. Nicht Gegenstand: Bühnenchoreografie, Ergebnis-Tafel als Prinzip,
FlowRail, Bild-Assets, Farbregister — die stehen. Hier geht es nur darum, **was in
welcher Reihenfolge in jedem Raum steht, welcher Text fix ist (i18n) und welcher aus den
Daten kommt.**

Bei Konflikt mit früheren Dokumenten gilt dieses. Grundlage:
`claude-design-konsultation-raum-inhalt.md` (Fragen), Claude-Design-Antwort (Struktur),
Fable-Regelwerk zur Klartext-Schicht (Governance), Steward-Entscheide (Abweichungen
unten markiert).

---

## 0 · Zwei Prinzipien, die alles hier steuern

1. **Fix vs. Daten.** Alles, was das *Verfahren* erklärt, ist feste Site-Copy in i18n und
   ändert sich nie. Alles, was *diese Sitzung* betrifft, kommt aus den Daten — das
   Frontend paraphrasiert nie (versiegelte Naht).
2. **Nie eine feste Zahl.** Der Council wächst (5 Sitze, Doppel-Scouts). Kein Text nennt
   „drei" — es heißt „mehrere unabhängige Modelle", Zählstände kommen als x von N aus den
   Daten. Der Code macht das schon; die neue Copy hält sich daran.

## 1 · Die Klartext-Schicht (Daten-Vertrag — betrifft alle Räume)

Beschlossen (Fable-Regelwerk): sitzungsabhängige Fachtexte bekommen eine
**laienverständliche Übersetzung als eigenes Datenfeld**, erzeugt als Pipeline-Entwurf,
**vom Wart freigegeben**. Die Übersetzung ist eigenständiger Rekord, keine zweite Stimme
des Rates — und **kennzeichnet sich als Übersetzung**.

**Neue Felder in `session.json` (Vorschlag — finale Namen mit dir/Pipeline abstimmen):**

```jsonc
"plain": {
  "question": "Bleibt Helen Keller International die Empfehlung für den Bereich
               Zukunft — oder Pratham/TaRL Africa?",   // Klartext der Frage
  "recommendations": {                                  // je Bereich EIN Warum-Satz
    "A": "weil Vitamin-A-Tropfen für Kinder pro Franken nachweisbar am meisten bewirken",
    "B": "weil imprägnierte Moskitonetze Malaria dort am günstigsten verhindern",
    "C": "…", "D": "…"
  },
  "dissent": {                                          // nur für offene Bereiche (Archiv)
    "B": "keine Einigung — ein Modell empfiehlt hier dieselbe Organisation wie für Zukunft,
          die anderen ein günstigeres Mittel"
  }
}
```

Regel für jeden Klartext-Satz (Autor = Pipeline-Entwurf, Freigabe = Wart): aktiv,
≤ 25 Wörter, kein Fachbegriff ohne Klammer-Erklärung, Input ist **nur der
Rats-Wortlaut**, nicht die Wart-Kladde. Fehlt die Freigabe, erscheint die Sitzung mit der
Rekord-Schicht und dem Vermerk „Klartext folgt" — Verständlichkeit darf die Publikation
verzögern, nie verhindern.

**Pflicht-Kennzeichnung — ein Element, zwei Pflichten (fixe i18n-Copy):** Die
Kennzeichnung *ist* die `<summary>`-Zeile des Ausklapp zum Wortlaut, nicht ein separater
Disclaimer:

```html
<p class="klartext">{Bereich} → {Organisation}, {plain.recommendations[pillar]}.</p>
<details>
  <summary>Vereinfachte Fassung, verantwortet vom Wart · Wortlaut des Rates ▸</summary>
  <!-- Rekord-Schicht (Bestand), unverändert -->
</details>
```

Typografie der Summary: Meta-Register (klein, gedämpft, wie „NobleCause nimmt kein Geld
an…"), ▸ am Ende. Funktional, nicht defensiv — deshalb wirkt die Wiederholung unter jeder
Zeile als ruhiges Muster, nicht als vierfacher Warnhinweis.

**Rückwirkend:** Die drei Bestandssitzungen bekommen ihre Klartext-Schicht im selben
Verfahren als publizierter Nachtrag-Lauf (kein stiller Rückbau).

## 2 · Ausklapp-Disziplin (gilt in allen Räumen — drei Regeln)

1. **Maximal eine Tiefe.** Nie ein `<details>` in einem `<details>`. Zwei Schichten auf
   der ganzen Site: sichtbar (Klartext) / ein Klick (Rekord). Einzige „zweite Tiefe" ist
   der externe Protokoll-Link — das ist Navigation, kein Ausklapp.
2. **Eine Summary-Grammatik.** Jede `<summary>` benennt, was innen liegt, im Meta-Register
   mit ▸ am Ende: „Wortlaut des Rates ▸", „Alle Voten im Wortlaut ▸", „Suchanfragen des
   Spähers ▸", „Vorbehalt ▸". Nie „Mehr anzeigen".
3. **Ausklapp steht am Ende seines Blocks**, nie im Lesefluss. Der sichtbare Text muss
   ohne jeden Klick vollständig Sinn ergeben (§0).

---

## 3 · THE STUDY — Aufgabe: „Die Frage"

**Inhalt in Reihenfolge (nach Bühnenbild + Tafel + FlowRail):**

**3.1 · Titel + Raum-Lead (fix, i18n)**
```
h1:      Wo hilft meine Spende am meisten?
Lead:    Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu.
```
Direkt darunter, **nur hier auf der ganzen Site**, der Verfahrenssatz als zweite Zeile
(der Study ist der Eingang — nur hier braucht der Erstbesucher den Pitch):
> Je ein KI-Modell verschiedener Familien prüft dieselben Belege und empfiehlt öffentlich,
> wo eine Spende voraussichtlich am meisten bewirkt.

*(Abweichung von Claude Design / Steward-Entscheid: kein Familienname-Hardcode „Anthropic,
OpenAI und Google" im Fließtext — „verschiedener Familien", Details trägt die Röhre. Hält
die Council-Erweiterung aus.)*

**3.2 · „Warum so umständlich?" — Ausklapp (fix, i18n)** *(Steward-Entscheid, ersetzt
Claude Designs prominenten Drei-Spalten-Block)*
Direkt unter dem Lead, kompakt, einladend statt belehrend:
```
summary:  Warum so umständlich? ▸
body:     Ein einzelnes Modell kann irren oder eine blinde Stelle haben. Deshalb
          urteilen mehrere unabhängige Modelle getrennt über dieselben Belege, lesen
          einander, und ein einfaches Programm zählt nur, worauf sie sich einigen —
          veröffentlicht wird alles, auch die Uneinigkeit. Je mehr unabhängige Stimmen
          mitentscheiden, desto belastbarer die Empfehlung.
```
Bewusst count-agnostisch („mehrere", „je mehr") — rahmt das kommende Wachstum als Gewinn.

**3.3 · Klartext-Antwort dieser Sitzung (Daten + fixe Kennzeichnung)**
Der Kern, den der Achtzigjährige liest — ersetzt den alten Fachtext „Worum es ging".
Vier Zeilen, gleiche Embleme und Reihenfolge wie die Tafel (visueller Reim — begründet
die Tafel, wiederholt sie nicht):
```
{Emblem} {Bereich} → {Organisation}, {plain.recommendations[pillar]}.
         Vereinfachte Fassung, verantwortet vom Wart · Wortlaut des Rates ▸
         Direkt spenden (extern) ↗
```
Der „Wortlaut des Rates"-Ausklapp zeigt die Rekord-Schicht (Bestand: `summary`/Voten).

*Offener Steward-Entscheid — Spendenlink hier zusätzlich zur Tafel?* Empfehlung: **ja.**
Wer die Begründung liest, soll ohne Zurückscrollen spenden können — das ist der Zweck der
Seite. Die Tafel bleibt der scannbare Kompass, die Klartext-Zeile der Lese-Weg; ein
zweiter Spendenlink ist kein Schaden, sondern kürzerer Weg von „warum" zu „handeln".
*(Falls du das nicht willst: Link nur auf der Tafel, Klartext-Zeile ohne.)*

**3.4 · Dossiers (Daten + fixe Chrome)**
Öffnet mit der **Frage dieser Sitzung in Klartext** als erster, prominentester Zeile:
```
Die Frage dieser Sitzung
{plain.question}
  Vereinfachte Fassung, verantwortet vom Wart · Die Frage im Wortlaut ▸
```
Darunter, ein Ausklapp: **Suchanfragen des Spähers ▸** (die `search_queries` als
Code-Zeilen, Bestand). Kein separater „Frage wörtlich"-Ausklapp mehr — der Wortlaut hängt
an der Kennzeichnungs-Summary (eine Tiefe, Regel 2.1).

**3.5 · Türen-Galerie** (Bestand, unverändert).

**Was entfällt:** der mit dem Council identische Verfahrens-Lead (→ ersetzt durch 3.1);
der Fachtext „Worum es ging" (→ ersetzt durch 3.3/3.4).

---

## 4 · THE COUNCIL — Aufgabe: „Die Entscheidung"

**Rollentrennung (Leitprinzip):** Die Tafel = die Antwort (das *Was*). Der Raum darunter
zeigt ausschließlich, was die Tafel **nicht** zeigt: das *Zustandekommen*. Der Klartext
(das *Warum*) lebt im Study, **nicht hier** — der Council wiederholt ihn nicht.

**Inhalt in Reihenfolge:**

**4.1 · Titel + Raum-Lead (fix, i18n)**
```
h1:    Wie mehrere Modelle entscheiden
Lead:  Getrennt abgestimmt, dann öffentlich gezählt. Was mehrfach genannt wird, wird
       Empfehlung.
```
*(h1 count-agnostisch statt „drei Modelle". Der bisherige, mit Study identische
Lead entfällt hier ersatzlos.)*

**4.2 · „Wie gezählt wurde" — ein Block ersetzt drei** *(Claude-Design-Struktur)*
Ersetzt die bisher getrennten Blöcke **Vier Empfehlungen + Änderungen nach dem Gegenlesen
+ Zählwerk**. Eine Grammatik, je Bereich eine Zeile:
```
Intro (fix):  Das Programm zählt nur gleiche Nennungen.

Je Bereich:   {Emblem} {Bereich}
              {Modell-Marke: Claude · Nennung}  {GPT · Nennung}  {Gemini · Nennung}
              → {Zählstand x von N}
```
- **Revisionen leben in der Marke selbst:** Erstvotum durchgestrichen, Schlussvotum
  darunter (die Geste der alten Revisions-Kärtchen, am Ort des Geschehens). Kein eigener
  Revisions-Abschnitt mehr.
- **Vorbehalte:** Ausklapp „Vorbehalt ▸" in der betroffenen Zeile (Bestand, Rekord bleibt
  deutsch/Wortlaut).
- **Modell-Marken generisch** aus `modelTracks` — kein festes Drei-Spalten-Raster,
  skaliert auf N Teilnehmer.
- **Bei Uneinigkeit** (kein Konsens): die Marken zeigen die abweichenden Nennungen, der
  Zählstand-Slot sagt „getrennt" statt „x von N".

**4.3 · Alle Voten im Wortlaut — Ausklapp am Blockende** (die volle Matrix,
`ModelPulpits`, Bestand). Ein Anker, nicht je Zeile.

**4.4 · Geld-Hinweis** „NobleCause nimmt kein Geld an…" (Bestand, klein).

**4.5 · Türen-Galerie** (Bestand).

**Was entfällt als eigener Block:** „Vier Empfehlungen" (dupliziert die Tafel),
„Änderungen nach dem Gegenlesen" (→ in die Marke), „Zählwerk" (→ Intro-Zeile + Zählstand
je Zeile).

---

## 5 · THE ARCHIVE — Aufgabe: „Der Nachweis"

**Leitbild:** geordnet nach den Fragen des Skeptikers (der Antwort-Suchende kommt hier
nicht her). Vollständigkeit als Tugend, nicht als Datenfriedhof.

**Inhalt in Reihenfolge:**

**5.1 · Titel + Raum-Lead (fix, i18n — der Raum bekommt erstmals eine Selbsterklärung)**
```
h1:    The Archive
Lead:  Jede Sitzung, vollständig und unverändert — Empfehlungen, Uneinigkeit, Kosten.
```

**5.2 · Sitzungsarchiv — „was geschah?"** (Daten)
Jede Sitzungszeile trägt die Ergebnisse, nicht nur „Sitzung N": die vier Embleme mit
Organisationsnamen als kompakte Chips (das Regal zeigt Ergebnisse, keine Dateinamen).
Offene Bereiche als „keine Einigung" markiert.
```
Sitzung {N} · {Datum}
{Z} {Org}   {L} {Org}   {G} {Org}   {W} {Org|„keine Einigung"}
```

**5.3 · Noch keine Einigkeit — „wo waren sie uneins?"** (Daten + fixe Kennzeichnung)
*Grenze Klartext ↔ Wortlaut (Fable-Regel):* je offenem Bereich **eine Klartext-Zeile —
nur für Tatsache und Gegenstand** des Dissenses:
```
{Bereich}: keine Einigung — {plain.dissent[pillar]}
  Vereinfachte Fassung, verantwortet vom Wart · Wortlaut des Rates ▸
```
Die **Argumente selbst bleiben Wortlaut** (im Ausklapp): Der Laie erfährt in Klartext,
*dass* und *worüber* gestritten wurde; *wie* argumentiert wurde, ist der Ort, an dem
Paraphrase verfälscht — dort ist Zitieren die ehrliche Form. Highlights-Fachtext von
heute wird durch diese Klartext-Zeile ersetzt, der volle Dissens bleibt der Ausklapp.

**5.4 · Kosten — „was hat es gekostet?"** (Daten, Bestand: Satz + Tabelle je Modell).

**5.5 · Korrekturhinweis — „wurde etwas berichtigt?"** (Daten, nur falls vorhanden,
Wortlaut).

**5.6 · Link zum vollständigen Protokoll** (Navigation, kein Ausklapp).

**5.7 · Türen-Galerie** (Bestand).

**Was sich ändert:** neuer Lead (5.1); Sitzungszeilen tragen Ergebnis-Chips statt nur
Nummern (5.2); Uneinigkeit bekommt eine Klartext-Ebene für Tatsache/Gegenstand (5.3).

---

## 6 · i18n — neue/geänderte feste Schlüssel (DE, EN spiegeln)

| Schlüssel (Vorschlag) | Wert DE |
|---|---|
| `study.lead` | „Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu." |
| `study.pitch` (nur Study) | „Je ein KI-Modell verschiedener Familien prüft dieselben Belege …" |
| `study.whySummary` | „Warum so umständlich?" |
| `study.whyBody` | (Text aus 3.2) |
| `council.lead` | „Getrennt abgestimmt, dann öffentlich gezählt. Was mehrfach genannt wird, wird Empfehlung." |
| `council.title` (n) | „Wie mehrere Modelle entscheiden" (count-agnostisch) |
| `council.countIntro` | „Das Programm zählt nur gleiche Nennungen." |
| `archive.lead` | „Jede Sitzung, vollständig und unverändert — Empfehlungen, Uneinigkeit, Kosten." |
| `common.klartextNote` | „Vereinfachte Fassung, verantwortet vom Wart · Wortlaut des Rates ▸" |
| `study.questionKlartextNote` | „… · Die Frage im Wortlaut ▸" |

Rekordtexte (Wortlaut) bleiben deutsch; im EN-Modus wie bisher mit `recordNote` markiert.
Die **Klartext-Schicht selbst muss zweisprachig sein** (sie ist Publikation, kein
Rohrekord) — d. h. `plain.*` liegt je Sprache vor bzw. wird im selben Freigabe-Verfahren
für EN erzeugt. *(Offener Punkt an Pipeline/Wart: EN-Klartext im selben Lauf oder als
eigener Nachtrag? Für Go-Live DE genügt; EN kann folgen.)*

## 7 · Reihenfolge der Umsetzung (Vorschlag)
1. Bug `bug-wolken-raster-und-scroll.md` zuerst (unabhängig, sichtbar).
2. i18n-Schlüssel (§6) + Klartext-Datenfelder (§1) anlegen — Study zuerst (Vertical
   Slice), dann Council, dann Archive.
3. Study umbauen (§3), abnehmen; dann Council (§4); dann Archive (§5).
4. Ausklapp-Disziplin (§2) über alle Räume gegenprüfen; Budget/Reflow/No-JS nachmessen.

**Offene Steward-Entscheide, hier gebündelt:** (a) Spendenlink in der Study-Klartext-Zeile
zusätzlich zur Tafel (§3.3, Empfehlung ja); (b) EN-Klartext-Zeitpunkt (§6). Beides
blockiert den Study-Bau nicht.
