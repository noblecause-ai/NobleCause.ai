# Erster bezahlter Pilot: Kostenbeobachtung statt Eingabegrenze

Steward-Anweisung vom 20.09.2026: „wir lassen die obergrenze zuerst weg und
beobachten die kosten pro modell. bitte ersten bezahlten testlauf starten“.
Sie ersetzt für diesen isolierten Pilot die B4-Startbedingung des Wart-Reviews.
Ein weiterer Review oder eine erneute Freigabe ist dafür nicht erforderlich.

Der ausdrücklich gewählte Modus `--live-council --observe-costs` prüft belegte
Ist-Kosten nach jedem Aufruf und vor dem nächsten Schritt. Er verlangt keinen
belegten Input-Bound und reserviert keine Abschlusskosten. Der alte, strengere
Modus bleibt als Standard erhalten. Tokenlimits, Endpunkt-/Preisverträge,
Abrechnungsprüfung und das vorhandene 10-Credit-Key-Limit bleiben bestehen;
es wird nichts am OpenRouter-Limit geändert. Die lokale Budgetzahl ist in
diesem Modus eine Stoppschwelle zwischen Aufrufen, keine garantierte Obergrenze
für einen bereits laufenden Aufruf. Ein vollständiger Abschluss ist daher
nicht durch eine Reserve abgesichert.

`costs-live.json` enthält nach jedem bestätigten Aufruf dessen Abrechnung und
Summen je Modell; Originalantwort und Generationsbeleg bleiben im Rohordner.
Ungeklärte Abrechnung oder ungültige Antwort stoppt Folgeaufrufe. Kein stiller
Fallback, keine automatische neue Inferenz und keine Veröffentlichung.

Die Vorprüfung bestätigte fünf gepinnte Endpunkte und ein unverändertes
Key-Limit von 10 Credits, davon 4,50224507 verbraucht und 5,49775493 übrig.
Die drei blinden Scout-Berichte vom 20.09. werden wiederverwendet. Die fünf
Erstvoten dienen zugleich als echte Adaptertests; zusätzliche bezahlte Pings
werden nicht vorgeschaltet. Der Vorsitz beginnt mit Fable 5.1.

Pilotfrage: „Welche Intervention und umsetzende Organisation bietet nach der
vorliegenden aktuellen Evidenz je NobleCause-Säule die stärkste begründete
Empfehlung für zusätzliche Mittel, und welche Unsicherheiten oder Gegenbelege
könnten diese Empfehlung ändern?“

Titel: „Erster Live-Rat-Pilot: Evidenz und Gegenbelege in vier Säulen“.
Die überholte Frage aus `next-session.json` wird nicht verwendet oder geändert.
Frontend, veröffentlichte Rekorde und Vorsitzrotation bleiben unberührt.

## Ergebnis des ersten bezahlten Laufs

`2026-09-20-pilot-01` wurde am 20.09.2026 gestartet und beim ersten Votum
ordnungsgemäß gestoppt. **Keine vollständige Sitzung und kein Modellvergleich.**
Fable 5.1 lieferte bei `reasoning.effort: max` und `max_tokens: 8192` keinen
sichtbaren Antworttext. Alle 8.192 gemeldeten Ausgabetokens waren Reasoning;
der native Abschluss war `max_tokens`, normalisiert `length`.

| Ratssitz | Kosten dieses Laufs in Credits | Ergebnis |
|---|---:|---|
| Claude Fable 5.1 | 0,91879000 | Erstvotum am Tokenlimit abgeschnitten; kein Votum |
| GPT-6 Astra | — | Nicht aufgerufen |
| Grok 4.6 | — | Nicht aufgerufen |
| Kimi K3 | — | Nicht aufgerufen |
| GLM-5.3 | — | Nicht aufgerufen |

Die Eingabe umfasste 50.919 abgerechnete Tokens (0,50919 Credits), die Ausgabe
8.192 Tokens (0,40960 Credits). Die Anfrage enthielt rund 108.000 Zeichen
Nutzerkontext; Dossier samt vollständiger Provenienz und historischer Vergleich
sind für jeden Ratsaufruf entsprechend umfangreich. Das ist ein konkreter
Optimierungsbefund, kein Beleg gegen die inhaltliche Qualität des Modells.

Die Ursache entspricht dem dokumentierten Zusammenspiel von Reasoning und
Ausgabelimit: beide teilen das Ausgabe-Budget; bei vollständigem Verbrauch
durch Reasoning kann der sichtbare Antworttext leer bleiben. Der nächste
Versuch braucht ein passendes Verhältnis zwischen Denk- und Antwortbudget;
auch unnötig wiederholte Archiv-/Provenienzfelder im Gesprächskontext sollten
vorher reduziert werden, bei vollständigem Erhalt im Prüfrekord.
Quelle: [OpenRouter: Reasoning tokens and max_tokens](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens#reasoning-tokens-and-max_tokens).

Antwort-Usage, Generationsbeleg und späterer Key-Abzug bestätigen denselben
Betrag von **0,91879 Credits**. Der erste Kontoabruf war noch nicht nachgebucht;
der abschließende lesende Abgleich ergibt:

- Key-Verbrauch vorher: 4,50224507; danach: 5,42103507 Credits.
- Rest im unveränderten 10-Credit-Testlimit: **4,57896493 Credits**.
- Genau ein bezahlter Modellaufruf; keine Wiederholung und kein Ersatzmodell.
- Kein fertiges `session.json`, keine Rotation oder Veröffentlichung.

## Aus dem Test korrigiert und nachgewiesen

Der erste Fehlerpfad bewahrte bereits Rohantwort und Abrechnung auf, führte
bestätigte Kosten einer ungültigen Antwort aber noch nicht in `costs-live.json`.
Das wurde korrigiert: bestätigte Abrechnung und gültiges Votum werden getrennt
behandelt. Auch abgeschnittene oder verweigerte Antworten erscheinen nun mit
Kosten und Fehlerstatus, ohne als Votum übernommen oder erneut bezahlt zu werden.
Fehlende oder widersprüchliche Abrechnung bleibt ausdrücklich ungeklärt.

Für diesen ersten Lauf wurde die bestätigte Kostensumme nachträglich aus den
unveränderten Rohbelegen in die Kostendatei übernommen. Das ursprüngliche
Abbruchereignis mit damaliger bestätigter Ledger-Summe 0 und dem Hinweis auf
möglicherweise unaufgelöste Kosten wurde nicht umgeschrieben. Die gesonderte
Abgleichdatei löst genau diesen Stand auf; 0 war keine Nullkostenrechnung.

**253 Python-Tests bestanden**, einschließlich des neuen Beobachtungsmodus,
bestätigter Kosten bei Tokenabbruch/Verweigerung und verhinderter Doppelaufrufe.
259 geschützte Dateien aus Frontend, veröffentlichten Rekorden, Registern,
Schedule und Manifest blieben hashgleich. Kein Commit, Push oder Deploy.

Belege:

- `.review/live-pilot-costs-20260920/launch.json`, `run.log`, `outcome.json`
- `.review/live-pilot-costs-20260920/accounting-reconciliation.json`
- `.review/live-sessions/2026-09-20-pilot-01/`: Auftrag, Dossier, Rohantworten,
  Ereignisrekord und abgeglichene `costs-live.json`
- Generation: `gen-1789924230-umhDHiTxdO67AxnPp8hR`
