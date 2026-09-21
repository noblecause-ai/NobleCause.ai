# Live-Rat-Pilot 2 — 20.09.2026

Steward-Auftrag: den vorgeschlagenen kompakteren Kontext, Reasoning nach Rolle,
16.384 Ausgabetokens für Voten und ein einzeln geprüftes Fable-Erstvotum umsetzen;
bei Erfolg mit genau dieser Antwort fortsetzen. Kosten werden nach Modell und
Rolle beobachtet. Das bestehende 10-Credit-Key-Limit wird nicht verändert.

## Umgesetzte Vorbereitung

Der Nutzerkontext umfasst 29.023 statt 108.134 Zeichen (−73,16 %). Alle zwölf
aktuellen Scout-Findings, sämtliche verworfenen Findings, Wortlaut, Unsicherheiten,
Gegenbelege, Quellen und Selbstauskünfte zu Suchanfragen bleiben erhalten.
API-Zitationshinweise und Suchzähler bleiben ausdrücklich von Selbstauskünften
getrennt; fehlende Zitationsmarker gelten nicht als Gegenbeweis zur Quelle.

Der Ratskontext enthält einen kompakten Bestandsvergleich zur Vorgängersitzung
einschließlich Stimmenzahl, konditionaler Vorbehalte und abweichender Voten.
Historische Journal-Findings und technische Rohmetadaten werden nicht an jeden
Sprecher mitgeschickt. Das vollständige ursprüngliche Dossier liegt unverändert
in `research.json`; der vollständige Archivvergleich in `history-full.md`.
Hashes und die Versionskennung `compact_evidence_v1` binden diese Auswahl an den
Prüfrekord. Der kompakte Kontext wird zusätzlich als eigene Datei gespeichert.
Es gibt keine modellgeschriebene Zusammenfassung oder inhaltliche Umdeutung.

| Rolle | Reasoning | Gesamtausgabetokens |
|---|---|---:|
| Erst- und Schlussvoten | Fable/Astra/Grok: medium; Kimi/GLM: high | 16.384 |
| Sachbeiträge | Dasselbe Modellprofil | 4.096 |
| Wortvergabe / Moderation | low | 4.096 |
| Leserfassung | Profil des Vorsitzmodells | 4.096 |

Die fünf Modell-IDs, Endpunkte und Quantisierungen bleiben unverändert. Der
Transport wartet bei einer Inferenz bis zu zehn Minuten auf die Antwort, damit
ein größeres Ausgabelimit nicht durch einen zu kurzen lokalen HTTP-Timeout
abgebrochen wird; es gibt weiterhin keinen automatischen Inferenz-Retry.

`--stop-after-first` erzeugt nach dem ersten formal gültigen Votum einen
Checkpoint, ohne das Erstvotum vorzeitig im Ereignisstrom offenzulegen.
`--resume` übernimmt anschließend die ursprüngliche Antwort samt Kostenbeleg.
Der Offline-Test belegt insgesamt 31 statt 32 Inferenzaufrufe für den vollständigen
Ablauf einschließlich dieses Checkpoints und einer zusätzlichen Absturzsimulation.

Die Kostendatei enthält nun Aufrufrolle, Reasoning-Einstellung, Eingabe-/Ausgabe-
und gemeldete Reasoning-Tokens sowie Summen je Modell und je Modell/Rolle.
Moderation und eigene Sachbeiträge des Vorsitzes werden getrennt ausgewiesen.

Arbeitsbelege: `.review/live-pilot-02-20260920/`.
Sitzungsartefakte: `.review/live-sessions/2026-09-20-pilot-02/`.
Der Pilot bleibt isoliert; Frontend, historische Rekorde und Rotation bleiben unverändert.

## Kalibrierung und geprüfte Adapterkorrektur

Fables Erstvotum war vollständig und wurde am Checkpoint geprüft: vier Säulen,
strukturierte Vorbehalte, keine abgeschnittene Antwort. 13.898 Eingabetokens
(vorher 50.919), 7.544 Ausgabetokens, davon 1.977 Reasoning; **0,51618 Credits**.
Der anschließende Lauf verwendet dieselbe Originalantwort aus dem Cache.

