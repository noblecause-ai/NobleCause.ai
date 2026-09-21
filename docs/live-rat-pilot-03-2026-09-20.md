# Live-Rat-Pilot 3 — strukturierte Wortvergabe

**Nachtrag:** Die beiden unten dokumentierten Befunde sind inzwischen
[im Backend geklärt](live-rat-votumsklaerung-2026-09-20.md). Eine gesonderte
Korrekturauswertung hält die geklärte Zählung fest; der Pilotrekord bleibt
unverändert. Die folgende Darstellung dokumentiert den ursprünglichen Lauf.

Steward-Auftrag: Moderationsformat absichern, anschließend den vollständigen
Backend-Lauf starten; falls das Testlimit voraussichtlich nicht reicht, die
Erweiterung vor dem bezahlten Start vorlegen.

## Ergebnis: vollständig durchgeführt, zwei offene Punkte vor Veröffentlichung

Der bezahlte Backend-Pilot `2026-09-20-pilot-03` ist abgeschlossen:
**31 eindeutige Modellaufrufe**, fünf unabhängig entstandene Erstvoten, zehn
strukturierte Wortvergaben, zwei Sachbeiträge je Mitglied, fünf unabhängig
abgegebene Schlussvoten und eine Leserfassung. Alle adressierten Einwände
wurden in den Schlussvoten einzeln beantwortet. Sämtliche Moderationen
erfüllten das neue Schema. Nach drei dokumentierten Unterbrechungen wurden
vorhandene Antworten unverändert wiederverwendet; keine Inferenz wurde wiederholt.

Die bestätigten Generationsbelege summieren sich auf **7,241845541 Credits**.
Der abschließende Key-Abgleich bestätigt exakt denselben Mehrverbrauch:
von 6,74369846 auf **13,985544001 Credits**. Innerhalb des unveränderten
20-Credit-Limits bleiben damit **6,014455999 Credits**. Die zuerst abgefragte
Anzeige enthielt die 0,4533 Credits der Leserfassung noch nicht; der finale
lesende Abgleich enthält sie vollständig. Die Freigabe reichte aus.
Pro Modell und Aufgabe:

| Modell | Erstvotum, Beiträge, Schlussvotum | Wortvergabe | Leserfassung | Gesamt |
|---|---:|---:|---:|---:|
| Fable 5.1 | 1,769160 | 3,401890 | 0,453300 | 5,624350 |
| GPT-6 Astra | 1,114033 | – | – | 1,114033 |
| Grok 4.6 | 0,223602 | – | – | 0,223602 |
| Kimi K3 | 0,202742 | – | – | 0,202742 |
| GLM-5.3 | 0,077119 | – | – | 0,077119 |

Tabellenwerte sind auf sechs Nachkommastellen gerundet; die vollständigen
Beträge stehen im Kostenbeleg. Fables höherer Gesamtbetrag umfasst die
zusätzlichen Vorsitzaufgaben. Allein die zehn Wortvergaben kosten rund 47 %
des Laufs; sie verarbeiten zusammen 324.359 Eingabetokens. Ein reiner
Modellkostenvergleich ohne diese Aufgabentrennung wäre irreführend.

**Noch keine Freigabe für den öffentlichen Regelbetrieb:**

1. In Säule C zählt der bestehende Aggregator fünf bedingte NTI-Stimmen,
   obwohl Astra ausdrücklich eine Enthaltung erklärt. Dafür fehlt ein
   maschinenlesbarer Abstimmungsstatus im Votumsvertrag. Die Rohtexte tragen
   vier bedingte Empfehlungen und eine erklärte Enthaltung; der fehlerhafte
   maschinelle Befund wird im Pilotrekord unverändert erhalten und hier benannt.
2. Alle fünf Schlussvoten nennen in Säule A Youth Impact. Die Organisation
   fehlt im Register, daher bleiben diese fünf Nennungen ausdrücklich
   `unresolved` und werden nicht gezählt. Die Registerprüfung funktioniert
   damit wie vorgesehen; nötig ist ein belegter additiver Organisationseintrag
   mit geprüftem offiziellen Spendenweg. Es erfolgt keine freie Namensauflösung.

Die Leserfassung nennt beide Widersprüche ausdrücklich. Sie ist dennoch ein
Modelltext und keine korrigierte Auszählung. Empfehlungen, angebliche Belege,
Förderbedingungen und selbst vergebene Prüfaufträge dieses Piloten sind
keine extern verifizierten Tatsachen oder automatisch ausgeführten Aufträge.

