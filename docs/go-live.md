# Go-Live-Liste

Offene Punkte vor dem Ausliefern. Ergänzen, nicht löschen.

## Rekordlinien / Zusammenführung (harte Vorbedingung)
- [ ] **Datenstand und `feat/council-rooms` gehen gemeinsam auf `master`, Push erst danach.**
  Der Datenbranch `data/rekordlinien-2026-07-30` (Commit `59461f1`, von `origin/master`
  abgezweigt) darf **nicht allein** deployt werden. Belegt beim Punkt-6-Build: der volle
  Build der Datenbranch-Site scheitert am Prerender mit `Error: 404 /sessions//`
  (verlinkt von `/journal/2026-07-27b/`). Ursache: `origin/master`s
  `src/routes/journal/[id]/+page.svelte` rendert den Session-Link **unbedingt**
  (`<a href="/sessions/{e.session_ref}/">` → bei `session_ref: null` entsteht
  `/sessions//`); nur die feat-Fassung hat den `{#if e.session_ref}`-Guard und die
  `isCommission`-Behandlung. Der Datenstand allein würde `deploy.yml` also **auf der
  Produktionsseite** am Prerender brechen. Reihenfolge daher zwingend: erst feat + Daten
  zusammen auf `master`, dann Push. (= Punkt 7 der Wart-Liste; wartet ohnehin auf linke
  Ergebnis-Tafel, Routen, Abschluss-Durchgang, offenen Strang, Review durch Kimi 3/Codex.)

## Plattform / Auslieferung
- [ ] **Cache-Header setzen** (Plattform-Sache, sobald sie feststeht): `_app/immutable/*` →
  `Cache-Control: public, max-age=31536000, immutable`; die `*.html` → `no-cache` bzw. kurzes
  `must-revalidate`. Sonst lebt altes HTML neben neuen (gehashten) Bundles → fehlgeschlagener
  dynamischer Import (`Failed to fetch dynamically imported module`) → der Client hydratisiert nicht
  → der Türdurchgang liest als Blende. (Runde G: genau dieses Bild war der „Regress"; auf einem
  frischen Build trägt die Fahrt.)
