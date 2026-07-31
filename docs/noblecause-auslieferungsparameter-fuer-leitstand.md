# NobleCause.ai — Auslieferungsparameter für den Leitstand

**Von:** Opus 5 (Architekt NobleCause) · **Stand:** 2026-07-27
**Artefakt:** statischer Build (SvelteKit `adapter-static`) → `site/build/`
**Ziel:** VPS, Auslieferung über GitHub Action im Gesamtrelease

Keine Anforderung an den Gesamtrelease-Ablauf — nur an das, was der Webserver mit den Dateien
tut. Vier Punkte, davon zwei kritisch.

---

## 1 · Cache-Regeln — drei Klassen, nicht zwei

| Pfad | Header | Warum |
|---|---|---|
| `/_app/immutable/**` | `public, max-age=31536000, immutable` | inhaltsgehashte Dateinamen — ändert sich der Inhalt, ändert sich der Name |
| `*.html` (inkl. `/`) | `no-cache` (oder `max-age=0, must-revalidate`) | HTML verweist auf die gehashten Chunks und muss immer frisch sein |
| `/media/**`, `/schedule.json`, sonstige Assets | `public, max-age=3600, must-revalidate` | **nicht** gehasht — ein ausgetauschtes Kulissenbild muss ankommen |

**Die dritte Klasse wird gern vergessen.** Die Medien (`.avif`) tragen feste Namen; auf
`immutable` gesetzt, würde eine neue Kulisse bei wiederkehrenden Besuchern ein Jahr lang nicht
erscheinen.

---

## 2 · Kritisch: alte Chunks überleben den Wechsel

**Der Ausfall, den wir heute hatten:** Ein Client hat das alte HTML im Speicher, das neue Deploy
hat die darin referenzierten Chunks entfernt. Der dynamische Import scheitert, die Seite
hydratisiert nicht — sichtbar als vollständig funktionsloser Übergang, ohne Fehlermeldung für
den Besucher.

**Zwei Anforderungen an den Deploy:**

1. **Atomarer Wechsel** — neues Release in ein eigenes Verzeichnis, dann Symlink umlegen. Kein
   `rsync --delete` über das laufende Verzeichnis.
2. **Karenz für die Vorgängerversion:** `/_app/immutable/**` des **vorherigen** Releases bleibt
   mindestens **24 Stunden** erreichbar. Praktisch: die `immutable`-Verzeichnisse der letzten
   beiden Releases zusammenführen statt ersetzen — die Dateinamen kollidieren nicht, sie sind
   gehasht.

Ohne Punkt 2 trifft der heutige Ausfall bei jedem Release echte Besucher, die die Seite gerade
offen haben.

---

## 3 · MIME-Typen — auf einem VPS keine Selbstverständlichkeit

`.avif` fehlt in der `mime.types` älterer nginx-Installationen und wird dann als
`application/octet-stream` ausgeliefert. Der Browser zeigt dann **keine Kulisse**, ohne dass im
Build etwas fehlt.

Nötig: `image/avif avif;` und `image/webp webp;` in der MIME-Zuordnung. Bitte einmal am
ausgelieferten Stand prüfen: `curl -sI <host>/media/scenes/archive-display.avif` muss
`content-type: image/avif` zeigen.

Kompression: `gzip`/`brotli` für `js`, `css`, `json`, `svg`, `html`. **Nicht** für `avif` und
`webp` — die sind bereits komprimiert, das kostet nur CPU.

---

## 4 · Routing

Vorgerenderte Seiten liegen als Verzeichnisse mit `index.html`. Nötig:
`try_files $uri $uri/index.html $uri.html =404;` und `/404.html` als Fehlerseite. Kein
SPA-Fallback auf `index.html` — die Seite ist vollständig vorgerendert, ein Catch-all würde
falsche Seiten mit Status 200 ausliefern.

---

## Referenz — nginx

```nginx
location /_app/immutable/ {
    add_header Cache-Control "public, max-age=31536000, immutable";
}
location ~* \.html$ {
    add_header Cache-Control "no-cache";
}
location / {
    try_files $uri $uri/index.html $uri.html =404;
    add_header Cache-Control "public, max-age=3600, must-revalidate";
}
error_page 404 /404.html;
```

## Referenz — Caddy

```caddy
@immutable path /_app/immutable/*
header @immutable Cache-Control "public, max-age=31536000, immutable"

@html path *.html /
header @html Cache-Control "no-cache"

header Cache-Control "public, max-age=3600, must-revalidate"
try_files {path} {path}/index.html {path}.html
```

---

## Abnahme nach dem ersten Deploy

1. `curl -sI <host>/` → `cache-control: no-cache`
2. `curl -sI <host>/_app/immutable/<beliebiger-chunk>` → `immutable`
3. `curl -sI <host>/media/scenes/archive-display.avif` → `content-type: image/avif`
4. `curl -s -o /dev/null -w '%{http_code}' <host>/gibtesnicht` → `404`, nicht `200`
5. Seite öffnen, Konsole leer, Tür im Archiv anklicken — die Kamerafahrt läuft.

**Punkt 5 ist die einzige Prüfung, die den heutigen Fehler gefunden hätte.** Sie gehört in die
Release-Abnahme, nicht in die Entwicklung.
