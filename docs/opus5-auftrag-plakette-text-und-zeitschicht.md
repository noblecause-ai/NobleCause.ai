# Ein Run: Plakettentext + Sitzinhaber + Zeitschicht

**Von:** Opus 5 (Architekt/Review) · **Für:** CC (Bau) · **Datum:** 2026-07-24
**Voraussetzung:** Commit `c87cb97` (Plakette an der Kopflinie) steht.
**Warum zusammen:** Beide Teile brauchen dieselben zwei Leser im Rooms-Layout und ändern
dieselben zwei Stellen (Plakette, Zeile unter der Röhre). Eine Runde, ein Review.

---

## §1 · Voraussetzung: die Daten von `master` holen

`origin/master` ist zwei Wochen voraus — `journal/2026-07-20/entry.json` existiert dort,
`master:schedule.json` steht auf `next_research: 2026-07-27` / `last_journal: /journal/2026-07-20/`.
Dieser Branch steht auf `07-20` / `07-08c`.

**Gegen die Branch-Daten gebaut, zeigt die Zeitschicht „letzte Prüfung 8. Juli" — falsch.**

`journal/**` und `schedule.json` sind auf `feat/*` Tabu-Pfade. Für genau diesen Fall gibt es
den Präzedenzfall im Repo: die Klartext-Datenpublikation `f3e67ed` wurde „sauber auf einem
Datenbranch erzeugt und per Fast-Forward hereingezogen (Guard-Hook nicht umgangen)".
**Derselbe Weg: `master` hereinziehen, dann bauen.** Kein `--no-verify`.

## §2 · Datenanbindung (einmal, trägt beide Teile)

`(rooms)/+layout.server.js` nimmt die zwei **bereits existierenden, bislang nicht
aufgerufenen** Leser aus `content.js` dazu: `getSchedule()` und `listJournalEntries()`.

Im View-Model zusätzlich exponieren — **wörtlich durchgereicht, keine Paraphrase, keine
Aggregation** (versiegelte Datennaht):

| Feld | Quelle | Für |
|---|---|---|
| `currentSession.ledBy` | `session.led_by.{model,label}` | Warden-Sitz |
| `lastResearch.date` | `listJournalEntries()[0].date` | „letzte Prüfung" |
| `lastResearch.model` | `…[0].model` | Scout-Sitz |
| `lastResearch.deputationNote` | `…[0].deputation_note` | Vertretung sichtbar machen |
| `lastResearch.convene` | `…[0].convene` | Warden-Entscheid |
| `schedule.nextSession` | `schedule.json.next_session` | Sitzungstermin |

**`schedule.json.next_research` wird NICHT gelesen** — der Wart-Termin wird aus dem Rhythmus
berechnet (§4.2).

**Wichtig zum Scout-Sitz:** Der letzte Research-Eintrag kann eine **Vertretung** sein.
`journal/2026-07-08c` trägt `model: kimi-k2` mit `deputation_note: "Durchgeführt von Kimi K2
(Moonshot AI) in Vertretung des Warts, auf Einberufung des Stewards."` Liegt eine
`deputation_note` vor, ist das anzuzeigen (mindestens als Vermerk), nicht zu glätten. Das ist
kein Sonderfall, das ist der Rekord.

## §3 · Die Plakette (Text, Sitz, Emblemreihe)

### 3.1 Copy — DE und EN als Spiegel (`de.js` / `en.js`)

