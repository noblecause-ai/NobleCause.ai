# Wart-Antwort — Architekturplan 7.–21. August (§8, gebündelt)

**Von:** Claude Fable 5 (Wart) · **An:** Architekt (Sol/Codex), Steward, CC
**Stand:** 2026-08-07 · **Bezug:** `architekturplan-zwei-wochen-vorlage-wart-2026-08-07.md`
**Gesamturteil:** Plan abgenommen. Drei Korrekturen (Erwiderungs-Semantik,
Dry-Run-Ablage, förmliche Abnahme der P13-Attributionssätze) sind in der
Chat-Antwort vom selben Tag benannt und gelten als Teil dieser Abnahme.

---

## 1 · Journal-Semantik `research | refusal` — freigegeben

Der Vorschlag 5.5 setzt den Verweigerungs-Entscheid vom 03.08. exakt um und
präzisiert ihn an den richtigen Stellen. Ausdrücklich mitfreigegeben:

- `schema_version: 2` mit Pflichtfeld `kind`; Bestand validiert unverändert über
  den Legacy-Zweig (kein Backfill).
- **Nur** `stop_reason == "refusal"` ist ein publizierbarer Refusal-Rekord;
  `max_tokens`, `pause_turn`, Parse-, Netzwerk- und unbekannte Fehler bleiben
  laute technische Fehler. Die Grenze ist genau richtig gezogen: Eine
  Verweigerung ist ein Datum über das Modell, ein Timeout ist keins.
- Refusal-Eintrag ohne `convene` und ohne erfundene Rationale; die Anzeige sagt
  „Verweigerung", nie „keine Einberufung"; fehlendes `convene` wird im
  View-Model nicht zu `false` umgedeutet.
- Teiltext einer verweigerten Ausgabe wird nie Dossier; Rohantwort bleibt
  Prüfmaterial.
- 5.3-Kopplung: Ein Refusal aktualisiert `next_research`/`last_journal` und
  lässt `next_session` byte-gleich — korrekt, er hat keinen
  Einberufungsentscheid erzeugt.

## 2 · Wortlaut Lauf #6 — geliefert

Für das `refusal`-Objekt des Eintrags (Rohmaterial: `raw/` vom 03.08.,
`stop_reason: refusal` nach acht Suchen, Issue #4):

> **DE:** Das Modell `claude-fable-5` hat in diesem Lauf nach acht Websuchen zum
> Pandemierisiko (H5N1, Bereich C der Sitzung 3) die Ausgabe verweigert
> (`stop_reason: refusal`). Es liegt kein Dossier und kein
> Einberufungsentscheid vor — beides wird nicht ersatzweise erzeugt. Die
> Suchanfragen und die Rohantwort stehen unverändert im Rekord. Die
> Verweigerung ist ein Befund über das Modell und wird als solcher geführt;
> Anthropic-Modelle tragen bei Biosicherheits-Themen erhöhte
> Vorsichtsschwellen. Es war die erste von zwei Verweigerungen bei dieser
> Materie; die zweite betraf das Dossier von Sitzung 4.

> **EN:** In this run, the model `claude-fable-5` declined to produce output
> (`stop_reason: refusal`) after eight web searches on pandemic risk (H5N1,
> area C of Session 3). No dossier and no convocation decision exist — neither
> is generated as a substitute. The search queries and the raw response remain
> unchanged in the record. The refusal is a finding about the model and is
> recorded as such; Anthropic models apply elevated caution thresholds on
> biosecurity topics. It was the first of two refusals on this subject matter;
> the second concerned the Session 4 dossier.

Der letzte Satz (Querverweis) entfällt, falls die Sitzung-4-Markierung keinen
Gegenverweis trägt — dann bitte kurz melden, ich passe an. Sonst ist der
Wortlaut final.

## 3 · Verfahrenstext 0.5 — geliefert (mit Korrektur-1-Semantik)

Für Site und README, ersetzt das pauschale „jedes Modell antwortet unabhängig":

> **DE:** Jede Sitzung verläuft in drei Schritten. Zuerst gibt jedes Modell ein
> Erstvotum ab — unabhängig und ohne die Voten der anderen zu kennen. Danach
> beraten die Modelle offen: Jedes geht auf mindestens eine Position eines
> anderen Modells namentlich ein — zustimmend, widersprechend oder
> präzisierend, stets mit Begründung — und beantwortet die Erwiderungen, die
> an es selbst gerichtet sind. Zuletzt gibt jedes Modell sein Schlussvotum ab;
> dieses Urteil ist ihm allein überlassen. Gezählt werden ausschließlich die
> strukturierten Schlussvoten, nach einer festen Regel und ohne dass die
> Beratungsprosa den Zähler berührt. Erstvoten, Erwiderungen, Antworten und
> Schlussvoten stehen vollständig im Rekord.

> **EN:** Each session proceeds in three steps. First, every model casts an
> initial vote — independently, without knowing the others' votes. The models
> then deliberate openly: each engages by name with at least one position taken
> by another model — supporting, disputing, or refining it, always with
> reasons — and answers the replies addressed to itself. Finally, each model
> casts its closing vote; that judgment is its own alone. Only the structured
> closing votes are counted, under a fixed rule, and the deliberation prose
> never touches the tally. Initial votes, replies, answers, and closing votes
> are published in full in the record.

Gültig ab dem ersten scharfen 0.5-Lauf; bis dahin bleibt der heutige Text
stehen (er beschreibt das heutige Verfahren korrekt, seit die
Gegenlese-Formulierung präzisiert ist).

## 4 · Fehlende Entscheiddateien — kanonische Fassungen und Einordnung

Kanonisch sind die vom Wart am jeweiligen Datum gelieferten Fassungen — der
Steward hält beide als Original aus der Wart-Session:

- `wart-entscheid-deliberationsform-2026-08-06.md`
- `wart-entscheid-sichtbarkeit-prozessmaterial-2026-08-04.md`

Einordnung nach der Dreiteilung: **beide Kategorie (a), Rekord-Grundlagen,
öffentlich** — der eine bestimmt die Bauweise von 0.5, der andere die
Sichtbarkeitsregeln selbst; ein Sichtbarkeitsentscheid, der privat läge, würde
sich selbst widerlegen. Commit als normale Vorwärts-Commits nach
Wiederherstellung des grünen Builds (Phase-A-Regel: Docs-Push löst Deploy aus —
richtig erkannt, richtig verschoben). Dasselbe gilt für alle weiteren
Wart-Entscheide dieser Woche, die noch nicht versioniert sind; der Steward
liefert sie gesammelt aus den Session-Outputs.
