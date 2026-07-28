> **Archiviert 2026-07-28 (CC) — Kimi-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# Kimi-Baubericht: Asset-Integration + Drei Räume (feat/council-rooms)

**Datum:** 17.07.2026 · **Vorher:** `docs/kimi-analysis.md` (Phase 1, genehmigt)
**Diff-Umfang:** nur `site/` + `docs/` — Tabu-Pfade unberührt (Hook-geprüft, `git status` sauber).

---

## 1) Assets integriert

Sechs freigegebene Bilder (ChatGPT, C2PA `gpt-image` v2.0 verifiziert) verarbeitet:

- **Originale** (byte-identisch, außerhalb Deploy): `docs/asset-originals/media/doors/`
  (2 Tür-Motive, 1086×1448) und `…/media/scenes/` (4 hellere Szenen, 1672×941).
- **Derivate** (einzige Auslieferung): Türen 480×640 q80 → `site/static/media/doors/`
  (54/65 kB); Szenen 1600×900 q70 → `site/static/media/scenes/` (356–593 kB; hellere
  Bilder haben mehr Entropie, q70 hält das Deploy leicht); vier Thumbnails 640×360 q72
  → `…/scene-thumbnails/` (hall/doorway neu hinzugekommen, weil Tür-Kacheln darauf
  verweisen).
- **Ruhestand:** die dunklen Vorgänger-Szenen + alten Thumbnails liegen als Provenienz
  unter `docs/asset-originals/media/provenance/scenes-display-v1/` (byte-exakt aus git
  gesichert; Dateinamens-Kollision Szene/Thumbnail dabei erkannt und durch
  `*-thumbnail.jpg`-Benennung gelöst). Nichts davon wird ausgeliefert.
- **Registry:** `docs/asset-originals/ASSETS.md` fortgeschrieben — Rolle, ChatGPT-
  Dateizuordnung, Prompt-Notiz (A1/A2 aus der Analyse; Szenen-Prompt nicht überliefert,
  visuell freigegeben), Datum, Quelle, C2PA-Hinweis (Originale behalten Credentials,
  `sips`-Derivate strippen sie bewusst), Bytes + SHA-256 aller Dateien.

## 2) Drei Räume gebaut

- **Echte Routen statt Scroll-Bühne:** `/` (Vorzimmer), `/ratssaal/`, `/archiv/` als
  Route-Group `(rooms)` mit einem gemeinsamen `+layout.server.js`, das das geerbte
  View-Model **einmal** lädt (wortgleicher Aufruf wie bisher). Historie ist damit per
  Konstruktion echt: ohne JS normale Seitenaufrufe (MPA), mit JS SvelteKit-Client-Router
  (`pushState`) — Zurück/Vorwärts/Direktaufruf/geteilte Links nativ. Der alte
  IntersectionObserver/Hash/`replaceState`-Code (der Hauptbug) ist vollständig entfernt,
  ebenso `+page.svelte`/`+page.server.js` der Bühne.
- **Datennaht unverändert:** `content.js`, `homepage.js`, `homepage.test.js` byte-identisch.
  Jeder Raum rendert nur seine Scheibe: Vorzimmer = Mechanismus/Legenden/Späher & Wart/
  Beleg-Spur (`wartDossier.search_queries`, verbatim) + Leitfrage; Ratssaal = 4
  Empfehlungen (Konsens + Nicht-Konsens gleichwertig, Zählungen aus `convergence`),
  Zählwerk, 3 Pulte Erst→Schluss, Revisionen (datengetrieben), Vorbehalte, Registry-
  Spendenlinks inkl. `null`-Fall; Archiv = Sitzungsliste, Kosten (Summe + `by_model`),
  Korrekturhinweis, Dissens (`dissentHighlights` als gerahmter Protokoll-Auszug +
  `dissent_md` gerendert in `<details>`), Protokoll-Link.
- **Übergänge:** `onNavigate` + View-Transitions-API, nur Raum-zu-Raum, nur bei
  `prefers-reduced-motion: no-preference` — Zoom-Öffnen 2,4 s vorwärts / 1,4 s zurück;
  sonst sofortiger Wechsel. Kein eigener Zustand, kein Framework.
