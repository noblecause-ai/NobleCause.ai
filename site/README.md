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

Die Startseite erweitert diesen dokumentarischen Grundzustand als „Ratssaal als lebende
Maschine“. Auf Desktop bleibt ein einziges, viewportfüllendes Instrument stehen und
wechselt beim Scrollen durch acht räumliche Zustände: Ankunft, Empfehlungen, Türöffnung,
Vorzimmer, Erstvoten, Umdenken, Zählung und Archiv. Mobil wird dieselbe Datenwahrheit als
kompakte lineare Bühne neu komponiert, nicht als verkleinerte Desktopansicht.

Der vollständige Inhalt wird vorgerendert. Erst nach erfolgreicher Hydration ersetzt die
inszenierte Bühne den eigenständigen HTML-Grundzustand. Ohne JavaScript bleiben
Empfehlungen, Voten, Revisionen, Dissens, Kosten, Protokoll- und Spendenlinks erreichbar.

`src/lib/server/homepage.js` baut aus aktueller Sitzung und `organizations.json` ein
explizites View-Model. Organisationen werden ausschließlich über `organization_id`
aufgelöst. Unbekannte IDs und unaufgelöste Stimmen brechen den Build ab.

Die byte-identisch übernommenen C2PA-Originale und ihre Hashes sind unter
`static/media/ASSETS.md` dokumentiert.

## Tests

```bash
npm run build
npm test
```

Die Node-Bordmitteltests prüfen Registryauflösung, Revisionen, Konsens und Nicht-Konsens
an den realen Sitzungen sowie die fachlich vollständige statische `build/index.html`.

## Deploy

Push auf `master` → GitHub Action baut und rsynct `build/` auf den VPS
(siehe `.github/workflows/deploy.yml`). Caddy serviert das Verzeichnis
statisch; ein Neustart ist nie nötig.
