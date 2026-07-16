# NobleCause.ai — Repository-, Daten-, Deployment- und Designanalyse

Stand: 15. Juli 2026  
Untersuchter Branch: `feat/immersive-homepage` (`345a13e`)  
Phase: Analyse; keine Implementierung

## 1. Executive Summary

Die neue Startseite muss in der bestehenden SvelteKit-Anwendung unter `site/` entstehen. Nur `site/` wird auf `master` in GitHub Actions mit Node 22 gebaut; das Ergebnis `site/build/` wird nach `/srv/noblecause/` auf den VPS synchronisiert und dort von Caddy statisch ausgeliefert. `sol-build/` ist ein nicht deployter, datengetriebener Vorläufer. Seine Gestaltung und seine reine Renderlogik sind wertvolle Referenzen, sein Python-Ausgabepfad ist aber kein Integrationsziel.

Die heutige produktive Startseite ist technisch solide, statisch vorgerendert und klein, vermittelt NobleCause jedoch als schmale dokumentarische Textseite mit Karten. Sie erklärt den öffentlichen Beratungsmechanismus erst abstrakt, zeigt weder Ratssaal noch Vorzimmer und macht die zwei Beratungsrunden oder sichtbare Meinungsänderungen auf der Startseite nicht erfahrbar. Das scheitert atmosphärisch nicht an mangelnder Lesbarkeit, sondern an fehlendem Raum, fehlender Dramaturgie und einer visuellen Grammatik, die austauschbare Inhaltsblöcke statt eines zusammenhängenden Verfahrens zeigt.

Die stärkste vorhandene gestalterische Grundlage ist die frühere Ratssaal-Sektion aus `sol-build/`: ein kreisförmiger Raum mit drei gleichwertigen, räumlich getrennten Pulten und einer leeren, mechanisch markierten Mitte. Bildkomposition, Lichtregie und räumliche Semantik erklären Gleichrangigkeit und Determinismus ohne Modellfiguren oder Dashboard-Metaphern. Diese Logik sollte in SvelteKit als eine semantische, serverseitig vorgerenderte Inhaltsfolge gebaut und auf Desktop durch eine sticky Bühnenansicht erweitert werden. Mobil braucht es stattdessen ein eigenständiges, lineares „Sitzungsbuch“ mit gut auffindbarem Ergebnis, direkten Spendenlinks und optionalen atmosphärischen Raumfenstern.

Die Daten reichen für Empfehlungen, Konsens/Nicht-Konsens, Modellattribution, konditionale Stimmen, Kosten und einen deterministischen Vergleich von Erst- zu Schlussvotum. Organisationsidentität, Beschreibung und Spendenweg müssen über `organization_id` aus `organizations.json` aufgelöst werden. `rationale_md` ist nur Aggregations-Boilerplate und keine Begründung. Die tatsächlichen Begründungen liegen in den publizierten `content_md`-Volltexten; sie können angezeigt, aber nicht zuverlässig in kurze Begründungssätze zerlegt werden. `dissent_md` und Korrekturtexte sind Markdown und können lange eingebettete JSON-Codeblöcke enthalten. Das Schema charakterisiert die Daten, wird von der SvelteKit-Ladelogik aber derzeit nicht validiert.

Empfehlung: `site/src/routes/+page.server.js` zu einem expliziten Homepage-View-Model aus Sitzung, Registry und strukturierten Voten erweitern; `site/src/routes/+page.svelte` ersetzen; szenenspezifische Komponenten unter `site/src/lib/components/home/` anlegen; die beiden C2PA-Originale unverändert in `site/static/` übernehmen und daraus nur mit nachweislich erhaltener Provenienz responsive Ableitungen erzeugen. Die bestehenden Sitzungsrouten bleiben das vollständige Archiv, sollten später aber dieselbe Identitätsauflösung und eine sichtbare Revisionsdarstellung erhalten.

## 2. Verifizierte Aussagen aus der Architektenübergabe

| Aussage | Befund | Beleg |
|---|---|---|
| `site/` ist das Deploymentziel | bestätigt | `.github/workflows/deploy.yml`, `site/svelte.config.js` |
| `adapter-static` wird verwendet | bestätigt | `@sveltejs/adapter-static`, Ausgabe nach `site/build/` |
| Deployment: `master` → Node 22 → `npm ci` → Build → rsync | bestätigt | Workflow synchronisiert `site/build/` nach `/srv/noblecause/` |
| `sol-build/` ist nicht Teil des Deployments | bestätigt | kein Workflow referenziert den Python-Generator |
| jüngste Sitzung wird nach `number` gewählt | für SvelteKit und SOL bestätigt | `content.js:listSessions()` und `build.py:latest_session()`; aktuell Nr. 3, `2026-07c` |
| `rationale_md` ist Boilerplate | bestätigt | alle untersuchten Werte beschreiben nur Konvergenz bzw. fehlende Konvergenz |
| strukturierte Voten liegen in `rounds[].votes[].recommendations[]` | bestätigt | beide Referenzsitzungen und Schema |
| `dissent_md` enthält Markdown/JSON | bestätigt | 6.386–7.173 Zeichen; zwei bzw. drei JSON-/Codeblöcke |
| `donation_url` kann `null` sein | bestätigt | Registry: `pratham`, `tarl-africa`, `global-road-safety-partnership` |
| Organisationsidentität kommt aus der Registry | bestätigt und zwingend | `organizations.json`, Aggregator und Golden-Tests |
| konditionale Stimme zählt zum Konsens | bestätigt | `2026-07c`, Säule A: 3/3, davon Claude konditional |
| Korrekturvermerk in `2026-07b` und `2026-07c` | bestätigt | `correction_notice`; in `2026-07` nicht vorhanden |
| Kosten liegen inline unter `costs` | bestätigt | alle `session.json`; kein sitzungsspezifisches `kosten.json` |
| Ratssaal- und Vorzimmer-Plates sind ca. 2 MB | bestätigt | 2.005.102 und 1.997.325 Bytes; Maße stimmen |
| C2PA darf nicht entfernt werden | Metadatenherkunft in `ASSETS.md` dokumentiert; nicht neu re-encodiert | Originaldateien blieben unverändert |

Eine zusätzliche Abweichung aus dem Golden-Test-Kommentar ist relevant: `run_wart.latest_session()` soll weiterhin nur nach Datum sortieren. Das betrifft nicht die produktive Homepage-Auswahl, ist aber ein dokumentiertes Backendrisiko außerhalb der erlaubten Präsentationspfade.

## 3. Aktueller technischer Aufbau

- Svelte 5.56 / SvelteKit 2.69 / Vite 8.1, ESM, rein statischer Adapter.
- `site/src/routes/+layout.js` setzt `prerender = true` und `trailingSlash = 'always'` global.
- `site/src/lib/server/content.js` liest synchron zur Buildzeit Dateien aus dem Repository-Root. Es gibt keine API und keine Laufzeitdatenbank.
- `marked` rendert Manifest-, Sitzungs-, Journal- und Dissens-Markdown zur Buildzeit in HTML.
- Routen: `/`, `/idee/`, `/manifest/`, `/sessions/`, `/sessions/[id]/`, `/journal/`, `/journal/[id]/`, `/impressum/`.
- Dynamische Sitzungs- und Journalrouten liefern über `entries()` alle statisch zu prerendernden IDs.
- `schedule.json` wird in `prebuild` nach `site/static/schedule.json` kopiert. Die Startseite enthält einen statischen Countdown und aktualisiert ihn nach Hydration jede Minute.
- Es existiert keine zentrale TypeScript-Typdefinition, kein View-Model-Schema, keine AJV-/JSON-Schema-Validierung in `site/` und kein Sanitizer für gerendertes Markdown.
- Es existieren keine npm-Skripte für Typprüfung, Linting oder Tests.

