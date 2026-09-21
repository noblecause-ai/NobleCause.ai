# Wart-Review des Gesamtplans — 20.09.2026

**Historischer Bericht zu Anlauf 1 und 2.** Die inzwischen abgelegte vollständige
[Abnahme aus Anlauf 3](wart-abnahme-live-rat-2026-09-20.md) lautet
`freigegeben_mit_auflagen`. Der Steward hat anschließend den Backend-Bau beauftragt;
siehe [Umsetzungsstand](live-rat-backend-2026-09-20.md). Alle folgenden Kosten-
und Statusangaben beziehen sich auf das Ende der ersten beiden Anläufe.

Der Steward hat vor dem Bau einen Review durch den bisherigen Wart verlangt.
Der [Gesamtplan](gesamtplan-live-rat-wart-review-2026-09-20.md) hält seine
Vorgabe fest: fünf Mitglieder und Stimmen, wechselnder zusätzlicher Vorsitz,
beginnend mit Fable 5.1. Fable 5 bleibt als bei Bedarf konsultierter Reviewer
außerhalb des laufenden Betriebs. Der Plan umfasst auch Wochenaufgaben,
blinde Scout-Recherche, fortlaufende Debatte, öffentliche Übertragung,
Kostenkontrolle und den Übergang zu einem stabilen Betrieb.

## Tatsächlich vorgelegtes Material

Der Review wurde über den bereits geprüften OpenRouter-Weg an
`anthropic/claude-fable-5`, fest auf Endpunkt `anthropic`, geschickt.
Es gab keinen Modell- oder Anbieterwechsel.

Jede der beiden Anfragen enthielt genau die jeweilige Planfassung, das
Manifest und den öffentlichen Verfahrensentscheid vom 06.08.2026.
Die beiden Grundlagentexte wurden vorher anonym vom öffentlichen Repository
geladen und bytegleich mit dem lokalen Bestand abgeglichen. Keine lokalen
Meta-Unterlagen waren Bestandteil der tatsächlich gesendeten Anfragen.

Die automatische Freigabeprüfung hatte eine zuerst geplante, umfangreichere
Zusammenstellung wegen lokaler Hintergrunddokumente blockiert. Dieser Aufruf
wurde nicht ausgeführt. Nach Reduktion und öffentlichem Herkunftsnachweis
wurden die zwei unten dokumentierten Anfragen zugelassen. Dieser anfängliche
Vorbehalt ist damit erledigt; die spätere Verweigerung stammt vom Modellanbieter.

## Versuch 1: Ausgabelimit erreicht

- Eingereicht: Revision 1.
- Generation: `gen-1789918218-P87wewPnH31ebqzypIgY`.
- Modell/Anbieter bestätigt: Fable 5 / Anthropic; kanonischer Modellname
  `anthropic/claude-5-fable-20260609`.
- Nativer Abschluss: `max_tokens`, normalisiert `length`.
- 14.275 Inputtokens, 4.096 Outputtokens, davon 3.450 Reasoningtokens.
- Kosten: **0,34755 Credits**, zwischen Antwort, Generation und Key-Verbrauch
  vollständig abgeglichen.

Der sichtbare Anfang nennt „freigegeben_mit_auflagen“ und begrüßt den
Rollenwechsel. Die Antwort bricht aber bereits während der ersten Sachfrage
mitten im Satz ab. Die Auflagen und die weiteren Prüffragen fehlen. Dieser
Anfang wird ausdrücklich **nicht als Abnahme** ausgegeben.

Unveränderte Unterlagen:

- `.review/live-rat-wart-20260920/submitted-plan-r1.md`
- `.review/live-rat-wart-20260920/prompt-system.txt` und `prompt-user.txt`
- `.review/live-rat-wart-20260920/wart-response.md`
- `.review/live-rat-wart-20260920/raw/plan-review/`
- `.review/live-rat-wart-20260920/accounting.json`

## Reproduzierter Auszählungsbefund und Revision 2

