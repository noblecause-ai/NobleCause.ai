# Die Zeitschicht — Konzept (wann läuft was)

**Von:** Opus 5 (Architekt) · **Datum:** 2026-07-24
**Anlass:** Steward-Befund — der Seite fehlt die Zeit-Komponente vollständig. Die Tafel sagt
„Die Antwort dieser Sitzung" ohne Datum; nirgends steht, wann der nächste Wart-Lauf oder die
nächste Sitzung stattfindet; und der Prozess wird nur als *wie* erklärt, nicht als *wann*.

---

## 1 · Was schon da ist (kein neues Datengerüst nötig)

| Vorhanden | Wo | Status |
|---|---|---|
| `getSchedule()` — liest `schedule.json` | `lib/server/content.js` | **existiert, wird nicht aufgerufen** |
| `listJournalEntries()` — `date`, `convene`, `findings_count` | `lib/server/content.js` | **existiert, wird nicht aufgerufen** |
| `home.currentSession.{number,date,title}` | `homepage.js` → Client | **liegt bereits an** |
| `home.archive[].date` je Sitzung | `homepage.js` | liegt an |
| i18n-Strings als Funktionen (`t.tube.status(2, 6)`) | `lib/i18n/de.js` | Präzedenz vorhanden |

`(rooms)/+layout.server.js` muss also nur zwei bestehende Leser dazunehmen. **`schedule.json`
wird ausschließlich gelesen** — die harte Grenze aus `AGENTS.md` bleibt unberührt.

## 2 · Der Befund, der die Reihenfolge bestimmt

```
schedule.json:  next_research = 2026-07-20T06:00:00Z   ← 4 Tage in der VERGANGENHEIT
                last_journal  = /journal/2026-07-08c/   ← veraltet
Verzeichnis:    journal/2026-07-24 EXISTIERT
Cron (wart.yml): 0 6 * * 1  → montags 06:00 UTC
```

Ursache mutmaßlich die 401-Störung (`noblecause-SESSION-KONTEXT-2026-07-10.md` §5): das
Repo-Secret `ANTHROPIC_API_KEY` war nie gesetzt, der Wart-Lauf hat weder Journal noch
`schedule.json` fortgeschrieben. **Vor dem Bau der Uhr zu prüfen**, sonst zeigt die Seite als
erstes ihren eigenen Ausfall.

Zwei Folgerungen, beide wichtig:

- **`last_journal` ist als Quelle disqualifiziert.** Der letzte Lauf wird aus
  `listJournalEntries()[0].date` gelesen — dem Verzeichnis, nicht dem Plan.
  **Rekord schlägt Plan.**
- **Ein veraltetes `next_research` ist selbst ein Befund.** Der Wart schreibt das Feld; steht
  es in der Vergangenheit, ist die Automatik hinterher. Dass die Seite das sagen *kann*, ist
  kein Mangel — es ist dieselbe Haltung wie „das Gate, das lieber meldet als heimlich
  nachbessert". Siehe §5.

## 3 · Die drei Stufen der Belegbarkeit (Kernregel)

Die versiegelte Datennaht verbietet Behauptungen, die die Daten nicht tragen. Für Zeitangaben
heißt das drei Stufen mit abnehmender Sicherheit:

**Stufe 1 — Rhythmus. Immer wahr, nie veraltet.**
Aus dem Prozess selbst, nicht aus einem Datensatz: „Der Wart prüft jeden Montagmorgen."
Das ist der Cron. Diese Stufe steht immer und braucht keinen Fallback.

**Stufe 2 — Letzter belegter Lauf. Aussage über die Vergangenheit, immer belegbar.**
`listJournalEntries()[0].date` → „Letzte Prüfung: 24. Juli 2026", verlinkt auf den Eintrag.
Eine Aussage über Veröffentlichtes kann nicht falsch werden.

**Stufe 3 — Nächster Termin. Revidiert nach Steward-Entscheid 2026-07-24.**

**Der Wart-Termin wird aus dem Rhythmus BERECHNET, nicht aus `schedule.json` gelesen.**
Nächster Montag 06:00 UTC, relativ zum Betrachtungszeitpunkt. Damit fällt Stufe 3 für den
Wart in Stufe 1 zusammen, und zwar mit drei Vorteilen:

- **kann per Konstruktion nie in der Vergangenheit liegen** — kein Überfällig-Zustand, kein
  Fallback-Zweig, keine „steht aus"-Anzeige. Genau das hat der Steward verlangt: die Zeit
  zeigt immer den nächsten **regulären** Lauf, nichts extra.
