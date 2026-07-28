> **Archiviert 2026-07-28 (CC) — Kimi-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# Auftrag für Kimi — Korrektur „Das Vorzimmer" (The Study)

## Rolle & Rahmen
- Du korrigierst die Svelte-Site. **Architektur/Design ist unten vorgegeben** — Umsetzung, Messung und Verifikation liegen bei dir.
- Bestehende Konventionen strikt einhalten: **kein Commit**; Tabu-Pfade unberührt; nur `site/` + `docs/`; Build warnungsfrei; **alle Tests grün**; DE + EN parallel; prerendered — **funktioniert ohne JS und per Tastatur**; `prefers-reduced-motion` respektieren; Mobil sauber (kein Overflow). Verifikation per Screenshot-Diff wie gehabt, Ablage unter `docs/review/`.
- Vorgehen: **erst inspizieren + messen, dann umsetzen, dann verifizieren.** Bei Unklarheit (z. B. Tür-Koordinaten) messen statt raten. Offene Punkte melden, nicht überschreiben.

## Nicht-Ziele
- Keine Neugestaltung der ganzen Site, keine neue Kunst generieren (fehlende Assets nur als Anforderung melden), Tabu-Pfade nicht anfassen, vorhandene Details nicht löschen — nur verschieben/verstecken.

---

## Aufgabe 1 — Falsche Tür korrigieren
**Problem:** Der bestehende `door-hotspot` in `StudyRoom.svelte` liegt auf einer **Wandfläche im falschen Plate**. Die Übergangs-Mechanik (View-Transition, `--vt-origin`, Hover/Fokus-Glow, Reduced-Motion, Zurück-Navigation) ist korrekt und **bleibt erhalten** — falsch sind nur **Bild + Hotspot-Position**.

**To do:**
- Die korrekten Plates liegen **neu in `docs/`** (Motiv „Wart wach" / „Wart schlafend"). Finde sie, prüfe Auflösung/Format, binde das richtige als Study-Plate ein (gleiche Größen-/Qualitäts-Konvention wie die übrigen `*-display.jpg`-Plates).
- Bestimme im **korrekten** Plate die tatsächliche Türzone per Crop-Messung (x/y in %) und setze den `door-hotspot` **exakt dorthin**.
- Falls im korrekten Motiv **keine reale Tür** sichtbar ist: den Hotspot **nicht auf eine Wand zwingen** — stattdessen kurz mit Foto-Beleg zurückmelden und einen Alternativ-Anker vorschlagen.
- „Wart wach/schlafend": Falls zwei Zustände gemeint sind, klären, welcher der Standard-Plate ist. Den zweiten nur einbinden, wenn im Design vorgesehen — sonst offenlassen und melden.

**Akzeptanz / Verifikation:** Hover- und Fokus-Glow messbar sichtbar (Flächenhelligkeit > Ausgangswert); Transition-Ursprung an der **neuen** Türmitte; Reduced-Motion-Pfad sauber; Zurück-Navigation ok; Mobil-Verhalten des Hotspots korrekt. Screenshots ablegen.

---

## Aufgabe 2 — Hintergründe statisch, Text fließend darüber
- Raum-Plates werden zur **statischen Hintergrundebene**: kein Bewegungs-/Parallax-/Transition-Effekt mehr **auf dem Bild selbst**. (Die Seite-zu-Seite-View-Transition **zwischen** Räumen bleibt unberührt.)
- Inhalt (Titel, Untertitel, Antwort-Board, Prozess) läuft als **normaler Fließtext/Scroll darüber**.
- Lesbarkeit über weichen **Verlaufs-Scrim** hinter den Textzonen sichern — **keine harten Kästen**. Kontrast WCAG-tauglich.
- **Reading-Order** korrigieren, falls invertiert: Titel/Frage → Untertitel (was passiert) → Antwort dieser Sitzung → Prozess → Dossiers.
- Konsistent für **alle Räume**, nicht nur Study.

---

## Aufgabe 3 + 4 — Prozess + „Scout/Warden" zusammenführen und entrümpeln
Ersetze den Block **„The Scout und The Warden — Späher und Wart"** samt roher Recherche-Listen durch **EINE bildhafte Ablauf-Leiste**. Der Prozess ist ein **gerichteter Ablauf** — das muss man **sehen**, nicht lesen.

### Ablauf (mit sichtbarer Richtung)
```
Der Späher  →  Der Wart  →  Der Rat  →  Die Antwort
```

### Namen — Variante B (verbindlich)
- **DE:** „Der Späher", „Der Wart", „Der Rat"
- **EN:** „The Scout", „The Warden", „The Council"
- **Pro Rolle genau EIN Name je Sprache.** Keine Doppelnennung „X — Y" mehr.

### Pro Stufe nur: Emblem + Name + ein Satz Klartext
- **Der Späher:** „Sammelt die Belege — Studien, Kosten-Wirksamkeit, Finanzierungslücken."
- **Der Wart:** „Ordnet und prüft die Belege und macht die Herleitung nachvollziehbar."
- **Der Rat:** „Wägt ab und entscheidet."
- **Die Antwort:** die vier Empfehlungen dieser Sitzung (verlinkt aufs Board).

### Pfeile / Richtung
Bernsteinfarbener Konnektor (`→`) zwischen den Stufen: **horizontal auf Desktop, vertikal gestapelt auf Mobil.** Alternative zum Glyph erlaubt (dünne Linie mit Pfeilspitze) — Hauptsache **Reihenfolge und Richtung sind eindeutig**.

### Entrümpeln
- **Keine Listen im sichtbaren Fließtext.** Die rohe „Recherche-Spur (wörtlich)", das Dossier, verworfene Funde und das „Protokoll" wandern hinter **Ausklapp/Link** („Dossier öffnen" / „Recherche zeigen"), **standardmäßig eingeklappt**.
- **Amtssprache raus:** „öffentliches Beratungsprotokoll", „Belege" ohne Bezug, „Recherche-Spur (wörtlich)" ersetzen durch die Klartext-Sätze. Ton: **erklärend, nicht behördlich.**
- „Scout/Warden" erscheinen **nicht mehr als zwei separate große Sektionen**, sondern nur als **zwei Stufen** dieser einen Leiste.

### Akzeptanz
- Ein Besucher versteht in **< 5 s ohne Klick**: wer sammelt, wer prüft, wer entscheidet — und in welcher Reihenfolge.
- Keine sichtbare Liste, keine Doppelnamen, keine rohen Suchanfragen im Erstkontakt.
- Alle Details vollständig erreichbar (nur verschoben, nicht gelöscht).

---

## Deliverables
- **Screenshots** (Desktop + Mobil, DE + EN) unter `docs/review/`:
  - Study mit korrekter Tür: hover / focus / transition / reduced-motion
  - Statischer Hintergrund + Fließtext (Lesbarkeit/Scrim)
  - Neue Ablauf-Leiste: eingeklappt + ausgeklappt
- **Kurzreport** im gewohnten Stil (was gemessen, was geändert, Testzahl, Auffälligkeiten). **Kein Commit.**
- **Offene Rückfragen** (z. B. Tür ohne Motiv, zweiter Wart-Zustand) explizit melden statt raten.
