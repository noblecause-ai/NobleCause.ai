# Auftrag an CC — Ausführung des Wart-Entscheids (Rekordlinien)

**Von:** Opus 5 (Architekt), 30. Juli 2026
**Grundlage:** `docs/wart-entscheid-rekordlinien-2026-07-30.md` (bindend) ·
`docs/review/rekord-inventar-2026-07-29.md` (Diagnose)
**Umfang:** Punkte 1–6 der Wart-Ausführungsliste. **Punkt 7 ist nicht Teil dieses Auftrags**
— siehe §5.

Der Wart-Entscheid ist bindend. Dieser Auftrag ergänzt ihn um eine Sicherung, zwei
Korrekturen und die Abnahme. **Wo dieser Text dem Entscheid widerspricht, gilt der
Entscheid** — außer bei §1 (Sicherung) und §3 (Faktenkorrektur), beides vom Steward
freigegeben.

---

## 0 · Warum hier besonders vorsichtig gearbeitet wird

**Der lokale Rekord-Stamm existiert nirgendwo sonst.** `origin` kennt weder `5071194` noch
`feat/council-rooms` — nichts davon ist gepusst. Dazu liegen Teile des Stamms als
**uncommittete Arbeitsbaum-Änderungen** vor (`gremium/prompts.py` modifiziert). Ein
fehlgeschlagener Branch-Umbau ist hier nicht „ärgerlich", sondern potenziell endgültig.

Deshalb: **§1 vollständig, bevor irgendein Branch angefasst wird.** Kein Schritt aus §2
beginnt, bevor §1 bestätigt ist.

---

## 1 · Schritt 0 — Sicherung (Pflicht, zuerst)

1. `git fetch origin` — und **jede** spätere Aussage über einen Remote-Stand nur nach einem
   `fetch` in derselben Befehlskette. (Der Architekt hat hier einen neun Tage alten
   remote-tracking ref als Tatsache genommen; daraus entstand ein falscher Alarm.)
2. Sicherungstags auf alle drei Stände, mit Datum im Namen:
   ```
   git tag -a backup/master-2026-07-30       -m "Sicherung vor Rekordlinien-Umbau" master
   git tag -a backup/feat-2026-07-30         -m "Sicherung vor Rekordlinien-Umbau" feat/council-rooms
   git tag -a backup/origin-master-2026-07-30 -m "Sicherung vor Rekordlinien-Umbau" origin/master
   ```
3. **Die uncommitteten Änderungen als Patch sichern** — sie überleben kein `reset`:
   ```
   git diff > ../nc-backup-2026-07-30-unstaged.patch
   git diff --staged > ../nc-backup-2026-07-30-staged.patch
   git status --porcelain > ../nc-backup-2026-07-30-status.txt
   ```
4. **Ein vollständiges Bundle außerhalb des Repos:**
   ```
   git bundle create ../nc-backup-2026-07-30.bundle --all
   ```
   Das ist die einzige Kopie, die einen kaputten `.git`-Ordner überlebt.
5. **Untracked prüfen, nicht raten:** `git status --porcelain | grep '^??'` — für jeden
   Treffer feststellen, ob er in einem Commit auf `master` oder `feat` enthalten ist. Was in
   **keinem** Commit steckt, zusätzlich als Dateikopie sichern. Erwartet betroffen:
   `gremium/run_commission.py`, `journal/2026-07-27/` (beide liegen auf `master`, erscheinen
   aber im auf `feat` ausgecheckten Baum als untracked — das ist harmlos, aber
   nachzuweisen, nicht anzunehmen).

**Berichten, bevor es weitergeht:** Tags gesetzt, Bundle-Größe, Patch-Zeilen, Ergebnis der
Untracked-Prüfung.

---

## 2 · Die Ausführung (Wart-Entscheid, Punkte 1–6)

