# Unreferenzierte Medien — bestellt, erhalten, nicht ausgeliefert

Diese `.avif` lagen bis zum 1. August 2026 untracked unter `site/static/media/**`.
Sie sind **bestellte Arbeit** und bleiben deshalb erhalten — aber **kein Code referenziert
sie**, also gehören sie nicht in den Auslieferbaum (`adapter-static` würde sie sonst als
tote Bytes mit deployen).

Warum unreferenziert (Stand Prüfung 2026-08-01, `grep` über `site/src/`):

- **`scenes/*-door-open-display.avif`** (antechamber, archive, hall) — die „Tür-offen"-
  Crossfade-Bilder für `StageHero`s `.room-bg-open`. Der Prop `sceneOpen` wird von **keinem**
  Raum gesetzt (`StageHero` hat `sceneOpen = null` als Default; kein `*Room.svelte` übergibt
  ihn), also lädt der Crossfade nichts.
- **`scenes/doorway-display.avif`, `scene-thumbnails/archive-display.avif`** — von keiner
  vollen `/media/…`-Pfadreferenz im Code getroffen (nur Basisnamen-Kollision mit den
  tatsächlich referenzierten, anders gepfadeten Dateien).
- **`doors/study-door-crop-{hoch,quer}.avif`** — Zuschnitte ohne Einbindung.
- **`ambient/window-{frame,sky}-study.avif`** — Study-Fenster-Ebenen, nicht eingebunden.
- **`actors/register.avif`** — Registerband, nicht eingebunden.

Wird eine davon später gebraucht, zurück nach `site/static/media/<Unterpfad>/` verschieben
und im Code referenzieren. Die Unterordner hier spiegeln den ursprünglichen Pfad.
