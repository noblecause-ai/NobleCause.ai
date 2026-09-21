# Klärung nach Live-Rat-Pilot 3

Steward-Auftrag: „bitte die zwei punkte klären“. Beide Punkte sind im Backend
bearbeitet; es wurden keine weiteren Modellaufrufe ausgeführt.

## Ergebnis für den abgeschlossenen Piloten

Die gesonderte, kuratierte Korrekturauswertung ergibt:

| Säule | Organisation | Empfehlungen | Davon bedingt | Enthaltungen | Ungültig |
|---|---|---:|---:|---:|---:|
| A | Youth Impact | 5 von 5 | 5 | 0 | 0 |
| B | Against Malaria Foundation | 5 von 5 | 4 | 0 | 0 |
| C | Nuclear Threat Initiative | 4 von 5 | 4 | 1 (Astra) | 0 |
| D | Lead Exposure Elimination Project | 5 von 5 | 5 | 0 | 0 |

Alle vier erreichen damit die unveränderte Mehrheitsschwelle von drei
Sitzstimmen. Die mittlere Modellkonfidenz für NTI beträgt unter den vier
Empfehlenden 0,51 statt 0,48 unter Einschluss der Enthaltung. Diese Kennzahl
ist eine Selbsteinschätzung der Modelle, keine gemessene Erfolgswahrscheinlichkeit.

Die Korrekturauswertung ist eine ausdrücklich kuratierte Interpretation der
vorliegenden Originalvoten. Astras Entscheidung wurde anhand der bereits
dokumentierten Erklärung im Schlussvotum eingeordnet; alle anderen Voten
behalten ihren Empfehlungsstatus. Ein automatisches Erraten von Enthaltungen
aus Formulierungen wurde nicht eingebaut. Der neue deterministische
Aggregator verarbeitet anschließend ausschließlich die expliziten Felder.

Das Original einschließlich Ereigniskette, Kosten, Modelltexten und der
damaligen fehlerhaften Zählung bleibt bytegleich. Auch die damalige
Leserfassung wird nicht ersetzt. Die Korrekturdatei enthält Hashwerte des
Sitzungsrekords, der Ereignisse, aller fünf Schlussantworten und des verwendeten
Organisationsregisters, die ursprünglichen C-Felder sowie die abgeleiteten Voten.

Artefakt: `.review/live-vote-fix-20260920/pilot-03-clarified-tally.json`.

## Enthaltungen in künftigen Sitzungen

Der neue Vertrag `explicit_abstention_v1` unterscheidet je Säule ausdrücklich
`recommend` und `abstain`. Eine Enthaltung benötigt eine Begründung und
enthält keine Organisation, Spendenadresse oder Förderbedingung. Kandidaten
dürfen im Text weiter besprochen werden. Die gleiche Vorgabe gilt für
Erst- und Schlussvoten; die Leserfassung muss Enthaltungen getrennt nennen.

Enthaltungen werden im Datenrekord separat ausgewiesen, nicht als Zustimmung
oder als ungültig gezählt. Sie verändern weder die fünf Sitze noch die
Mehrheit von drei Stimmen. Fehlende und widersprüchliche Statusangaben sowie
Doppelvoten bleiben sichtbare Fehler. Die Prüfung des Endrekords vergleicht
die Entscheidungen mit dem Originaltext und verhindert, dass ein Enthaltender
in der Liste der Unterstützer auftaucht. Sie prüft die strukturierten
Originalfelder, nicht die sprachliche Bedeutung der Prosa.

Ältere Rekorde ohne diesen Vertragsmarker verwenden weiterhin ihre damalige
Zählweise. Es gibt keine automatische Migration oder rückwirkende Neuzählung.
Die Persona, Modellselbstnennungen und formal gleichen Stimmengewichte bleiben
wie vereinbart. Die Änderung ist offline geprüft; ein weiterer bezahlter
Gesamtlauf wurde nicht gestartet.

## Youth Impact: Identität und Spendenweg

Die offizielle [Spendenseite](https://www.youth-impact.org/donate) nennt
Youth Impact als Handelsnamen von Young 1ove und bietet Spendenwege für die
einzelnen Programme an. Die [ConnectEd-Seite](https://www.youth-impact.org/connected)
bestätigt die Zuordnung der telefonischen Lernförderung zur Organisation.
Geprüft am 20.09.2026.

Das Register wurde um `youth-impact` ergänzt, mit den belegten Namen
„Youth Impact“ und „Young 1ove“. Als Spendenweg dient die offizielle
Spendenseite; sie verlinkt unter anderem das ConnectEd-Formular bei
`secure.lglforms.com`. Der Abruf dieses externen Formulars war im Webwerkzeug
nicht verfügbar; die Verlinkung auf der offiziellen Spendenseite wurde geprüft.
„ConnectEd“ wurde als Programmname ausdrücklich nicht zum Organisationsalias.
Alle vorhandenen Registereinträge bleiben objektgleich.

Diese Prüfung belegt Identität, Programmzuordnung und den offiziellen
Spendenweg. Sie bestätigt keine behauptete Finanzierungslücke und keine
vergleichende Wirksamkeitsrangfolge. Die Förderbedingungen der Ratsmitglieder
bleiben bestehen.

## Prüfung und Auslieferungsstand

287 Backend-Tests bestehen, darunter Mehrheitsgrenzen, sämtliche
Enthaltungen, fehlende/widersprüchliche Statusfelder, Doppelvoten,
Registerauflösung und ein vollständiger Offline-Sitzungslauf mit Enthaltung.
Schema-Tor, Organisationsschema, Site-Build und 46 Site-Tests bestehen.
460 geschützte Dateien einschließlich aller bisherigen Sitzungs- und
Pilotartefakte bleiben bytegleich; einzig das Register erhält den beauftragten
additiven Eintrag. Zusätzliche API-Kosten: **0 Credits**.

Frontend-Einbau und Veröffentlichung folgen nach der vereinbarten
Besprechung. Dies ist keine Deployment- oder Auszahlungsfreigabe.
