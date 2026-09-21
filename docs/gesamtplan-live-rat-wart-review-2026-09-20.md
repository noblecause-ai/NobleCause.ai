# Gesamtplan: öffentlicher Live-Rat mit wechselndem Vorsitz

**Abnahmestatus: `freigegeben_mit_auflagen`.** Die vollständig abgelegte
[Wart-Abnahme aus Anlauf 3](wart-abnahme-live-rat-2026-09-20.md) ist maßgeblich.
Die ersten beiden Antworten und eingereichten Fassungen bleiben als
[Review-Historie](wart-review-live-rat-2026-09-20.md) unverändert erhalten.

Stand: 20. September 2026 · Revision 2 mit Abnahmestatus und korrigierten
Textentwürfen. Nach Steward-Auftrag wird zuerst das Backend umgesetzt;
der Frontend-Einbau wird vorher besprochen. Verbindliche Präzisierungen:
[Verfahrensnachtrag 0.6](verfahren-0.6.md). Umsetzung und offene Startbedingungen:
[Backend-Abnahme](live-rat-backend-2026-09-20.md). Die Abschnitte zum damaligen
Bauzustand und zur Kostenaufnahme beschreiben den Stand vor dem Review.

## 1. Verbindlicher Auftrag des Stewards

Der bisherige Wart war eine Instanz außerhalb des Rates, um während des
Aufbaus strategische und architektonische Entscheidungen mit Auswirkungen
auf spätere Urteile und Abläufe zu prüfen und zu protokollieren. Nach diesem
Umbau soll ein stabiler Betrieb mit möglichst wenig weiteren Kernänderungen
folgen. Fable 5 bleibt für ausdrücklich beauftragte Reviews oder eine
spätere Übergabe verfügbar, ist aber keine notwendige laufende Nebeninstanz.

Es gibt genau fünf Ratsmitglieder und fünf gleich gewichtete Stimmen. Jeweils
ein Ratsmitglied hat zusätzlich den Vorsitz; dieser wechselt von Sitzung zu
Sitzung. Erster Vorsitz: Fable 5.1. Der Vorsitz darf selbst argumentieren und
abstimmen. Er bekommt keine zweite Stimme und kein Recht, die Auszählung zu
ändern. Eine öffentliche Live-Diskussion soll fortlaufend auf vorangegangene
Beiträge eingehen können. Vor der Umsetzung prüft der bisherige Wart diesen
Gesamtplan.

Bereits bestätigte Besetzung, jeweils über OpenRouter mit festem Endpunkt:

| Sitz | Modell | Endpunkt | ausgewiesene Quantisierung |
| --- | --- | --- | --- |
| Anthropic | `anthropic/claude-fable-5.1` | `anthropic` | unbekannt |
| OpenAI | `openai/gpt-6-astra` | `azure/us` | unbekannt |
| xAI | `x-ai/grok-4.6` | `xai/zdr` | unbekannt |
| Moonshot | `moonshotai/kimi-k3` | `inference-net/fp4` | fp4 |
| Z AI | `z-ai/glm-5.3` | `baidu/fp8` | fp8 |

Die erste eingereichte Fassung bleibt unter
`.review/live-rat-wart-20260920/submitted-plan-r1.md` erhalten. Die erste
Wart-Antwort wurde am Ausgabelimit abgeschnitten und gilt nicht als
abgeschlossene Abnahme. Revision 2 ergänzt den anschließend reproduzierten
Grenzfall der bisherigen Auszählung; Produktcode wurde dafür nicht geändert.

Die Endpunkte sind Kandidatenverträge, noch keine fünf erfolgreich live
geprüften Ratssitze. Ein Ausfall erlaubt keinen stillen Modell-/Hosterwechsel.

## 2. Vorsitz, Rotation und laufender Betrieb

Zur Abnahme vorgeschlagene Ausführungsregeln:

- Feste Rotation in der obigen Reihenfolge, danach wieder Fable 5.1. Die
  Reihenfolge ist explizite Konfiguration; Dateisortierung darf sie nicht ändern.
