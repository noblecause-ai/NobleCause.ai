> **Archiviert 2026-07-28 (CC) — Codex-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# Codex-Auftrag: NobleCause.ai für Live-Gang fertigstellen

Arbeite im bestehenden Repository auf dem aktuellen Branch. Lies zuerst:

- `AGENTS.md`
- `docs/handoff-notes-for-codex.md`
- `docs/codex-analysis.md`
- `docs/codex-corrective-build-report.md`
- `site/static/media/ASSETS.md`

## Aufgabe

1. **Neue Bilder aus `docs/` übernehmen**
   - Finde die neu abgelegten Prozess- und Säulenbilder.
   - Ordne sie eindeutig zu:
     - Prozess: Frage, Belege sammeln, drei Antworten, Gegenlesen/Umdenken, Zählen, Veröffentlichen
     - Säulen: Investition in die Zukunft, Linderung von Leid, Schutz vor großen Gefahren, Übersehenes
   - Benenne sie semantisch und konsistent um.
   - Lege sie sauber unter `site/static/media/` ab, z. B.:
     - `site/static/media/process/`
     - `site/static/media/pillars/`
   - Bewahre Originale unverändert, dokumentiere Quelle, Dateiname, Maße, Größe und SHA-256 in `site/static/media/ASSETS.md`.
   - Entferne die Arbeitskopien aus `docs/` erst, wenn die produktiven Kopien geprüft sind.

2. **Bilder in die Startseite integrieren**
   - Ersetze die bisherigen generischen Prozesssymbole durch die neuen gemalten Motive.
   - Ersetze die bisherigen Säulensymbole durch die vier neuen gemalten Motive.
   - Die Bilder müssen Teil derselben Ratssaal-Bildsprache sein, nicht wie fremde Kacheln wirken.
   - Passe Zuschnitt, Vignette, Kontrast und Größe so an, dass Text und Bild zusammengehören.
   - Keine neuen fachlichen Texte erfinden.

3. **Beschriftungen räumlich korrekt verankern**
   - Korrigiere besonders die Modellnamen im Ratssaal.
   - Labels müssen exakt bei den zugehörigen Pulten sitzen, nicht nur ungefähr im Bild.
   - Verwende ein nachvollziehbares Anchor-Modell pro Szene und Breakpoint, bevorzugt relative Bildkoordinaten/CSS-Custom-Properties statt verstreuter Pixelwerte.
   - Prüfe mindestens bei:
     - 1440 × 900
     - 1024 × 768
     - 390 × 844
     - 320 × 700
   - Bei wechselndem `object-fit` oder `object-position` müssen die Labels weiterhin auf den Objekten bleiben.
   - Wenn eine präzise Verankerung mobil nicht möglich ist, verwende dort eine eigene, bewusst komponierte Beschriftung statt falscher Overlays.

4. **Repository aufräumen**
   - Entferne nur eindeutig veraltete, unreferenzierte Homepage-Assets, CSS-Platzhalter, tote Komponenten und alte Review-Artefakte.
   - Verändere keine geschützten Datenpfade:
     - `sessions/**`
     - `journal/**`
     - `schedule.json`
     - `gremium/**`
     - `schema/**`
   - `sol-build/` bleibt historische Referenz, sofern keine bereits freigegebene Cleanup-Regel etwas anderes verlangt.
   - Keine zweite App und keinen neuen Prototypordner anlegen.
   - Prüfe nach dem Cleanup auf tote Imports, ungenutzte Assets und gebrochene Links.

5. **Für Live-Gang vorbereiten**
   - Führe mindestens aus:
     ```bash
     cd site
     npm ci
     npm test
     npm run build
     npm run preview
     ```
   - Prüfe die produktive Ausgabe aus `site/build/`.
   - Prüfe alle acht Szenenzustände, No-JS, Reduced Motion, Tastatur, Browser-Zurück und Hash-Navigation.
   - Prüfe Desktop und Mobil auf Überlauf, abgeschnittene Labels und falsche Bildanker.
   - Prüfe direkte Spendenlinks, Archivlinks und alle internen Routen.
   - Prüfe Bildgrößen und unnötige Mehrfachdownloads.
   - Erzeuge aktualisierte finale Screenshots unter:
     - `docs/review/final-release/`
   - Noch nicht mergen, deployen oder nach `master` pushen.

## Abnahmekriterien

- Alle zehn neuen Bilder sind semantisch benannt und sauber im produktiven Assetpfad abgelegt.
- Prozess- und Säulenbilder sind sichtbar und stilistisch integriert.
- Modellnamen und andere Bildbeschriftungen treffen ihre tatsächlichen Objekte in allen geprüften Viewports.
- Keine sichtbaren CSS-Platzhalter mehr.
- Keine toten Assets oder gebrochenen Imports.
- Tests und Produktionsbuild sind erfolgreich.
- Die komplette Site wirkt konsistent, nicht nur die Startseite.
- Die produktive Ausgabe liegt in `site/build/`.

## Abschlussbericht

Erzeuge:

`docs/codex-release-readiness-report.md`

Der Bericht ist für OpenAI- und Anthropic-Review bestimmt und enthält:

1. Zusammenfassung der Änderungen
2. Liste der umbenannten und verschobenen Bilder
3. Mapping Bild → Prozessschritt/Säule
4. Beschreibung des Anchor-Modells für Beschriftungen
5. Geänderte und entfernte Dateien
6. Ausgeführte Befehle mit Exit-Codes
7. Testergebnisse
8. geprüfte Viewports und Szenenzustände
9. No-JS-, Reduced-Motion- und Tastaturbefund
10. Performance- und Assetbefund
11. verbleibende Risiken oder offene Punkte
12. klare Empfehlung: `READY FOR REVIEW`, `READY FOR MERGE` oder `NOT READY`, mit Begründung

Beende nach Bericht und Screenshots. Kein Merge und kein Deployment.
