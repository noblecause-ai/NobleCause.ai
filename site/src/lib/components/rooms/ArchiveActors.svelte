<script>
	// The Archive — zweite Ebene (Szene-Kantenprinzip, wie CouncilActors/StudyActors):
	// ZWEI VERSCHIEDENE Möbel nehmen von UNTEN ihre Plätze an den unteren Ecken ein
	// (nicht zwei gleiche Kästen):
	//   rechts = das Pult mit der Leuchte (bringt eine warme, flackernde Lichtquelle
	//            mit, die einfährt — der Gewinn gegenüber einem stummen Schrank),
	//   links  = der Karteikasten (register.avif), nur einmal.
	// (Steward: Pult von rechts; die Serie-5-Kulisse hat geräumte Ecken, also kein
	//  Verdopplungskonflikt mehr mit gemaltem Möbel.)
	// REINE KULISSE, keine Datenbindung; asymmetrisch, Mitte frei (trägt Röhre/Tafel/
	// Text — Kantenprinzip). KANTENPRINZIP „von unten": die Basislinie (~100 % der
	// bbox-getrimmten Box) steht knapp unter der Viewport-Unterkante (~5 % Anschnitt).
	// Einfahrt per translateY (1,7 s Gleiten, Staffelung über --i), Rückzug vertikal
	// über die globale --retreat-Scrub (stage.js). Ruheposition steht im pragerenderten
	// HTML; Anfangszustände nur unter html.stage-armed + no-preference; reduced-motion/
	// No-JS = statischer Endzustand (§0).
	let { t } = $props();
</script>

<div class="scene2">
	<!-- rechts: das leuchtende Pult (näher, größer) — mit warmem Lampen-Glow. -->
	<div class="rail pult-desk" data-side="right" style="--x: 80; --i: 0">
		<figure class="reg-figure">
			<img
				src="/media/actors/pult-lamp.avif"
				alt={t.archive.pultAlt}
				width="1026"
				height="1148"
				decoding="async"
			/>
			<!-- Prise Leben: der Messingschirm leuchtet leise (zwei Glow-Ebenen,
			     teilerfremde Perioden — wie die Council-Pulte). -->
			<span class="lamp" aria-hidden="true"
				><span class="lamp-a"></span><span class="lamp-b"></span></span
			>
		</figure>
	</div>
	<!-- links: der Karteikasten, nur einmal. -->
	<div class="rail register" data-side="left" style="--x: 20; --i: 1">
		<figure class="reg-figure">
			<img
				src="/media/actors/register.avif"
				alt={t.archive.registerAlt}
				width="1064"
				height="1338"
				decoding="async"
			/>
		</figure>
	</div>
</div>

<!-- Mobil: warmer Türschimmer am Hochformat-Plate (eigene Koordinaten). -->
<span class="door-shimmer" aria-hidden="true"></span>

