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
