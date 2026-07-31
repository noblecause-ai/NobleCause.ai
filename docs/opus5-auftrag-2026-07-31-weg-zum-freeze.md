# Auftrag an CC — der Weg bis Freeze und Review

**Von:** Opus 5 (Architekt), 31. Juli 2026
**Umfang:** alles zwischen dem Routen-Commit und dem eingefrorenen Review-Stand.
**Nicht enthalten:** die Review-Runde selbst, Merge nach `master`, Push.

Fünf Blöcke, in dieser Reihenfolge. Nach jedem Block ein kurzer Bericht — aber nicht auf
Freigabe warten, außer wo es ausdrücklich steht.

---

## 0 · Der Routen-Commit ist freigegeben

Verifiziert: `sitzungen/` vorhanden, `sessions/` weg, Rekord unberührt. Committen.
Die drei verbliebenen `/sessions`-Treffer sind korrekt — das Datenverzeichnis behält seinen
Namen, die GitHub-Links müssen darauf zeigen.

---

## 1 · Der Guard-Hook bestimmt, wo integriert wird

Nachgesehen: Der Hook ist **kein** globaler Schutz. Er greift ausschließlich auf
`feat/immersive-homepage*` und `feat/council-rooms*`, sonst `exit 0`.

**Folge: `master` kann nicht in `feat/council-rooms` gemergt werden.** Der Merge-Commit
trüge `journal/`, `sessions/`, `gremium/` und `schema/` im Index — der Hook blockt, und
`--no-verify` ist ausgeschlossen.

**Deshalb: ein Integrationsbranch außerhalb des `feat/`-Musters.** Vorschlag
`integration/go-live-0.4`. Dort ist der Hook no-op, dort dürfen Rekord und Frontend
zusammenkommen, und `master` bleibt unberührt, bis alles geprüft ist. **Der Freeze und die
Review laufen auf diesem Branch** — er ist der Stand, der live geht.

Der Guard bleibt unverändert. Er hat seinen Zweck erfüllt: die Trennung hat gehalten,
bis sie bewusst aufgehoben wird.

---

## 2 · Den offenen Strang aufräumen — vor der Integration

Ein Review auf einem dirty Arbeitsbaum ist kein Review. Jeder Posten einzeln, mit
Entscheidung im Bericht:

- **`docs/go-live.md`** (modifiziert) — deine Hash-Aktualisierung. Committen.
- **`AGENTS.md`** (modifiziert) — **berichten, was geändert wurde, bevor du committest.**
  Die Datei trägt die Präsentationsregel, auf die sich der Guard beruft. Änderungen daran
  sind keine Bauarbeit.
- **22 gelöschte `.jpg` unter `site/static/media/**`** — der Medien-Strang (Übergabe 28.07.
  §7 Punkt 5). Prüfe, dass für jede gelöschte `.jpg` eine `.avif` existiert und im Code
  referenziert wird, dann die Löschungen committen. **Wo eine `.avif` fehlt, stopp.**
- **57 Zeitstempel-Bilder untracked in `docs/`** — laut Übergabe bewusst nach Go-Live
  verschoben. Sie blockieren aber den sauberen Baum. Vorschlag: nach `docs/asset-originals/`
  oder in eine `.gitignore`-Regel, **ohne sie zu löschen**. Deine Wahl, im Bericht nennen.
- **`gremium/prompts.py`** (modifiziert) und **`commissions/`** (untracked) — beide liegen
  bereits committet auf `master`. **Prüfe, ob die Arbeitsbaum-Fassungen inhaltsgleich sind.**
  Wenn ja: verwerfen, der Merge bringt sie. Wenn nein: **stopp und melden** — dann liegt
  hier eine Änderung, die nirgends committet ist.

Ziel: `git status` zeigt nichts außer bewusst Ignoriertem.

---

## 3 · Integration und voller Build — der erste Test mit allem

1. `integration/go-live-0.4` von `feat/council-rooms` abzweigen.
2. `master` hineinmergen. Erwartete Konflikte: keine — `feat` hat den Rekord nie angefasst,
   seit er auf `master` versöhnt wurde. **Falls doch, insbesondere bei `schedule.json`:
   immer die `master`-Fassung, und danach `git show HEAD:schedule.json` prüfen —
   `last_journal` muss `/journal/2026-07-27/` sein.** Steht dort etwas Älteres, abbrechen.
