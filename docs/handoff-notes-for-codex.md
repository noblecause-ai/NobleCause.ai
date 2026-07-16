# Handoff-Notes für Codex — verifizierte Fakten

Faktendokument zur Beschleunigung der Analyse. **Komplementär zu `AGENTS.md`** (dort:
Guardrails/Tabu — hier NICHT wiederholt). Nur verifizierte Fakten, keine Design-Meinungen —
die Gestaltung ist frei. Alle Angaben unten wurden gegen die realen Dateien geprüft
(Branch `feat/immersive-homepage`, Basis #12).

---

## 1) Deploy — statische Generierung ist die starke Default-Wahl (kein Zwang)

Statische Generierung ist die starke Default-Wahl — **nicht aus Ressourcenmangel**:
- **(a) publish-on-commit:** Der Inhalt ändert sich nur bei Commit, ist für alle Besucher
  identisch — kein per-Request-Rendering nötig.
- **(b) statisch ≠ limitiert:** Jede scroll-reaktive / animierte / 3D-Ambition läuft
  **clientseitig** auf statischem HTML. Die visuelle Decke bleibt unberührt.
- **(c) static-from-committed-data** hält die Runtime aus der Vertrauenskette: Was Caddy
  ausliefert, steht **byte-genau im öffentlichen Repo** — passt zur Transparenz-Verfassung.

**SvelteKit: `adapter-static` bevorzugt.** (Der bestehende `site/`-App nutzt bereits
`@sveltejs/adapter-static` — `site/svelte.config.js`.)

**ESCAPE HATCH:** Eine Server-Runtime auf dem VPS ist **verfügbar**, wenn ein ECHTER Bedarf
mit Trade-off belegt wird (etwas, das clientseitig/zur Build-Zeit wirklich nicht geht).
**Ressourcen sind NICHT der Blocker** — der VPS gehört dem Projekt und kann mehr.

**Aktueller Pfad (belegt, `.github/workflows/deploy.yml`):**
```
push → master
  └─ GitHub Actions (ubuntu, Node 22)
       └─ working-directory: site/  →  npm ci && npm run build   (adapter-static → site/build/)
            └─ rsync -avz site/build/  →  noblecause@185.143.100.222:/srv/noblecause/
                 └─ Caddy liefert statische Dateien aus (kein Service-Restart, kein Healthcheck)
```
Hinweis: Der **deployte** App ist `site/` (SvelteKit). `sol-build/` (Python-Generator) ist
der bisherige SOL-Build, aus dem die Review-Seiten stammen — dieselben Daten, andere
Render-Schicht.

---

## 2) Datenvertrag — Eigenheiten (echte Ausschnitte)

Kanonisches Schema: `schema/session.schema.json`. Doku: `sol-build/data-contract.md`.
Datenquellen (nur lesen): `sessions/2026-07c` (Konsens), `sessions/2026-07` (Nicht-Konsens),
`sessions/2026-07b`, `organizations.json`.

**`organizations.json.beschreibung`** — 13/13 Orgs, kuratiert, neutral (der Kartentext „was
die Org tut"; **kein** erfundenes „Warum"):
```
helen-keller-international →
  "Verteilt Vitamin-A-Präparate an Kinder in Ländern mit hoher Mangelrate und senkt so
   vermeidbare Erblindung und Kindersterblichkeit."
```

**`recommendations[].rationale_md` ist maschinelles Boilerplate** — kein redaktioneller
Text, nur die Zähl-Zusammenfassung. Echter Wert (2026-07c, Säule A):
```
"Konvergenz im Schlussvotum: 3 von 3 Modellen, davon 1 konditional, empfehlen diese
 Organisation (Claude Opus, GPT, Gemini Pro). Begründungen in den Schlussvoten."
```

**Strukturierte Voten — Protokoll IMMER aus `rounds[].votes[].recommendations[]` rendern,
NIE `content_md`-Prosa parsen.** Form je Votum:
```json
{ "model": "claude-opus-4-8", "content_md": "…Prosa…", "confidence": 0.xx,
  "recommendations": [
    { "pillar": "A", "organization_id": "helen-keller-international",
      "organization": "Helen Keller International",
      "title": "Vitamin-A-Supplementierung (VAS) — konditional, …" } ] }
```
`content_md` existiert, ist aber **nur Anzeige-Prosa** — die Struktur kommt aus
`recommendations[]` (registry-aufgelöst).

**`dissent_md` und `correction_notice.text` sind ROH-Markdown** — literale `**` und ganze
` ```json `-Blöcke, mehrere Bildschirmhöhen. **Rendern/falten**, nie verbatim dumpen, aber
**Wortlaut nie ändern** (publizierter Text). Gemessen:
```
2026-07 : dissent_md 7173 Zeichen, 78× "**", 2 ```-Blöcke   (KEIN correction_notice)
2026-07b: dissent_md 6386 Zeichen, 22× "**", 3 ```-Blöcke   (correction_notice: JA)
2026-07c: dissent_md 6941 Zeichen, 30× "**", 3 ```-Blöcke   (correction_notice: JA)
```
Beispiel-Anfang `dissent_md` (2026-07c): `**Claude Opus:** **Säule A — ich weiche weiterhin
von Gemini und dem GPT-Erstvotum ab, …**`

**`donation_url` kann `null` sein.** Er stammt aus der Registry (aufgelöst), nicht aus dem
Votum. Ohne offiziellen Spendenweg = `null` → UI muss den Fall tragen (kein Link). Orgs
ohne URL: `pratham`, `tarl-africa`, `global-road-safety-partnership`.

**Konditionale Voten.** `recommendations[].convergence.conditional_count` + je Votum
`conditional` (bool) und `reservation` (Text). Echt (2026-07c, Säule A / Helen Keller
International): `conditional_count: 1` — Claude Opus `conditional: true`, `reservation:
"Vitamin-A-Supplementierung (VAS) — konditional, mit Vertagungsantrag …"`; GPT + Gemini Pro
`conditional: false`. Ein konditionales Votum **zählt** zum Konsens, ist aber markiert.

**`correction_notice`** — Objekt `{ "date", "text" }`, vorhanden in **2026-07b und 2026-07c**,
**nicht** in 2026-07. Inhalt = Aggregations-Korrektur-Vermerk (Datum 2026-07-14); die
Kurzfassung/der Dissens-Text bleiben unverändert und können der korrigierten Aggregation
widersprechen.

**Kosten liegen INLINE in `session.json` unter `costs`** — **kein** `kosten.json`. Form:
```json
"costs": { "currency": "EUR", "total": 2.6, "fx_rate_usd_eur": 0.85,
  "by_model": [ { "model": "claude-opus-4-8", "label": "Claude Opus",
    "input_tokens": 20886, "output_tokens": 9932, "usd": 0.3527, "eur": 0.2998 }, … ] }
```

---

## 3) Determinismus — jüngste Sitzung nach NUMMER

Die „jüngste Sitzung" wird nach `session.number` (absteigend) bestimmt, **nicht** nach
Datum. Bei gleichem Datum war eine datums-/dateisystem-basierte Auswahl ein Bug (Zufall).
Belege: `sol-build/build.py:latest_session()` sortiert nach `(number, name)` absteigend;
`gremium/run_session.py:prior_session()` sortiert nach Nummer. Aktuell jüngste = **Sitzung 3
= `2026-07c`** (voller Konsens); `2026-07` = **Sitzung 1** (Säule A ohne Konsens).

---

## 4) Assets — Plates mit C2PA (nicht strippen)

Details: `sol-build/site/static/ASSETS.md`.

| Datei | Maße | Größe | Motiv |
|---|---|---|---|
| `sol-build/site/static/ratssaal.png` | 1672 × 941 | ~2,0 MB (2 005 102 B) | Kreisrunder Ratssaal, drei beleuchtete Pulte (Hero + Saal) |
| `sol-build/site/static/vorraum.png` | 1915 × 821 | ~2,0 MB (1 997 325 B) | Vorzimmer, Schiefertafel, Späher, Wart (Vorraum + Archiv) |

- Beide **KI-generiert**, tragen eingebettete **C2PA Content Credentials** (`gpt-image` v2.0,
  `digitalSourceType: trainedAlgorithmicMedia`; Assertions `c2pa.actions.v2` / `c2pa.created`
  / `c2pa.icon`). **Nicht entfernen** — Teil der Transparenz.
- **Optimierte Anzeige-Variante nötig** (~2 MB/Bild ist fürs Web schwer), aber **Original mit
  intakten Credentials behalten**. `sips` strippt C2PA → C2PA-erhaltender Weg (z. B. `oxipng`
  mit Metadaten-Erhalt / Re-Embed via `c2patool`, oder `srcset`-Varianten neben dem Original).

---

## 5) Positiv-Anker — die „Ratssaal"-Sektion des alten Builds

Als gelungenes Vorbild (nur Referenz, keine Design-Vorgabe): die Sektion **„Der Ratssaal"**
im alten SOL-Build — kreisrunde Saal-Plate als Navigation, drei gleich große Pult-Hotspots,
Zählmaschine in der Mitte. Quelle: `sol-build/build.py:378–395` (`class="hall-section"` →
`hall-map`, `machine-symbol`, `hotspot pulpit …`). Live ansehbar in der Review-Auslieferung
(`serve/index.html`, Sektion „Der Ratssaal").