**Gloss entfällt** (`gloss: 'der Späher'` / `'der Wart'`). Steward-Entscheid: nur die
englischen Bezeichnungen. Explizite Negationen („zählt nicht selbst") bleiben **draußen** —
sie werfen die Frage auf, die sie beantworten wollen. Der Punkt steht als „Wie gezählt wurde"
im Ratssaal.

```
The Scout · Aktuell: claude-fable-5
[Die Frage]  geht der Frage nach, welche Projekte und Organisationen dem Wohl der
             Menschheit in vier Bereichen am wirksamsten dienen.
[Zukunft] [Leid lindern] [Große Gefahren] [Was sonst übersehen wird]
```

```
The Warden · Aktuell: claude-fable-5
[Die Belege] prüft anhand der Belege des Scout, ob der Council einberufen wird.
             Falls ja, leitet er die Sitzung und veröffentlicht alles.
Zuletzt: nicht einberufen · 20. Juli 2026
```

### 3.2 Warum die Bereichsnamen NICHT im Satz stehen (gerechnet)

Die Tube rendert dieselben Medaillons mit `clamp(1.9rem, 4vw, 2.7rem)` = 30–43 px, die Tafel
mit 64 px. **Inline in einen 0,72-rem-Satz landen sie bei 17–20 px** — unter dem Boden, den
das Design für sie selbst setzt.

Und die Höhe: vier Bereichsnamen plus fünf Inline-Embleme ergeben bei 15 rem sechs bis sieben
Zeilen, bei 24 rem vier — mit Namens- und Sitzzeile **130–150 px**. Verfügbar sind bei 605 px
Höhe zwischen Masthead-Unterkante (229 px) und Kopflinie (369 px) genau **140 px**, im
günstigsten Zweig. Bei 1280 × 720 reicht es nicht.

**Als Reihe unter dem Satz stehen die vier Embleme bei ihren richtigen 1,9 rem**, sind
wiedererkennbar, und die Plakette bleibt bei ~90 px. Die Bereichsnamen stehen ohnehin direkt
daneben auf der Ergebnis-Tafel; im Satz wären sie Wiederholung, als Emblemreihe sind sie
Wiedererkennung. Steward-Entscheid 2026-07-24.

### 3.3 Emblem-Details

- **Karten-Sigel** vor dem Satz: Scout `/media/process/process-question-display.avif`
  („Die Frage"), Warden `/media/process/process-evidence-display.avif` („Die Belege") —
  dieselben Dateien wie die Tube, also echte Wiedererkennung.
- **Bereichsreihe:** `t.pillars.{A,B,C,D}.src`, alle vier, in der Reihenfolge A–D wie auf der
  Tafel und in der Klartext-Antwort.
- **Barrierefreiheit:** Die Reihe ist **nicht** dekorativ — sie trägt die vier Bereiche, die
  im Satz nicht mehr genannt werden. Also `alt={t.pillars[x].label}` je Emblem, nicht `alt=""`.
  Das Karten-Sigel dagegen wiederholt nur den Satz → `alt=""`.
- **Kein Tab-Stopp**, kein interaktives Element in der Plakette (StageTube-Regel).

### 3.4 Kein Link in der Plakette

Die Scout-Plakette sitzt bei `left: 72%` — gemessen x 543–758 bei 1305 px Breite. Der
Tür-Hotspot spannt dort über **x 480–825, y 165–795**. Die Plakette liegt also im klickbaren
Türfeld. Ein Link darin bräuchte `pointer-events: auto` und würde den Hotspot blockieren
(inklusive des `:hover`-Effekts, der die gemalte Tür öffnet); ohne `pointer-events` ist er
nicht klickbar. **Der Manifest-Link gehört in die persistente Zeile unter der Röhre** (§4.2) —
dort ist er auch auf Touch erreichbar, was er in einer Hover-Plakette nie wäre.

### 3.5 Höhenbudget

Ziel **≤ 95 px**. Nach dem Umbau ist „vollständig über der Kopflinie" bei **1280 × 720** und
**1440 × 700** neu nachzuweisen — bei 1280 klärte die Scout-Plakette die Tafel zuletzt nur um
10 px. Reicht es nicht: zuerst die Sitzzeile in die Namenszeile ziehen (`The Scout ·
claude-fable-5`), dann den Satz kürzen — **nicht** die Emblemreihe verkleinern, sie ist der
Grund für diese Fassung.

## §4 · Die Zeitschicht

Konzept mit Begründungen: `docs/opus5-zeitschicht-konzept.md`. Hier nur, was zu bauen ist.

### 4.1 Die Tafel bekommt Identität
`t.study.boardTitle`: „Die Antwort dieser Sitzung" → **„Die Antwort der letzten Sitzung"**,
darunter eine Datenzeile **„Sitzung {number} · {date}"** als `<time datetime="YYYY-MM-DD">`.
Formatierung per `Intl.DateTimeFormat` in der Raumsprache.
**Die Nummer muss mit:** alle drei Bestandssitzungen tragen `date: 2026-07-07`, `listSessions()`
sortiert deshalb nach `number` — ein Datum allein wäre mehrdeutig.

### 4.2 Persistente Zeile je Raum — Zeit lebt beim Akteur
- **Study** (unter der Röhre): Rhythmus + letzter belegter Lauf + Manifest-Link.
  *„Der Scout prüft jeden Montagmorgen. Letzte Prüfung: 20. Juli 2026. Die Bereiche und
  Kanons: Das Manifest ▸"* (Link → `/manifest`, dort stehen Artikel II und III.)
  **Der Termin wird aus dem Rhythmus berechnet** (nächster Montag 06:00 UTC, relativ zum
  Betrachtungszeitpunkt), **nicht** aus `schedule.json`. Damit kann er per Konstruktion nie in
  der Vergangenheit liegen: kein Überfällig-Zustand, keine Staleness-Logik, kein `buildTime`.
  Steward-Entscheid — „nichts extra hier".
- **Council:** Sitzungstakt. *„Der Council tagt, wenn genug Neues vorliegt. Nächste Sitzung
  geplant: 8. August 2026."* Aus `schedule.json.next_session`, formuliert als **Plan**. Liegt
  das Datum in der Vergangenheit: **Datumsangabe weglassen**, Rhythmussatz bleibt stehen. Kein
  zusätzlicher Zustand, nur das Ausbleiben einer unbelegten Behauptung.
- **Archive:** keine Zukunft. `home.archive[].date` ist vorhanden — prüfen, ob es im Regal
  sichtbar ist, und ergänzen wo nicht.

### 4.3 Der Countdown ist Verzierung
Relativangaben („in 3 Tagen") nur als JS-Zugabe. Ohne JS und bei Reduced-Motion steht das
absolute Datum — das ist der vollständige Zustand (§0). Nie ein Zähler als einzige Information.

### 4.4 „Wann" neben „Wie"
- **`/idee`** (Seite existiert): kurzer Abschnitt **„Wann was läuft"** — Scout wöchentlich
  montags · Council anlassbezogen, wenn genug Neues vorliegt · Veröffentlichung unmittelbar
  nach der Sitzung · **und zwischen den Läufen entscheidet kein Mensch.** Der letzte Satz ist
  der Punkt: der Takt ist Teil des Vertrauensversprechens, nicht Terminservice.
- **Ein Satz zum Takt** in den „Warum so umständlich?"-Ausklapp im Masthead — dort fragen die
  Leute nach.
- Optional: `t.tube.status()` ist schon eine Funktion, der Statussatz könnte den Takt aufnehmen.

## §5 · Abnahme

1. **Datenherkunft:** Alle neuen Werte kommen aus den Daten, keiner ist Copy. Gegenprobe:
   `lastResearch.date` zeigt **20. Juli 2026** (nicht 8. Juli) → beweist, dass `master`
   hereingezogen ist.
2. **Vertretungsfall:** Mit `journal/2026-07-08c` als jüngstem Eintrag (temporär simulieren)
   erscheint `kimi-k2` samt Vertretungsvermerk, nicht `claude-fable-5`.
3. **Plakette:** ≤ 95 px, vollständig über der Kopflinie bei **1280 × 720** und
   **1440 × 700**, Gesichter frei, Embleme bei 1,9 rem, Bereichs-`alt` gesetzt, kein Tab-Stopp,
   kein Link, `pointer-events` unverändert → Tür-Hotspot und `:hover`-Türöffnung intakt.
4. **Kein Überfällig-Zustand** im gesamten Code. Wart-Termin aus dem Rhythmus; bei
   verstrichenem `next_session` entfällt die Datumsangabe.
5. **No-JS / Reduced-Motion:** absolute Daten stehen, keine Relativangabe als einzige Quelle.
6. **i18n-Spiegel:** jeder neue String in `de.js` **und** `en.js`. Der publizierte Rekord
   bleibt in beiden Sprachen deutsch; Datumsformatierung ist keine Übersetzung.
7. Reflow 320/390, Build warnungsfrei, Testsuite grün, Preview neu gestartet.

## §6 · Danach: The Archive

Zu trennen:
- **Inhalt/Zeit im Archiv** (Daten am Regal, §4.2) — geht **jetzt**, braucht keine Assets.
- **Die Kulisse** — `archive-*` sind die alten Plates. **Codex Serie 3 (Register/Karteikästen)
  ist noch nicht geliefert.** Erst Lieferung, dann Gate, dann Einbau nach dem Kantenprinzip
  (Register von unten). Bestelldisziplin analog `docs/codex-serie-2-council.md`.

Das heißt: Archive-Inhalt kann direkt nach diesem Run beginnen, die Kulisse wartet auf Codex.
