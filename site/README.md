# site/ — die statische Website

SvelteKit mit `adapter-static`. Kein Server, kein JS-Zwang beim Besucher —
die Seiten werden beim Build vollständig vorgerendert.

## Inhalt kommt aus dem Repo-Root

`src/lib/server/content.js` liest zur Build-Zeit:

- `../manifest.md` → Seite `/manifest` (englisches Original wörtlich, deutsche Übersetzung im Svelte-Template)
- `../sessions/*/session.json` → `/sessions` (Index) und `/sessions/[id]` (Protokoll-Ansicht)

Eine neue Sitzung braucht daher **keine** Code-Änderung: Ordner unter
`sessions/` committen, pushen, fertig.

## Befehle

```bash
npm install       # einmalig
npm run dev       # lokale Entwicklung
npm run build     # statischer Build nach build/
npm run preview   # gebauten Stand lokal ansehen
```

## Design

Nüchtern-dokumentarisch (Parlaments-Protokoll, nicht Charity-Marketing):
Serifenschrift des Systems, Papierton, Linien statt Kästen, keine externen
Fonts, keine Tracker, keine Cookies.

## Deploy

Push auf `master` → GitHub Action baut und rsynct `build/` auf den VPS
(siehe `.github/workflows/deploy.yml`). Caddy serviert das Verzeichnis
statisch; ein Neustart ist nie nötig.
