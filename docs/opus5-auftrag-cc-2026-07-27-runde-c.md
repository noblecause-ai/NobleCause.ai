# Auftrag an CC — Runde C: Spalt zeigt den Zielraum · Durchgang in Study und Council

**Von:** Opus 5 (Architekt) · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Vorlauf:** §6 Phase 1 lebt und trägt (Steward-Live-Blick bestanden).
**Commit-Freigabe für die Passage erteilt** — `door-passage.js`, `room-transitions.js`,
`(rooms)/+layout.svelte` bitte als eigenen Commit setzen, bevor Runde C beginnt. Kein Push.

---

## §1 · Der Spalt muss den Zielraum zeigen — auch im Ruhezustand

**Befund des Stewards:** Beim Hover steht der Spalt offen, dahinter ist Leere. Der Zielraum wird
erst beim Klick sichtbar, kurz vor der Fahrt.

Das ist der letzte Bruch im Rundgang. Der Spalt verspricht einen Nachbarraum und zeigt nichts —
und der Klick liefert dann etwas nach, das schon hätte da sein müssen. Umgekehrt ist es richtig:
**der Blick durch den Spalt ist das Versprechen, die Fahrt löst es ein.**

### Entscheid: der Ruhezustand benutzt denselben Ebenenstapel wie die Fahrt

Der Raum trägt im Ruhezustand **nicht** mehr ein einkomponiertes Auf-Plate, sondern den
Stapel bei Kamera 0: Void → Zielraum-Plate in der Ferne → Flügel → Wand-mit-Loch. Beim Hover
spreizen die Flügel; dahinter steht der Zielraum bereits an genau der Stelle, an der ihn die
Fahrt abholt.

**Das revidiert bewusst einen Teil meines §3-Entscheids.** Damals war das statische Auf-Plate
richtig, weil der Ebenenstapel noch nicht existierte und seine einzige Aufgabe ein Hover-Bild
gewesen wäre. Jetzt ist der Stapel gebaut, bewiesen und ohnehin im Betrieb — das Kostenargument
hat sich umgedreht. Der Grund für damals ist weggefallen, also fällt der Entscheid mit.

**Der zweite Grund wiegt schwerer:** Frame 1 der Fahrt muss dem Ruhebild exakt gleichen. Ein
gebackenes Auf-Plate kann das nur bei genau einem Viewport-Verhältnis leisten, weil die Ferne
im Stapel an der **Cover-Geometrie** hängt, im Plate aber an den Plate-Pixeln. Auf jedem anderen
Seitenverhältnis driften beide auseinander — und genau dort springt es beim Klick. Aus demselben
Stapel gebaut ist die Gleichheit **konstruktiv** statt gemessen. Das ist dieselbe Begründung, mit
der die Handoff-Anforderung in §6.3 steht.

### Auflagen

- **Der Ruhezustand ist statisch.** Keine rAF-Schleife, keine Animation, solange nicht gehovert
  wird — nur ein Stapel mit festen Transforms.
- **Kosten begrenzen:** das ferne Plate im Ruhezustand in kleiner Auflösung laden (es erscheint
  bei ≈ 0,38 × Cover hinter einem Spalt von wenigen Prozent Bildbreite). Die volle Auflösung
  wird beim Klick geladen — dort ist der `decode()`-Deckel ohnehin schon eingebaut.
- **§0 unverändert:** ohne JS und bei `prefers-reduced-motion` steht die geschlossene Tür. Der
  Stapel erzeugt keinen Inhalt, er zeigt Tiefe.
- **Nur Desktop ≥ 1200 px.** Mobil bleibt beim heutigen Bild.

**Abnahme:** Beim Hover ist durch den Spalt der Zielraum erkennbar (nicht nur Lichtschein);
Frame 1 der Fahrt ist vom Ruhebild ununterscheidbar — auf 16:9, auf 21:9 und auf einem hohen
schmalen Desktop-Fenster geprüft; kein Layout-Shift beim Hover.

---

## §2 · Study und Council bekommen den Durchgang — ohne Bestellung

Für beide Räume gilt: **es wird kein neues Bild bestellt.** Der Archiv-Weg (P7 bestellen, P8
bestellen, Plate daraus komponieren) war richtig, solange das Plate ohnehin ersetzt werden
musste. Hier muss es das nicht — und es *darf* es auch nicht:

