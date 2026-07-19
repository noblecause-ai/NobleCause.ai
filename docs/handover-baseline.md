# Übergabe-Baseline — IST-Zustand der Startseite (feat/council-rooms)

**Zweck:** Gemeinsamer, verifizierter Ausgangsstand für den Drei-Wege-Vergleich
(Kimi / Claude Code / Codex). Dieses Dokument beschreibt ausschließlich, **was
ist** — keine Konzepte, keine Empfehlungen, keine Bewertungen von Lösungswegen.
Ein eigener Entwurf von Kimi liegt als `docs/kimi-buehnenspiel-plan--SKIP.md`
im Branch; er ist **nicht** Teil dieser Baseline und soll übersprungen werden.

**Stand:** Branch `feat/council-rooms` (Basis: `sol/nachbesserung` #12 via
`feat/immersive-homepage`). Verifiziert am 19.07.2026: `npm run build`
warnungsfrei, `npm test` 16/16 grün, 11 Routen HTTP 200. Arbeitsregeln und
Tabu-Pfade: `AGENTS.md` (maßgebend), Kurzfassung in §8.

---

## 1) Routen und Räume

Die Startseite besteht aus **drei Räumen, je zweisprachig** — sechs vollständig
pragerenderte Seiten (adapter-static, es gibt keine Scroll-Bühne und keinen
per JS versteckten Wahrheitsblock mehr):

| Deutsch (Default) | Englisch | Raum |
|---|---|---|
| `/` | `/en/` | The Study (Vorzimmer) — Einstieg, Ergebnis-Tafel, Prozess, Dossiers |
| `/ratssaal/` | `/en/council/` | The Council — Empfehlungen, Revisionen, Zählwerk, Voten |
| `/archiv/` | `/en/archive/` | The Archive — Sitzungsliste, Kosten, Korrektur, Dissens |

