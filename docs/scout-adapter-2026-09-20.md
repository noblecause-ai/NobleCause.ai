# Schlanker Scout-Adapter — 20.09.2026

Umgesetzt nach „bitte fortfahren, möglichst schlank“. Grok, Sonar und Opus
behalten ihre eigenen Suchwege. Keine zusätzliche Suchplattform, keine neuen
Abhängigkeiten. Der Wart nutzt denselben Versandweg mit seinem unveränderten
Modell Fable 5, ohne Suchwerkzeuge. Für diesen Rechercheablauf genügt der
vorhandene OpenRouter-Key. Die Ratsbesetzung wird dadurch nicht umgestellt.

## Was der Adapter leistet

`gremium/openrouter_scout.py` verbindet Wochen- und Sitzungslauf mit den
gemessenen Parametern. Er prüft Modelle, gepinnte Anbieter, unterstützte
Parameter, Token-/Suchpreise und ein finanziertes, nicht zurückgesetztes
Key-Limit. Keine automatische Wiederholung von Modellaufrufen und kein stiller
Wechsel von Modell, Anbieter oder Suchmaschine. Nur verzögert erscheinende
Generationsmetadaten werden lesend nachgeladen.

Anfrage, Originalantwort, Endpunktdaten, Generationsbeleg und Auswertung bleiben
getrennt erhalten. Identität, Tokenverbrauch, Abschluss und Kosten werden
zwischen Antwort und Generation abgeglichen. Datierte Namen sind nur erlaubt,
wenn der abgefragte Katalog sie als kanonischen Namen des angeforderten Modells
ausweist. Groks nativer Abschluss `completed` wird intern als abgeschlossen
verarbeitet; das Original bleibt erhalten.

Die schlanke Variante behauptet ausdrücklich **kein vollständiges Suchprotokoll**:
`query_log_complete: false`, `api_search_queries: null`. API-Zitate und
Suchzähler bleiben getrennt von Suchanfragen aus dem Modelltext. Fehlende Zähler
werden nicht als null Suchen ausgegeben. Fehlende Belege und überschrittene
angeforderte Limits erscheinen in Daten und Dossier. Das Journal kennzeichnet
Modellangaben bei den Suchanfragen. API-Zitate allein beweisen weder
Quellenrichtigkeit noch einen vollständig offengelegten Rechercheweg.

Es zählen abgerechnete Kosten, keine Rückrechnung aus Listenpreisen. Ungeklärte
Abrechnung oder Identität stoppt weitere bezahlte Schritte. Abgeschnittene oder
formal ungültige Berichte bleiben mit Kosten sichtbar. Native Suchlimits sind
keine sichere Kostenobergrenze; die lokale Grenze stoppt zwischen Schritten.
Das vorhandene Key-Limit bleibt die serverseitige Ausgabengrenze und wird vom
Adapter weder erhöht noch zurückgesetzt.

## Echter Integrationstest

Drei neue Recherchen mit der offenen Frage über die vier Säulen, ohne frühere
Ergebnisse und ohne Antworten der anderen Scouts. Anschließend wurden dieselben
Rohantworten ohne erneute Bezahlung durch den regulären Wochenlauf verarbeitet;
nur der Wart wurde zusätzlich aufgerufen. Er erhielt erst danach den
hashgeprüften öffentlichen Archivbestand.

| Rolle | Technisches Ergebnis | Credits |
|---|---|---:|
| Grok 4.6 | vier Findings; 14 Suchen bei acht angeforderten | 0,269100 |
| Sonar Pro | vier Findings; 45 API-Zitate, kein Suchzähler | 0,039600 |
| Opus 5 kompakt | vier Findings; vier Suchen, keine API-Zitationsliste | 0,414265 |
| Wart / Fable 5 | gültiger Entscheid über OpenRouter, keine Suchwerkzeuge | 0,508180 |
| Gesamt | drei Recherchen und ein Wart-Entscheid | **1,231145** |

Der Test-Wart entschied gegen eine zusätzliche Einberufung und ordnete den
TaRL-Skalierungsbefund als Wiederentdeckung ein. Das ist keine fachliche
Abnahme aller zwölf Findings: Sonar lieferte unter anderem schwache Quellen
und eine fragliche Säule-C-Zuordnung. Der Wart deutete außerdem 0 % exakte
Topic-/Source-Überschneidung zu weitgehend als fehlende unabhängige Bestätigung.
Die Originalantwort bleibt erhalten; der Vergleichsprompt wurde danach gegen
diesen Fehlschluss präzisiert. Kein weiterer bezahlter Aufruf dafür.

Artefakte: `.review/scout-adapter-20260920/`. Der vollständige technische
Testrekord liegt dort in `integration-run/journal/2026-09-20/entry.json`, nicht
im veröffentlichten Journal. Der erste Kontoabruf enthielt die letzte
Abrechnung noch nicht; separate Abgleichdateien dokumentieren die Nachbuchung.

## Auslieferungsstand

Adapter integriert und live geprüft. `three_scouts.enabled` bleibt bis zur
kontrollierten Auslieferung aus; „Suchadapter fehlt“ ist kein Blocker mehr.
Die begrenzte Nachweispolitik heißt in der Konfiguration
`native_observations_with_disclosed_gaps`.

Die Workflows reichen beim nächsten freigegebenen Rollout zusätzlich das Secret
`OPENROUTER_API_KEY` durch. Der lokale Key wurde nicht nach GitHub kopiert;
ob das Repository-Secret schon besteht, wurde nicht geprüft. Kein Commit,
Push, Deploy oder Automationsstart. Historische Rekorde bleiben unverändert.

216 Python-Tests bestanden; Site-Build und alle 46 Site-Tests bestanden.
Die Journal-Kennzeichnung wurde zusätzlich mit synthetischen neuen und alten
Daten gerendert. Der Bestand mit fünf Sitzungen und 15 Journalen validiert.
Die zwei bestehenden Svelte-Hinweise in CouncilRoom/StageHero sind unverändert.

Referenzen: [OpenRouter Web Search](https://openrouter.ai/docs/guides/features/server-tools/web-search)
und die [offizielle Dokumentationsquelle](https://github.com/OpenRouterTeam/docs/blob/main/guides/features/server-tools/web-search.mdx).
Letztere erläutert, dass native Anbieter außer Anthropic keinen entsprechenden
`max_uses`-Parameter erhalten. Die gemessenen Grenzen werden deshalb nicht
durch stärkere Garantien aus dem Prompt ersetzt.
