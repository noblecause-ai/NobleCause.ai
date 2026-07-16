# NobleCause.ai — Buildbericht der immersiven Startseite

Stand: 15. Juli 2026  
Branch: `feat/immersive-homepage`  
Produktiver Pfad: `site/`

## 1. Umgesetzte Designidee

Die Startseite ist als „Ratssaal als lebende Maschine“ direkt in der produktiven
SvelteKit-App umgesetzt. Ein Ratssaal-Plate bildet die durchgehende räumliche Bühne.
Semantische Akte führen von Was/Warum über vier gleichrangige Ergebnisregister, Frage und
Vorzimmer, drei Modellpulte, sichtbare Revisionen und die mechanische Zählmitte bis zum
veröffentlichten Protokoll und der Archivtür.

Auf großen Viewports aktiviert JavaScript eine feste Bühne, diskrete Szenenfokusse,
Pult-/Maschinenlicht und eine Akt-Navigation. Es gibt kein Scrolljacking. Auf kleineren
Viewports bleibt die Seite ein lineares Sitzungsbuch mit gezielt beschnittenen
Raumfenstern. Papier, Schiefer, Messing, Holz und Stein ersetzen Dashboardkarten.

## 2. Geänderte und neue Dateien

Geändert:

- `site/package.json`
- `site/README.md`
- `site/src/lib/server/content.js`
- `site/src/routes/+page.server.js`
- `site/src/routes/+page.svelte`
- `site/src/routes/sessions/[id]/+page.server.js`
- `site/src/routes/sessions/[id]/+page.svelte`
- `site/src/routes/journal/[id]/+page.svelte`
- `site/src/lib/components/ConfidenceBar.svelte`

Neu:

- `site/src/lib/server/homepage.js`
- `site/src/lib/server/homepage.test.js`
- `site/tests/homepage-build.test.js`
- `site/static/media/ASSETS.md`
- `site/static/media/provenance/ratssaal.png`
- `site/static/media/provenance/vorraum.png`
- `docs/codex-build-report.md`
- `docs/review/home-desktop.png`
- `docs/review/home-mobile.png`
- `docs/review/home-nojs.png`

Die kleinen Änderungen an Journal und `ConfidenceBar` beseitigen bereits vorhandene
Svelte-5-Reaktivitätswarnungen. Geschützte Daten-, Schema-, Journal- und Backendpfade
wurden nicht verändert.

## 3. Tatsächlicher Datenfluss

`+page.server.js` liest zur Buildzeit die nach `number` jüngste Sitzung, alle
Archivsitzungen und `organizations.json`. `homepage.js` erzeugt daraus das View-Model:

- `currentSession`
- `recommendations`
- `modelTracks`
- `revisions`
- `correction`
- `dissent`
- `costs`
- `archive`

Organisationen werden ausschließlich über `organization_id` gegen eine Registry-Map
aufgelöst. Name, neutrale Beschreibung und Spendenlink stammen aus dem Registryeintrag.
Ein unbekannter oder widersprüchlicher Eintrag sowie `unresolved_votes` brechen den Build
explizit ab. `rationale_md` wird nicht verwendet. Runden werden über `kind` gefunden und
fehlende `votes` toleriert. Markdown für vollständige Voten, Dissens und Korrektur wird
mit der bestehenden Buildzeit-Pipeline gerendert.

## 4. Konsens und Nicht-Konsens

Der aktuelle Fall `2026-07c` zeigt vier gleichrangige Bereiche. Säule A zeigt 3 von 3 und
den tatsächlichen konditionalen Vorbehalt; Säule B zeigt korrekt 2 von 3. Die UI bestimmt
keinen globalen Sieger.

Die gemeinsame Ergebnisprimitive unterstützt den Nicht-Konsensfall aus `2026-07`:
Säule A enthält drei gleich große Einzelvoten mit Modellattribution und je eigenem
Registrylink. Kein Konfidenzwert erzeugt eine visuelle Rangfolge. Der Fall wird durch einen
Golden-Test gegen die echte Sitzung abgesichert und im Archiv säulenweise bezeichnet.

## 5. Revisionsdarstellung

