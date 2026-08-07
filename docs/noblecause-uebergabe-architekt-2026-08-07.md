# Übergabe Architekt — Fortschreibung, Stand 7. August 2026

**Von:** Opus 5 (Architekt) · **Ergänzt** `claude/noblecause-uebergabe-architekt-2026-08-03.md`
— die dortigen §2 (Rollen), §6 (Arbeitsregeln), §7 (Fehler) und §8 (Wo alles liegt) gelten
unverändert und werden hier nicht wiederholt.

---

## 1 · Der Stand in einem Absatz

**Sitzung 4 hat am 6. August stattgefunden und ist im Rekord.** Sie ist inhaltlich korrekt,
aber **nicht ausgeliefert**: Die Live-Seite steht seit dem 2. August auf `ad75650` und zeigt
Sitzung 3. Der Build bricht an fehlenden Medaillon-Assets für die neue Ratsbesetzung ab. Das
ist der einzige harte offene Punkt — und er liegt beim Steward, nicht bei CC.

---

## 2 · Sitzung 4 — was geschah

**Der Lauf** (6. August, `02c0dc4`, 2,70 € von 15): formal sauber, Schema-Tor grün, alle vier
Bereiche, drei Modelle in beiden Runden.

**Fable hat das Dossier erneut verweigert** — zweite Verweigerung in Folge bei
Biosicherheits-Materie. **Der Guard hat gehalten**, genau wie gebaut: Marker
`wart_dossier_refusal`, kein Teiltext, kein Absturz, die Sitzung lief durch. Das war der erste
scharfe Test der Härtung, und er ist bestanden.

**Der Namens-Spalt.** Alle drei Modelle bestätigten NTI (C) und LEEP (D) — aber schrieben im
strukturierten Feld „Nuclear Threat Initiative" statt des Kanonnamens mit Klammer-Akronym.
Der Resolver matchte nicht, sechs Stimmen landeten in `unresolved_votes`, und die Schutzklausel
in `homepage.js:140` verweigerte den Build. **Kein Dissens — ein Auflösungsfehler**, dieselbe
Klasse wie B1 und P3: Auflösung, die an einer Formalie bricht.

Behoben nach Wart-Kriterium (`1dd0dd6`): zwei Alias-Einträge als **Daten** in der Registratur,
kein Fuzzy-Matching. Reaggregiert aus unveränderten Rohvoten: C = NTI 3/3, D = LEEP 3/3,
`unresolved_votes` leer, Korrekturhinweis DE+EN. Diff nur `recommendations`,
`unresolved_votes`, `correction_notice` — alles andere byte-identisch.

**Der zweite Blocker, vom ersten verdeckt:** Die Seite bildet den Medaillon-Pfad direkt aus der
Modell-ID (`/media/medallions/{track.model}-lo.avif`). Sitzung 4 ist die erste mit der neuen
Besetzung; für `claude-opus-5`, `gpt-5.6-sol`, `gemini-3.5-flash` existieren keine Medaillons.
Sechs Dateien fehlen, der Build bricht ab.

---

## 3 · Drei Wart-Entscheide, alle im Rekord

**`wart-entscheid-sichtbarkeit-prozessmaterial-2026-08-04.md`**
`raw/` ist unantastbar — die Rohantworten *sind* das Produkt, nicht ein Beleg dafür.
Dreiteilung: (a) Rekord-Grundlagen, (b) Prüfmaterial, (c) Arbeitsmaterial — **nur (c) darf ins
private meta-Repo.** Kein History-Rewrite (zwei unabhängige K.O.-Gründe; der publizierte
`correction_notice` trägt ein `commit`-Feld — nach einem Rewrite zeigt der Belegapparat ins
Leere). Verschiebungen laufen als reguläre Commits **vorwärts**; das Verschobene bleibt in der
Historie sichtbar. Personennamen künftig als Rollen, Bestand per regulärem Commit, Historie
bleibt.

