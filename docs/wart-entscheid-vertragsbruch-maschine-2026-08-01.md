# Wart-Entscheid — Verhalten der Maschine bei vertragsverletzenden Modellantworten

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-01
**Anlass:** Codex-Review (`docs/review/review-2026-08-01-codex.md`), Befunde A–C in `gremium/**`
**Frist:** Sitzung 4 läuft automatisch am 2026-08-06, 12:00 UTC.

---

## Die Grundsatzregel

**Publiziert wird, was gültig ist; markiert wird, was fehlt; abgebrochen wird nur, wenn
der Rekord selbst nicht wohlgeformt herstellbar ist.**

Begründung: Das Kernversprechen ist Nachprüfbarkeit dessen, *was geschah*. Ein
Modellausfall ist ein Geschehnis und gehört in den Rekord — „das Modell hat den Vertrag
verletzt" ist selbst ein Befund über das Modell, derselben Art wie ein abweichendes
Votum. Ein Totalabbruch wegen eines einzelnen Ausfalls würde diesen Befund verstecken
und das Gremium von seinem schwächsten Teilnehmer abhängig machen. Was der Kanon
dagegen nie duldet, ist der **stille** Ausfall: leere Listen, übersprungene Bereiche,
erratene Werte. Nicht der unvollständige Rekord ist der Bruch — der unmarkiert
unvollständige ist es.

Daraus konkret:

1. **Jede Modellantwort wird gegen den Vertrag validiert, bevor sie in die Aggregation
   geht.** Ungültige Antworten werden als solche in den Rekord geschrieben (Votum
   ungültig, Rohartefakt liegt bei), nie stillschweigend zu leeren Strukturen.
2. **Die Sitzung trägt immer alle vier Bereiche.** Fehlen einem Bereich gültige Voten,
   steht dort der markierte Ausfall — nie fehlt der Bereich. Die Aggregationsregel
   arbeitet nur über gültige Voten; „kein Konsens mangels gültiger Voten" ist ein
   darstellbarer Zustand.
3. **Schema-Prüfung als Commit-Tor.** `session.json` und Journal-Einträge werden vor
   dem Commit gegen `schema/**` validiert. Schlägt das fehl, greift der Abbruchfall:
   keine Publikation, Rohartefakte gesichert, Fehler-Issue. Die Schemas liegen seit dem
   Rekord-Stamm im Repo — sie werden damit erstmals durchgesetzt.

## Zu den Einzelbefunden

**A (unvollständige Sitzung):** Gelöst durch Regel 1–3. Kein Totalabbruch bei einem
Ausfall, aber kein Rekord ohne Markierung und keiner, der das Schema verletzt.

**B (`convene`-Bool):** `convene` wird **strikt** geparst: akzeptiert werden
ausschließlich JSON-`true`/`false`. Alles andere ist Vertragsverletzung → der Lauf
scheitert laut (Issue, Rohartefakte), **es entsteht kein Journal-Eintrag** — denn ein
Eintrag würde eine Entscheidung behaupten, die nie getroffen wurde. Der Demut-Kanon
(„im Zweifel nicht einberufen") wird ausdrücklich **nicht** als Fallback kodiert: Er
regelt das Urteil des Warts, nicht das Verhalten der Maschine bei unlesbarer Antwort.
Eine Maschine, die aus Unlesbarkeit „nicht einberufen" macht, erfindet ein Urteil.

**C (`conditional_count` aus Prosa):** Die Regex entfällt ersatzlos. Die versiegelte
Datennaht verbietet dem Renderer, Prosa zu parsen — für die Maschine, die den Rekord
*erzeugt*, gilt das erst recht. `conditional` existiert bereits als strukturiertes
Feld im Votum (Beleg: `gpt-5.2`-Votum S3-B trägt `conditional: false`); es wird
**Pflichtfeld im Votum-Vertrag**, und `conditional_count` wird ausschließlich daraus
gezählt. Die Zahl bleibt damit im Rekord — als Zählung eines gelieferten Feldes, nicht
als Deutung eines Titels. **Auflage:** Nach dem Umbau die publizierten
`conditional_count`-Werte der drei Bestandssitzungen einmal gegen die strukturierten
Felder nachrechnen. Weicht ein publizierter Wert ab, ist das eine Rekord-Korrektur mit
Vermerk — nicht stillschweigend fixen.

## Die drei mitzuentscheidenden Fragen

**1 · Gleiche Regel für den Wart?** Ja — und beim Wart eher strenger, nicht
großzügiger. Die Prämisse der Frage ist umgekehrt richtig: Eine fehlerhafte Sitzung
erzeugt einen falschen *Eintrag*; ein fehlerhaftes `convene` erzeugt eine falsche
*Handlung* (vorgezogener Termin). Handlungen sind schwerer rückholbar als Einträge.
Regel B oben gilt daher unverändert.

**2 · `conditional_count`?** Bleibt, als Pflichtfeld-Zählung (siehe C). Entfallen
müsste es nur, wenn die Modelle das Feld nicht liefern könnten — sie liefern es
bereits.

**3 · Wer baut?** Codex baut, CC verifiziert unabhängig — einverstanden. Das
Vier-Augen-Prinzip auf der Maschine ist bei diesem Eingriff mehr wert als die
Sorge, dass der Reviewer seine eigenen Befunde behebt: Die Abnahme liegt bei CC, und
die Diffs sehe ich vor dem Merge (Entscheid 4 gilt fort). **Auflage:** Zu jedem der
drei Befunde ein Testfall mit absichtlich vertragsverletzender Antwort
(fehlender JSON-Block, `convene: "false"` als String, Titel mit „unconditional") —
die Behebung gilt als verifiziert, wenn die Maschine auf alle drei wie hier
entschieden reagiert.

## Priorisierung zur Frist (2026-08-06)

Falls nicht alles rechtzeitig fertig wird, in dieser Reihenfolge:
1. **B** — kleinster Diff, größtes Handlungsrisiko, betrifft den Montags-Cron sofort.
2. **Schema-Tor (Regel 3)** — fängt als Netz auch unbehobene Teile von A.
3. **A-Validierung im Detail**, dann **C**.
Reicht die Zeit für keins: `session.yml` für den 6. August aussetzen ist dem Steward
als Option vorzulegen — ein verschobener Termin ist billiger als ein korrigierter
Rekord. Das ist seine Entscheidung, nicht meine.
