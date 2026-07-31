# Auftrag an CC — Runde G: Der Durchgang ist weg. Zuerst das.

**Von:** Opus 5 · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

---

## §1 · Regression — der Raumübergang ist wieder eine Blende

**Steward-Befund:** Der Durchgang, der in Runde C in allen drei Räumen live bestätigt war, ist
weg. **Das hat Vorrang vor allem anderen in dieser Runde.**

Zwischen „bestätigt" und „weg" liegen genau drei Commits:

| Commit | Was |
|---|---|
| `af8eca7` | Passage (Stand: bestätigt) |
| §1-Commit Ruhe-Stapel | Ruhezustand aus dem Ebenenstapel |
| `d1b20ed` | Council-Türmitte **+ Freischnitt-Fix** |
| `22f2575` | Medien-Strang, **10 Dateien ausgeschlossen** |

**Zwei Verdächtige, in dieser Reihenfolge prüfen:**

**1. Der Medien-Commit.** Unter den zehn als „unreferenziert" ausgeschlossenen Dateien sind
**drei `door-open`-Auf-Plates**. Wenn irgendein Pfad — Fallback, Hover vor dem Ruhe-Stapel,
Mobil, reduced-motion, oder ein Zweig, der bei fehlendem `decode()` greift — sie noch anfährt,
fehlt die Kulisse und der Übergang fällt auf die Portalblende zurück. **Referenz-Check
wiederholen, aber gegen den gebauten Zustand**, nicht nur gegen Quelltext-Verweise: fehlende
Datei im Netzwerk-Log ist der Beweis, ein `grep` ist es nicht.

**2. Der Türmitte-Fix.** `perspective-origin` kommt jetzt zur Laufzeit. Rechnet er im Council
richtig, aber in Study und Archiv falsch — oder liefert er vor dem ersten Layout `0/0` — dann
zielt die Kamera daneben und die Fahrt liest wieder als Zoom. Der „Freischnitt-Fix" im selben
Commit ist ein zweiter Kandidat: er hat an denselben Ebenen gearbeitet.

**Vorgehen:** Nicht raten. **Bisect gegen das Abnahmekriterium**, das schon einmal funktioniert
hat — Frame-Reihe 0/25/50/65/80/100 %, bei 65 % ist die Ausgangswand aus dem Bild, die letzten
35 % sind reiner Zielraum. Je Raum. Der erste Commit, bei dem das Kriterium fällt, ist die
Ursache.

**Bericht:** welcher Commit, welche Zeile, warum es durch die Abnahme gekommen ist. Der letzte
Punkt ist der wichtigste — dieses Kriterium existiert genau dafür, und es hat diesmal nicht
gegriffen. **Wenn die Abnahme nach dem Türmitte-Fix nicht erneut gefahren wurde, sag das.** Eine
Lücke im Verfahren ist ein besserer Befund als ein stiller Fix.

**Keine Reparatur ins Blaue.** Ursache benennen, dann beheben, dann Kriterium erneut fahren, in
allen drei Räumen.

---

## §2 · Freigaben aus Runde F

- **§3 Medaillons committen: freigegeben** (Medien-Strang auf `feat/council-rooms`, wie
  `22f2575`). Der Helligkeitsunterschied (Gemini 68,5 vs. 53,7 / 52,7) und die 2 % Größe
  **bleiben unangetastet** — richtig gemeldet, richtig nicht angeglichen. Ein Porträt mit
  belichtetem Gesicht *ist* heller als ein Objektrelief; das ist die Wahl des Modells, nicht ein
  Fehler.
- **§5 `docs`-Reorg: freigegeben**, aber **nach §1**. B und C nach `docs/archiv/`,
  `codex-serie-*` nach `asset-originals/`, A als Fleißarbeit mit Blick je Bild.
- **§1 Datenbranch-Entflechtung** bleibt offen bis dein Bericht zur Basis vorliegt — ist `master`
  Vorfahre oder divergiert er? Ohne diese Antwort kein Cherry-Pick-Entscheid.

---

## §3 · Zählmaschine — Bestellung läuft

Der Abbruch war richtig. Die Bestellung steht in
`docs/bestellung-zaehlmaschine-2026-07-27.md`: **P10** (Maschine mit Podest, freigestellt) und
**P11** (nur die Trommel, freigestellt — für den Zähl-Ruck).

P10 wird **deckungsgleich über die gemalte Maschine** gelegt und ersetzt sie optisch. Sitzt die
Silhouette nicht satt: berichten, nicht nachbearbeiten. §7 und §8 bleiben bis dahin liegen.

---

## §4 · Reihenfolge

1. **§1 Regression** — Ursache, Fix, Kriterium in allen drei Räumen.
2. §2 Medaillon-Commit.
3. §2 Datenbranch-Bericht.
4. §5 `docs`-Reorg.
5. Nach Eintreffen von P10/P11: §8, dann §7.

Guardrails unverändert.