Pro Modell und Säule vergleicht die Buildzeitlogik `initial_vote` und `final_vote` über
`organization_id`. Bei einer Änderung bleibt die erste Organisation in `<del>` sichtbar;
„Erstvotum“ und „Geändert zu“ erklären den Zustand zusätzlich. Gründe werden nicht
erfunden. Die vollständigen publizierten Erst- und Schlussvoten stehen in nativen
`<details>`.

## 6. No-JS-Verhalten

Die komplette inhaltliche Fassung wird statisch in `site/build/index.html` gerendert:
Leitfrage, Erklärung, alle Empfehlungen und Links, Modellvoten, Revisionen, Kosten,
Korrektur, Dissenszugang, Vollprotokoll und Archiv. Erst `onMount` setzt
`home-enhanced`; der Client berechnet keine fachlichen Daten. Ohne JavaScript bleibt die
lineare Seite vollständig, einschließlich Ratssaal- und Vorzimmerbild.

Der HTML-Goldentest verifiziert zentrale Organisationen, Stimmenzahlen, Mechanismussätze,
Kosten, Protokolllink, Registrylink und das durchgestrichene TaRL-Erstvotum direkt in der
gebauten Datei.

## 7. Mobiles Verhalten

Unter 70 rem wird die feste Bühne deaktiviert. Ergebnisse und Modellpulte stehen
untereinander. Unter 44 rem werden Ergebnisaktionen vollbreit, Nicht-Konsens-Voten
einspaltig, das Vorzimmer zu Bildfenster plus normaler Textfläche und die Maschine zu
einer einspaltigen Komposition. Es gibt keine `100vh`-Sticky-Kamera auf Mobilgeräten.
Touchziele der zentralen Links und Navigation sind mindestens 44 CSS px hoch.

Die CSS-Fälle für 390/320 px und Reduced Motion sind implementiert. Die lokal unter
`~/.folio-tools` vorhandene Playwright-Installation wurde mit einem echten 390 × 844
Viewport verwendet. Gemessen wurden `innerWidth: 390` und `scrollWidth: 390`; es besteht
kein horizontaler Überlauf. Desktop, Mobile und eine No-JS-/Reduced-Motion-Fassung sind
unter `docs/review/` dokumentiert.

## 8. Accessibility-Entscheidungen

- ein H1 mit der Leitfrage und logische H2/H3-Struktur;
- Skiplinks zu Empfehlungen und Verfahren;
- normale DOM- und Tab-Reihenfolge;
- Text für 2/3, 3/3, Vorbehalt und fehlenden Konsens;
- `<del>` plus sprachliche Änderungslabels;
- keine fachliche Information ausschließlich in Licht/Bewegung;
- sichtbare Links und native `<details>`;
- feste Bilddimensionen und sinnvolle/dekorative Alttexte;
- scrollbar formatierte Markdown-Codeblöcke;
- `prefers-reduced-motion` deaktiviert fixed Bühne, Übergänge und smooth scroll;
- `forced-colors`-Rahmen für wesentliche Oberflächen;
- keine ungefragt neuen Tabs.

## 9. Assets und Provenienz

Die Originalbytes aus `sol-build/site/static/` wurden unverändert nach
`site/static/media/provenance/` kopiert. SHA-256 der Quelle und Kopie stimmen:

- Ratssaal: `b19282508301fe946b1f025e3bc43c6318fb5ed2c3fa546850b64ee13a2fbbbd`
- Vorzimmer: `0e02cc4dfa508dc9d29e71325442fc8bbf3ad2b4903a2b0d9a74388cf2d79b56`

Keine responsive Re-Encodierung wurde erzeugt, da kein C2PA-erhaltender Prozess lokal
verifiziert war. Ratssaal wird einmal priorisiert geladen, Vorzimmer einmal lazy. Der
statische Build ist dadurch 6,4 MB groß; jedes Plate hat rund 1,9 MiB auf dem Dateisystem.

## 10. Ausgeführte Befehle und Exit-Codes