**Abschlussprüfung:** 269 Backend-Tests, Schema-Tor und `git diff --check`
bestanden. Der komplette Manifesttext und der gemeinsame Rollenauftrag sind
in allen 31 Anfragen nachgewiesen. Ereigniskette, Sprecherquoten,
Generations-IDs, Kostenbelege und der bytegleiche Wortlaut von Feed und
Endrekord sind geprüft. 259 geschützte Dateien und 76 Dateien früherer Piloten
sind unverändert. Keine Veröffentlichung, keine Rotation, kein Commit oder
Deploy; der Frontend-Einbau bleibt Gegenstand der gesonderten Besprechung.

Lokale Ergebnisse:

- `.review/live-sessions/2026-09-20-pilot-03/session.json`: unveränderter Endrekord.
- `.review/live-pilot-03-20260920/originalprotokoll.md`: lesbare Originalbeiträge.
- `.review/live-pilot-03-20260920/verification.json`: formale Abschlussprüfung.
- `.review/live-pilot-03-20260920/accounting-reconciled.json`: exakter Kontoabgleich.
- `.review/live-sessions/2026-09-20-pilot-03/costs-live.json`: Einzelkosten und Rollenaufteilung.

## Beobachtungen zur Beratung und Rollenwirkung

Es fand tatsächliche Bezugnahme mit Positionsänderungen statt: GLM zog
Vitamin A aus Säule A zurück, Astra seinen behaupteten Pratham-Vorrang,
Kimi die zunächst unbedingte Youth-Impact-Empfehlung. Die fünf Schlussvoten
tragen bedingte Youth-Impact-Empfehlungen; Astras C-Enthaltung bleibt als
inhaltlicher Dissens erhalten. Diese Konvergenz beweist keine höhere
fachliche Richtigkeit der Empfehlungen.

Grok nannte sich zunächst als GPT und korrigierte sich im Gespräch; Kimi
nannte zunächst Claude/Anthropic und korrigierte sich nach Fables Einwand
auf Kimi/Moonshot AI. Beide kennzeichnen die spätere Selbstauskunft als
unsicher. GLMs Selbstadressierung ist separat markiert. Aufforderungen der
Modelle, frühere falsche Angaben zu streichen, wurden nicht ausgeführt:
Ursprung und spätere Korrektur bleiben nebeneinander sichtbar. Die
API-Zuordnung der Sitze und die Stimmengewichte bleiben unverändert.

Die fiktive alte Ratsrolle zeigt sich in Sprache und Metaphern. Die
Korrekturen nach gegenseitigen Hinweisen sind beobachtbar, aber weder ein
Nachweis verlässlicher Selbsterkenntnis noch ein isolierter Qualitätsgewinn
durch die Persona. Dafür fehlt ein vergleichbarer Kontrolllauf.

## Vorbereitung abgeschlossen

Die Moderation nutzt `response_format: json_schema` mit `strict: true`.
Das Schema enthält genau `next_model_id` und `question`; die Modell-ID ist auf
die im jeweiligen Schritt zulässigen Redner begrenzt. Zusätzliche Felder sind
ausgeschlossen. Der Vorsitz liefert ein reines JSON-Objekt, keinen Markdown-Zaun.
Das betrifft nur die Wortvergabe; die freien Sachbeiträge und Voten bleiben
wortgetreu erhalten.

