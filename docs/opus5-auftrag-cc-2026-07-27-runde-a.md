# Auftrag an CC — Runde A: Archiv committen, Council-Korrekturen abräumen

**Von:** Opus 5 (Architekt) · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Vorlage:** `docs/handover-cc-2026-07-27-council-rooms.md` (dein eigener Übergabestand)
**Arbeitsweise:** Plan → Freigabe → Bau → Browser-Verifikation → Bericht. **Commit nur auf
ausdrückliche Freigabe. Kein Push.**

---

## §0 · Vorab: eine verwaiste Lock-Datei

Beim Statuslesen ist `.git/index.lock` entstanden und blockierte git. Sie wurde nach
`.git/index.lock.stale-remove-me` verschoben — git läuft wieder. **Bitte diese Datei löschen**
(sie ist leer und funktionslos, stört aber im Verzeichnis).

---

## §1 · Das gebaute Archiv-Möbel committen — Freigabe erteilt

`ArchiveActors.svelte` + `i18n/de.js`/`en.js` (`pultAlt`) + `tests/homepage-build.test.js` sind
gebaut, verifiziert und laut deinem Bericht 23/23 grün. **Freigabe ist hiermit erteilt.**

Vorher einmal `npm run build` und die Tests laufen lassen — nur, um sicherzugehen, dass der
Zustand seit deinem Bericht unberührt ist.

**Nur diese vier Dateien in den Commit.** Der Arbeitsbaum trägt daneben einen ganzen Strang
`jpg → avif`-Migration (gelöschte `.jpg`, untracked `.avif`), Änderungen an `AGENTS.md`,
`app.html`, `EmblemLegend`, `RecommendationCard`, den Journal-Seiten, `schedule.json` und zwei
gelöschte Komponenten (`FlowRail`, `RoomHero`). Das ist **nicht** Teil dieses Commits.

**Bericht erbeten:** eine Zeile pro offenem Strang — was ist das, wohin gehört es, blockiert es
Go-Live? Insbesondere: gehören `FlowRail`/`RoomHero` wirklich gelöscht, und warum steht
`site/static/schedule.json` im Arbeitsbaum, obwohl der Guard-Hook Daten schützt?

---

## §2 · Council-Crossfade auf die Archiv-Technik umstellen

`hall-door-open` ist eine eigene Generation und weicht außerhalb der Tür um 5,86 / 17,96 % ab —
beim Blenden wandert der halbe Raum. Im Archiv ist dasselbe Problem mit dem **gefederten
Tür-Composite** gelöst (1,06 / 0,30 %). Diese Technik unverändert auf den Ratssaal übertragen.

**Study nicht anfassen** (0,78 / 0,65 % — grenzwertig, aber unauffällig; ein Eingriff dort ist
Risiko ohne Gewinn).

**Abnahme:** außerhalb der Türkontur ist während der Blende keine Bewegung sichtbar; Werte im
Bericht nennen.

---

## §3 · Council-Sitzzeilen über die Pulte

`figcaption` an die **Oberkante** des Pults, `z-index` über dem Bild — die
`.pult img { z-index: 1 }`-Falle beachten. **Vignette statt Kasten**, exakt wie die
Scout-/Warden-Plaketten im Study (`c87cb97`). Kein neuer Text, keine neue i18n-Zeile.

**Abnahme:** Plakette liest auf hellem wie auf dunklem Pultgrund; kein Layoutsprung beim
Einfahren; Fokusreihenfolge unverändert.

---

## §4 · Was in dieser Runde ausdrücklich NICHT passiert

- **Kein Anfassen des Archiv-Plates.** Eine Bild-Bestellung läuft
  (`docs/bestellung-serie-5-archiv-2026-07-27.md`): geräumte Flanken + Tür in Ebenen. Der
  Einbau ist Runde B und braucht die neuen Bilder.
- **Kein Türdurchgang, keine Sitze um die Zählmaschine.** Beide hängen an derselben
  Übergangsebene und kommen als eigener Auftrag, sobald das Konzept steht.
- **Keine Protokollseiten.** Eigenes Paket.
- **Kein Medien-Commit.** Der avif-Strang wird gebündelt committet, kurz vor Go-Live, in einer
  eigenen Runde — nicht nebenbei.

---

## §5 · Guardrails (unverändert)

- Guard-Hook blockt `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`, `schema/**`,
  `prompts.py` auf `feat/*`. Daten nur über eigenen Datenbranch + `git merge --ff-only`.
  **Nie `--no-verify`.**
- §0-Verfassung: voller Inhalt ohne JS und bei `prefers-reduced-motion`; die Bühne verzögert
  und bewegt, sie erzeugt und versteckt nie. Kein `buildTime`, kein Überfällig-Zustand.
- Versiegelte Datennaht: das Frontend paraphrasiert nie.
- Geometrie immer am gerenderten AVIF messen, nie am Master.
