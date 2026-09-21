# Erste öffentliche Live-Sitzung — Inbetriebnahme

Steward-Auftrag vom 21.09.2026: „bitte live setzen und erste sitzung durchführen“.
Ergänzung: Vorher für alle fünf neuen Ratsmitglieder eigene Medaillons über das
vorhandene Bestellverfahren bestellen und einbauen. Der OpenRouter-Key wurde
vom Steward von 20 auf 40 Credits erhöht. Kosten werden weiterhin je Modell
beobachtet; ein Anbieterlimit wird nicht als belegte Kostenobergrenze ausgegeben.

## Anschluss

Der bestehende SSH-Deploy-Zugang zu `/srv/noblecause/` wird verwendet. Auf dem VPS
liegt der kleine Dateipublisher außerhalb des Webroots unter
`/home/noblecause/council-runtime/`; Python-Venv und JSON-Schema-Validator sind
vorhanden. Es gibt keinen neuen HTTP-Dienst und keinen OpenRouter-Key auf dem VPS.

`SshPublisher` überträgt ausschließlich die öffentliche Sitzungsbeschreibung und
den bereits geprüften Ereignisrekord über authentifiziertes SSH. Der Empfänger
prüft dieselben Schema-, Hash- und Präfixregeln unter einer Prozesssperre. Er
schreibt atomar öffentlich lesbare Dateien und bestätigt den Hash der Original-
Ereignisdatei. Ohne passende Bestätigung erfolgt kein weiterer Modellaufruf.
Das Lebenszeichen nutzt denselben Weg. Site-Deploys schließen `/live/` aus.

Ein technischer HTTPS-Test außerhalb des Rats-Feeds unter
`/live-check-20260921/` hat zwei ausdrücklich synthetische Ereignisse bytegleich
zurückgeliefert. Es gab dabei keine Modellaufrufe.

## Erster Lauf

Der erste Live-Lauf verwendet den ausdrücklich gewählten Modus `--public-session`
zusätzlich zu `--live-council --observe-costs`. Der Modus ist standardmäßig aus.
Er verlangt eigene freigegebene Medaillons und einen angeschlossenen Feed.
Der Originalrekord entsteht unter `sessions/<id>/`; erst sein validierter
Abschluss wird übernommen und dreht den Vorsitz genau einmal weiter. Abbrüche
bleiben im öffentlichen Ereignisarchiv. Bestätigte Antworten werden mit
`--resume` wiederverwendet, unklare Aufrufe niemals erneut gesendet.

Frage: Welche Intervention und umsetzende Organisation bietet nach der
vorliegenden aktuellen Evidenz je NobleCause-Säule die stärkste begründete
Empfehlung für zusätzliche Mittel, und welche Unsicherheiten oder Gegenbelege
könnten diese Empfehlung ändern?

Quelle: das bereits bezahlte blinde Drei-Scout-Dossier vom 20.09.2026, innerhalb
seiner siebentägigen Aktualitätsfrist. Die Verwendung wird als Wiederverwendung
mit Datum und Hash im Rekord ausgewiesen. Die neuen Schlussvoten verwenden den
Vertrag `explicit_abstention_v1`; die alten Pilotrekorde werden nicht korrigiert.

Die bestehende Website-Auslieferung über Push nach `master` bleibt der Deployweg.
Die dauerhafte Standardaktivierung des neuen Sitzungsworkflows wurde von der
automatischen Freigabeprüfung wegen ihres über den ersten Lauf hinausreichenden
Umfangs abgelehnt und deshalb nicht vorgenommen. Insbesondere bleiben die
bestehenden automatischen Verfahrensschalter unverändert. Der Wochenrollenwechsel
ist als gesonderte Steward-Frage offen; die erste Besetzung des Vorsitzes durch
Fable 5.1 ist bereits bestätigt.

## Vollständige Antworten trotz überschrittenem Anbieter-Tokenlimit

Bei der Medaillonbestellung lieferte Grok eine vollständige Antwort, meldete
aber 3467 abgerechnete Ausgabetokens bei 3000 angeforderten Tokens (davon
3298 interne Reasoning-Tokens). Der strikte Adapter stoppte korrekt.

Im ausdrücklich gewählten Kostenbeobachtungsmodus wird eine solche Abweichung
nun unter `output_limit_observation` protokolliert und nach belegter Abrechnung
akzeptiert. Im begrenzten Modus bleibt sie ein Fehler. Abgeschnittene Antworten,
unbekannte Abschlussgründe, unklare Abrechnung und Preisüberschreitungen bleiben
Fehler. Die gespeicherte Grok-Antwort wurde ohne erneute Inferenz übernommen;
ursprünglicher Fehlerbeleg und zusätzliche Übernahme bleiben erhalten.

## Auslieferung und Beginn

