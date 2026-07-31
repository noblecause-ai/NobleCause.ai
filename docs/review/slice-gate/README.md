# Slice-Gate — Artefakte (B1/B2/B4 + Replikation)

Lauf: 2026-07-19, Branch `feat/council-rooms`, Brave headless (Chrome 150) per CDP,
Preview aus `site/build` (adapter-static). **36/36 Checks OK** — siehe `checks.txt`.

## B1 (sperrend) — Reflow 320/390, per CDP-Emulation (Falle 9)
- Vier Study-Konfigurationen (320/390 × DE/EN): **OK**, scrollWidth = Viewport in den
  Zuständen Eingang/Mitte/Ende. Screenshots `b1-{320,390}-{de,en}-{eingang,ende}.png`.
- LEEP-Sichtprobe 320 px: bricht sauber auf 3 Zeilen (`b1-320-de-tafel-leep.png`).
- **Befund+Fix:** Röhrenschiene überlief 320 px (rechts ~18 px). Fix `StageTube.svelte`:
  `.bead-name max-width:100%` + neue ≤360-px-Stufe. Re-Messung grün.

## B2 (sperrend) — Fokusring als Verhalten (echte Tab-Sequenz)
- 6 Röhren-Perlen: `outline solid 2px rgb(215,170,85)` — Clips `b2-perle-{1,2,6}.png`.
- 4 Spendenlinks: Browser-Default-Ring, sichtbar auf dunkler Tafel — Clips
  `b2-spendenlink-{1..4}.png`. Kein Eingriff nötig.
- 2 Tür-Links: Bernstein-Outline + Box-Shadow — Clips `b2-tuer-link-{1,2}.png`.
- **Befund+Fix (vorab deklariert):** Perlen hatten kein `tabindex` — Minimal-Nachrüstung
  `tabindex="0"` + `:focus-visible`-Ring. Keine Mechanik-Änderung.
- Testfalle dokumentiert: Screenshot-`clip` ist dokument-relativ (Chrome 150).

## B4 (nicht sperrend) — Preload
- Feuert real: Tür ≥60 % sichtbar + Lock ⇒ 1 Request `hall-display.jpg` (mobil, 390 px).
- Navigation hängt nie daran: `saveData` erzwungen ⇒ Preload 0 Requests, Tap navigiert
  trotzdem vollständig nach `/ratssaal/` (Tafel gerendert nach ~830 ms).

## Replikation (nach B1+B2 grün, ohne Prüfrunde)
- B1 auf `/ratssaal/`, `/archiv/`, `/en/council/`, `/en/archive/` bei 320 + 390:
  **8/8 OK** (Screenshots `b1-repl-320-*.png`).
- B2-Stichproben je Raum (Perlen, Spendenlinks, Tür-Links): **alle Ringe sichtbar**.

## Verifikation
- `npm test`: **18/18 grün** · `npm run build`: warnungsfrei.
- `git status`: nur `site/`, `docs/`, `AGENTS.md` (Standing Rule). Kein Commit.

Publikations-Notiz: vier Gerüst-Funde vor Kunst, 2,1 KB Choreografie — „Gerüst vor
Kunst" ist ein Messergebnis. Dazu kamen im Gate zwei weitere Messfunde (Röhren-Overflow
320 px, Archiv-Plate 579 KB als Budget-Ausreißer).
