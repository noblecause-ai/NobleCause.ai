# Auftrag an CC — Aufräumen nach dem Lauf, und die Türmitte

**Von:** Opus 5 (Architekt) · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Anlass:** Der Cron ist heute Morgen gelaufen, während mehreres noch nicht gemerged war. Der
Wart hat seinen Teil bereits entschieden; hier steht der Rest, geordnet.
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

---

## §1 · Der Journal-Eintrag von heute (Wart-Vorgabe, wörtlich zu befolgen)

Der Lauf vom **2026-07-27** hat mutmaßlich einen Journal-Eintrag geschrieben, **bevor** der
Backend-Branch mit dem `model_label`-Schreiben gemerged war.

**Wart-Entscheid:** Der Eintrag fällt unter den **Backfill** und wandert mit in den Datenbranch —
gleiche Regel wie die Bestandseinträge: **`model` gesetzt → Label nachziehen.** Kein neuer
Vorgang, nur ein Eintrag mehr auf der bestehenden Liste.

- Über den **Datenbranch** + `git merge --ff-only`. **Nie `--no-verify`.**
- **Zuerst prüfen und berichten**, ob der Eintrag überhaupt existiert und was er enthält
  (`model`, `convene`, `convene_rationale`, `deputation_note`, `findings`). „Mutmaßlich" ist
  Wart-Sprache für „bitte nachsehen".
- Wenn der Lauf **etwas anderes** als erwartet hinterlassen hat — fehlender Eintrag, Abbruch,
  Teilschreibung — **nicht reparieren, sondern berichten.** Das berührt den Rekord und geht dann
  über die Noble-Session an den Wart zurück.

---

## §2 · Die Türmitte — vermutlich in allen drei Räumen falsch

Steward-Befund: Die Council-Tür öffnet nicht mittig, sondern nach rechts versetzt.

**Verdacht:** `perspective-origin` steht als **feste Prozentzahl des Viewports**, die Aperturmitte
wandert aber mit dem **Cover-Crop**. Weicht das Seitenverhältnis vom Messfall ab, zielt die Kamera
neben die Tür. Im Council fällt es am stärksten auf — dort klaffen zwischen gemessener
Hotspot-Mitte (50,7 % / 42,1 %) und gesetztem Origin (50,5 % / 48 %) schon im Messfall sechs
Punkte in y.

**Auftrag:** `perspective-origin` **zur Laufzeit aus derselben Cover-Rechnung ableiten**, aus der
auch der Türhotspot seine Position bekommt. Eine Quelle, kein zweiter Satz gepflegter Konstanten —
dieselbe Begründung wie beim Ruhe-Stapel.

**Abnahme:** In allen drei Räumen bei 16:9, 21:9 und einem hohen schmalen Fenster liegt die
Fahrtachse auf der Türmitte. Abweichung in Prozentpunkten je Raum und Fall im Bericht.

---

## §3 · Der Medien-Strang

Er steht seit Runde A auf „blockiert Go-Live: JA" und ist inzwischen deutlich gewachsen (Serie 5,
Auf-Plates, Wand-Löcher, Flügel, Kleinauflösungen). **Jetzt bündeln und committen.**

Vorher **eine Zeile je Datei**: wird sie referenziert, von wo? Was nicht referenziert wird, kommt
nicht mit — es sind Zwischenstände, und ein Medien-Commit ist der letzte Ort, an dem man sie noch
billig los wird. Insbesondere `register.avif` (aus §2 der Runde B ausgebaut) und alles, was der
`jpg → avif`-Migration entstammt und keinen Verweis mehr hat.

**Abnahme:** ein sauberer Checkout von HEAD rendert alle drei Räume vollständig — das war der
ganze Zweck des Strangs.

---

## §4 · `docs/` aufräumen

Der Ordner trägt inzwischen über hundert untracked Dateien: Bild-Originale mit
Generator-Dateinamen, `--SKIP`-Entwürfe, Aufträge und Berichte aus zwei Wochen, Review-Ordner.
Der Steward hat das früh als „müssen wir ohnehin aufräumen" angemeldet.

**Vorschlag zur Freigabe — kein Bau ohne Bestätigung:**

- `ChatGPT Image *.png` und die `P*`-Positionen nach `docs/asset-originals/` in die bestehende
  Provenienz-Struktur, benannt nach Serie und Position statt nach Generatorzeit.
- `--SKIP`-Dokumente und überholte Kontextdokumente nach `docs/archiv/`, mit einer Zeile im
  Kopf, warum sie überholt sind. **Nicht löschen** — sie erklären, warum Dinge so sind.
- Aufträge und Berichte bleiben, wo sie sind; sie sind der Verlauf.
- Erst danach entscheiden, was von `docs/` überhaupt getrackt wird.

**Bitte zuerst eine Liste vorlegen**, keine Verschiebung. Und daran denken: auf dieser Maschine
kann ich nichts löschen — was weg soll, macht der Steward selbst.

---

## §5 · Reihenfolge und was liegen bleibt

1. §1 Journal-Backfill — **zuerst**, weil es den Rekord berührt.
2. §2 Türmitte, alle drei Räume.
3. §8 Zählmaschine (Weg 1), falls noch nicht gesetzt.
4. §3 Medien-Strang.
5. §4 `docs/` — Liste vorlegen.

**Liegt bewusst:** §7 Medaillons (wartet auf die Bestellungen der Modelle, Verfahren steht in
`docs/opus5-2026-07-27-bestellverfahren-selbstdarstellung.md`), das Vordergrund-Cutout der
Zählmaschine (Freischnitt zuerst versuchen), der **Protokoll-Explorer inkl. 2b**.

---

## §6 · Guardrails (unverändert)

Guard-Hook auf `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`, `schema/**`,
`prompts.py`; Daten nur über Datenbranch + `--ff-only`; **nie `--no-verify`**; kein Push.
§0-Verfassung. Versiegelte Datennaht. Geometrie am gerenderten AVIF messen.
