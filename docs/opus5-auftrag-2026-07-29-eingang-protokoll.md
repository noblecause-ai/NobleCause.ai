# Auftrag an CC — Eingang zum Protokoll (Archiv)

**Von:** Opus 5 (Architekt), 29. Juli 2026
**Betrifft:** Übergabe `UEBERGABE-2026-07-28-architekt.md` §7 Punkt 1
**Vorlage:** `docs/mockup-2026-07-29-eingang-protokoll.html` — **im Browser öffnen, bevor du
anfängst.** Das Mockup ist die Vorlage, dieser Text erklärt sie nur. Bei jedem Widerspruch
zwischen Prosa und Mockup gilt das Mockup.

Dieser Auftrag enthält den fertigen Diff. Du musst nichts aus einer Beschreibung ableiten —
das ist der Punkt (§6 der Übergabe: „Plausibel ist oft falsch"). Deine Aufgabe ist
**anwenden, bauen, messen, berichten** — nicht entwerfen.

---

## 0 · Vorbedingungen

**Der Arbeitsbaum ist dirty.** Vor dem ersten Befehl prüfen:

- `gremium/prompts.py` ist modifiziert — **Guard-Tabupfad auf `feat/*`**. Nicht anfassen,
  nicht mitcommitten. Wenn der Guard-Hook beim Revert-Commit anschlägt, **melden und
  stoppen**, nicht `--no-verify`.
- `AGENTS.md` modifiziert, dazu ~30 gelöschte `.jpg` unter `site/static/media/**` — das ist
  der offene Medien-Strang (Übergabe §7 Punkt 5). **Gehört nicht in diesen Auftrag.**
  Nicht mitcommitten, nicht wiederherstellen.
- Alle diese Änderungen sind unstaged; `git revert` sollte daran nicht scheitern. Falls
  doch: `git stash push` nur für die betroffenen Pfade, danach zurück. Kein globales stash.

Branch: `feat/council-rooms`. **Kein Push.**

---

## 1 · Schritt 1 — Rückbau (eigener Commit)

```
git revert --no-edit b32df19
```

`b32df19` ist HEAD, der Revert sollte konfliktfrei laufen. Er entfernt:

- `site/src/lib/desk-passage.js` (174 Zeilen)
- den Einhänger in `site/src/routes/(rooms)/+layout.svelte` (50 Zeilen)
- die Klasse `desk-link` an **zwei** Stellen in `ArchiveRoom.svelte` — Zeile 116
  (Sitzungsarchiv-Zeilen) und Zeile 219 (Protokoll-Link)

> **Merke für den Bericht:** Der Übergang hing an *allen* Archiv→Explorer-Links, nicht nur
> am Protokoll-Link. Das erklärt das Symptom vollständig: der Schreibtisch blitzte bei jedem
> Klick aus dem Sitzungsarchiv auf.

**Gegenprobe nach dem Revert:**

```
grep -rn "desk-link\|desk-passage" site/src/     # muss leer sein
```

Danach: frischer Build, Archiv im Browser, ein Klick auf eine Sitzungszeile — kein
Schreibtisch mehr, normale Navigation. **Erst wenn das sitzt, Schritt 2.**

---

## 2 · Schritt 2 — Die Plakette (eigener Commit)

Zwei getrennte Commits, damit der Rückbau für sich prüfbar bleibt.

### 2.1 · Import ergänzen

`site/src/lib/components/rooms/ArchiveRoom.svelte`, Import-Block (nach Zeile 14):

```diff
 	import { locales, roomPaths } from '$lib/i18n/index.js';
+	import { formatDate } from '$lib/format.js';
 	import { TUBE_FILLED } from '$lib/stage.js';
 	import { DOOR_PASSAGES } from '$lib/door-passages.js';
```

`formatDate` ist der einzige Datums-Formatter im Projekt (`lib/format.js`) und in
`ArchiveRoom.svelte` bisher **nicht** importiert. Nicht selbst formatieren, nicht
`item.date` roh ausgeben.

### 2.2 · Markup

Dieselbe `<section class="room-section">` wie heute (nach dem Revert Zeile ~219):

```diff
 		<section class="room-section">
-			<a class="protocol-link" href="/sessions/{home.currentSession.id}/">{t.archive.protocolLink}</a>
+			<a class="protocol-plaque" href="/sessions/{home.currentSession.id}/">
+				<span class="plaque-meta"
+					>{t.archive.sessionLabel(home.currentSession.number)} ·
+					<time datetime={home.currentSession.date}
+						>{formatDate(home.currentSession.date, t.lang)}</time
+					></span
+				>
+				<span class="plaque-label">{t.archive.protocolLink}</span>
+			</a>
 			{#if t.archive.protocolNote}
 				<small class="record-note">{t.archive.protocolNote}</small>
 			{/if}
 		</section>
```

**Keine neue Zeichenkette.** `t.archive.protocolLink` und `t.archive.sessionLabel(n)` gibt es
beide schon (`de.js:293`, `de.js:300`) — die EN-Fassung kommt ohne neue Übersetzung mit.
`home.currentSession.{number,date}` liegt bereits am Client an (siehe `ResultBoard.svelte`,
das die Kombination genauso baut).

Das `<time datetime>` ist Pflicht: dieselbe Semantik wie in `ResultBoard.svelte:25` und
`StudyActors.svelte:129`. Nicht weglassen.

### 2.3 · CSS

Der Block `.protocol-link` (heute Zeile ~408) wird **ersetzt**, nicht ergänzt:

```css
	/* Eingang zum Protokoll — Messingschild am Ende des Flusses.
	   Rechtsbündig, damit das Schild an derselben Kante endet, an der das Pult
	   (ArchiveActors, .rail.pult-desk bei --x: 80) in der fixen Bühne dahintersteht:
	   gleiche Flucht, gleiches Material. Das Möbel selbst bleibt Kulisse und behält
	   pointer-events: none — der Eingang gehört in den Fluss, weil sein Ziel ein Text
	   ist und kein Ort (Übergabe §5).
	   Der Zustandswechsel ist Licht, keine Bewegung: kein transform, keine Bewegungs-
	   freigabe nötig (§0). */
	.protocol-plaque {
		display: block;
		position: relative;
		margin-left: auto;
		width: min(400px, 72%);
		padding: 0.8rem 1.05rem 0.9rem;
		border: 1px solid var(--line);
		border-left: 3px solid var(--line-strong);
		border-radius: 2px;
		background: linear-gradient(180deg, rgba(28, 22, 14, 0.94), rgba(15, 12, 8, 0.96));
		box-shadow: 0 0.5rem 1.6rem rgba(0, 0, 0, 0.5);
		text-decoration: none;
		transition:
			border-color 0.35s ease,
			background 0.35s ease,
			box-shadow 0.35s ease;
	}
	.protocol-plaque .plaque-meta {
		display: block;
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.64rem;
		letter-spacing: 0.16em;
		text-transform: uppercase;
		color: var(--muted);
		transition: color 0.35s ease;
	}
	.protocol-plaque .plaque-label {
		display: block;
		margin-top: 0.2rem;
		font-size: 1.02rem;
		line-height: 1.35;
		color: #cfc4ae;
		transition: color 0.35s ease;
	}

	/* Warmer Saum aus 250° — das ist „von rechts oben", also aus Richtung der
	   Pultleuchte. Die Gradrichtung ist nicht beliebig, sie ist die halbe Idee. */
	.protocol-plaque::after {
		content: '';
		position: absolute;
		inset: -1px;
		border-radius: 2px;
		pointer-events: none;
		opacity: 0;
		mix-blend-mode: screen;
		background: linear-gradient(250deg, rgba(255, 196, 118, 0.26), rgba(255, 176, 92, 0) 58%);
		transition: opacity 0.45s ease;
	}

	.protocol-plaque:hover,
	.protocol-plaque:focus-visible {
		border-color: var(--line-strong);
		background: linear-gradient(180deg, rgba(42, 32, 18, 0.95), rgba(21, 16, 10, 0.97));
		box-shadow:
			0 0.6rem 2rem rgba(0, 0, 0, 0.55),
			0 0 2.4rem rgba(255, 176, 92, 0.14);
	}
	.protocol-plaque:hover .plaque-label,
	.protocol-plaque:focus-visible .plaque-label {
		color: var(--ink);
	}
	.protocol-plaque:hover .plaque-meta,
	.protocol-plaque:focus-visible .plaque-meta {
		color: var(--life);
	}
	.protocol-plaque:hover::after,
	.protocol-plaque:focus-visible::after {
		opacity: 1;
	}

	/* Der Lichtwechsel allein ist als Fokusanzeige zu weich — Ring dazu. */
	.protocol-plaque:focus-visible {
		outline: 2px solid var(--line-strong);
		outline-offset: 3px;
	}

	/* Mobil trägt dasselbe Element: volle Spaltenbreite statt rechtsbündig.
	   Kein Sonderfall, keine Ausblendung — derselbe Eingang auf allen Größen. */
	@media (max-width: 1199px) {
		.protocol-plaque {
			margin-left: 0;
			width: 100%;
		}
	}
```

**Token-Vorbehalt:** `--line`, `--line-strong`, `--muted`, `--ink`, `--life` stammen aus
`:global(:root)` in `src/routes/+layout.svelte`. Prüfe, ob das Rooms-Layout eigene Namen
setzt; wenn ja, **die dortigen Namen verwenden**. Werte niemals hart einsetzen.

---

## 3 · Verifikations-Vorstufe (Pflicht, jedes Mal)

```
rm -rf site/build site/.svelte-kit && npm run build
```

Erst danach messen. Konsole ohne Chunk-Ladefehler. `vite preview` neu starten.

## 4 · Abnahmekriterien

Berichte zu jedem Punkt einzeln, mit Messwert oder Screenshot:

1. **1554 × 784 und 1280 × 800** — Schild sitzt rechtsbündig in der Fluss-Spalte, endet an
   deren rechter Kante. Nenne die gemessene rechte Kante des Schilds und die der Spalte.
2. **Hover** — Saum sichtbar, Kicker wird messingfarben, Zeile wird hell.
   **Das Schild bewegt sich nicht.** Nachweis: `getBoundingClientRect()` vor und im
   Hover-Zustand identisch.
3. **Tab** — Schild wird erreicht, Ring sichtbar, `:focus-visible` greift auch nach
   Maus-Klick nicht fälschlich.
4. **`prefers-reduced-motion: reduce`** — voll bedienbar, Zustandswechsel darf bleiben
   (kein `transform` im Spiel), nichts flackert zusätzlich.
5. **JS aus** — Link funktioniert, Schild vollständig gerendert, Datum korrekt formatiert.
6. **390 px** — volle Spaltenbreite, keine Überlappung mit dem von unten aufsteigenden Pult.
7. **`grep -rn "desk-link\|desk-passage" site/src/`** — leer.
8. **EN-Fassung** `/en/archive/` — Schild da, Datum in `en-US`, Text aus `en.js`.
9. **Bühne unberührt** — `git diff` zeigt **keine** Änderung an `ArchiveActors.svelte` und
   keine an `pointer-events` irgendwo.

## 5 · Ausdrücklich nicht

- Kein Eingriff an `ArchiveActors.svelte`, kein `pointer-events`-Sonderfall am Pult.
  Die Variante „Schild am Möbel" ist geprüft und **verworfen** — bei 1554 px liegen 190 von
  266 px des Pults unter der Fluss-Spalte (endet bei x 1300). Begründung und Diagramm im
  Mockup, Abschnitt A. Nicht neu aufrollen.
- Keine Bewegung, keine Animation, kein neues Asset, keine neue Zeichenkette.
- Kein `--no-verify`, kein Push, kein Mitcommitten des Medien-Strangs oder von
  `gremium/prompts.py`.

## 6 · Commits

```
fix(rooms): Lesetisch-Übergang zurückbauen (Revert b32df19)
feat(archive): Protokoll-Eingang als Messingschild am Ende des Flusses
```

**Committen nur auf ausdrückliche Freigabe des Stewards**, nach dem Bericht.
