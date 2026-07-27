<script>
	// The Study — zweite Ebene (§3 der Dramaturgie): Wolkenzug im Mondfenster
	// (Ambient, Zwei-Achsen-Drift 13 s/20 s — teilerfremde Perioden, kein
	// Pendel-Sync, nur transform; reduced-motion/no-JS = statischer
	// Stand), die beiden Akteure The Scout / The Warden als freigestellte
	// Ebenen auf SCHIENEN (.rail: Einfahrt 1,7 s sichtbares Gleiten, Rückzug
	// per --retreat beim Scrollen bzw. vor der Türfahrt — die Schiene ist
	// generisch: jedes weitere Seitenelement (Pflanze, Raumteil) bekommt
	// einfach dieselbe .rail) und eine Prise Leben als Lampenflackern.
	// KANTENPRINZIP (docs/szene-kantenprinzip-fuer-kimi.md, 24.07.): bewegliche
	// Elemente berühren/schneiden einen Viewport-Rand und verlassen die Szene
	// über genau diese Kante (--side) — Scout links, Warden rechts. Ausnahme
	// mit Begründung: auf ≥1200 px belegt die fixe Ergebnis-Tafel die linke
	// Kante (L 21–395 px, T 264–B 556–813 px, CDP-Messung) — ein links
	// verankerter Scout (Box ~300 px breit) läge zu ~95 % hinter ihr. Dort
	// bleibt der Scout an der TAFELkante verankert (sein Rückzug gleitet
	// hinter die Tafel wie hinter eine Wand); volle Kante hat er <1200 px.
	// Der Scout ist seit 24.07. der SITZENDE am Schreibtisch (Nachtrag,
	// ASSETS.md) — Fußlinie des Cutouts bei 82 % der Bildhöhe, darum steht
	// die Schiene um 18 % der Bildhöhe tiefer als die Box-Unterkante.
	// Alles steht im pragerenderten HTML im Endzustand; Anfangszustände nur
	// unter html.stage-armed (JS) + no-preference. Positionen folgen demselben
	// Zwei-Fälle-Modell wie der Tür-Hotspot (Plate 16:9 quer, center top;
	// Hochformat-Plate 2:3 unter 1200 px) — Prozentzonen der Plates, rem-frei
	// nur hier, weil die Ebene AN das Plate gebunden ist (Bühne, kein Text).
	import { formatDate } from '$lib/format.js';
	// Sitzinhaber & Warden-Entscheid aus den Daten (wörtlich durchgereicht):
	// Scout-Sitz = Modell des letzten Research-Laufs, Warden-Sitz = session.led_by.
	// Beide sind aktuell dieselbe Instanz (claude-fable-5) — zwei Ämter, ein Sitz,
	// offen gezeigt. Eine Vertretung (deputationNote) wird angezeigt, nicht geglättet.
	let { t, lastResearch = null, ledBy = null } = $props();
	const pillars = ['A', 'B', 'C', 'D'];
</script>

