# Raumübergang — Review des WebGL-Plans + Bauauftrag „Tür-Gegenprobe"

**Von:** Opus 5 (Architekt/Review) · **Für:** CC (Bau) · **Datum:** 2026-07-24
**Betrifft:** `docs/webgl-portal-architektur-plan.md` (Revision) und einen vorgezogenen
CSS-Spike, der die 3D-Entscheidung erst entscheidbar macht.

**Steward-Entscheid 2026-07-24 (nach Review):** Vor jeder 3D-Zeile wird die **billige
Gegenprobe** gebaut (§B). Der WebGL-Plan bleibt gültig, aber mit den Korrekturen aus §A —
und erst, wenn die Gegenprobe nachweislich nicht genügt.

---

## §A · Korrekturen am WebGL-Portal-Plan (verbindlich, bevor Phase 0 startet)

### A1 — Die 3D-/Canvas-Ebene gehört ins persistente Layout, nicht in den Raum
Der Plan sagt „Canvas über dem Study-Hero", also in den `scene2`-Slot von `StudyRoom`.
SvelteKit zerstört `StudyRoom` beim Routenwechsel — der Canvas stirbt **genau im Moment des
Durchflugs**. Mount-Punkt ist `site/src/routes/(rooms)/+layout.svelte` (überlebt alle drei
Raum-Routen); der aktive Raum kommt per Prop/Store hinein. Ohne das ist Phase 1 nicht baubar.

### A2 — View-Transitions und ein live gerenderter Durchflug schließen sich aus
Die VT-API friert alte und neue Seite als **statische Snapshots** ein. Eine animierende
3D-Ebene wäre darin eingefroren. „VT optional" (Plan §2) ist zu weich. Verbindliche Sequenz:

1. Klick auf die Tür → Räum-Beat (`stage-clearing`, `--retreat: 1`) wie heute
2. DOM-Overlay (Plakette, Röhre, Raumtext) blendet ab — Tafel und Masthead bleiben stehen
3. **Fahrt** auf der persistenten Bühnen-Ebene, VT **unterdrückt**
4. An der Schwelle `goto()` — der DOM-Wechsel passiert unsichtbar hinter dem gefüllten Frame
5. Ruhekomposition des Zielraums, Overlay wieder ein, `playStage()`

Konsequenz: `view-transition-name: board` / `masthead` verlieren während der Fahrt ihre
Shared-Element-Mechanik. Ersatz: beide liegen als DOM **über** der Bühne und bleiben
schlicht stehen; nur ihr Textinhalt crossfadet. (Der VT-Pfad bleibt als Fallback für alle
Fälle ohne 3D-Ebene erhalten — das ist ohnehin §0.)

### A3 — Three.js ist für das beschriebene Ziel überdimensioniert
Plan §2 beschreibt: vier Ebenen auf verschiedenen Z, Pointer-Parallaxe, Dolly in die
Türmitte. Das ist exakt `perspective` + `translateZ` auf den vorhandenen `<img>`-Ebenen.
Vorteile von CSS-3D gegenüber Three.js hier:

- keine ~150 kB Dependency, kein Lazy-Chunk-Thema, kein zweiter Renderer
- die AVIF-Decodes der bestehenden `<img>` werden wiederverwendet (Speicher, Mobil)
- **keine zweite Kompositions-Implementierung** (siehe A4 — der eigentliche Kostenpunkt)
- keine `pointer-events`/Fokusreihenfolge-Risiken, DOM bleibt DOM

Three.js erst, wenn ein konkreter Effekt es erzwingt: echter Stencil-Portal, Depth-Map-
Parallaxe **innerhalb** eines Plates, Shader-Licht durch die Türöffnung. Die MotionSites-
Vorlage nutzt WebGL, weil sie mehr macht als wir brauchen — das ist kein Argument für uns.

