# Abnahme der Maschinen-Härtung — NobleCause.ai

**Dies ist deine vollständige Aufgabenbeschreibung.** Du brauchst keine weiteren
Anweisungen; alles Nötige steht hier oder in den unten genannten Dokumenten.

*(Diese Datei ist untracked und gehört nicht in einen Commit — du committest ohnehin
nichts, siehe Grenzen.)*

---

## Ausgangslage

Du hast am 1. August diesen Stand geprüft und Befunde gemeldet. Sie wurden behoben.
**Dies ist keine neue Review, sondern eine Abnahme:** Prüfe, ob die Behebung tut, was sie
soll — nicht, ob dir sonst noch etwas auffällt.

**Was abgenommen wird:** 11 Commits über `origin/master` (`59461f1`).

| | |
|---|---|
| **Dein Worktree** | `/Users/afschinmirhamed/Projects/nc-abnahme-kimi` |
| **Commit** | `599998dd6e3f334e673066634b4f2d608c1c1d8b` (detached) |
| **Tests** | `gremium/.venv/bin/python -m pytest gremium/tests/` → 43/43 grün |
| **Port** (optional, für `npm run preview`) | 4220 |

Der Kern der Abnahme ist Code — `gremium/**`, `schema/**`, `.github/workflows/**` — plus
die Testsuite. Die Website ist **nicht** Gegenstand.

---

## Der Maßstab

Nicht deine Befunde, sondern die Entscheide der Rekord-Instanz. **Lies zuerst:**

- `docs/wart-entscheid-vertragsbruch-maschine-2026-08-01.md` — die Grundsatzregel
- dessen Nachträge zur Sortierung, zur Zählweise („2 von 3 · 1 ohne auswertbares Votum")
  und zu `conditional`
- `docs/opus5-auftrag-2026-08-01-maschine-haerten.md` — die Umsetzungsvorgabe
- `docs/wart-freigabe-korrekturhinweis-sortierfehler-2026-08-01.md` — der Wortlaut der
  Korrekturhinweise

Die Grundsatzregel in einem Satz: *Publiziert wird, was gültig ist; markiert wird, was
fehlt; abgebrochen wird nur, wenn der Rekord selbst nicht wohlgeformt herstellbar ist.
Nicht der unvollständige Rekord ist der Bruch — der unmarkiert unvollständige ist es.*

---

## Die eine Frage, die über allem steht

Am **6. August, 12:00 UTC** läuft Sitzung 4 automatisch durch diese Maschine — der erste
Produktivlauf.

> **Läuft sie durch? Und wenn sie abbricht: aus dem richtigen Grund?**

Eine Härtung, die zu streng ist, verhindert jede Sitzung. Eine, die zu lasch ist, lässt
genau die Fehler durch, die du gemeldet hast. **Such nach beidem.**

Der wahrscheinlichste Bruchpunkt ist die neue `conditional`-Pflicht: Liefert ein Modell das
Feld an anderer Stelle oder in anderer Form, als der Parser erwartet, sind nach dem
Entscheid **alle** Voten ungültig — und es gäbe keine Sitzung 4.

---

## Im Einzelnen, gegen die Entscheide

1. **Sortierung und Gate.** Ist die Auswahl der jüngsten Sitzung jetzt deterministisch,
   unabhängig von der Dateisystem-Reihenfolge? Greift das Gate auch bei künftigen Ursachen
   derselben Wirkung?
2. **`convene`.** Ausschließlich JSON-`true`/`false`, kein Fallback auf „nicht einberufen"?
   Entsteht bei Verletzung wirklich **kein** Journal-Eintrag?
3. **Schema-Tore.** Greifen sie vor dem Commit oder danach? Validieren alle Bestandsdaten
   dagegen — Sitzungen wie Journal-Einträge, inklusive Bootstrap und Kommission?
4. **Vier Bereiche, Zähler, Gleichstand.** Trägt die Sitzung wirklich immer vier Bereiche?
   Ist `has_consensus` bei Gleichstand `false`? Zählt der Zählstand nach dem Muster
   „2 von 3 · 1 ohne auswertbares Votum", also **ohne den Ausfall wegzurechnen**?
5. **`conditional`.** Ist die Regex ersatzlos weg, auch in Nebenpfaden? Fordert der Prompt
   das Feld eindeutig genug an?
6. **Die Tests.** Prüfen sie, was sie behaupten? Ein Test, der grün ist, weil er die falsche
   Sache misst, ist schlimmer als keiner.
7. **Die Korrekturhinweise.** Steht der Wart-Wortlaut unverändert in beiden Einträgen
   (`journal/2026-07-20`, `journal/2026-07-27`), DE und EN?

---

## Nicht Gegenstand

Frontend, Website, Deploy — und alles, was du beim ersten Mal als `punktversion` oder
`geschmack` gemeldet hast. Das ist gesichtet und wird separat abgearbeitet.

---

## Rückmeldung

Knapp: je Punkt **„trägt"** oder **„trägt nicht"** mit einer Begründung. Am Schluss ein Satz
zur Kernfrage oben. **Kein Fließtext-Bericht.**

**Was du nicht prüfen konntest, sag es** — beim letzten Mal war das der wertvollste Teil
deines Berichts.

Ablage: `docs/review/abnahme-2026-08-02-kimi.md` in deinem Worktree.

---

## Grenzen

- Nichts ändern, nichts committen, kein Branch, kein Push.
- **Nichts ausführen, was Geld kostet oder Rekord schreibt:** `run_session.py`,
  `run_wart.py`, `run_commission.py`, `probe_conditional.py` und die Workflows. `pytest` und
  statische Analyse ja.
- Nur in diesem Worktree arbeiten.
- Ein zweites Modell nimmt parallel denselben Stand ab. Ihr seht die Berichte des anderen
  nicht und sollt nicht danach fragen.

## Zeit

Der Stand muss am **4. August, 12:00 UTC** öffentlich sein, sonst wird Sitzung 4 ausgesetzt.
**Knapp und schnell ist besser als vollständig und spät.**