- Am Study-Plate hängt die **Fensterparallaxe** (P5/P6 sind auf dieses Fenster eingepasst).
- An beiden Plates hängt die **gemessene Geometrie der Akteure** (Scout, Warden, Pulte,
  Plaketten).

Ein neu generiertes Plate verschiebt beides und zieht eine Runde Nachmessen nach sich, für die
es keinen Gegenwert gibt.

### Der Weg: aus dem vorhandenen Plate schneiden

Das ist der **§6-Spike aus der Übergabe**, jetzt fällig:

1. Die **Türflügel entlang der Laibung freischneiden**. Das herausgeschnittene Stück ist die
   Flügel-Ebene, das Loch ist die Apertur.
2. **Laibung, Sturz, Schwelle, Wandleuchten bleiben stehen** — sie liegen außerhalb der Flügel
   und werden vom Schnitt nicht berührt.
3. Was hinter den Flügeln fehlt, wird **nicht** gebraucht: die Flügel spreizen hinter die opake
   Laibung, dahinter steht die ferne Ebene. Genau so läuft es im Archiv bereits.

**Der Gewinn ist nicht nur die gesparte Bestellung:** Wand und Flügel stammen aus **denselben
Pixeln** wie das Ruhebild. Der geschlossene Zustand ist damit konstruktiv identisch mit dem
heutigen Plate — kein Nachmessen, keine Akteur-Korrektur, kein neuer Abgleich.

### Wenn der Schnitt nicht trägt

Trägt er in einem der beiden Räume nicht — weil die Flügel im Plate zu unscharf, zu schräg oder
mit der Laibung verbacken sind — **abbrechen und berichten, nicht nachbessern.** Dann bestelle
ich für diesen einen Raum P7/P8 nach (die zwei Prompts stehen in
`docs/bestellung-serie-5-archiv-2026-07-27.md` und sind in zwei Minuten auf den Raum umgeschrieben),
und wir nehmen das Nachmessen bewusst in Kauf. Ein halb überzeugender Freischnitt ist die
schlechteste der drei Möglichkeiten.

### Pro Tür, nicht pro Raum

Jede Tür braucht ihre eigene Apertur **und die Ferne ihres eigenen Ziels**. Bitte im Bericht den
Türgraph nennen (welche Tür führt wohin) und je Tür die am gerenderten AVIF gemessene Aperturmitte
für `perspective-origin`. Die bekannten Türzonen: Study 40–60 / 17–82 %, Council 43,5–57,9 /
18,3–65,9 %, Archiv 43–54,5 / 19,5–62,5 % — die sind je Raum verschieden, das war immer so.

---

## §3 · Parameter aus Phase 1 übernehmen, nicht neu erfinden

`perspective` ≈ 0,6 × Fahrtstrecke, `perspective-origin` auf die **gemessene** Aperturmitte,
Near-Fade fertig bei ≈ 55 % Distanz, Blur zieht vorher hoch, Void hinter den Ebenen, Fahrtkurve
spät beschleunigend. Diese Werte sind im Archiv erprobt — **ohne Anlass keine Abweichung**, und
falls doch, mit Messung begründet.

**Abnahme je Raum wie in Phase 1:** Frame-Reihe 0/25/50/65/80/100 %; bei 65 % ist die Ausgangswand
aus dem Bild; die letzten 35 % sind reiner Zielraum; Wachstumsverhältnis nah zu fern nennen;
Handoff auf Cover 1,0 bewiesen.

---

## §4 · Reihenfolge

1. Passage-Commit aus Phase 1 setzen.
2. **§1** (Spalt zeigt den Zielraum) — zuerst im Archiv, weil dort alles liegt.
3. **§2** Freischnitt Study, Durchgang bauen, Bericht.
4. **§2** Freischnitt Council, Durchgang bauen, Bericht.
5. Erst danach **§7** (Sitze um die Zählmaschine) auf der Tiefenlogik dieser Ebene.

Unverändert nicht Teil dieser Runde: der gebündelte **Medien-Strang** und die
**Protokollseiten**.

---

## §5 · Guardrails (unverändert)

Guard-Hook; Daten nur über Datenbranch + `--ff-only`; **nie `--no-verify`**; kein Push.
§0-Verfassung. Versiegelte Datennaht. Geometrie immer am gerenderten AVIF messen.
**Kein WebGL, kein Three.js** — falls es ohne nicht geht: abbrechen und berichten.