### A4 — Der eigentliche Kostenblock ist die Paritätspflicht, nicht die Szene
„Ruhebild deckungsgleich mit dem heutigen 2D-Bild" heißt konkret: `object-fit: cover` +
`object-position: var(--bg-pos)` je Breakpoint, Portrait-Plates, die 800/1024-srcset-Stufen
und der `--retreat`-Scrub müssten in Kamera-/UV-Mathematik nachgebaut **und dauerhaft
synchron gehalten** werden. Jede künftige 2D-Korrektur wäre doppelt zu pflegen. Genau daran
sterben solche Ebenen. Bei CSS-3D existiert die Frage nicht: dieselbe Komposition, nur mit Z.

### A5 — 3D-Container und fixe Bühne: harter Fallstrick
`perspective`/`transform` auf einem Vorfahren macht diesen zum **Containing-Block für
`position: fixed`**. Die fixe Bühne (`.room-bg img`, `.clouds`, künftig `.rail`) hängt genau
daran; `docs/cc-fix-akteure-fixe-buehne.md` hält ausdrücklich fest, dass kein Vorfahre
`transform`/`filter` trägt. → Der 3D-Container muss **selbst** das fixe Element sein:
`position: fixed; inset: 0; perspective: …`, die Ebenen darin `position: absolute`.
**Reihenfolge: erst der Akteur-Fix landen und abnehmen, dann 3D. Nicht parallel.**

### A6 — Asset-Konsequenz härter fassen (blockiert Phase 1, nicht Phase 0)
Plan §6 nennt nur „Hintergrund hinter der Tür gefüllt". Für einen echten Durchflug fehlt
das Gegenteil. Gebraucht wird je Raum-Paar:

- **Wand-Plate mit ausgeschnittener Türöffnung (Alpha)** — sonst ist der Zielraum nie
  *durch* die Öffnung sichtbar, sondern immer nur davor oder dahinter
- **Türblatt als eigener Cutout** + Laibung/Rahmen als eigene Ebene
- **Zielraum-Plate in höherer Auflösung** — am Ende der Fahrt füllt es den Frame; die
  heutige VT skaliert auf `scale(2.4)` und wird dabei sichtbar weich

Das ist eine konkrete Codex-Serie (Disziplin analog `docs/codex-serie-2-council.md`), keine
Prüfaufgabe. **Für Phase 0 (nur Parallaxe) genügt das heutige Material — das stimmt im Plan.**

### A7 — Zeitbudget: nicht die Fahrt kürzen, den Leerlauf entfernen
**Revidiert 2026-07-24 nach Steward-Klarstellung.** Wirkung ist Pflicht — eine Fahrt von
1,2–2,0 s ist **nicht** das Problem und wird nicht wegoptimiert. Das Problem sind die
Sekunden, in denen **nichts passiert**:

- **Vor** der Fahrt: `480 ms` Räum-Beat, in denen der Klick noch keine Kamerabewegung
  erzeugt — das fühlt sich wie ein hängender Link an. Ziel: **≤ 200 ms bis zur ersten
  Bewegung**; das Schienen-Räumen darf **in** die Fahrt hineinlaufen, statt ihr voranzugehen.
- **Nach** der Landung: bis `2100 ms` Eintritts-Choreografie, in denen der Angekommene auf
  Inhalt wartet. Ziel: der Zielraum ist bei Ankunft **sofort lesbar**; die Beats laufen über
  bereits lesbarem Inhalt, nicht davor.

Messgrößen also: **Zeit bis erste Bewegung ≤ 200 ms** und **Zeit bis Zielraum lesbar
≤ 2,5 s**. Die Fahrtdauer selbst ist frei — sie ist der Effekt, nicht der Aufwand.

---

## §B · Bauauftrag: Tür-Gegenprobe (vorgezogen, klein, entscheidungstragend)

**Warum:** Der heutige Übergang ist „ganzer Frame skaliert 2.4 + Crossfade". Er liest nicht
als Tür — aber nicht, weil 2D zu wenig kann, sondern weil (a) keine Parallaxe existiert und
(b) **der Zielraum nicht durch die Türöffnung erscheint**, sondern den ganzen Frame ersetzt.
(b) lässt sich ohne jede 3D-Ebene testen: Der neue Raum wird per `clip-path` **aus dem
Türrechteck heraus aufgezogen**. Die Koordinaten liegen bereits vor.