- **i18n-Grundlage:** alle UI-Strings in `site/src/lib/i18n/de.js` (`strings` als einziger
  Zugriffspunkt); Daten-Namen bleiben in der Datenschicht. Englisch dockt später über
  dieselbe Struktur an.
- **A11y:** genau ein `h1` pro Raum (Test), Türen als echte Links ≥ 44 px mit Alt-Text,
  Embleme `alt=""` (sichtbarer Begriff trägt), Text auf Plaketten/Panels (kontrastsicher),
  Fokus-Ringe, `prefers-reduced-motion` überall respektiert.

## 3) Befund: `door-council-archive` (wie gewünscht nur gemeldet, nicht nachbearbeitet)

Dunkelstes der sechs Bilder: obere Bildhälfte fast Schwarz, die Tür liest sich aus dem
Bild allein nur über die Lichtfuge unten und den Griff. **Im gebauten Kontext** trägt die
Kachel die Anklickbarkeit (Messing-Rahmen, Label-Leiste „Die schlichte Tür · Ins Archiv →",
Hover/Focus-Glow) — funktional ausreichend. **Empfehlung:** bei nächster Generierungsrunde
eine hellere Variante von A2 anfordern; der Kontrast zum deutlich wärmeren A1 ist sonst
auffällig. Keine Bild-Nachbearbeitung vorgenommen.

## 4) Verifikation

- `npm run build` warnungsfrei; `npm test` **11/11 grün** (6 Naht-Unit-Tests unverändert,
  5 Build-Tests ehrlich nachgezogen: je Raum Pflicht-Strings gegen die gebaute Datei,
  genau ein `h1`, Emblem-/Tür-/Szenen-Referenzen + Deploy-Existenz, Negativproben
  Fachbegriff/hartkodierte Revision).
- `npm run preview`: `/`, `/ratssaal/`, `/archiv/`, `/sessions/`, `/sessions/2026-07c/`,
  `/journal/`, `/manifest/`, `/idee/`, `/impressum/` → **200**, Inhalte stichprobiert.
