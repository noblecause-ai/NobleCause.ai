# Übergabe an die neue Architekt-Session — Stand der Räume (2026-07-27)

**Von:** CC · **Branch:** `feat/council-rooms` · **Zweck:** Kontext für Opus 5 nach Session-Verlust.

## 1 · Was zuletzt gebaut wurde (chronologisch)

Auf Basis von vier Aufträgen dieser Runde (`opus5-auftrag-archive-einbau.md` + `-nachtrag`,
`opus5-auftrag-council-tuer.md`, `opus5-korrekturen-und-portalfrage.md`):

- **§4 Zeitschicht + Tafel Weg A + Checkpoint-Fixes** — committet `0b80df1`.
- **Datenbranch (EN-Klartext, S3-Säule-B, `model_label`)** — via FF `cef3faf` (Sitzungen/Journal).
- **The Archive** (Türhotspot → Study, Crossfade mit gefedertem Tür-Composite, `ArchiveActors`,
  i18n, Tests) — committet `71690c3`.
- **Tür-Hotspot im Ratssaal** (Council → Archive) — committet `ee4443e`.
- **§3 „nicht zwei gleiche Möbel"** — Pult mit Leuchte gekeyt + `ArchiveActors` umgebaut (links
  leuchtendes Pult, rechts EIN Karteikasten) — **gebaut & verifiziert, UNCOMMITTET** (Freigabe stand aus).

## 2 · Aktueller Stand

**Committet auf `feat/council-rooms`** (kein Push): `ee4443e` ← `71690c3` ← `cef3faf` ← `0b80df1`.

**Uncommittet (§3, verifiziert, wartet auf Commit-Freigabe):**
`ArchiveActors.svelte` (M), `i18n/de.js`+`en.js` (M, `pultAlt`), `tests/homepage-build.test.js` (M).
Build warnungsfrei, **23/23 Tests grün**.

**Medien-Strang (wichtig):** ALLE `site/static/media/**/*.avif` sind **untracked** (jpg→avif-Migration
+ alle Cutouts/Plates/Tür-offen-Composites, inkl. `actors/pult-lamp.avif`, `actors/register.avif`,
`scenes/archive-*.avif`). Der Raum-Code referenziert sie; lokal rendert alles, aber ein sauberer
Checkout von HEAD findet die Kulisse erst nach einem Medien-Commit. Das ist ein **separater Strang,
nicht Teil der Raum-Commits** (bewusst so gehalten). **Muss vor Go-Live committet werden.**

**Drei-Räume-Rundgang steht:** Study → Council → Archive → (zurück) Study. Alle drei haben jetzt
einen In-Szene-Türhotspot (Desktop, ≥1200 px) + Crossfade auf ein Tür-offen-Plate; Portalblende
liest ihr Rechteck beim Klick (`room-transitions.js`, unverändert). Türgeometrie ist **per Raum**
gemessen (Study 40–60/17–82, Council 43,5–57,9/18,3–65,9, Archiv 43–54,5/19,5–62,5 — das war nie
identisch, und das ist der Normalfall).

## 3 · Offene Queue (aus `opus5-korrekturen-und-portalfrage.md`, je eigene Runde)

- **§1 Council-Crossfade** — `hall-door-open` ist eine separate Generation (außerhalb der Tür
  5,86 / 17,96 % > 8 → der halbe Raum blendet um). **Fix bekannt und erprobt:** dieselbe gefederte
  Tür-Composite-Technik wie beim Archiv (dort 1,06 / 0,30 %). Study prüfen (0,78 / 0,65 %,
  grenzwertig, vermutlich lassen).
- **§2 Council-Sitzzeilen über die Pulte** — `figcaption` an die Oberkante des Pults, `z-index`
  über dem Bild (die `.pult img z-index:1`-Falle beachten), Vignette statt Kasten. Wie Scout/Warden.
- **§4 (des Docs) Protokollseiten** — `/sessions`, `/sessions/[id]`, `/journal`, `/journal/[id]`
  liegen außerhalb der `(rooms)`-Gruppe und tragen noch das alte Dokumentlayout. Opus 5 nennt das
  **die letzte große Designlücke vor Go-Live** — ein eigener Explorer über die Protokolle (Überblick,
  Filter nach Bereich/Sitzung, Wortlaut eine Ebene darunter). Eigene Runde, nicht in die Korrekturen
  mischen.
