# Council: Live-Gespräch über der Maschine

Stand: 21. September 2026. Der Steward hat die Chatvariante nach dem interaktiven
Mockup zum Einbau freigegeben. Der Einbau ändert weder Prompts noch Voten oder
historische Rekorde. Veröffentlichung und ein neuer bezahlter Lauf sind getrennte
Schritte. Die Wochenrolle C3 wird durch diesen UI-Auftrag nicht aktiviert.

## Darstellung

Im bestehenden Council-Raum öffnet sich ein gerahmtes Gesprächsfenster über der
Zählmaschine. Fünf Medaillons wandern aus ihrer Umlaufbahn an den oberen Rand.
„Saal ansehen“ klappt das Fenster ein; die Medaillons kehren zur Maschine zurück.
Auf kleinen Bildschirmen bleibt der Rahmen innerhalb der Bildschirmbreite; die
Seite kann vertikal scrollen. `prefers-reduced-motion` schaltet die Bewegung aus.

Neue abgeschlossene Beiträge erscheinen unten im gemeinsamen Chat. Solange der
Leser am Ende ist, folgt der Verlauf. Beim Nachlesen bleibt seine Position stehen;
„Zum neuesten Beitrag“ aktiviert das Folgen wieder. Ein Medaillon führt zum
letzten veröffentlichten Beitrag seines Mitglieds. Der aktive Sitz leuchtet;
laufende Erzeugung heißt „denkt nach“, neu eingegangene Beiträge leuchten kurz.

Vorsitzfragen, Sachbeiträge und Leserfassung tragen ihre tatsächliche Rolle.
Erst- und Schlussvoten erscheinen jeweils erst nach der gemeinsamen Offenlegung
aller fünf Antworten in aufklappbaren Gruppen. Das Frontend zählt keine Stimmen.
Der ältere, übernommene Ergebnisstand bleibt unterhalb des Gesprächs mit seiner
eigenen Sitzungsnummer sichtbar.
Die bisherige Prozessröhre bleibt während eines verfügbaren Gesprächs verborgen,
da sie noch den historischen Ablauf und die frühere Ratsbesetzung beschreibt.

Die sichtbare Prosa bleibt im Original. JSON-Steuerdaten und der gesamte
Originalwortlaut sind unter „Original und Herkunft“ zugänglich. Der gemeinsame
Markdown-Renderer aus `site/src/lib/markdown.js` neutralisiert Roh-HTML und
gefährliche Link-Schemata auch bei zur Laufzeit eintreffenden Beiträgen. Die
englische Ansicht übersetzt die Bedienung, nicht die Modellantworten.

Die im Mockup akzeptierten Vorgängersymbole von Opus 5 und GPT-5.6 bleiben vorerst
für Fable 5.1 und Astra sichtbar; `medallion_source_model` und die Herkunftsanzeige
legen das offen. Grok, Kimi und GLM tragen neutrale Buchstabensiegel. Es wurde kein
neues Bildnis bestellt und die additive Modellregistratur nicht umgeschrieben.

## Schlanker Dateivertrag

`gremium/publish_live.py` stellt einen `FilePublisher` und eine reine Offline-
Wiedergabe bereit. Das ausdrücklich gewählte Zielverzeichnis wird unter `/live/`
vom vorhandenen statischen Webserver ausgeliefert:

- `current.json`: aktueller vollständiger Snapshot mit öffentlicher Sitzungs-
  beschreibung, Originalereignissen, bestätigt bekannten Kosten und Lebenszeichen.
- `sessions/<id>/snapshot.json`: letzter Stand derselben Sitzung; bleibt erhalten.
- `sessions/<id>/events.json`: vollständiger Originalereignisrekord, bytegleich zur
  kanonischen lokalen Ereignisdatei beim selben Ereignisstand.

Jeder Schreibvorgang prüft Schema, lückenlose Nummerierung, Hashkette und den
bereits veröffentlichten Präfix. Er schreibt zuerst das Archiv und zuletzt den
aktuellen Zeiger; einzelne Dateien werden atomar ersetzt. Frühere Ereignisse
werden nie gekürzt oder umgeschrieben. Ein späterer Site-Deploy schließt `/live/`
explizit vom rsync aus und berührt den Verlauf daher nicht.

