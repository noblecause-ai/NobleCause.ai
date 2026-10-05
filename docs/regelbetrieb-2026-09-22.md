# Autonomer Regelbetrieb ab 22. September 2026

Steward-Auftrag: „bitte den regelbetrieb herstellen, dass muss jetzt autonom
laufen bis zur nächsten update“. Dies bestätigt den bisher offenen Übergang
der Wochenrolle an den jeweils nächsten Ratsvorsitz (Wart-Abnahme C3), den
automatischen Start fälliger öffentlicher Sitzungen und deren Veröffentlichung.
Erster nächster Vorsitz: Astra. Die weitere Reihenfolge bleibt unverändert.

## Ablauf und Mandat

Die vorhandenen GitHub-Actions-Workflows bleiben der einzige Scheduler.
`wart.yml` kontrolliert täglich um 06:00 UTC die Research-Fälligkeit; bezahlt
wird nur, wenn `schedule.json.next_research` erreicht ist, regulär montags.
Drei Scouts recherchieren unabhängig und blind. Erst danach erhält der nächste
Vorsitz den historischen Vergleich und entscheidet über eine frühere Sitzung.
Ein solcher Entscheid dreht die Vorsitzrotation nicht weiter.

`session.yml` prüft täglich um 12:00 UTC die Sitzungsfälligkeit. Die bislang
bloße Erinnerung wird durch den wirklichen öffentlichen Live-Lauf ersetzt.
Die gemeinsame, vom Steward bereits verwendete Frage ist in
`gremium/config.json:regular_operation` ausdrücklich als wiederkehrender Auftrag
festgehalten; kein Modell und kein Scheduler erfindet eine neue Fragestellung.
`next-session.json` bleibt manuelle Vorbereitung und wird nicht gelesen.

Eine Sitzung verwendet das jüngste vollständige blinde Drei-Scout-Dossier mit
Datum und Hash, höchstens sieben Tage alt. Die bezahlten Scout-Originale werden
unverändert mitarchiviert. Nach geprüftem Abschluss: einmalige Rotation,
Fortschreibung um 30 Tage, Commit, bestehender Website-Deploy. Eine frühere
Einberufung kann diesen Termin vorziehen. Keine künstliche Zusatzsitzung bei
Aktivierung des Regelbetriebs. Der aktuelle Plan ist Research am 28.09.2026,
reguläre Sitzung am 21.10.2026.

## Budget und Redetoleranz

Kostenbeobachtung bleibt der ausdrücklich gewünschte Betriebsmodus. Es gibt
keinen neu erfundenen Token-Bound und keine garantierte Abschlussreserve. Der
verbleibende Betrag unter dem bestehenden, nicht zurückgesetzten OpenRouter-
Key-Limit wird vor dem Lauf gelesen; abgerechnete Kosten werden vor Folgeaufrufen
berücksichtigt. Das Limit von 40 Credits wird nicht erhöht. Unter zehn Credits
meldet die kostenlose tägliche Prüfung einen deduplizierten Budgethinweis.
Ohne verfügbares Budget starten keine weiteren Modellaufrufe.

Die vom Wart bereits geprüfte Regel für 181–200 Wörter wird mit dem vorliegenden
Auftrag zum Regelbetrieb als Nachtrag `0.6-speech-limit-2` aktiviert. Der Prompt
verlangt weiterhin 180 Wörter; bis einschließlich 200 bleiben vollständige,
strukturell gültige und abgerechnete Beiträge unverändert im Rekord, mit
Wortzahl, Überschuss und Nachtraghash. Mehr als 200 Wörter bleiben ein Fehler.
Alle fünf Mitglieder haben dieselbe Toleranz und weiterhin zwei Redeplätze.
Die Regel wird je neuer Sitzung in `speech-policy.json`, dem Laufauftrag und
dem öffentlichen Start-Ereignis ausgewiesen. Die Einzelregel der Sitzung vom
21.09.2026 und alle alten Texte, Bilder und Rohantworten bleiben unverändert.

## Anschluss, Reservierung und Fehler

Ein gemeinsamer wiederverwendbarer Workflow hält die bestehende
`gremium-records`-Sperre vom Checkout bis zum abschließenden Push. Vor der ersten
Zahlung wird eine Laufreservierung in `schedule.json` committet und gepusht.
Nur genau derselbe GitHub-Laufversuch darf sie ausführen. Auch bei Runner-Ausfall,
Abbruch oder verlorenem Abschluss-Push bleibt so sichtbar, dass ein bezahlter
Lauf begonnen haben kann. Ein späterer Trigger bezahlt ihn nicht erneut.

