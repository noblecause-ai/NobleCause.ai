# Abnahme Maschinen-Härtung — kimi, 2026-08-02

Stand: `599998d` (detached, 11 Commits über `origin/master`), Worktree `nc-abnahme-kimi`.
Maßstab: Wart-Entscheid Vertragsbruch-Maschine + `WART-NACHTRAEGE.md` (1 Sortierung /
2 Zählweise / 3 conditional) + Opus-5-Auftrag + Wart-Freigabe Korrekturhinweis.
Methode: Code gelesen, Testsuite selbst gelaufen (43/43), Schema-Tor selbst gelaufen
(Bestand: 3 Sitzungen + 8 Journal-Einträge, alle gültig), fünf Sitzungs-Szenarien
synthetisch durch Writer **und** Schema gejagt, Rohvoten und Korrekturhinweise
maschinell verglichen. Kein Lauf ausgeführt, der Geld kostet oder Rekord schreibt.

---

**1 · Sortierung und Gate — trägt.**
`run_wart.py:109` sortiert nach `(number, date)`, identisch zu `run_session.py:117`.
`assert_current_session()` (`run_wart.py:113-139`) leitet das Maximum unabhängig neu her
und bricht laut ab, **bevor** Verzeichnis oder API-Call entstehen (`run_wart.py:305-308`
vor 313) — fängt damit auch künftige Ursachen derselben Wirkung, nicht nur den
Sortierfehler (Nachtrag 1). Tests decken Gleichdatum, Nummer-schägt-Datum, Gate-Ja,
Gate-Nein, unbekannte Ref.

**2 · `convene` — trägt.**
`parse_wart_answer` (`run_wart.py:59-89`) akzeptiert ausschließlich `isinstance(…, bool)`
— String `"false"`, Zahl `1`, fehlend: je lauter Abbruch. Kein Prosa-Fallback
(`fallback_from_markdown` ist entfernt, Test bewacht das). Abbruch vor dem Schreiben
des Eintrags (`run_wart.py:350` vor 379): es entsteht kein Journal-Eintrag, Rohartefakte
liegen bereits. `stop_reason != "end_turn"` bricht vor dem Parsen ab. Workflow-Machinerie
(Artifact + Issue) vorhanden.

**3 · Schema-Tore — trägt nicht, an genau einer Stelle.**
Tor läuft in beiden Workflows **vor** dem Commit (`session.yml:91-94`, `wart.yml:40-43`),
Bestand validiert unverändert (selbst ausgeführt: 3 Sitzungen, 8 Einträge inkl. Bootstrap
`2026-07-07` und Kommission `2026-07-27b` — 0 Fehler). **Aber:** `schema/session.schema.json:54`
tippt `rounds[].votes[].recommendations[].conditional` als `boolean`, nicht nullable.
Der Writer (`run_session.py:309,316`) schreibt dort bewusst `null` als Ungültig-Marker,
wenn ein Modell das Pflichtfeld nicht liefert. Meine Probe durch den echten Writer gegen
das echte Schema: **fehlendes `conditional` bei auch nur einem Modell → Tor fällt → keine
Publikation der ganzen Sitzung.** Entschieden (Nachtrag 3) ist aber „Votum ungültig,
markiert, kein Titel-Raten" — also publizieren mit Markierung, nicht Abbruch. Schema und
Writer widersprechen sich; der Rekord wäre wohlgeformt herstellbar, das Tor lehnt ihn
trotzdem ab. Eine Zeile (`"type": ["boolean", "null"]` an :54) schließt es.

**4 · Vier Bereiche, Zähler, Gleichstand — trägt.**
Die Aggregation läuft immer über alle vier Säulen; der dritte Zustand (kein gültiges
Votum) ist ein markierter Bereich, nie ein fehlender (`run_session.py:407-423`).
Zählweise nach Nachtrag 2 verifiziert: `convergence.total` bleibt 3, Ausfall steht als
`votes_invalid` + Vermerk „N Modell(e) ohne auswertbares Votum" daneben, nie eingerechnet
(Probe: 2 von 3 + 1 unlesbar → `votes_valid 2 / votes_invalid 1`, Konsens steht).
Randfälle des Nachtrags: 1 gültiges Votum → kein Konsens, Einzelvotum mit Modell-
Attribution (`individual_votes`); 0 gültige → markierter Ausfall. Gleichstand →
`has_consensus: false`, `tie: true`, kein stiller Sieger mehr (`run_session.py:433`).
Doppelvotum → Warnung im Rekord. Tests decken alle vier Fälle mit den entschiedenen
Erwartungen.

