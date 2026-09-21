# Live-Rat 0.6 — Backend-Abnahme, 20.09.2026

**Nachfolgender Steward-Entscheid:** Der erste bezahlte Pilot ist inzwischen
mit [Kostenbeobachtung ohne Eingabegrenze](live-rat-kostenbeobachtung-2026-09-20.md)
beauftragt. Die unten genannte B4-Sperre beschreibt den ursprünglichen
Backend-Abnahmestand und gilt weiter für den Standardmodus.

**Stand:** Backend-Pilot implementiert und offline geprüft, standardmäßig aus.
Keine neuen Modellaufrufe oder API-Kosten in diesem Bauauftrag. Kein Commit,
Push oder Deploy. Der Frontend-Einbau wird wie beauftragt vorher besprochen.

Grundlagen: [vollständige Wart-Abnahme](wart-abnahme-live-rat-2026-09-20.md),
[Gesamtplan](gesamtplan-live-rat-wart-review-2026-09-20.md) und
[Verfahrensnachtrag 0.6](verfahren-0.6.md). Die abgelegte Wart-Antwort wurde
bytegleich aus `meta/noblecause/wart-review-live-rat-2026-09-20.md` übernommen.
Die frühere Meldung „keine Abnahme“ beschreibt nur Anlauf 1 und 2.

## Gebaut

- Fünf unabhängige Erstvoten, dann eine fortlaufende Debatte. Jeder neue Redner
  sieht alle bis dahin abgeschlossenen Beiträge. Erstvoten werden gemeinsam
  offengelegt; die fünf Schlussvoten entstehen anschließend voneinander getrennt.
- Ein zusätzlich vorsitzendes Ratsmitglied, beginnend mit Fable 5.1. Höchstens
  zwei Sachbeiträge mit je 180 durch Leerraum getrennten Wörtern pro Sitz;
  Wortvergabe nur an die bislang wenigsten Redner. Moderation und eigener
  Sachbeitrag sind getrennte Aufrufe. Kein Stichentscheid, keine zweite Stimme.
- Schlussvoten beginnen mit einem Einwands-Teil und beantworten jeden
  adressierten Einwand einzeln. Fehlende Antworten sind ein Vertragsfehler.
  Die Zählung benötigt für 0.6 mindestens drei von fünf Sitzstimmen; ungültige
  Stimmen verkleinern den Nenner nicht. Historische Regeln bleiben erhalten.
- Lokaler Ereignisrekord mit fortlaufenden Nummern, Zeit, Rolle, Modell,
  Originaltext und SHA-256-Kette. Der Abschluss verweist auf denselben
  Ereignisrekord; der Validator prüft bytegleichen Wortlaut und Redeanteile.
  Die optionale Dateispiegelung akzeptiert nur unveränderte Präfixe.
- Dauerhafte Aufrufbelege vor jeder Inferenz, Abbruchereignisse und explizites
  `--resume`. Bestätigte Antworten werden aus ihren Belegen wiederverwendet.
  Ein möglicherweise bezahlter, unbestätigter Aufruf wird nicht erneut gesendet.
  Auch ein Fehler bei der abschließenden Dateiprüfung bleibt sichtbar und kann
  ohne neue Inferenz fertiggestellt werden.
- Rotation erst durch ausdrückliche Übernahme eines gültigen, nicht als Probe
  markierten Abschlusses, und genau einmal je Rekord. Proben/Abbrüche drehen
  die Rotation nicht weiter. Unbekannte Schedule-Felder bleiben erhalten.
- Wochenrolle über denselben Ratsadapter: striktes `convene`-Boolean,
  Vertragsfehler ohne erfundene Entscheidung, native Verweigerung als Journal.
  Jeder der fünf Sitze kann diese Rolle übernehmen; ein dauerhaft externer
  Wart ist dafür keine Konfigurationsabhängigkeit. Die drei blinden Scouts
  sind Voraussetzung des neuen Wochenpfads.
- Gemeinsame Prozesssperre für Sitzung, Wochenlauf und Übernahme;
  GitHub-Sitzungs- und Wochenworkflow teilen jetzt eine Konkurrenzgruppe.
  OpenRouter-Vorprüfung ist vorbereitet. Die öffentlichen Workflows verwenden
  weiterhin den bisherigen Ablauf; Aktivierung ist ein gesonderter Schritt.

Kernmodule: `gremium/live_session.py`, `live_debate.py`, `council_state.py` und
`cost_bounds.py`. Der vorhandene Ratsadapter wurde um kanonische Modellnamen,
den belegten Grok-Abschlussgrund und begrenzte lesende Abrechnungsnachfragen
ergänzt. Endpunkte bleiben fest; es gibt keine Inferenzwiederholung oder Ersatzroute.

## Kostenauflage B4 — noch offen

Der neue Budgetwächter prüft vor jedem bezahlten Schritt bestätigte Ist-Kosten,
die belegte Obergrenze dieses Aufrufs und die Reserve für alle noch erforderlichen
Schlussvoten samt Zusammenfassung. Wird die Debatte zu teuer, wird sie mit
sichtbarem Grund geschlossen. Fehlende Abrechnung stoppt Folgeaufrufe.

