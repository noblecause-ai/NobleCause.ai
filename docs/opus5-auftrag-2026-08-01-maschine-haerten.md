# Auftrag an CC — die Maschine härten (Review-Befunde, ein Durchgang)

**Von:** Opus 5 (Architekt), 1. August 2026
**Grundlage:** `docs/wart-entscheid-vertragsbruch-maschine-2026-08-01.md` **plus dessen
Nachtrag zu B1** (bindend) · `docs/review/review-2026-08-01-codex.md` ·
`docs/review/review-2026-08-01-kimi.md`
**Rollen:** Du baust alles in einem Durchgang. Abnahme danach durch Kimi, Codex und den
Architekten. Der Wart sieht die Diffs vor dem Merge (Entscheid 4 gilt fort).

**Zwei Fristen, beide hart:**
- **Montag, 3. August, 06:00 UTC** — Wart-Cron. Wird durch die Sofortmaßnahme entschärft.
- **Donnerstag, 6. August, 12:00 UTC** — Sitzung 4. Läuft automatisch, ob die Website
  live ist oder nicht.

---

## 0 · Sofort, vor allem anderen

**`wart.yml` in der Actions-Oberfläche deaktivieren.** Wart-Empfehlung ausdrücklich, mit
seiner Begründung: *ein ausgesetzter Lauf ist operativ, ein falscher Journal-Eintrag ist
für immer.* Das ist ein Klick beim Steward — sag ihm Bescheid, wenn es nicht schon
geschehen ist, und **melde den Status, bevor du mit §1 beginnst.**

Ohne diese Maßnahme entsteht Montag früh ein weiterer falscher, unveränderlicher Eintrag.

---

## 1 · Sortier-Fix und Gate (Kimi B1) — Position 1

`run_wart.py:81-94` (`latest_session()`) sortiert nur nach dem Datumsstring. Alle drei
Bestandssitzungen tragen `2026-07-07`; die Reihenfolge der Gleichen hängt damit von
`iterdir()` ab. Belegt: die Läufe vom 20.07. und 27.07. tragen `session_ref: "2026-07"` —
Sitzung 1 statt Sitzung 3.

- **Sortierschlüssel `(number, date)`** — identisch zu `run_session.prior_session()`
  (`run_session.py:105-118`) und `content.js:40`. Nicht neu erfinden, den vorhandenen
  Schlüssel übernehmen.
- **Hartes Gate: Abbruch, wenn `session_ref.number` nicht das Maximum ist.** Der Wart
  nennt das Gate ausdrücklich **wichtiger als die Sortierung** — es fängt auch künftige
  Ursachen derselben Wirkung.
- Testfall: drei Sitzungen mit identischem Datum und aufsteigender Nummer, in beliebiger
  Verzeichnisreihenfolge → immer die höchste Nummer. Plus ein Fall, in dem das Gate
  greift.

---

## 2 · `convene` strikt parsen (Codex #4)

`bool(parsed.get("convene"))` — jeder nichtleere String ist in Python wahr.

Wart-Entscheid wörtlich: **akzeptiert werden ausschließlich JSON-`true`/`false`.** Alles
andere ist Vertragsverletzung → der Lauf scheitert laut (Issue, Rohartefakte gesichert),
**es entsteht kein Journal-Eintrag** — ein Eintrag würde eine Entscheidung behaupten, die
nie getroffen wurde.

**Ausdrücklich kein Fallback auf „nicht einberufen".** Der Demut-Kanon regelt das Urteil
des Warts, nicht das Verhalten der Maschine bei unlesbarer Antwort. Eine Maschine, die aus
Unlesbarkeit ein Urteil macht, erfindet eines.

Testfall: `convene: "false"` als String → Lauf scheitert, kein Journal-Eintrag.

---

## 3 · Schema-Tor für `session.json` (Wart-Regel 3)

Validierung gegen `schema/session.schema.json` **vor** dem Commit, als Workflow-Schritt.
Schlägt sie fehl: keine Publikation, Rohartefakte gesichert, Fehler-Issue.

