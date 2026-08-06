# Diagnose: Der Namens-Spalt in Sitzung 4 (Bereich C/D) — Vorlage für den Wart zur Re-Aggregation

**Datum:** 2026-08-06
**Anlass:** Sitzung 4 (`sessions/2026-08/`) trägt sechs unaufgelöste Stimmen (Bereich C und D). Der Seiten-Build ist deshalb rot (Schutzklausel `homepage.js:140`), die Live-Seite unversehrt auf dem Stand `ad75650`. Diese Vorlage liefert dem Wart das Material für seine **Pro-Votum-Entscheidung** nach seinem Kriterium: *Re-Aggregation zulässig bei mechanischer Zuordnung ohne Deutungsakt.*

**Nichts angelegt, nichts reaggregiert, nichts am Frontend, nichts an `sessions/**` — nur diese Vorlage. Der Wart sieht die Diff vor dem Lauf.**

---

## 1 · Die sechs unaufgelösten Rohvoten im Wortlaut

Quelle: `sessions/2026-08/raw/r2-*.json` (finale Voten — die Aggregation speist aus `aggregate_recommendations(r2)`, nicht aus `session.json`). Angegeben ist das Feld `organization` **exakt wie vom Modell geschrieben** — das ist, was der Resolver liest —, die Normalform `_norm` (siehe §2), und der umgebende Satz aus der Prosa. Alle sechs stehen unter `conditional = true` (mit Vorbehalt **gehalten**; sachlich eine Bestätigung derselben Organisationen wie Sitzung 3). Die vollständigen `reservation`-Wortlaute liegen in `raw/` und sind auf Wunsch beizulegen.

### Bereich C — Große Gefahren

| Modell | `organization` (exakt) | `_norm` | Umgebender Satz (Rohtext) |
|---|---|---|---|
| Claude Opus (`claude-opus-5`) | `Nuclear Threat Initiative` | `nuclearthreatinitiative` | „### Säule C — Nuclear Threat Initiative · gehalten, aber revidiert zu `conditional = true`" |
| GPT (`gpt-5.6-sol`) | `Nuclear Threat Initiative` | `nuclearthreatinitiative` | „**Schlussvotum: Nuclear Threat Initiative – nukleare und biologische Risikoreduktion.** Ich **halte** die Empfehlung, jedoch ausdrücklich bedingt." |
| Gemini (`gemini-3.5-flash`) | `Nuclear Threat Initiative` | `nuclearthreatinitiative` | „**Entscheidung:** Ich halte an der **Nuclear Threat Initiative (NTI)** fest, setze das Votum jedoch auf **conditional = true**." |

### Bereich D — Übersehenes

| Modell | `organization` (exakt) | `_norm` | Umgebender Satz (Rohtext) |
|---|---|---|---|
| Claude Opus (`claude-opus-5`) | `Lead Exposure Elimination Project` | `leadexposureeliminationproject` | „### Säule D — Lead Exposure Elimination Project · gehalten, Vorbehalt präzisiert" |
| GPT (`gpt-5.6-sol`) | `Lead Exposure Elimination Project` | `leadexposureeliminationproject` | „**Schlussvotum: Lead Exposure Elimination Project – Eliminierung von Bleifarbe.** Ich **halte** die Empfehlung unter verstärktem Vorbehalt." |
| Gemini (`gemini-3.5-flash`) | `Lead Exposure Elimination Project` | `leadexposureeliminationproject` | Aus der Reservation: „Ein Steward muss prüfen, ob die 2024 gestartete ‚Partnership for a Lead-Free Future' (PLFF) LEEPs operative Lücken bereits vollständig geschlossen hat. Sollte LEEP keine ungedeckte Finanzierungslücke [nachweisen] …" |

**Beobachtung, die die Diagnose trägt:** In **allen sechs** JSON-`organization`-Feldern fehlt das Klammer-Akronym, das der kanonische Registry-Name führt. Bei Gemini/C nennt die **Prosa** ausdrücklich „Nuclear Threat Initiative (NTI)", das strukturierte Feld aber „Nuclear Threat Initiative" — der Resolver liest nur das Feld. Es ist durchgängig dieselbe Auslassung, nicht drei verschiedene Fehler.

---

## 2 · Vorgeschlagene Alias-Einträge (Diff-Vorlage — NICHT angelegt)

Der Alias-Mechanismus **existiert bereits**: `organizations.json` führt je Organisation ein `aliases`-Feld; `organizations.resolve(s)` schlägt `_norm(s)` in einer aus `canonical_name` + `aliases` gebauten Map nach. `_norm` entfernt alles außer `[a-z0-9]` und senkt Groß-/Kleinschreibung:

```
_norm("Nuclear Threat Initiative (NTI)")  ->  "nuclearthreatinitiativenti"
_norm("Nuclear Threat Initiative")        ->  "nuclearthreatinitiative"     # unbelegt -> unresolved
```

Es fehlen **genau zwei** Einträge:

