# Integrationsplan: Prozess-Embleme und Säulenbilder

Stand: 16. Juli 2026  
Phase: 1 — Recherche und Planung, keine Implementierung

## Verifizierter Ist-Zustand

Der aktuelle Branch ist `feat/immersive-homepage` auf Commit `f8c51b6`. Der Working Tree
enthält ausschließlich fünf neue Bilddateien und den neuen Zwei-Phasen-Auftrag unter
`docs/`; die bereits implementierte Homepage ist committed.

Claude Code hat seit dem vorherigen Codex-Stand drei relevante Commits vorgenommen:

- `3e3032a`: bisherigen immersiven Aufbau, Datenlogik, Tests, Bilder und Berichte gesichert;
- `7153876`: No-JS-Fallback vervollständigt, Revisionen datengetrieben gemacht, tote
  Serverprojektionen entfernt, Originalbilder aus dem Deploypfad nach
  `docs/asset-originals/` verschoben und das initiale Saalbild verkleinert;
- `f8c51b6`: schlecht erkennbare Rastercrops aus der sichtbaren UI entfernt und durch
  A–D-Buchstaben beziehungsweise 1–6-Nummern ersetzt; Kontraste erhöht; die auf Mobil
  geclippte Prozessleiste ausgeblendet.

Die Startseite wird weiterhin vollständig durch `site/src/routes/+page.svelte` gerendert.
Es gibt derzeit keine getrennten Säulen- oder Prozesskomponenten:

- vier Säulen: `.recommendation-console .rec-row summary i`, aktuell A–D als Text;
- sechs Schritte: `.process-rail`, aktuell 1–6 als Text;
- mobile Prozessdarstellung: `.process-rail` ist unter 800 px `display:none`;
- erste Säulenerklärung: `arrival-plaque` mit dem Satz „Für Menschen heute, unsere
  Zukunft, große Gefahren und Übersehenes“, derzeit ohne Zeichen;
- erste Prozesserklärung: `mechanism-plaque`, derzeit nur zwei Textzeilen ohne Zeichen;
- No-JS-Fallback: semantisch vollständig, aber noch mit internen A–D-Kürzeln.

Die Szenensteuerung bleibt ein kleiner `IntersectionObserver` in derselben Datei. Daten,
Registryauflösung, Revisionen und Konsenslogik liegen außerhalb der Präsentationszeichen
und müssen nicht verändert werden.

## Tatsächliche Asset- und Provenienzkonvention

Claude hat die frühere Konvention bewusst geändert:

- unveränderte, hochauflösende Originale liegen unter
  `docs/asset-originals/media/` und werden nicht deployed;
- ausschließlich kleine `*-display.jpg`-Derivate liegen unter `site/static/media/`;
- die kanonische Provenienzdokumentation ist jetzt
  `docs/asset-originals/ASSETS.md`;
- `site/static/media/ASSETS.md` existiert nicht mehr, damit kein interner
  Provenienz-/Arbeitsbericht mit der Website ausgeliefert wird.

Phase 2 soll diese bereinigte Konvention beibehalten. Der im Auftrag noch genannte alte
Manifestpfad wird nicht blind wiederhergestellt. Stattdessen wird das kanonische
`docs/asset-originals/ASSETS.md` aktualisiert. Falls ein Manifest zwingend unter
`site/static/media/` verlangt wird, wäre dafür eine eigene Freigabe sinnvoll, weil es
Claudes ausdrücklich eingeführte Deploy-Hygiene rückgängig macht.

## Mapping der neuen Säulenbilder

Alle fünf Dateien messen 1254 × 1254 Pixel. Die Zuordnung wurde nach dem sichtbaren Inhalt
und durch SHA-256-Prüfung vorgenommen:

| Quelldatei unter `docs/` | Inhalt | Säule | Bytes | SHA-256 |
|---|---|---|---:|---|
| `...14_24_58.png` | startende Rakete | Zukunft | 2.619.231 | `f1cf408ad75773f87564b3ebed2a83a0087557747e98bb6fcfa98503c14b57b4` |
| `...14_25_26.png` | gebende und empfangende Hand | Leid lindern | 2.358.139 | `7839270a12c066d370be927d43104d16cd294be6e31f67cc38d39ad0e8ee53da` |
| `...14_25_13.png` | vereinfachter Atompilz | Große Gefahren | 2.562.631 | `6c17d338fec4fab8bb8fd911bf4ff8e2da7cbb053fab43c1eadd836b28d2fd6f` |
| `...14_24_39.png` | Brücke, Auto und herausfallender Tragstein | Was sonst übersehen wird | 2.676.957 | `e77f3f8f22dd38812af9f6e703e7995fe5c3a57152fd61e7c5bd2ff1b6a0890f` |
| `...14_25_40.png` | startende Rakete | exaktes Duplikat | 2.619.231 | `f1cf408ad75773f87564b3ebed2a83a0087557747e98bb6fcfa98503c14b57b4` |