Astra lieferte ebenfalls ein vollständiges Vier-Säulen-Votum für
**0,2846305 Credits** (7.329 Eingabe-, 3.343 Ausgabe-, davon 710 Reasoning-Tokens).
Der erste Adapterbefund lehnte den nativen Abschluss `completed` ab; beide
API-Belege meldeten gleichzeitig den normalisierten Erfolg `stop`. Diese
belegte Azure-Variante wurde für Astra ergänzend zugelassen und im Schema
nachgezogen. 101 gezielte Adapter-/Live-Rat-Tests und danach alle 255
Backend-Tests bestanden.

Die Nachprüfung erfolgte ausschließlich lokal an den vorhandenen Originalen.
`initial-1-openai-revalidated.json` bindet den neuen Prüfbefund an SHA-256-Werte
von Anfrage, Antwort, Generationsbeleg, Endpunkt und ursprünglichem Fehlerbericht.
Alle fünf Originaldateien bleiben unverändert. Die Fortsetzung darf diese
Antwort wiederverwenden; es wurde kein zweiter Astra-Aufruf für das Erstvotum
bezahlt. Dieses Verfahren kann keine verweigerte oder abgeschnittene Antwort
in ein gültiges Votum umwandeln: der vollständige aktuelle Validator muss bestehen.

## Verzögerter Generationsbeleg

Grok lieferte ein vollständiges Erstvotum für 0,06404 Credits. Kimi antwortete
ebenfalls vollständig, jedoch gab der lesende Generationsabruf viermal HTTP 404
zurück. Der Lauf hielt mit ungeklärter Abrechnung an. Ein späterer lesender Abruf
bestätigte exakt dieselbe Generations-ID, Modellidentität, Tokens und Kosten von
0,0539637 Credits. Der frische Key-Verbrauch bestätigte diese Nachbuchung.

Die Wiederaufnahme kann diesen verspäteten Beleg jetzt als zusätzliche,
hashgebundene Rohdatei verwenden. Originalantwort, ursprüngliche 404-Belege und
Fehlerbericht bleiben unverändert. Die Nachprüfung ruft selbst kein Netzwerk auf;
sie verlangt den ursprünglichen 404, prüft den vollständigen aktuellen Validator
und bindet auch die neue Datei an ihren Hash. Ein Offline-Test prüft insbesondere
die Ablehnung einer fremden Generations-ID sowie nachträglicher Veränderungen.
Alle 102 gezielten Adapter-/Live-Rat-Tests bestanden. Die Fortsetzung löst keinen
erneuten Aufruf für eines der vier vorhandenen Erstvoten aus.

Inhaltlicher Qualitätsbefund: Kimi und GLM erklären im Votum fälschlich eine
Anthropic-Familienherkunft. Anfrage, Antwortmetadaten und Generationsbeleg weisen
Kimi/MoonshotAI beziehungsweise GLM/Z.AI aus. Diese Selbstauskunft wird nicht als technische Identität
übernommen und nicht nachträglich im Wortlaut korrigiert. Formaler Transporterfolg
ist kein Nachweis inhaltlicher Richtigkeit; der Befund gehört in die Auswertung
vor einer öffentlichen Sitzung.

GLM zeigte dieselbe Verzögerung. Die lesenden Folgeabrufe warten nun insgesamt
bis zu 120 Sekunden auf einen zunächst fehlenden Generationsbeleg; einzelne
Warteintervalle dauern höchstens 30 Sekunden. Das betrifft ausschließlich GET,
nie eine erneute Inferenz. Ein verbleibender 404 wird ausdrücklich als fehlender
Generationsbeleg gemeldet und hält den Lauf weiterhin an.

