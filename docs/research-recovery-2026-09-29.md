# Abschluss des Recherchelaufs vom 28.09.2026

Der beauftragte Regelbetrieb vom 22.09.2026 wird nach Prüfung der unveränderten
Belege wieder aufgenommen. Die erneute Störungsmeldung des Stewards am
29.09.2026 wurde ohne neue Modellaufrufe untersucht und behoben.

## Befund und Kosten

Der [bezahlte Lauf 36420475113](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/36420475113)
lieferte drei Scout-Antworten und einen Entscheid des Wochenvorsitzes Astra.
Astra gab ein gültiges JSON-Objekt ohne Markdown-Einfassung aus. Der Parser
verlangte dagegen einen Markdown-JSON-Block und brach vor dem Journalabschluss
ab. Groks Scout-Antwort enthielt nur Prosa, kein strukturiertes Dossier; dieser
separate Modellfehler bleibt als Ausfall erhalten. Sonar und Opus lieferten
verwertbare strukturierte Dossiers. Astra entschied gegen eine vorgezogene
Sitzung und berücksichtigte den fehlenden Scout ausdrücklich.

Abgerechnete Originalkosten in USD/OpenRouter-Credits:

| Aufruf | Kosten |
| --- | ---: |
| Grok Scout | 0.275670 |
| Sonar Scout | 0.035190 |
| Opus Scout | 0.428880 |
| Astra Wochenvorsitz | 0.419628 |
| Gesamt | 1.159368 |

Die Sitzungsprüfung vom 28.09. und die Rechercheprüfung vom 29.09. stoppten
an der gespeicherten Betriebssperre vor Reservierung und Modellaufrufen.
Der [kostenlose Preflight vom 29.09.](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/36561965060)
bestätigte 17.088019716 verbleibende Credits unter dem unveränderten Key-Limit
von 40. Das ist exakt der Stand vor dem Fehlerlauf minus dessen vier Rechnungen.
Es entstanden durch diese erneuten Fehlermeldungen keine weiteren Modellkosten.

## Deterministische Wiederherstellung

Der Parser akzeptiert nun ein vollständiges JSON-Objekt mit oder ohne
Markdown-Einfassung. Boolean-Entscheid und Begründung bleiben Pflicht;
freie Prosa, abgeschnittenes JSON, Listen und Zeichenketten statt Booleans
werden weiterhin abgelehnt. Auch Klammern innerhalb von JSON-Zeichenketten
werden korrekt gelesen. Prompts und Entscheidungskriterien wurden nicht geändert.

Gemäß der Wiederherstellungsregel in `docs/regelbetrieb-2026-09-22.md` und dem
Präzedenzfall der gespeicherten Antworten vom 21.09. wurde der vorhandene
Wochenrunner in einer temporären Kopie ausschließlich mit gespeicherten
Antworten ausgeführt. HTTP- und Socket-Verbindungen waren dabei gesperrt.
Alle vier erzeugten Auftragsobjekte mussten exakt den ursprünglichen
Aufträgen entsprechen. Anbieteridentität, Generation, Tokenzahlen und Kosten
wurden mit den bestehenden Validatoren erneut gegen die Originalbelege geprüft.

Alle 45 vorhandenen Rohdateien blieben bytegleich; insbesondere blieben die
ursprünglichen Dossiers, Prompts, Antworten und Abrechnungen unverändert.
Neu hinzu kamen ausschließlich der bisher fehlende Journalabschluss, der
wortgleiche extrahierte Astra-Entscheid und `journal/2026-09-28/recovery.json`.
Letztere Datei enthält Hashes aller Originale und den vorherigen Sperr-/Zeitplanstand.
Es gab keine Reparaturinferenz, keine neue Recherche und keine neue Rechnung.
Der öffentliche Eintrag nennt weiterhin zwei verwertbare Scouts und den
Grok-Ausfall; er ist kein vollständiges Drei-Scout-Dossier für eine Ratssitzung.

Erst nach erfolgreicher Offline-Prüfung wurden die zu diesem Lauf gehörende
Reservierung und Sperre abgeschlossen. Die Rotation bleibt auf Astra, die
reguläre Sitzung auf dem 21.10.2026 um 12:00 UTC. Der nächste wöchentliche
Recherchetermin ist der 05.10.2026 um 06:00 UTC. Künftige Sitzungen verlangen
weiterhin ein höchstens sieben Tage altes vollständiges Drei-Scout-Dossier.

## Separater GLM-Anschlussfehler

Der festgelegte Endpunkt `z-ai/glm-5.3` / `baidu/fp8` ist am 29.09. verfügbar
(Status 0), kostet laut öffentlicher OpenRouter-Endpunktantwort jedoch
1.40 USD pro Million Eingabetokens und 4.40 USD pro Million Ausgabetokens.
Die bisherigen Preisvorgaben waren 0.8918 / 2.8028. Die feste Preisvorgabe
wurde für denselben Anbieter und dieselbe Quantisierung auf den verifizierten
Tarif aktualisiert. Das Key-Limit von 40 Credits und die Kostenbeobachtung
bleiben bestehen; es gibt keine automatische Erhöhung weiterer Preisgrenzen
und keinen Anbieterwechsel.

## Abnahme

333 Backend-Tests und 60 Website-Tests bestanden. Der Produktionsbuild und
das Schema-Tor für sechs Sitzungen und 18 Journal-Einträge sind erfolgreich.
Die neuen Regressionen verwenden auch die echten gespeicherten Antworten:
Astra wird unverändert akzeptiert, Groks Prosa bleibt ungültig. Der Offline-
Wiederaufbau bestätigte zusätzlich die Auftragsgleichheit aller vier Aufrufe,
die Originalkosten und sämtliche Originalhashes. Die Wiederaufnahme wird
anschließend über die kostenlosen Produktionschecks geprüft.