Aufruf, Buchungsbelege, Beitragsprüfung und SSH-Publisher bleiben die bestehenden
Adapter. Vor jeder Sitzung wird der kleine Publisher aus demselben Checkout
auf dem bestehenden VPS bereitgestellt und geprüft. Vor jeder neuen Inferenz
muss der Server den veröffentlichten Ereignishash bestätigen. Website-Deploys
lassen `/live/` weiterhin unberührt. Der OpenRouter-Key gehört ausschließlich
als verschlüsseltes Secret in das bestehende GitHub-Repository, nicht auf den
VPS oder in Git. Nach Erläuterung der Zugriffsmöglichkeiten hat der Steward am
22.09.2026 ausdrücklich die Übertragung dieses Keys als verschlüsseltes
`OPENROUTER_API_KEY`-Secret an `noblecause-ai/NobleCause.ai` und die Aktivierung
bestätigt („dann hast du mein erlaubnist“). Das Secret wurde über die GitHub-CLI
ohne Ausgabe oder Speicherung des Wertes in Git hinterlegt. Die zuvor von der
automatischen Freigabeprüfung geforderte konkrete Zustimmung liegt damit vor.

Anschlussfehler vor der Laufreservierung sind kostenlos erneut prüfbar.
Ungeklärte bezahlte Läufe setzen eine dauerhafte Betriebssperre und einen
GitHub-Betriebsalarm. Schema-gültige Teilrekorde und Rohbelege werden gesichert;
zusätzlich gibt es Wiederherstellungsartefakte mit 90 Tagen Aufbewahrung. Ein
Schemafehler verhindert weiterhin den Commit des fehlerhaften Rekords.
Bei Wiederherstellung zuerst die unveränderten Rohbelege und Serverereignisse
prüfen, dann bestätigte Antworten explizit wiederverwenden. Keine automatische
Reparaturinferenz, keine Ersatzmodelle, kein stiller Reset einer Sperre.

`workflow_dispatch` startet standardmäßig nur die kostenlose Anschluss- und
Fälligkeitsprüfung (`check_only`). Der normale Scheduler arbeitet scharf.
Die neue Wochenrolle erhält das gemeinsame Ratsprofil, das vollständige
Manifest und unveränderte Einberufungskriterien. Boolescher Entscheid bleibt
strikt, Verweigerungen werden veröffentlicht, technische Vertragsbrüche nicht
zu einem Urteil umgedeutet.

## Prüfung vor Aktivierung

325 Backend-Tests und 60 Website-Tests bestanden; Produktionsbuild, Schema-Tor
(sechs Sitzungen und 17 Journal-Einträge), actionlint 1.7.12 und Diff-Prüfung sind
grün. Neue Regressionen prüfen Fälligkeit, Nachholen eines verspäteten Triggers,
Altersgrenze des Dossiers, beständige Sitzungs-IDs, Laufreservierung über
Runner-Abbrüche hinweg, unbekannte Schedule-Felder, die strikte Wochenentscheidung
im Kostenbeobachtungsmodus und den unveränderten Wortlaut mit versionierter
Redetoleranz. Veröffentlichte Rekorde, Registratur und bisheriger Zeitplan sind
unverändert.

Der kostenlose reale Wochen-Check mit Astra und allen drei Scouts sowie der
SSH-Publisher-Check bestanden. Beim Anschlusscheck am 22.09.2026 meldete der
festgelegte GLM-Endpunkt `baidu/fp8` Status -5 statt betriebsbereit (0). Das wird
sichtbar gemeldet und bei den nächsten kostenlosen Checks erneut geprüft; keine
Ersatzroute wurde eingestellt. Verfügbares Key-Budget weiterhin 18,247387716
Credits. Für diese Inbetriebnahme entstand keine Inferenzrechnung.

## Aktivierung abgeschlossen

Die Freigabe und der Regelbetrieb wurden mit Commit
`74629519de0cdc67fd9dd02d91f6d37d3573dcec` per Fast-forward auf `master`
ausgeliefert. Der [Produktions-Deploy](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/35776195348)
und alle drei kostenlosen GitHub-Prüfungen waren erfolgreich:
[Wochenlauf mit Astra und drei Scouts](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/35776257979),
[Sitzungsanschluss samt SSH-Publisher](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/35776261184),
[täglicher Preflight und Budget](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/35776264448).

Der GLM-Endpunkt war bei dieser abschließenden Prüfung wieder verfügbar; der
bestehende Preflight-Alarm wurde automatisch geschlossen. Keine Ersatzroute war
nötig. Beide Zeitplan-Workflows sind aktiv; die Checks bestätigen den nächsten
Research am 28.09.2026 und die reguläre Sitzung am 21.10.2026. Der bestehende
Sitzungsfeed wurde nach dem Deploy bytegleich über HTTPS verifiziert, der
Zeitplan inhaltlich unverändert. Es wurde keine zusätzliche Sitzung gestartet.

## Tarifprüfung am 02.10.2026

