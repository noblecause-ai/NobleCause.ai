# Genehmigte Scout-Besetzung — 20.09.2026

Steward-Entscheid: „einverstanden. bitte scout mit diesen drei besetzen.“
Die Modellauswahl aus dem Vergleich ist damit bestätigt. Eine weitere
Bestätigung dieser Besetzung ist nicht erforderlich.

Die einzige Konfigurationsquelle ist `gremium/config.json`, Feld `scouts`:

| Aufgabe | Modell | Gepinnter Anbieter | Suchprofil |
|---|---|---|---|
| Entdeckung | x-ai/grok-4.6 | xai/zdr, xAI | native, high Reasoning, 8 angeforderte Suchschritte |
| Regionale Ergänzung | perplexity/sonar-pro | perplexity, Perplexity | integrierte Suche, low search context |
| Gegenbelege | anthropic/claude-opus-5 | anthropic, Anthropic | native, medium Reasoning, 4 Suchschritte |

Alle drei erhalten höchstens vier Findings mit höchstens 100 Wörtern je
Finding und 8.000 als angefordertem Outputlimit. Provider-Limits sind keine
garantierten requestweiten Kostenobergrenzen; der Test zeigte Überschreitungen
bei nativen Suchabläufen. Kosten müssen deshalb mit realer Usage abgeglichen
werden. Keine automatische Modell- oder Anbieterersetzung.

Rollenaufträge stehen in `prompts.scout_system_for`. Die Aufgaben unterscheiden
sich; alle drei Profile tragen `research_context: blind`. Begrenzungen,
Quellenalter, Gegenbelege und die vier Säulen gehören zum gemeinsamen Auftrag.

## Erst unabhängig suchen, danach vergleichen

Steward-Präzisierung vom 20.09.2026: Die neue Suche soll keine alten Ergebnisse
kennen. Wiederentdeckungen sind ausdrücklich erwünscht und können zeigen,
dass frühere Recherchen reproduzierbar sind.

1. Die drei Scouts erhalten jeweils einen eigenen Kontext: eine offene
   Suchfrage, den Stichtag, die vier Säulen und ihre Rechercherolle. Keine
   früheren Empfehlungen, Journalthemen, Wart-Eröffnung, kuratierte Quellenliste
   oder Antworten der anderen Scouts. Auch bekannte Organisationen werden
   nicht ausgeschlossen. Die Entdeckungsrolle verlangt Breite, keine behauptete
   Neuheit gegenüber einem unbekannten Archiv.
2. Die offene Suchfrage ist vom historischen Sitzungsauftrag getrennt:
   Die letzte Sitzungsfrage nennt selbst vier frühere Empfehlungen und darf
   deshalb nicht automatisch zum Suchprompt werden. Wochen- und Sitzungslauf
   nutzen für die drei Scouts standardmäßig `SCOUT_BLIND_QUESTION`. Für eine
   ausdrücklich vorgegebene eigenständige Suchfrage unterstützt der Sitzungslauf
   `--scout-question`; diese Eingabe wird wörtlich übernommen und sollte keine
   früheren Ergebnisse vorwegnehmen. `--question` bleibt die Ratsfrage.
3. Erst nach Abschluss aller Scouts wird der Vergleichskontext geladen:
   Empfehlungen der Vorgängersitzung und strukturierte Findings der Journale
   vor dem Recherchetag, mit exakten Herkunftspfaden. Beim Wochenlauf erhält
   ihn der Wart, bei Sitzungen der Rat. Die Vergleiche gehören in deren
   Begründungen. Der Suchbericht selbst wird nicht nachträglich umgeschrieben
   und Wiederentdeckungen werden nicht herausgefiltert.

Der Vergleich unterscheidet Wiederentdeckungen derselben Ursprungsquelle,
mögliche unabhängige Bestätigungen, im Vergleichsbestand nicht enthaltene
Funde, Widersprüche und ungeklärte Fälle. Andere Domains allein belegen keine
Unabhängigkeit; dieselbe Studie kann vielfach zitiert werden. Eine
Wiederentdeckung belegt weder automatisch die Richtigkeit einer Aussage noch
die Vollständigkeit der bisherigen Suche.

Der Vergleichsbestand wird im Modellprompt vollständig ausgewiesen und
gespeichert. Er ist auf strukturierte Findings und die Vorgängersitzung begrenzt;
Archivprosa und ältere Sitzungen werden nicht zusätzlich erschlossen. „Nicht
im Vergleichsbestand“ ist deshalb kein weltweiter Neuheitsnachweis. Das
bisherige Scout-Feld `delta_assessment` enthält im blinden Verfahren nur eine
Zusammenfassung der aktuellen Evidenzlage, keinen behaupteten historischen
Vergleich. Neue Rekorde markieren das Verfahren als `blind_then_compare`.

Die Trennung betrifft die übergebenen Kontexte. Vorwissen aus Modelltraining
oder zufällig in Suchergebnissen auftauchende NobleCause-Seiten lässt sich
damit nicht ausschließen. Die Prompts untersagen gezielte Archivsuche und
verlangen, zufällige Begegnungen offenzulegen; das ist eine Modellanweisung,
keine bereits technisch garantierte Filterung durch den Suchanbieter.