Branchname: `data/rekordlinien-2026-07-30` — dem Muster der bestehenden Datenbranches
folgend (`data/commission-selbstdarstellung`, `data/pull-master-0720`).

1. **Datenbranch von `origin/master` abzweigen.** Nicht vom lokalen `master`. Das ist der
   Kern des Entscheids: der Cron-Rekord und die aktuelle `schedule.json` sind Basis und
   können so nicht rückwärts überschrieben werden.
2. **Kommission umbenennen:** `journal/2026-07-27/` (Kommissionsfassung, vom lokalen
   `master`) → `journal/2026-07-27b/`. `commissions/2026-07-27/` **bleibt unverändert** —
   eigener Namensraum. `commission_ref` zeigt weiterhin dorthin.
   **Verweise nachführen und vorher suchen, nicht vermuten:**
   ```
   grep -rn "2026-07-27" --include=*.json --include=*.js --include=*.svelte --include=*.py . \
     | grep -v node_modules
   ```
   Jeden Treffer einzeln bewerten: zeigt er auf den Wart-Research (bleibt) oder auf die
   Kommission (wird `2026-07-27b`)? **Die Trefferliste mit Bewertung in den Bericht.**
3. **Rekord-Stamm aufbringen:** `schema/**` · angereicherte `sessions/**` (Klartext,
   `plain_en`, `model_label`, DE-Ergänzungssatz S3-B) · `journal/2026-07-24/` ·
   `journal/2026-07-27b/` · `gremium/run_commission.py`.
   Inhaltlich aufbringen, **nicht** den lokalen `master` mergen — sonst kommt die alte
   `schedule.json` mit.
4. **Backfill:** `journal/2026-07-27/` (Wart-Research) erhält
   `"model_label": "Claude Fable 5 (Anthropic)"`. Ein Eintrag auf der bestehenden
   Backfill-Liste, kein neuer Vorgang.
5. **`schedule.json` nicht anfassen.** Die O-Fassung bleibt wörtlich stehen
   (`next_research 2026-08-03`, `next_session 2026-08-06`,
   `last_journal /journal/2026-07-27/`). Wenn ein Schritt sie ändern will, ist der Schritt
   falsch — nicht die Datei.
6. **Diff-Bericht `gremium/**` an den Wart** — ein Bericht, drei Diffs, keine Merges vorab:
   `prompts.py` (O↔M) · `run_session.py` (O↔F) · `reaggregate.py` (O↔F).
   Bis zum Wart-Entscheid gilt für alle drei der O-Stand. Bei `run_session.py` ausdrücklich
   die Frage beantworten, ob die 27 Zeilen der gestrichene `led_by.model_label`-Strang sind
   — der Wart hat den Verdacht benannt, der Bericht muss ihn bestätigen oder ausräumen.

---

## 3 · Korrektur zum Entscheid: `schedule.json` ist auf `feat` **getrackt**

Der Entscheid schreibt in §2, die Datei bleibe auf `feat/*` untracked „(Stand seit
`72c78d5`)". **Das trifft nicht zu** — dein eigenes Inventar hat es korrigiert: `72c78d5`
untrackte `site/static/schedule.json` (die vom `prebuild` kopierte Fassung), nicht die
Wurzeldatei. Der Irrtum stammt aus dem Architekten-Auftragstext, nicht vom Wart.

