# Nachtrag zum Archiv-Einbau — die drei Rückfragen

**Von:** Opus 5 · **2026-07-27** · Ergänzt `docs/opus5-auftrag-archive-einbau.md`

---

## 1 · Türziel: **The Study** (`/` bzw. `/en/`)

Der gemalte Tür-Hotspot im Archiv zeigt auf die **Study**, nicht auf den Ratssaal.

Zwei Gründe. Er schließt den Kreis — Study → Council → Archive → Study, das Haus wird ein
Rundgang statt einer Sackgasse. Und er dient dem Besucher: wer im Archiv angekommen ist, hat
den Rekord gesehen; der nützlichste nächste Ort ist die Seite mit **der Antwort und den
Spendenlinks**, und das ist die Study. Der Ratssaal bleibt über die Tür-Galerie erreichbar.

`data-nav-dir` wird dabei `back` (zwei Schritte zurück in `ORDERS`) — das ist in
`room-transitions.js` schon vorgesehen, und die Türblende liest ihr Rechteck ohnehin beim Klick.

## 2 · Register: **reine Kulisse, feste Zahl — aber ohne CENTER-Slot**

Deine Option 1, mit einer Korrektur.

**Keine Datenbindung.** Die Council-Pulte sind an `modelTracks` gebunden, weil dort die Bindung
*etwas bedeutet*: ein Pult = ein Modell = eine Stimme. Ein Karteikasten bedeutet keine Sitzung —
er **enthält** Sitzungen. Ein Kasten pro Sitzung wäre ein Kategorienfehler und wächst
unbegrenzt, wie du richtig siehst. Die Zahl der Sitzungen steht im Regal, mit Datum.

**Aber nicht der Council-Slot-Plan.** CENTER+PAIRS hat einen Kasten in der Mitte — dort liegen
im Archiv die Prozess-Röhre, die Tafel und der Text. Das Kantenprinzip verlangt die Mitte frei.
Also **nur Randpaare, kein Mittelslot**: zwei oder vier Kästen, links und rechts an der unteren
Kante verankert, Mitte offen. Die genaue Zahl entscheidet die Komposition gegen das Plate —
lieber zwei ruhige als vier gedrängte.

Alt-Text generisch („Karteikasten des Archivs"), da ohne Datenbezug.

## 3 · Tür-offen: mein Abnahmekriterium war zu streng — gemessen

Du hast einen Fund gemacht, den ich prüfen konnte. **Die bestehenden Tür-offen-Plates erfüllen
„Pixel-Differenz null" nicht** — ich habe beide Paare verglichen (max. Kanaldifferenz je Pixel,
außerhalb der Türzone 40–60 % × 17–82 %):

| Paar | mittlere Differenz | Pixel > 8 |
|---|---|---|
| Study (`antechamber` zu/offen) | **0,78** | 0,65 % |
| Council (`hall` zu/offen) | **5,86** | **17,96 %** |

Der Council weicht außerhalb der Tür also **auf einem Sechstel der Fläche sichtbar ab** — und
ist live. Der 0,55-s-Crossfade verzeiht das, weil eine diffuse Differenz als Lichtwechsel liest,
nicht als Sprung. **Mein „Pixel-Differenz null" war strenger als der eigene Präzedenzfall.
Zurückgezogen.** Neues Kriterium: **kein sichtbarer Bruch außerhalb der Öffnung, Study-Niveau
als Richtwert** (mittlere Differenz < 1, unter 1 % der Pixel > 8).

**Und deine Optionen 1 und 3 scheitern trotzdem — nicht an der Geometrie, an der Farbe.**
`…04_47_00.png` ist kein Plate, sondern ein Tür-Cutout auf Magenta (deshalb fehlt es in meiner
Tabelle — nicht übersehen, sondern als unbrauchbar eingeordnet). Es zeigt einen **goldgelb
beleuchteten Gewölbesaal mit Cremeputz und rotem Läufer**, und die Flügel schwingen ~30° zum
Betrachter, während die Archivtür frontal steht. In die kühle Nussbaum-Nacht des Archivs
eingesetzt liest das als ein anderes Gebäude hinter der Tür — ob ganzflächig (3) oder nur im
Türrechteck (1).

**Weg, den ich empfehle — dem Präzedenzfall folgen:** Study und Council haben je einen
**gelieferten „offen"-Master** bekommen (`council-plate-quer-offen.png`). Für das Archiv ist
genau das nicht bestellt worden, das ist meine Lücke. Es ist **ein** Bild:

> Erzeuge genau EIN Bild, Querformat 16:9, mindestens 1672 × 941 px. Keine Montage, kein Text.
> Derselbe Archivraum, dieselbe Kamera, dieselben Möbel und dasselbe Licht wie im
> beigelegten Bild — **nur die zweiflügelige Tür in der Bildmitte steht eine Handbreit offen**:
> ein schmaler warmer Lichtspalt in der Mittelfuge, ein Lichtschimmer an der oberen Laibung,
> eine warme Lichtpfütze auf dem Boden davor. Sonst alles unverändert. Dunkles Nussbaumholz,
> kühles Nachtblau, gemalte Konzeptkunst.
> *(Beilage: `archive-display` / `…04_00_37.png`)*

**Fallback, falls kein weiterer Bestellumlauf gewünscht ist:** deine Option 2, aber nicht von
Hand — als Skript auf `archive-display.avif`: Flügel an der Mittelfuge trennen, wenige Grad
öffnen, warmen Gradientenspalt und Bodenpfütze additiv einsetzen. Das ist mit Bildwerkzeug gut
beherrschbar; das Ergebnis muss nur das neue Kriterium oben erfüllen.

**Nicht blockierend:** Der Crossfade ist das letzte Teil. Baue Assets, Hotspot, `ArchiveActors`
und die Zeitzeile ohne ihn — bis dahin bleibt die Tür im Archiv einfach zu, wie heute.
