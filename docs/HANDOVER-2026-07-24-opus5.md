# Übergabe — NobleCause.ai Bühnenspiel (Stand 2026-07-24, für Opus 5)

**Zweck:** Ein einziger Einstiegspunkt für einen frischen Opus-5-Start — als Architekt/
Berater (Chat) **oder** als CC (Bau). Der bisherige Architekt-Thread (Opus 4.x) wird hier
übergeben, weil er sehr lang ist und Opus 5 gewünscht ist. Lies zuerst dieses Dokument,
dann die verlinkten Docs nach Bedarf.

---

## 1 · Was NobleCause ist
Ein öffentliches KI-Deliberationsprotokoll: mehrere KI-Modelle verschiedener Familien
(Anthropic, OpenAI, Google — bald mehr) prüfen dieselben Belege und empfehlen öffentlich,
wo eine Spende in vier Bereichen am meisten bewirkt. Alles wird veröffentlicht:
Empfehlungen, Meinungsänderungen, Uneinigkeit, Kosten. **Es fließt kein Geld über die
Seite** — Spendenlinks führen direkt zu den Organisationen. SvelteKit + `adapter-static`;
Deploy = GitHub Actions build → rsync → Caddy auf VPS.

## 2 · Der aktuelle Auftrag: das Bühnenspiel
Die Site ist als **Haus mit drei Räumen** gebaut, jeder Aufruf ein Bühnenauftritt: man
betritt einen Raum, die Beteiligten treten auf, die Antwort erscheint auf einer reisenden
Tafel, eine Tür führt weiter. Räume als echte prerenderte Routen:
`/` (The Study) · `/ratssaal/` (The Council) · `/archiv/` (The Archive), je + `/en/…`.
Vollständige Vision: **`docs/buehnenspiel-gesamtbild-fuer-kimi.md`**.

## 3 · Rollen (Stand jetzt)
- **CC = Bau** (ab jetzt auf Opus 5). Kimi wurde der Bauauftrag entzogen (Qualität + der
  Steward stieß an ein Usage-Limit). Falls Kimi wieder verfügbar ist, darf er CCs Code
  **bewerten**, nicht bauen.
- **Fable = Wart** (claude-fable-5, claude.ai): Governance, Klartext-Freigaben, Journal.
- **Codex/ChatGPT = Bilder** (Serien-Aufträge, Kontaktbogen-Gates).
- **Opus = Architekt/Berater** (dieser Platz — jetzt Opus 5).
- **Steward = der Nutzer** (Afschin), letzte Instanz.

## 4 · Harte Prinzipien (Verfassungsrang — nie brechen)
- **§0:** Die Seite ist vollständig, bevor das Spiel beginnt. No-JS / `prefers-reduced-
  motion` = derselbe vollständige Zustand. Inszenierung verzögert und bewegt nur, erzeugt
  und versteckt nie Inhalt.
- **Der 80-Jährige:** muss in 30 Sekunden finden, wohin er spenden kann. Lesbarkeit ist der
  **Boden**, nicht das Ziel.
- **Versiegelte Datennaht:** Das Frontend paraphrasiert nie; sitzungsabhängiger Text kommt
  aus den Daten, feste Copy aus i18n (`de.js`/`en.js`, Spiegel).
- **Tabu-Pfade auf dem Frontend-Branch:** `sessions/**`, `journal/**`, `schema/**`,
  `gremium/**`, `schedule.json`, `prompts.py`. Ein **`pre-commit`-Guard-Hook**
  (`.git/hooks/pre-commit`) blockt Commits, die diese Pfade auf `feat/immersive-homepage*`
  oder `feat/council-rooms*` berühren (auf anderen Branches no-op). Nicht mit `--no-verify`
  umgehen. Datenpublikationen laufen auf einem Nicht-`feat/*`-Branch (siehe §6).
- **Kanten-/Bühnen-Prinzip:** **`docs/szene-kantenprinzip-fuer-kimi.md`** — bewegliche
  Elemente sind viewport-kantenverankert, `position: fixed` (fixe Bühne, scrollen NICHT
  vertikal mit, nur seitliches Ausweichen via `--retreat`). Tafel = Asset oben-links,
  reist per VT `board`. Kopf = `view-transition-name: masthead`, ganz oben, stabil.

## 5 · Zustand je Raum
- **The Study — visuell fertig.** Neue Plates (`antechamber-*`), **sitzender Scout**
  (`actors/scout.avif`, aus dem 24.07-Kontaktbogen freigestellt), Warden, driftende Wolke
  (Ruhewert 13 s/20 s), Klartext live. Offene Feinrunde: siehe §7.1/§7.2.
- **The Council — vermutlich integriert, VERIFIZIEREN.** Kimi berichtete Einbau der neuen
  Saal-Plates + N Lesepulte (`hall-door-open-display.avif`, `hall-portrait-*`,
  `actors/lectern.avif` liegen vor). Der Steward sah aber noch alte Hintergründe —
  **mutmaßlich stale `vite preview` (sirv)-Cache** (Kimi-Befund: Preview nach jedem Build
  neu starten). **Erster Schritt: Preview frisch bauen/starten und prüfen, ob die neuen
  Council-Plates live sind, bevor irgendetwas neu gebaut wird.**
- **The Archive — alte Kulisse, Art offen.** `archive-*` sind die alten Plates. Serie 3
  (Register/Karteikästen) ist gerade erst als Prompt formuliert (in Kimis letztem Bericht),
  **noch nicht geliefert**. Danach: Gate + Einbau, gleiches Kantenprinzip.