Übrige Routen (publizierter Rekord, **deutsch-only**): `/sessions/`,
`/sessions/<id>/`, `/journal/`, `/manifest/`, `/idee/`, `/impressum/`.
Sprachumschalter: schlichter Link auf die Schwester-Route (pragerendert,
funktioniert ohne JS), `<html lang>` routenbasiert via `site/src/hooks.server.js`
(`%lang%`-Platzhalter in `app.html`), `hreflang`-Alternates je Raum.
**Rekord-Politik:** Sitzungsprosa, Dissens, Korrekturhinweise, Voten-Texte,
Suchanfragen werden nie übersetzt — im EN-Modus stehen sie deutsch mit
`lang="de"` und Vermerk („Original protocol in German.").

Historie ist per Konstruktion echt: ohne JS normale Seitenaufrufe (MPA), mit
JS der SvelteKit-Client-Router — Zurück/Vorwärts/Direktaufruf/geteilte Links
nativen Verhaltens.

## 2) Dateistruktur (site/src)

```
site/src/
├─ app.html                      # %lang%-Platzhalter, Grundgerüst
├─ hooks.server.js               # setzt html lang je Route
├─ routes/
│  ├─ +layout.svelte             # Site-Rahmen (Header/Footer, globale Styles)
│  ├─ +layout.js
│  ├─ +error.svelte
│  ├─ (rooms)/                   # Route-Group: die drei Räume (kein URL-Anteil)
│  │  ├─ +layout.server.js       # EIN Load für alle Räume (View-Model + orgEn
│  │  │                          #   + questionSummary + gerendertes dissent/correction)
│  │  ├─ +layout.svelte          # Raum-Chrome: Sprachumschalter (fixed), Scrim,
│  │  │                          #   Ausweich-Spalte ≥1200 px, Footer, View-Transition-CSS
│  │  ├─ +page.svelte            # The Study (DE)
│  │  ├─ ratssaal/+page.svelte   # The Council (DE)
│  │  ├─ archiv/+page.svelte     # The Archive (DE)
│  │  └─ en/{,+page.svelte,council/+page.svelte,archive/+page.svelte}
│  ├─ sessions/…  journal/…  manifest/…  idee/…  impressum/…
├─ lib/
│  ├─ server/
│  │  ├─ content.js              # VERSIEGELT — Repo-Leser (sessions, journal, Registry)
│  │  └─ homepage.js             # VERSIEGELT — View-Model (Registry-Auflösung, keine Neuzählung)
│  ├─ i18n/{de.js,en.js,index.js}# Chrome-Texte, Schlüssel-für-Schlüssel-Spiegel;
│  │                             #   index.js: roomPaths, langOfPath, siblingPath
│  ├─ room-transitions.js        # onNavigate + View-Transitions-API (nur Enhancement)
│  └─ components/rooms/
│     ├─ RoomHero.svelte         # fixe Vollbild-Bildebene (position:fixed, 100svh,
│     │                          #   object-fit:cover), Plakette (eyebrow/h1/lead), Overlay-Slot
│     ├─ ResultBoard.svelte      # Ergebnis-Tafel (Schiefer-Panel, rem; ≥1200 px fixed
│     │                          #   oben links, darunter erstes Fluss-Element) — liest
│     │                          #   home.recommendations, nie neu gezählt; Prop emphasizeCount
│     ├─ FlowRail.svelte         # Prozess-Leiste, 6 Schritte (Schritt 3 trägt
│     │                          #   Teilnehmerzahl aus den Daten als Funktion von n)
│     ├─ StudyRoom.svelte        # Studie: Tafel, FlowRail, Frage-Dossier (Klartext-
│     │                          #   Kontext sichtbar + Frage wörtlich hinter details),
│     │                          #   Recherche-Dossier, Tür-Karten, Tür-Hotspot im Bild
│     ├─ CouncilRoom.svelte      # Council: h1+Erklärtext (datengetrieben), Tafel,
│     │                          #   FlowRail, Ein-Zeilen-Empfehlungen (Vorbehalt hinter
│     │                          #   details), Revisionen → Zählwerk → Pulte hinter details
│     ├─ ArchiveRoom.svelte      # Archiv: Sitzungen, Kosten, Korrektur, Dissens (details)
│     ├─ ModelPulpits.svelte     # Voten-Matrix je Modell (Erst/Schluss), N aus Daten
│     ├─ RecommendationCard.svelte # derzeit UNREFERENZIERT (Council entrümpelt) —
│     │                          #   hier lebt der orgEn-Mechanismus (beschreibung_en-
│     │                          #   Fallback), bewusst im Repo belassen
│     ├─ Door.svelte             # Tür-Karte (Bild-Kachel als echter Link, ≥44 px)
│     └─ EmblemLegend.svelte     # (Altbestand, von den Räumen nicht mehr referenziert)
```

Zentrale Konventionen: Räume bekommen `home` und `lang` als Props; Texte nur aus
`locales[lang]` (kein stiller Globalimport in Unterkomponenten — `t` wird
weitergereicht). Daten-Namen (Organisationen, Bereiche) kommen aus der
Datenschicht, stehen bewusst NICHT in den Locales.

## 3) Die versiegelte Datenschicht

`site/src/lib/server/content.js` + `homepage.js` werden **nur gelesen, nie
editiert** (gleiche Schutzstellung wie die Tabu-Pfade). Grundprinzip: Das
View-Model wird **einmal** in `(rooms)/+layout.server.js` gebaut
(`buildHomepageViewModel({session, sessions, registry})`, wortgleicher Aufruf wie
auf der alten Startseite); jeder Raum rendert nur seine Scheibe. **Das Frontend
aggregiert nie neu** — Zählstände kommen aus `convergence`, Empfehlungen aus
`recommendations`, Voten aus `rounds[].votes[].recommendations[]`; Prosa wird nie
geparst. Organisationen werden **registry-aufgelöst** (`organizations.json`,
Schlüssel `organization.id`; `resolveOrganization` wirft bei unbekannter ID und
bei Widerspruch zwischen Votums- und Registry-Name).

View-Model (`home`): `currentSession{id,number,date,title,question}`,
`recommendations[]` (Konsens: `organization{name,description,donationUrl}`,
`count/total/conditionalCount` aus convergence, `reservations[]`; Nicht-Konsens:
`votes[]` registry-aufgelöst), `modelTracks[]` (je Teilnehmer `rows[]` Erst→Schluss
mit `changed`-Flag), `revisions[]` (abgeleitet aus modelTracks),
`correction`, `dissent` (roh), `dissentHighlights[]`, `costs`, `wartDossier`,
`archive[]` (Sitzungsliste inkl. `nonConsensusPillars`). Der Layout-Load reicht
zusätzlich durch: `orgEn` (Registry-Feld `beschreibung_en` je ID, derzeit 0/13
belegt — Fallback deutscher Text + Hinweis), `correctionHtml`/`dissentHtml`
(markdown-gerendert, Wortlaut unverändert), `questionSummary`
(`session.summary`, kuratierter Protokoll-Kontext, wörtlich).

**Eigenheiten des Datenvertrags** (Details: `sol-build/data-contract.md`,
`docs/handoff-notes-for-codex.md`):
- `recommendations[].rationale_md` ist **maschinelles Boilerplate** (nur die
  Zähl-Zusammenfassung, kein redaktioneller Text).
- `dissent_md` und `correction_notice.text` sind **Roh-Markdown** mit literalen
  `**` und ganzen ```` ```json ````-Blöcken, mehrere Bildschirmhöhen — rendern +
  hinter `<details>` falten, nie verbatim dumpen, Wortlaut nie ändern.
- `donation_url` kann `null` sein (`pratham`, `tarl-africa`,
  `global-road-safety-partnership`) — UI muss den Fall ohne Link tragen.
- **Jüngste Sitzung nach `number`**, nicht nach Datum (alle drei Sitzungen
  teilen ein Datum; datumsbasierte Auswahl war ein Zufalls-Bug).
- Voten IMMER strukturiert aus `rounds[].votes[].recommendations[]` —
  `content_md` ist nur Anzeige-Prosa.
- Konditionale Voten: `convergence.conditional_count`, je Votum `conditional`
  + `reservation` (zählt zum Konsens, ist aber markiert).
- Kosten liegen **inline** in `session.json` unter `costs` (kein `kosten.json`).
- `correction_notice` existiert in 2026-07b und 2026-07c, nicht in 2026-07.

## 4) Assets

Ausgeliefert wird nur `site/static/media/` (leichte `*-display.jpg`-Derivate):
- `scenes/` — Raum-Plates (antechamber/hall/archive landscape, antechamber/
  archive portrait, doorway); Council-Portrait-Slot ist bewusst Platzhalter.
- `doors/` — zwei Tür-Motive (480×640) für Tür-Karten.
- `pillars/` (4), `process/` (6) — farbige Embleme.
- `scene-thumbnails/` — Kacheln für Tür-Karten.

**Originale + Provenienz** liegen außerhalb des Deploy-Pfads unter
`docs/asset-originals/` (`media/`, `media/provenance/` inkl. der dunklen
Vorgänger-Fassungen). Registry: `docs/asset-originals/ASSETS.md` (Rolle, Quelle/
ChatGPT-Datei, Prompt-Notiz, Datum, Bytes, SHA-256, C2PA-Hinweis). C2PA: die
PNG-Originale tragen Content Credentials (`gpt-image` v2.0) — nicht strippen;
die `sips`-Derivate verlieren sie bewusst (Anzeige-Derivate, Neucodierung
unkritisch). `sips` kann lokal kein WebP — Derivate sind JPEG.

## 5) Testnetz

- **`site` (Node, `npm test` = `node --test src/lib/server/homepage.test.js
  tests/homepage-build.test.js`, pretest baut):** 16 Tests.
  - 6 Unit-Tests an der Daten-Naht (`homepage.test.js`) — unverändert geerbt.
  - 10 Build-Tests gegen die **gebauten HTML-Dateien** in `site/build/`: je
    Raum × Sprache Pflicht-Strings (Empfehlungen, Zählstände „3 von 3"/„3 of 3",
    Registry-Spendenlinks, Revisionen, Zählwerk, Geldfluss, Klartext-Kontext +
    Frage wörtlich, Tür-Hotspot), Umschalter + `html lang` + `hreflang` in allen
    sechs Räumen, genau **ein h1** je Raum, Asset-Referenzen + Deploy-Existenz,
    Negativproben (keine Amtssprache, kein hartkodierter Revisions-Text),
    Voten-Reihenfolge (Revisionen vor Matrix).
  - **Ehrlicher No-JS-Test:** die Prüfung läuft gegen das pragerenderte HTML —
    was darin steht, trägt ohne JavaScript. Es gibt keinen zweiten, JS-versteckten
    Wahrheitsblock (der alte Doppelbau ist entfernt).
- **Golden-Tests (Repo-Wurzel, pytest):** `tests/golden/test_golden_aggregation.py`
  (Aggregations-Ergebnisse byte-stabil) und `test_golden_determinism.py`
  (Determinismus, u. a. Sitzungswahl nach Nummer). `conftest.py` isoliert den
  Registry-Global pro Test (sonst reihenfolgeabhängig rot — Beleg im Kommentar).
  Ausführung: `pytest` aus der Repo-Wurzel (venv in `gremium/.venv`).

## 6) Deploy

`.github/workflows/deploy.yml`: push auf **master** → Runner (ubuntu, Node 22)
`npm ci && npm run build` in `site/` (adapter-static → `site/build/`) →
`rsync -avz site/build/` → `noblecause@185.143.100.222:/srv/noblecause/` →
**Caddy** liefert statisch aus (kein Restart, kein Healthcheck). `prebuild`
kopiert `schedule.json` nach `site/static/`. Deployt wird ausschließlich
`site/build/`; `sol-build/` (alter Python-Renderer) ist NICHT der Deploy-App.
Deploy passiert erst beim Merge auf master — nie aus einem Feature-Branch.

## 7) Randbedingungen und FALLEN (hart erkämpft)

Jede Zeile hier hat bereits einmal Zeit gekostet — bitte nicht erneut „entdecken":

1. **Zurück-Button / `replaceState` (der Hauptbug der alten Bühne):** Die
   Scroll-Bühne simulierte Räume per IntersectionObserver + Hash + `replaceState`
   — Zurück/Vorwärts/Direktlinks waren kaputt. **Gilt jetzt:** echte Routen
   (MPA ohne JS, Client-Router mit JS), kein eigener Navigationszustand, kein
   `replaceState` für Räume.
2. **`container-type: inline-size` auf `fit-content`-Element kollabiert die
   Breite** (Size-Containment) — die Bühne brach zusammen; Elemente mit
   Container-Type brauchen explizite Breite.
3. **Grid-Track + `min(46rem, %)`-Breite = Zirkularität** — die Spur blähte sich
   auf (~780 px, mobil abgeschnitten); Hero ist bewusst Block-Layout.
4. **fixed-Ebene mit `z-index:-1` verschwindet hinter dem Shell-Hintergrund.**
   Funktionierendes Muster (RoomHero/Layout): Bild `position:fixed; z-index:0`;
   `main`/Footer `position:relative` + Hintergrund (früher deckend, heute
   transluzenter Scrim) scrollen darüber.
5. **svh/vw-Pixelkette an das Bild erzeugt springende Schriftgrößen**
   (Ultrawide): Tafel-Overlay war in vier svh/vw-Regimen ans Plate gekettet.
   Gilt jetzt: Overlays sind eigenständige rem-Panels, **nicht** an Bildpixel
   gekettet (einzige bewusste Ausnahme: der Deko-Tür-Hotspot, der die gemalte
   Tür trifft — er trägt nie allein Navigation).
6. **Doppelbau Fallback+Bühne:** die alte Seite pflegte einen separaten,
   per JS versteckten No-JS-Wahrheitsblock — doppelte Pflege, driftete
   auseinander. Gilt jetzt: **ein** pragerenderter Wahrheitsgehalt; JS ist
   ausschließlich Enhancement (Default-Zustand = alles sichtbar).
7. **`object-fit: cover` schneidet Randmotive weg:** der Tür-Hotspot liegt im
   Study-Plate bei x 86–99 % — unter Seitenverhältnis ~2,1 ist die Tür im
   Cover-Ausschnitt schlicht nicht da (Hotspot dann `display:none`, Tür-Karten
   tragen die Navigation). Konsequenz: was im Bild zuverlässig sichtbar sein
   soll, gehört in die Bildmitte; jede In-Bild-Navigation braucht immer einen
   echten Link zusätzlich.
8. **`vite preview` (sirv) cacht Verzeichnisliste/gehashte Assets** — nach jedem
   Build Preview neu starten, sonst 404-/Stale-Fallen.
9. **Headless-Browser-`--window-size` hat ein Minimum (~500 px; Brave klemmt
   bei ~347 px)** — echte 320/390-Reflows per CDP-Emulation
   (`Emulation.setDeviceMetricsOverride`, bei 320 `mobile:true`) messen, nicht
   per Fenstergröße.
10. **`Page.captureScreenshot` fotografiert den Live-DOM, nicht die
    View-Transition-Pseudo-Ebene** — Zwischenframes einer Fahrt sind per
    Screenshot nicht festhaltbar; Übergänge per Instrumentierung
    (`startViewTransition`-Hook, Zeitstempel) messen (Zielwerte bisher ~2,0 s
    vorwärts / ~1,2 s zurück).
11. **Geschlossenes `<details>` + `content-visibility` bläht `scrollWidth`** —
    im geschlossenen Zustand `display:none` setzen (Mobil-Overflow-Bug).
12. **Node 20 hat kein WebSocket** — CDP-Helferskripte (Screenshots, Messungen)
    brauchen Node ≥ 22 (lokal: `/opt/homebrew/opt/node@22/bin`).

Harte Randbedingungen, die aus diesen Fallen folgen: No-JS-Vollwahrheit jedes
Zustands; `prefers-reduced-motion` ⇒ sofortiger Wechsel ohne jede Animation;
ein wirksames h1 je Seite; Tippziele ≥ 44 px; Reflow 320/390 ohne Überlauf;
Kontraste ≥ AA auf Panels/Scrims.

## 8) Tabu-Pfade, Guard-Hook, Arbeitsregeln

**Niemals anfassen** (`AGENTS.md`, „HARTE GRENZE"): `sessions/**`, `journal/**`,
`schedule.json`, `gremium/**`, `schema/**`, `prompts.py` / `**/prompts.py`.
Ein `pre-commit`-Hook (`.git/hooks/pre-commit`) blockt auf
`feat/immersive-homepage*` und `feat/council-rooms*` jeden Commit, der diese
Pfade berührt. Erlaubt ist die Präsentationsebene: `site/`, `docs/`, statische
Assets. Die Datenschicht (`content.js`, `homepage.js`) wird wie eine Tabu-Datei
behandelt (nur lesen). Scheint eine Aufgabe eine Änderung an Tabu-Pfaden zu
verlangen: stoppen und melden, nicht umgehen.

Arbeitsregeln: nie Push auf `master`, nie Merge ohne ausdrückliche Freigabe;
Deploy erst beim Merge. Im Feature-Branch frei committbar; vor GitHub/master
wird zu sauberen Einheiten gesquasht. Review lokal (statischer Server aus dem
Build), aus echten Daten rendern. Kein Netzzugriff nach außen ohne Nachfrage.
Kein erfundenes „Warum": die Darstellung paraphrasiert/übersetzt/aggregiert
keine publizierten Inhalte.

## 9) Lokal bauen, testen, reviewen

```bash
cd site
npm ci                      # einmalig
npm run build               # adapter-static → site/build/ (muss warnungsfrei sein)
npm test                    # baut vor (pretest); 16/16 erwartet
npm run preview -- --port 4173   # Review-Server; NACH JEDEM BUILD NEU STARTEN (sirv-Cache)
```

Routen-Check: `curl -o /dev/null -w '%{http_code}' http://localhost:4173/ratssaal/`
usw. (11 Routen: 6 Räume + `/sessions/2026-07c/`, `/manifest/`, `/idee/`,
`/journal/`, `/impressum/`). Screenshots/CDP-Messungen: Brave headless mit
`--remote-debugging-port=9222`, Helferskripte per Node ≥ 22
(`/opt/homebrew/opt/node@22/bin`); Review-Bilder ablegen unter `docs/review/`.

## 10) Bewusst NICHT in diesem Dokument

Alles, was ein künftiges Konzept betrifft. Der Kimi-Entwurf liegt als
`docs/kimi-buehnenspiel-plan--SKIP.md` bei — lesen oder nicht, aber nicht als
Baseline missverstehen. Die Vergleichs-Arbeiten sollen unabhängig entstehen.