**5 · `conditional` — trägt, mit der Einschränkung aus 3.**
Regex ersatzlos weg — gegreppt über `gremium/**`, inkl. Nebenpfade (`reaggregate.py`,
`run_commission.py`; beide Signatur-konsistent, kein Titel-Parsing mehr). Der Prompt
(`prompts.py:73-97`, ROUND2:124-126) fordert das Feld im JSON-Template, mit Erklärung,
Beispiel beider Fälle und ausdrücklicher Konsequenz („kann nicht gezählt werden") —
eindeutiger geht es ohne JSON-Schema-Enforcement kaum. Zählung läuft ausschließlich über
das strukturierte Feld (`read_conditional`, `run_session.py:325-336`), Verletzung →
ungültig + Warnung, kein Raten. Meine Rohdaten-Probe bestätigt Nachtrag 3 unabhängig:
**kein** rohes Votum aller drei Sitzungen enthält den String `conditional` — die
publizierten Bool-Werte im Bestand sind Regex-Erbe. Der Bestands-Zählstand
(`2026-07c` A = 1) bleibt davon unberührt (Nachtrag 3: Methodenwechsel, keine
Nachrechnung). Genau deshalb ist der Fall „Modell liefert das Feld nicht" am 6.8. real —
und er landet heute im Tor aus Punkt 3 statt in der entschiedenen Markierung.

**6 · Die Tests — trägt.**
Alle sieben Testdateien gelesen; sie rufen die echten Funktionen auf und prüfen die
entschiedenen Erwartungen (u. a. Bestand validiert; `"false"`-String bricht; Titel mit
„unbedingt/vorbehaltlos/nicht konditional/unconditional" erzeugt keinen Vorbehalt;
fehlendes Feld → ungültig, nicht geraten; Gleichstand ≠ Konsens). Kein Test grün, weil
er das Falsche misst. **Eine Lücke:** kein Test kreuzt Writer × Schema im Markierungsfall
(Aggregation und Tor werden nur getrennt getestet) — genau dort sitzt der Befund aus 3.
43/43 grün, selbst gelaufen.

**7 · Korrekturhinweise — trägt.**
`correction_notice` in `journal/2026-07-20` und `journal/2026-07-27`: DE und EN jeweils
**byte-gleich** mit dem freigegebenen Wortlaut (maschinell verglichen, Markdown-
Quote/Fettung normalisiert), `date: 2026-08-01`. Die Einträge selbst sind unverändert —
der Hinweis ist angehängt, nichts redigiert (Diff geprüft).

---

## Kernfrage

**Sitzung 4 läuft durch, wenn alle drei Modelle das neue Pflichtfeld liefern — Happy
Path, Teilausfall (2 von 3) und Totalausfall (4 markierte Bereiche) habe ich durch Writer
und Tor gejagt, alle drei publizieren korrekt. Aber liefert auch nur ein Modell
`conditional` nicht als echtes JSON-Boolean, bricht die Sitzung ab — aus dem falschen
Grund: entschieden ist „ungültig markiert publizieren" (Nachtrag 3), gebaut ist „ganze
Sitzung scheitert am Schema-Tor" (`schema/session.schema.json:54` vs. `run_session.py:316`).
Da kein Modell das Feld je roh geliefert hat, ist das der wahrscheinlichste einzelne
Bruchpunkt am 6. August; eine Schema-Zeile behebt ihn.**

## Nicht geprüft / nicht prüfbar von hier

- **Ob die drei neuen Modelle (`claude-opus-5`, `gpt-5.6-sol`, `gemini-3.5-flash`) das
  Feld tatsächlich liefern** — `probe_conditional.py` durfte ich nicht ausführen
  (kostet Geld). Genau dafür ist es gebaut: ein Probelauf vor dem 6.8. beantwortet die
  Kernfrage empirisch statt statisch.
- Die Workflows in echter Ausführung (nur statisch gelesen) und die Actions-UI:
  ob `wart.yml` dort wirklich deaktiviert ist (Auftrag §0) — im Repo steht der Cron
  weiter, das war so vorgesehen.
- Ob `gemini-3.5-flash` das „stärkste verfügbare Modell" der Familie ist (Epochen-Vermerk
  verspricht das) — Steward-Entscheid, offline nicht verifizierbar; „flash" war historisch
  die Spar-Variante. Ein Satz Prüfung wert, bevor der Vermerk das behauptet.
- Das Zusammenspiel neuer `max_output_tokens: 32768` mit den OpenAI-/Gemini-Callern
  (Truncation-Risiko nur statisch eingeschätzt: fiele in den entschiedenen
  Markierungspfad, nicht in den Abbruch).
