# Verfahrensnachtrag 0.6 — Live-Rat

Grundlage: Steward-Auftrag vom 20.09.2026 und
[Wart-Abnahme, Anlauf 3](wart-abnahme-live-rat-2026-09-20.md).
Der folgende Backend-Bau ist beauftragt; Frontend und öffentlicher Start
folgen erst nach Besprechung. Die Quellentscheidung bleibt wörtlich erhalten.
Dieser Nachtrag und die Schemaänderungen gehören gemeinsam in den späteren
Auslieferungscommit; die vorliegenden Arbeitsdateien sind noch nicht committet.

## Verfahrensversion und Auszählung (A1, A2)

Neue Sitzungen tragen `schema_version: 3` und das Pflichtfeld
`procedure_version: "0.6"` (Verfahrensversion). Bestehende Sitzungen ohne dieses
Feld bleiben beim bisherigen Verfahren. 0.5 bezeichnet weiterhin die
adressierte Einzel-Erwiderungsrunde. 0.6 ersetzt sie durch eine fortlaufende
Debatte. Kein Modell steuert den Mechanismus: Phasen, Budget, Redeanteile,
Rekord und Auszählung bleiben Programmregeln. Ein Ratsmitglied darf innerhalb
der Debatte die Gesprächsführung übernehmen. Der entsprechende Ausschluss
im Wart-Entscheid vom 06.08. wird für 0.6 abgelöst; kein erzwungener Dissens.

Die Rotation lautet Fable 5.1 → Astra → Grok → Kimi → GLM → Fable 5.1.
Der Vorsitz hat genau eine der fünf Stimmen und dasselbe Redekontingent.
Im Pilot gibt es höchstens zehn Sachbeiträge und zehn Moderationsaufrufe;
Wortvergabe nur an Mitglieder mit den bislang wenigsten Sachbeiträgen.
Erst- und Schlussvoten werden jeweils verdeckt erzeugt. Schlussvoten müssen
offene Einwände ausdrücklich beantworten, bevor sie ihre Empfehlung abgeben.

Bei 0.6 benötigt eine gemeinsame Empfehlung mindestens drei verschiedene
Sitzstimmen für dieselbe registrierte Organisation, bei festem Nenner fünf.
2:1:1:1 und 2:2:1 ergeben keine gemeinsame Empfehlung; 3:1:1 genügt. Die
Bestandsregel (mindestens zwei, kein Gleichstand) bleibt für alte Versionen
erhalten. Öffentlichkeit: „Mehrheit“, tatsächlicher Zählstand und Dissens.
Alle fünf technisch gültigen Schlussvoten sind Erfolgskriterium des **Piloten**,
keine allgemeine Bedingung dafür, einen unvollständigen Rekord aufzubewahren.

### Explizite Enthaltung nach Pilot 3

Steward-Auftrag: „bitte die zwei punkte klären“ — Enthaltungszählung und
Registrierung von Youth Impact. Neue Live-Sitzungen tragen zusätzlich
`ballot_contract: "explicit_abstention_v1"`. Der Pilot 3 und ältere Rekorde
bleiben unverändert und erhalten diesen Vertrag nicht nachträglich.

Jedes Erst- und Schlussvotum enthält je Säule genau eine Entscheidung:
`decision: "recommend"` mit Organisation und expliziter Konditionalität oder
`decision: "abstain"` mit `abstention_reason`. Bei Enthaltung sind Organisation,
Spendenweg, Konditionalität und Vorbehalt jeweils `null`. Ein im Text genannter
Prüfkandidat wird dadurch nicht zur Empfehlung. Die Rollenpersona und die
ungezwungene Selbstauskunft bleiben bestehen.

Enthaltungen zählen weder als Empfehlung noch als ungültiges Votum und
verändern den Nenner nicht. `votes_valid` zählt auswertbare registrierte
Empfehlungen, `votes_abstained` Enthaltungen, `votes_invalid` fehlende oder
ungültige Entscheidungen. Die drei Zahlen ergeben fünf. Begründungen stehen
in `abstentions`; eine Mehrheit verlangt weiterhin mindestens drei Empfehlungen
für dieselbe registrierte Organisation. Zwei Empfehlungen und drei
Enthaltungen ergeben keine Mehrheit. Fehlende, doppelte oder widersprüchliche
Entscheidungen werden nicht aus Prosa geraten.

Für Pilot 3 liegt eine gesonderte, kuratierte Korrekturauswertung mit
Original-Hashbelegen vor: Youth Impact fünf bedingte Empfehlungen, NTI vier
bedingte Empfehlungen und Astras erklärte Enthaltung. Sie ersetzt keinen
Originalrekord oder Modelltext. Details und Quellen:
[Klärung nach Pilot 3](live-rat-votumsklaerung-2026-09-20.md).

Die Wochenaufgabe geht im vorbereiteten neuen Verfahren an den nächsten
Vorsitz. Striktes `convene`-Boolean, lauter Vertragsbruch und sichtbarer
Refusal gelten für alle fünf Familien. Der neue Pfad bleibt ausgeschaltet;
der öffentliche Start setzt die ausdrückliche Bestätigung dieser Wochenrolle
voraus (C3). Fable 5.1 als erster Vorsitz ist bereits vom Steward festgelegt.

## Ereignisrekord (A3)

`schema/live-events.schema.json` beschreibt den Ereignisstrom. Nummern beginnen
bei eins und sind lückenlos; der Backend-Validator prüft Nummern und Hashkette.
Die JSON-Datei wird atomar ersetzt und ausschließlich um Ereignisse ergänzt.
Abgeschlossene Reden bleiben als UTF-8-Text bytegleich; ihr SHA-256-Wert steht
im Ereignis. Ein gültiger Endrekord verweist auf denselben archivierten
Ereignisstrom und dessen Hash. Ein veröffentlichter Stream bleibt auch nach
Ende/Abbruch erhalten; er wird nie durch eine zusammenfassende Fassung ersetzt.
Eine Lücke, nachträgliche Änderung oder unklare Abrechnung stoppt den Lauf.
Übertragung darf gespeicherte Bytes wiederholen, niemals Modellaufrufe.

## Manifestprüfung (C2)

`manifest.md`, Version 1.0, enthält weder drei Sitze noch eine
Zwei-Stimmen-Regel noch das wörtliche Ablaufsteuerungs-Verbot. Keiner der vom
Wart benannten Änderungsfälle trifft zu. Das Manifest bleibt unverändert.

## Öffentliche Texte — für die spätere Frontend-Besprechung

Die DE/EN-Texte des Gesamtplans werden mit beiden Wart-Korrekturen übernommen:
eigene Beiträge und möglicher Einfluss der Vorsitzfragen werden ausdrücklich
genannt; modellgenannte Suchanfragen heißen Selbstauskunft. Dieser Backend-
Auftrag baut die Texte nicht in die Site ein.

## Gates nach dem Backend-Bau

Vor bezahlten Tests: B1–B3 offline belegen; B4 benötigt einen belegten Bound
für den konkreten Input jedes Aufrufs samt Schlussvotenreserve. Tokenzählungen
aus einer anderen API oder bloße Zeichen-/Token-Schätzungen genügen nicht.
Fehlende Evidenz wird als Sperre umgesetzt und nicht durch den gesamten
Katalogkontext ersetzt. Anschließend fünf Canaries und isolierter Gesamtlauf.
Vor Veröffentlichung zusätzlich C1–C3, Frontend-Besprechung und Auslieferung.
