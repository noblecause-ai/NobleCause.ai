# Code-Review — SOL-Frontend-Build (noblecause-sol-build.zip)

Stand: 2026-07-15 · **NUR Review, kein Merge, kein Deploy, keine Live-Daten geändert.**
Reproduziert: `python build.py` grün, `tests/` (2) grün, Build byte-gleich zum
mitgelieferten `index.html`. Quellen (Text) unter `sol-sources/` eingecheckt
(vendored for review, **nicht zum Merge**; ~2 MB-PNGs ausgelassen).

## Urteil
**Taugt als Basis — nachbessern vor der Design-Abnahme.** Architektur (no-JS-first,
progressive Enhancement), Barrierefreiheit, Sprache und Datenschutz sind **stark und
korrekt**. Vor der Abnahme blockieren **1 MUSS-FIX** (dein Fund, bestätigt) und **1
Integrations-Härtung** (der Datentausch ist kein reiner Swap). Nicht wegwerfen.

## Funde nach Schweregrad
| # | Schwere | Kategorie | Fund |
|---|---|---|---|
| F1 | **KRITISCH** | Verfassung | `rationale_md` frontend-erfunden (Säule A vergleichende Behauptung), sichtbar auf der Karte |
| F2 | **HOCH** | Integration | Datentausch ist **kein reiner Swap** — Sols Datei erfindet/erwartet Felder, die das Backend nicht liefert |
| F3 | MITTEL | Vertrag | Schema-Dublette (`sitzung.schema.json` == `session.schema.json`), gebaut gegen **ungemergtes** PR #10 |
| F4 | MITTEL | Sprache | „Dissens" im sichtbaren **Sitzungstitel** (echtes Datum, kein Frontend-Label) |
| F5 | MITTEL | A11y/Alter | Tap-Ziele grenzwertig für die 80-Jährige (Reiter ~37 px, quiet-links klein) |
| F6 | NIEDRIG | Semantik | `<h1>` = führende Org „LEEP", nicht Seiten-/Site-Titel |

**Stark (kein Fund):** Kontrast (alle Paare AA+), Datenschutz (0 Tracker/Fonts/Cookies),
no-JS (Inhalt vollständig statisch), Tastatur/Fokus, oma-taugliche Sprache. Details unten.

---

## MUSS-FIX vor Design-Abnahme
1. **F1 — `rationale_md` neu verankern** (Lösungsentwurf in `datenvertrag-vorschlag.md`).
2. **F2 — Integrations-Datenvertrag festziehen** (welche Felder das echte Backend
   liefern MUSS, siehe unten). Erst danach ist der Swap echte→Beispieldaten sauber.
3. **F3 — Schema-Dublette auflösen** + Entscheid, ob PR #10-Schema abgenommen wird.

---

## Aufgaben 1–7 im Detail

### 1. Barrierefreiheit (index/styles/app)
- **Kontrast (rechnerisch, WCAG-AA):** ALLE funktionalen Text/Hintergrund-Paare bestehen.
  Schwächstes Paar `--faint #8f887d` auf `#0b1012` = **5,46:1** (AA ≥4,5 erfüllt);
  `--muted` 10,1:1; Links `--blue` 8,8:1 / `--brass` 9,0:1; Hero-Text 16,5:1; gewählter
  Reiter (dunkel auf Messing-hell) 12,4:1. **Keine Kontrast-Fehler.**
- **Semantik:** genau ein `<h1>`, Landmarks/`role`s, `<article class="recommendation-card">`,
  ARIA-Tabs (`role=tablist/tab/tabpanel`, `aria-selected/controls/labelledby`),
  `aria-hidden` auf Dekor. Überschriften h1→h4 vorhanden.
