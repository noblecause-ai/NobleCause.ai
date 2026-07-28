> **Archiviert 2026-07-28 (CC) — Codex-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# NobleCause.ai — Release-Readiness-Bericht

Stand: 16. Juli 2026  
Branch: `feat/immersive-homepage`  
Produktiver Pfad: `site/`  
Buildausgabe: `site/build/`

## 1. Zusammenfassung

Die zehn neuen Prozess- und Säulenmotive sind semantisch benannt, byteidentisch als
Originale im produktiven Assetpfad abgelegt, für die UI abgeleitet und in die Startseite
integriert. Die generischen Prozessziffern und Säulenkreise wurden durch gemalte Motive in
derselben Holz-, Messing- und Mondblauwelt ersetzt.

Die drei Modelllabels verwenden in der Desktopszene ein gemeinsames relatives
Bildkoordinatenmodell und liegen bei 1440 × 900 sowie 1024 × 768 an den drei sichtbaren
Pulten. Mobil erscheinen die Modelle bewusst als lineare Pultregister ohne räumlich falsche
Overlays. Sichtbare CSS-Platzhalter für Tür und Zählmaschine wurden entfernt.

## 2. Übernommene und umbenannte Bilder

| Ursprünglicher Exportname | Produktives Original |
|---|---|
| `...08_57_14 (1).png` | `media/process/question.png` |
| `...08_57_15 (2).png` | `media/process/evidence.png` |
| `...08_57_15 (3).png` | `media/process/three-answers.png` |
| `...08_57_16 (4).png` | `media/process/review-and-revise.png` |
| `...08_57_16 (5).png` | `media/process/count.png` |
| `...08_57_16 (6).png` | `media/process/publish.png` |
| `...08_57_17 (7).png` | `media/pillars/future.png` |
| `...08_57_17 (8).png` | `media/pillars/suffering.png` |
| `...08_57_17 (9).png` | `media/pillars/global-risks.png` |
| `...08_57_17 (10).png` | `media/pillars/overlooked.png` |

Maße, Bytes, vollständige Ursprungsnamen und SHA-256 stehen in
`site/static/media/ASSETS.md`. Nach Hash- und Buildprüfung wurden nur diese zehn generischen
Arbeitskopien aus `docs/` entfernt; die semantischen produktiven Originale bleiben erhalten.

## 3. Mapping

- Prozess: Frage → Fragezeichen; Belege → Dossier; drei Antworten → drei Pulte;
  Gegenlesen/Umdenken → revidiertes Buch; Zählen → Messingabakus; Veröffentlichen →
  versiegeltes Protokoll.
- Säulen: Zukunft → Pflanze; Leid → Moskitonetz; große Gefahren → Tresortür;
  Übersehenes → Farbeimer und Pinsel.

## 4. Anchor-Modell

`lecternAnchors` beschreibt jedes Modellpult durch `x/y`-Prozentwerte im unverzerrten
Ratssaalbild: links oben Anthropic, rechts oben OpenAI, unten mittig Google. Diese Werte
werden als `--anchor-x` und `--anchor-y` an alle Pultschilder übergeben. Die `initial`-Szene
verwendet `object-fit: contain`, Zoom 1 und eine zentrierte 16:9-Szene. Dadurch bleibt das
Koordinatensystem bei 1440 × 900 und 1024 × 768 stabil; die seitlichen Register werden in
diesem Zustand abgedunkelt. Unter 800 px wird das Overlaymodell deaktiviert und durch drei
gleichwertige, normal fließende Register ersetzt.

## 5. Geänderte und entfernte Dateien

Geändert wurden:

- `site/src/routes/+page.svelte`
- `site/static/media/ASSETS.md`

Neu sind:

- zehn Originale unter `site/static/media/process/` und `pillars/`
- zehn 320-px-Anzeigederivate neben den Originalen
- vier 1600-px-Szenenderivate unter `site/static/media/scenes/`
- zwei 640-px-Vorschaubilder unter `site/static/media/scene-thumbnails/`
- dreizehn finale Reviewbilder unter `docs/review/final-release/`
- dieser Bericht

Entfernt wurden die zehn verifizierten, generisch benannten Arbeitskopien `08_57_*` aus
`docs/` sowie die toten CSS-/DOM-Platzhalter der früheren Tür und Zählmaschine. Historische
C2PA-Originale und `sol-build/` blieben unangetastet.

## 6. Befehle und Exit-Codes