## 6 · Git-Situation
- Branch **`feat/council-rooms`** (Wegwerf-Präsentationsbranch laut `AGENTS.md`).
- Letzter Commit **`f3e67ed`** = die Klartext-Datenpublikation (3 `session.json` + Journal),
  sauber auf einem Datenbranch erzeugt und per Fast-Forward hereingezogen (Guard-Hook nicht
  umgangen). `data/klartext-bootstrap` zeigt auf denselben Commit — löschbar.
- **~136 uncommittete Einträge** = Kimis gesamte Frontend-Arbeit (bewusst „kein Commit"-
  Disziplin; wird später gesquasht/gemerged). Trunk ist **`master`**.
- Klartext-Schicht **live**: `homepage.js` liest `session.plain`; alle drei Sitzungen
  zeigen echten Klartext. EN fällt auf DE mit Sprachhinweis zurück (EN-Klartext ist offen).

## 7 · Offene Bau-Punkte (priorisiert)
1. **Akteur-Fix (sichtbarer Fehler):** Akteure scrollen zur Decke, weil `.rail`/`.scene2`
   `position: absolute` im scrollenden Hero sind (Wolke/Tür-Schimmer wurden gefixt, die
   Schienen nicht). Ein-Zeilen-Fix + Warden auf Scout-Bodenlinie:
   **`docs/cc-fix-akteure-fixe-buehne.md`**. Schnellster Gewinn — zuerst.
2. **WebGL-Portal (Steward-Entscheid):** Der „durch die Tür"-Übergang wird mit
   **Three.js** gebaut — als Enhancement über dem 2D-Boden, §0 bleibt. Phasen-Plan:
   **`docs/webgl-portal-architektur-plan.md`** — **dieser Plan ist von Opus 5/CC zu
   prüfen, bevor gebaut wird.** Phase 0 = Parallaxe-Spike über dem Study, dann Portal.
   Hintergrund zum „warum überhaupt": die Vorlage (motionsites dreamcore) ist ein
   3D/WebGL-Template; unser 2D-Plate-Ansatz stößt genau am Tür-Durchflug an die Decke.
3. **Council verifizieren + ggf. Feinschliff** (§5), Kantenprinzip anwenden (Pulte von
   unten ist schon so gebaut).
4. **Archive komplett:** Serie 3 (Register) liefern → Gate → einbauen.
   Bild-Bestelldisziplin: analog **`docs/codex-serie-2-council.md`** (Plate ohne
   einfahrende Elemente, Cutout mit Alpha/Chroma-Grün-Fallback, gleiche Welt).
5. **Vor Go-Live:** EN-Klartext (eigener Wart-Nachtrag), Gründungs-/Founder-Story in den
   eigenen Worten des Stewards, echtes-Gerät-Mobiltest, tote Design-PRs schließen,
   squash/merge auf `master`, Klartext-Daten-Commit sauber auf `master` cherry-picken.

## 8 · Raum-Inhalt & Texte (falls Content angefasst wird)
Finalisiert in **`docs/raum-content-final-fuer-kimi.md`** (Reihenfolge/Copy je Raum,
Klartext-Schema, Ausklapp-Disziplin) und **`docs/titelbereich-neuordnung-fuer-kimi.md`**
(stabiler Kopf oben + dynamischer Raumteil, FlowRail entfernt, Raumwort Study/Council/
Archive). Klartext-Governance + Freigabe: **`docs/fable-2026-07-24-klartext-freigabe.md`**,
Entwurf/Fundstellen: **`docs/klartext-entwurf-bestandssitzungen.md`**.

## 9 · Build & Verifikation
- `npm run build` in `site/` muss warnungsfrei sein; Testsuite (zuletzt 21/21).
- **Nach jedem Build den Preview neu starten** (`vite preview`/sirv cached Assets im
  Speicher — sonst misst/sieht man den alten Stand). Bekannte Falle.
- Reflow 320/390 per CDP-Emulation (`mobile:true`), 6 Routen, kein Overflow.
- No-JS + reduced-motion = voller Ruhezustand, bitidentisch mit dem JS-Endzustand.
- Kein Commit ohne Steward-Freigabe; Tabu-Pfade/Guard-Hook beachten.

## 10 · Dokument-Index (kanonisch, aktuell)
- Vision: `buehnenspiel-gesamtbild-fuer-kimi.md`
- Prinzip fixe Bühne/Kanten: `szene-kantenprinzip-fuer-kimi.md`
- Raum-Content final: `raum-content-final-fuer-kimi.md` · Titel: `titelbereich-neuordnung-fuer-kimi.md`
- Akteur-Fix: `cc-fix-akteure-fixe-buehne.md`
- WebGL-Plan: `webgl-portal-architektur-plan.md`
- Bilder: `codex-serie-1b-study-nachbestellung.md`, `codex-serie-2-council.md`
- Klartext: `fable-2026-07-24-klartext-freigabe.md`, `klartext-entwurf-bestandssitzungen.md`
- Wolken-Bug/Tuning: `bug-wolken-raster-und-scroll.md`
- Ältere Synthese (Kontext): `fable-2026-07-19-buehnenspiel-synthese-umlauf--mit-runde3-codex.md`, `opus-buehnenspiel-plan.md`
- Projektregeln: `../AGENTS.md`

## 11 · Ton/Arbeitsweise mit dem Steward
Deutsch, knapp, sachlich. Er ist Informatiker (20 J. IT-Beratung, 10 J. SAP BI) — bei
Coding-Aufgaben Tools/Architektur selbst wählen, aber **als Plan vorlegen** und begründen.
Er schätzt ehrliche Fehlerbenennung (eigene Fehler offen zugeben), Gegenrede mit Substanz
und Entscheidungen, die er selbst treffen kann, sauber herausgearbeitet.
