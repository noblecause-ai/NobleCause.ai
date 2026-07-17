# Umbau-Brief: Startseite als drei Räume (feat/council-rooms)

**An:** den Agenten, der auf `feat/council-rooms` arbeitet (Kimi).
**Zuerst lesen:** `AGENTS.md` (harte Grenze + Sauberkeitsregeln). Dieser Brief ist der
konkrete Auftrag. Es ist ein **Wegwerf-Experiment**; scheitert es, wird der Branch gelöscht.

## Ziel in einem Satz
Ersetze die **eine lange Scroll-Bühne** der Startseite (heute:
`site/src/routes/+page.svelte`, `.council-stage` mit acht scroll-gesteuerten Szenen
`arrival → recommendations → door-opening → antechamber → initial → revision → count →
archive`) durch **drei diskrete Räume**, zwischen denen man wechselt (Türen/Navigation)
statt endlos zu scrollen. **Nur die UI-Architektur** ändert sich — Inhalt, Daten und
Embleme bleiben.

## Die drei Räume
Nutze die bereits vorhandene Erzählung und die vorhandenen Plates
(`site/static/media/scenes/{antechamber,hall,archive,doorway}-display.jpg`):

1. **Vorzimmer — „Belege".** Ankunft/Einstieg: die Leitfrage, „was ist NobleCause" (der
   Mechanismus in zwei schlichten Sätzen), Späher & Wart, die Belege; die **Säulen-Legende**
   (vier Bereiche mit Emblem + Alltagswort) und die **Prozess-Legende** (sechs Schritte)
   werden hier bei ihrer ersten sprachlichen Nennung eingeführt.
2. **Ratssaal — „Beratung".** Der Kern: drei Modelle antworten getrennt, lesen einander,
   dürfen umdenken; die Zählmaschine zählt (nur Zählwerk, keine Intelligenz). Hier stehen die
   **vier Empfehlungen** (Konsens **und** Nicht-Konsens gleichwertig), **Revisionen**
   (Erst→Schluss), **Vorbehalte** und die **direkten Spendenlinks**.
3. **Archiv — „Veröffentlicht".** Frühere Sitzungen, **Kosten**, **Korrekturhinweis**,
   **Dissens-Zugang**, Link zum vollständigen Protokoll.

Der Wechsel zwischen den Räumen soll sich wie ein Gang durch Türen anfühlen, nicht wie ein
einziger Scroll. Wie genau (Klick/Tab/Anker/Sanftes) ist deine Gestaltung — solange die
Regeln unten halten.

## ERBEN — nicht anfassen (die verifizierte Datennaht)
- **`site/src/lib/server/content.js`** — Loader (jüngste Sitzung nach `number`, nicht Datum).
- **`site/src/lib/server/homepage.js`** — View-Model. Es **liest** `recommendations[]` und
  `convergence` (Zählstände `count/total/conditional_count`) aus der Sitzung. **Zähle NIE
  selbst neu, aggregiere NIE im Frontend.** Die „3 von 3" / „2 von 3" kommen aus
  `convergence`, nicht aus einer Schleife über Voten. Revisionen kommen aus den
  strukturierten Voten über `organization.id`, nicht aus Prosa (`content_md`).
- **Embleme** (schon integriert): `site/static/media/pillars/pillar-*-display.jpg`,
  `site/static/media/process/process-*-display.jpg`. Verwende sie; regeneriere sie nicht.
- **Daten/Registry:** `sessions/2026-07c` (Konsens), `sessions/2026-07` (Nicht-Konsens),
  `organizations.json` — **nur lesen**.

## BEIBEHALTEN (Regressionsverbot — heute erfüllt, muss erfüllt bleiben)
- **No-JS-Vollfallback:** Ohne JavaScript muss die **ganze Wahrheit** sichtbar sein —
  vier Empfehlungen, Zählungen, Spendenlinks, Mechanismus, **Vorbehalte, Erst- UND
  Schlussvoten, Revisionen, Kosten, Korrekturhinweis, Dissens-Zugang, Archiv, Protokoll-
  Link**. Der Test `site/tests/homepage-build.test.js` prüft das **im sichtbaren Fallback-
  Block** (nicht im per-JS-versteckten Teil) — wenn du die Fallback-Struktur änderst, ziehe
  den Test ehrlich nach (weiter gegen den ohne-JS-sichtbaren Block prüfen).
- **A11y:** genau **ein** wirksames `h1` je Zustand; Kontrast funktionaler Texte ≥ WCAG AA;
  Alt-Texte (leer nur bei rein dekorativer Wiederholung, wo der sichtbare Begriff die
  Information trägt); volle Tastaturbedienung; `prefers-reduced-motion` respektiert; Tap-Ziele
  ≥ 44 px; sauberer Reflow bei **320** und **390** CSS-px, kein horizontaler Overflow.
- **Verfassungssprache:** oben keine unerklärten Fachbegriffe — „Bereich" statt „Säule A–D",
  „noch keine Einigkeit" statt „Dissens", „Belege" statt „Evidenz". Fachbegriffe bleiben im
  vollständigen Sitzungsdokument.
- **Spendenlink** ausschließlich aus der Registry; `donation_url: null` sauber (kein toter
  Knopf).
- **Dissens/Korrektur** als Markdown gerendert (nicht roh gedumpt, nicht per Regex geparst).

## TABU (Hook erzwingt es)
Keine Änderung unter `sessions/ journal/ schedule.json gremium/ schema/ prompts.py`. Ein
`pre-commit`-Hook blockt solche Commits auf diesem Branch (rc=1). Wenn eine Idee eine
Datenänderung zu verlangen scheint: **stoppen und melden**, nicht umgehen. Keine erfundenen
Inhalte/Zahlen — die Startseite visualisiert die **publizierte** Zählung, sie erzeugt keine.

## Abgabe / Definition of Done
- `cd site && npm ci && npm test` **grün** (inkl. ehrlichem No-JS-Test); `npm run build`
  **warnungsfrei**; `npm run preview` → alle Routen (`/`, `/sessions/`, `/sessions/2026-07c/`,
  `/journal/`, `/manifest/`) **200 und inhaltlich intakt**.
- `git diff` nur unter `site/` (+ ggf. `docs/`); Tabu-Pfade unberührt; `site/build/` ohne
  hochauflösende Originale.
- Screenshots Desktop (1440) + Mobil (320/390) der drei Räume; No-JS-Grundzustand.
- Frei committen ist ok; **vor** irgendeinem Push/Merge zu sauberen Einheiten squashen.
- **Kein Push auf master, kein Merge** ohne ausdrückliche Freigabe.

## Referenz
Der bisherige Aufbau (Scroll-Bühne + No-JS-Fallback + Datennaht) steht komplett in
`site/src/routes/+page.svelte` und den beiden `server/`-Modulen — als Vorlage für das, was
inhaltlich erhalten bleiben muss. Frühere Abnahme-Screenshots: `docs/review/`.
