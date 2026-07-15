# Design-Nachbesserung (nach Abnahme PR #13)

Umsetzung der Gestaltungs-Befunde. **Nur Darstellung** — publizierter Sitzungstext
(`session.json`) unverändert (verifiziert: `git diff` zeigt keine `sessions/`-Änderung).
Änderungen ausschließlich in `sol-build/build.py` + `styles.css`.

| Fund | Vorher | Nachher |
|---|---|---|
| **P1a Hero** | `<h1>`+Intro füllten eine volle Bildschirmhöhe (`min-height:100svh` + ~9rem Top-Padding); LEEP + Spendenknopf unter der Falz | Intro gestrafft (kleineres `<h1>`, kompaktere Zeilen, Top-Padding gekappt); **LEEP-Karte + „Hier direkt spenden" oberhalb der Falz** (Desktop-Screenshot belegt) |
| **P1b Rohtext** | `dissent_md` (6941 Z.) verbatim gedumpt: rohe `**`, ganze ` ```json `-Blöcke über mehrere Bildschirme | `md_min()`-Renderer (escape-first, faithful): Dissens **hinter `<details>`** (eingeklappt), Markdown gerendert, **JSON-Blöcke eingeklappt**. Wortlaut byte-exakt (nur umschlossen) |
| **P1c Revision/Höhe** | Revision je Modell **doppelt** gestapelt; Karte A ~2× so hoch | Revision **einmal**, Modelle zusammengefasst („GPT & Gemini Pro: TaRL Africa → HKI"); **Karten gleich hoch**, Spenden-CTAs auf einer Grundlinie; fokussierte Karte D führt via Messing-Rahmen |
| **P2 Kreide** | Protokoll nannte neue Org **doppelt** (`<ins>` + `<h4>`); Durchstreichung blass | `<ins>`-Doppelung entfernt (Org **einmal** als `<h4>`); Kreide-Strike größer/kräftiger (2,5px, opak), weiter handschriftlich lesbar |
| **P3 Hotspots** | Ringe subtil, kein Hover/Fokus | sichtbare `:hover` **und** `:focus-visible`-Affordanz (Ring heller/größer, Outline); `prefers-reduced-motion`: kein Skaliersprung, Affordanz über Glühen/Farbe |

## MUSS — Nicht-Konsens gegengeprüft
`build.py --session 2026-07` (Sitzung 1, Säule A ohne Konsens) gerendert:
**„Keine Einigung" → „Alle Antworten bleiben nebeneinander stehen"** mit drei
gleichwertigen Voten (Claude Sonnet/HKI, Gemini/IGN, GPT/Evidence Action), je mit
Modell-Attribution, faktischer Beschreibung und **eigenem Spendenlink** — **kein
Fehlerfall-Look**. (Screenshot im PR. Committet wird weiterhin die jüngste Sitzung als
`index.html`; `--session <id>` rendert jede Sitzung.)

## Ehrliche Grenze
Der Desktop-Falz ist per Screenshot belegt (Spendenknopf bei ~550 px im 784-px-Viewport).
Ein **eigener Mobil-Render** war in dieser Umgebung nicht erzeugbar (Fenster reflowt nicht
unter die Mindestbreite); die Mobil-Falz stützt sich auf das kompakte Mobil-CSS
(`@media max-width:760px`, reduziertes Hero-Padding) + das gestraffte Intro — vor der
finalen Freigabe auf einem echten Gerät gegenprüfen.

## Verifikation
`build.py` grün; `pytest` 13 grün (3 build + 10 golden); `git diff` nur `sol-build/`,
keine `sessions/`-Textänderung. Screenshots (Hero-Falz, Karten gleich hoch, Nicht-Konsens)
im PR. **Kein Merge** — geht zur unabhängigen ästhetischen Abnahme an Claude Design.