**Folge:** Die Kanon-Regel („gehört ausschließlich dem Mechanismus") greift nicht von
selbst. Damit sie wirkt, muss die Wurzeldatei auf `feat/*` untracked werden.

**Aber nicht jetzt und nicht auf `feat`.** `schedule.json` ist dort Guard-Tabupfad — ein
`git rm --cached` samt Commit würde vom pre-commit-Hook blockiert, und `--no-verify` ist
ausgeschlossen. Deshalb:

- **In diesem Auftrag nur dokumentieren**, nicht ausführen.
- Die Untrackung wird Teil von Punkt 7 (Merge), zusammen mit der ohnehin nötigen
  Konfliktauflösung zugunsten der O-Fassung.
- Beim späteren Merge `feat` → Stamm gilt: **`schedule.json` immer O-Fassung**, unabhängig
  davon, was Git vorschlägt. Nach dem Merge `git show HEAD:schedule.json` prüfen —
  `last_journal` muss `/journal/2026-07-27/` sein. Steht dort `/journal/2026-07-20/` oder
  `/journal/2026-07-08c/`, ist der Rekord rückwärts gelaufen: **abbrechen, nicht
  nachbessern.**

---

## 4 · Korrektur zum Entscheid: was aus dem lokalen `master` wird

Der Entscheid sagt es nicht, und ungesagt bleibt es eine zweite Wahrheit auf der Platte:
Nach diesem Umbau ist der lokale `master` **überholt**. Sein Inhalt ist in §2.3 neu
aufgebracht, sein Commit `5071194` wird nicht gemergt.

**Erst wenn §6 vollständig abgenommen ist**, wird er auf den neuen Stand gezogen. Nicht
vorher, nicht „nebenbei". Der Sicherungstag aus §1.2 bleibt in jedem Fall stehen — auch
nach dem Zurücksetzen, auch nach dem Push. Er wird nicht gelöscht.

---

## 5 · Was dieser Auftrag ausdrücklich nicht umfasst

- **Punkt 7 der Wart-Liste** (Zusammenführung mit `feat/council-rooms` und Push). Das ist
  derselbe Schritt wie Punkt 8 im Gesamtplan und wartet auf: linke Ergebnis-Tafel, Routen,
  Abschluss-Durchgang, offenen Strang, Review-Runde durch Kimi 3 und Codex.
  **Punkte 1–6 sind reine Rekord-Arbeit und laufen unabhängig davon.**
- **Kein Push.** Nichts, gar nichts, auch nicht der Datenbranch.
- **Kein Merge** von `feat/council-rooms` in irgendetwas.
- **Keine Änderung** an `gremium/prompts.py`, `run_session.py`, `reaggregate.py`,
  `wart.yml`, `session.yml` — nur Diffs berichten.
- **Der offene Strang bleibt liegen:** `AGENTS.md`, die gelöschten `.jpg` des
  Medien-Strangs. Nicht mitcommitten, nicht wiederherstellen.

---

## 6 · Abnahme

Jeder Punkt einzeln mit Beleg:

1. **Nichts verloren.** Auf dem Datenbranch stehen: Wart-Research `2026-07-27` **mit**
   `raw/` und `actions_run_url` · Kommission als `2026-07-27b` · `journal/2026-07-24` ·
   angereicherte `sessions/**` · `schema/**` · `run_commission.py`.
   Nachweis: Dateiliste je Pfad plus Zeilenzahlen der Sessions gegen das Inventar.
2. **`schedule.json` unverändert:** `git diff origin/master -- schedule.json` ist leer.
3. **Keine tote Referenz:** die `grep`-Trefferliste aus §2.2, jeder Treffer bewertet und
   nachgeführt. Kein Verweis zeigt auf eine ID, die es nicht gibt.
4. **Backfill sitzt:** `model_label` in `journal/2026-07-27/entry.json`.
5. **Site baut und zeigt es richtig:** frischer Build (`rm -rf site/build site/.svelte-kit
   && npm run build`), Journal-Seite listet Wart-Research **und** Kommission als zwei
   getrennte Einträge, beide mit korrektem Datum und Typ. Ratssaal zeigt weiterhin den
   6. August. Screenshot der Journal-Seite.
6. **`origin/master` unberührt:** `git log --oneline -1 origin/master` = `972a9ba`.
7. **Sicherungen stehen:** die drei Tags und das Bundle sind vorhanden und lesbar
   (`git bundle verify`).

**Committen und Zurücksetzen des lokalen `master` erst auf ausdrückliche Freigabe des
Stewards, nach dem Bericht.**