Die Architektur ist für committed content und statische Veröffentlichung passend. Der Ausbau sollte ihre Buildzeit-Datenquelle beibehalten und keine Client-API einführen.

## 4. Tatsächlicher Build- und Deploymentpfad

Der produktive Pfad ist eindeutig:

```text
Repository-Root-Daten
  ├─ sessions/*/session.json
  ├─ organizations.json
  ├─ manifest.md
  └─ schedule.json
          ↓ Buildzeit-Lader
site/src/** (SvelteKit)
          ↓ cd site && npm ci && npm run build
site/build/
          ↓ rsync -avz (ohne --delete)
noblecause@185.143.100.222:/srv/noblecause/
          ↓
Caddy (statische Auslieferung)
```

Antworten auf die sechs Deploymentfragen:

1. Die neue Startseite muss in `site/src/routes/+page.svelte`, ihrem Server-Loader und Komponenten/Assets innerhalb von `site/` implementiert werden.
2. `+page.svelte` sollte vollständig ersetzt und `+page.server.js` erweitert werden. `content.js` sollte Registry-Laden, validierte Identitätsauflösung und ein Homepage-View-Model erhalten. `+layout.svelte` muss für eine vollbreite Bühnenroute erweitert werden, ohne die Dokumentrouten zu beschädigen. `ResultCard.svelte` kann nicht unverändert die Hauptbühne tragen; seine Ergebnislogik kann extrahiert bzw. in eine neue semantische Ergebnis-Komponente überführt werden. Die Sitzungsdetailroute sollte später Revisionsdarstellung und Registry-Beschreibungen teilen.
3. Übernehmbar aus `sol-build/`: räumliche Semantik, Ratssaal-/Vorzimmer-Originale, deterministische Funktionen für Revisionen und Ergebniszustände, zugängliches Tab-/Tastaturmuster, No-JS-Prinzipien und einzelne institutionelle Texte aus `frontend-config.json` nach inhaltlicher Prüfung. Nicht übernehmen: generiertes HTML, Python-Buildpfad, globale CSS-Datei als Ganzes oder die dortige Auswahl einer einzelnen „führenden“ Empfehlung.
4. `sol-build/` jetzt weder löschen noch in den Deploypfad kopieren. Es als historische Referenz ignorieren bzw. nach abgeschlossener Integration in einem separaten, freigegebenen Cleanup archivieren. Entfernen ist in dieser Phase unnötig und würde Tests/Provenienz verlieren.
5. Lokal/CI produktiv: `cd site && npm ci && npm run build`; statische Ausgabe: `site/build/`. Deployment zusätzlich per Workflow-Rsync nach `/srv/noblecause/`.
6. Verhindern eines Waisen-Prototyps: jede Homepage-PR muss Dateien unter `site/src/routes/` enthalten, `npm run build` aus `site/` bestehen, das Ergebnis aus `site/build/` lokal reviewbar machen und einen Integrationstest besitzen, der die produktive `/`-Ausgabe auf aktuelle Sitzungsdaten, Registry-Links und beide Ergebniszustände prüft. Kein separates Entry-HTML und kein zweiter Generator.

Risiko im aktuellen Deploy: rsync läuft bewusst ohne `--delete`; entfernte alte Dateien können auf dem VPS liegen bleiben. Das erzeugt nicht die Homepage selbst falsch, kann aber verwaiste URLs konservieren.

## 5. Aktueller visueller Aufbau

Die produktive Startseite ist ein maximal 44 rem breites Dokument mit System-Serifenschrift, Papierfarbton, einfachem Header, horizontalen Trennlinien und einem abstrakten SVG. Danach folgen Einleitung, jüngste Sitzung, vier `ResultCard`-Ergebnisse, Countdown, Säulentabelle, Kanons, Sitzungsindex und Geldfluss-Hinweis. Dark Mode wird nur über `prefers-color-scheme` umgesetzt.

`ResultCard` unterscheidet Konsens und Nicht-Konsens korrekt: Konsens erhält Rahmen, Konvergenzpunkte, Konfidenzbalken, Vorbehalte und Link; Nicht-Konsens erscheint als linksgestrichene Reihe mit gleichwertigen Einzelvoten. Auf der aktuellen Homepage ist aber nur der Konsensfall `2026-07c` sichtbar. Die Bühne, Runden, Belege und Revisionen fehlen.

Die Sitzungsdetailroute zeigt Ergebnis, Kurzfassung, Dissens-Highlights, Dossier, Moderation, Prompts, Volltexte und Kosten in aufeinanderfolgenden Überschriften und `<details>`. Sie veröffentlicht viel, übersetzt die Daten jedoch nicht in ein räumliches oder vergleichendes Interaktionsmodell.

## 6. Warum der derzeitige Build atmosphärisch scheitert

1. Die Seite ist eine Dokumentkolumne, kein Raum. Jede Information nimmt denselben linearen Modus ein.
2. Das Hero-SVG ist ein neutrales Flussdiagramm. Es erzeugt weder Maßstab noch Materialität, Licht oder institutionelle Gravitas.
3. Ergebnisblöcke sind standardisierte Karten mit Rahmen und Hintergrund. Sie könnten aus nahezu jedem redaktionellen Dashboard stammen.
4. Die drei Modelle sind im Erstkontakt unsichtbar. Gleichrangigkeit wird behauptet, nicht räumlich erfahren.
5. Die deterministische Mitte fehlt. Dadurch bleibt der entscheidende Unterschied „Modelle beraten, Programm zählt“ abstrakt.
6. Der Prozess folgt erst nach dem Ergebnis als Textgliederung; es gibt keine Zustandsverwandlung, keinen Fokuswechsel und keine bleibende Bühne.
7. Warme Bernstein-/Messing- und kalte Mondlichtpole fehlen. Papierfarben und Akzentgrün/-orange sind lesbar, aber nicht szenisch.
8. Die Informationsdichte der Karten konkurriert mit dem Hero, statt Teil einer Raumhandlung zu sein.
9. Die Ursprungsmotivation und die klare Leitfrage „Wo hilft meine Spende am meisten?“ fehlen im Erstkontakt.
10. `rationale_md` wird auf Sitzungsseiten als `rationale_html` vorbereitet, aber `ResultCard` zeigt es nicht; zugleich fehlt eine belastbare alternative Kurzerklärung aus der Registry.

## 7. Warum die frühere Ratssaal-Sektion besser funktioniert

Die Ratssaal-Plate besitzt eine starke zentrale Perspektive: konzentrische Stein- und Holzringe führen zur leeren Mitte, drei warme Pulte bilden ein gleichwertiges Dreieck, kaltes Mondlicht definiert den institutionellen Raum. Die Menschen/Arbeitsplätze sind klein gegenüber der Architektur; dadurch wirken die Modelle nicht wie sprechende Maskottchen. Das leere Zentrum visualisiert, dass kein Modell herrscht.