Liest das schon als „durch die Tür", spart es das größte Arbeitspaket des Projekts. Liest es
nicht, haben wir eine ehrliche Referenz, gegen die Phase 0 antreten muss. Das ist das
Gate-Prinzip des Projekts auf die eigene Bauentscheidung angewandt.

### B1 — JS: Türgeometrie in CSS-Variablen (`site/src/lib/room-transitions.js`)

Im bestehenden `click`-Handler, direkt nach `const rect = door.getBoundingClientRect();` —
der Handler greift für `.door-hotspot` (Desktop) **und** `.door-gallery a` (Mobil/Fallback),
beides sind echte Rechtecke, beides funktioniert:

```js
// Türrechteck als inset() für die Portal-Blende. Das Ziel wird aus GENAU
// dieser Kontur aufgezogen — dieselbe Geometrie, die auch --vt-origin trägt.
const el2 = document.documentElement;
el2.style.setProperty('--door-top',    `${Math.max(0, Math.round(rect.top))}px`);
el2.style.setProperty('--door-right',  `${Math.max(0, Math.round(window.innerWidth  - rect.right))}px`);
el2.style.setProperty('--door-bottom', `${Math.max(0, Math.round(window.innerHeight - rect.bottom))}px`);
el2.style.setProperty('--door-left',   `${Math.max(0, Math.round(rect.left))}px`);
```

Das `data-portal`-Flag wird **erst** gesetzt, wenn feststeht, dass die Fahrt wirklich läuft —
also nach allen Guards, direkt neben `el.classList.add('stage-clearing')`:

```js
el.dataset.portal = '';
```

So bleibt Browser-Back/Forward (kein Klick auf eine Tür) beim heutigen Verhalten — dort ist
ein Türrechteck bedeutungslos.

Aufräumen in `transition.finished.finally(...)` **und** im `catch`-Zweig, neben
`delete document.documentElement.dataset.navDir`:

```js
delete document.documentElement.dataset.portal;
```

### B2 — CSS: die Blende (`site/src/routes/(rooms)/+layout.svelte`, Style-Block)

Ergänzend zu den bestehenden Regeln im `@media (prefers-reduced-motion: no-preference)`-Block.
`::view-transition-old/new(root)` sind gewöhnliche Boxen — `clip-path` animiert dort normal.
`board` und `masthead` haben eigene VT-Namen, liegen also **außerhalb** dieser Blende und
bleiben sichtbar stehen, während der Raum wächst (gewollt: der Kopf ist der feste Rahmen).

```css
/* ---- Tür-Gegenprobe (Spike): der Zielraum wird aus der Türkontur
   aufgezogen, statt den ganzen Frame zu ersetzen. Nur bei echter
   Türfahrt (data-portal, gesetzt im Klick-Handler) — Back/Forward und
   Quereinstiege behalten das bisherige Verhalten. Fallback-Werte in
   var() greifen, falls die Geometrie fehlt (dann: Blende aus der Mitte). */
:root[data-portal]::view-transition-old(root) {
  animation: portal-out 1.1s cubic-bezier(0.45, 0, 0.8, 0.6) both;
}
:root[data-portal]::view-transition-new(root) {
  animation: portal-in 1.1s cubic-bezier(0.2, 0.7, 0.2, 1) both;
}
:root[data-portal]::view-transition-group(board),
:root[data-portal]::view-transition-group(masthead) {
  animation-duration: 1.1s;
}
@keyframes portal-out {
  to {
    /* deutlich schwächer als die alten 2.4 — der Frame fährt auf die Tür
       zu, statt an ihr vorbeizuschießen; die Blende trägt jetzt den Effekt */
    transform: scale(1.55);
    opacity: 0;
    filter: brightness(0.34);
  }
}
@keyframes portal-in {
  from {
    clip-path: inset(
      var(--door-top, 30%) var(--door-right, 40%)
      var(--door-bottom, 12%) var(--door-left, 40%) round 6px
    );
    transform: scale(1.14);
  }
  to {
    clip-path: inset(0 0 0 0 round 0);
    transform: none;
  }
}
```