Website und Medaillons: Commit `fd02f578f9220342432e66d6543defeace143d07`,
[erfolgreicher Produktions-Deploy](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/35631869839).
Vor Auslieferung: 311 Backend-Tests, 60 Website-Tests, Schema-Tor und
Produktionsbuild erfolgreich. 129 historische Dateien unverändert; sechs alte
Medaillon-Einträge objektgleich. Original-Rohantworten behalten einschließlich
Transport-Leerzeichen ihre ursprünglichen Bytes; die Quellcode-Formatprüfung
ist grün.

Die öffentliche Sitzung `2026-09-21-live` wurde als Sitzung 6 am 21.09.2026
um 17:26 UTC begonnen. Vorsitz: Fable 5.1, Rotationsindex 0. Der öffentliche
Ereignisrekord liegt unter `/live/sessions/2026-09-21-live/events.json`.
Das vor dem Lauf abgefragte Key-Limit betrug 40 Credits, der bestätigte bisherige
Verbrauch 14,363424135 Credits und der verfügbare Rest 25,636575865 Credits.

Die fünf Medaillons und zwei Wart-Prüfungen kosteten zusammen 0,377880134 Credits
(siehe `asset-originals/medaillons-kommission-3.md`). Das wiederverwendete
Recherche-Dossier trägt SHA-256
`bd04167c7a7a0f12c1627a568322f07c81462b7f7757237b8f1eda136eea54f4`.
Seine 27 Original-Scout-Artefakte sind zusätzlich unverändert unter
`sessions/2026-09-21-live/research-raw/` gesichert. Daraus entstanden keine neuen
Recherchekosten.

## Abschluss

Sitzung 6 ist abgeschlossen und genau einmal übernommen. Alle fünf Erst- und
Schlussvoten sind gültig, alle zehn Sachbeiträge liegen vor. Der vollständige
Rekord enthält 59 Ereignisse einschließlich eines erhaltenen Abbruchs und einer
Wiederaufnahme. Anlass und erlaubte Behandlung von Kimis 186-Wort-Beitrag sind
in `live-rat-redelaenge-2026-09-21.md` dokumentiert. Sämtliche neun bis dahin
bezahlten Antworten wurden ohne neue Inferenz wiederverwendet.

Endergebnis aus der deterministischen Zählung: B / Against Malaria Foundation
5 von 5, davon Astra mit Vorbehalt; A, C und D jeweils 5 Enthaltungen. Keine
ungültigen oder unaufgelösten Schlussstimmen. Die Oberfläche zeigt Enthaltungen
als solche, nicht als Meinungsstreit oder fehlende Antworten.

Kosten der Sitzung: **7,214258149 Credits**, 31 Modellaufrufe. Aufteilung:

| Modell | Aufrufe | Credits |
|---|---:|---:|
| Claude Fable 5.1 | 15 | 5.54399 |
| GPT-6 Astra | 4 | 1.10417450 |
| Grok 4.6 | 4 | 0.217588 |
| Kimi K3 | 4 | 0.26022705 |
| GLM-5.3 | 4 | 0.088278599 |

Fable enthält zusätzlich zu seinen vier Ratsbeiträgen zehn Moderationen und die
Leserfassung. Der gesonderte Wart-Review zur Wiederaufnahme kostete 0,17493
Credits. Mit Medaillonbestellungen und deren Prüfungen (0,377880134) beträgt der
Verbrauch dieses Inbetriebnahme-Auftrags **7,767068283 Credits**.
Nach dem Abschluss bestätigt die Key-API 21,752612284 verbrauchte und
**18,247387716 verbleibende Credits** innerhalb des 40-Credit-Limits.

SHA-256 des öffentlichen Ereignisrekords:
`d143e42e16a83b88af15937957332c48da1ef5aa0165b215e2d4c80bb4d96e48`.
Ein erneuter HTTPS-Abruf nach Abschluss war bytegleich zum lokalen Original.
SHA-256 des übernommenen `session.json`:
`b6c24ced0b7f6a455ec068bd7c1a76e41e40e3b8414182f77ee4987a1023813a`.

Nächster Vorsitz: Astra (Index 1). Nächster regulärer Sitzungstermin laut
bestehendem 30-Tage-Abstand: 21.10.2026, 12:00 UTC. Unbekannte Schedule-Felder
sind erhalten. Der laufbezogene Redetoleranz-Nachtrag ist kein neuer Standard;
der Wochenrollenwechsel bleibt eine gesonderte offene Bestätigung.

Die abschließende Browserprüfung deckt das veröffentlichte Ratsgespräch und die
Archivansicht ab. Beim ersten Archivaufbau wurde die Kostenliste auf die bereits
vom Backend berechneten Modell-Summen umgestellt: mehrere Aufrufe desselben
Modells dürfen keine doppelten Svelte-Schlüssel erzeugen. Die Oberfläche zählt
keine Stimmen und summiert keine Modellkosten selbst. Die Verfahrenstexte der
drei Räume wechseln für abgeschlossene 0.6-Rekorde auf fünf Sitze und die
Dreiermehrheit; historische Sitzungsprosa bleibt unverändert.