Vor dem ersten Votum und vor jeder Moderation wird geprüft, ob der festgelegte
Endpunkt `structured_outputs` und `response_format` unterstützt. Anbieterbindung,
`require_parameters: true` und ausgeschaltete Ersatzrouten bleiben bestehen.
Der lesende Vorabcheck bestätigt die Unterstützung des Fable-Endpunkts.
Grundlage: [OpenRouter: Structured Outputs](https://openrouter.ai/docs/guides/features/structured-outputs).

Jede Antwort wird zusätzlich lokal gegen genau das angeforderte Schema geprüft.
Ein Anbieter, der es nicht einhält, verursacht weiterhin einen sichtbaren Stopp;
die Originalantwort und bestätigte Kosten bleiben erhalten. Es gibt weder
JSON-Heilung noch erneute Inferenz. Acht neue Offline-Fälle prüfen maskierte
Anführungszeichen, fehlende Endpunktfähigkeiten, ungültiges JSON, fremde Redner,
fehlende beziehungsweise zusätzliche Felder und unerlaubte Markdown-Verpackung.
Der Gesamtlauf einschließlich Wiederaufnahme prüft alle zehn Schema-Anfragen.
**266 Backend-Tests bestehen.**

Der Lauf verwendet die zuletzt vereinbarten gemeinsamen Rollenprompts und das
unveränderte Manifest. Promptvertrag und Moderationsschema werden im Laufauftrag
festgehalten. Die fünf Erstvoten entstehen neu, weil der Rollenauftrag gegenüber
Pilot 2 geändert wurde. Das vorhandene aktuelle Scout-Dossier kann unverändert
weiterverwendet werden. Fable beginnt als Vorsitz; insgesamt sind 31 Aufrufe
vorgesehen. Die 10-Credit-Einstellung ist bisher unverändert.

## Budget vor dem Start

Der frische lesende Key-Abgleich bestätigt 10 Credits Limit, 6,74369846 Credits
Verbrauch und **3,25630154 Credits Rest**, ohne periodische Rücksetzung.

Als einfache Referenzrechnung, ausdrücklich keine Preisgarantie: Die fünf
Erstvoten des Vorgängerlaufs kosteten 0,93502339 Credits. Zehn Moderationen zum
gemessenen ersten Moderationspreis von 0,38764 würden weitere 3,8764 Credits
kosten. Diese beiden Posten allein ergäben **4,81142339 Credits**; Sachbeiträge,
Schlussvoten und Leserfassung fehlen darin noch. Der geänderte Kontext und
unterschiedliche Antwortlängen können die tatsächlichen Beträge ändern.

Vorschlag zur Freigabe: **Key-Limit von 10 auf insgesamt 20 Credits erhöhen**.
Das sind zusätzliche 10 Credits und damit 13,25630154 verfügbare Credits für
den neuen Lauf. Dies ist eine Planungsreserve; die Kosten bleiben beobachtet
und pro Modell/Rolle dokumentiert. Der vorbereitete Start prüft den ausdrücklich
freigegebenen Limitwert gegen die API. Vor der Bestätigung und tatsächlichen
Limitanpassung wird keine neue bezahlte Inferenz gestartet.

Vorbereitete Dateien: `.review/live-pilot-03-20260920/`. Neue Sitzungsartefakte
entstehen erst beim Start unter `.review/live-sessions/2026-09-20-pilot-03/`.
Frontend, publizierte Rekorde und Rotation bleiben unverändert.

## Budget freigegeben und Lauf gestartet

Der Steward bestätigt: „ist auf 20 erhöht, laut anzeige bisher 6.55 verbraucht.“
Der anschließende lesende API-Abgleich bestätigt das nicht zurückgesetzte
Key-Limit von **20 Credits**, meldet **6,74369846 Credits Verbrauch** und rund
**13,25630154 Credits Rest**. Die Ursache der Abweichung zur genannten
Oberflächenanzeige ist ungeklärt; für den Lauf zählt der gespeicherte
API-Startstand mit den einzelnen Generationsbelegen.

`2026-09-20-pilot-03` wurde mit diesem freigegebenen Budget als vollständiger
Backend-Lauf gestartet. Die Scouts werden nicht erneut aufgerufen. Die fünf
Erstvoten verwenden erstmals den neuen Rollenauftrag; anschließend folgen
Wortvergabe, Beratung und Schlussvoten. Keine Veröffentlichung oder Rotation.

## Belegte Abrechnungsanpassung während des Piloten

Die fünf Erstvoten sind vollständig. Beim GLM-Votum stoppte zunächst der
Abrechnungsvergleich: Completion `0.0165124872`, Generationsfelder `usage` und
`total_cost` beide `0.016512487`. Der neue Beleg verwendet neun Nachkommastellen,
während der entsprechende Fall in Pilot 2 acht Stellen hatte. Der Adapter
respektiert nun die feinere Präzision des Generationsbetrags und rundet niemals
gröber als acht Stellen. Die originale Completion-Kostenangabe bleibt erhalten;
gebucht wird ausschließlich der bestätigte Generationsbetrag.

267 Backend-Tests bestehen einschließlich beider tatsächlich beobachteter
Präzisionen und Ablehnung einer Abweichung an der letzten Abrechnungsstelle.
Die vorhandene GLM-Antwort wurde offline nachgeprüft; der zusätzliche
Prüfbeleg bindet alle fünf Originaldateien an ihre Hashwerte. Die Fortsetzung
verwendet sämtliche Erstvoten ohne erneute Inferenz. Ihre Gesamtkosten betragen
**0,681465137 Credits**.

## Selbstzuordnung als beobachtetes Ergebnis

Die erste strukturierte Wortvergabe gelang für 0,30976 Credits. Fable rief GLM
auf. Dessen Antwort war vollständig, formal lesbar und mit 162 Wörtern innerhalb
des Kontingents. GLM sprach jedoch, als gehöre es zu einer anderen Position, und
adressierte seinen Einwand ausdrücklich an `z-ai/glm-5.3`, also an den eigenen
API-Sitz. Die bisherige Prüfung fremder Adressaten hielt daran den Lauf an.

Die bereits ausdrückliche Steward-Vorgabe lautet, falsche Selbstnennungen als
Ergebnis zu protokollieren. Entsprechend bleibt eine Selbstadressierung nun mit
`identity_observation: self_addressed_contribution` sichtbar. Originaltext,
wörtlich genannter Adressat und tatsächlicher API-Sprecher bleiben unverändert.
Es wird kein anderer Sprecher geraten und keine Stimme oder Redequote verändert.
Auch dieser Einwand bleibt im Schlussvotum des wörtlich adressierten Sitzes zu
beantworten. Unbekannte Sitz-IDs, ungültige Ereignisverweise und andere
Formatverletzungen bleiben Fehler. Dies ändert keine Wortvergabe oder Zählregel.

Die bereits bezahlte Antwort wird ohne neue Inferenz übernommen. Kosten:
0,015583352 Credits. Das ursprüngliche Abbruchereignis bleibt erhalten.

## Weitere belegte Dezimaldarstellung

Beim zweiten GLM-Beitrag weichen Completion (`0.0167890536`) und
Generationsabrechnung (`usage` und `total_cost` jeweils `0.016789053`)
erneut ausschließlich in der Dezimaldarstellung ab. Hier liegt eine Kürzung
statt der zuvor beobachteten Rundung vor. Der Vergleich erlaubt nun beide
Darstellungen auf der belegten Genauigkeit des Generationsbetrags, weiterhin
niemals gröber als acht Nachkommastellen. Beide Abrechnungsfelder müssen
übereinstimmen; der Originalbetrag bleibt erhalten. Eine Abweichung außerhalb
dieser beiden exakten Dezimaldarstellungen bleibt ein Fehler.

**269 Backend-Tests bestehen.** Der zusätzliche Hashbeleg wurde offline
erstellt; auch dieser Beitrag wird ohne erneute Inferenz wiederverwendet.
Die bisherigen Unterbrechungen und Originaldateien bleiben erhalten.

## Befund vor einem öffentlichen Regelbetrieb: Enthaltung

Astras Schlussvotum erklärt für Säule C ausdrücklich: „sie darf nicht als
bedingte Zustimmung gezählt werden.“ Im strukturierten Teil nennt es dennoch
NTI mit `conditional: true`; die Enthaltung steht in Titel und `reservation`.
Der derzeitige Votumsvertrag verlangt für jede Säule eine Organisation und
enthält keinen strukturierten Abstimmungsstatus für Enthaltungen. Der
Aggregator wertet ausschließlich die registrierte Organisation und das
Boolean aus. Damit würde diese erklärte Enthaltung als Zustimmung zählen.

Dies ist eine Lücke zwischen Befangenheitsauftrag, Votumsformat und Zählung,
nicht lediglich eine falsche Modellselbstauskunft. Weder Originalvotum noch
Auszählung werden während des Piloten still umgedeutet. Vor dem öffentlichen
Regelbetrieb braucht es einen ausdrücklichen maschinenlesbaren Status je
Säule für Empfehlung oder Enthaltung, mit unverändertem Nenner fünf und
Mehrheit ab drei Stimmen. Alte Rekorde bleiben unberührt. Der Pilot dient
hier als konkreter Fehlerbeleg, nicht als Veröffentlichungsfreigabe.

Beleg: `raw/final-1-openai-response.json` im Sitzungsverzeichnis;
aktueller Vertrag: `gremium/prompts.py::VOTE_FORMAT`;
Zählung: `gremium/run_session.py::aggregate_recommendations`.