Der alte SOL-Aufbau verstärkt diese Semantik durch drei gleich große Hotspots und eine CSS-Zählmaschine in der Mitte. Raum und Navigation sind dasselbe System: Pult führt zum Modellprotokoll, Maschine zum Ergebnis. Damit trägt die Szene Information, statt nur Hintergrund für Karten zu sein. Die visuelle Hierarchie entsteht aus Licht, Entfernung und Position, nicht primär aus schwarzen Overlayboxen.

Schwächen des alten Aufbaus, die nicht kopiert werden sollten: Er bleibt trotzdem eine lange Folge aus Hero, Prozessband, Ratssaal, Vorzimmer, Tab-Protokoll und Archiv; der Hero legt erneut vier dunkle Karten über dasselbe Bild; die Maschine ist ein typografisches Zahnrad-Symbol und kein glaubwürdiges Raumelement; `dissent_md` wird in `build.py` escaped und dadurch nicht als Markdown formatiert; die fokussierte „führende Empfehlung“ ist eine zusätzliche Präsentationsrangfolge, die fachlich nicht mit der Vier-Säulen-Gleichwertigkeit verwechselt werden darf.

## 8. Relevante Dateien und Verzeichnisse

| Pfad | Rolle |
|---|---|
| `docs/handoff-notes-for-codex.md` | technische Übergabe |
| `AGENTS.md` | harte Pfad- und Integrationsgrenzen |
| `.github/workflows/deploy.yml` | einziger produktiver Deployworkflow |
| `site/` | tatsächlich deployte SvelteKit-App |
| `site/src/routes/+page.*` | aktuelle Homepage und Datenprojektion |
| `site/src/routes/+layout.*` | globale schmale Dokumenthülle, Prerender/Slash-Regeln |
| `site/src/routes/sessions/[id]/*` | vollständige Sitzungsansicht |
| `site/src/lib/server/content.js` | Buildzeit-Dateilader und Markdown-Parsing |
| `site/src/lib/components/ResultCard.svelte` | aktueller Konsens-/Dissensrenderer |
| `schema/session.schema.json` | charakterisierendes Sitzungsschema |
| `schema/organizations.schema.json` | Registryvertrag |
| `sessions/2026-07c/session.json` | Konsensreferenz, Sitzung 3 |
| `sessions/2026-07/session.json` | Nicht-Konsensreferenz, Sitzung 1 |
| `organizations.json` | kanonische Org-Identität, Beschreibung, Spendenwege |
| `sol-build/build.py` | nicht deployter Referenzrenderer und Revisionslogik |
| `sol-build/styles.css`, `app.js` | frühere Raum-/Interaktionssprache |
| `sol-build/frontend-config.json` | Präsentationskonstanten des Vorläufers |
| `sol-build/site/static/*.png` | Ratssaal-/Vorzimmer-Originale mit C2PA |
| `tests/golden/` | Aggregations- und Determinismusregressionen |
| `sol-build/tests/` | Renderzustände des Vorläufers |

`serve/` enthält eine lokale Review-Ausgabe des SOL-Builds und Symlinks auf dessen CSS/JS/Assets. Es ist kein produktiver Quell- oder Deploymentpfad.

## 9. Tatsächliche Datenstruktur laut Schema

Top-Level Pflichtfelder: `schema_version` (konstant 2), `id`, `number`, `date`, `title`, `question`, `summary`, `dissent_highlights`, `participants`, `prompts`, `rounds`, `dissent_md`, `recommendations`, `unresolved_votes`, `costs`. `additionalProperties: true` ist bewusst gesetzt, weil das Format bei unveränderter Schema-Version evolviert ist.

Zuverlässig direkt verwendbar:

- Sitzung: `id`, `number`, `date`, `title`, `question`.
- Modellzuordnung: `participants[].family`, `.model`, `.label`; Verknüpfung über `model`.
- Rundenart: `rounds[].kind`, nicht nur die numerische `round` (es gibt -1, 0, 1, 1.5, 2).
- Strukturierte Entscheidung: `rounds[kind=initial_vote|final_vote].votes[].recommendations[]` mit `pillar`, `organization_id`, `organization`, `title`, `confidence`, `conditional`, `reservation`.
- Ergebnis: `recommendations[].pillar`, `has_consensus`; bei Konsens `organization_id`, `convergence`; bei Nicht-Konsens `individual_votes`.
- Kosten: `costs.currency`, `.total`, `.fx_rate_usd_eur`, `.by_model[]`.
- Korrektur: optionales `correction_notice`.
- Unaufgelöste Stimmen: `unresolved_votes` müssen sichtbar als Datenproblem behandelt werden und dürfen nicht verschwinden.

Nur nach Transformation verwendbar:

- Orgname, Beschreibung und URL: anhand `organization_id` mit Registry abgleichen; die Registry ist maßgeblich.
- Meinungsänderung: pro `model + pillar` Erst- und Schlussvotum anhand `organization_id` vergleichen.
- Modelllabel in Voten: `vote.model` gegen `participants[].model` auflösen; Ergebnis-`convergence.models` enthält dagegen schon Labels.
- Markdown: `content_md`, `dissent_md`, Wart-Texte und Korrekturtext semantisch rendern/falten.
- `dissent_highlights`: laut Schema Array oder String; UI muss normalisieren. Aktuelle drei Sitzungen verwenden Arrays.
- Datum/Währung/Konfidenz: lokalisiert formatieren, aber Rohwert nicht verändern.

Nicht als Tatsachenbegründung verwenden: `rationale_md`. `summary` und `dissent_highlights` sind modellgeschriebene Leserfassungen und können nach einer Aggregationskorrektur der korrigierten Ergebnisstruktur widersprechen.

## 10. Organisationsregistry und Identitätsauflösung

`organizations.json` enthält 13 kuratierte Organisationen. `id` ist die kanonische technische Identität; `canonical_name`, `beschreibung` und `donation_url` kommen aus demselben Eintrag. Aliase sind Eingabeauflösung des Aggregators, nicht die Vergleichsbasis des Frontends.

Regeln für die Darstellung:

1. Niemals Organisationsnamen als Identität vergleichen.
2. Jede Ergebnis- und Rundennennung über `organization_id` in eine `Map` der Registry auflösen.
3. `canonical_name` und `beschreibung` aus der Registry anzeigen; ein abweichender publizierter `organization`-String ist ein Validierungsfehler, kein alternativer Name.
4. Ausschließlich `registry.donation_url` verlinken. Modell-URLs aus Prosa/Rohantworten ignorieren.
5. Bei unbekannter ID oder widersprüchlichem Namen keine Ersatzorganisation erfinden: Empfehlung mit klarer Datenwarnung und ohne Link rendern; Build in CI möglichst fehlschlagen lassen.
6. Bei `donation_url: null` keine tote CTA erzeugen. Neutral „Kein kuratierter direkter Spendenweg veröffentlicht“ anzeigen.

Drei von 13 Einträgen haben keine URL; sieben von 13 haben kein `donation_url_verified_at`. „URL vorhanden“ darf daher nicht mit „aktuell verifiziert“ gleichgesetzt werden. Die Registry enthält außerdem Prüfnotizen, die nicht für die öffentliche Kartenbegründung gedacht sind.

## 11. Markdown-, JSON- und Inhaltsfallen

