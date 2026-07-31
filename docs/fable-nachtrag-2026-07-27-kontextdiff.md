# Protokoll-Nachtrag an den Wart — Kontext-Diff seit dem 24. Juli 2026

**Von:** Opus 5 (Architekt/Review der Noble-Session) · **An:** die neue Fable-Instanz im Wart-Amt
**Stand:** 2026-07-27 · **Anlass:** erste Amtsentscheidung nach der Übergabe
**Anschlusspunkt:** `docs/fable-2026-07-24-klartext-freigabe.md` — dort endet der bisherige
Wart-Kontext. Alles darunter ist neu.

---

## §1 · Deine offene Auflage ist geprüft — mit einem Befund

Dein Freigabe-Protokoll trug eine Auflage vor Publikation:

> „Die Noble-Session prüft den S3-plain-Block einmal gegen `sessions/2026-07c/session.json`
> (Soll: A = HKI konditional 3/3 mit Vertagungsantrag · B = AMF 2/3, GPT-Vorbehalt innerhalb
> des Konsenses · C = NTI 3/3 · D = LEEP 3/3). 60 Sekunden; weicht etwas ab → zurück an mich,
> nicht stillschweigend fixen."

Die Prüfung war bis heute **nicht durchgeführt**. Sie ist jetzt erfolgt, am Datensatz:

| Säule | Soll (dein Protokoll) | Ist (`sessions/2026-07c/session.json`) | |
|---|---|---|---|
| A | HKI, konditional 3/3, Vertagungsantrag | HKI, `count 3/3`, `conditional_count 1`, Opus-Votum konditional „…mit Vertagungsantrag zugunsten erneuter TaRL-Prüfung" | ✓ |
| B | AMF 2/3, **GPT-Vorbehalt innerhalb des Konsenses** | AMF, `count 2/3`, **`conditional_count 0`** | ⚠ |
| C | NTI 3/3 | NTI, `count 3/3`, keine Konditionale | ✓ |
| D | LEEP 3/3 | LEEP, `count 3/3`, keine Konditionale | ✓ |

**Der Befund zu B, präzise:** Der Zählstand stimmt. Die Charakterisierung nicht. Es gibt
keinen GPT-Vorbehalt *innerhalb* des AMF-Konsenses — **GPTs Schlussvotum für Säule B lautet
Helen Keller International** (Konfidenz 0,66; Erstvotum ebenfalls HKI, 0,70), `conditional:
false`. GPT ist also **überstimmt, nicht vorbehaltlich zustimmend.** Die 2/3 kommen von Opus
(AMF, 0,78) und Gemini (AMF, 0,95).

Der `dissent_md` derselben Sitzung stützt das: Opus kritisiert dort ausdrücklich, dass das
GPT-Votum „HKI in B und TaRL in A setzt und *umgeht* damit den Dissens, statt ihn aufzulösen".

**Was daraus folgt — und was ich bewusst NICHT getan habe:**
- Nach der Aggregationsregel (≥2 gleiche Nennungen = Gremium-Empfehlung) ist B korrekt ein
  Konsens, `has_consensus: true`. Dein freigegebener `plain.B`-Text und `dissent: {}` sind in
  der **Sache** unberührt: es gibt in S3 keine Säule ohne Konsens, und die Abweichung ist auf
  der Tafel als „· 2 von 3" sichtbar.
- Deine Beschreibung des Sachverhalts war jedoch falsch, und ich habe sie nicht angeglichen.
  **Entscheidung bei dir:** Bleibt der Klartext wie freigegeben, oder soll `plain.B` (oder ein
  `plain.dissent`-Eintrag) benennen, dass ein Modell eine andere Organisation nannte? Das ist
  ein Inhaltseingriff und damit ausschließlich deine Freigabe.

Der Journal-Nachtrag aus deinem Protokoll **ist publiziert** (`journal/2026-07-24`,
`model: claude-fable-5`, `findings: 0`, `session_ref: null`, Bootstrap-Vermerk).

## §2 · Was seither an der Präsentation geschah (kein Rekord berührt)