<div class="scene2" aria-hidden="false">
	<!-- Mobiler Dauer-Schimmer: unter 1200 px gibt es keinen Tür-Hotspot und
	     kein Hover — die angelehnte Tür (im Hochformat-Plate gebacken) atmet
	     stattdessen leise warm, damit sie als Wegweiser lesbar bleibt. -->
	<span class="door-shimmer" aria-hidden="true"></span>

	<!-- Wolkenzug im Fenster: screen-Blend über dem gemalten Mond; zwei
	     verschachtelte Drift-Achsen mit teilerfremden Perioden (13 s × 20 s)
	     — die Achsen pendeln versetzt, ohne je synchron zu schlagen.
	     WICHTIG: beide Achsen sind inset:0-Ebenen — translate-Prozente
	     brauchen eine Bezugsgrösse, sonst driftet die Achse gegen 0 px. -->
	<div class="clouds" aria-hidden="true">
		<div class="drift-x">
			<div class="drift-y">
				<img src="/media/ambient/clouds-study.avif" alt="" width="384" height="512" loading="lazy" decoding="async" />
			</div>
		</div>
	</div>

	<!-- Schiene + Akteur: die .rail trägt Position und Rückzug (--retreat),
	     die Figur darauf die Einfahrt (transform getrennt, kein Konflikt). -->
	<div class="rail scout" style="--side: -1">
		<figure class="actor scout">
			<img src="/media/actors/scout.avif" alt="{t.study.actors.scout.name}: {t.study.actors.scout.sentence}" width="935" height="1168" decoding="async" />
			<!-- Boden-Reflexion: Diele ist spiegelnd, der Raum trägt die Figur. -->
			<span class="reflection" aria-hidden="true"><img src="/media/actors/scout.avif" alt="" width="935" height="1168" decoding="async" loading="lazy" /></span>
			<!-- Prise Leben: das Schirmlicht flackert leise (zwei verschachtelte
			     Glow-Ebenen, 6,7 s × 10,9 s — wirkt wie eine echte Flamme). -->
			<span class="lamp lamp-desk" aria-hidden="true"><span class="lamp-a"></span><span class="lamp-b"></span></span>
			<span class="lamp lamp-screen" aria-hidden="true"><span class="lamp-c"></span></span>
			<figcaption>
				<!-- Sitzzeile aus den Daten. Bei Vertretung (deputationNote vorhanden)
				     kurzes Label „In Vertretung: {model}" statt „Aktuell:" — der volle
				     Wortlaut steht im Rekord (journal/[id]), die Plakette zitiert ihn
				     nicht (115-px-Budget, kein Link/pointer-events). -->
				<span class="cap-name"
					><strong>{t.study.actors.scout.name}</strong>{#if lastResearch?.model}<span class="sitz">
							· {lastResearch.deputationNote
								? t.study.actors.deputyPrefix
								: t.study.actors.sitzPrefix}
							{lastResearch.model}</span
						>{/if}</span
				>
				<span class="cap-body"
					><img
						class="sigil"
						src="/media/process/process-question-display.avif"
						alt=""
						width="30"
						height="30"
						decoding="async"
					/>{t.study.actors.scout.sentence}</span
				>
				<!-- Bereichsreihe: TRÄGT die vier Bereiche (nicht dekorativ) → alt=label. -->
				<span class="pillars">
					{#each pillars as k}<img
							src={t.pillars[k].src}
							alt={t.pillars[k].label}
							width="30"
							height="30"
							decoding="async"
							loading="lazy"
						/>{/each}
				</span>
			</figcaption>
		</figure>
	</div>
	<div class="rail warden" style="--side: 1">
		<figure class="actor warden">
			<img src="/media/actors/warden.avif" alt="{t.study.actors.warden.name}: {t.study.actors.warden.sentence}" width="1024" height="1536" decoding="async" />
			<span class="reflection" aria-hidden="true"><img src="/media/actors/warden.avif" alt="" width="1024" height="1536" decoding="async" loading="lazy" /></span>
			<span class="lamp lamp-desk" aria-hidden="true"><span class="lamp-a"></span><span class="lamp-b"></span></span>
			<figcaption>
				<span class="cap-name"
					><strong>{t.study.actors.warden.name}</strong>{#if ledBy?.model}<span class="sitz">
							· {t.study.actors.sitzPrefix} {ledBy.model}</span
						>{/if}</span
				>
				<span class="cap-body"
					><img
						class="sigil"
						src="/media/process/process-evidence-display.avif"
						alt=""
						width="30"
						height="30"
						decoding="async"
					/>{t.study.actors.warden.sentence}</span
				>
				<!-- Warden-Entscheid aus den Daten (convene/date des letzten Laufs). -->
				{#if lastResearch?.date}<span class="last"
						>{t.study.actors.warden.lastPrefix}
						{lastResearch.convene
							? t.study.actors.warden.convened
							: t.study.actors.warden.notConvened} ·
						<time datetime={lastResearch.date}>{formatDate(lastResearch.date, t.lang)}</time></span
					>{/if}
			</figcaption>
		</figure>
	</div>
</div>

<style>
	.scene2 {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	/* ---- Mobiler Tür-Schimmer (Dauer-Zustand statt Hover) ------------------
	   Hochformat-Plate 2:3, cover center top → Bildbreite 66,67 svh um 50 vw;
	   die warme Türöffnung sitzt bei x ~44–58 %, y ~24–63 % der Plate.
	   position:fixed + z-index:0 wie die Wolkenebene (Befund 2). */
	.door-shimmer {
		display: none;
	}
	@media (max-width: 1199px) {
		.door-shimmer {
			display: block;
			position: fixed;
			z-index: 0;
			left: calc(50vw - 4.7svh);
			top: 24svh;
			width: 9.4svh;
			height: 39svh;
			background: radial-gradient(ellipse 50% 50% at 50% 46%, rgba(255, 196, 118, 0.42), rgba(255, 176, 92, 0) 70%);
			mix-blend-mode: screen;
			opacity: 0.14;
			pointer-events: none;
		}
	}
	@media (max-width: 1199px) and (prefers-reduced-motion: no-preference) {
		.door-shimmer {
			animation: door-shimmer 7.5s ease-in-out infinite;
		}
	}
	@keyframes door-shimmer {
		0%,
		100% {
			opacity: 0.1;
		}
		46% {
			opacity: 0.3;
		}
		58% {
			opacity: 0.24;
		}
	}

	/* ---- Wolkenzug (Ambient) ---------------------------------------------
	   Fenster-Zonen der Plates (quer: Glas x 75–89 %, y 14–60 %; hoch:
	   x 79–93 %, y 21–50 %) — Overscan (−16 %/−10 %, 132 % × 120 %) im
	   Container mit overflow:hidden, damit die Drift (±12 %/±6 %) nie den
	   Rand zeigt.
	   position:fixed + z-index:0 — dieselbe Ebene wie .room-bg: die Wolke
	   haftet am Fenster der fixen Szene, statt mit dem Hero wegzuscrollen
	   (Befund 2); Vorfahren müssen dafür transform-frei bleiben. */
	.clouds {
		position: fixed;
		z-index: 0;
		overflow: hidden;
		mix-blend-mode: screen;
		opacity: 0.5;
	}
	/* Beide Drift-Achsen MÜSSEN die volle Container-Grösse haben — Prozent-
	   translates beziehen sich auf die eigene Box; ohne inset:0 ist die
	   (absolute) Bild-Box aus dem Fluss und die Achse driftet gegen 0 px. */
	.drift-x,
	.drift-y {
		position: absolute;
		inset: 0;
	}
	.clouds img {
		position: absolute;
		/* Overscan deckt die Ruhe-Amplitude ±12 %/±6 % mit Rand ab, damit die
		   Drift nie den Bildrand ins Fenster zieht. */
		left: -16%;
		top: -10%;
		width: 132%;
		height: 120%;
		object-fit: cover;
	}
	@media (prefers-reduced-motion: no-preference) {
		/* Ruhewert nach Diagnose (2026-07-24): sichtbar, aber unaufdringlich.
		   Teilerfremde Perioden (13s × 20s) → kein Pendel-Sync. Halbe Intensität
		   des Test-Werts (6s/10s, ±16/±8). */
		.drift-x {
			animation: drift-x 13s ease-in-out infinite alternate;
		}
		.drift-y {
			animation: drift-y 20s ease-in-out infinite alternate;
		}
	}
	@keyframes drift-x {
		from {
			transform: translateX(-12%);
		}
		to {
			transform: translateX(12%);
		}
	}
	@keyframes drift-y {
		from {
			transform: translateY(-6%);
		}
		to {
			transform: translateY(6%);
		}
	}

	/* ---- Schienen ---------------------------------------------------------
	   Generisch für N Seitenelemente: Position (left/bottom/height) + Rückzug
	   über --retreat (0..1, schreibt stage.js als Scroll-Scrub bzw. 1 beim
	   Bühnen-Räumen vor der Türfahrt). --side: -1 = Element links (zieht
	   nach links ab), +1 = rechts. Der Scrub ist transitionslos (direkte
	   Kopplung); nur beim Räumen (html.stage-clearing) gleitet die Schiene
	   weich — darum liegt die Transition ausschliesslich auf dieser Klasse. */
	.rail {
		position: fixed;
		pointer-events: none;
	}
	:global(html.stage-clearing) .rail {
		transition: transform 0.38s ease-in;
	}

	/* ---- Akteure -----------------------------------------------------------
	   Bodenlinie ~82 % der Plate (Füße auf der gemalten Diele), Höhe ~52 %
	   (Figur ≈ 80 % der Türhöhe — Maßstab ist die Raumarchitektur). */
	.actor {
		position: absolute;
		left: 0;
		bottom: 0;
		height: 100%;
		margin: 0;
		transform: translateX(-50%);
		pointer-events: auto;
	}
	.actor > img {
		display: block;
		height: 100%;
		width: auto;
		position: relative;
		z-index: 1;
	}
	/* Kontaktschatten: weiche Ellipse unter dem Tisch — Erdung auf der Diele. */
	.actor::before {
		content: '';
		position: absolute;
		left: 50%;
		bottom: -1.5%;
		width: 112%;
		height: 9%;
		transform: translateX(-50%);
		background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(0, 0, 0, 0.62), rgba(0, 0, 0, 0) 68%);
	}
	/* Sitzender Scout: Fuß-/Tischbein-Linie liegt bei 82 % der Box (unter ihr
	   18 % transparent) — der Schatten gehört an die Fußlinie, nicht an die
	   Box-Unterkante. */
	.actor.scout::before {
		bottom: 16.5%;
	}
	/* Warden: Fußlinie ebenfalls über der Box-Unterkante (AVIF-Alpha im Browser
	   gemessen: 0,81 → below ≈ 19 %). Schatten auf die Fußlinie, nicht an die
	   Box-Unterkante — analog zum Scout. */
	.actor.warden::before {
		bottom: 17.5%;
	}
	/* Reflexion auf der spiegelnden Diele: gespiegelte Kopie unter den Füßen,
	   schnell ausklingend. */
	.reflection {
		position: absolute;
		top: 100%;
		left: 0;
		width: 100%;
		height: 100%;
		overflow: visible;
		pointer-events: none;
	}
	.reflection img {
		display: block;
		height: 100%;
		width: auto;
		transform: scaleY(-1);
		transform-origin: top;
		opacity: 0.16;
		mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.9), transparent 42%);
		-webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.9), transparent 42%);
	}

	/* ---- Lampenflackern (Prise Leben) --------------------------------------
	   Warme Glow-Ellipse über dem gemalten Schirm, screen-Blend. Zwei Ebenen
	   mit unregelmässigen Keyframes und teilerfremden Perioden (6,7 s ×
	   10,9 s) — die Überlagerung wirkt wie Flammenzittern, nicht wie Loop.
	   Positionen = % der Cutout-Box (vermessen am Alpha-Master). */
	.lamp {
		position: absolute;
		z-index: 2;
		pointer-events: none;
		mix-blend-mode: screen;
	}
	.lamp > span {
		position: absolute;
		inset: 0;
	}
	.lamp-desk > span {
		background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(255, 196, 118, 0.5), rgba(255, 176, 92, 0.12) 55%, rgba(255, 176, 92, 0) 72%);
	}
	.scout .lamp-desk {
		left: 49%;
		top: 23%;
		width: 22%;
		height: 16%;
	}
	.warden .lamp-desk {
		left: 9%;
		top: 24%;
		width: 32%;
		height: 20%;
	}
	/* Der Monitor des Scouts glüht kühl und atmet noch langsamer (13,7 s). */
	.scout .lamp-screen {
		left: 60%;
		top: 32%;
		width: 23%;
		height: 16%;
	}
	.lamp-screen > span {
		background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(126, 196, 255, 0.34), rgba(110, 176, 236, 0.08) 58%, rgba(110, 176, 236, 0) 74%);
	}
	@media (prefers-reduced-motion: no-preference) {
		.lamp-a {
			animation: flicker-a 6.7s linear infinite;
		}
		.lamp-b {
			animation: flicker-b 10.9s linear infinite;
		}
		.lamp-c {
			animation: breathe-c 13.7s ease-in-out infinite;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.lamp-a,
		.lamp-b,
		.lamp-c {
			opacity: 0.14;
		}
	}
	@keyframes flicker-a {
		0% { opacity: 0.16; }
		11% { opacity: 0.24; }
		23% { opacity: 0.1; }
		37% { opacity: 0.3; }
		49% { opacity: 0.14; }
		61% { opacity: 0.26; }
		73% { opacity: 0.08; }
		86% { opacity: 0.22; }
		100% { opacity: 0.16; }
	}
	@keyframes flicker-b {
		0% { opacity: 0.1; }
		13% { opacity: 0.2; }
		29% { opacity: 0.06; }
		43% { opacity: 0.24; }
		57% { opacity: 0.12; }
		71% { opacity: 0.28; }
		83% { opacity: 0.09; }
		100% { opacity: 0.1; }
	}
	@keyframes breathe-c {
		0%, 100% { opacity: 0.1; }
		50% { opacity: 0.3; }
	}
	/* Namens-Plakette: Hover-Zugabe (Maus), dieselbe Information steht im
	   alt-Text und im DOM — kein Tab-Stopp auf einem nicht-interaktiven
	   Element (StageTube-Regel).
	   ÜBER DER KOPFLINIE (Auftrag A3/A4): früher hing sie unter dem Kasten und
	   ragte ins schmale Röhren-Band — brach bei 1440×700. Jetzt sitzt sie
	   VOLLSTÄNDIG über der Kopflinie (--head, per Canvas-Alpha-Scan am AVIF
	   gemessen), z-index 2 hebt sie über das Bild (img z-index 1) — kein Bildteil
	   davor, kein Haar durch den Text. Bleibt im Figurband, kann per Konstruktion
	   nicht mit Masthead/Tafel kollidieren (kein clamp()). Schwebende Vignette
	   statt opaker Kasten (wie .room-plaque, StageHero) — ein Rahmen läse über
	   der Vertäfelung als aufgeklebtes UI. Horizontal: zwei eingemessene Werte je
	   Akteur (keine --side-Formel, die ruhigen Flächen liegen unsymmetrisch). */
	.actor figcaption {
		position: absolute;
		left: 50%;
		bottom: auto;
		top: calc(var(--head, 0.18) * 100%);
		transform: translate(-50%, calc(-100% - 0.4rem));
		z-index: 2;
		width: max-content;
		max-width: 17rem;
		padding: 0.35rem 0.95rem 0.45rem;
		text-align: center;
		background: radial-gradient(ellipse 82% 94% at 50% 50%, rgba(3, 6, 7, 0.84), rgba(3, 6, 7, 0) 76%);
		text-shadow: 0 1px 7px rgba(3, 6, 7, 0.95);
		/* Die Plakette liegt im Tür-Hotspot (§3.4) — nie Hotspot oder :hover-
		   Türöffnung blockieren. Reine Anzeige, kein Ziel für den Zeiger. */
		pointer-events: none;
		opacity: 0;
		transition: opacity 0.35s ease;
	}
	/* Scout (links verankert): Kopf bei ~41 % der Box, innen Lampe/Bildschirm
	   (unruhig), über dem Kopf ruhige Vertäfelung → über den Kopf, leicht nach
	   aussen (links). */
	/* Scout ist per Kantenprinzip an der Tafelkante verankert — links ihrer Box
	   liegt die Ergebnis-Tafel. Die Plakette muss daher nach RECHTS, über die
	   dunkle Tür-Vertäfelung (wohin die Scout ohnehin blickt), sonst verschwindet
	   sie bei schmaleren Breiten hinter der Tafel (N5). */
	.actor.scout figcaption {
		--head: 0.177;
		left: 79%;
	}
	/* Warden (rechts verankert): Kopf bei ~68 % der Box, innen ruhige Wand, über
	   dem Kopf das helle Fenster (unruhig) → schräg über den Kopf nach innen
	   (links, weg vom Fenster). */
	.actor.warden figcaption {
		--head: 0.161;
		left: 14%;
	}
	.actor:hover figcaption {
		opacity: 1;
	}
	/* Plakette-Innenleben (Auftrag §3): Namens-/Sitzzeile, Karten-Sigel + Satz,
	   darunter die vier Bereichsembleme (Scout) bzw. der Warden-Entscheid.
	   Höhe ist ~115/103 px (Steward akzeptiert: „vollständig über der Kopflinie"
	   hält bei 1280×720 und 1440×700; 1200×605 kommt praktisch nicht vor).
	   STELLSCHRAUBE bei Höhennot: die Sitzzeile ist bereits in der Namenszeile;
	   dann den Satz kürzen — NIE die Emblemreihe verkleinern (sie ist der Grund
	   dieser Fassung, §3.2). */
	.actor figcaption .cap-name {
		display: block;
		line-height: 1.2;
	}
	.actor figcaption strong {
		color: #f0d899;
		font-size: 0.8rem;
		font-weight: 600;
		letter-spacing: 0.04em;
	}
	.actor figcaption .sitz {
		color: #b7a67e;
		font-size: 0.68rem;
	}
	.actor figcaption .cap-body {
		display: block;
		margin-top: 0.15rem;
		color: #d9cfb6;
		font-size: 0.72rem;
		line-height: 1.28;
	}
	/* Karten-Sigel vor dem Satz — dieselbe Datei wie die Tube (Wiedererkennung),
	   dekorativ (wiederholt den Satz) → alt="". */
	.actor figcaption .sigil {
		display: inline-block;
		vertical-align: -0.35em;
		width: 1.5rem;
		height: 1.5rem;
		margin-right: 0.4rem;
		border-radius: 50%;
		border: 1px solid rgba(190, 139, 58, 0.6);
		background: #080b0c;
		object-fit: cover;
	}
	/* Bereichsreihe bei ihren richtigen 1,9 rem — nicht verkleinern (§3.2). */
	.actor figcaption .pillars {
		display: flex;
		justify-content: center;
		gap: 0.45rem;
		margin-top: 0.3rem;
	}
	.actor figcaption .pillars img {
		width: 1.9rem;
		height: 1.9rem;
		border-radius: 50%;
		border: 1px solid rgba(190, 139, 58, 0.6);
		background: #080b0c;
		object-fit: cover;
	}
	.actor figcaption .last {
		display: block;
		margin-top: 0.35rem;
		color: #c9b98f;
		font-size: 0.68rem;
		letter-spacing: 0.02em;
	}

	/* Eintritts-Takt 2 (0,55–2,3 s): Schienen-Einfahrt — Scout von links,
	   Warden von rechts, 1,7 s SICHTBARES Gleiten (die Figur blendet in den
	   ersten 22 % ein und fährt dann sichtbar auf ihren Platz — wie auf
	   Schienen, nicht wie ein Fade). Spielt bei fresh UND arrival; nur die
	   Plate und die Tafel sind fresh-only. Endwerte explizit in den
	   Keyframes. Desktop gleitet seitlich, Mobil steigt von unten (vertikale
	   Dramaturgie des Hochformats). */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .actor.scout {
			opacity: 0;
			transform: translateX(calc(-50% - 20vw));
		}
		:global(html.stage-armed) .actor.warden {
			opacity: 0;
			transform: translateX(calc(-50% + 20vw));
		}
		:global(html.stage-armed.stage-play) .actor {
			opacity: 1;
			animation-duration: 1.7s;
			animation-timing-function: cubic-bezier(0.16, 0.6, 0.24, 1);
			animation-delay: 0.55s;
			animation-fill-mode: both;
		}
		:global(html.stage-armed.stage-play) .actor.scout {
			animation-name: actor-in-left;
		}
		:global(html.stage-armed.stage-play) .actor.warden {
			animation-name: actor-in-right;
		}
		:global(html.stage-skip) .actor {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
		}
	}
	@keyframes actor-in-left {
		from {
			opacity: 0;
			transform: translateX(calc(-50% - 20vw));
		}
		22% {
			opacity: 1;
		}
		to {
			opacity: 1;
			transform: translateX(-50%);
		}
	}
	@keyframes actor-in-right {
		from {
			opacity: 0;
			transform: translateX(calc(-50% + 20vw));
		}
		22% {
			opacity: 1;
		}
		to {
			opacity: 1;
			transform: translateX(-50%);
		}
	}

	/* ---- Positionierung: drei Fälle wie der Tür-Hotspot ------------------- */
	/* Mobil + Tablet (< 1200 px): Hochformat-Plate 2:3, cover, center top —
	   Bildbreite = 66,67 svh, Bildmitte bei 50 vw. KANTENPRINZIP: beide
	   Akteure voll am Viewport-Rand verankert (die Tafel fliesst hier im
	   Dokument und belegt keine Kante) — Scout Box-L −2 svh (Anschnitt
	   Stuhl), Warden Box-R +1,5 svh. Füße auf der Diele-Linie 24 svh; der
	   sitzende Scout (Füße bei 82 % der Box) steht mit der Schiene um 18 %
	   seiner Höhe tiefer. Wolken im Fenster (x 78–95 %, y 21–52 % der
	   Plate). Rückzug VERTIKAL (Elemente tauchen nach unten ab — dieselbe
	   Richtung wie die Einfahrt). */
	.rail {
		height: 33svh;
		bottom: 24svh;
		transform: translateY(calc(var(--retreat, 0) * 16vh));
	}
	.rail.scout {
		bottom: 18svh;
		left: 11.2svh;
	}
	.rail.warden {
		/* Diele 24svh (= Basis-bottom, wie beim Scout); Fußlinie 19 % über der
		   Box-Unterkante → Box um 0,19·33svh tiefer, Füße auf der Diele. */
		bottom: 17.73svh;
		left: calc(100vw - 9.5svh);
	}
	.clouds {
		left: calc(50vw + 18.67svh);
		top: 21svh;
		width: 11.33svh;
		height: 31svh;
	}
	@media (max-width: 1199px) and (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .actor.scout,
		:global(html.stage-armed) .actor.warden {
			opacity: 0;
			transform: translate(-50%, 22vh);
		}
		:global(html.stage-armed.stage-play) .actor.scout,
		:global(html.stage-armed.stage-play) .actor.warden {
			animation-name: actor-in-up;
		}
	}
	@keyframes actor-in-up {
		from {
			opacity: 0;
			transform: translate(-50%, 22vh);
		}
		22% {
			opacity: 1;
		}
		to {
			opacity: 1;
			transform: translate(-50%, 0);
		}
	}

	@media (min-width: 1200px) {
		/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite
		   177,78 svh um die Mitte; Zonen in svh um 50 vw. KANTENPRINZIP:
		   Warden an der RECHTEN Viewport-Kante (Box-R +2 svh Anschnitt);
		   Scout-Ausnahme mit Begründung: die fixe Ergebnis-Tafel belegt
		   hier die linke Kante (L 21–R 397 px), ein links verankerter
		   Scout läge fast vollständig hinter ihr — darum steht seine Box
		   mit Box-L = 23,5 rem exakt an der Tafelkante (sein Rückzug
		   gleitet hinter die Tafel wie hinter eine Wand). Sitzend: 45 svh
		   (stehende Präsenz-Achse wie 52 svh beim Warden), Schiene um
		   18 % der Höhe unter der Diele-Linie 18 svh.
		   Rückzug SEITLICH: Scout nach links, Warden nach rechts (--side). */
		.rail {
			height: 52svh;
			bottom: 18svh;
			transform: translateX(calc(var(--retreat, 0) * var(--side, 1) * 13vw));
		}
		.rail.scout {
			height: 45svh;
			bottom: 9.9svh;
			left: calc(23.5rem + 18svh);
		}
		.rail.warden {
			/* Diele 18svh (= Basis-bottom); Fußlinie 19 % über der Box-Unterkante
			   → bottom = 18 − 0,19·52svh, Füße auf derselben Diele wie der Scout. */
			bottom: 8.12svh;
			left: calc(100vw - 15.33svh);
		}
		.clouds {
			left: calc(50vw + 44.44svh);
			top: 14svh;
			width: 24.89svh;
			height: 46svh;
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		/* Bild füllt die Breite: Bildhöhe 56,25 vw ab top — Zonen in vw.
		   Bodenlinie geklemmt, damit Ultrawide die Füße nicht unter die
		   Faltkante zieht. Warden an der rechten Kante (Box-R +Anschnitt);
		   Scout rechts der Tafelkante (~36 vw) — volle linke Kante läge
		   auch hier hinter der fixen Tafel (Ausnahme s.o.). Schiene des
		   sitzenden Scouts um 18 % seiner Höhe unter der Bodenlinie. */
		.rail {
			height: min(29.25vw, 56svh);
			bottom: max(2svh, calc(100svh - 46.13vw));
		}
		.rail.scout {
			height: min(23.6vw, 45svh);
			bottom: calc(max(2svh, 100svh - 46.13vw) - 0.18 * min(23.6vw, 45svh));
			left: 36.5vw;
		}
		.rail.warden {
			/* Diele = Bodenlinie max(2svh, 100svh−46.13vw) (= Basis-bottom);
			   Fußlinie 19 % über der Box-Unterkante → Box um 0,19·Höhe tiefer. */
			bottom: calc(max(2svh, 100svh - 46.13vw) - 0.19 * min(29.25vw, 56svh));
			/* Box-R = 100vw + 2 svh Anschnitt, über alle Seitenverhältnisse
			   exakt: halbe Box-Breite = 0,333 × Höhe (Cutout 2:3). */
			left: calc(100vw + 2svh - min(9.75vw, 18.67svh));
		}
		.clouds {
			left: 75vw;
			top: 7.88vw;
			width: 14vw;
			height: 25.88vw;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.actor figcaption {
			transition: none;
		}
	}
</style>