### B3 — Nebenfix im selben File (§0-Lücke, gehört dazu)

`room-transitions.js:78` — `setTimeout(() => goto(to), 480)`. `stage-clearing` und
`--retreat: 1` werden **ausschließlich** über `applyEntryMode()` in `onNavigate` zurück-
gesetzt. Findet die Navigation nicht statt (abgebrochen, Fehler, offline), bleibt die Bühne
**dauerhaft ausgeräumt** — der `pageshow`-Guard fängt nur den bfcache-Fall. Analog zum
`playStage`-Watchdog in `stage.js`:

```js
el.classList.add('stage-clearing');
el.style.setProperty('--retreat', '1');
// §0-Sicherung: bleibt die Navigation aus, wird die Bühne zurückgeholt,
// statt dauerhaft ausgeräumt stehen zu bleiben.
const guard = setTimeout(() => {
  el.classList.remove('stage-clearing');
  el.style.removeProperty('--retreat');
  delete el.dataset.portal;
}, 1800);
setTimeout(() => goto(to).finally(() => clearTimeout(guard)), 480);
```

### B4 — Abnahme

1. Study → Council auf 1440 px: Der Ratssaal **wächst aus der Türkontur** heraus; Kopf und
   Tafel stehen dabei stabil. Ohne `data-portal` (Browser-Back) unverändertes Verhalten.
2. 390 px: dieselbe Blende, Ursprung ist die angeklickte Galerie-Karte. Kein Overflow.
3. `prefers-reduced-motion: reduce`: kein Ride, sofortiger Wechsel — unverändert.
4. Kein JS / fehlende VT-API: normaler Link. Unverändert.
5. Zeitmessung Klick → gelockte Szene: soll unter 2,5 s liegen (A7). Falls nicht, zuerst die
   Eintritts-Choreografie kürzen, nicht die Fahrt.
6. `npm run build` warnungsfrei, Testsuite grün, **Preview nach dem Build neu starten**.

### B5 — Was der Spike NICHT beantwortet

Die Parallaxe zwischen Wand, Türlaibung und Akteuren fehlt weiterhin — die trägt Phase 0
(A3, CSS-3D). Die Gegenprobe beantwortet nur die Frage: *Wie viel „durch die Tür" kommt
allein aus der Blende?* Das Ergebnis geht zurück an den Steward, bevor Phase 0 startet.

---

## §C · Priorität (revidiert 2026-07-24 nach Steward-Klarstellung)

Ursprünglich hatte ich das Portal hinter das Go-Live gestellt, mit dem Argument, es sei „am
wenigsten notwendig". **Dieses Argument ziehe ich zurück.** Wirkung ist Pflicht; der
Türübergang ist Kernwert, nicht Zierrat. Was bleibt, ist reine Abhängigkeitslogik: Phase 1
braucht Assets, die es noch nicht gibt (§A6), und das Archive wartet ohnehin auf Serie 3.

1. Akteur-Fix (Voraussetzung für alles Weitere, §A5)
2. **Tür-Gegenprobe (§B)** — billig, und sie kann den Wow-Effekt bereits liefern
3. Council verifizieren
4. **Entscheidungspunkt Steward: trägt die Gegenprobe den Effekt?**
   - **ja** → Archive/EN/Merge, Go-Live mit diesem Übergang; Phase 0/1 danach als Ausbau
   - **nein** → **Phase 0 (CSS-3D-Spike) vor dem Go-Live**, parallel die Asset-Serie aus §A6
     bei Codex bestellen. Dann ist der Durchflug Teil des ersten Eindrucks, nicht ein
     Nachtrag.

Nicht verhandelbar bleibt nur: erst Akteur-Fix, dann 3D (§A5) — und keine 3D-Ebene, bevor
die Assets aus §A6 vorliegen.