| Befehl | Exit | Ergebnis |
|---|---:|---|
| `cd site && npm ci` | 0 | 52 Lockfile-Pakete installiert, keine neue Abhängigkeit |
| `cd site && npm test` | 0 | Build im `pretest`; 7/7 Tests bestanden |
| `cd site && npm run build` | 0 | warnungsfreier Adapter-Static-Build nach `site/build/` |
| `cd site && npm run preview -- --host 127.0.0.1 --port 4181` | 0 | Produktionsbuild lokal ausgeliefert |
| erster Previewversuch in eingeschränkter Sandbox | 1 | `listen EPERM`; anschließend mit freigegebenem lokalen Preview erfolgreich |
| `git diff --check` | 0 | keine Whitespacefehler |
| Playwright-Abnahme | 0 | Szenen, Viewports, Navigation, Routen und Screenshots erfolgreich |

Das Projekt definiert weiterhin keine separaten `lint`- oder `check`-Skripte. Es werden
deshalb keine entsprechenden Ergebnisse behauptet.

## 7. Testergebnisse

Alle sieben Node-Tests bestehen: Sitzungswahl nach Nummer, Registry als Identitäts- und
URL-Quelle, Highlightnormalisierung, Konsensfall `2026-07c`, Nicht-Konsensfall `2026-07`,
fehlertolerante leere Runden/harte unresolved votes und vollständige No-JS-Prerenderausgabe.

Alle elf aus der Homepage erreichbaren internen Ziele antworteten im lokalen
Produktionspreview mit HTTP 200. Die vier sichtbaren direkten Spendenlinks entsprechen den
Registryzielen für Helen Keller International, Against Malaria Foundation, NTI und Lead
Exposure Elimination Project.

## 8. Viewports und Szenen

Geprüft wurden alle acht Zustände bei 1440 × 900 sowie die Pultanker bei 1024 × 768.
Mobile Reflow wurde bei 390 × 844 und 320 × 700 geprüft. In allen vier Viewports gilt
`scrollWidth === innerWidth`. Dreizehn Screenshots liegen unter
`docs/review/final-release/` (acht Desktopzustände, 1024-Pultansicht, zwei Mobilansichten,
No-JS und Reduced Motion).

## 9. No-JS, Reduced Motion und Tastatur

- Ohne JavaScript bleibt der semantische Fallback sichtbar und enthält Empfehlungen,
  Stimmen, Änderungen, Links und Protokollzugang.
- Bei `prefers-reduced-motion: reduce` werden Übergänge auf praktisch null reduziert; alle
  acht Szenen bleiben verfügbar.
- Der erste Tab erreicht den NobleCause-Home-Link. Hashnavigation aktiviert `count`;
  Browser-Zurück kehrt zu `arrival` zurück.
- Mobil werden Pultlabels bewusst nicht auf ein skaliertes Bild projiziert.

## 10. Performance- und Assetbefund

Die zehn unveränderten 1254-px-Originale umfassen rund 20,6 MB, werden aber nicht von der
Homepage geladen. Ihre 320-px-Derivate liegen jeweils bei rund 18–20 kB. Die großen
Szenenderivate liegen bei 271–367 kB; Vorschaubilder bei 41–62 kB.

Im gemessenen Initialzustand wurden ungefähr 664 kB Bildressourcen übertragen, davon rund
368 kB für den priorisierten Ratssaal. Tür, großes Vorzimmer und großes Archiv werden erst
im jeweiligen Zustand in den DOM eingesetzt. Jede geladene URL war eindeutig; es gab keine
doppelten Downloads desselben Bildes.

Homepage-CSS: 19,52 kB (3,70 kB gzip). Homepage-JS: 15,20 kB (4,55 kB gzip).

## 11. Verbleibende Risiken

- Ein manueller Screenreader- und Realgeräte-Test bleibt vor dem öffentlichen Merge
  empfehlenswert; automatisiert geprüft wurden Semantik, Tastatur, Reflow und No-JS.
- Die JPEG-Derivate tragen nicht den Provenienznachweis der unveränderten PNG-Originale.
  Die Originale und Hashes bleiben deshalb separat erhalten und dokumentiert.
- Der Deployment-Rsync arbeitet ohne `--delete`; bereits auf dem Server liegende alte,
  inzwischen entfernte Dateien können als verwaiste URLs bestehen bleiben.
- Kein Lighthouse-/WebPageTest-Lauf wurde durchgeführt; die reale Netz- und LCP-Messung
  bleibt Teil des Review vor Merge.

## 12. Empfehlung

**READY FOR REVIEW**

Die produktive App erfüllt die Asset-, Daten-, Build-, Routing-, Interaktions- und
Screenshotkriterien. Ein Merge wird noch nicht empfohlen, bevor OpenAI-/Anthropic-Review,
manueller Screenreader-/Realgeräte-Smoke-Test und die Entscheidung zum Rsync-`--delete`-
Risiko abgeschlossen sind. Es wurde weder gemergt noch deployed.