- Der gewählte Vorsitz wird vor dem ersten bezahlten Sitzungsschritt zusammen
  mit Modell, Rolle, Protokollversion und Sitzung-ID festgeschrieben.
- Der nächste Vorsitz wird erst mit dem erfolgreich abgeschlossenen,
  übernommenen Sitzungsrekord fortgeschrieben. Probeläufe, Abbrüche und
  Wiederaufnahme desselben Laufs verbrauchen keinen Rotationsplatz.
- Der für die nächste Sitzung bestimmte Vorsitz übernimmt auch die bisherige
  wöchentliche Auswertung der Scout-Berichte und den begründeten Entscheid,
  ob eine frühere Sitzung nötig ist. Dieser Rollenübergang ist ein Vorschlag
  dieser Vorlage, keine bereits ausgesprochene Einzelanweisung des Stewards.
- Wochenentscheid, Moderation und eigenes Ratsvotum werden als verschiedene
  Rollenaufrufe protokolliert. Es gibt keinen versteckten Gesprächsspeicher:
  Alle Ratsmitglieder erhalten denselben offengelegten Sachkontext.
- Der reguläre Sitzungsrhythmus bleibt bestehen; ein negativer Wochenentscheid
  kann eine regulär fällige Sitzung nicht dauerhaft verhindern.
- Bestehende Startregeln bleiben zunächst erhalten: Wochenrecherche nach
  Zeitplan; Sitzung mit ausdrücklich übergebener Frage und Titel. Der bestehende
  Terminprozess erinnert an fällige Sitzungen. Eine automatisch erfundene Frage
  oder ein neuer unbeaufsichtigter Sitzungsstart ist nicht Teil dieses Umbaus.
- Eine Aktualisierung der Modellbesetzung oder Verfahrensregeln bleibt ein
  eigener dokumentierter Vorgang. Der Vorsitz kann sie anregen, nicht selbst
  während einer Sitzung in Kraft setzen. Fable 5 ist kein Ausfallersatz.

Bei Ausfall des Vorsitzmodells gibt es im ersten Pilot keinen spontanen
Ersatzvorsitz. Der Lauf stoppt sichtbar. Eine spätere Vertretungsregel wäre
eine ausdrückliche Änderung, keine stille Ausnahme.

## 3. Drei Scouts: erst blind recherchieren, anschließend vergleichen

Die bestätigten Scouts bleiben Grok 4.6 (Entdeckungsbreite), Sonar Pro
(regionale und sprachliche Breite) und Opus 5 kompakt (Gegenbelege).
Jeder erhält die offene Forschungsfrage, vier Säulen, Stichtag und seinen
Rechercheauftrag; keine früheren Empfehlungen, Journalthemen, anderen
Scout-Ergebnisse oder richtungsweisende Vorsitz-Eröffnung.

Bekannte Interventionen werden nicht ausgeschlossen. Erst nach Abschluss
aller drei Recherchen erhält die Auswertung frühere öffentliche Ergebnisse.
Wiederentdeckungen bleiben sichtbar; dieselbe Ursprungsquelle, unabhängige
Bestätigung, zusätzlicher Befund, Widerspruch und ungeklärter Fall sind zu
unterscheiden. Unterschiedliche Domains oder null identische Topic-/Source-
Paare beweisen keine Unabhängigkeit und keine Neuheit.

Der getestete schlanke Adapter behält native Suchwege. Die akzeptierte
technische Grenze muss öffentlich klar sein: kein vollständiges Suchprotokoll;
Suchanfragen im Modelltext sind Selbstauskunft, API-Zitate und Suchzähler
werden separat ausgewiesen. Quellenqualität ist damit noch nicht bewiesen.
Angeforderte Suchlimits wurden im Versuch teilweise überschritten und sind
keine harte Kostenzusage. Der Wart soll diese Abweichung vom ursprünglichen
strengeren Suchprovenienz-Vertrag ausdrücklich mitprüfen.