| Befehl | Exit | Ergebnis |
|---|---:|---|
| `npm test` (vor neuem Build) | 1 | 6 Datentests bestanden; HTML-Test traf erwartungsgemäß den alten Build |
| `npm run build` | 0 | statischer Produktionsbuild erfolgreich; zunächst bestehende und eine neue CSS-Warnung sichtbar |
| `npm test` (nach Build, vor Regexkorrektur) | 1 | 6/7 bestanden; HTML enthielt `<del class=…>`, Test erwartete zu eng `<del>` |
| `npm test` (final; enthält `pretest`-Build) | 0 | Build erfolgreich, 7/7 Tests bestanden |
| `npm run preview -- --host 127.0.0.1` (Sandbox) | 1 | Portbindung mit `EPERM` blockiert |
| derselbe Previewbefehl mit lokaler Freigabe | laufend/anschließend beendet | Server erfolgreich auf `127.0.0.1:4173` gestartet |
| lokaler `curl` aus Sandbox | 7 | getrennte Sandbox konnte freigegebenen Server nicht erreichen |
| lokale HTTP-Prüfung mit Freigabe | 0 | `/` und Ratssaalasset jeweils HTTP 200; erwartete Inhalte ausgeliefert |

Der finale Build war warnungsfrei. Er transformierte 173 SSR- und 182 Clientmodule.
Homepage-CSS: 17,91 kB / 4,26 kB gzip. Homepage-Node-JavaScript: 16,84 kB / 5,29 kB
gzip; darin steckt Svelte-Komponentencode einschließlich des kleinen Szenencontrollers.

## 11. Buildwarnungen und verbleibende Probleme

Final verbleiben keine Compilerwarnungen. Vorhandene Reaktivitätswarnungen in der
Sitzungsroute, Journalroute und `ConfidenceBar` wurden beseitigt; der ungenutzte
Homepage-CSS-Selektor wurde korrigiert.

Offene Punkte:

- Die Playwright-Prüfung deckt Desktop 1440 × 900, Mobile 390 × 844 und No-JS mit
  Reduced Motion ab. Ein vollständiger manueller Screenreader-Test steht weiterhin aus.
- Die beiden Original-PNGs sind schwer. Optimierte Derivate bleiben absichtlich offen,
  bis C2PA nach der Transformation verifiziert werden kann.
- Die bestehende `marked`-/`{@html}`-Vertrauensannahme für committed Markdown wurde nicht
  durch eine neue Sanitizer-Abhängigkeit verändert.
- Aktuell existiert keine Svelte-Typcheck-/Lint-Toolchain im Paket. Der Svelte/Vite-Build
  selbst und die Node-Goldentests sind grün.

## 12. Testresultate

Final: **7 Tests, 7 bestanden, 0 fehlgeschlagen, 0 übersprungen.**

Geprüft sind Sortierung nach Sitzungsnummer, Registryidentität, unbekannte IDs,
Registry-Spendenlinks, Null-URL, Highlight-Normalisierung, Runden ohne Voten,
unaufgelöste Stimmen, Revisionen, konditionale Stimmen, realer Konsensfall, realer
Nicht-Konsensfall und die statische No-JS-Ausgabe.

## 13. Nicht umgesetzte Punkte

- Keine Bildderivate: Schutz der vorhandenen C2PA-Provenienz hatte Vorrang.
- Kein automatisierter Screenreader-Test; die semantische und visuelle Browserprüfung
  ersetzt keine Prüfung mit VoiceOver/NVDA.
- Keine neue Runtime- oder Dev-Abhängigkeit: Node-Bordmittel reichen für die Goldentests.
- Kein Redesign der übrigen Dokumentrouten: nur gemeinsame Markdown-/Anker- und
  Reaktivitätskorrekturen, die für konsistente Verlinkung notwendig sind.
- Kein `ScrollTimeline`: IntersectionObserver und CSS-Zustände erfüllen den Zweck mit
  breiterer Unterstützung.

## 14. Produktive Ausgabe

Der produktive statische Build liegt unter:

`site/build/`

Der unveränderte Deploymentworkflow synchronisiert genau diesen Inhalt nach
`/srv/noblecause/`, sobald auf `master` ausgeliefert wird. Es wurde kein zweiter
Prototyp oder alternativer Entry-Point angelegt.