| Alias (neu) | → kanonische Org (`id`) | `_norm` des Alias | Warum zweifelsfrei dieselbe Organisation |
|---|---|---|---|
| `Nuclear Threat Initiative` | `nuclear-threat-initiative` | `nuclearthreatinitiative` | Wort-für-Wort der kanonische Name „Nuclear Threat Initiative (NTI)" **minus** das Klammer-Akronym „(NTI)", das per Definition genau für diese Organisation steht. Die bestehenden `aliases` führen bereits sechs Suffix-Varianten **derselben** Org (u. a. „…(NTI)", „…(NTI) – Biosecurity"). |
| `Lead Exposure Elimination Project` | `lead-exposure-elimination-project` | `leadexposureeliminationproject` | Ebenso: kanonischer Name „Lead Exposure Elimination Project (LEEP)" minus „(LEEP)". |

**Konkrete Diff (zur Ansicht, nicht ausgeführt):**

```diff
  // organizations.json → org "nuclear-threat-initiative" → "aliases":
      "Nuclear Threat Initiative (NTI)",
+     "Nuclear Threat Initiative",
      … (bestehende Suffix-Varianten unverändert)

  // organizations.json → org "lead-exposure-elimination-project" → "aliases":
      "Lead Exposure Elimination Project (LEEP)",
+     "Lead Exposure Elimination Project"
```

**Kollisionsschutz greift automatisch:** `load_registry()` bricht laut ab, wenn eine normalisierte Zeichenkette bereits einer **anderen** `id` zugeordnet ist. Beide Normalformen (`nuclearthreatinitiative`, `leadexposureeliminationproject`) sind derzeit unbelegt — genau deshalb sind die Voten unresolved; kein Konflikt.

**Der Grundsatz des Warts — „Ein Alias, über den man diskutieren kann, ist keiner"** — ist bei diesen zwei erfüllt: identischer Wortlaut minus das **definitorische** Akronym, das die Klammer selbst als Kürzel eben dieser Org ausweist. **Bewusst NICHT vorgeschlagen** (das wäre ein Deutungsakt): „NTI | bio" als eigenständige Org, „Pure Earth" als Alternative in Säule D (von Opus/Gemini als *andere* Adresse erwogen), oder irgendeine Zuordnung, die über das reine Weglassen des Akronyms hinausgeht. Im Zweifel bleibt das Votum ungelöst.

---

## 3 · Eine Korrektur, die in die Diagnose gehört

In der ersten Meldung wurde die „Publikations-Klausel" so benannt, als wäre sie eine Klausel **in einem Votum**. Das ist unzutreffend und würde auf eine Einordnung warten lassen, die es nicht gibt.

Sie ist **Code**, kein Modelltext:

> `site/src/lib/server/homepage.js:140` — `if ((session.unresolved_votes ?? []).length) throw` — die Schutzklausel, die den Seiten-Build verweigert, sobald die jüngste Sitzung unaufgelöste Stimmen trägt.

**Kein Modell hat etwas zur Publikation gesagt.** Die sechs Voten betreffen ausschließlich die Organisationswahl (C: NTI, D: LEEP, jeweils bedingt gehalten). Es bleibt **ein** zu entscheidender Fall: der Namens-Spalt. Werden die zwei Aliase gesetzt und wird reaggregiert, verschwinden die unaufgelösten Stimmen, und die Schutzklausel greift von selbst nicht mehr — **ohne dass an der Klausel irgendetwas geändert würde**. Das Frontend bleibt unberührt.

---

## 4 · Der Resolver-Fix (Beschreibung — NICHT gebaut)

**Was ich ändern würde:** die **Alias-Tabelle in der Registratur** um die zwei Einträge aus §2 ergänzen. Nicht den Matcher im Code aufweichen.

Begründung:
- **Aliase sind Daten.** Sie werden committet, stehen im Rekord, sind pro Eintrag begründet und nachprüfbar — ein Prüfer sieht, welche Zuordnung wann mit welcher Begründung entstand. Das deckt sich mit dem Kriterium des Warts: mechanische Zuordnung, kein Deutungsakt.
- **Kein Fuzzy-Matching.** Ein Matcher, der aus Ähnlichkeit rät (Teilstring, Levenshtein, Embedding), ist die nächste Fehlerquelle: er verschmilzt irgendwann zwei verschiedene Organisationen oder trifft die falsche — ohne Spur und ohne Beleg. Der bestehende Ansatz (exakter Abgleich der Normalform gegen bekannte, committete Aliase) bleibt **unverändert** streng und belegbar; er wird nur um zwei Datensätze erweitert.
- Der Fix ist damit **rein additiv**: keine Codeänderung, keine Logikänderung, nur zwei Zeilen Daten, die je einen zweifelsfreien Namens-Spalt schließen.

---

## Grenzen (eingehalten)
Nichts an `sessions/**` (unveränderlich), kein reaggregate-Lauf, keine Alias-Einträge angelegt, nichts am Frontend. Der Build bleibt rot; die Live-Seite ist unversehrt (`ad75650`). Diese Vorlage wartet auf die Pro-Votum-Entscheidung des Warts.