- `rationale_md` klingt wie Begründung, ist aber nur maschinelle Zählzusammenfassung. Nicht als „Warum diese Organisation“ darstellen.
- Die ausführlichen Begründungen liegen in `votes[].content_md`. Struktur daraus nicht per Regex oder Markdown-Parsing ableiten.
- `dissent_md`: `2026-07` 7.173 Zeichen/78 `**`/2 Codeblöcke; `2026-07b` 6.386/22/3; `2026-07c` 6.941/30/3. Der Text braucht `<details>`, gute Codeblock-Überläufe und eine kurze, getrennte Einstiegsebene.
- `correction_notice.text` ist im Schema als Text bezeichnet, laut Übergabe aber als Roh-Markdown zu behandeln. Die aktuelle Sitzungsroute rendert es als normales `<p>`; Markdown-Auszeichnung würde dort literal erscheinen.
- `marked.parse` wird mit `{@html}` ausgegeben. Inhalt ist committed/trusted, dennoch besteht ohne Sanitizer ein Supply-Chain-/Content-XSS-Vertrag: zukünftiges Markdown mit HTML wird als HTML ausgeführt. Mindestens `marked` auf HTML-Unterdrückung konfigurieren oder Buildzeit-Sanitization bewusst einführen.
- Codeblöcke mit JSON müssen `overflow-x: auto`, lesbare Zeilenhöhe und Kopierbarkeit erhalten; nie in eine Raumkarte zwängen.
- Die aktuelle SOL-Referenz escaped `dissent_md`, statt Markdown zu rendern; sie ist hier kein Implementierungsvorbild.
- `dissent_highlights` kann String sein. Ein String darf nicht mit Sveltes `{#each}` zeichenweise iteriert werden.
- `rounds` enthalten Wart-Runden ohne `votes`; jede Iteration braucht `(votes ?? [])`.
- `confidence` kann auf Votum- und Empfehlungsebene `null` sein. Null ist „nicht publiziert“, nicht 0 %.
- Aktuelle Sitzungsdetailseite bezeichnet alle `{@html}`-Inhalte als trusted; diese Vertrauensannahme muss dokumentiert und getestet werden.

## 12. Abbildung des Konsensfalls `2026-07c`

`2026-07c` ist Sitzung Nr. 3 und daher die aktuelle Sitzung. Alle vier Säulen haben Konsens:

| Säule | Organisation aus Registry | Stimmen | Besonderheit | URL |
|---|---|---:|---|---|
| A | Helen Keller International | 3/3 | 1 konditionale Stimme (Claude Opus) | vorhanden |
| B | Against Malaria Foundation | 2/3 | GPT stimmt im Schlussvotum für HKI | vorhanden |
| C | Nuclear Threat Initiative (NTI) | 3/3 | kein Vorbehalt | vorhanden |
| D | Lead Exposure Elimination Project (LEEP) | 3/3 | kein Vorbehalt | vorhanden |

Die Homepage muss alle vier Empfehlungen gleichwertig auffindbar machen. „Konsens“ darf nicht pauschal „3/3“ bedeuten: Säule B ist mit 2/3 regelkonformer Konsens. Säule A darf nicht als vorbehaltlos dargestellt werden. Der Korrekturvermerk vom 14.07.2026 muss erreichbar sein, weil Kurzfassung und Dissens unverändert geblieben sind und widersprechen können.

Der glaubwürdige Karteninhalt ist: Säule, Registryname, Registrybeschreibung, Stimmenzahl, konditionaler Status/Reservation, direkter Registrylink, Link zum vollständigen Schlussvotum. Der `rationale_md`-Satz bringt darüber hinaus keinen Erkenntnisgewinn.

## 13. Abbildung des Nicht-Konsensfalls `2026-07`

Sitzung Nr. 1 hat nur in Säule A keinen Konsens. Die drei Schlussvoten stehen gleichwertig nebeneinander:

- Claude Sonnet → Helen Keller International, Konfidenz 0,70.
- Gemini Pro → Iodine Global Network (IGN), Konfidenz 0,90.
- GPT → Evidence Action, Konfidenz 0,63.

Alle drei besitzen derzeit Registry-URLs, aber `donation_url_verified_at` ist nur für HKI gesetzt. Die UI darf weder den höchsten Konfidenzwert zum Sieger machen noch eine der drei Organisationen visuell als Standard-CTA hervorheben. Jede Nennung erhält identische Hierarchie und ihren eigenen direkten Link. Die Zählmaschine zeigt „keine zwei gleichen Nennungen“ als regulären Ruhezustand, nicht als Warnung oder leeren Fehlerzustand.

Säulen B, C und D dieser Sitzung haben Konsens (3/3, 2/3, 2/3). Ein Sitzungslabel „Nicht-Konsensfall“ darf daher nicht suggerieren, die gesamte Sitzung sei ohne Empfehlungen; der Zustand ist säulenweise.

## 14. Sichtbare Meinungsänderungen

Deterministische Regel: Für jede Kombination aus Modell und Säule wird die `organization_id` des `initial_vote` mit der des `final_vote` verglichen. Bei Unterschied wird zuerst das alte Votum sichtbar durchgestrichen und danach das neue Votum gezeigt. Titel- oder Konfidenzänderungen bei gleicher Organisation können zusätzlich als Detail erscheinen, sind aber keine Organisationsänderung.

Verifizierte Änderungen:

| Sitzung | Modell | Säule | Erstvotum → Schlussvotum |
|---|---|---|---|
| `2026-07c` | GPT | A | TaRL Africa → Helen Keller International |
| `2026-07c` | GPT | D | GRSP → LEEP |
| `2026-07c` | Gemini Pro | A | TaRL Africa → Helen Keller International |
| `2026-07` | GPT | D | Pure Earth → LEEP |
| `2026-07` | Gemini Pro | B | AMF → Malaria Consortium |
| `2026-07` | Gemini Pro | C | NTI → GovAI |

Die bestehende SvelteKit-App zeigt diese Änderungen nicht vergleichend; sie veröffentlicht beide Runden nur in getrennten `<details>`. Der SOL-Renderer besitzt bereits `pillar_revisions()` als brauchbare Referenz. Die neue Komponente sollte kein abgeleitetes Änderungsfeld persistieren, sondern den Vergleich beim Build deterministisch erzeugen.

Fehlende Erst- oder Schlussstimme muss als „kein vergleichbares Votum publiziert“ sichtbar bleiben. `unresolved_votes` darf nicht als unveränderte Stimme behandelt werden.

## 15. Festgestellte Lücken im Datenvertrag

1. Es gibt keine strukturierte Kurzbegründung pro Empfehlung/Modell. `content_md` ist vollständig, `rationale_md` Boilerplate, `beschreibung` beschreibt nur die Organisation.
2. Quellen sind nicht als einheitliche strukturierte Liste pro Behauptung/Empfehlung definiert. Wart-Dossiers und Modellprosa können Links enthalten, aber eine belastbare Quellenkarte kann daraus nicht ohne Prosa-/HTML-Extraktion entstehen.
3. `schema_version` blieb 2 trotz Formänderungen; `additionalProperties: true` und fehlende Laufzeitvalidierung verringern die Schutzwirkung.
4. Das Schema wird als „Charakterisierung, nicht im Code erzwungen“ beschrieben. Die produktive Site validiert Daten vor dem Rendern nicht.
5. `dissent_highlights` ist Array oder String.
6. Markdownvertrauen und erlaubtes HTML sind nicht im Datenvertrag festgelegt.
7. `correction_notice.text` ist semantisch Markdown, aber im Schema nur `string` ohne Formatkennzeichnung.
8. Registry-URLs können vorhanden, aber unverifiziert sein; gewünschte öffentliche Kennzeichnung ist nicht definiert.
9. Es gibt kein kanonisches Homepage-/Archivindex-Dokument. Die Site leitet es korrekt aus Ordnern ab, aber ein Buildzeit-View-Model fehlt.
10. Es gibt keinen strukturierten `change_reason`; sichtbar ist zuverlässig nur die geänderte Organisation. Die Begründung fürs Umdenken bleibt im Schlussvotum-Volltext.
11. Es gibt keine explizite Ergebnisgesamtlage; Konsens ist je Säule herzuleiten.
12. Es gibt kein Asset-/Provenienzmanifest im produktiven `site/static/`.