**`wart-entscheid-deliberationsform-2026-08-06.md`**
Erwiderungsrunde mit namentlichem Adressat ist **zulässig** — „unabhängig sein muss das Urteil,
nicht das Gespräch". Ebenso Fragen, die eine Wahl erzwingen. **Auflage:** Die
Verfahrensbeschreibung der Seite muss vorher präzisiert werden (heute: „jedes Modell antwortet
unabhängig" — nach der Änderung eine Halbwahrheit). Publikation als Schichtung: Tafel bleibt
Ergebnis, die Beratung gehört in die Tiefe.

**Re-Aggregations-Kriterium** (in der Kommunikation zum Namens-Spalt)
Re-Aggregation ist zulässig, wenn drei Bedingungen zusammen gelten: Rohvoten gültig und
eindeutig · Fix deterministisch und aus `raw/` nachrechenbar · Korrekturhinweis, altes Ergebnis
bleibt in der Historie. **Sobald die Auflösung Interpretation braucht, bleibt `unresolved_votes`
stehen — der Rekord rät nicht.**

---

## 4 · Neue Kanon-Regeln

1. **Ohne Dossier keine Evidenzprüfungs-Frage.** Sitzung 4 war ein *Meinungsbild*, keine
   Evidenzprüfung — eine Bestätigungsfrage ohne neue Belege produziert Bestätigung. Fällt das
   Dossier aus, muss die Frage das berücksichtigen. Betrifft die nächste Sitzung (5. September).
2. **Ein Entscheid, der eine Bauweise bestimmt, wird mit dem Bau committet — nicht danach.**
   Fünfmal in einer Woche lagen Grundlagen in keinem Commit.
3. **Ein Personenname ist kein Sortierkriterium** für privat/öffentlich. Namen werden separat
   und vorwärts auf Rollen umgestellt; sortiert wird ausschließlich nach Prüfbarkeit.
4. **Aliase sind Daten, kein Code.** Ein Matcher, der rät, ist die nächste Fehlerquelle.

---

## 5 · Offen — nach Dringlichkeit

| | Was | Wer |
|---|---|---|
| **1** | **Drei Medaillon-Sätze** (je `.avif` + `-lo.avif`) für `claude-opus-5`, `gpt-5.6-sol`, `gemini-3.5-flash`. **Einziger Build-Blocker.** Ohne sie friert die Seite weiter ein, während der Rekord wächst | **Steward** |
| 2 | `1dd0dd6` FF-Push (freigegeben, Deploy bleibt rot bis 1) | CC/Steward |
| 3 | Teil 2 `journal.schema kind` → dann A2 (Verweigerungseintrag Lauf #6). Macht nebenbei die Wacht sehend und beendet „Letzte Prüfung: 27. Juli" | CC |
| 4 | Sortier-Listen (a)/(b)/(c)/(d) für die Reorg-Session | CC |
| 5 | Deliberationsform bauen — **erst nach der Verfahrensbeschreibungs-Anpassung**, und nicht in der Woche eines scharfen Laufs | — |
| 6 | Einstieg (Konzept vom 2.8.) → dann Scout-Redundanz → dann größerer Rat | — |

**Neu in der 0.4.1-Liste:**

- **P12** — Runde-2-Loop ordnet über `zip(config["models"], r1)` statt über einen Schlüssel.
  Hier ungefährlich (Identität reist mit dem Spec), aber die dritte Stelle mit
  Reihenfolge-Abhängigkeit nach B1 und P3.
- **P13** — Medaillon-Pfad direkt aus der Modell-ID. **Jede Besetzungsänderung bricht den
  Build.** Bei der Rats-Erweiterung auf fünf Modelle läuft es sofort wieder auf. Fix: neutrales
  Standard-Medaillon als Fallback statt 404 → Abbruch. Dieselbe Regel wie bei den
  Refusal-Guards: *die Abwesenheit eines Zulieferers darf nicht den ganzen Vorgang töten.*

---

## 6 · Die Erkenntnis, die über allem steht

Der Steward hat nach Sitzung 4 benannt, was das Verfahren wirklich ist: **eine Delphi-Umfrage,
kein Weisen-Gremium.** Drei Modelle antworten unabhängig, sehen einander erst in Runde 2, ein
Zähler bildet das Ergebnis. Kein Modell spricht zu einem anderen.

Drei Ursachen, und nur eine ist strukturell:

1. **Die Frage lud zum Bestätigen ein** — sie stammt vom Architekten. *Eng genug für Konsens*
   und *Konsens durch Konstruktion* sind zwei verschiedene Dinge. Mein Kriterium lautete „sie
   muss ein Nein zulassen"; zulassen ist nicht herausfordern.
2. **Das Dossier fehlte.** Ohne neue Belege gab es nichts zu bestreiten. Das ist der übersehene
   Preis der Verweigerung: nicht ein fehlender Beipack, sondern **der fehlende
   Streitgegenstand.**
3. **Das Format kennt keine Erwiderung.** Nur das ist die eigentliche Baustelle.

**Das ist die 0.5, nicht die Sitzerweiterung.** Fünf Modelle, die nebeneinander abstimmen, sind
nur eine größere Umfrage. Der Wart hat die Form freigegeben; gebaut wird nach Steward-Freigabe.

---

## 7 · Zwei Fallen, die diese Woche mehrfach zugeschlagen haben

**Der Hauptbaum `~/Projects/NobleCause.ai` ist als Informationsquelle unbrauchbar.** Er steht
auf `a25d1ee`, 109 Commits zurück, mit untrackter `docs/`-Kollision. Jede „existiert
nicht"-Aussage von dort ist wertlos — die Datei liegt im Repo, nur nicht im Checkout. Alles
Aktuelle: `nc-sanitize`. Das hat den Steward zweimal und mich einmal auf eine Fehlspur geführt.

**„Liegt vor" ist kein Beleg — sechs Wiederholungen in einer Woche.** Gate-Zeilen 5a/5c, der
Verweigerungs-Entscheid, der Familien-Entscheid, vier Prüferberichte, fünf Wart-Entscheide vom
1. August. Jedes Mal gerettet, bevor es weg war. Die Regel steht in §6 der 03.08-Übergabe; sie
wird offenbar leichter aufgeschrieben als befolgt.