<style>
	.scene2 {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	/* ---- Schiene: dieselbe Grammatik wie die Council-Rails — die .rail trägt
	   Position und Rückzug (--retreat, stage.js), die Figur darauf die Einfahrt.
	   Rückzug VERTIKAL (die Möbel tauchen nach unten ab). ---------------------- */
	.rail {
		position: fixed;
		pointer-events: none;
		transform: translateY(calc(var(--retreat, 0) * 18vh));
	}
	:global(html.stage-clearing) .rail {
		transition: transform 0.38s ease-in;
	}

	/* ---- Möbel: bbox-getrimmter Cutout → Basislinie ≈ 100 % der Box; die
	   Schiene steht um ~5 % Anschnitt unter der Viewport-Unterkante. ---------- */
	.reg-figure {
		position: absolute;
		left: 0;
		bottom: 0;
		height: 100%;
		margin: 0;
		transform: translateX(-50%);
		pointer-events: none;
	}
	.reg-figure > img {
		display: block;
		height: 100%;
		width: auto;
		position: relative;
		z-index: 1;
	}
	/* Kontaktschatten an der Basislinie (Box-Unterkante). */
	.reg-figure::before {
		content: '';
		position: absolute;
		left: 50%;
		bottom: 1%;
		width: 104%;
		height: 6%;
		transform: translateX(-50%);
		background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0) 68%);
	}

	/* ---- Lampen-Glow (nur am Pult) ----------------------------------------
	   Warme Ellipse über dem gemalten Messingschirm (am Cutout gemessen ≈ x 60 %,
	   y 13 %), screen-Blend; zwei Ebenen mit teilerfremden Perioden. */
	.pult-desk .lamp {
		position: absolute;
		z-index: 2;
		pointer-events: none;
		mix-blend-mode: screen;
		left: 53%;
		top: 7%;
		width: 14%;
		height: 13%;
	}
	.pult-desk .lamp > span {
		position: absolute;
		inset: 0;
		background: radial-gradient(
			ellipse 50% 50% at 50% 50%,
			rgba(255, 196, 118, 0.5),
			rgba(255, 176, 92, 0.12) 55%,
			rgba(255, 176, 92, 0) 72%
		);
	}
	@media (prefers-reduced-motion: no-preference) {
		.lamp-a {
			animation: flicker-a 6.7s linear infinite;
		}
		.lamp-b {
			animation: flicker-b 10.9s linear infinite;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.lamp-a,
		.lamp-b {
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

	/* ---- Eintritts-Takt: Einfahrt von unten (wie die Pulte) ---------------- */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .reg-figure {
			opacity: 0;
			transform: translate(-50%, 26vh);
		}
		:global(html.stage-armed.stage-play) .reg-figure {
			opacity: 1;
			animation: register-in-up 1.7s cubic-bezier(0.16, 0.6, 0.24, 1) both;
			animation-delay: calc(0.55s + var(--i, 0) * 0.12s);
		}
		:global(html.stage-skip) .reg-figure {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
		}
	}
	@keyframes register-in-up {
		from {
			opacity: 0;
			transform: translate(-50%, 26vh);
		}
		22% {
			opacity: 1;
		}
		to {
			opacity: 1;
			transform: translate(-50%, 0);
		}
	}

	/* ---- Positionierung: drei Fälle wie die Council-Schienen ---------------
	   x in Plate-Prozent (--x). Das Pult ist NÄHER/GRÖSSER (§3): eigene Höhe;
	   halbe Box-Breite für die Links-Klemme = 0,447 · Höhe (Pult 1026×1148 ≈ 0,894).
	   Register-Höhe kleiner (1064×1338 ≈ 0,795). Fußlinie ≈ 100 % → ~5 % Anschnitt. */
	/* Mobil + Tablet (< 1200 px): Hochformat-Plate 2:3 (cover), Bildbreite 66,67 svh. */
	.rail.pult-desk,
	.rail.register {
		left: calc(50vw + (var(--x, 50) - 50) * 0.6667svh);
	}
	.rail.pult-desk {
		height: 30svh;
		bottom: calc(-0.05 * 30svh);
	}
	.rail.register {
		height: 28svh;
		bottom: calc(-0.05 * 28svh);
	}
	@media (min-width: 1200px) {
		/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite 177,78 svh. */
		.rail.pult-desk,
		.rail.register {
			left: calc(50vw + (var(--x, 50) - 50) * 1.7778svh);
		}
		.rail.pult-desk {
			height: 38svh;
			bottom: calc(-0.05 * 38svh);
		}
		.rail.register {
			height: 34svh;
			bottom: calc(-0.05 * 34svh);
		}
		/* Linke Flanke (jetzt der Karteikasten): nie hinter die fixe Ergebnis-Tafel
		   (23,5 rem); halbe Box-Breite = 0,3975 · Höhe (Register 1064×1338). */
		.rail.register[data-side='left'] {
			left: max(
				calc(50vw + (var(--x, 50) - 50) * 1.7778svh),
				calc(23.5rem + 0.3975 * 34svh)
			);
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		/* Bild füllt die Breite (Ultrawide): Bildhöhe 56,25 vw ab top — Zonen in vw. */
		.rail.pult-desk {
			height: min(21vw, 38svh);
			bottom: calc(-0.05 * min(21vw, 38svh));
			left: calc(var(--x, 50) * 1vw);
		}
		.rail.register {
			height: min(19vw, 34svh);
			bottom: calc(-0.05 * min(19vw, 34svh));
			left: calc(var(--x, 50) * 1vw);
		}
		.rail.register[data-side='left'] {
			left: max(calc(var(--x, 50) * 1vw), calc(23.5rem + 0.3975 * min(19vw, 34svh)));
		}
	}

	/* ---- Mobiler Türschimmer (Hochformat-Plate) --------------------------- */
	.door-shimmer {
		display: none;
	}
	@media (max-width: 1199px) {
		.door-shimmer {
			display: block;
			position: fixed;
			z-index: 0;
			/* Tür sitzt am „right top"-Crop bei ≈ 27 vw, y ≈ 32–60 %. */
			left: calc(27vw - 5svh);
			top: 32svh;
			width: 10svh;
			height: 28svh;
			background: radial-gradient(
				ellipse 50% 50% at 50% 46%,
				rgba(255, 196, 118, 0.42),
				rgba(255, 176, 92, 0) 70%
			);
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
		50% {
			opacity: 0.2;
		}
	}
</style>