Diese Lücken sind zu dokumentieren, nicht im Frontend mit erfundenen Texten zu füllen. Eine spätere Datenvertragsänderung liegt außerhalb dieser Präsentationsphase und der geschützten Pfade.

## 16. Empfohlene Seitenarchitektur

Desktop sollte als eine zusammenhängende, viewportfüllende Ratssaal-Bühne mit semantischem Dokument darunter/innerhalb derselben DOM-Struktur gebaut werden. Keine acht autonomen Vollbreitensektionen, sondern fünf dramaturgische Akte:

1. **Eintritt / Was und Warum:** Leitfrage, Kernaussage, vier Wirkungsräume, Transparenzsatz und knappe Ursprungsgeschichte. Der Ratssaal ist zunächst weit und dunkel; Text sitzt auf einer echten architektonischen Fläche, nicht auf einer schwarzen Karte.
2. **Heutige Beratung / Ergebnis:** Kamera senkt sich zur Mitte; vier gleichrangige Ergebnisregister werden als Messing-/Papiermechanik am Raumrand zugänglich. Direkte Links sind sofort vorhanden. Dies erfüllt den wichtigsten Informationsbedarf vor Prozessdramaturgie.
3. **Vorbereitung und getrennte Stimmen:** räumlicher Fokus wechselt durch die Tür ins Vorzimmer (Belege/Wart), dann zurück zu drei Pulten. Frage und Recherche können zu einem Akt zusammengelegt werden; erste Stimmen erscheinen pultbezogen.
4. **Gegenlesen und Zählen:** Lichtlinien verbinden Pulte; geänderte Voten bleiben durchgestrichen; anschließend fokussiert die mechanische Mitte. Gegenlesen und Maschine gehören in einen kontinuierlichen Zustandswechsel, bleiben semantisch aber getrennte Schritte.
5. **Veröffentlichung / Archiv:** Die Maschine prägt das Ergebnisprotokoll; die monumentale Tür führt zu vollständiger Sitzung und früheren Sitzungen. Kosten, Korrektur und vollständiger Dissens bleiben erreichbar.

Die aktuelle Empfehlung steht früh, nicht erst nach einer langen Prozessinszenierung. Der vollständige Inhalt bleibt in normaler DOM-Reihenfolge; die Bühne ändert lediglich räumlichen Fokus und Sichtbarkeit.

## 17. Empfohlene Komponentenarchitektur

```text
+page.server.js
  └─ buildHomepageViewModel(session, registry, sessions, schedule)
       ├─ currentSession
       ├─ recommendations[] (registry-resolved)
       ├─ modelTracks[] (initial/final/change)
       ├─ dissent/correction/costs
       └─ archive[]

+page.svelte
  ├─ HomeIntro
  ├─ CouncilStage
  │   ├─ ScenePlate
  │   ├─ StageNavigation
  │   ├─ RecommendationLedger
  │   ├─ ModelLectern × 3
  │   ├─ RevisionMark
  │   └─ CountingMachine
  ├─ Antechamber
  ├─ ProtocolDisclosure
  └─ ArchiveDoor
```

Empfohlene Trennung:

- reine Serverfunktionen für Registry-Map, Validierung, neueste Sitzung, Revisionsvergleich und View-Model;
- semantische Inhaltskomponenten, die ohne JS vollständig rendern;
- ein einzelner optionaler `CouncilStageController` für IntersectionObserver, Fokus und CSS-Custom-Properties;
- keine Datenlogik in Animationskomponenten;
- Ergebnisdarstellung als gemeinsame Primitive für Homepage, Mobile und später Sitzungsroute, nicht als visueller Kartenmonolith;
- Markdown-Renderer/Policy zentralisieren.

## 18. Szenen- und Zustandsmodell

Empfohlene endliche Zustände:

| Zustand | Raum/Kamera | Primärer Inhalt | Übergang |
|---|---|---|---|
| `arrival` | weiter Ratssaal, Tür-/Raumtiefe | Was, Warum, Ursprung | langsame Annäherung |
| `recommendations` | Mitte und vier Register | aktuelle Ergebnisse/Links | Fokus fährt vom Text zur Maschine |
| `question` | Mitte/Schiefertafel | Sitzungsfrage und Regel | Tür öffnet zum Vorzimmer |
| `evidence` | Vorzimmer | Belege, Späher, Wart, Dossierlink | Rückkehr durch Tür |
| `initial` | alle drei Pulte gleich hell | getrennte Erstvoten | nacheinander fokussierbar, nicht hierarchisch |
| `review` | Lichtwege zwischen Pulten | Schlussvoten und Revisionen | alte Voten bleiben sichtbar |
| `count` | mechanische Mitte | reine Nennungszählung | Zahnräder/Marken nur dekorativ |
| `publish` | geprägtes Protokoll/Tür | Ergebnis, Kosten, Korrektur, Archiv | normale Navigation |

`question` und `evidence` können als ein Scrollakt mit internem Raumwechsel umgesetzt werden. `review` und `count` dürfen visuell fließend übergehen, aber die Zählregel muss als eigenständiger Fokuszustand erkennbar bleiben. Zustände werden aus Scrollposition abgeleitet und niemals als einzige Quelle für Inhaltszugänglichkeit verwendet.

## 19. Scroll-, Fokus- und Tastaturmodell

- Desktop: sticky Bühne (`position: sticky; min-height: 100svh`) neben/über einer semantischen Folge kurzer „Cue“-Abschnitte. IntersectionObserver setzt nur `data-scene`; CSS interpoliert Opazität, Transform und Licht.
- Keine Scrolljacking-Logik, kein erzwungenes `preventDefault`, keine künstliche Scrollgeschwindigkeit und kein Canvas-only-Inhalt.
- Eine stets erreichbare Szenennavigation listet die fünf Akte, nicht alle Mikroanimationen. Anker aktualisieren URL-Hash optional per `history.replaceState`.
- Tab-Reihenfolge folgt der Dokumentreihenfolge, nicht der visuellen Pultposition. Dekorative Hotspots sind nicht zusätzlich fokussierbar, wenn dieselbe Aktion bereits einen Textlink besitzt.
- Für die drei Pulte eignet sich ein zugängliches Tablist-Muster nur dann, wenn dadurch Inhalte wirklich alternativ gezeigt werden. Ohne JS bleiben alle drei Pultartikel sichtbar. Pfeil links/rechts, Home/End und korrekte `aria-selected`-Zustände können aus `sol-build/app.js` übernommen werden.
- Bei Fokus auf verborgenem/überblendeten Inhalt wird die passende Szene sofort aktiviert und der Inhalt ohne Übergangsverzögerung sichtbar.
- Skiplinks: „Zu den Empfehlungen“, „Zum Verfahren“, „Zum vollständigen Protokoll“.
- Browser-Zurück, Hash-Direktaufruf und Reload müssen denselben semantischen Zielpunkt erreichen.