`14_24_58` wird als kanonische Raketenquelle gewählt; `14_25_40` kann nach erfolgreicher
Übernahme als byteidentische Arbeitskopie entfernt werden.

## Endgültige Namen und Zielpfade

Unveränderte Originale, nicht deployed:

- `docs/asset-originals/media/pillars/pillar-future.png`
- `docs/asset-originals/media/pillars/pillar-relieve-suffering.png`
- `docs/asset-originals/media/pillars/pillar-major-risks.png`
- `docs/asset-originals/media/pillars/pillar-overlooked.png`
- `docs/asset-originals/media/process/process-question.png`
- `docs/asset-originals/media/process/process-evidence.png`
- `docs/asset-originals/media/process/process-three-answers.png`
- `docs/asset-originals/media/process/process-reconsider.png`
- `docs/asset-originals/media/process/process-count.png`
- `docs/asset-originals/media/process/process-publish.png`

Deployte UI-Derivate:

- `site/static/media/pillars/pillar-*-display.jpg`
- `site/static/media/process/process-*-display.jpg`

Die langen Präfixe sind beabsichtigt: Dateiname, Ordner und Verwendung bleiben auch in
Performance-Traces eindeutig.

## Originale, Webderivate, Hashes und Dokumentation

Für jedes der zehn Motive wird Phase 2:

1. das ausgewählte/generierte Original byteidentisch im Originalarchiv ablegen;
2. Maße, Bytes, Quelle/Generierungsdatum und SHA-256 erfassen;
3. mit der vorhandenen lokalen Pipeline ein quadratisches 320 × 320-JPEG-Derivat erzeugen;
4. für die tatsächliche 32–44-px-Verwendung Qualität und Schärfe visuell vergleichen;
5. nur das Derivat nach `site/static/media/` legen;
6. `docs/asset-originals/ASSETS.md` um Original- und Derivatinformationen ergänzen;
7. sicherstellen, dass kein Original in `site/build/` landet.

JPEG ist für die gemalte, vollflächige Stein-/Messingtextur derzeit passender als PNG und
bereits Repositorykonvention. WebP/AVIF wird nur verwendet, wenn ein vorhandenes lokales
Werkzeug reproduzierbar verfügbar ist; es wird keine neue Abhängigkeit nur dafür ergänzt.
Die HTML-Bilder erhalten feste Maße, leere Alttexte bei dekorativer Wiederholung und einen
zugänglichen Namen über den unmittelbar sichtbaren Begriff.

## Spezifikation der sechs Prozess-Embleme

Codex kann die sechs Motive in dieser Umgebung mit der eingebauten hochwertigen
Bildgenerierung selbst erzeugen. Phase 2 verwendet pro Motiv einen eigenen Generate-Call,
mit dem vorhandenen Ratssaal und der realen Maschine als Stil-/Objektreferenz. Es werden
keine SVG-, CSS- oder typografischen Ersatzbilder gebaut.

Gemeinsamer Vertrag:

- quadratisches, frontales Messingrelief auf sehr dunklem mattem Schiefer;
- derselbe schmale, zurückhaltende Messingring wie bei den neuen Säulenbildern;
- ein einziges starkes Motiv, großzügige Negativfläche, hoher Silhouettenkontrast;
- warmes Bernstein-Kantenlicht, minimale kalte Mondblau-Umgebung;
- kein Text, keine Buchstaben, keine Ziffern, keine Menschen, kein Hochglanz;
- für einen kreisförmigen Crop sicher komponiert;
- bei 32 px muss die Hauptform ohne Detailwissen benennbar bleiben.

Einzelmotive:

1. **Frage:** einzelne Feder schräg über einem fast leeren Blatt; ein großes, tief
   graviertes Fragezeichen ist der einzige Inhalt des Blatts. Feder und Fragezeichen bilden
   gemeinsam eine klare Diagonalsilhouette.