Die Scouts erhalten durch den Rollenwechsel des Vorsitzes keinen historischen
Kontext. Rat und Vorsitz dürfen nach der Recherche den Vergleichsbestand
kennen. Für den ersten vollständigen Sitzungstest kann das bereits bezahlte
Dossier vom 20.09. verwendet werden; Datum und Wiederverwendung stehen dann
im Testrekord. Vor einer späteren öffentlichen Sitzung wird seine Aktualität
geprüft.

## 4. Echte fortlaufende Beratung

### Auftakt

Alle fünf Erstvoten entstehen mit identischem Sachkontext und ohne Kenntnis
anderer Erstvoten. Auch das Erstvotum des Vorsitzenden wird vorher abgegeben.
Eine inhaltliche Moderation beginnt erst nach Abschluss dieser Phase. Danach
werden die Erstvoten gemeinsam offengelegt.

### Debatte

Es spricht jeweils ein Mitglied. Jeder nächste Redner erhält den vollständigen
bisherigen öffentlichen Gesprächsverlauf einschließlich aller Moderations-
und Sachbeiträge. Ein abgeschlossener Beitrag steht allen folgenden Aufrufen
zur Verfügung; es werden nicht nur gezielt zugestellte Erwiderungen gezeigt.
Auf eine vorangegangene Replik kann erneut reagiert werden. Keine verpflichtende
Widerspruchsrolle, kein vorgeschriebenes Ergebnis.

Der Vorsitz erteilt das Wort, kann offene Fragen benennen und um eine Antwort
auf konkrete Aussagen bitten. Seine eigenen Sachbeiträge zählen gegen dasselbe
Redekontingent wie die anderer Mitglieder. Moderation soll kurz und als solche
gekennzeichnet sein. Inhaltliche Stellungnahmen gehören in einen Sachbeitrag.
Dass eine Frage des Vorsitzes den Gesprächsverlauf beeinflussen kann, wird
offengelegt; Neutralität wird nicht allein aus dem Rollenetikett abgeleitet.

Pilotvorschlag: zehn Sachbeiträge, zwei je Mitglied, maximal 180 Wörter je
Beitrag als Promptvorgabe, zusätzlich technisch begrenzte Ausgabetokens.
Der Vorsitz wählt den nächsten Redner unter Mitgliedern mit der bisher
geringsten Zahl an Sachbeiträgen. So kommen erst alle einmal zu Wort, dann
alle ein zweites Mal. Ein kurzer Vorsitzaufruf vor jedem Beitrag kann eine
konkrete Frage und den nächsten Redner nennen; höchstens zehn solcher Aufrufe.
Diese zusätzlichen Aufrufe werden vollständig eingepreist.

Das Programm prüft Rolle, zulässigen nächsten Redner, Redekontingent, Budget
und Reihenfolge. Es erfindet keine Äußerungen. Ein ungültiger Steuerauftrag
beendet den Pilot sichtbar, ohne zusätzliche bezahlte Reparaturschleife.
Kein Modell wird nach jedem Beitrag bloß zum Mithören kostenpflichtig
aufgerufen. Eigenständige Wortmeldungen zwischen API-Aufrufen gibt es im
Pilot nicht; jeder neue Aufruf erhält den aktuellen Verlauf.

### Abschluss

Nach der Debatte bekommen alle denselben eingefrorenen vollständigen Verlauf.
Jeder beantwortet darin offen gebliebene Einwände an seine Position und gibt
sein Schlussvotum ab. Kein Schlussvotum wird einem anderen Modell vor dessen
eigenem Schlussvotum gezeigt. Nur strukturierte Schlussvoten zählen; Vorsitz,
Prosa und Zusammenfassung ändern keine Stimme. Die Organisationsregistratur
und die deterministische Auszählung werden weiterverwendet, mit der folgenden
ausdrücklich zu prüfenden Schwellenänderung für das neue Verfahren. Es gibt keine vom
Vorsitz erzwungene Einigung. Die Leserfassung erstellt der Vorsitz getrennt
und auf Grundlage von Rekord und maschinell gezähltem Ergebnis.