## 20. Eigenständiges mobiles Konzept

Mobil wird kein verkleinerter Ratssaal verwendet. Vorgeschlagen ist ein **Sitzungsbuch mit Raumfenstern**:

1. kompakter Header mit Leitfrage und zwei direkten Sprüngen: „Empfehlungen“ und „So wird gezählt“;
2. Ergebnisregister als vier horizontale Kapitel, je Säule sofort mit Organisation, Beschreibung, Stimmenstatus und direktem Link; Nicht-Konsens klappt drei gleichrangige Voten untereinander auf, ohne vorausgewählten Sieger;
3. ein breites, niedriges Ratssaal-Fenster als atmosphärischer Trenner, dessen Bildausschnitt per `object-position` bewusst komponiert wird;
4. drei Pult-Kapitel in konsistenter Reihenfolge Anthropic/OpenAI/Google, jeweils Erstvotum → sichtbare Änderung → Schlussvotum;
5. Vorzimmer als separates Bildfenster mit Belege-/Dossierzugang;
6. Zählregel als taktile, rein mit CSS gezeichnete Messingmarken und Klartext;
7. Archiv als große Türzeile und normale Linkliste.

Keine sticky 100-vh-Kamera auf kleinen Displays; mobile Browserleisten, Zoom und Bildschirmtastatur würden sie fragil machen. Atmosphärische Bilder sind optional, Text bleibt sofort da. Animation beschränkt sich auf kurze Offenblendungen und Details-Pfeile. Empfehlungslinks müssen ohne Aufklappen auffindbar sein; bei Nicht-Konsens sind alle drei Links mit gleicher Gewichtung sichtbar.

## 21. Progressive Enhancement und Fallback

Der robuste Grundzustand wird direkt als prerendered HTML aus `+page.server.js` und Svelte erzeugt. In der initialen HTML-Ausgabe stehen:

- alle Empfehlungen und abweichenden Einzelvoten;
- Registry-Beschreibungen und direkte Links bzw. expliziter Null-Fall;
- Erst- und Schlussvoten sowie durch `<del>` markierte alte Organisationsvoten;
- Modelllabel, konditionale Stimmen und Reservations;
- Frage, Kosten, Korrektur, Dissens, Dossier-/Quellenzugänge;
- Link zum vollständigen Sitzungsprotokoll und Archiv.

CSS liefert den normalen linearen Inhalt zuerst. Nur unter einer Enhancement-Klasse, die nach erfolgreicher Controller-Initialisierung gesetzt wird, werden Desktop-Cues zu einer sticky Szene überlagert. Ohne JS gibt es keine versteckten Panels. Native `<details>` sind für lange Rohtexte geeignet und funktionieren ohne JS. Bilder nutzen `alt` je nach Rolle; dekorative Wiederholungen bleiben leer.

Hydration darf keine Wahrheit berechnen. Der Client kennt nur Szenen-IDs, nicht Aggregationsregeln. Damit sind Grundzustand und Bühne ein Produkt und dieselbe DOM-Wahrheit.

## 22. Assetstrategie

- Die beiden Original-PNGs unverändert und mit C2PA in `site/static/media/provenance/` übernehmen. Hash und Dateigröße dokumentieren.
- Für produktive Auslieferung responsive Varianten (z. B. 640/960/1280/1672 bzw. 1915 px) erstellen, aber erst mit einem verifizierten C2PA-erhaltenden Prozess. Vor und nach Transformation mit `c2patool` prüfen; Original immer verlinkbar behalten.
- Keine neuen KI-Bilder in der ersten Implementierungsstufe: Die vorhandenen Plates tragen Ratssaal, Vorzimmer und Tür bereits. Zusätzliche Mechanik als semantisch dekorative CSS/SVG-Ebene bauen, sofern sie nicht fälschlich fotografische Authentizität suggeriert.
- Die leere Tafel eignet sich für HTML-Text mit perspektivisch zurückhaltender Positionierung; auf kleinen Viewports nicht in das Bild zwingen.
- Ratssaal nicht mehrfach als Vollbild laden. Ein Bild kann innerhalb der sticky Bühne wiederverwendet werden; mobile Variante mit `picture` und passendem Crop.
- CSS-Verläufe, Vignetten und Lichtmasken dürfen Atmosphäre ergänzen, aber keine opaken Kartenwand erzeugen.
- Provenienztext und Original-Link im Impressum/Assethinweis erwägen.

## 23. Animationstechnik

Empfohlen sind CSS-Transforms/Opacity/Filter, gesteuert über wenige Custom Properties und eine kleine Svelte-Action bzw. Controller-Komponente. IntersectionObserver aktiviert diskrete Szenenzustände; optional kann `ScrollTimeline` als progressive Kür für kontinuierliche Licht-/Kamerabewegung verwendet werden, mit Observer-Fallback.

Technische Leitplanken:

- nur `transform` und `opacity` für große Ebenen; keine permanent animierten Layout-Eigenschaften;
- maximal zwei bis drei große Compositing-Layer; `will-change` nur während aktiver Übergänge;
- Kameraillusion durch 2D-Scale/Translate und Masken statt WebGL/Three.js;
- Pultlicht als CSS-Radialgradient, Zählmarken als inline SVG/CSS; keine Canvas-Wahrheit;
- Zustandswechsel 350–700 ms, ruhig und mechanisch, nicht federnd;
- keine neue Laufzeitabhängigkeit notwendig;
- Übergänge erst nach Bilddekodierung aktivieren, um Sprünge zu vermeiden.

WebGL wäre angesichts zweier gemalter Plates, statischem Adapter und Accessibility-Anforderung unverhältnismäßig. Es erhöht Bundle, Energieverbrauch und Fallbackkomplexität, ohne zusätzliche Informationsqualität.

## 24. Verhalten bei `prefers-reduced-motion`

Bei `prefers-reduced-motion: reduce`:

- keine Scroll-gebundene Kamera, Parallaxe, Lichtwanderung oder Zahnradrotation;
- Szenenzustände wechseln sofort bzw. mit höchstens kurzer Opazitätsänderung;
- sticky Bühne darf zu normalem Dokumentfluss werden, wenn Fokus-/Lesereihenfolge sonst irritiert;
- `scroll-behavior: auto` statt smooth;
- alte/neue Voten bleiben durch Typografie, `<del>` und Textlabel verständlich;
- keine Information darf nur über Bewegung oder zeitliche Reihenfolge vermittelt werden.

Die Media Query muss in Komponenten-/globalen Tests abgedeckt werden. Ein manueller Test auf macOS/iOS und Windows ist erforderlich.

## 25. Barrierefreiheit