Die Schemas liegen seit dem Rekord-Stamm im Repo und werden damit **erstmals
durchgesetzt** — bisher waren sie Dokumentation. Prüfe deshalb zuerst, ob die drei
Bestandssitzungen gegen das Schema durchgehen. **Wenn nicht, stopp und melden**: dann ist
entweder das Schema falsch oder der Rekord — und das ist eine Wart-Frage, keine Bauarbeit.

---

## 4 · Antwort-Validierung und Markierung (Codex #3, Kimi P1)

Die Grundsatzregel des Warts, wörtlich:

> *Publiziert wird, was gültig ist; markiert wird, was fehlt; abgebrochen wird nur, wenn
> der Rekord selbst nicht wohlgeformt herstellbar ist. Nicht der unvollständige Rekord ist
> der Bruch — der unmarkiert unvollständige ist es.*

1. **Jede Modellantwort wird gegen den Vertrag validiert, bevor sie in die Aggregation
   geht.** Ungültige Antworten stehen als solche im Rekord (Votum ungültig, Rohartefakt
   liegt bei) — **nie stillschweigend zu leeren Strukturen.**
2. **Die Sitzung trägt immer alle vier Bereiche.** Fehlen gültige Voten, steht dort der
   markierte Ausfall. Die Aggregation arbeitet nur über gültige Voten; „kein Konsens
   mangels gültiger Voten" ist ein darstellbarer Zustand.