**Nachtrag zur Auszählung:** Der heutige Code markiert mindestens zwei
übereinstimmende Stimmen ohne Gleichstand als `has_consensus: true`. Ein
synthetischer Aufruf mit fünf Stimmen im Verhältnis 2:1:1:1 hat dies bestätigt
(`.review/live-rat-wart-20260920/existing-tally-check.json`). Deshalb wird die
Regel nicht unverändert auf den Fünfer-Rat übertragen. Vorschlag zur Wart-Abnahme:
Eine gemeinsame Empfehlung im neuen Verfahren benötigt mindestens drei der
fünf Sitzstimmen für dieselbe registrierte Organisation. Der Nenner bleibt
fünf, auch bei nicht auswertbaren Stimmen; der Pilot verlangt zusätzlich alle
fünf technisch gültigen Schlussvoten für einen erfolgreichen Abschluss.
2:1:1:1 und 2:2:1 liefern keine gemeinsame Empfehlung; 3:1:1 genügt. Es gibt
keinen Stichentscheid des Vorsitzes. Die öffentliche Bezeichnung lautet
„Mehrheit“ mit sichtbarer Stimmenzahl, nicht „Einstimmigkeit“. Frühere Rekorde
und ihre Zwei-Stimmen-Regel bleiben unverändert; die Verfahrensversion legt
fest, welche Regel beim Nachvollziehen eines Rekords anzuwenden ist.

Der konkrete Mechanismus verändert den bisherigen Entscheid vom 06.08.,
der eine vom Wart inhaltlich gelenkte Gesprächsführung ausschloss. Die neue
Steward-Vorgabe ersetzt diesen Teil für künftige Sitzungen ausdrücklich.
Frühere Entscheide und Sitzungen bleiben in ihrer damaligen Form erhalten.
Der Wart soll prüfen, ob die neue Regel als Verfahrensnachtrag genügt; das
Manifest wird nicht beiläufig geändert.

## 5. Öffentliche Live-Anzeige und endgültiger Rekord

Bestehende Infrastruktur: Python-Sitzungslauf, statische SvelteKit-Site,
Deployment auf einen eigenen VPS mit Caddy. Für den Pilot reicht eine
öffentliche Ereignisdatei je Sitzung; ein dauerhafter neuer Anwendungsserver,
WebSockets oder eine zusätzliche Datenbank sind nicht erforderlich.

- Jedes Ereignis hat eine fortlaufende Nummer, Sitzung-ID, Zeitpunkt,
  Phase, Modell-ID, Rolle und gegebenenfalls die ID des beantworteten Beitrags.
  Abgeschlossene Beiträge behalten ihren Originalwortlaut.
- Das lokal dauerhaft geschriebene Ereignis wird nach Abschluss und
  technischer Prüfung des Modellaufrufs veröffentlicht. Die Veröffentlichung
  geschieht als atomarer Dateiaustausch; ein neuer Stand enthält alle zuvor
  veröffentlichten Ereignisse unverändert und fügt nur neue hinzu.
- Die Website lädt den Stand während der Sitzung etwa alle drei Sekunden
  nach. Sie zeigt aktuellen Redner, Warten auf Antwort, abgeschlossene Beiträge,
  Stand der Abrechnung und Sitzungsstatus. Modell-Denkzeiten sind reale Pausen.
  Es wird kein ungeprüfter Tokenstrom als fertige Rede ausgegeben.
- Die Live-Ansicht ist klar als laufendes, noch nicht abschließend validiertes
  Protokoll markiert. Ohne Nachricht innerhalb des erwarteten Intervalls
  zeigt sie eine unterbrochene Übertragung statt eines weiterlaufenden Redners.
- Übertragungsfehler erzeugen keine erneuten Modellaufrufe. Dauerhaft
  gespeicherte Ereignisse können unverändert erneut übertragen werden. Bei
  andauerndem Übertragungsfehler pausiert der Lauf vor dem nächsten bezahlten
  Schritt; ein Abbruch und seine Kosten bleiben erhalten.
- Modellidentität, Rohantworten, Kosten und technische Fehler bleiben im
  Abschlussrekord nachvollziehbar. Ein begonnenes öffentliches Protokoll
  verschwindet auch bei Abbruch nicht. Die Ausfallform bekommt einen eigenen
  klaren Status; sie darf keine erfolgreiche Empfehlung vortäuschen.
