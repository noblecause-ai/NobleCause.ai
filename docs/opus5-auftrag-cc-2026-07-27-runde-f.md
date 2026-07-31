# Auftrag an CC — Runde F: Medaillons einbauen, Datenbranch entflechten, §7

**Von:** Opus 5 · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

---

## §1 · Datenbranch-Basis — Entscheid

**Rekord-Daten dürfen nicht an einem Feature-Branch hängen.** `master` ist der Stamm des Rekords;
alles andere überlebt die UI nicht.

1. Prüfen, ob `master` **Vorfahre** des letzten Datenstands ist (der Stand mit `model_label` und
   den Schemas aus `cef3faf` / `f3e67ed`).
2. Wenn ja: `master` per `--ff-only` auf diesen Stand bringen. **Dann** den neuen Datenbranch
   **von `master`** abzweigen und die Commission-Records darauf setzen.
3. Wenn `master` divergiert ist: **nichts mergen, Lage berichten** — mit der Angabe, welche
   Commits auf welcher Seite stehen.

Nie `--no-verify`. Der Guard bleibt an.

---

## §2 · Was in den Rekord kommt — ehrlich, so wie es gelaufen ist

Der Steward hat entschieden, **ohne Wart-Rücksprache weiterzugehen**. Das ist zulässig — der Wart
hat den Rahmen gesetzt, die Prüfung ist mechanisch, und alle drei Bestellungen erfüllen ihn. Aber
der Rekord muss zeigen, **wer** entschieden hat, nicht so tun, als hätte der Wart geprüft.

- `warden_review`: Entscheid **Steward**, nicht Wart; Datum; Vermerk sinngemäß „Rahmen erfüllt,
  Annahme durch den Steward ohne Wart-Vorlage".
- `person`: bei Gemini **„Florence Nightingale"** eintragen (†1910). Bei Opus und GPT `null`.
- `within_limits: false` bei Opus **bleibt stehen**, dazu der Vermerk, dass der Überhang von
  19 Zeichen angenommen wurde — die Grenze war Architektensetzung und ist inzwischen aufgehoben.
- **Ein Bildlauf je Modell statt drei.** In die Registratur schreiben, wie es war (`renders: 1`).
  Die Gleichbehandlung bleibt gewahrt — alle drei bekamen einen Lauf —, aber die Abweichung vom
  geplanten Verfahren gehört in den Rekord, nicht in die Erinnerung.

**Nichts an den Bestelltexten ändern.** Sie sind Rekord: wörtlich, unverändert, auch die
Überlänge.

---

## §3 · Medaillons einbauen

Die drei Bilder liegen unter `docs/`.

- Keying wie gehabt (Magenta → Alpha, v5-Kette), Despill, bbox-Crop. Der Medaillonrand ist
  **rund und hart** — auf Fransen an der Rundung besonders achten, dort fällt Treppung auf.
- Ablage `site/static/media/actors/` oder ein eigener `medallions/`-Ordner, deine Wahl; Namen
  nach Modellkennung, nicht nach Anzeigename.
- **Kleinauflösung** mitliefern, wie bei den fernen Plates — die Medaillons erscheinen klein.
- Alle drei nebeneinander gegenprüfen: gleiche Größe der Prägefläche, gleicher Randanteil,
  vergleichbare Helligkeit. **Weicht eines sichtbar ab, berichten statt angleichen** — sie sind
  Rekord-nah, und stilles Nachbearbeiten wäre ein Eingriff.

Der Lauf war laut Steward „buggy"; wir arbeiten mit dem Ergebnis. Wenn dir beim Keying
Artefakte auffallen, die den Einbau gefährden: berichten, nicht retuschieren.

---

## §4 · §7 — die Medaillons umkreisen die Zählmaschine

Konzept unverändert in `docs/opus5-konzept-2026-07-27-durchgang-und-sitze.md` §7 und
`opus5-auftrag-cc-2026-07-27-runde-d.md` §7. Bindend:

- Billboard-Ellipse, b deutlich kleiner als a; aus dem Winkel folgt die Tiefe, aus der Tiefe
  Skalierung (≈ 0,62 → 1,0), Helligkeit, ein Hauch Blur und `z-index`.
- **Echte Verdeckung** braucht das Vordergrund-Cutout der Zählmaschine. **Zuerst den Freischnitt
  am `hall`-Plate versuchen**, wie bei den Türen — trägt er nicht, abbrechen und berichten, dann
  bestelle ich. Ohne Cutout wird §7 **nicht** mit halber Verdeckung gebaut.
- Einflug nach dem Eintrittstakt der Pulte, Ankunft mit leichtem Überschwingen, dann Kreisen.
  Kein Blinken, kein Aufleuchten.
- Kreisen nur im Ruhezustand; auf `--retreat` weitet sich die Ellipse. Eine rAF-Schleife,
  pausiert bei `hidden` und außerhalb des Viewports. Umdrehung 40–60 s.
- §0: Ruhepositionen im prärenderten HTML; reduced-motion und No-JS zeigen die Medaillons still.

**Bauvorgabe aus dem Gesichter-Entscheid, jetzt bindend:** Der **Modellname steht immer am
Medaillon** — nie das Bildnis allein. Das ist der Schutz gegen „Nightingale empfiehlt" statt
„Gemini empfiehlt" und keine Gestaltungsfrage. Plakettengrammatik wie Scout/Warden/Pulte.

Motiv- und Begründungstext gehören **nicht** in den Raum — sie liegen eine Ebene darunter und
kommen mit dem Protokoll-Explorer.

---

## §5 · `docs/`-Reorg — Entscheid zur vorgelegten Liste

- **B** (SKIP-Pläne, `webgl-portal-architektur-plan`) → `docs/archiv/`. Freigegeben.
- **C** → `docs/archiv/`, freigegeben für die Codex-Ära, die Kimi-Ära und die
  Pre-CC-Bühnenspiel-Entwürfe. Je eine Zeile im Kopf, warum überholt.
- **`codex-serie-1..4-*`** → **Provenienz**, nach `docs/asset-originals/`. Es sind
  Bestellungen, keine Baupläne; sie erklären, wie die Bilder entstanden sind, und gehören zu
  ihnen.
- **A** (70 Bild-Originale): beim Verschieben je Bild einmal ansehen und nach Serie/Position
  benennen, wie du vorgeschlagen hast. Das ist Fleißarbeit ohne Abkürzung — lieber langsam als
  falsch einsortiert.
- **D** bleibt unberührt.

Verschieben, nicht löschen. Was weg soll, macht der Steward.

---

## §6 · Reihenfolge

1. §1 Datenbranch-Basis klären → berichten, **bevor** committet wird.
2. §2 + §3 Records und Medaillons.
3. §4 Freischnitt-Versuch Zählmaschine → dann §7 oder Abbruchbericht.
4. §5 `docs/`-Reorg.

**Danach steht als Letztes vor Go-Live der Protokoll-Explorer inkl. 2b.**

Guardrails unverändert: Guard-Hook, Datenbranch + `--ff-only`, nie `--no-verify`, kein Push,
§0-Verfassung, versiegelte Datennaht, Geometrie am gerenderten AVIF.
