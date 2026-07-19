# Kimi-Korrektur 2 — Vorzimmer / Räume (Feinschliff)

## Rahmen (unverändert, strikt)
Kein Commit. Nur `site/` + `docs/`. Tabu-Pfade unberührt (`sessions/ journal/ schedule.json gremium/ schema/ prompts.py`). **No-JS-Vollfallback bleibt** (ganze Wahrheit ohne JS sichtbar, Test ehrlich nachziehen). A11y: genau ein wirksames `h1`, WCAG AA, volle Tastaturbedienung, `prefers-reduced-motion`, Tap-Ziele ≥ 44 px, sauberer Reflow bei 320 und 390 px ohne horizontalen Overflow. Spendenlinks ausschließlich aus der Registry. DE + EN parallel. Build warnungsfrei, Tests grün. Screenshots nach `docs/review/`. **Erst inspizieren + messen, dann umsetzen, dann verifizieren** — bei Unklarheit messen/melden, nicht raten.

---

## A — Ergebnisse auf die Tafel
- Das Antwort-Board (je Eintrag: **Emblem + Bereich + Organisation + „x von y" + Spendenlink**) wandert aus dem separaten Block **hinauf in die leere Tafelfläche der Study-Szene** — erster Screen.
- **Nur die Ergebnisse** auf die Tafel. **Keine Erklärtexte** dort (Untertitel „Je ein KI-Modell …", Mechanismus-Sätze o. Ä. bleiben außerhalb der Tafel). Die kurze Überschrift „Die Antwort dieser Sitzung" darf als Tafel-Titel bleiben.
- Tafelzone per Crop vermessen, Board exakt dort platzieren. Lesbarkeit sichern (heller Text auf dunkler Tafel; dezenter Scrim nur falls nötig).
  - **Desktop:** Tafel liegt oben links im Plate.
  - **Mobil:** Tafel liegt im oberen Bildbereich der Study-Hochformat-Plate (siehe C) — Board dort.
- Restliche Reihenfolge: Hero mit Ergebnissen → „So läuft es" (Prozess) → Dossiers → Türen.

## B — Hintergrund wirklich fixieren (alle Räume)
- Der bisherige „static"-Umbau reicht nicht: das Plate scrollt noch mit hoch. Nötig ist eine **feste Vollbild-Bildebene hinter dem scrollenden Inhalt**: `position:fixed`, `100svh`, `object-fit:cover`. **Nicht** `background-attachment:fixed` (iOS Safari ignoriert es). Inhalt scrollt über dem stehenden Bild.
- Die Seite-zu-Seite-View-Transition zwischen den Räumen bleibt unangetastet.

## C — Responsive Plates (eigene Hochformat-Bilder für Mobil)
- Die feste Bildebene lädt **quellenabhängig**: Querformat-Plate ≥ Desktop-Breakpoint, **Hochformat-Plate darunter**.
- Neue Mobile-Plates liegen in `docs/`. Pro Bild: Original byteidentisch ins Originalarchiv, Derivat nach `site/static/media/…` über die bestehende Pipeline, Original + Maße + SHA-256 in `ASSETS.md`.
  - **Study (final):** `docs/ChatGPT Image 18. Juli 2026, 20_35_45 (1).png` — leere Tafel oben (= Board-Fläche), Protagonist, dunkle Textzonen.
  - **Archiv (final):** `docs/ChatGPT Image 18. Juli 2026, 20_35_46 (3).png` — Prunkschrank rechts, dunkle Textspalte links.
  - **Ratssaal:** Neuversion noch nicht final → **Platzhalter.** Vorerst kein eigenes Hochformat-Bild einbinden; Slot so bauen, dass später **nur die Datei getauscht** wird.

## D — Embleme größer
- Antwort-Board- und Prozess-Embleme sind im Verhältnis zum Text zu klein; die feinen Gravuren und Farben gehen verloren. **Deutlich vergrößern** (Richtwert ~2× der aktuellen Größe), final visuell prüfen (Desktop + Mobil). Kreis-Crop und Messingring beibehalten, Layout nicht sprengen.

## E — Selbst-Link fixen
- Im Prozess-Streifen ist nur „Die Antwort" verlinkt und zeigt **auf sich selbst**. Ziel: Sprung **hoch zum Antwort-Board** (jetzt in der Tafel). Falls die anderen Stufen sinnvoll auf ihren Abschnitt/ihr Dossier verlinkbar sind, konsistent machen; sonst „Die Antwort" korrekt ankern und tote/Self-Links entfernen.

## F — Prozessschritte: erst erklären, dann ggf. alle sechs
- **Frage an dich (Kimi), im Report beantworten:** Warum hast du den Prozess auf vier Stufen reduziert und die Embleme `process-question` (Frage) und `process-reconsider` (Umdenken) aus dem Deploy genommen?
- **War es nur eine UI-/Platz-Entscheidung:** stelle **alle sechs kanonischen Schritte** dar —
  **Frage → Belege → Drei Antworten → Umdenken → Zählen → Veröffentlichen** —
  mit den sechs vorhandenen Emblemen (`process-question, process-evidence, process-three-answers, process-reconsider, process-count, process-publish`). Gerichtete Bernstein-Pfeile; Desktop horizontal, Mobil als 3×2-Matrix (gemäß Integrationsplan). `process-question` und `process-reconsider` wieder einbinden (Derivate zurück in den Deploy, `ASSETS.md` nachziehen).
- **Gab es einen inhaltlichen Grund** (z. B. die Rollennamen Späher/Wart/Rat waren bewusst gewählt): kurz melden **mit Vorschlag, bevor** du umbaust — dann entscheiden wir gemeinsam.
- Ziel unverändert: **gerichteter Ablauf** mit sichtbarer Reihenfolge und Richtung, je Schritt Emblem + **ein** Satz Klartext, keine Listen, keine Amtssprache.

---

## Deliverables
- **Screenshots** (Desktop + Mobil, DE + EN) unter `docs/review/`: Ergebnisse auf der Tafel; fixierter Hintergrund über 2–3 Scrollstände (Bild steht, Inhalt zieht durch); größere Embleme; Prozess-Streifen im Endstand; funktionierende Links.
- **Kurzreport:** Antwort auf die Prozess-Frage (F), was gemessen/geändert wurde, Testzahl, Auffälligkeiten. **Kein Commit.**
- **Offene Punkte** explizit melden statt raten.
