# Fieldnote — Abschluss-Durchgang §7 (Sanitizing-Auftrag), 2026-08-01

**Von:** Claude Code · **Grundlage:** `opus5-auftrag-2026-08-01-sanitizing.md` §7 ·
Schnittstellenpapier §5 Punkt 2
**Stand:** Branch `fix/sanitize-model-html` (ab `integration/go-live-0.4`), Sanitizing-Commit
`93e10ef` enthalten · **kein Push, kein Merge**
**Messweg:** headless (Puppeteer, exakte Viewports, dpr 1) gegen den gebauten Go-Live-Stand,
Preview `:4190`. Beleg-Screenshots im Worktree unter `site/qa-belege/` (Dev-Artefakt, nicht
getrackt). Warum headless: die Live-Browser-Umgebung ließ die Fenster­breite nicht unter
innerWidth 1920 stellen (nur Höhe reagierte) — 1280/1440/390 waren so nicht messbar.

## Ergebnis je Prüfpunkt

| § | Prüfung | Ergebnis | Beleg |
|---|---|---|---|
| 7.1 | Türfahrten beide Richtungen Study↔Council↔Archiv | erfüllt — sechs Landungen, je korrekter Inhalt | `trans-1…6` |
| 7.2 | Zurück + erneute Fahrt **ohne Neuladen** | erfüllt — `goBack`→Council→Study, `goForward`→Council, Inhalt stabil, kein Bruch | `trans-4…6` |
| 7.3 | 390 px · `prefers-reduced-motion` · **ohne JS** | erfüllt — alle drei Räume stehen ohne JS (main+Tafel, ~435–447 KB prerendert), reduced-motion sauber | `m390-nojs-*`, `m390-rm-*` |
| 7.4 | Protokoll-Eingang Pult: Ruhe/Hover/Fokus/Touch, ohne JS | erfüllt — Tastaturfokus erreicht das Pult (→`/sitzungen/2026-07c/`), Fokusring + Protokoll-Label; CSS-`:hover` trägt ohne JS | `pultstate-*`, `pult-nojs-*` |
| 7.5 | Pult (z-index:4) über den ganzen Scrollweg, 1280 **und** 1440 | **Befund, belassen** — siehe unten | `pult-1280/1440-worst` |
| 7.6 | Scout Text-über-Figur, 1280, scrollY 410–585 | 41 % Spitze bei scrollY 510 (Band 35–41 %) — **Steward live abgenommen** | `scout-1280-peak` |
| §8 | Zähl-Ruck vorbereitet + abgenommen | `/ratssaal/`, Trommel mittig (Hotspot x 40–60 %, y 66–78 % der Platte), Hover-Auslöser — **Steward live abgenommen** | `drum-rest` |

## §7.5 — der eine Befund, bewusst belassen

Bei **scrollY ≈ 200** überlappt der unsichtbare `.pult-hit` (`z-index:4`, `pointer-events:auto`)
die rechte Ecke der **Sitzungsarchiv-Karte** — **17 470 px² bei 1280**, **24 692 px² bei 1440**.
Wirkung: ein Klick genau dort öffnet das Pult-Protokoll statt des Archiv-Eintrags. **Optisch ist
nichts verdeckt** (die Trefferfläche ist transparent), die Haupt-Tafel oben ist nie betroffen, und
der `--retreat` (22vw) zieht das Pult bei weiterem Scrollen frei — deshalb liegt der schlimmste
Stand früh, vor vollem Rückzug.

**Steward-Entscheid 2026-08-01: belassen** als geringfügiger Randfall. Der Befund ist zusätzlich als
Kommentar direkt an `.pult-hit` in `ArchiveActors.svelte` vermerkt, damit ihn ein künftiger
Bearbeiter an der Stelle sieht und nicht still „repariert". Falls je behoben: **`--retreat` früher
greifen lassen** (Pult vor scrollY 200 frei), **nicht** den z-index für den Fluss erhöhen.

## Reibung / fürs nächste Mal

- Die Breiten-Sperre der Live-Browser-Umgebung (innerWidth fix 1920) kostete drei Anläufe. Puppeteer
  headless war der verlässliche Weg zu exakten 1280/1440/390 und liefert reproduzierbare Belege —
  beim nächsten breitensensiblen Durchgang gleich so beginnen.
- Der Scout-Prozentwert (41 %) stammt aus einer eigenen Metrik (Figurfläche unter Text) und ist mit
  der früher genannten Zahl (30/37/33 %) nicht direkt vergleichbar; der Steward hat live abgenommen.