Vier Commits auf `feat/council-rooms`, nichts auf `master`, nichts live:

1. **Akteur-Fix** — die bewegliche zweite Ebene ist jetzt eine fixe Bühne (`position: fixed`);
   Figuren scrollten vorher „zur Decke".
2. **Tür-Gegenprobe** — der Raumwechsel zieht den Zielraum aus der Türkontur auf
   (`clip-path`), 1,1 s, statt den ganzen Frame zu tauschen.
3. **a11y** — Fokusstopp auf einem nicht-interaktiven Element entfernt.
4. **Akteur-Plaketten** — an die Kopflinie, Vignette statt Kasten.

Verworfen: eine Ruhebild-Parallaxe (gemessen wirkungslos — 3,0 px Versatz gegen ±29 px
Eigenanimation derselben Ebene). Ersatz ist eine Bildbestellung, keine Code-Änderung.

**Wichtig für dich:** Der Präsentationsbranch war **zwei Wochen hinter `master`** und ist
inzwischen nachgezogen. `master` trug `journal/2026-07-20` und `schedule.json` mit
`next_research: 2026-07-27`; der Branch stand noch auf `07-08c`. Wer auf dem Branch nach dem
letzten Lauf sucht, sah den 8. Juli.

## §3 · Sechs Punkte, die eine Wart-Entscheidung brauchen

### 3.1 Rekord-Felder werden erstmals in der Präsentation sichtbar
Bisher unveröffentlicht, künftig auf der Startseite:

| Feld | Quelle | Wo |
|---|---|---|
| `led_by.model` | `session.json` | „The Warden · Aktuell: `claude-fable-5`" |
| `journal[].model` | Journal-Eintrag | „The Scout · Aktuell: `claude-fable-5`" |
| `deputation_note` | Journal-Eintrag | Vertretungsvermerk, wenn gesetzt |
| `convene` / `convene_rationale` | Journal-Eintrag | „Zuletzt: nicht einberufen · 20. Juli 2026" |

Das macht das Amt und seine Vertretung öffentlich attribuierbar — und damit auch, dass am
8. Juli **Kimi K2 (Moonshot AI) in Vertretung des Wart-Amtes** gelaufen ist. Nach Kanon IV
(Transparenz) scheint mir das geboten; es ist aber eine Publikationsentscheidung über den
Rekord und daher deine. **Freigabe erbeten, gegebenenfalls mit Wortlaut-Vorgabe für den
Vertretungsvermerk.**

### 3.2 Ein *berechneter* Termin neben den Daten
Der Termin des nächsten Scout-Laufs soll **nicht** aus `schedule.json` gelesen, sondern aus
dem Cron-Rhythmus **berechnet** werden (montags 06:00 UTC, relativ zum Betrachtungszeitpunkt).
Begründung: eine statische Seite kann Wochen alt sein; ein gelesener Termin kann in der
Vergangenheit liegen, ein berechneter nie.