Ein isolierter, synthetischer Aufruf der vorhandenen Auszählung zeigt:
Bei fünf Stimmen im Verhältnis 2:1:1:1 erhält die führende Organisation
`has_consensus: true`, mit offen ausgewiesenen zwei von fünf Stimmen.
Das ist die bisherige Zwei-Stimmen-Schwelle, keine bereits umgesetzte
Dreiermehrheit. Es wurden keine Sitzungs- oder Produktdateien geändert.

Revision 2 schlägt deshalb für das neue Verfahren ausdrücklich mindestens
drei von fünf Stimmen für eine gemeinsame Empfehlung vor, bei unverändertem
Nenner und ohne Stichentscheid des Vorsitzes. Die alte Regel und die alten
Rekorde bleiben ihrer Verfahrensversion zugeordnet. Diese Ergänzung wurde
dem Wart zur Prüfung vorgelegt; sie ist noch keine abgenommene Umsetzung.

Beleg: `.review/live-rat-wart-20260920/existing-tally-check.json`.

## Versuch 2: Anbieter-Verweigerung

- Eingereicht: Revision 2 einschließlich des Auszählungsnachtrags.
- Generation-ID der Antwort: `gen-1789918501-PN114KGSlEB4v8YffRhx`.
- Angefordert: dasselbe Fable 5 bei Anthropic; für diesen Review allein
  `reasoning.effort: medium` und maximal 12.000 Outputtokens, um genügend
  Platz für die eigentliche Antwort zu lassen. Produktkonfiguration unverändert.
- Antwort meldet `native_finish_reason: refusal`, `finish_reason: content_filter`,
  keinen Inhalt und keine Usage.
- Der Anbieter nennt eine vermutete Verletzung seiner Bedingungen zu
  Reverse Engineering oder zum Duplizieren von Modellausgaben. Das ist die
  gemeldete Ablehnungsbegründung, keine Feststellung dieses Berichts über
  den Zweck des Projekts. Beauftragt war eine Verfahrensprüfung.
- Die Generationsmetadaten waren nach den lesenden Nachfragen weiterhin
  nicht verfügbar (404). Deshalb fehlt eine vollständig abgleichbare
  Kostenabrechnung für diese Anfrage.

Nach der Verweigerung wurde kein weiterer Modellaufruf gesendet. Es gab
lediglich lesende Abfragen zu Generation und Key-Verbrauch. Für Versuch 2
war zum letzten Abruf **kein zusätzlicher Key-Abzug beobachtbar**; daraus
wird ohne Usage-/Generationsbeleg keine bestätigte Nullkostenrechnung abgeleitet.

Unveränderte Unterlagen:

- `.review/live-rat-wart-20260920-r2/submitted-plan-r2.md`
- `.review/live-rat-wart-20260920-r2/prompt-system.txt` und `prompt-user.txt`
- `.review/live-rat-wart-20260920-r2/raw/plan-review/openrouter-response.json`
- `.review/live-rat-wart-20260920-r2/generation-readonly-followup.json`
- `.review/live-rat-wart-20260920-r2/accounting-status.json`

## Budget und Arbeitsstand

Bestätigte neue Kosten: **0,34755 Credits**. Der beobachtete Gesamtverbrauch
des Keys liegt bei **4,50224507**, sein unverändertes 10-Credit-Limit lässt
**5,49775493 Credits** übrig. Die zweite Anfrage bleibt hinsichtlich einer
eigenen Abrechnungsquelle unaufgelöst.

247 Dateien aus Produktcode, Workflows, Schemata, Registraturen und
veröffentlichten Rekorden sind gegenüber dem Zustand vor diesem Auftrag
hashgleich. Es wurden nur Plan- und Review-Unterlagen angelegt. Kein Commit,
Push, Deploy, Rotationswechsel oder öffentlicher Sitzungslauf.

Es fehlt eine **vollständige Wart-Abnahme**, einschließlich der vorgeschlagenen
Wochenzuständigkeit und der neuen Mehrheitsschwelle. Eine abgebrochene
Zustimmung oder die Anbieter-Verweigerung ersetzt sie nicht. Die für eine
spätere Fortsetzung nötige konkrete Vorlage liegt vollständig vor.