2. **Belege:** große Lupe über exakt drei parallel ausgerichteten Dokumentblättern; keine
   lose Papierwolke, keine Schrift, keine zusätzlichen Werkzeuge.
3. **Drei Antworten:** exakt drei identische, vereinfachte Pulte als klares Dreieck, je ein
   helles Blatt; die drei Lichtpunkte müssen bei 32 px separat bleiben. Zusätzlich wird eine
   stärker reduzierte Variante erzeugt und im 32-px-Vergleich ausgewählt.
4. **Umdenken:** ruhiges seitliches Kopfprofil als nicht-anatomisches Relief; im Kopf eine
   einzige Gedankenbahn mit deutlich sichtbarer 180-Grad-Wendung/Pfeil. Kein Buch, keine
   Dokumente, keine Chatblase, kein medizinisches Gehirn.
5. **Zählen:** vereinfachte Frontansicht der tatsächlichen Ratssaalmaschine: zentrale
   Zähltrommeln, drei klar getrennte Zuflüsse/Marken, runder Sockel. Kein Abakus, Gesicht,
   Bediener oder Intelligenzsymbol. Das vorhandene Maschinenbild ist verbindliche
   Objektreferenz.
6. **Veröffentlichen:** weit geöffnetes offizielles Protokoll auf kleinem Sockel, mittig ein
   deutliches geprägtes Siegel; kein Umschlag und keine private Briefanmutung.

Nach jeder Erzeugung wird zunächst das hochauflösende Original geprüft, danach ein echter
32 × 32-Crop auf dunklem UI-Grund. Verwechselbare Ergebnisse werden nicht integriert,
sondern mit genau einer gezielten Korrektur neu erzeugt.

## Geplante UI-Integration

`site/src/routes/+page.svelte` bleibt zunächst die einzige betroffene Renderdatei; eine
Komponentenaufteilung nur für zehn kleine Bilder wäre unnötig. Geplant sind zwei zentrale
Konstanten (`pillarEmblems`, `steps` mit Bildpfad und Alltagstext), damit Pfade und Begriffe
nicht mehrfach auseinanderlaufen.

- Empfehlungsregister: A–D-Medaillons werden durch die vier Säulenmotive ersetzt; der
  sichtbare Text beginnt mit Alltagssprache, nicht mit dem Buchstaben.
- Prozessleiste Desktop: 1–6-Kreise werden durch die sechs Embleme ersetzt; der aktive
  Zustand verändert ausschließlich Licht, Ring und Kontrast.
- Mobile: keine Rückkehr zur geclippten Desktopleiste. Stattdessen eine eigene zweizeilige
  3×2-Prozessübersicht im normalen Dokumentfluss.
- No-JS: dieselben sichtbaren Begriffe und Embleme stehen im prerendered Fallback; Bilder
  bleiben ergänzend, Text ist vollständig.
- Archiv/Sitzungen: nur dort wiederholen, wo Säulen oder Prozessschritte tatsächlich
  benannt werden. Keine dekorative Iconflut und keine Änderung der Sitzungsdaten.

## Erste sprachliche Erklärung oben

Die Bildsprache muss vor den Registern verständlich werden:

- Direkt bei der ersten Vier-Bereiche-Aussage erscheint eine kompakte Säulenlegende mit
  Bild und Alltagstext: „Zukunft“, „Leid lindern“, „Große Gefahren“, „Was sonst übersehen
  wird“. Auf Desktop liegt sie als flache gravierte Viererreihe unter der Leitfrage; mobil
  als gut lesbares 2×2-Raster im normalen Fluss.
- Direkt bei „Drei Modelle antworten getrennt …“ erscheint eine Prozesslegende mit allen
  sechs Bildern und den Begriffen „Frage“, „Belege“, „Drei Antworten“, „Umdenken“,
  „Zählen“, „Veröffentlichen“. Desktop nutzt eine flache, instrumentartige Laufbahn;
  mobil eine 3×2-Matrix. Diese erste Erklärung ist keine zweite Navigation.
- Erst nach diesen Legenden dürfen kompakte Wiederholungen in Empfehlungsregister und
  Prozessnavigation folgen.

Auf der obersten Ebene werden `Säule A–D`, `Dissens` und `Evidenz` nicht als unerklärte
Einstiegsbegriffe benutzt. Fachlich notwendige Protokollbegriffe bleiben im vollständigen
Sitzungsdokument erhalten; die Startseite sagt zunächst „Bereich“, „noch keine Einigkeit“
und „Belege“.

