# Go-Live-Liste

Offene Punkte vor dem Ausliefern. Ergänzen, nicht löschen.

## Plattform / Auslieferung
- [ ] **Cache-Header setzen** (Plattform-Sache, sobald sie feststeht): `_app/immutable/*` →
  `Cache-Control: public, max-age=31536000, immutable`; die `*.html` → `no-cache` bzw. kurzes
  `must-revalidate`. Sonst lebt altes HTML neben neuen (gehashten) Bundles → fehlgeschlagener
  dynamischer Import (`Failed to fetch dynamically imported module`) → der Client hydratisiert nicht
  → der Türdurchgang liest als Blende. (Runde G: genau dieses Bild war der „Regress"; auf einem
  frischen Build trägt die Fahrt.)