Zusätzlich meldete GLMs Completion `0.0162091908`, während der verspätete
Generationsbeleg in `total_cost` und `usage` übereinstimmend `0.01620919` ausweist.
Der tatsächliche Key-Verbrauch stieg ebenfalls um genau `0.01620919`
(`key-reconcile-2.json` → `key-reconcile-3.json`). Das ist im Pilot ein belegter
Rundungsfall. Der Adapter akzeptiert jetzt eine solche Abweichung nur, wenn beide
Generationsbeträge übereinstimmen und der Completion-Betrag dezimal auf acht
Nachkommastellen gerundet exakt diesen Wert ergibt. Es gibt keine Float-Toleranz;
schon eine Abweichung um die letzte Abrechnungsstelle wird abgelehnt. Gebucht wird
der Generationsbetrag, der Originalbetrag bleibt in den Nutzungsdaten erhalten.
Der [offizielle Generationsendpunkt](https://openrouter.ai/docs/api/api-reference/generations/get-generation)
liefert die Kosten- und Nutzungsfelder; die beobachtete Rundung ist durch die
lokalen API-/Key-Belege dokumentiert, keine behauptete allgemeine API-Garantie.

Nach diesen belegten Adapterkorrekturen bestehen alle **258 Backend-Tests**.
Die fünf Erstvoten kosten zusammen **0,93502339 Credits**. Keine Originalantwort
wurde verändert oder für die Wiederaufnahme erneut angefordert.

## Endstand: Erstvoten vollständig, Moderation abgebrochen

Alle fünf Erstvoten wurden gemeinsam offengelegt. Fable wählte anschließend
GLM für eine konkrete Rückfrage zur unterschiedlichen Schätzung bleibedingter
Todesfälle. Diese Moderationsantwort ist vollständig abgerechnet und nicht
abgeschnitten, enthält jedoch ein nicht maskiertes ASCII-Anführungszeichen
innerhalb des JSON-Fragetexts. Der JSON-Parser scheitert an Zeichenposition 128.
Damit ist die Wortvergabe strukturell ungültig. Die Originalantwort wird weder
repariert noch erneut angefordert. Der Ablauf endete vor dem ersten Sachbeitrag;
es gibt keinen Schlussbeschluss und keinen abgeschlossenen Sitzungsrekord.

| Modell | Rolle | Eingabe | Ausgabe | Reasoning | Credits |
|---|---|---:|---:|---:|---:|
| Fable 5.1 | Erstvotum | 13.898 | 7.544 | 1.977 | 0,51618 |
| Astra | Erstvotum | 7.329 | 3.343 | 710 | 0,2846305 |
| Grok 4.6 | Erstvotum | 7.765 | 8.117 | 6.153 | 0,06404 |
| Kimi K3 | Erstvotum | 8.907 | 3.220 | 698 | 0,0539637 |
| GLM-5.3 | Erstvotum | 7.885 | 3.693 | 1.718 | 0,01620919 |
| Fable 5.1 | Moderation, ungültiges JSON | 35.614 | 630 | 385 | 0,38764 |
| **Gesamt** | **6 Inferenzaufrufe** | | | | **1,32266339** |

Der tatsächliche Key-Verbrauch stieg von 5,42103507 auf 6,74369846 Credits,
exakt gleich der Summe aller sechs Generationsbelege. Im unveränderten
10-Credit-Testlimit bleiben **3,25630154 Credits**. Die Wiederaufnahmen haben
keine bezahlten Aufrufe wiederholt. `accounting-reconciled.json` belegt den
Kontenabgleich; `verification.json` die Originaldateien und Schutzgrenzen.

Die Kosten zeigen außerdem: Bei der Moderation entfielen 0,35614 Credits auf
Eingabe und 0,0315 auf Ausgabe; ein niedrigeres Reasoning allein beseitigt die
Kosten des erneut übermittelten Gesprächskontexts nicht. Diese einzelne Messung
ist keine belastbare Hochrechnung für eine vollständige Sitzung.

Nächste kleine Nachbesserung vor einem weiteren bezahlten Versuch: das
Moderationsformat durch nachgewiesen unterstützte strukturierte Ausgabe
absichern. Die vollständige Ratsdiskussion und Schlussabstimmung sind weiterhin
nur offline, noch nicht in einem abgeschlossenen Live-Lauf geprüft.

Steward-Korrektur nach dem Pilotbericht: Modellname und Familienherkunft werden
dem Modell nicht als eigene Identität vorgegeben. Falsche Selbstauskünfte bleiben
unverändert als Ergebnis im Protokoll und können bei der Beurteilung seiner
Aussagen berücksichtigt werden. Die technische Zuordnung bleibt durch die
API-Belege nachvollziehbar. Der frühere Vorschlag einer Identitätsvorgabe ist
zurückgenommen; weder alte Voten noch Stimmengewichte werden damit verändert.
Zur Diskussion steht stattdessen die ausdrücklich fiktive Rolle eines alten,
weisen Ratsmitglieds, das viele Generationen menschlicher Geschichte überblickt,
kurz und bedacht spricht und freiwillig eine an seiner Medaillonperson
orientierte Persönlichkeit wählen kann. Ihre nachfolgende Umsetzung ist
unten dokumentiert und vom abgeschlossenen Pilotversuch getrennt.

Abnahme dieses Slices: 258 Backend-Tests bestanden, Schema-Tor für 5 historische
Sitzungen und 15 Journale gültig, `git diff --check` sauber. Die 259 geschützten
Dateien bleiben bytegleich. Keine Frontend-Änderung in diesem Slice, keine
Publikation, keine Rotation, kein Commit, Push oder Deploy.

## Nachfolgende Prompt-Anpassung auf Steward-Auftrag

Nach dem Pilot wurde der gemeinsame Ratsauftrag in `gremium/prompts.py`
umgesetzt: ausdrücklicher Bezug auf das vollständige Manifest, fiktives altes
und weises Ratsmitglied, ruhige kurze Rede sowie freiwillige Orientierung an
einer dokumentierten Medaillonperson. Die frühere Wiederholung der vier Kanons
und die historischen Anthropic-Beispiele der Befangenheitsregel entfallen.
Modellname und Familienherkunft bleiben selbst abgegebene Aussagen; dafür
werden weder Lösungen vorgegeben noch automatische Stimmabschläge eingeführt.
Für die neue Fünferbesetzung ist noch keine Medaillonperson registriert;
die freiwillige Orientierung setzt entsprechende bereitgestellte Unterlagen
voraus. Es werden keine Personen erfunden oder Vorgänger automatisch übertragen.

Der Live-Rat trennt nun gemeinsamen Kontext und jeweiligen Auftrag. Erstvotum,
Wortvergabe, Sachbeitrag, Schlussvotum und Leserfassung verwenden denselben
Grundton. Das Manifest bleibt vollständig und unverändert enthalten. Spätere
Rollen bekommen nicht mehr zusätzlich den Auftrag zum unabhängigen Erstvotum;
das vollständige Votenformat steht beiden Abstimmungsphasen zur Verfügung.
Die Leserfassung erhält nun ebenfalls den gemeinsamen Kontext mit Manifest.
Der Vorsitz verwendet den gemeinsamen Rollenrahmen plus Moderationsauftrag.

Der Offline-Gesamtlauf prüft diese Zusammensetzung an allen 31 tatsächlichen
Adapteranfragen: Manifest einmal je Anfrage, gemeinsamer Systemrahmen,
Erstvotenauftrag ausschließlich bei den ersten fünf Aufrufen. Alle 258
Backend-Tests und das historische Schema-Tor bestehen. Die Änderung betrifft
künftige Läufe; sämtliche Pilotantworten und veröffentlichten Rekorde bleiben
unverändert. Für diese Anpassung erfolgte kein bezahlter Modellaufruf. Die
explizitere JSON-Anweisung ersetzt keinen Nachweis gültiger Live-Ausgaben;
der Formatfehler des Piloten bleibt als Ergebnis bestehen.