- **Reflow 320/390 vermessen** (CDP, echte Viewports — die CLI-`--window-size`-Falle
  „Minimum 500 px" umgangen): alle sechs Raum/Breite-Kombinationen `innerWidth == docW ==
  320/390`, **null** sichtbar überlaufende Elemente. Drei echte Mobil-Fehler gefunden und
  behoben: Pult-Tabellen (3-Spalten-Mindestbreite → unter 560 px gestapelt), Diff-Hash im
  Korrekturtext (umbrechbares Token → `overflow-wrap: break-word`), geschlossenes
  `<details>` bläht via `content-visibility` das Dokument-`scrollWidth` auf
  (`display:none` im geschlossenen Zustand).
- **Screenshots** in `docs/review/`: je Raum Desktop 1440 + Mobil 320 + Mobil 390,
  No-JS-Grundzustand (`rooms-study-nojs.png`, JS per CDP deaktiviert — Seite vollständig,
  identisch zur JS-Fassung, da rein servergerendert).

## 5) Offene Punkte / Hinweise

- Übergänge (2,4 s) sind Code-geprüft, aber nur im interaktiven Browser erlebbar — per
  Screenshot nicht prüfbar. Kurzer Sicht-Check nach Merge-Freigabe empfohlen.
- Bonus-Screenshot `rooms-archive-nojs.png` fehlt (CDP-Tooling-Hänger bei deaktiviertem
  JS); der No-JS-Nachweis ist durch den Study-Screenshot + die Build-Tests erbracht.
- `vite preview` hält gehashte Assets nach Rebuild nicht zuverlässig vor (404-Falle):
  Preview nach jedem Build neu starten.
- **Kein Commit** erfolgt (lokaler Stand). Vor jedem Push: Squash zu sauberen Einheiten;
  kein Push auf `master`, kein Merge ohne Freigabe.

---

## Nachtrag: Zweisprachigkeit (DE/EN) + generische Teilnehmerzahl

**Mechanik.** Die drei Räume existieren je zweimal: Deutsch unter den unveränderten URLs
(`/`, `/ratssaal/`, `/archiv/`), Englisch gespiegelt unter `/en/`, `/en/council/`,
`/en/archive/`. Alle übrigen Routen (Sitzungen, Journal, Manifest, Idee, Impressum)
bleiben deutsch-only — sie sind der publizierte Rekord. Umgesetzt über drei
Raum-Komponenten (`StudyRoom`/`CouncilRoom`/`ArchiveRoom.svelte`) mit `lang`-Prop;
die sechs Routen sind 5-Zeilen-Wrapper. Texte leben in `site/src/lib/i18n/de.js` und
`en.js` (Schlüssel-für-Schlüssel-Spiegel, Eigennamen The Study/The Council/The Archive
und The Scout/The Warden in beiden Sprachen; deutscher Gloss nur im DE-Modus).
Unterkomponenten erhalten `t` als Prop — kein stiller Globalimport mehr.
Der **Umschalter** ist ein schlichter absoluter Link auf die Schwester-Route
(`siblingPath` in `i18n/index.js`) — funktioniert ohne JS, ist pragerendert und trägt
`hreflang`/`aria-label`. `<html lang>` setzt `site/src/hooks.server.js` routenbasiert
(`%lang%`-Platzhalter in `app.html`); jeder Raum bringt `hreflang`-Alternates
(de/en/x-default→de) mit. Übergänge (`room-transitions.js`) laufen nur innerhalb
einer Sprachfolge — der Sprachwechsel selbst ist ein sofortiger schlichter Wechsel.

**Rekord-Politik.** Sitzungsprosa, Dissens, Korrekturhinweis, Vorbehalte und
Suchanfragen werden nie übersetzt. Im EN-Modus stehen sie unverändert deutsch im
Dokument, maschinell als `lang="de"` markiert, mit kuratiertem Vermerk
„Original protocol in German." (Frage-Panel, Vorbehalt, Korrektur, Dissens) bzw.
„The full protocol is published in German." am Protokoll-Link.

**Organisationsbeschreibungen.** `(rooms)/+layout.server.js` liefert `orgEn`
(Registry-Feld `beschreibung_en` je `organization.id`). Das Feld ist derzeit bei
**0 von 13** Organisationen belegt — die Karten zeigen daher überall den deutschen
Text plus Hinweis „…English translation is being prepared." Die englischen Texte
schreibt Afschin (Content-Kaskade); das Frontend liest das Feld nur.

**Generische Teilnehmerzahl (Option B).** Pulte und Zählstände waren bereits
datengetrieben (`session.participants` → `modelTracks`; `count`/`total` aus
`convergence`) — Audit-Befund: einzige hartkodierte „3" steckte in drei Copy-Stellen.
Jetzt funktional: `study.mechanism(n)`, `study.head.description(n)` (Zahlwörter 1–12
je Locale, darüber Ziffern — „Drei Modelle", künftig „Fünf Modelle"),
`study.lead(families)` mit deduplizierter Familienliste via `Intl.ListFormat`;
Anzeigenamen der Familien (`familyNames` in den Locales, Fallback Rohwert), da die
Daten die Familie klein führen („anthropic" → „Anthropic", „openai" → „OpenAI").
Trennwort der Zählung locale-abhängig (`ofWord`: „von"/„of").

**Bekannter Zukunfts-Touchpoint (bewusst zurückgestellt).** Das Schritt-Label
„Drei Antworten" (`steps[2]`, de/en) und sein Emblem
(`process-three-answers-display.jpg` zeigt wörtlich drei Antworten) werden bei einer
Council-Erweiterung inhaltlich falsch. Nicht angetastet — mit dem Amendment neu
anzufassen (Label + Emblem neu generieren).

**Verifikation.** `npm run build` warnungsfrei; `npm test` **16/16 grün** (6 Naht-Unit-
Tests unverändert, 10 Build-Tests: je Raum × Sprache Pflicht-Strings, Umschalter in
allen sechs Räumen, `html lang`/`hreflang`, genau ein `h1`, Asset-Referenzen +
Deploy-Existenz, Rekord-Assertions: EN-Archiv enthält „Korrektur vom 14.07.2026"
unverändert + Vermerk, orgEn-Fallback-Hinweis sichtbar). `vite preview` neu gestartet:
**11 Routen 200** (6 Räume + Sitzung/Manifest/Idee/Journal/Impressum). Screenshots in
`docs/review/`: `rooms-en-{study,council,archive}-desktop.png` (1440) und
`rooms-en-study-390.png` — EN-Chrome englisch, Rekord deutsch mit Vermerk, Umschalter
sichtbar (mobil klar als „DE"-Pille oben rechts). Kein Commit.

---

## Nachtrag 2: Tafel-Ergebnis, Vollbild-Bühne, Übergänge (R1–R4 + Bildbeschnitt)

**Anlass.** Rückmeldung: Plates wurden je nach Fensterformat beschnitten (`object-fit: cover`
auf `92svh` — bei hohen Fenstern verlor das 16:9-Plate die Seiten). Dazu R1–R4.

**Vollbild-Bühne (alle Räume).** `RoomHero` zeigt das Plate jetzt immer komplett:
Bühne im Blockfluss, `width: min(100%, 1600px, calc(92svh * 16 / 9))`, Bild trägt die
Höhe über sein natürliches Seitenverhältnis — kein Crop, kein Upscale, Letterbox auf
`#05090b` bei extremen Formaten. Zwei reale CSS-Fallen dabei gefunden und behoben:
(1) `container-type: inline-size` auf einem `fit-content`-Element kollabiert die Breite
(Size-Containment) → Bühne bekam explizite Breite; (2) Grid-Track + `min(46rem, %)`-Breite
erzeugte eine Zirkularität, die die Spur auf ~780 px aufblähte (mobil abgeschnitten) →
Hero ist wieder Block-Layout. Drift-Animation entfernt (sie würde beschneiden).
Die Plakette schwebt jetzt: radiale Vignette + `text-shadow`, keine opake Box (R3).

**R1 — Die Tafel trägt das Ergebnis.** Overlay auf der Schiefer-Zone des Study-Plates
(Zone ≈ x 7–47 %, y 8–57 %; Schrift in `cqw`, bildstabil). Inhalt aus
`home.recommendations` (gelesen, nie gezählt): Bereich, Organisation, „X von Y",
Registry-Spendenlink — Kreide-Duktus nur für Labels, Name/Link in klarer ui-sans,
Links ≥ 44 px. Unter 1200 px Viewport wird dasselbe Panel statisch unter dem Bild
gerendert (ein DOM-Knoten, keine Duplikate). Steht pragerendert im HTML — No-JS trägt
die Antwort am Eingang (Screenshot-Nachweis `rooms-study-tafel-nojs.png`).

**R2 — Übergang vermessen, nicht vermutet.** Instrumentierung per CDP (Hook auf
`startViewTransition` + `data-nav-dir`-Lebenszyklus): forward `svt@2423 → fin@4450`
= **2027 ms**, back `2426 → 3650` = **1224 ms** — die Fahrt spielt wie gebaut
(2,0 s / 1,2 s, Zoom 1,3 zum Klickpunkt via `pointerdown`-Origin, Fallback `center`).
Befund vorher: Der Übergang lief auch schon in Phase 2 — er war nur nie visuell
nachgewiesen. **Einschränkung:** `Page.captureScreenshot` im Headless-Brave fotografiert
den Live-DOM, nicht die View-Transition-Pseudo-Ebene — Zwischenframes sind per
Screenshot nicht festhaltbar; der Nachweis ist die Laufzeit-Messung. Reduced-motion
und No-JS bleiben sofortige Wechsel (Code-Guard unverändert).

**R4 — Frage als Zitat.** Klartext-Lead aus den Locales („Die Frage dieser Sitzung —
wörtlich aus dem Protokoll:" / „This session's question — verbatim from the protocol:"),
Sitzungsfrage unverändert in `<blockquote>` mit Zitat-Strich (EN weiter `lang="de"` +
recordNote). Keine Paraphrase.

**Verifikation.** Build warnungsfrei; `npm test` **16/16 grün** (Build-Test ehrlich
erweitert: Tafel-Inhalte DE/EN inkl. „3 von 3"/„3 of 3" + Registry-Link auf der
Startseite, `questionLead`, `<blockquote>`). 11 Routen 200. Reflow 320/390 auf allen
sechs Raum-Routen: `docW == Viewport`, null Überlauf (12/12). Screenshots in
`docs/review/`: `rooms-{study-tafel,en-study-tafel}-desktop.png`,
`rooms-{council,archive}-vollbild-desktop.png`, `rooms-study-tafel-390.png`,
`rooms-study-tafel-nojs.png`. Nur `site/` + `docs/review/` + dieser Bericht;
Datennaht unangetastet. Kein Commit.