- **Tastatur:** Skip-Link „Direkt zu den Empfehlungen" **unabhängig verifiziert**
  (Tab → sichtbarer Messing-Fokusring, Screenshot). Reiter mit `←/→/Pos1/Ende`
  (`app.js`). Spendenlinks sind echte `<a>`. **„Tür" (`archive-door`) ist dekorativ
  (`aria-hidden`), „Pulte" (`lit-floor`) ist ein Container** — keine Klick-only-Divs,
  kein Keyboard-Trap; Inhalt ist ohnehin statisch da.
- **Fokus-Sichtbarkeit:** `:focus-visible` in CSS, im Browser als klarer Ring belegt.
- **Alt-Texte:** beschreibend für Ratssaal/Vorraum, leer (`alt=""`) für Dekor — korrekt.
- **`prefers-reduced-motion: reduce`** vorhanden.

### 2. no-JS wirklich vollständig — **belegt**
- **Inhalt ist statisch**, nicht JS-injiziert: im Roh-HTML 4 `recommendation-card`,
  **9 Spenden-`<a>`**, **6 `model-column`** (3 Modelle × 2 Runden), 4 Archiv-Einträge.
- **`app.js` (1,7 KB) injiziert nichts** — schaltet nur Reiter (`aria-selected`,
  `panel.hidden`) und Tastatur; hash-sync. Reine Kür.
- **Korrekte Progressive-Enhancement-Mechanik:** `<html class="no-js">` + Inline
  `className='js'`; CSS `.no-js .protocol-tabs{display:none}` (Reiter weg) und
  `.js .tab-panel[hidden]{display:none}` (Panels nur mit JS verborgen). Tabpanels tragen
  **kein** statisches `hidden`. → **Ohne JS sind alle drei Protokollteile gestapelt
  sichtbar.** Bestätigt durch Sols `preview-mobile-nojs.png` (alle vier Empfehlungen +
  Spendenlinks + beide Runden + Archiv sichtbar).

### 3. Mobil
- Viewport-Meta vorhanden; Breakpoints (760/1100 px), Karten stapeln, Reiter
  `overflow-x:auto`, Saal degradiert zum Kopfbild (`.hero-shade`/`.hero-content`
  mit solidem BG — **kein Text über Foto**). Keine festen `px`-Breiten, die Overflow
  erzwingen (`white-space:nowrap` nur auf einem kleinen Hotspot-Label). Sols
  Mobil-Previews zeigen sauberes Einspalten ohne horizontalen Overflow.
- **Einschränkung (ehrlich):** mein eigener 360-px-Render reflowte im Fenster nicht
  (Mindestbreite) — Mobil-Beleg stützt sich auf CSS-Analyse + Sols Previews, nicht auf
  einen eigenen 360-px-Screenshot.
- **F5:** Tap-Ziele grenzwertig für die 80-Jährige — Protokoll-Reiter ~37 px hoch,
  `quiet-link` klein. WCAG-AA (24 px) erfüllt, AAA (44 px) nicht. Empfehlung: ≥44 px.

### 4. Sprache — sehr gut, mit einem Grenzfall
- **Sichtbarer Text ist oma-tauglich, Fachwörter sind ersetzt:** „**Sicherheit: 71 von
  100**" (nicht Konfidenz), „**3 von 3 nennen dieselbe Organisation**" (nicht Konvergenz),
  „**Einigkeit mit Vorbehalt**" (nicht konditional), „**Die Zählmaschine zählt**" (nicht
  Orchestrator/Aggregation). Verbotsliste im sichtbaren Text = **sauber**.