- **§5/§6 Echter Türdurchgang** — statt des gemalten Ersatzes hinter dem Türspalt das echte
  Ziel-Plate. Opus 5: möglich **ohne Three.js** (`perspective`+`translateZ` auf einer eigenen
  Übergangsebene, VT während der Fahrt aus). Braucht vermutlich **keine Bestellung**: Wand-Plate mit
  Loch + Türblatt als Ebene = Maskierarbeit am vorhandenen Plate. **Nächster konkreter Schritt = ein
  Spike:** im Study-Plate die Türflügel entlang der Laibung freischneiden und prüfen, ob die Öffnung
  sauber liest (Laibung/Sturzschatten/Schwelle stehen bleiben). Trägt der Schnitt → Phase 1 in
  Reichweite; trägt er nicht → ein Wand-Plate vom Generator, für den Preis einer Stunde.
- **§7 Rotierende Sitze um die Zählmaschine** — Billboard-Ellipse (Umkreisen, nicht Drehen), nur im
  Hero-Band/Ruhezustand, weicht beim Scrollen an die Ränder. Teilt Übergangsebene + Tiefenlogik mit
  §6 → **erst der §6-Spike**, dann beides zusammen.

## 4 · Zwei kleine Ermessenspunkte im Archiv (Steward-Veto möglich)

- Register **auch auf Mobil** sichtbar (an den Ecken als Vordergrund-Möbel) — aktuell ja.
- **Mobiler Türschimmer** — subtiler 14%-Glow, auf ≈ 27 vw gesetzt (Tür sitzt am „right top"-Crop
  links der Mitte).

## 5 · Arbeitsweise / Guardrails (für Kontinuität)

- Plan → Steward-Freigabe → Bau → Browser-Verifikation → Bericht → **Commit nur auf ausdrückliche
  Freigabe.** Kein Push.
- **Guard-Hook** blockt Commits an `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`,
  `schema/**`, `prompts.py` auf `feat/*`. Daten landen via **eigenem Datenbranch + `git merge
  --ff-only`** (Präzedenz `cef3faf`, `f3e67ed`) — **nie `--no-verify`.**
- **Asset-Pipeline** (kein ImageMagick auf der Maschine): `avifenc -s 6 -q 55` (Duell gegen
  `cwebp -q 80`, kleinere gewinnt); Magenta→Alpha-Keying über eine Python-„v5-Kette"
  (`ffmpeg`→roh-RGBA → Ecken-Median-Key SAD T=100, border-connected, 1-px-Erode, Despill,
  bbox-Crop). Skripte im Scratchpad. Geometrie IMMER am gerenderten AVIF messen, nicht am Master.
- **§0-Verfassung:** voller Inhalt ohne JS und bei `prefers-reduced-motion`; Bühne verzögert/bewegt
  nur, erzeugt/versteckt nie; kein `buildTime`, kein Überfällig-Zustand. Kantenprinzip: bewegte
  Bühnenelemente `position: fixed`, von der Kante, Rückzug nur über `--retreat`.
- **Versiegelte Datennaht:** Frontend paraphrasiert nie; Sitzungs-/Journaltext wörtlich; Renderer
  parst keine Prosa (nur strukturelle Signale wie `search_queries`).

## 6 · Empfohlene Reihenfolge für die neue Session

1. **§3 committen** (Freigabe erteilen — ist gebaut/grün) → dritter Raum-Commit.
2. **§1 Council-Crossfade** (schnell, Technik steht) + **§2 Sitzzeilen** — die zwei kleinen
   Council-Korrekturen abräumen.
3. **§6-Spike** (Türflügel-Freischnitt) — entscheidet über den echten Durchgang UND §7.
4. **Protokollseiten** als eigenes großes Paket planen — die letzte Designlücke vor Go-Live.
5. Vor Go-Live: **Medien-Strang committen** (die untracked AVIF).