- Live-Dateien sind einem eigenen Pfad zugeordnet, den der normale
  Site-Deploy nicht überschreibt. Testläufe veröffentlichen keinen Feed.
- Nach Schema- und Vollständigkeitsprüfung verweist die Live-Ansicht auf den
  normalen Sitzungsrekord. Die Site zählt weiterhin keine Stimmen selbst.

Live bedeutet hier Veröffentlichung abgeschlossener Beiträge während einer
tatsächlich laufenden Sitzung. Erstvoten werden erst gemeinsam offengelegt;
Abschlussvoten ebenso erst nach Abschluss ihrer unabhängigen Erzeugung.
Zugangsdaten bleiben im Runner; die Site liest ausschließlich öffentliche Daten.

## 6. Kosten, Grenzen und offene technische Arbeit

Der Steward hat insgesamt 109 OpenRouter-Credits über mehrere Monate und
zunächst einen Testdeckel von 10 Credits vorgesehen. Letzter abgeglichener
Stand vor diesem Review: 4,15469507 verbraucht, 5,84530493 im unveränderten
Key-Limit übrig. Das ist keine Zusage, dass eine vollständige Live-Debatte
in den Rest passt. Dieses Wart-Review wird ebenfalls transparent abgerechnet.

Eine Sitzung umfasst fünf Erstvoten, zehn Sachbeiträge, bis zu zehn
Vorsitzaufrufe, fünf Schlussvoten und eine Leserfassung, zusätzlich zu einer
gegebenenfalls neuen Scout-Recherche. Der wachsende Verlauf erhöht den
Inputbedarf. Konkrete Rollen- und Tokenlimits sowie eine Gesamtkalkulation
müssen vor einem bezahlten Sitzungstest feststehen.

Vor jedem Aufruf werden Ist-Kosten, maximal vertretbare Kosten des nächsten
Aufrufs und die Reserve für fünf Schlussvoten und den Abschluss geprüft.
Unsichere Zeichen-pro-Token-Schätzungen sind keine nachgewiesene harte Grenze.
Der bisherige Ratsadapter reserviert pauschal den ganzen Modellkontext; ein
engerer Bound muss belegbar sein. Solange die Kostenkontrolle das nicht trägt,
startet keine Sitzung. Ein Zeit-/Kostenlimit kann die Debatte vorzeitig
schließen; fehlende Wortbeiträge und der Grund bleiben sichtbar. Ungeklärte
Abrechnung stoppt weitere bezahlte Schritte auch dann, wenn dadurch kein
vollständiger Abschluss mehr möglich ist. Keine automatische Wiederholung
eines möglicherweise bereits bezahlten Calls, keine Erhöhung des Key-Limits.

Aktueller Bauzustand:

- Drei Scouts und unveränderter Wart Fable 5 wurden live geprüft: zusammen
  1,231145 Credits für den letzten Integrationslauf, davon 0,508180 Wart.
- 216 Python-Tests und 46 Site-Tests mit Build waren vor diesem Plan grün.
  Diese Zahlen belegen keine Live-Debatte; 122 veröffentlichte Rekorddateien
  blieben unverändert.
- Ratsadapter vorhanden, aber kanonische Modellnamen, native Stop-Gründe und
  verzögerte Abrechnungsdaten müssen noch mit realen fünf Ratssitzen geprüft
  und an die bereits beim Scout belegten Fälle angepasst werden.
- Die vorhandene Deliberation 0.5 ist eine adressierte Zwischenrunde. Sie ist
  ausgeschaltet und erfüllt die hier beschriebene fortlaufende Debatte nicht.
- Neu zu bauen: wechselnder Vorsitz einschließlich Wochenrolle, fortlaufender
  Gesprächsverlauf, gleiche Redeanteile, Live-Ereignisse und deren Darstellung,
  konsistenter Abschluss/Abbruch und zugehörige Schemafelder.
- Rollenaufrufe sollen dieselben geprüften Ratsadapter verwenden; keine
  dauerhaft separate Fable-5-Route als neue Betriebsabhängigkeit.