- Ein einziges klares `<h1>` mit der Leitfrage; logische Überschriften unabhängig von Szenen.
- Landmarken und Skiplinks; aktuelle Szenennavigation mit `aria-current`, nicht mit Live-Region-Spam.
- Kontrast der Messingtexte gegen dunkles Holz mindestens WCAG AA; atmosphärische Schatten nicht als Kontrastgrundlage.
- Textzoom bis 200 %, Reflow bei 320 CSS px, keine abgeschnittenen sticky Texte.
- Touchziele mindestens 44 × 44 CSS px; sichtbare `:focus-visible`-Ringe in Mondblau/Messing.
- Konsenszustand als Text („2 von 3“), nicht nur Punkte/Farbe. Konditionalität und Nicht-Konsens ebenfalls sprachlich.
- Konfidenz nicht als Qualitätsrangfolge inszenieren; SVG-Bar braucht zugänglichen Text und Nullbehandlung.
- Durchstreichung zusätzlich mit „Erstvotum“/„geändert zu“ beschriften.
- Externe Spendenlinks als solche kennzeichnen; kein ungefragtes neues Fenster.
- Lange Markdown-Codeblöcke scrollbar, Tabellen responsiv, Links nicht nur farblich kenntlich.
- Bild-Alttexte nur bei inhaltlicher Rolle; dieselbe Plate bei dekorativer Wiederholung mit `alt=""`.
- Die drei Modelle gleichrangig in DOM, Fläche, Kontrast und Fokusbehandlung.

## 26. Performance und Bildoptimierung

Der aktuelle SvelteKit-Build ist nur ca. 1,7 MB, enthält aber die Plates noch nicht. Zwei unoptimierte Bilder würden die initiale Last um rund 4 MB erhöhen.

Budgetvorschlag:

- mobiles initiales Bild ≤ 180 KB, Desktop-Ratssaal ≤ 450 KB; Vorzimmer lazy ≤ 350 KB; C2PA-Originale nicht initial laden;
- LCP-Plate mit `fetchpriority="high"`, korrektem `width`/`height` und responsive `srcset`;
- Vorzimmer `loading="lazy"`, `decoding="async"`;
- kritisches CSS klein, keine externen Fonts, keine Tracker/CDNs;
- Szenen-JS zielwertig < 15 KB gzip zusätzlich;
- kein doppeltes Plate-Download durch unterschiedliche URLs für dieselbe Auflösung;
- lange Protokolltexte sind HTML-lastig; Volltexte auf der Homepage nur in kompakten, aber vorhandenen `<details>` bzw. über die statische Sitzungsroute. Das vollständige Protokoll bleibt mit einem normalen Link erreichbar.

Prüfen mit Lighthouse/WebPageTest lokal bzw. CI, Slow 4G, mobilem Safari, deaktiviertem Cache und JS. CLS muss durch Bildmaße praktisch null bleiben.

## 27. Teststrategie

1. **Daten-/Unit-Tests:** neueste Sitzung nach `number`; Registryauflösung; unbekannte/fehlende ID; URL nur aus Registry; Null-URL; `dissent_highlights` String/Array; Runden ohne Votes; Revisionsvergleich; konditionale Stimme.
2. **Golden-Rendering:** `2026-07c` zeigt vier Konsensresultate und A als konditional; `2026-07` zeigt A mit drei gleichwertigen Voten und drei Links; alte Voten sind in beiden Referenzfällen sichtbar.
3. **Buildtests:** `npm ci && npm run build`; prüfen, dass `/`, alle Sitzungen und Assets in `site/build/` existieren und keine unbekannten Registry-IDs vorliegen.
4. **No-JS-Test:** gebaute HTML-Datei ohne Hydration prüfen: Organisationen, Stimmen, Änderungen, Kosten, Dissenszugang und Links vorhanden.
5. **Komponententests:** sobald bestehende Toolchain ergänzt/freigegeben ist; keine neue Dependency in dieser Phase.
6. **E2E/A11y:** Tastatur, Hashnavigation, Fokus bei Szenenwechsel, reduced motion, 200-%-Zoom, 320-px-Reflow, Kontrast und Semantik.
7. **Visual Regression:** Desktop 1440/1024, Mobile 390/320, Light-/forced-colors soweit relevant, JS aus/reduced motion.
8. **Performance:** Bildbudget, LCP, CLS, Long Tasks; C2PA-Verifikation der Originale und Derivate.
9. **Bestehende Backend-Golden-Tests:** beibehalten, da sie die Wahrheit des Frontends absichern; aktuell lokal mangels pytest nicht ausführbar.

Vor Implementierung sollte die Site eine minimale Qualitäts-Toolchain mit `check`, `lint` und `test` erhalten; das ist eine explizite spätere Änderung, nicht Teil dieser Analyse.

### Ausgeführte technische Prüfungen

| Befehl | Exit | Tatsächliches Ergebnis |
|---|---:|---|
| `cd site && npm ci` | 0 | 52 lockfile-definierte Pakete installiert; keine neuen Abhängigkeiten gewählt |
| `cd site && npm run build` | 0 | Vite/SvelteKit erfolgreich; adapter-static schrieb `site/build/`; ca. 1,7 MB |
| `cd site && npm run check` | 1 | Script `check` fehlt |
| `cd site && npm run lint` | 1 | Script `lint` fehlt |
| `cd site && npm test` | 1 | Script `test` fehlt |
| `cd site && npm run` | 0 | nur `prebuild`, `dev`, `build`, `preview` vorhanden |
| `python3 -m pytest -q` | 1 | `/opt/homebrew/opt/python@3.14` hat kein Modul `pytest`; nichts nachinstalliert |
| Python-Schema-Validierung mit `jsonschema` | 1 | Modul `jsonschema` fehlt; nichts nachinstalliert |

Buildwarnungen (Build blieb erfolgreich):

- `site/src/routes/sessions/[id]/+page.svelte`: `data` wird nur initial erfasst.
- `site/src/routes/+page.svelte`: `data` wird für `latestRecs` nur initial erfasst.
- `site/src/routes/journal/[id]/+page.svelte`: `data` wird nur initial erfasst.
- `site/src/lib/components/ConfidenceBar.svelte`: `confidence` wird für `pct` und `barWidth` nur initial erfasst (zwei Warnungen).

Der Build erzeugte unter anderem `site/build/index.html`, statische Seiten für alle drei Sitzungen sowie alle Journal-/Dokumentrouten. `prebuild` kopierte `schedule.json`; dessen Inhalt blieb laut Git-Diff unverändert. Keine produktive Datei wurde in dieser Phase geändert.

## 28. Konkreter Implementierungsplan

1. Qualitätsbaseline schaffen: Svelte-Check/Lint/Testskripte mit bereits freigegebener Toolchain festlegen; bestehende Reaktivitätswarnungen beseitigen.
2. Homepage-View-Model in `site/src/lib/server/` implementieren: Registry laden, IDs strikt auflösen, Referenzdaten normalisieren, Erst-/Schlussvoten paaren, Revisionen ableiten.
3. Unit-/Golden-Tests für `2026-07c` und `2026-07` vor der visuellen Arbeit schreiben.
4. Assets mit intakter C2PA-Provenienz in `site/static/` integrieren; responsive Pipeline verifizieren und dokumentieren.
5. Layout um einen bewusst vollbreiten Homepage-Modus erweitern, Dokumentrouten visuell unverändert halten.
6. Semantischen No-JS-Grundzustand der neuen Homepage bauen: Intro, Ergebnisregister, Verfahren, drei Modellspalten, Revisionen, Maschine, Veröffentlichung/Archiv.
7. Eigenständige Mobile-CSS-/Komponentenkomposition zuerst bis 320 px und 200 % Zoom fertigstellen.
8. Desktop-Ratssaalbühne als progressive Schicht hinzufügen; diskrete Zustände und Ankernavigation implementieren.
9. Fokus-, Tastatur-, Hash- und Reduced-Motion-Verhalten ergänzen.
10. Markdownpolicy zentralisieren; Korrektur/Dissens/Codeblöcke sicher und faltbar rendern.
11. Sitzungsdetailroute an gemeinsame Org-/Revision-Primitives anbinden, damit Homepage und Vollprotokoll nicht divergieren.
12. Build, No-JS, Daten-Goldens, Accessibility, Visual Regression und Performancebudgets ausführen.
13. Review ausschließlich aus `site/build/` bzw. `npm run preview`; PR-Check belegt, dass genau der Workflowpfad deployt.

