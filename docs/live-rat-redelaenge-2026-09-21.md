# Sitzungsnachtrag 0.6-speech-limit-1 · 21. September 2026

Sitzung 2026-09-21-live hielt nach Kimis erstem Beitrag an: 186 durch Leerraum
getrennte Tokens ohne JSON überschritten den Promptauftrag von 180 Wörtern.
Ohne alleinstehende Gedankenstriche sind es 183 Wörter. Der Abbruch bleibt im
öffentlichen Ereignisrekord unverändert. Bestätigte Kosten zu diesem Zeitpunkt:
1,313412493 Credits.

Der bisherige Wart Fable 5 hat die Wiederaufnahme dieser konkreten Sitzung als
Fehlerbehebung innerhalb des bestehenden Steward-Auftrags freigegeben. Seine
unveränderte Antwort und die Rohbelege stehen unter
`sessions/2026-09-21-live/procedure-review/`; der Zusatzreview kostete
0,17493 Credits. Eine dauerhafte Umstellung verlangt weiterhin eine ausdrückliche
Steward-Bestätigung und wurde nicht aktiviert.

Der ausschließlich für diese Wiederaufnahme übergebene Nachtrag
`procedure-amendment-1.json` setzt 200 Wörter als äußerste Toleranz. 180 bleiben
unveränderter Promptauftrag. Strukturell gültige, vollständige und belegbar
abgerechnete Beiträge zwischen 181 und 200 Wörtern bleiben wörtlich erhalten;
Wortzahl, Lexemzahl, Überschuss und Nachtraghash werden öffentlich am Beitrag
vermerkt. Oberhalb 200 bleibt der Abbruch bestehen. Dieselbe Regel gilt für
alle fünf Mitglieder; jeder Beitrag belegt genau einen der zwei Redeplätze.

Zählung: `strip_json_block(text).split()` einschließlich alleinstehender
Satzzeichen. Zusätzlich wird die Zahl der Tokens mit mindestens einem
alphanumerischen Zeichen ausgewiesen. Kein Wort wird geändert. Rollen,
Wortvergabe, Antwortstruktur, Kostenprüfung und Schlussvotenvertrag bleiben
unverändert. Die Wiederaufnahme hängt einen `resumed`-Eintrag mit Nachtrag und
Hash an und verwendet sämtliche bestätigten Antworten ohne neue Inferenz.

Ohne expliziten, zur Sitzungs-ID passenden Nachtrag und `--resume` gilt weiterhin
die harte 180-Wort-Grenze. Kein Workflow und kein automatischer Standard wird
mit dieser Ausnahme verändert.
