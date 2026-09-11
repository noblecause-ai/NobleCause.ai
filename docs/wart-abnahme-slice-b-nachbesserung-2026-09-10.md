# NobleCause.ai — Slice B, Nachbesserung zur Wart-Abnahme

Stand: 10. September 2026
Basis: `origin/master` / `de50cfd`
Status: lokal, beide Feature-Schalter aus, nicht gestaged, nicht committet,
nicht gepusht, keine API- oder Rekordläufe

## Gegenstand

Diese Vorlage beantwortet ausschließlich die drei Auflagen aus der
Teil-Abnahme des Warts.

### 1. Verpflichtende adressierte Erwiderung

- Jedes Ratsmodell muss genau eine fremde, überprüfbare Position über die
  exakte Modell-ID adressieren.
- `stance` ist Pflicht und ausschließlich `support | dispute | refine`.
- Eine Enthaltung ist weder im Prompt noch im Parser, Schema oder UI-Vertrag
  vorhanden. Begründete Zustimmung wird als `support` geführt.
- Ungültige oder technisch ausgefallene Zulieferungen bleiben als `invalid`
  beziehungsweise `unavailable` sichtbar; sie werden nicht in eine gültige
  Erwiderung umgedeutet.
- Nur gültige, exakt adressierte Strukturfelder werden dem Zielmodell vor dem
  Schlussvotum zugestellt. Die Beratungsprosa berührt die Aggregation nicht.

### 2. Doppelte Scout-Verweigerung

- Verweigern alle konfigurierten Scouts explizit mit
  `stop_reason == "refusal"`, schreibt der Lauf einen Journal-Rekord der neuen
  Form `schema_version: 2`, `kind: "refusal"`.
- Dieser Rekord enthält die Modelle, Rohpfade, tatsächlich beobachteten
  Suchanfragen, Kosten und einen sachlichen DE/EN-Vermerk.
- Er enthält absichtlich weder `convene` noch `convene_rationale`; der Wart wird
  in diesem Pfad nicht aufgerufen.
- `schedule.last_journal` und `next_research` werden fortgeschrieben;
  `next_session` und unbekannte Schedule-Felder bleiben erhalten.
- Ein technischer Doppelausfall, ein Parse-Fehler oder jeder andere
  `stop_reason` erzeugt weiterhin keinen publizierbaren Rekord und bricht laut
  ab.
- Journalübersicht, Journaldetail und Study-Zeitschicht stellen den Refusal als
  Verweigerung ohne Einberufungsentscheid dar, nicht als „nicht einberufen“.

### 3. Entscheidquellen

Der wörtliche öffentliche DE/EN-Verfahrenstext liegt bereits in
`docs/wart-antwort-architekturplan-2026-08-07.md`, Abschnitt 3.

Die drei vom Wart zusätzlich verlangten Originaldateien wurden aus ihren
kanonischen Quellen unverändert in den Slice übernommen:

- `docs/wart-entscheid-deliberationsform-2026-08-06.md` aus dem
  claude.ai-Projekt `noblecause.ai`
- `docs/wart-entscheid-sichtbarkeit-prozessmaterial-2026-08-04.md` aus dem
  lokalen Meta-Bestand (bytegleich; SHA-256
  `e143fa74b08f162a8f5db2d3773e787363ca8cbe3b8886143530cbd92828f22c`)
- `docs/claude/noblecause-einstiegskonzept-2026-08-02.md` aus dem
  `claude/`-Namensraum des claude.ai-Projekts `noblecause.ai`

Damit liegen Entscheid, Sichtbarkeitsregel und Einstiegskonzept gemeinsam mit
dem darauf beruhenden Bau vor. Insbesondere bestätigt der Originalentscheid
die verpflichtende adressierte Erwiderung mit den Formen Zustimmung,
Widerspruch oder Präzisierung.

## Prüfstand

- Python: 103/103 Tests grün.
- Synthetischer Doppelt-Refusal: Journal-Schema gültig, kein Wart-Aufruf, kein
  Einberufungsfeld, Schedule-Fremdfeld und `next_session` erhalten.
- Schema-Tor: 4/4 Sitzungen und 14/14 bestehende Journale gültig.
- Site: 45/45 Tests grün; statischer Produktionsbuild erfolgreich.
- `git diff --check`: sauber.
- Bestehende Sitzungs-, Journal- und Commission-Rekorde unverändert.

## Erbetene Entscheidung des Warts

Volle Abnahme des nachgebesserten Slice B einschließlich der drei
Entscheidquellen. Die beiden Feature-Schalter bleiben auch nach einem späteren
Commit auf `enabled: false`.