Die kostenlosen Preflights am 01. und 02.10. meldeten beim festgelegten Kimi-
Endpunkt `moonshotai/kimi-k3` / `inference-net/fp4` eine Preisabweichung. Der
öffentlich abgefragte Endpunkt war verfügbar (Status 0, InferenceNet, FP4),
kostete aber 13 statt der hinterlegten maximalen 10.95 USD pro Million
Ausgabetokens (+18.72 %). Eingabetokens kosteten 1.39 USD pro Million und lagen
damit unter der bestehenden Grenze von 2.10. Die Ausgabe-Preisgrenze wurde auf
den verifizierten Tarif 13 aktualisiert; Modell, Anbieter, Quantisierung und
Gesamtlimit von 40 Credits bleiben bestehen. Weitere Tarifänderungen werden
weiterhin vor einem Modellaufruf geprüft und nicht automatisch übernommen.

Der [Preflight vom 02.10.](https://github.com/noblecause-ai/NobleCause.ai/actions/runs/36999853144)
bestätigte weiterhin 17.088019716 verfügbare Credits. Seit dem Recherchelauf vom
28.09. gab es keine zusätzlichen Modellkosten. Die Fälligkeitsprüfungen für
Recherche und Ratssitzung waren erfolgreich; der nächste Research bleibt am
05.10., die reguläre Sitzung am 21.10.2026. Der am 29.09. reparierte JSON-Parser
war an dieser neuen Meldung nicht beteiligt.

Preisfehler nennen nun Tokenart, tatsächlichen Tarif und hinterlegte Grenze
direkt im Protokoll. Neue Preflight-Alarme beschreiben die kostenlose
Anschlussprüfung und behaupten nicht mehr pauschal einen Key- oder
Erreichbarkeitsfehler. Die Tarifprüfung wird mit aufgezeichneten Preiswerten
ohne HTTP-Inferenz getestet; der Produktionscheck erfolgt ebenfalls kostenlos.

## Stiller Anschlussstatus ab 05.10.2026

Der Steward hat die wiederkehrenden Failure-E-Mails der täglichen Preflights
ausdrücklich abgelehnt. Auslöser am 05.10. war erneut der Kimi-Ausgabetarif:
14 statt 13 USD pro Million Tokens am unveränderten Endpunkt `inference-net/fp4`.
Der Anbieter war verfügbar; der aktuelle Eingabetarif betrug 0.67 USD pro
Million Tokens. Die frühere Änderung der Tarifgrenze hatte die Ursache der
wiederkehrenden E-Mails nicht behoben: Ein diagnostischer Tagescheck wurde als
fehlgeschlagener Ausführungsjob behandelt und erzeugte zusätzlich ein Issue.

Die weiterhin kostenlose tägliche Anschlussabfrage ist jetzt ein stiller
Statusbericht. `preflight.yml` hat ausschließlich Leserechte und erzeugt weder
Issues noch Kommentare. Job und Prüf-Schritt verwenden `continue-on-error`:
[GitHub dokumentiert](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idcontinue-on-error),
dass ein solcher Job den Workflow nicht fehlschlagen lässt. Der ursprüngliche
Prüfstatus aus `steps.preflight.outcome` wird ausdrücklich erhalten, nicht durch
die tolerierte Schritt-Conclusion ersetzt. Die Zusammenfassung und das
30 Tage aufbewahrte Artefakt unterscheiden `ready`, `not_ready` und
`not_checked`; fehlende oder gescheiterte Prüfungen sind niemals bereit.
Der Workflow-Abschluss bestätigt nur die Verarbeitung des Statusberichts.

Die Ausführungsprüfungen in `regular-operation.yml` und den Modelladaptern
bleiben strikt. Ohne passende Endpunkte, Preise und verfügbares Budget wird
keine Zahlung gestartet. Die dauerhafte Sperre nach unvollständigen bezahlten
Läufen bleibt erhalten. Eine Budgetwarnung unter zehn Credits wird nun bei
der Anschlussprüfung des eigentlichen Regelbetriebs einmalig gemeldet,
anstatt vom stillen Tagesmonitor. Echte Betriebsfehler werden weiter gemeldet.
Das Key-Limit beträgt unverändert 40 Credits.

Der Recherchelauf vom 05.10. wurde unabhängig von dieser Meldung abgeschlossen
und veröffentlicht: 1.122581 Credits für drei Scout-Aufrufe und Astra. Groks
erneut fehlendes strukturiertes Dossier ist als Ausfall dokumentiert, Sonar und
Opus lieferten verwertbare Dossiers. Es ist weiterhin kein vollständiges
Drei-Scout-Dossier für eine Ratssitzung. Der nächste Research ist am 12.10., die
reguläre Sitzung am 21.10.2026 vorgesehen. Für die Monitoränderung werden keine
bezahlten Aufrufe wiederholt.
