> **Archiviert 2026-07-28 (CC) — Codex-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# Abschlussbericht: Prozess- und Säulenembleme

Stand: 16. Juli 2026  
Branch: `feat/immersive-homepage`  
Umfang: freigegebene Phase 2 aus `codex-process-and-pillar-emblems-two-phase.md`

## Ergebnis

Die vier gelieferten Säulenbilder und sechs neu erzeugten Prozessbilder sind in der
produktiven SvelteKit-Startseite unter `site/` integriert. Die Zeichen erscheinen bei der
ersten sprachlichen Erklärung, im Empfehlungsregister und in der Prozesssteuerung. Desktop
verwendet die instrumentartige Sechserleiste; Mobile besitzt eine eigene 2×2-Bereichs- und
3×2-Prozesskomposition im Dokumentfluss. Aktive Prozesszustände verändern nur Licht und
Kontrast, nicht das Motiv.

Die bisherigen A–D- und 1–6-Medaillons sowie die eindeutig unreferenzierten alten
Rasterassets wurden entfernt. Begriffe auf der Einstiegsebene wurden in Alltagssprache
übersetzt: „Zukunft“, „Leid lindern“, „Große Gefahren“, „Was sonst übersehen wird“,
„Belege“ und „noch keine Einigkeit“. Vollständige fachliche Protokollinhalte bleiben in den
Sitzungen verfügbar.

Die bestehende Sitzungs-, Konsens-, Revisions- und Registrylogik wurde nicht verändert.
Insbesondere blieben `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`, `schema/**`
und `prompts.py` unverändert.

## Assets und Provenienz

- Vier Auftraggeberoriginale: byteidentisch und semantisch benannt unter
  `docs/asset-originals/media/pillars/` archiviert.
- Sechs Codex-Generierungen: je ein hochauflösendes PNG unter
  `docs/asset-originals/media/process/` archiviert.
- Zehn ausgelieferte Derivate: 320 × 320 JPEG, Qualität 72, je 25–31 kB unter
  `site/static/media/{pillars,process}/`.
- SHA-256, Maße, Bytes, Motiv, Quelle und Derivatkonvention stehen vollständig in
  `docs/asset-originals/ASSETS.md`.
- Der statische Build ist 3,9 MB groß; `site/static/media` 1,5 MB. Im Build befinden sich
  keine hochauflösenden Emblemoriginale und keine Datei über 1 MB.
- Die fünf generischen Arbeitskopien unter `docs/` wurden erst nach Hashprüfung und
  Archivierung entfernt; die doppelte Rakete war byteidentisch.

## UI- und Robustheitsänderungen

- Zentrale `pillarEmblems`- und `steps`-Definitionen verhindern auseinanderlaufende Pfade
  und Bezeichnungen.
- Bilder sind ergänzend: sichtbarer Text und zugängliche Gruppenbezeichnungen tragen die
  Bedeutung; wiederholte Bilder haben leere Alttexte.
- Der No-JS-Prerender enthält alle zehn Zeichen, Empfehlungen, Abweichungen, Voten,
  Revisionen, Links, Kosten und das Archiv.
- Direkte Szenen-Hashes wählen den Kamerazustand ohne doppelten Fragment-Scroll; mobile
  Inhaltsanker werden nach der Hydrierung aufgelöst.
- `prefers-reduced-motion` behält die bestehende praktisch sofortige Übergangslogik.

## Ausgeführte Prüfungen

| Befehl | Exit | Tatsächliches Ergebnis |
|---|---:|---|
| `cd site && npm ci` | 0 | 52 Lockfile-definierte Pakete installiert; keine neue Abhängigkeit hinzugefügt |
| `cd site && npm test` | 0 | Produktionsbuild erfolgreich; 8/8 Node-Tests bestanden |
| `cd site && npm run build` | 0 | über `pretest` mehrfach erfolgreich; `adapter-static` schrieb nach `site/build` |
| `cd site && npm run preview -- --host 127.0.0.1` | 0 beim Start | Produktionspreview lokal auf Port 4174 geprüft (4173 war bereits belegt) |
| Headless Chromium, 1440×900 / 390×844 | 0 | zehn Reviewartefakte erzeugt und visuell geprüft |
| `shasum -a 256 …` | 0 | zehn Originale und zehn Derivate erfasst |
| Referenz- und Deploysuche mit `rg`/`find` | 0 | keine Laufzeitreferenz auf entfernte Altassets; keine Originale im Build |

Das Projekt definiert keine separaten `lint`- oder Typprüfskripte. Es wurden deshalb keine
nicht vorhandenen Prüfergebnisse behauptet. Vite/Svelte kompilierten ohne Warnung; Headless
Chromium meldete ausschließlich macOS-`task_policy_set`-Diagnostik, ohne Einfluss auf
Exitcode oder Screenshots.

## Visuelle Abnahme

Die zehn Artefakte liegen unter `docs/review/final-emblems/`:

1. `01-desktop-arrival.png`
2. `02-desktop-recommendations.png`
3. `03-desktop-process.png`
4. `04-desktop-antechamber.png`
5. `05-desktop-count.png`
6. `06-mobile-introduction.png`
7. `07-mobile-recommendations.png`
8. `08-mobile-process.png`
9. `09-emblems-at-32px.png`
10. `10-no-js.png`

Für die mobilen Detailabnahmen wurde zusätzlich eine ungeclippte 500-Pixel-Aufnahme des
vollständigen echten Dokumentflusses erstellt, auf die Zielzustände zugeschnitten und
proportional als 390 × 844 Reviewartefakt ausgegeben. Der No-JS-Screenshot basiert auf dem finalen `build/index.html`, aus dem für
die Aufnahme ausschließlich Script-Tags entfernt wurden. Der automatisierte Buildtest
prüft denselben Fallbackblock zusätzlich direkt im Prerender.

Alle zehn Motive bleiben bei exakt 32 CSS-Pixeln unterscheidbar. Besonders die Dreizahl der
Pulte, der Wendepfeil, die drei Zuflüsse des Zählwerks und das öffentliche Protokollsiegel
sind im gemeinsamen Kontaktbogen lesbar.

## Dateien

Geändert:

- `site/src/routes/+page.svelte`
- `site/tests/homepage-build.test.js`
- `docs/asset-originals/ASSETS.md`

Neu: zehn semantische Originale, zehn Displayderivate, dieser Bericht sowie die
Reviewartefakte. Entfernt: die korrespondierenden zwanzig unreferenzierten Altassets.

Es wurde kein zweiter Prototyp, kein neuer Buildpfad, kein Deployment und kein Merge
erstellt. Produktiver Ausgabepfad bleibt `site/build/`.
