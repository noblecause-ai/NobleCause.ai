# Go-Live-Build-Inventare — Bereitschaftsbericht §5 Punkte 5–7

**Von:** Claude Code (NobleCause-Session) · **Datum:** 2026-08-01
**Quelle:** gebauter `site/build/` auf `integration/go-live-0.4` = **`b1cad2f`**
(Sanitizing `93e10ef` + §7-Durchgang enthalten). Reine Erhebung aus dem Build, keine Vermutung.

---

## 5 · Routen-Inventar (alle ausgelieferten Verzeichnisse + Permalinks)

**Räume (sprachgetrennte URLs):**
| Raum | DE | EN |
|---|---|---|
| Study | `/` | `/en/` |
| Council | `/ratssaal/` | `/en/council/` |
| Archive | `/archiv/` | `/en/archive/` |

**Rekord-Permalinks (sprachneutrale Einzel-URLs, Sprache via hooks/Cookie — kein `/en/`-Präfix):**
- Sitzungen: `/sitzungen/2026-07/`, `/sitzungen/2026-07b/`, `/sitzungen/2026-07c/`
- Journal: `/journal/` (Index) + `/journal/2026-07-07/`, `/2026-07-08/`, `/2026-07-08b/`,
  `/2026-07-08c/`, `/2026-07-20/`, `/2026-07-24/`, `/2026-07-27/`, `/2026-07-27b/`

**Statische Seiten (sprachneutral):** `/manifest/`, `/idee/`, `/impressum/`

**Top-Level-Dateien:** `/index.html`, `/__data.json`, `/favicon.svg`, `/schedule.json`

**Für die Umzugstabelle (Punkt 8) relevant:**
- **Kein `/sessions/` im Build** — der Protokoll-Pfad heißt jetzt `/sitzungen/`. Alle alten
  `/sessions/*`-Permalinks brechen und brauchen 301 alt→neu.
- **EN liefert nur die drei Raum-Landings** (`/en/`, `/en/council/`, `/en/archive/`). Rekord-,
  Journal- und statische Seiten haben **keine** `/en/`-Varianten; sie sind sprachneutrale
  Einzel-URLs. Ein `/en/sitzungen/…` o. ä. existiert nicht — bei den 301 nicht darauf verweisen.

---

## 6 · Asset-Inventar (Pfade + Formate aller ausgelieferten Medien)

**Formate unter `/media/`:** 50× AVIF, 1× WEBP.
**Die eine WEBP:** `/media/process/process-three-answers-display.webp`
**Gehashte Build-Assets** unter `/_app/immutable/assets/`: 12 Dateien (CSS/JS/Schriften, inhaltsgehasht).

**Jede AVIF-Datei (50) — Grundlage der `image/avif`-MIME-Prüfung:**

```
/media/actors/antechamber-leaf-left.avif      /media/scenes/antechamber-display-lo.avif
/media/actors/antechamber-leaf-right.avif     /media/scenes/antechamber-display.avif
/media/actors/council-drum-lo.avif            /media/scenes/antechamber-portrait-800.avif
/media/actors/council-drum.avif               /media/scenes/antechamber-portrait-display.avif
/media/actors/council-machine-lo.avif         /media/scenes/antechamber-wall-hole.avif
/media/actors/council-machine.avif            /media/scenes/archive-display-lo.avif
/media/actors/door-leaf-left.avif             /media/scenes/archive-display.avif
/media/actors/door-leaf-right.avif            /media/scenes/archive-portrait-800.avif
/media/actors/hall-leaf-left.avif             /media/scenes/archive-portrait-display.avif
/media/actors/hall-leaf-right.avif            /media/scenes/archive-wall-hole.avif
/media/actors/lectern.avif                    /media/scenes/hall-display-lo.avif
/media/actors/pult-lamp.avif                  /media/scenes/hall-display.avif
/media/actors/scout.avif                      /media/scenes/hall-portrait-800.avif
/media/actors/warden.avif                     /media/scenes/hall-portrait-display.avif
/media/ambient/clouds-study.avif              /media/scenes/hall-wall-hole.avif
/media/doors/door-council-archive-display.avif
/media/doors/door-study-archive-display.avif
/media/medallions/claude-opus-4-8-lo.avif     /media/pillars/pillar-future-display.avif
/media/medallions/claude-opus-4-8.avif        /media/pillars/pillar-major-risks-display.avif
/media/medallions/gemini-2.5-pro-lo.avif      /media/pillars/pillar-overlooked-display.avif
/media/medallions/gemini-2.5-pro.avif         /media/pillars/pillar-relieve-suffering-display.avif
/media/medallions/gpt-5.2-lo.avif             /media/process/process-count-display.avif
/media/medallions/gpt-5.2.avif                /media/process/process-evidence-display.avif
/media/scene-thumbnails/antechamber-display.avif  /media/process/process-publish-display.avif
/media/scene-thumbnails/doorway-display.avif      /media/process/process-question-display.avif
/media/scene-thumbnails/hall-display.avif         /media/process/process-reconsider-display.avif
```

**MIME-Prüfpunkt (Go-Live):** ein `/media/*.avif` abrufen und `content-type: image/avif` belegen.
Caddy Stufe 2a hat `.avif` im Medien-Cache-Matcher; ob es auch den MIME setzt, ist ungemessen
(bisher keine AVIF live). Nicht vorab regeln, am ersten Deploy messen.

---

## 7 · Chunk-Erwartung (24-Stunden-Karenz)

**`_app/immutable/` im neuen Build:** `entry/` 2, `chunks/` 15, `nodes/` 18, `assets/` 12 =
47 gehashte Dateien; `_app/` gesamt 48 Dateien / 400 KB. Namen inhaltsgehasht
(z. B. `entry/app.DxNB58NE.js`, `entry/start.DTSojuZI.js`).

**Deploy-Mechanik bestätigt:** `deploy.yml` deployt mit `rsync -avz` **ohne `--delete`**
(Zeile 54–56). Es wird nichts entfernt, nur hinzugefügt/aktualisiert.

**Was für die Karenz erhalten bleiben muss:** die `_app/immutable/*`-Chunks der
**Vorgängerversion** — konkret der aktuell live stehende **14.-Juli-Build** auf dem VPS. Ein
Besucher, der die alte `index.html` noch geladen hat, referenziert alt-gehashte Chunk-Namen; ohne
`--delete` bleiben genau diese Dateien liegen, sodass sie ≥24 h nachladbar sind statt 404.
**Voraussetzungen (beide erfüllt):** `--delete` bleibt aus **und** es existiert keine Aufräum-Routine
unter `/srv/noblecause/` (Caddy-Stufe-1-Bericht). Nach diesem Deploy liegen erstmals **zwei**
Generationen auf der Platte (bisher nur eine, 14. Juli) — das ist der Karenz- und Rollback-Puffer.