- Modellregistratur additiv ergänzen; aktive Konfiguration und Workflow-
  Vorprüfung auf die genehmigte Besetzung umstellen. Neue Modellmedaillons
  können über die vorhandene Commission-Kette folgen; für den ersten
  technischen Test genügt eine ehrliche neutrale Darstellung.
- `next-session.json` bezieht sich noch auf Sitzung 3 und wird vor dem neuen
  Lauf durch eine aktuelle, ausdrücklich übergebene Frage/Titel ersetzt.
- `OPENROUTER_API_KEY` lokal vorhanden. GitHub-Secret noch nicht überprüft;
  bestehende Workflow-Timeouts und getrennte Konkurrenzgruppen müssen gegen
  längere Debatte, Rotation und gleichzeitige Wochenläufe geprüft werden.

## 7. Umsetzung erst nach Wart-Review

1. Dieses Gesamtpaket vom bisherigen Wart Fable 5 prüfen lassen. Originalantwort,
   eingereichte Fassung, Herkunft und Kosten erhalten. Verbindliche Einwände
   werden sichtbar beantwortet; eine bedingte Abnahme heißt nicht „alles fertig“.
2. Nach Abnahme kleine zusammenhängende Änderungen hinter ausgeschalteter
   Konfiguration: Ratsadapter, Rollen/Rotation, Debattenlauf, Ereignisrekord und
   Live-Anzeige. Öffentliche DE/EN-Verfahrenstexte gleichzeitig vorbereiten.
3. Gezielte Offline-Tests: jede neue Rede sieht alle früheren Beiträge;
   Erst-/Schlussvoten bleiben gegenseitig verborgen; Vorsitz hat eine Stimme
   und gleiche Redeanteile; Rotation genau einmal; alle fünf Modelle können
   Vorsitz und Wochenentscheid ausführen; Budgetreserve; Abbruch, Wiederaufnahme
   ohne Doppelaufruf, lückenloser Feed; keine Änderung historischer Rekorde.
   Die neue Dreiermehrheit wird gegen 2:1:1:1, 2:2:1, 3:1:1 und ungültige
   Stimmen geprüft; die frühere Auszählung bleibt für alte Verfahren erhalten.
4. Fünf kleine echte Adapterprüfungen, anschließend ein vollständiger isolierter
   Sitzungstest mit festem Budget und vorhandenem Dossier. Keine zusätzliche
   Recherche bloß für einen technischen Wiederholungstest. Der verfügbare
   Testrest wird vor Beginn geprüft, nicht still aus dem Gesamtguthaben ergänzt.
5. Prüfergebnisse und Änderungen zur konkreten Auslieferungsfreigabe vorlegen.
   Commit, Push, öffentliche Live-Sitzung und Deploy sind jetzt nicht ausgelöst.
   Danach stabiler Betrieb; Strategie-Reviews nur bei tatsächlichem Anlass.

## 8. Entwurf des öffentlichen Verfahrenstextes zur Wart-Prüfung

**DE:** Fünf KI-Modelle beraten über dieselben Belege. Zunächst formuliert jedes
sein Erstvotum, ohne die Antworten der anderen zu kennen. Danach diskutieren
sie unter wechselndem Vorsitz eines ihrer Mitglieder. Jeder neue Redebeitrag
kennt den bisherigen Gesprächsverlauf. Der Vorsitz organisiert das Gespräch,
beteiligt sich mit eigenen Beiträgen im gleichen Redekontingent und stimmt mit
genau einer Stimme mit; dass seine Fragen den Verlauf beeinflussen können, ist
Teil des offenen Protokolls. Feste Regeln begrenzen Redeanteile und
Kosten. Abgeschlossene Beiträge können während der Sitzung öffentlich verfolgt
werden; laufende und abgebrochene Sitzungen sind als solche gekennzeichnet.
Am Ende gibt jedes Modell sein eigenes Schlussvotum ab, ohne die Schlussvoten
der anderen zu kennen. Ein festes Programm zählt ausschließlich diese Voten.
Eine gemeinsame Empfehlung benötigt mindestens drei der fünf Stimmen;
die Stimmenverteilung und abweichende Empfehlungen bleiben sichtbar.
Beiträge, Quellen, Ausfälle und Kosten bleiben im Protokoll nachvollziehbar.
Die Scouts recherchieren vorher getrennt und ohne vorgegebene frühere
Ergebnisse. Der historische Vergleich folgt erst danach. Die Suchanbieter
liefern kein vollständiges Suchprotokoll; entsprechende Lücken werden ausgewiesen,
und von den Modellen genannte Suchanfragen sind als Selbstauskunft gekennzeichnet.