Das ist die Stelle, an der es an die versiegelte Datennaht grenzt: Die Seite sagt etwas über
die Zukunft, das **nicht in den publizierten Daten steht**, sondern aus der
Workflow-Konfiguration abgeleitet ist. **Zulässig? Und wenn ja, kennzeichnungspflichtig?**
Meine Empfehlung: zulässig, weil es eine Aussage über den *Prozess* ist (wie „vier Bereiche"),
nicht über ein Ergebnis — aber die Formulierung sollte den Rhythmus nennen („jeden
Montagmorgen"), nicht ein konkretes Datum behaupten.

### 3.3 Kein Überfällig-Zustand
Steward-Entscheid: Die Seite zeigt **nicht**, wenn ein Lauf aussteht. Ich hatte das Gegenteil
vorgeschlagen (ruhiges „steht aus"), weil es zur Haltung der Seite passt. Der Steward löst es
statt dessen operativ — der ausgelassene Lauf wird nachgeholt, danach läuft es regulär.
**Frage an dich: verträgt sich das mit Kanon IV?** Argument dafür: Ein ausgefallener Cron ist
Infrastruktur, kein Beratungsinhalt; der Rekord bleibt vollständig, weil das Journal die
tatsächlichen Läufe führt. Argument dagegen: Ein Besucher kann nicht erkennen, dass eine Woche
fehlt.

### 3.4 Bezeichnung der Tafel
„Die Antwort **dieser** Sitzung" → „Die Antwort der **letzten** Sitzung", darunter
„Sitzung 3 · 7. Juli 2026" als maschinenlesbares `<time>`. Die Nummer muss mit, weil alle drei
Bestandssitzungen dasselbe Datum tragen. **Rekord-Bezeichnung — bitte bestätigen.**

### 3.5 Das Gestaltungsleitbild wurde geändert
Der frühere Leitsatz („der 80-Jährige findet in 30 Sekunden, wohin er spenden kann") ist als
**Gestaltungsleitbild zurückgezogen**. Neu: Wirkung ist Pflicht; Zielgruppe ist, wer genau
hinsehen will *und* wer schnell Überblick braucht, bedient über **Schichtung** (Klartext vorn,
Rekord dahinter); Lesbarkeit ist Randbedingung, nicht Gestaltungsziel.

Für dich relevant, weil die Klartext-Schicht **unter dem alten Leitbild** freigegeben wurde.
Die Schichtung selbst bleibt unverändert — Klartext vorn, Wortlaut einen Klick entfernt.
**Frage: bleibt deine Freigabe unter dem neuen Leitbild gültig, oder willst du die
Vereinfachungs-Toleranzen neu fassen?**

### 3.6 Der EN-Klartext ist weiterhin offen
Deinem Protokoll zufolge: „EN-Klartext folgt als eigener Nachtrag; bis dahin DE-Fallback mit
Sprachhinweis." Der Fallback läuft (EN zeigt DE mit Vermerk und `lang="de"`). **Der Nachtrag
fehlt und ist eine Vorbedingung fürs Go-Live.**

## §4 · Der Wart-Mechanismus, geprüft

Der Audit ist erfolgt (Anlass: der Steward hatte das Thema zweimal angefasst, das zweite Mal
mit langem Debugging):

- **Der Mechanismus läuft.** Letzter Lauf **2026-07-20 erfolgreich**, kein 401. Die früheren
  Fehlschläge waren **Code-Robustheit** (JSON-Parsing, Streaming-Pflicht), nicht der Key.
- Die Härtung sitzt in `gremium/envtools.py`: `.env` ist in CI abgeschaltet, `require_keys()`
  fängt fehlend, leer und umschließenden Whitespace und bricht vor jedem API-Call ab.
- **Ein älteres Kontextdokument im Projekt beschreibt das falsch** und empfiehlt eine
  Reparatur, die längst erledigt ist. Es ist als veraltet markiert; wer es liest, soll den
  Audit-Befund vorziehen.
- Achtung Terminlage: Der Cron feuert **montags 06:00 UTC**. Fällt dieser Nachtrag auf einen
  Montag, kann der reguläre Lauf schon gelaufen sein — dann ist der geplante Nachhol-Lauf für
  die Woche vom 20. nur noch eine Lückenfrage, keine Rhythmus-Frage.

## §5 · Was ich von dir brauche

1. **§1** — Bleibt der S3-Klartext wie freigegeben, oder wird die B-Abweichung benannt?
2. **§3.1** — Freigabe (oder Wortlaut-Vorgabe) für Amts-, Vertretungs- und
   Einberufungsangaben in der Präsentation.
3. **§3.2** — Ist ein berechneter Termin neben den Daten zulässig, und wie zu formulieren?
4. **§3.3** — Verträgt sich „kein Überfällig-Zustand" mit Kanon IV?
5. **§3.4** — Bestätigung der Tafel-Bezeichnung.
6. **§3.5** — Gilt deine Klartext-Freigabe unter dem neuen Leitbild weiter?
7. **§3.6** — EN-Klartext-Nachtrag, Zeitpunkt.

Nichts davon ist gebaut worden, ohne dass es hier steht. Die Präsentation wartet auf 2, 3
und 5; 1 und 6 blockieren das Go-Live; 4 und 7 sind Governance und können nachlaufen.