Die Orchestrierung unterstützt jetzt drei Berichte, weist Ausfälle aus und
speichert jede Rechercherolle. Der exakte Divergenzvergleich enthält für drei
Berichte gemeinsame, paarweise gemeinsame und jeweils exklusive Findings.
Er ist ausdrücklich kein semantischer Neuheitsnachweis. Bei einem Ausfall
bleiben die ursprünglichen Scout-Indizes den verbleibenden Berichten zugeordnet.
Mehr als vier Findings werden als Vertragsfehler erhalten statt still gekürzt.

## Technische Aktivierung

Die Auswahl ist genehmigt (`selection_status: approved`). Der schlanke Adapter
ist inzwischen mit drei Scout-Aufrufen und einem Wart-Entscheid live geprüft.
Er erhält die nativen Suchwege und kennzeichnet fehlende Suchprotokolle;
vollständige Query-Provenienz wird nicht behauptet. Der Wart nutzt sein
unverändertes Modell über OpenRouter. Details:
[Adapter, Kosten und Integrationstest](scout-adapter-2026-09-20.md).

`three_scouts.enabled` bleibt bis zur kontrollierten Auslieferung aus. Es fehlt
keine erneute Modellfreigabe und es gibt keinen Datenschutzvorbehalt gegen
öffentliche Journale. Der bisherige Produktionspfad bleibt lauffähig.
Die bereits vorhandenen Ein- und Zwei-Scout-Verträge bleiben erhalten.
Eine Veröffentlichung erfordert weiterhin den üblichen Commit-/Push-Schritt;
dieser Auftrag allein erzeugt keinen Deploy und keinen neuen Sitzungsrekord.

## Öffentliche Journale und Neuheitsvergleich

NobleCause ist ein offenes Projekt. Der Steward hat ausdrücklich klargestellt,
dass veröffentlichte Projektinhalte als öffentlicher Recherchekontext dienen.
Die im Scout-Vergleich gemeinten „historischen Journalthemen“ waren Topic-
Überschriften und ihre Herkunftspfade aus zehn veröffentlichten Journalen
vom 07.07. bis 14.09.2026: etwa HKI-Finanzierung, Malaria-Evidenz, New START,
DNA-Synthese-Screening und LEEP-Finanzierung.

Alle zehn Dateien wurden am 20.09.2026 ohne Anmeldung von
`raw.githubusercontent.com/noblecause-ai/NobleCause.ai/master/journal/.../entry.json`
abgerufen (HTTP 200). Ihre SHA-256-Hashes stimmen mit den lokal verwendeten
Dateien überein. Beleg:
`.review/public-journal-verification-20260920.json` im isolierten Arbeitsbaum.

Die vorherige automatische Prüfung hatte den vorgesehenen Versand dieser
Themen als möglichen Export interner Daten abgelehnt. Für diese Dateien war
die Einstufung ein Fehlalarm; es wurden keine vertraulichen Projektinhalte
entdeckt. Öffentliche Journale dienen nach der Präzisierung des Stewards erst
nach Abschluss der unabhängigen Suche zur Erkennung bereits bekannter Funde.
Die Trennung ist methodisch begründet, nicht durch vermeintliche Vertraulichkeit.
Eine lokale .env oder
Zugangsdaten sind kein Bestandteil dieses öffentlichen Kontextes.

Beim Einbau des nachträglichen Vergleichs blockierte die automatische Prüfung
zunächst die Übergabe des historischen Bestands an Modellprompts wegen möglicher
privater Inhalte. Der vollständige tatsächlich vorgesehene Bestand wurde daraufhin
abgeglichen: Die zehn bereits verifizierten Journale sind sämtliche Journale mit
strukturierten Findings. Zusätzlich ist `sessions/2026-09/session.json` anonym
öffentlich abrufbar und bytegleich; Beleg:
`.review/public-session-verification-20260920.json`. Nach diesem Nachweis wurde
die Änderung zugelassen. Es ist keine zusätzliche Inhaltsfreigabe offen.

Der vorhandene historische Neuheitsvergleich wurde bereits lokal abgeschlossen.
Für die Korrektur der Einordnung ist kein erneuter bezahlter Modelllauf nötig.

## Prüfung

Vor der Adapterintegration bestanden 197 Python-Tests, darunter 20 Tests für Besetzung, Familientrennung,
Rollen, drei unabhängige Zulieferungen, Ausfälle, Finding-Limit, Speicherung
aller drei Berichte und die Trennung von Suche und Vergleich. Die Tests prüfen
die tatsächlichen Wochen- und Sitzungsaufrufe mit markierten früheren Inhalten,
historischer Sitzungsfrage und Wart-Eröffnung; Wiederentdeckungen bleiben im
Wochenrekord erhalten. Der komplette veröffentlichte Bestand validiert weiterhin:
5 Sitzungen und 15 Journale. Die damaligen Transport- und Orchestrierungstests
waren offline mit Stubs. Der anschließende echte Adaptertest und seine Kosten
sind im oben verlinkten Adapterbericht getrennt dokumentiert.
Beim vorangegangenen Besetzungsschritt bestanden auch Site-Build und alle 46
Site-Tests; für diese reine Änderung der Recherchekontexte wurde die unveränderte
Site nicht erneut gebaut. Die beiden bereits vorhandenen
Svelte-Hinweise in CouncilRoom/StageHero bleiben unverändert.