**Für die fünf produktiven Endpunkte fehlen noch belegte Eingabegrenzen.**
`live_council.input_bounds` bleibt deshalb leer. Die echte Vorprüfung bricht
nachweislich mit `B4: kein belegter Input-Bound` ab, bevor sie einen Key lädt
oder das Netzwerk verwendet. Die Testbelege sind ausdrücklich synthetisch
und werden nicht als Anbieterbeweis übernommen.

Ein zulässiger Beleg muss Modell, Endpunkt, Quantisierung, maximale Größe des
tatsächlich serialisierten Requests und die daraus belegte maximale Eingabe-
Tokenzahl einschließlich Nachrichtenrahmung verbinden. Er wird per SHA-256
an eine geprüfte Belegdatei gebunden. Durchschnittswerte, eine fremde
Tokenzähl-API oder Zeichen-pro-Token-Schätzungen erfüllen das nicht. Die
pauschale Reservierung des gesamten Modellkontexts wird im neuen Pfad nicht
als Ersatz verwendet. Ein Key-Limit allein löst diese Auflage ebenfalls nicht.

Erst danach folgen fünf kleine echte Ratsadapter-Tests und ein isolierter
Gesamtlauf mit vorhandener Recherche. Den verfügbaren Rest des bereits
genehmigten 10-Credit-Limits dann frisch abgleichen. Der Bau hat nichts davon
verbraucht; der frühere Kontostand ist keine aktuelle Guthabenzusage.

## Bedienung des isolierten Piloten

Nach belegtem B4-Vertrag, mit ausdrücklich gewählter Frage und festem Budget:

```bash
python gremium/run_session.py --live-council \
  --session-id LIVE-PILOT-ID --question 'FREIGEGEBENE FRAGE' \
  --title 'FREIGEGEBENER TITEL' --dossier-json /pfad/zum/dossier.json \
  --budget-cap EUR-BETRAG
```

Das Dossier muss die drei bestätigten blinden Scout-Berichte mit Provenienz
enthalten und höchstens sieben Tage alt sein. Der Pilot schreibt unter
`.review/live-sessions/LIVE-PILOT-ID/`: eingefrorenen Auftrag, Dossier,
Rohantworten, Ereignisse und bei bestandenem Abschluss `session.json`.
`--output-dir` kann einen anderen isolierten Elternpfad wählen; veröffentlichte
Rekord- und Site-Verzeichnisse sind gesperrt. `--resume` verlangt identische
Eingaben. Die Probe bleibt `dry_run: true` und publiziert nichts.

Ein öffentlicher Publisher, sein VPS-Pfad, die Website-Abfrage und die
Produktionsübernahme sind noch nicht angeschlossen. Die Backend-Funktion
zur Rotation ist vorhanden; der Pilot ruft sie absichtlich nicht auf.

## Nachweise und verbleibende Freigaben

- **249 Python-Tests grün**, davon 33 neue Fälle zum Live-Rat. Ein vollständiger
  synthetischer Lauf mit dem echten Adapter umfasst 31 Aufrufe; ein Abbruch
  nach gespeicherter Antwort und Wiederaufnahme verursacht zusammen ebenfalls
  genau 31 Inferenzaufrufe. Das belegt die Mechanik, nicht echte Modellqualität.
- **46 Site-Tests mit Build grün**; bestehende Svelte-Hinweise bleiben bestehen.
  Schema-Tor: fünf historische Sitzungen und 15 Journale gültig. `git diff --check`
  ohne Befund.
- **259 geschützte Dateien hashgleich** zum Beginn dieses Bauauftrags:
  122 veröffentlichte Rekorddateien, 133 Site-Dateien sowie Modell- und
  Organisationsregister, Schedule und Manifest. Schon zuvor vorhandene
  Frontend-Änderungen zum Scout-Adapter wurden weder erweitert noch verworfen.
- Wart **A1–A3**: Nachtrag, Versionspflicht, Mehrheit und Ereignisregeln liegen
  vor. Der in A1 verlangte Commit steht mit der Auslieferung noch aus;
  `AGENTS.md` verlangt dafür Steward-Freigabe. Der aktuelle Bauauftrag wurde
  als Auftrag zur lokalen Umsetzung ausgeführt, nicht als Commitfreigabe.
- **B1–B3** sind offline belegt. **B4** bleibt die technische Startsperre.
- **C1–C3** bleiben Startbedingungen: Belegklassen und Quantisierung öffentlich
  darstellen, korrigierte DE/EN-Texte einbauen, Wochenrollen-Übergang ausdrücklich
  bestätigen. Fable 5.1 als erster Vorsitz ist bereits bestätigt. Die
  Manifestprüfung ergab keinen Änderungsbedarf. Modellregistratur, öffentliche
  Workflow-Aktivierung und Übertragung folgen erst beim vereinbarten Einbau.

Maschinelle Prüfergebnisse und Logs: `.review/live-backend-20260920/`.