**EN:** Five AI models consider the same evidence. Each first writes an initial
vote without seeing the others' answers. They then discuss the evidence under
a rotating chair drawn from their own members. Each new contribution receives
the conversation so far. The chair organizes the discussion, contributes its own
remarks within the same speaking quota, and has exactly one vote; that its
questions can shape the course of the debate is part of the open record.
Fixed rules limit speaking turns and costs. Completed contributions
can be followed publicly while the session is running; ongoing and aborted
sessions are clearly marked. Each model then casts its own final vote without
seeing the others' final votes. A fixed program counts only those votes.
A shared recommendation requires at least three of the five votes;
the vote distribution and dissenting recommendations remain visible.
Contributions, sources, failures and costs remain traceable in the record.
The Scouts research separately beforehand, without being given earlier findings.
Comparison with the historical record takes place afterward. Search providers
do not supply complete search logs; these gaps are disclosed,
and search queries stated by the models are labeled as self-reported.

Der vorhandene, bereits geprüfte OpenRouter-Provenienztext wird ergänzend
beibehalten. Historische Sitzungen erhalten keine neue Verfahrensbeschreibung,
die ein damals nicht stattgefundenes Gespräch behauptet.

## 9. Konkrete Fragen an den bisherigen Wart

Bitte entscheide über den Bauplan, nicht über eine noch ungeprüfte
Produktionsfreigabe. Keine Zustimmung allein wegen der Steward-Vorgabe:
konkrete Widersprüche zu Evidenz, Unparteilichkeit, Demut, Transparenz und
Rekordtreue ausdrücklich benennen.

1. Trägt der Wechsel von externer Aufbauinstanz zu fünf Stimmen mit rotierendem,
   stimmberechtigtem Vorsitz? Welche frühere Regel wird ausdrücklich abgelöst?
2. Genügen die vorgeschlagenen Grenzen für Moderation, eigene Beiträge,
   gleiche Redeanteile und unabhängige Erst-/Schlussvoten? Ist die ausdrücklich
   versionierte Dreiermehrheit aus dem Nachtrag zulässig und hinreichend klar?
3. Ist der Übergang der Wochenaufgaben an den nächsten Vorsitz konsistent?
   Sind Rotation, Abschluss, Abbruch und Wiederaufnahme ausreichend bestimmt?
4. Ist die begrenzte Suchprovenienz zusammen mit der blinden Recherche ehrlich
   und vertretbar? Welche Mindestnachweise fehlen vor dem produktiven Start?
5. Ist die Veröffentlichung laufender/abgebrochener Sitzungen rekordtreu?
   Welche Lücken bei Feed, Fehlern oder Abschluss müssen vor dem Bau geschlossen
   werden, ohne eine neue Plattform zu verlangen?
6. Sind die DE/EN-Verfahrenstexte freigabefähig? Falls nicht, genaue minimale
   Korrekturen liefern. Erfordert etwas wirklich eine Manifeständerung?
7. Welche Auflagen gelten vor Bau, welche vor bezahltem Test und welche vor
   öffentlichem Start? Bitte zwingende Auflagen von bloßen Empfehlungen trennen.

Gewünschter Abschluss: `freigegeben`, `freigegeben_mit_auflagen` oder
`nicht_freigegeben`, mit wenigen konkret prüfbaren Auflagen. Keine neue
Review-Kaskade oder zusätzliche Instanz ohne benannten tatsächlichen Bedarf.