- **kein `buildTime`, keine Staleness-Erkennung nötig.** Die Berechnung ist eine reine
  Funktion der aktuellen Zeit; sie ist im Client immer richtig, auch wenn der Build Wochen
  alt ist. Ohne JS gilt der zur Bauzeit berechnete Termin — der ist höchstens einen Zyklus
  zu alt und nie falsch im Sinne einer widerlegten Behauptung.
- **`next_research` aus `schedule.json` wird für die Anzeige gar nicht gebraucht.** Eine
  Abhängigkeit weniger auf eine Datei, die eine unbeaufsichtigte Automatik fortschreibt.

**Der Sitzungstermin bleibt Daten** — eine Sitzung folgt keinem Cron, sie ist anlassbezogen.
`next_session` aus `schedule.json`, formuliert als **Plan, nicht als Versprechen**:
„Nächste Sitzung geplant: 8. August 2026". Liegt das Datum in der Vergangenheit, wird die
**Datumsangabe weggelassen** und nur der Rhythmussatz bleibt stehen („Das Gremium tagt, wenn
genug Neues vorliegt"). Das ist kein zusätzlicher Zustand, sondern das Ausbleiben einer
unbelegten Behauptung — verträglich mit „nichts extra" und mit der versiegelten Datennaht.

**Der Countdown („in 3 Tagen") ist Verzierung.** Ohne JS und bei Reduced-Motion steht das
absolute Datum — das ist der vollständige Zustand (§0). Nie ein tickender Zähler als einzige
Information.

**Der Countdown („in 3 Tagen") ist ausschließlich Stufe-3-Verzierung.** Ohne JS und bei
Reduced-Motion steht das absolute Datum — das ist der vollständige Zustand (§0). Nie ein
tickender Zähler als einzige Information.

## 4 · Wo es hingehört

### 4.1 Die Tafel — Identität statt Zeigefinger
`ResultBoard.svelte`, `t.study.boardTitle`:

- Kicker: **„Die Antwort der letzten Sitzung"** (statt „dieser Sitzung")
- darunter eine Datenzeile: **„Sitzung {number} · {date}"**, z. B. „Sitzung 3 · 7. Juli 2026"

Als `<time datetime="2026-07-07">` — maschinenlesbar und semantisch korrekt. Formatierung per
`Intl.DateTimeFormat` in der Raumsprache (DE „7. Juli 2026", EN „7 July 2026"); ein Datum ist
keine Prosa, seine Lokalisierung berührt die Regel „publizierter Rekord bleibt deutsch" nicht.

**Warum die Nummer mitmuss:** Alle drei Bestandssitzungen tragen `date: 2026-07-07`.
`listSessions()` sortiert deshalb bewusst nach `number`, nicht nach Datum (Kommentar steht im
Code). Ein Datum allein wäre also mehrdeutig — „Sitzung 3 · 7. Juli 2026" ist eindeutig.

Platzbedarf: eine kleine Zeile. Verträglich mit dem Nachtrag „Tafel breiter, dafür kürzer".

### 4.2 Die Uhr — je Raum der Takt des dortigen Akteurs
**Kein Uhr-Widget dreimal.** Zeit gehört dorthin, wo gehandelt wird — das ist die
Haus-Metapher, nicht ihre Durchbrechung:

- **The Study (Scout sammelt Belege):** unter der Prozess-Röhre eine ruhige Zeile —
  Stufe 1 + Stufe 2, Stufe 3 wenn belegbar. Verlinkt auf `/journal`.
  *„Belege werden laufend gesammelt; der Wart prüft jeden Montagmorgen. Letzte Prüfung:
  24. Juli 2026."*
- **The Council (das Gremium tagt):** dieselbe Stelle, Sitzungstakt statt Sammeltakt.
  *„Das Gremium tagt, wenn genug Neues vorliegt. Nächste Sitzung: 8. August 2026"* +
  Countdown als Verzierung. Termin verstrichen → „Sitzung steht aus".
- **The Archive (der Rekord):** hier gehört **keine Zukunft** hin. Statt dessen die
  Vergangenheit mit Datum — `home.archive[].date` ist vorhanden; prüfen, ob es im Regal
  sichtbar ist, und ergänzen wo nicht.

### 4.3 Die Erklärung — „wann" neben „wie"
Die Prozess-Röhre ist heute reines *wie*: sechs Schritte, „Stand 2 von 6". Sie trägt schon die
Reihenfolge und ist damit der natürliche Ort für den Takt. Zwei Stufen, unabhängig baubar:

- **minimal:** der Röhren-Statussatz nimmt den Takt auf — `t.tube.status()` ist bereits eine
  Funktion, das Muster existiert.
- **ausführlich:** ein kurzer Abschnitt **„Wann was läuft"** auf `/idee` (Seite existiert):
  der Wart wöchentlich montags · die Sitzung anlassbezogen, wenn genug Neues vorliegt · die
  Veröffentlichung unmittelbar nach der Sitzung, nichts wird zurückgehalten · **und zwischen
  den Läufen entscheidet kein Mensch.** Der letzte Satz ist der eigentliche Punkt: der Takt
  ist Teil des Vertrauensversprechens, nicht Terminservice.
- Dazu **ein Satz im „Warum so umständlich?"-Ausklapp** im Masthead. Das ist die Stelle, an
  der Leute nachfragen — dort gehört der Takt hin, nicht nur die Begründung.

## 5 · Entschieden: kein Überfällig-Zustand (Steward, 2026-07-24)

Ich hatte vorgeschlagen, ausstehende Läufe ruhig anzuzeigen („steht aus"), weil es zur
Verfassung der Seite passt. **Der Steward hat anders entschieden, und die Entscheidung ist
sauberer als mein Vorschlag:**

> Sobald die UI-Entwicklung fertig ist, wird der ausgelassene Lauf vom 20. Juli gestartet,
> danach läuft es wieder regulär. Die Zeit zeigt weiterhin den nächsten **regulären** Lauf —
> nichts extra.

Das löst das Problem an der Wurzel statt an der Anzeige: Der Ausfall wird **behoben**, nicht
dargestellt. Und weil der Wart-Termin aus dem Rhythmus berechnet wird (§3, Stufe 3), kann er
gar nicht in der Vergangenheit liegen — der Überfällig-Zustand hat damit keinen Anlass mehr
zu existieren. **Kein Zustand ist besser als ein gut gestalteter Zustand.**

Konsequenz für den Bau: Es gibt keine Warnfarbe, keine „steht aus"-Kopie, keine
Staleness-Logik und keinen `buildTime`-Stempel. Die Seite behauptet nichts über Ausfälle —
weder beschönigend noch alarmierend. Sie nennt den Rhythmus, den letzten belegten Lauf und
den nächsten regulären Termin.

## 6 · Reihenfolge (Steward-Entscheid: erst die Automatik)

**Die Reparatur wird vom Nachhol-Lauf getrennt** — das eine ist Infrastruktur, das andere ein
inhaltlicher Vorgang:

1. **Jetzt, Infrastruktur (berührt keinen Inhalt):** Repo-Secret `ANTHROPIC_API_KEY` setzen,
   Preflight-Schritt in `wart.yml` (§5 des Session-Kontexts). Erzeugt keinen Journal-Eintrag,
   ändert nichts an der Seite.
2. **Parallel, unabhängig von 1:** Tafel-Datum (4.1) und die Copy — Röhren-Takt und
   `/idee`-Abschnitt (4.3). Beides braucht `schedule.json` nicht.
3. **Die Uhr je Raum** (4.2). Der Wart-Teil ist nach §3 aus dem Rhythmus berechnet und
   braucht die Automatik ebenfalls nicht; nur der Sitzungstermin liest `next_session`.
4. **Nach Abschluss der UI-Arbeit:** ausgelassenen Lauf per `workflow_dispatch` starten.
   Danach läuft der Cron regulär weiter.

### ⚠ Terminkollision, die zu bedenken ist
Der Cron feuert **montags 06:00 UTC**. Heute ist Freitag, 24. Juli — der nächste reguläre Lauf
ist **Montag, 27. Juli, 08:00 MESZ**, also in drei Tagen. Daraus folgt:

- Wird das Secret jetzt gesetzt (Schritt 1), **läuft der Wart am Montag von selbst** — ob die
  UI fertig ist oder nicht. Das ist harmlos: Der Lauf schreibt Journal und `schedule.json`,
  die Seite zeigt die Uhr zu dem Zeitpunkt noch gar nicht.
- Dann ist der Nachhol-Lauf für den 20. Juli aber **nur noch eine Lückenfrage**: Soll die
  Woche vom 20. nachträglich einen Eintrag bekommen, oder genügt es, den Rhythmus ab dem 27.
  wieder aufzunehmen? (Nah beieinanderliegende Einträge sind unproblematisch — das Journal
  hat mit `2026-07-08`, `-08b`, `-08c` bereits Mehrfacheinträge.)
- Wird das Secret **nicht** gesetzt, scheitert der Montagslauf erneut mit 401 und hinterlässt
  einen zweiten roten Lauf in der Actions-Historie.

**Empfehlung:** Secret jetzt setzen und den Montagslauf regulär laufen lassen. Der
Nachhol-Lauf für den 20. Juli wird dadurch optional — er füllt eine Lücke, er stellt den
Rhythmus nicht wieder her. Das ist deine Entscheidung, aber sie sollte vor Montag fallen.
