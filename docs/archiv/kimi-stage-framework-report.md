> **Archiviert 2026-07-28 (CC) — Kimi-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# Bühnenspiel — §3 Schritt 2: Choreografie-Gerüst (Kurzbericht)

Stand: 2026-07-19, Branch `feat/council-rooms`. Gebaut über den **heutigen Plates**, ohne
ein einziges neues Bild. Beweisziel §0: Das Dokument ist vollständig, bevor irgendeine
Inszenierung läuft — No-JS und reduced-motion zeigen denselben vollständigen Endzustand.

## Was das Gerüst trägt

- **Eintritts-Klassifikator** (`site/src/lib/stage.js`): `fresh` (Direktaufruf/Hard-Reload),
  `arrival` (Raum→Raum gleiche Sprache), `language` (DE↔EN = kein Raumwechsel, keine
  Sequenz, nur Texttausch). Die Route ist die Wahrheit; alles reagiert auf from→to.
- **Beat-Sequenz** nur bei `fresh`: Plate → Plakette → Tafel → Röhre, Lock nach ~2,1 s,
  §0-Watchdog 3,5 s (schaltet das Dokument vollständig sichtbar, falls etwas nicht anläuft).
- **Arrival**: Tafel erscheint **nicht erneut** — sie steht von Beat 0 auf der Bühne
  (bereits sichtbar in der View-Transition-Capture), die Plakette fadet nach der Fahrt ein.
- **Röhre** (`StageTube.svelte`): 6 Perlen, SSR-Füllstand je Raum (Study 2, Council 5,
  Archive 6), Caption = aktiver Schritttext, sr-only-Status „Schritt n von 6". Gestaffeltes
  Einlaufen nur bei `fresh`.
- **Tafel**: genau **eine** `ResultBoard`-Instanz pro Route (jetzt auch im Archiv),
  `id="antwort"`, datengetrieben aus `recommendations`, keine Re-Aggregation.
- **Scroll während des Aufbaus** = Sprung in den Endzustand (`stage-skip` + Lock), keine
  Sperre, keine Queue. Nach dem Lock toggelt Scrollen `stage-unlocked`.
- **Mobile-Preload** der Nachbar-Plates: IntersectionObserver ≥60 % + Lock +
  `requestIdleCallback` (setTimeout-Fallback 400 ms), kein Preload bei `saveData`/2g,
  Navigation hängt nie am Prefetch.
- **Boot-Script** in `app.html`: setzt `stage-armed stage-play mode-fresh` vor dem ersten
  Paint nur für die sechs Raum-Pfade — kein Aufblitzen, kein FOUC.

## §0-Beweis: Modi × Verhalten (per CDP verifiziert)

| Modus | Sequenz | Ergebniszustand |
|---|---|---|
| Fresh (Direktaufruf) | spielt 2,1 s | identisch |
| Arrival (Türklick) | nur Plakette fadet nach | identisch, Tafel nie doppelt |
| Sprachwechsel DE↔EN | keine | Szene steht, Texte tauschen |
| Scroll während Aufbau | abgebrochen → Endzustand | identisch |
| prefers-reduced-motion | keine | identisch, sofort |
| No-JS | keine | identisch, vollständig im HTML |

Nachweise: 20 Frames + `checks.txt` in **`docs/review/stage-framework/`** —
**19/19 Checks OK** (Fresh-Sequenz 5 Frames, Ankunft /→/ratssaal/, Browser-Back mit
`navDir=back`, Sprachwechsel ohne `stage-armed`, Scroll-Skip, reduced-motion bei t=300 ms
komplett, No-JS Study + Council, Mobil 390×844 Lock + gescrollte Tafel).

## Budget-Messung (CDP Network, Cache aus, encodedDataLength)

| Messung | Initial | Cap §4 | Stand |
|---|---|---|---|
| Desktop `/` | 798 KB (35 req) | ≤ 1,2 MB | 67 % |
| Desktop `/archiv/` (schwerster Raum) | 1050 KB (31 req) | ≤ 1,2 MB | 87 % |
| Mobil `/` | 702 KB (33 req) | ≤ 900 KB | 78 % |
| Mobil `/ratssaal/` | 667 KB (33 req) | ≤ 900 KB | 74 % |
| Stage-JS (Layout-Chunk: stage.js + room-transitions.js) | **2,1 KB gzip** | ≤ 10 KB | 21 % |

Größte Einzelposten: Mobil-Plate `antechamber-portrait-display.jpg` 231 KB, prerendered
HTML 121 KB (das ist §0 — das ganze Dokument steht im HTML). Keine Bibliothek, animiert
wird nur `transform`/`opacity`. Das Preload feuerte in den Mess-Viewports nicht (Tür
<60 % sichtbar) — spec-konformer Opportunismus, keine Navigationsabhängigkeit.

## Gefundene und behobene Fehler (im Gerüst-Lauf)

1. **Implizites Keyframe-`to`**: im `.stage-play`-Block fehlte explizites `opacity: 1` —
   die statische Versteck-Regel las im Keyframe-Endzustand mit. Überall explizit gemacht.
2. **Plate in der VT-Capture**: der Plate-Takt lief auch bei `arrival` → Zielraum kam ohne
   sichtbare Plate in die Transition. Takt jetzt strikt `mode-fresh`.
3. **Plakette hinter fixer Tafel** ≥1200 px: `padding-left: 23.5rem` auf der Plakette.
4. **Testfallen**: sirv-Cache nach Rebuild (Preview-Neustart nötig), Preview bindet nur
   IPv6-`localhost` (127.0.0.1 refused), Reload stellt Scroll-Position wieder her
   (Skip-Test muss über `about:blank` navigieren).

## Tests / Build

- `site/tests/homepage-build.test.js`: **18/18 grün** — zwei neue Blöcke (Röhren-Füllstand
  DE+EN; §0: kein `stage-armed` im ausgelieferten `<html>`-Tag, genau eine ResultBoard +
  `id="antwort"` je Route). Build warnungsfrei.

## Slice-Grenze (ausdrücklich NICHT Teil dieses Schritts)

Kommt erst nach Abnahme des Gerüsts im Vertical Slice:

- kein Türblatt / keine freigestellte Tür-Ebene, keine Durch-die-Tür-Kamerafahrt
- keine **Tafel-Reise** (`view-transition-name`, `board-traveling`)
- kein **Röhren-Diff** 2→5 beim Übergang (Röhre hat heute festen SSR-Füllstand je Route)
- keine Akteur-Visuals (Scout/Warden als einfahrende Ebenen)

Berichtspflicht erfüllt; warte auf Abnahme bzw. „los" für den Vertical Slice.