Der Browser fragt ohne Cache alle drei Sekunden ab (im Hintergrund alle 15).
Er prüft Nummerierung, Sitzidentität, den bereits gesehenen Präfix und SHA-256
des Originalwortlauts. Die vollständige Ereignis-Hashprüfung bleibt im Backend;
Python und JavaScript kodieren Zahlen nicht in jedem Fall identisch. Bei einer
Lücke, widersprüchlichen Daten oder HTTP-Fehlern bleibt der letzte gültige Stand
sichtbar. Eine neue Sitzungs-ID wird ausdrücklich zum Öffnen angeboten, statt
einen gerade gelesenen Verlauf zu ersetzen.

Während eines angeschlossenen Laufs erneuert der Publisher sein Lebenszeichen
alle 15 Sekunden. Nach 75 Sekunden ohne Lebenszeichen zeigt die Site einen
unterbrochenen Feed statt eines unbegrenzt nachdenkenden Modells. Ein Schreib-
fehler wird festgehalten und stoppt vor dem nächsten bezahlten Modellaufruf.
Der lokale Abbruch bleibt auch dann erhalten, wenn das öffentliche Ziel bereits
nicht mehr erreichbar ist. Wiederaufnahme erfordert wie bisher `--resume`.

## Lokale Wiedergabe ohne API-Kosten

Nach dem Site-Build kann der vorhandene Pilot in ein getrenntes Vorschauziel
geschrieben werden. Das ersetzt und verändert keinen Sitzungsrekord:

```sh
python gremium/publish_live.py .review/live-sessions/2026-09-20-pilot-03 \
  --destination site/build/live --through 41
```

Ohne `--through` wird der ganze vorhandene Verlauf ausgegeben. Für eine zeitlich
gestaffelte Wiedergabe: neues, leeres Vorschauziel verwenden und `--replay
--interval 2` angeben. Eine bereits ausgegebene Sitzung darf auch in der Vorschau
nicht zurückgespult oder verkürzt werden. Ein neuer Build entfernt generierte
Vorschaudaten; sie müssen anschließend erneut bereitgestellt werden.

Die Darstellung bezeichnet diese Daten ausdrücklich als „Wiedergabe · Testlauf“.
Abbrüche und Wiederaufnahmen des Piloten bleiben darin sichtbar. Seine spätere
[Votumsklärung](live-rat-votumsklaerung-2026-09-20.md) bleibt ein additiver Befund;
das Chatfenster korrigiert keine historischen Modellantworten oder Zusammenfassungen.

## Anschluss eines künftig freigegebenen Laufs

Der bestehende isolierte Runner nimmt optional `--live-feed-dir <Verzeichnis>`
entgegen. Ohne diese Angabe bleibt der Lauf lokal. Mit ihr veröffentlicht er
geprüfte Ereignisse synchron vor dem jeweils nächsten Modellaufruf und hält das
Lebenszeichen aktuell. Da dieser Runner weiter einen Pilotrekord erzeugt,
kennzeichnet der Feed ihn als „Testlauf · vorläufig“.

Das Ziel muss auf dem ausführenden Host als Verzeichnis erreichbar sein. Ein
Upload, ein neuer Serverdienst, VPS-Zugriff oder eine öffentliche Sitzung werden
durch diesen Einbau nicht gestartet. Vor dem öffentlichen Start ist das Ziel unter
`/live/` auf dem vorhandenen VPS konkret anzuschließen und ein vollständiger
Transporttest dort zu machen. Der Site-Deploy allein startet keine Sitzung.

## Prüfung

Gezielte Tests decken unveränderte Präfixe, Hash- und Wortlautprüfung, gemeinsame
Votenfreigabe, Archivierung, Abbruch/Wiederaufnahme, Veröffentlichungsausfall vor
Inferenz, Lebenszeichen, Kostenprovenienz, Markdown-Sicherheit und Scrollfolge ab.
Die Browserprüfung verwendet ausschließlich den bereits bezahlten Pilot 3.
Historische Sitzungen, Journale, Commissions und sämtliche Pilotdateien werden
vor und nach dem Einbau per SHA-256 verglichen. Es entstehen keine neuen API-Kosten.

## Nachtrag: eigene Medaillons vor dem öffentlichen Start

Die zuvor dokumentierten Vorgängersymbole gelten für den UI-Piloten. Vor der
ersten öffentlichen Sitzung wurden alle fünf eigenen Medaillons bestellt, vom
Wart geprüft und eingebaut. Siehe `asset-originals/medaillons-kommission-3.md`
und `live-rat-inbetriebnahme-2026-09-21.md`.
