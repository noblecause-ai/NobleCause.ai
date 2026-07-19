# Kimi-Analyse: Drei-Räume-Umbau der Startseite (feat/council-rooms)

**Status:** Phase 1 — Analyse und Plan. Keine Quelldatei außer diesem Dokument geändert.
**Arbeitsnamen → UI-Namen (Seite ist deutsch, Verfassungssprache):** The Study = **Vorzimmer**
(„Belege"), The Council = **Ratssaal** („Beratung"), The Archive = **Archiv**
(„Veröffentlicht"); The Scout = **Späher**, The Warden = **Wart**.

---

## 0) Zusammenfassung (vorab, wie verlangt)

Ich erbe eine verifizierte, unangetastete Datennaht: `site/src/lib/server/content.js`
(Loader, „jüngste Sitzung" deterministisch nach `number`) und `site/src/lib/server/
homepage.js` (View-Model, das `recommendations[].convergence` **liest** — „3 von 3" kommt
aus dem Zählwerk der Sitzung, nie aus einer Frontend-Schleife —, Voten über
`organization.id` registry-auflöst und bei Widersprüchen hart wirft), dazu den Unit-Test
`homepage.test.js` und die bereits integrierten Embleme (4 Säulen-, 6 Prozess-Zeichen) und
vier Szenen-Plates. Ich fasse **nicht** an: `sessions/**`, `journal/**`, `schedule.json`,
`gremium/**`, `schema/**`, `prompts.py` (Hook-erzwungen), und ich aggregiere im Frontend
nichts neu — die Startseite visualisiert die publizierte Zählung, sie erzeugt keine. Den
Hauptbug (acht Scroll-Szenen, die per `history.replaceState` nur einen Hash umschreiben —
kein History-Eintrag, kaputtes Zurück/Vorwärts, fragiler Deep-Link-Scroll-Sync) löse ich
durch **drei echte, pragerenderte Routen**: `/` (Vorzimmer), `/ratssaal/`, `/archiv/` —
damit sind Zurück, Vorwärts, Direktaufruf und geteilte Links ohne eigene Zustandsmaschine
natürlich korrekt, ohne JS als normale Seitenaufrufe, mit JS über SvelteKits Client-Router
(echte History-Einträge). Ohne JavaScript steht die **ganze Wahrheit** als vollständig
gerendertes HTML in den drei Seiten; JS liefert ausschließlich den Tür-Übergang
(View-Transitions-API, ~2,4 s, bei `prefers-reduced-motion` oder fehlender API sofortiger
Wechsel). Die Raum-Inhalte sind exakt die Scheiben des bestehenden View-Models, verteilt
nach dem Brief: Belege/Mechanismus/Legenden ins Vorzimmer, Empfehlungen/Voten/Revisionen/
Vorbehalte/Spendenlinks in den Ratssaal, Sitzungen/Kosten/Korrektur/Dissens/Protokoll-Link
ins Archiv. Fehlende Tür-Bilder (zwei schlichte Archivtüren) spezifiziere ich als präzise
Asset-Anforderungen (etwas heller als der sehr dunkle Bestand, gleiche
Bernstein/Messing-gegen-Mondblau-Handschrift) — erfunden wird nichts.

---

## 1) Verifikation des Briefs am echten Code

| # | Aussage (Brief/Handoff) | Befund | Beleg |
|---|---|---|---|
| 1 | Heutige Startseite = eine Scroll-Bühne, 8 Szenen | ✔ exakt: `arrival, recommendations, door-opening, antechamber, initial, revision, count, archive` | `site/src/routes/+page.svelte:10` |
| 2 | `content.js` lädt jüngste Sitzung nach `number`, nicht Datum | ✔ `listSessions()` sortiert `(number desc, date)`; Kommentar begründet Determinismus; `getLatestSession()` = `[0]` | `content.js:37–41, 57–61` |
| 3 | `homepage.js` liest `recommendations`/`convergence`, zählt nie selbst | ✔ `count/total/conditional_count` werden **durchgereicht**; nirgends eine Zähl-Schleife über Voten für Konsensstände | `homepage.js:77–109` |
| 4 | Revisionen aus strukturierten Voten via `organization.id`, nicht aus Prosa | ✔ `buildModelTracks` vergleicht Erst-/Schlussvotum je Säule über `organization.id`; Registry-Name wird gegen Votums-`organization` verifiziert (Wurf bei Widerspruch) | `homepage.js:29–75` |
| 5 | Embleme integriert: `pillar-*` ×4, `process-*` ×6 | ✔ je 320×320 px JPG, im Fallback **und** auf der Bühne referenziert | `site/static/media/{pillars,process}/` |
| 6 | Szenen-Plates `scenes/{antechamber,hall,archive,doorway}-display.jpg` | ✔ je 1600×900 px, 200–365 KB | `site/static/media/scenes/` |
| 7 | `donation_url` kann `null` sein | ✔ `pratham`, `tarl-africa`, `global-road-safety-partnership` (13 Orgs gesamt) | `organizations.json` |
| 8 | `dissent_md`/`correction_notice.text` = Roh-Markdown, rendern statt dumpen | ✔ 6 941 Zeichen (2026-07c); `+page.server.js` rendert via `marked` zu `dissentHtml`/`correctionHtml`; Wortlaut unangetastet | `+page.server.js:18–19` |
| 9 | Kosten inline in `session.json.costs` | ✔ EUR 2,60 gesamt, `by_model` inkl. „Der Wart (Fable)" mit `web_search_requests` | `sessions/2026-07c/session.json` |
| 10 | Deploy = adapter-static → `site/build/` → rsync → Caddy | ✔ `svelte.config.js` (strict, `handleHttpError:'fail'`), Workflow baut in `site/` und rsynct; `+layout.js`: `prerender=true`, `trailingSlash='always'` | `.github/workflows/deploy.yml` |
| 11 | No-JS-Test prüft gegen den sichtbaren Fallback-Block | ✔ schneidet `class="home-fallback"` bis `class="council-stage"` aus `build/index.html` und prüft 18 Pflicht-Strings + Emblem-Deploy | `site/tests/homepage-build.test.js` |
| 12 | Tabu-Pfade per pre-commit-Hook auf diesem Branch geblockt | ✔ Hook matcht `feat/council-rooms*`, rc=1 | `.git/hooks/pre-commit` |

**Zusatzbefunde (nicht im Brief, relevant):**
- `HeroGraphic.svelte` wird nirgends importiert (Altlast; bleibt unberührt, kein Handlungsbedarf).
- `dissentHighlights` (5 kuratierte Stichpunkte) steht im View-Model, wird auf der Startseite
  **nirgends gerendert** — ebensowenig `wartDossier` und `summary` (siehe §7).
- `sessions/[id]/+page.svelte` liefert die Anker `#wart-dossier` und `#vollprotokoll` —
  Ziele für Raum-Links bereits vorhanden.
- `scene-thumbnails/` (antechamber, archive; 640×360) existiert; `provenance/` ist leer.

### Der Hauptbug, präzise lokalisiert
`+page.svelte:29–63`: ein `IntersectionObserver` über einem 800-vh-`.scene-track` setzt
`scene` und ruft `history.replaceState(null,'','#'+scene)` auf — **replace**, also entsteht
pro Szene kein History-Eintrag; Zurück/Vorwärts springt nicht zwischen Szenen. Deep-Links
(`#revision` u. ä.) erzwingen einen `scrollTo`-Re-Sync gegen den Scroll-Controller
(`+page.svelte:47`), Hash-Änderungen und Observer konkurrieren um denselben Zustand. Die
„Navigation" ist gleichzeitig Scrollposition, Hash und JS-Variable — drei Wahrheiten, keine
davon die des Browsers. Unter 800 px kippt die Bühne ohnehin in eine statische Flex-Liste.
**Konsequenz:** kein Fix dieses Konstrukts, sondern Ersatz durch echte URLs.

---

## 2) Ziel-Architektur: drei Räume als drei Routen

```
GET /            Vorzimmer (The Study)     — Einstieg: Leitfrage, Mechanismus, Späher & Wart,
                                             Belege, Säulen-Legende (4), Prozess-Legende (6)
GET /ratssaal/   Ratssaal (The Council)    — 4 Empfehlungen (Konsens + Nicht-Konsens
                                             gleichwertig), Zählwerk, 3 Pulte Erst→Schluss,
                                             Revisionen, Vorbehalte, Spendenlinks
GET /archiv/     Archiv (The Archive)      — Sitzungsliste, Kosten, Korrekturhinweis,
                                             Dissens-Zugang, Protokoll-Link
```

**Warum Routen statt Zustände-in-einer-Seite:** Jeder Raum ist eine eigene, statisch
pragerenderte URL. Damit ist die Browser-Historie **per Konstruktion** echt:
- **Ohne JS:** Türen sind `<a href>`; jeder Raum ein vollständiges HTML-Dokument (MPA).
  Zurück/Vorwärts/Direktaufruf/geteilte Links = natives Browser-Verhalten. Nichts davon
  hängt an JavaScript.
- **Mit JS:** SvelteKits Client-Router fängt interne Links ab, navigiert per History-API
  (`pushState`) — dieselben URLs, dieselben Einträge, Zurück/Vorwärts funktionieren
  identisch. Es gibt **keinen** selbstverwalteten Raum-Zustand, keinen Hash, keinen
  Scroll-Controller.

**URL-Benennung:** deutsch (`/ratssaal/`, `/archiv/`), konsistent zu `/sessions/`,
`/journal/`, `/manifest/` und zur Verfassungssprache. Die englischen Namen aus dem Auftrag
bleiben Arbeitsnamen. (Alternative `/council/`, `/archive/` möglich — Entscheidung vor Bau.)

**Datenfluss (unveränderte Naht, nur verteilt):**

```
sessions/*/session.json ─┐
organizations.json ──────┼─► content.js (Loader) ─► homepage.js buildHomepageViewModel()
                         │                                    │  (einzige Aggregation,
                         │                                    │   heute wie morgen)
                         ▼                                    ▼
              Route-Group (rooms): +layout.server.js lädt EINMAL { home } —
              /, /ratssaal/, /archiv/ rendern je ihre Scheibe desselben View-Models.
              dissentHtml/correctionHtml weiterhin per marked im Server-Load.
```

Eine Route-Group `src/routes/(rooms)/` mit gemeinsamem `+layout.server.js` verhindert, dass
der verifizierte Builder-Aufruf dreifach kopiert wird; er bleibt wörtlich derselbe Aufruf
wie heute in `+page.server.js`. **Kein neues Aggregat, keine neue Zählung, kein Prosa-Parsen.**

**No-JS-Vollwahrheit, neu verteilt (ersetzt den heutigen Doppelbau Fallback+Bühne):**
- Heute: `home-fallback` (Wahrheit) + `council-stage` (display:none bis `.stage-ready`) —
  dieselbe Wahrheit zweimal im DOM.
- Geplant: Jede Raum-Seite **ist** ihr servergerendertes HTML; es gibt keinen JS-versteckten
  Wahrheitsblock mehr. Die Pflichtliste aus dem Brief landet raum-genau:
  - Vorzimmer: h1/Leitfrage, Mechanismus in zwei Sätzen, Späher & Wart, Beleg-Zugang,
    beide Legenden mit Emblemen.
  - Ratssaal: vier Empfehlungen mit Zählungen (`convergence`), „Keine zwei gleichen
    Nennungen"-Fall mit Einzelvoten, Vorbehalte, Erst- **und** Schlussvoten je Modell,
    Revisionen, Spendenlinks (Registry-only; `null` → „Kein kuratierter Spendenweg."),
    „Kein Geld fließt über NobleCause."
  - Archiv: Sitzungsarchiv mit Nicht-Konsens-Markierung, Kosten, Korrekturhinweis,
    Dissens-Zugang (geklappt, marked-gerendert), Link zum vollständigen Protokoll.
- `homepage-build.test.js` wird **ehrlich nachgezogen**: statt des String-Schnitts
  `home-fallback…council-stage` prüft er die drei gebauten Dateien `build/index.html`,
  `build/ratssaal/index.html`, `build/archiv/index.html` gegen die jeweilige Pflichtliste
  (inkl. `3 von 3`, `2 von 3`, `giving.helenkellerintl.org`, `Unter Vorbehalt`,
  `Korrekturhinweis`, `Sitzung 1`, `/sessions/2026-07c/`, Emblem-Referenzen + Deploy-
  Präsenz, Negativprobe „unerklärter Fachbegriff"). Sichtbarkeits-Logik gibt es nicht mehr
  — der Test prüft weiterhin genau das, was ohne JS im Dokument steht.

**Datei-Plan (alles unter `site/`, erlaubte Präsentationsebene):**
```
site/src/routes/(rooms)/+layout.server.js   home-View-Model einmal laden (wie +page.server.js heute)
site/src/routes/(rooms)/+layout.svelte      Raum-Rahmen: Vollbild, Raum-Chrome, Tür-Nav
site/src/routes/(rooms)/+page.svelte        Vorzimmer (ersetzt heutiges +page.svelte; alter
                                            +page.server.js entfällt zugunsten des Group-Loads)
site/src/routes/(rooms)/ratssaal/+page.svelte
site/src/routes/(rooms)/archiv/+page.svelte
site/src/lib/components/rooms/*.svelte      Door, Plaque, PulpitRow, CountingMachine, …
site/src/lib/nav.js (o. ä.)                 onNavigate → View Transition (progressive Enhancement)
site/tests/homepage-build.test.js           ehrlicher Nachzug (s. o.)
site/static/media/doors/*.jpg               NEUE Tür-Kunst (§5)
```
`+layout.svelte` (Root) verliert die `.page:has(.council-stage)`-Sonderregeln; die Raum-Group
bekommt einen eigenen Chrome ohne Site-Header/Footer (wie heute die Bühne). `+layout.js`
(`prerender`, `trailingSlash`) bleibt. Der 800-vh-`.scene-track`, der IntersectionObserver,
`replaceState`- und Deep-Link-Sync-Code entfallen vollständig.

---

## 3) Reuse-Matrix

**UNVERÄNDERT übernommen (geerbt, kein Edit):**
- `site/src/lib/server/content.js` — Loader inkl. Nummern-Determinismus.
- `site/src/lib/server/homepage.js` — View-Model: `recommendations` (convergence-Durchreichung),
  `modelTracks` (Erst/Schluss via `organization.id`), `revisions`, `correction`, `dissent`,
  `dissentHighlights`, `costs`, `wartDossier`, `archive` + `nonConsensusPillars`, Würfe bei
  `unresolved_votes`/Namenswiderspruch. **PILLARS-Mapping bleibt die einzige Namensquelle.**
- `site/src/lib/server/homepage.test.js` — Unit-Vertrag der Naht.
- marked-Renderweg für `dissent_md`/`correction_notice.text` (Server-Load, Wortlaut unverändert).
- Embleme `pillars/*`, `process/*` (320²) — weder regeneriert noch neu gefärbt.
- Szenen-Plates `scenes/*-display.jpg` als Raum-Hintergründe (antechamber→Vorzimmer,
  hall→Ratssaal, archive→Archiv; doorway als Motiv im Übergang/den Tür-Karten, solange keine
  neue Kunst existiert).
- Registry-Auflösung inkl. `donation_url:null`-Fall; Sessions-Routen und deren Anker
  (`#wart-dossier`, `#vollprotokoll`) als Linkziele; Deploy-Pipeline unverändert.

**Ersetzt (nur Präsentation):**
- `src/routes/+page.svelte` (Scroll-Bühne, 449 Z.) → drei Raum-Seiten + Group-Layout.
- Der Doppelbau „Fallback + versteckte Bühne" → „jede Seite ist ihre eigene Wahrheit".
- Hash-/Scroll-Navigation → echte URLs; IntersectionObserver → entfällt.
- `homepage-build.test.js` → gleiche Strenge, neue Schnittstelle (drei Dateien).
- Raum-CSS neu (aus den Layout-Tokens: `--bg/#080c0e`, Bernstein `#d7aa55`, Mondblau
  `#8bb7ca`), nicht 1:1 aus der Bühne übernommen — die Bühne ist Vollbild-Fixed-Layout,
  die Räume sind dokumentfluss-tauglich (320/390-Reflow ohne `!important`-Kaskaden wie
  heute in `@media (max-width:800px)`).

**Neu:** Tür-Komponente (Bild-Kachel + Label + Ziel), Übergangs-Modul (View Transitions),
Tür-Bilder (§5), ggf. `ASSETS.md`-Eintrag für neue Kunst (Provenienz, Prompt, C2PA-Hinweis —
analog `sol-build/site/static/ASSETS.md`).

---

## 4) Übergänge (Konzept)

**Mechanik:** SvelteKit `onNavigate` → `document.startViewTransition(updateDOM)`, nur wenn
(a) Navigation intern zwischen den drei Räumen, (b) `document.startViewTransition`
vorhanden, (c) `matchMedia('(prefers-reduced-motion: no-preference)')`. Sonst: sofortiger
Wechsel (das ist der komplette Fallback-Pfad — Browser ohne VT-API navigieren normal).

**Choreografie (~2,4 s, im 2–5-s-Fenster):** „Durch die Tür gehen" — die alte Ansicht
zoomt sanft in die angeklickte Tür hinein (`::view-transition-old`: scale 1→1,35 mit
Transform-Ursprung auf der Tür-Position, Abdunklung), gleichzeitig öffnet sich die neue
Ansicht aus der Türmitte heraus (`::view-transition-new`: eingeklappt per `clip-path`/
scale 0,92→1, Aufhellung). Die angeklickte Tür-Kachel wird per
`view-transition-name` zum nahtlosen Übergangsmotiv. Dauer ~2,4 s mit ruhigem
cubic-bezier; Rückwärtsnavigation (Zurück-Knopf) dieselbe Bewegung umgekehrt und kürzer
(~1,4 s) — Orientierung ohne Zwang zum Warten.
**Reduced motion:** keine Transition, keine Bewegung — sofortiger Raumwechsel (auch die
dekorativen Raum-Ambient-Animationen fallen auf `transition-duration:.01ms`).
**A11y:** Fokus wandert nach dem Wechsel auf das `h1` des Zielraums (`tabindex="-1"`,
ohne Scroll-Sprung); genau ein wirksames `h1` pro Route; Türen sind echte Links mit
sichtbarem Label (≥44 px), Tastatur und Screenreader navigieren ohne jede Transition.

---

## 5) Bilder / Embleme

**Bestand (geerbt):** 4 Szenen 1600×900 (sehr dunkel, gemalte Konzeptkunst; Bernstein-/
Messing-Lichtpunkte gegen kaltes Mondblau), 10 Embleme 320², 2 Thumbnails 640×360.
Stilurteil aus eigener Anschauung: konsistente Handschrift, hohe Qualität — aber die
Mitten liegen fast im Schwarz; auf hellen Displays wirken große Flächen leer.

**Neue Kunst — Bedarf und Regeln.** Ich kann hier keine Bilder generieren; die folgenden
Anforderungen sind als fertige Generierungs-Aufträge (ChatGPT) formuliert. Gemeinsame
Vorgaben je Bild: **etwas heller als der Bestand** (Mitteltöne sichtbar anheben,
Lampenlicht großzügiger, Schatten nicht mehr reines Schwarz — ohne Stilbruch: weiterhin
gemalte Konzeptkunst, Öl-/Gouache-Textur, dieselbe Palette dunkles Holz + Messing/Bernstein
gegen kühles Mondblau), **kein Text/Schriftzug im Bild**, keine Fotorealistik, ruhige
Zonen für Overlay-Beschriftung. Format Tür-Karten: **Hochformat 3:4** (Generierung
1024×1365, Anzeige ~480×640), Fokus mittig auf die Tür.

- **A1 — `door-study-archive` (schlichte Archivtür aus dem Vorzimmer):**
  Motiv: schmale, schlichte Holztür in einer Wand aus dunklen Karteischränken —
  bewusst **weniger prunkvoll** als die Doppeltür der doorway-Plate: unverziertes
  Eichenholz, kleines Messingschild (leer), ein einzelner Messinggriff, darüber ein
  kleines warmes Wandlämpchen. Stimmung: Arbeitszimmer-Durchgang, Einladung zum Stöbern,
  kein Zeremoniell. Fokus: Tür füllt mittlere zwei Drittel. Ruhige Zonen: oberes Viertel
  (Wand/Lämpchen-Glow) und unteres Sechstel (Boden) frei von Kanten/Objekten für Label.
  Helligkeit: Lämpchen als Hauptlichtquelle, sichtbare Holzmaserung in den Mitten.

- **A2 — `door-council-archive` (schlichte Archivtür aus dem Ratssaal):**
  Motiv: unauffällige Seitentür zwischen zwei dunklen Steinsäulen des kreisrunden Saals —
  gleiche schlichte Tür wie A1 (Wiedererkennbarkeit), aber kühleres Umfeld: Mondblau-
  Streiflicht von oben, nur eine schmale Bernstein-Lichtfuge unter der Tür und ein
  dezenter Messinggriff als warme Kontrapunkte. Stimmung: Nebenausgang, diskret, nicht
  triumphal. Fokus/rhythmische Zonen wie A1 (oben Säulenschatten ruhig, unten Boden
  ruhig). Helligkeit: Mitten wie A1 angehoben, Kontrast blau-kalt vs. bernstein-warm
  bewahren.

- **A3 — optional, Helligkeits-Refresh der Raum-Plates:** falls nach Einbau der Türen der
  Sprung „helle Tür / sehr dunkler Raum" stört: dieselben vier Szenen-Motive mit
  angehobenen Mitten neu generieren (nur auf Freigabe; die geerbten Plates bleiben
  Default). C2PA-Credentials der Neugenerierungen nicht strippen; Provenienz in
  `site/static/media/ASSETS.md` dokumentieren (Prompt, Datum, Quelle).

Bis neue Kunst liegt, nutzen Tür-Karten Ausschnitte der vorhandenen Plates (doorway für
Ratssaal-Zugänge, archive-Thumbnail für Archiv-Zugänge) — funktional vollwertig, optisch
als Übergang gekennzeichnet.

---

## 6) Datenlücken und Ungenutztes (nichts davon wird erfunden)

1. **Tür-Bilder fehlen** (A1/A2 oben) — die einzige echte Asset-Lücke.
2. **„Belege" im Vorzimmer:** verfügbar, aber heute auf der Startseite ungenutzt:
   `wart_dossier` (Objekt: `label`, `model`, `search_queries[]`, `content_md`, `costs`)
   steht bereits im View-Model. Plan: `search_queries` (strukturierte Liste) als sichtbare
   Beleg-Spur zeigen, `content_md` **nicht** auf der Startseite duplizieren (Anzeige-Prosa,
   bleibt im Protokoll; verlinkt via `#wart-dossier`). Kein erfundenes „Warum".
3. **`dissent_highlights`** (5 kuratierte, publizierte Stichpunkte) liegt im View-Model,
   wird nirgends gerendert. Enthält Fachvokabular („Säule A", „TaRL") — Verfassungssprache
   verbietet unerklärte Begriffe **im Einstieg**; im Archiv als ausgewiesener
   „Auszug aus dem Protokoll" (Zitat-Kontext) zulässig. Nutzung optional, Entscheidung vor
   Bau; der volle `dissent_md` bleibt ohnehin geklappt erreichbar.
4. **`summary`** (kuratierte Kurzfassung der Sitzung) existiert in `session.json`, ist nicht
   Teil des View-Models. Falls fürs Archiv/Vorzimmer gewünscht: Der Route-Load reicht
   `session.summary` zusätzlich durch — **ohne** `homepage.js` anzufassen (das geerbte
   Modul bleibt byte-identisch). Keine Pflicht, nur Möglichkeit.
5. **Keine Einzelporträts von Späher/Wart:** die antechamber-Plate zeigt beide Figuren
   bereits (Schreibtisch/Lampe); sie werden als Plate/Ausschnitt wiederverwendet, nicht
   neu erfunden. Neue Porträt-Kunst ist **nicht** angefordert.
6. **Kosten-Detailtiefe:** `costs.by_model` (inkl. Wart-Zeile, Token, FX-Kurs) ist
   verfügbar; heute zeigt die Startseite nur die Summe. Archiv kann die vorhandene
   Aufschlüsselung als Tabelle zeigen — reine Darstellung vorhandener Felder.

---

## 7) Regressions- und Abnahme-Checkliste (für die Bauphase)

- No-JS: alle Pflichtinhalte der drei Räume im jeweiligen pragerenderten HTML (Liste §2);
  Test ehrlich nachgezogen und grün (`cd site && npm ci && npm test`), `npm run build`
  warnungsfrei, `npm run preview`: `/`, `/ratssaal/`, `/archiv/`, `/sessions/`,
  `/sessions/2026-07c/`, `/journal/`, `/manifest/` → 200, inhaltlich intakt.
- Historie: Zurück/Vorwärts über alle drei Räume, Direktaufruf `/ratssaal/` + `/archiv/`,
  geteilter Link — ohne JS (MPA) und mit JS (Client-Router) gleichermaßen.
- A11y: ein `h1` pro Raum; Kontraste funktionaler Texte ≥ AA (Raum-Palette an die
  Layout-Tokens angebunden, nicht an die Bühne); Alt-Texte (Embleme dekorativ-nur wo der
  sichtbare Begriff trägt; Szenen/Türen mit echten Alternativen wo sie navigieren);
  Tastatur vollständig; Tap-Ziele ≥ 44 px; Reflow 320/390 ohne horizontalen Overflow;
  `prefers-reduced-motion` → sofortige Wechsel, keine Ambient-Animation.
- Verfassungssprache oben: „Bereich", „noch keine Einigkeit", „Belege"; Fachbegriffe nur
  im verlinkten Protokoll bzw. als ausgewiesenes Zitat; Negativprobe `>Dissens
  (vollständiger Wortlaut)<` bleibt Teil des Tests.
- Spendenlinks ausschließlich aus Registry; `null` → Hinweis statt totem Knopf.
- Dissens/Korrektur als marked-HTML, geklappt, Wortlaut unverändert.
- `git diff` nur `site/` + `docs/`; `site/build/` ohne hochauflösende Originale;
  Screenshots 1440 + 320/390 je Raum + No-JS-Grundzustand.

## 8) Offene Entscheidungen (bitte vor „los" bestätigen oder überstimmen)

1. **URLs deutsch** `/ratssaal/`, `/archiv/` (Empfehlung: Konsistenz + Verfassungssprache)
   statt englisch `/council/`, `/archive/`.
2. **Übergangsdauer** ~2,4 s vorwärts / ~1,4 s zurück (im 2–5-s-Rahmen; Zurück bewusst
   kürzer, damit Orientierung nicht zur Warte wird).
3. **`dissent_highlights` im Archiv** als „Auszug aus dem Protokoll" zeigen (Empfehlung: ja,
   mit Zitat-Rahmen) oder weglassen.
4. **`summary`** zusätzlich ins Vorzimmer/Archiv durchreichen (Empfehlung: nein — nicht
   nötig; Vorzimmer trägt Leitfrage + Mechanismus, Archiv trägt Titel/Datum/Status).
5. **A3 (Helligkeits-Refresh der vier Szenen-Plates)** nur falls der Kontrast zur helleren
   Tür-Kunst stört; Default: geerbte Plates unverändert.

**Ende Phase 1. Kein Baubeginn vor „los".**
