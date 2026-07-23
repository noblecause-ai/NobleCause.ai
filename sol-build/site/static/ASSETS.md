# Bild-Assets — Herkunft & Transparenz

Beide Bilder sind **KI-generiert** und tragen eingebettete **C2PA Content
Credentials** (Content Authenticity). Das ist Teil der Projekt-Transparenz und wird
bewusst **nicht entfernt**.

| Datei | Motiv | Größe | Maße |
|---|---|---|---|
| `ratssaal.png` | Kreisrunder Ratssaal mit drei beleuchteten Pulten (Hero + Saal) | ~2,0 MB | 1672 × 941 |
| `vorraum.png` | Vorzimmer mit Schiefertafel, Späher, Wart (Vorraum + Archiv-Tür) | ~2,0 MB | 1915 × 821 |

## C2PA-Provenienz (aus den eingebetteten Credentials)
- **Erzeuger (`claim_generator`):** `gpt-image` v2.0
- **`digitalSourceType`:** `http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia`
  → deklariert die Bilder als **von einem trainierten Algorithmus erzeugt (KI)**.
- **Assertions:** `c2pa.actions.v2`, `c2pa.created`, `c2pa.icon`.
- **Manifest-IDs:** `urn:c2pa:5af2f08a-…` (ratssaal), `urn:c2pa:5162eb7f-…` (vorraum).

## Optimierung — bewusst aufgeschoben (Begründung)
Eine verlustarme Verkleinerung wurde **nicht** durchgeführt, weil das einzige lokal
verfügbare Werkzeug (`sips`) beim Re-Encodieren die **C2PA-Credentials strippen**
würde — das widerspricht der Transparenzanforderung. Empfehlung für die Integration:
ein C2PA-erhaltender Optimierer (z. B. `oxipng` mit Metadaten-Erhalt oder Re-Embed via
`c2patool`) in einem Build-Schritt, oder responsive `srcset`-Varianten. Bis dahin
liegen die Originale mit intakten Credentials hier.

## Nutzung im Build
`build.py` referenziert `site/static/ratssaal.png` und `site/static/vorraum.png` mit
festen `width`/`height` (Layout-Stabilität). Der dekorative Hero-Einsatz nutzt
`alt=""`; die inhaltlichen Einsätze (Saal, Vorraum) tragen beschreibende Alt-Texte.
