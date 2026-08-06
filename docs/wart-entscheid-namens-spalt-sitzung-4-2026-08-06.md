# Wart-Entscheid — Namens-Spalt Sitzung 4: Pro-Votum-Entscheidung und Re-Aggregation

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-06
**Grundlage:** `diagnose-namens-spalt-sitzung-4-2026-08-06.md` (sechs Rohvoten im Wortlaut,
Alias-Diff zur Ansicht, nichts angelegt, nichts reaggregiert).

---

## 1 · Pro-Votum-Entscheidung: alle sechs lösbar

Das Kriterium — mechanische Zuordnung ohne Deutungsakt — ist in allen sechs Fällen
erfüllt, und zwar im stärksten denkbaren Sinn: Die `organization`-Felder sind nicht
*ähnlich* zum kanonischen Namen, sie **sind** der kanonische Name, wortgleich bis auf
das definitorische Klammer-Akronym — das Kürzel, das die Registratur selbst als Kürzel
genau dieser Organisation ausweist. Es gibt nichts zu deuten; es gibt eine Auslassung
zu belegen.

| Votum | Entscheid |
|---|---|
| C · Claude Opus (`Nuclear Threat Initiative`) | lösbar → `nuclear-threat-initiative` |
| C · GPT (`Nuclear Threat Initiative`) | lösbar → `nuclear-threat-initiative` |
| C · Gemini (`Nuclear Threat Initiative`) | lösbar → `nuclear-threat-initiative` |
| D · Claude Opus (`Lead Exposure Elimination Project`) | lösbar → `lead-exposure-elimination-project` |
| D · GPT (`Lead Exposure Elimination Project`) | lösbar → `lead-exposure-elimination-project` |
| D · Gemini (`Lead Exposure Elimination Project`) | lösbar → `lead-exposure-elimination-project` |

Bei Gemini/C liefert der Rekord die Bestätigung gleich mit: Die Prosa desselben Votums
schreibt „Nuclear Threat Initiative (NTI)" aus — Feld und Prosa meinen dieselbe
Organisation, nur das Feld ließ das Akronym weg.

## 2 · Alias-Freigabe: beide, exakt wie im Diff

Freigegeben werden **genau die zwei** Einträge aus §2 der Diagnose, keine weiteren:

- `"Nuclear Threat Initiative"` → `nuclear-threat-initiative`
- `"Lead Exposure Elimination Project"` → `lead-exposure-elimination-project`

Der Ansatz ist der richtige und wird als Kanon bestätigt: **Aliase sind Daten** —
committet, pro Eintrag begründet, nachprüfbar. **Der Matcher bleibt streng**; kein
Fuzzy-Matching, nie: Ein Matcher, der aus Ähnlichkeit rät, erzeugt Zuordnungen ohne
Beleg, und eine unbelegbare Zuordnung ist im Rekord schlimmer als eine ungelöste.
Ebenso bestätigt: Was die Diagnose bewusst *nicht* vorschlägt („NTI | bio" als eigene
Org, Pure Earth als Alternative), wäre Deutung gewesen — richtig weggelassen.

## 3 · Re-Aggregation: freigegeben

`reaggregate.py` läuft nach Anlage der zwei Aliase über Sitzung 4. Erwartung nach
Rohlage: C = NTI 3/3, D = LEEP 3/3, alle sechs `conditional = true` — der Vorbehalt
fließt über das strukturierte Pflichtfeld in `conditional_count`, wie seit dem
1. August vorgesehen; nichts wird aus Prosa erschlossen. `unresolved_votes` leert
sich, die Schutzklausel (`homepage.js:140`) greift von selbst nicht mehr — an ihr
wird, wie in der Diagnose zugesagt, nichts geändert. Sie hat getan, wofür sie da ist:
Sie hat einen unfertigen Rekord von der Bühne ferngehalten, ohne ihn anzutasten.

§3 der Diagnose ist zur Kenntnis genommen: Die „Publikations-Klausel" war Code, kein
Votumtext — es gab von Anfang an nur einen Fall, den Namens-Spalt. Damit entfällt die
im Kriteriums-Entscheid angekündigte Pro-Votum-Weiche für Klauseln ersatzlos.

## 4 · Korrekturhinweis für Sitzung 4 — Wortlaut

> **DE — Korrekturhinweis (2026-08-06):** Bei der Erstaggregation dieser Sitzung
> blieben sechs Voten (Bereiche C und D) unaufgelöst: Die Modelle schrieben die
> kanonischen Organisationsnamen ohne das Klammer-Akronym („Nuclear Threat
> Initiative" statt „Nuclear Threat Initiative (NTI)"), und die Alias-Tabelle der
> Registratur kannte diese Schreibweise nicht. Die Voten selbst waren gültig und
> eindeutig. Behoben durch zwei Alias-Einträge in der Registratur (Daten, keine
> Code-Änderung) und Neu-Aggregation aus den unveränderten Rohvoten; das Ergebnis —
> C: Nuclear Threat Initiative, D: Lead Exposure Elimination Project, jeweils 3 von 3
> mit Vorbehalt — ist aus `raw/` nachrechenbar. Die Rohvoten stehen unverändert im
> Rekord.

> **EN — Correction notice (2026-08-06):** In this session's initial aggregation,
> six votes (areas C and D) remained unresolved: the models wrote the canonical
> organization names without the parenthetical acronym ("Nuclear Threat Initiative"
> instead of "Nuclear Threat Initiative (NTI)"), and the registry's alias table did
> not know this spelling. The votes themselves were valid and unambiguous. Fixed by
> two alias entries in the registry (data, no code change) and re-aggregation from
> the unchanged raw votes; the result — C: Nuclear Threat Initiative, D: Lead
> Exposure Elimination Project, each 3 of 3 with reservation — can be recomputed
> from `raw/`. The raw votes remain unchanged in the record.

## 5 · Ausführung (auf dieses Wort)

1. Zwei Alias-Einträge anlegen (Diff aus §2 der Diagnose, unverändert).
2. `reaggregate.py` über `sessions/2026-08/` — Ergebnis muss der Erwartung aus
   Ziffer 3 entsprechen; weicht es ab, stopp und zurück an mich.
3. Korrekturhinweis (Ziffer 4) an den Sitzungseintrag.
4. Build wird grün von selbst; am Frontend nichts anfassen.

Ein Satz zur Wurzel, ohne Bauauftrag: Der Spalt entstand, weil Modelle Namen
natürlich schreiben und die Registratur formal führt. Die Alias-Tabelle ist dafür
das richtige, wachsende Gefäß — jeder künftige Spalt derselben Art ist ein
Zwei-Zeilen-Datum mit Begründung, kein Vorgang. Am Prompt ist nichts zu ändern.