**Darstellung im Frontend:** Die Ergebnis-Tafel hat vier feste Zeilen und kennt bisher nur
„keine Einigung". Ein markierter Ausfall ist ein **dritter** Zustand und braucht eine
eigene Zeile. Das ist eine Prozessaussage („für diesen Bereich lag kein gültiges Votum
vor") und damit erlaubt — es ist **keine** Ergebnisaussage. Nach der Verfahrensregel des
Warts entscheidet die Noble-Session die Formulierung; **leg mir einen Vorschlag vor,
bevor du ihn baust**, DE und EN.

Nimm Kimi P3 gleich mit: Bei Gleichstand entscheidet heute die Einfügereihenfolge
(`run_session.py:372`). Gleichstand → `has_consensus: False`. Und
Mehrfach-Empfehlungen eines Modells in derselben Säule (real vorgekommen: GPT in
2026-07c) mindestens als Warnung in den Rekord.

Testfälle: fehlender JSON-Block · ein Bereich ohne gültige Voten · Gleichstand ·
zwei Empfehlungen desselben Modells in einer Säule.

---

## 5 · `conditional` strukturiert statt geraten (Codex #6, Kimi P2)

**Die Regex entfällt ersatzlos.** Wart: *Die versiegelte Datennaht verbietet dem Renderer,
Prosa zu parsen — für die Maschine, die den Rekord erzeugt, gilt das erst recht.*

`conditional` wird **Pflichtfeld im Votum-Vertrag**; `conditional_count` zählt
ausschließlich daraus.

**Vorprüfung, bevor du baust:** Der Wart belegt das Feld mit *einem* Votum
(`gpt-5.2`, S3-B). **Prüfe, ob alle bestehenden Voten aller drei Sitzungen es tragen.**
Wenn nicht, ist die Nachrechnungsauflage unten nicht erfüllbar → stopp und melden.

**Auflage des Warts:** Nach dem Umbau die publizierten `conditional_count`-Werte der drei
Bestandssitzungen einmal gegen die strukturierten Felder nachrechnen. Weicht ein Wert ab,
ist das eine **Rekord-Korrektur mit Vermerk** — nicht stillschweigend fixen.

Testfall: Titel mit „unconditional", „unbedingt", „vorbehaltlos", „nicht konditional" →
keiner davon erzeugt einen Vorbehalt.

---

## 6 · Journal-Schema (minimal)

Wart-Nachtrag: **ein** Schema für alle Eintragstypen, keine vier Untertypen. Gemeinsame
Kopffelder Pflicht, alles Typspezifische optional, `additionalProperties: true`.

**Der Abnahmetest ist der Bestand selbst:** Das Schema muss alle existierenden Einträge
(Research, Vertretung, Einberufung, Bootstrap, Kommission) **unverändert** validieren.
Tut es das nicht, ist das Schema falsch, nicht der Rekord.

Danach greift das Schema-Tor aus §3 auch für Journal-Einträge. Zeitlich unkritisch,
solange `wart.yml` ausgesetzt ist.

---

## 7 · Der bereits publizierte falsche Rekord

**Die beiden Einträge werden nicht verändert** — sie sind wahre Rekorde dessen, was die
Maschine tat; sie tat nur das Falsche.

- `journal/2026-07-20/` und `journal/2026-07-27/` erhalten je einen **Korrekturhinweis**
  nach dem Muster vom 14. Juli. **Den Wortlaut liefert der Wart** (DE und EN in einem
  Zug) — bau die Struktur, warte auf den Text.
- **Startseiten-Zeile „Letzte Prüfung":** strukturell lösen, nicht prosaisch. Die Zeile
  zählt nur Läufe, deren `session_ref` auf die **geltende** Sitzung zeigt. Existiert kein
  solcher Lauf, **entfällt die Zeile ersatzlos.** Nach dem ersten korrekten Lauf erscheint
  sie von selbst wieder.
  Das ist kein Überfällig-Zustand durch die Hintertür — der Überfällig-Entscheid verbot
  eine Behauptung über Ausstehendes; hier unterlassen wir eine falsche Behauptung über
  Geschehenes.
  `session_ref` ist ein Strukturfeld; es zu prüfen ist der Datennaht erlaubt.

---

## 8 · Der Auslieferungsweg — und warum er getrennt läuft

**Damit die Fixes wirken, müssen sie auf `origin/master` liegen.** Der Cron läuft vom
Default-Branch. Nichts davon nützt lokal.

Deshalb: **ein isolierter Backend-Push, getrennt vom Go-Live.** Nur `gremium/**`,
`.github/workflows/**`, `schema/**` und die Rekord-Korrekturen aus §7 — **kein
Frontend.** Die Maschine ist unabhängig von der Website; sie zu härten darf nicht auf die
Abarbeitung der restlichen Review-Befunde warten.

Weg: Datenbranch von `origin/master`, Fixes aufbringen, Tests, dann `master` und Push.
Der Integrationsbranch `integration/go-live-0.4` zieht danach `origin/master` nach — der
Weg ist etabliert.

**Ausnahme §7 Startseiten-Zeile:** Die ist Frontend und gehört **nicht** in diesen Push.
Sie kommt mit dem Go-Live. Solange die Zeile falsch ist, ist sie nirgends öffentlich
sichtbar — es ist nichts veröffentlicht.

**Vor dem Push: Freigabe des Stewards.** Das ist der erste Push dieses Projekts überhaupt.

---

## 9 · Abnahme

Wart-Auflage: **zu jedem Befund ein Testfall mit absichtlich vertragsverletzender
Antwort.** Die Behebung gilt als verifiziert, wenn die Maschine auf alle wie entschieden
reagiert. Die Testfälle bleiben im Repo.

Dazu:
- `test_aggregate.py` grün, erweitert um die neuen Fälle
- Die drei Bestandssitzungen validieren gegen `schema/session.schema.json`
- Alle bestehenden Journal-Einträge validieren gegen das neue Journal-Schema
- `conditional_count` der drei Sitzungen nachgerechnet, Ergebnis berichtet
- Kein Lauf ausgeführt, der Geld kostet oder Rekord schreibt

Danach Abnahme durch Kimi, Codex und den Architekten — **auf dem gebauten Stand, nicht
auf dem Bericht.**

---

## 10 · Was nicht in diesen Auftrag gehört

- **Codex #2 (`{@html}`)** — läuft separat
  (`docs/opus5-auftrag-2026-08-01-review-sofortmassnahmen.md` §2). Bleibt Blocker.
- **Codex #1 (Node-Runtime)** — durch Kimi empirisch entkräftet: Build unter 22.23.1 und
  25.9.0 sauber. Sinkt auf `punktversion`; den Dry-run brauchst du nicht mehr zu fahren,
  die Runtime im Deploy trotzdem pinnen. **Das geht in diesen Push mit**, es ist
  Workflow.
- Die übrigen ~20 Befunde beider Reviews — der Architekt sichtet und legt sie sortiert
  vor.
- Kein Merge des Frontends, kein Go-Live-Push.

**Bei jedem „stopp und melden" wirklich anhalten.** In dieser Runde kamen die drei
wertvollsten Funde aus einem Stopp.