## 29. Risiken und offene Entscheidungen

- **Kurze Begründung fehlt strukturiert:** Registrybeschreibung ist kein „Warum“. Entscheidung nötig, ob Homepage nur Beschreibung + Stimmen + Link zum Schlussvotum zeigt oder lange Modellbegründungen inline faltet.
- **Quellenmodell fehlt:** „Belege“ kann auf Dossier und Volltexte verweisen; einzelne Quellen dürfen nicht künstlich Empfehlungen zugeordnet werden.
- **C2PA-Optimierung:** Werkzeug/CI-Schritt muss Provenienz nachweislich erhalten. Bis dahin Performance-Trade-off oder Original nur als Provenienzdownload.
- **Globales Layout:** vollbreite Homepage vs. schmale Dokumentseiten verlangt eine saubere Routenausnahme.
- **Aktuelle Sitzung vollständig konsensual:** Nicht-Konsens muss dennoch anhand `2026-07` getestet und im Archiv deutlich erfahrbar sein, ohne falschen aktuellen Zustand zu inszenieren.
- **Korrekturwidersprüche:** `summary`/`dissent_md` können dem Ergebnis widersprechen; Korrektur muss vor diesen Texten sichtbar sein.
- **Markdown-XSS-Vertrag:** committed content ist vertrauenswürdig behandelt, aber erlaubtes HTML ist nicht formalisiert.
- **Unverifizierte Spendenlinks:** sieben Registryeinträge ohne Prüfdatum; UI-Policy dazu ist offen.
- **Rsync ohne `--delete`:** alte Produktionsdateien bleiben potenziell erhalten.
- **Browserunterstützung:** ScrollTimeline darf nur Kür sein; Safari-/Firefox-Fallback ist Pflicht.
- **Hero-Fokus:** keine einzelne Organisation als globaler „Sieger“ hervorheben. Vier Säulen sind eigenständige Beratungsbereiche.
- **Ursprungstext:** knappe Formulierung zur beendeten Spende nach Skandal braucht redaktionelle Freigabe; keine Gründerinszenierung.
- **Terminologie:** vorgegebene Aussagen dürfen typografisch, nicht inhaltlich verändert werden. „KI-Modell“ und vier Bereiche sollten im Erstkontakt alltagssprachlich bleiben.

## 30. Vollständige Liste der später zu ändernden oder neu anzulegenden Dateien

Die genaue Granularität kann beim Implementieren leicht variieren; folgende Liste deckt den empfohlenen produktiven Pfad vollständig ab.

**Zu ändern**

- `site/package.json` — Qualitäts-/Testskripte, nur nach Freigabe der benötigten bestehenden/neuen Dev-Tools.
- `site/package-lock.json` — nur falls freigegebene Dev-Abhängigkeiten ergänzt werden.
- `site/src/routes/+layout.svelte` — vollbreiter Homepage-Modus, Skiplinks, globale Tokens ohne Dokumentroutenbruch.
- `site/src/routes/+page.server.js` — vollständiges Homepage-View-Model statt gekürzter Empfehlungsliste.
- `site/src/routes/+page.svelte` — neue semantische Homepage und progressive Bühne.
- `site/src/lib/server/content.js` — Registryladen, normalisierte Markdownpolicy und/oder gemeinsame Datenhelfer.
- `site/src/routes/sessions/[id]/+page.server.js` — gemeinsame Registry-/Revisionsprojektion.
- `site/src/routes/sessions/[id]/+page.svelte` — sichtbare Änderungen, Korrektur-Markdown, gemeinsame Ergebnisprimitive.
- `site/src/lib/components/ResultCard.svelte` — entweder auf gemeinsame Ergebnisprimitive reduzieren oder nach Migration entfernen; nicht parallel divergieren lassen.
- `site/README.md` — neue Architektur, Assets, Tests, No-JS und Reviewpfad dokumentieren.
- `.github/workflows/deploy.yml` — optional erst nach Entscheidung: Qualitätschecks/C2PA-Prüfung vor Build; Deploypfad selbst bleibt gleich.

**Neu anzulegen**

- `site/src/lib/server/homepage.js` — View-Model, Registryauflösung und Revisionsableitung.
- `site/src/lib/server/homepage.test.js` — Konsens-/Nicht-Konsens-/Identitäts-Goldens.
- `site/src/lib/server/markdown.js` — zentraler Markdownvertrag/Renderer, sofern nicht in `content.js` belassen.
- `site/src/lib/components/home/HomeIntro.svelte`
- `site/src/lib/components/home/CouncilStage.svelte`
- `site/src/lib/components/home/StageNavigation.svelte`
- `site/src/lib/components/home/RecommendationLedger.svelte`
- `site/src/lib/components/home/RecommendationEntry.svelte`
- `site/src/lib/components/home/ModelLectern.svelte`
- `site/src/lib/components/home/RevisionMark.svelte`
- `site/src/lib/components/home/CountingMachine.svelte`
- `site/src/lib/components/home/Antechamber.svelte`
- `site/src/lib/components/home/ProtocolDisclosure.svelte`
- `site/src/lib/components/home/ArchiveDoor.svelte`
- `site/src/lib/components/home/CouncilStageController.svelte` oder eine gleichwertige kleine Action.
- `site/src/lib/components/home/home.css` — nur falls Styles nicht komponentennah bleiben.
- `site/static/media/provenance/ratssaal.png` — unverändertes C2PA-Original.
- `site/static/media/provenance/vorraum.png` — unverändertes C2PA-Original.
- `site/static/media/ratssaal-*.png|webp|avif` — responsive Derivate nur nach C2PA-Entscheidung.
- `site/static/media/vorraum-*.png|webp|avif` — responsive Derivate nur nach C2PA-Entscheidung.
- `site/static/media/ASSETS.md` — Herkunft, Hashes, Transformation und C2PA-Prüfung.
- `site/tests/homepage-render.test.*` — statische HTML-/No-JS-Goldens.
- `site/tests/homepage.e2e.*` — nur wenn eine E2E-Toolchain freigegeben wird.

**Nicht zu ändern**

- `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`, `schema/**` in dieser Präsentationsarbeit.
- `sol-build/` während der Integration, außer ein später ausdrücklich freigegebener Archiv-/Cleanup-Schritt.
- kein neuer Prototyp- oder Buildordner außerhalb von `site/`.

---

**Terminal-Kurzfassung**

- Bericht erstellt: `docs/codex-analysis.md`
- Prüfungen: `npm ci` und produktiver SvelteKit-Build erfolgreich; Check/Lint/Frontendtests nicht konfiguriert; Python-Tests/Schema-Validierung wegen fehlender installierter Module nicht ausführbar
- Deploymentpfad: `site/build/` → `/srv/noblecause/` → Caddy
- wichtigste Datenrisiken: Boilerplate in `rationale_md`, Markdown/JSON in Dissens/Korrektur, Registrypflicht für Identität/URL, fehlende strukturierte Kurzbegründungen/Quellen, korrigierte Aggregation kann Summary/Dissens widersprechen
- keine Implementierung vorgenommen