3. **Voller Build.** Das ist der erste Build, der Frontend *und* Rekord zusammen sieht —
   der Prerender-404 aus der Go-Live-Vorbedingung muss hier verschwinden, weil feats
   `{#if e.session_ref}`-Guard jetzt bei den Daten ist.
4. Alle Routen durchgehen, DE und EN, plus `/sitzungen/2026-07-27b/`… bzw. der
   Journal-Eintrag der Kommission. **Der Kommissionseintrag ist der Grund für die
   Vorbedingung — er muss sichtbar rendern.**

**Bericht und Stopp.** Wenn dieser Build sauber durchläuft, ist die Go-Live-Vorbedingung
aus `docs/go-live.md` erfüllt und kann dort abgehakt werden.

---

## 4 · Abschluss-Durchgang — auf dem Integrationsstand

Alles auf dem gemergten Stand, nicht auf `feat`. Verifikations-Vorstufe vorweg.

**Die Räume:**
- Jede Türfahrt in beide Richtungen, Study ↔ Council ↔ Archiv.
- Zurück und erneute Fahrt **ohne Neuladen** — der Fall, an dem die Rückwärts-Stabilität
  schon einmal hing.
- 390 px, `prefers-reduced-motion: reduce`, ohne JS.
- Der Protokoll-Eingang am Pult in allen Zuständen: Ruhe (jetzt sichtbar), Hover, Fokus,
  Touch, ohne JS.

**Die zwei aufgelaufenen Auflagen — beide sind derselbe Prüfschritt:**
Fixe Bühnenelemente, die den Fluss überlagern, werden **über den gesamten Scrollweg**
geprüft, nicht nur im Ruhebild.

- **Pult (`z-index: 4`, Archiv):** bei 1280 und 1440 die ganze Seite durchscrollen. Kein
  Scrollstand verdeckt Rekordtext. Wenn doch: früherer `--retreat`, **nicht** höherer
  z-index für den Fluss.
- **Scout (Study):** die gemessenen 30/37/33 % Text-über-Figur im echten Browser ansehen —
  liest es sich unruhig oder ruhig? Das ist eine Wahrnehmungsfrage, keine Zahl. Screenshot
  bei 1280 am Spitzenwert (`scrollY ≈ 410–585`), damit der Steward es beurteilen kann.

**§8 Zähl-Ruck:** Der Steward muss ihn abnehmen. Bereite es vor — sag ihm, **auf welcher
Seite, an welcher Stelle und bei welchem Scrollstand** er hinsehen muss. Abnahmekriterium:
die **Kanten** der Trommel bewegen sich nicht, nur ihre Oberfläche.

---

## 5 · Freeze und Review-Paket

Erst wenn 2–4 durch sind.

1. Arbeitsbaum sauber, annotiertes Tag auf `integration/go-live-0.4`:
   `git tag -a review-2026-08-XX -m "Stand für UI- und Code-Review"`
2. Reproduzierbarer Build wörtlich dokumentieren — **inklusive der Node-Version, mit der du
   gebaut hast.** `rolldown` bringt native Bindings mit; ein Versionssprung bricht den Build
   beim Reviewer.
3. Referenz-Screenshots aus **deinem** Build: Study, Council, Archiv, Explorer, je 1440 und
   390, plus Ruhe und Hover für Türen, Medaillons, 2b, Pult-Eingang und die 2×2-Tafel.
   Zweck: „bei mir sieht das anders aus" von einem echten Finding unterscheidbar machen.
4. `docs/opus5-2026-07-29-review-vorbereitung.md` finalisieren — Tag, Commit-Hash,
   Build-Befehle, Screenshot-Pfade eintragen. **Die Liste „bekannt, bitte nicht melden"
   auf den heutigen Stand bringen:** Tafel und Routen sind erledigt und gehören dort
   gestrichen; erster Frame/LCP, Explorer-Anbindung und der durchscheinende Szenentext bei
   2b bleiben drauf.

**Bericht und Stopp.** Die Reviewer werden vom Steward beauftragt, nicht von dir.

---

## Grenzen

- **Kein Push**, nichts, auch nicht der Integrationsbranch.
- **Kein Merge nach `master`** — das ist der Schritt nach der Review.
- **Keine Änderung am Guard-Hook**, an `wart.yml`, `session.yml` oder `gremium/**` über das
  in §2 Genannte hinaus.
- Bei jedem „stopp und melden" wirklich anhalten. Vier der letzten fünf echten Funde kamen
  aus einem Stopp, nicht aus einem Durchmarsch.
