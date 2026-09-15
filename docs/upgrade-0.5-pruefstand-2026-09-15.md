# NobleCause.ai — Prüfstand Punkte 1–3

**Stand:** 15. September 2026  
**Status:** lokaler Architektur-Slice, nicht committet, nicht gepusht

## 1 · Betrieb schließen

- Der Wart-Lauf vom 14.09. ist als `journal/2026-09-14` auf `master` vorhanden.
- `schedule.json` zeigt auf `next_research = 2026-09-21T06:00:00Z` und
  `next_session = 2026-10-14T12:00:00Z`.
- Es gibt aktuell keinen laufenden Workflow und kein offenes GitHub-Issue.
- `session.yml` schließt nach einem erfolgreichen **scharfen** Sitzungscommit nun
  auch offene `session-due`-Issues. Trockenläufe und No-op-Läufe schließen sie
  ausdrücklich nicht.

## 2 · Zwei Scouts prüfen

- Der vorhandene Zwei-Scout-Vertrag bleibt unverändert: verschiedene Familien,
  mindestens eine außerhalb des Rates, gleiche Aufgabe, getrennte Rohpfade,
  sichtbare Ausfälle und exakter Divergenzausweis.
- Der fehlende zweite Websuche-Adapter ist ergänzt: Google Search Grounding über
  den bestehenden `google-genai`-Client.
- Die Provider-Rohantwort bleibt vollständig erhalten; Stop-Grund und eindeutige
  Suchqueries werden für den bestehenden Scout-Vertrag normalisiert.
- Sicherheitsblockaden werden als sichtbare `refusal` behandelt, technische
  Fehler bleiben laut.
- Die tatsächlichen Google-Suchqueries bestimmen Zählung und Kosten; der
  aktuelle Listenpreis ist 14 USD je 1.000 Requests nach dem Freikontingent.
- Die produktive Konfiguration bleibt aus. Mit dem heutigen Dreier-Rat wäre
  Google nicht „außerhalb des Rates“; mit dem vorgeschlagenen Fünfer-Rat ist die
  Invariante erfüllt.

## 3 · Deliberation 0.5 prüfen

- Der bereits vom Wart abgenommene Bau bleibt hinter
  `features.deliberation_0_5.enabled = false`.
- Der synthetische Vertrag prüft: genau eine fremd adressierte Erwiderung pro
  Modell, `support | dispute | refine`, nur gültige Zustellung, Antwort im
  Schlussvotum und Aggregation ausschließlich aus strukturierten Schlussvoten.
- Bestehende Rekorde bleiben unverändert; die 0.5-Schemaerweiterung wird erst in
  einem neuen Rekord verwendet.

## Noch ausstehendes Aktivierungsgate

Ein echter bezahlter Zwei-Scout-/0.5-Dry-run wird nicht gegen die überholte
Dreierbesetzung ausgeführt. Er folgt nach Bereitstellung der drei neuen
Provider-Secrets und Anbindung des vorgeschlagenen Fünfer-Rats in einem
isolierten Lauf mit ausdrücklich festgelegtem Budgetdeckel. Dadurch entsteht
kein Wegwerf-Rekord und kein unnötiger API-Aufwand.

## Lokale Abnahme

- `pytest -p no:cacheprovider gremium/tests`: **109/109 grün**;
- `schema_gate.py all`: **5 Sitzungen und 15 Journale gültig**;
- `npm test`: **45/45 grün**;
- `npm run build`: **grün**, nur die zwei bekannten Svelte-Hinweise zu
  `CouncilRoom.svelte:29` und `StageHero.svelte:38`;
- der `session-due`-Schließpfad wurde mit einem isolierten `gh`-Stub geprüft:
  passendes Issue erkannt, kommentiert und als erledigt geschlossen;
- `git diff --check`: sauber.