- **F4:** „**Dissens**" erscheint 1× sichtbar — im **echten Sitzungstitel** „Auflösung des
  Säule-A-Dissens" (und Archiv-Titel). Das ist **Daten, kein Frontend-Label** (das
  Frontend darf den Titel nicht umschreiben). Entscheidung beim Steward: falls oma-tauglich
  gewünscht, ist das eine **redaktionelle/Backend-Titel**-Frage, nicht Sols Bug.
  („Konfidenz" steckt nur im eingebetteten JSON-`focus_rule`, **nicht** im sichtbaren Text.)

### 5. Externe Links / Datenschutz — **sauber**
- Alle **9** externen Links (nur die vier Spenden-Domains) tragen `target="_blank"` **und**
  `rel="noopener noreferrer"`. **0** Tracker/Analytics, **0** Fremd-CDN/Google-Fonts
  (nur System-Fonts + `cursive`-Fallback), **0** Cookies/`localStorage`/`fetch`/Beacons,
  **0** `@font-face`/externe `<link>`. Vorbildlich.

### 6. Integrationsfähigkeit — **F2: kein reiner Swap**
Sols Startseiten-Datei `data/sitzung.json` weicht vom echten Backend-Kontrakt
(`gremium/run_session.py` → `sessions/<id>/session.json`, Schema aus PR #10) ab:
| Abweichung | Sol erwartet | Backend liefert |
|---|---|---|
| **erfundene Präsentationsfelder** | `presentation.archive`, `.focus_rule`, `.pillar_labels`, `.pillar_symbols` | — (nichts davon) |
| **Voten-Struktur** | `rounds[].votes[].recommendations[]` (strukturiert) — daraus leitet Sol die Meinungsänderung Pratham→HKI ab | nur `votes[].content_md` (Prosa) |
| **erfundenes Empfehlungsfeld** | `recommendations[].rationale_md` | — (siehe F1) |
| **Datei-/Namensraum** | `data/sitzung.json` (deutsch) | `sessions/<id>/session.json` (englisch) |
| **weggelassene Echtfelder** | ignoriert `wart_dossier`, `designation`, `led_by`, `wart_opening_md`, `wart_moderation_md` (in 2026-07c real vorhanden) | liefert sie |
→ **Der Swap Beispiel→echt ist NICHT rein.** Ohne die erfundenen Vote-`recommendations[]`
kann das Frontend die (real belegte) Revision nicht deterministisch zeigen; ohne
`presentation.*` fehlen Säulen-Labels/Symbole und die Archiv-Liste. Sols README benennt
diese Lücken selbst ehrlich. **Vor Integration:** Datenvertrag festziehen — entweder das
Backend liefert diese Felder (strukturierte Vote-Recs, Labels/Symbole, Archiv-Übersicht,
`focus_rule`), oder ein klar definierter, buildseitig erzeugter **Startseiten-Datenvertrag**
speist die Präsentationsschicht. `build.py` ist ein eigenständiger Python-Generator, weit
weg vom SvelteKit-`site/` — die Naht ist der Datenvertrag, nicht der Generator.

### 7. Schema-Dublette — **F3**
`schema/session.schema.json` und `schema/sitzung.schema.json` sind **byte-identisch**
(diff = 0). Sols README bestätigt: `sitzung.schema.json` ist ein **Alias** meines
`session.schema.json` aus **PR #10 (nicht gemergt)**. → Empfehlung: **eine** kanonische
Datei (`session.schema.json`), Alias streichen; Sprach-/Namensentscheidung
(`sitzung` vs `session`) im Vertrag festziehen; und **PR #10-Schema erst abnehmen**,
bevor darauf gebaut wird.

---

## Lob (bewusst festhalten)
no-JS-first sauber umgesetzt; Datenschutz vorbildlich; Kontrast durchweg AA+; Sprache
konsequent entjargonisiert; Skip-Link + sichtbarer Fokus; deterministische Führung
(LEEP „nach einer festen Regel") korrekt und transparent gerendert; ehrliche
Selbstauskunft über die Vertragslücken in der README. Das ist ein tragfähiger Prototyp.

## Nicht getan (Grenzen dieses Reviews)
Kein eigener 360-px-Render (Fenster-Reflow, s. F5-Notiz) — Mobil per CSS + Sol-Previews.
Keine automatisierte Axe/Lighthouse-Suite. Keine Prüfung der ~2 MB-PNG-Assets.