## Cleanup-Liste für Phase 2

Erst nach erfolgreicher Integration, Hashprüfung, Build und Screenshotvergleich:

- alte unreferenzierte Derivate unter `site/static/media/pillars/{future,suffering,
  global-risks,overlooked}-display.jpg` entfernen;
- alte unreferenzierte Derivate unter `site/static/media/process/{question,evidence,
  three-answers,review-and-revise,count,publish}-display.jpg` entfernen;
- korrespondierende alte Originale unter `docs/asset-originals/media/pillars/` und
  `process/` entfernen, sobald die neuen Originale und ihre Dokumentation verifiziert sind;
- das Raketen-Duplikat `docs/...14_25_40.png` und die vier übrigen Arbeitskopien erst nach
  byteidentischer Übernahme entfernen;
- A–D-/1–6-spezifische CSS-Regeln und tote Bildpfade entfernen;
- auf tote Imports, 404-Pfade, doppelte Downloads und nicht referenzierte Derivate prüfen;
- `sol-build/` und alle geschützten Datenpfade unangetastet lassen.

Alte Review-Screenshots werden nicht automatisch gelöscht: Sie dokumentieren frühere
Abnahmen und sind keine Laufzeitassets.

## Test- und Screenshotplan

Technische Befehle nach der Integration:

```bash
cd site
npm ci
npm test
npm run build
npm run preview
```

Prüfmatrix:

- 1440 × 900 und 1024 × 768: Ankunft, Empfehlungen, komplette Prozessnavigation,
  Vorzimmer, Zählung und Pultanker;
- 390 × 844 und 320 × 700: Einführung, Empfehlungen, neue mobile Prozessmatrix, Reflow;
- 200-%-Zoom, No-JS, Reduced Motion, Tabfolge, Hashnavigation und Browser-Zurück;
- alle zehn Motive einzeln und als gemeinsame Kontaktseite bei exakt 32 × 32 CSS-Pixeln;
- visuelle Unterscheidbarkeit ohne Text, anschließend mit zugänglichem sichtbarem Text;
- keine horizontalen Überläufe, gebrochenen Bildpfade oder unnötigen Mehrfachdownloads;
- alle internen Links per lokalem Preview; externe Spenden-URLs gegen Registrywerte, ohne
  Organisationsidentität aus Text abzuleiten;
- `site/build/` enthält Derivate, aber keine hochauflösenden Originale.

Finale Screenshots unter `docs/review/final-emblems/`:

1. Desktop Ankunft
2. Desktop Empfehlungen
3. Desktop Prozessnavigation
4. Desktop Vorzimmer
5. Desktop Zählung
6. Mobile Einführung
7. Mobile Empfehlungen
8. Mobile Prozessnavigation
9. 32-px-Vergleich aller zehn Embleme
10. No-JS-Grundzustand

## Phase-2-Dateien

Voraussichtlich geändert:

- `site/src/routes/+page.svelte`
- `site/tests/homepage-build.test.js`
- `docs/asset-originals/ASSETS.md`
- gegebenenfalls `site/README.md` für die neue Zeichenlegende

Neu:

- vier neue Säulenoriginale und sechs generierte Prozessoriginale im Originalarchiv
- zehn neue deployte Derivate
- `docs/review/final-emblems/*`
- `docs/codex-emblems-integration-report.md`

Entfernt werden nur die oben eindeutig identifizierten Altassets und verifizierten
Arbeitskopien. Keine Datei unter `sessions/**`, `journal/**`, `gremium/**`, `schema/**`,
`schedule.json` oder `prompts.py` wird verändert.

## Entscheid und Haltepunkt

Codex kann die sechs Prozessbilder mit der verfügbaren hochwertigen Rasterbildgenerierung
selbst erzeugen und anhand der vorhandenen Ratssaal-/Maschinenreferenzen iterieren. Es
fehlen für Phase 2 keine Bilddateien vom Auftraggeber.

Gemäß Zwei-Phasen-Auftrag endet die Arbeit hier. Es wurde ausschließlich dieser Plan neu
angelegt. Keine produktive Datei, kein Bild und kein Style wurde verändert. Umsetzung erst
nach der ausdrücklichen Nachricht `FREIGABE`.
