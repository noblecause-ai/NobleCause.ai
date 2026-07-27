<script>
	// The Archive — zweite Ebene: EIN Möbel, das leuchtende Pult mit der Leuchte,
	// betritt die Bühne von der RECHTEN Kante — dieselbe Grammatik wie der Warden
	// im Study (StudyActors): Schiene an der Seitenkante, horizontale Einfahrt,
	// Rückzug horizontal über --retreat (Desktop); mobil steigt es von unten
	// (Hochformat-Dramaturgie, wie der Warden mobil). Reine Kulisse, keine
	// Datenbindung; die LINKE Flanke bleibt leer (Serie-5-Kulisse mit geräumten
	// Ecken, die Ergebnis-Tafel steht frei — das Regal ist ersatzlos entfallen).
	// Lampen-Glow fährt mit. Ruheposition steht im pragerenderten HTML; Anfangs-
	// zustände nur unter html.stage-armed + no-preference; reduced-motion/No-JS =
	// statischer Endzustand (§0).
	let { t } = $props();
</script>

<div class="scene2">
	<!-- rechts: das leuchtende Pult — mit warmem Lampen-Glow, fährt von rechts ein. -->
	<div class="rail pult-desk" data-side="right" style="--x: 80; --side: 1">
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
</div>

<!-- Mobil: warmer Türschimmer am Hochformat-Plate (eigene Koordinaten). -->
<span class="door-shimmer" aria-hidden="true"></span>

<style>
	.scene2 {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	/* ---- Schiene: die .rail trägt Position + Rückzug (--retreat), die Figur die
	   Einfahrt (getrennte transforms, kein Konflikt). Rückzug mobil vertikal,
	   Desktop horizontal (--side) — dieselbe Grammatik wie die Study-Schienen.
	   --side: 1 = rechts (zieht nach rechts ab). Die Transition liegt nur auf
	   stage-clearing (der Scrub selbst ist transitionslos). */
	.rail {
		position: fixed;
		pointer-events: none;
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

	/* ---- Lampen-Glow (am Pult) --------------------------------------------
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

	/* ---- Eintritts-Takt: Einfahrt von RECHTS (wie der Warden) — Default; mobil
	   von unten (Override im <1200-Block). 1,7 s sichtbares Gleiten, Delay 0,55 s,
	   dieselbe Kurve wie actor-in-right. */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .reg-figure {
			opacity: 0;
			transform: translateX(calc(-50% + 20vw));
		}
		:global(html.stage-armed.stage-play) .reg-figure {
			opacity: 1;
			animation: pult-in-right 1.7s cubic-bezier(0.16, 0.6, 0.24, 1) 0.55s both;
		}
		:global(html.stage-skip) .reg-figure {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
		}
	}
	@keyframes pult-in-right {
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

	/* ---- Positionierung: drei Fälle wie die Study-Schienen ----------------
	   x in Plate-Prozent (--x). Fußlinie ≈ 100 % → ~5 % Anschnitt. */
	/* Mobil + Tablet (< 1200 px): Hochformat-Plate 2:3 (cover), Bildbreite 66,67 svh.
	   Rückzug VERTIKAL, Einfahrt von unten (Override unten). */
	.rail.pult-desk {
		left: calc(50vw + (var(--x, 50) - 50) * 0.6667svh);
		height: 30svh;
		bottom: calc(-0.05 * 30svh);
		transform: translateY(calc(var(--retreat, 0) * 18vh));
	}
	@media (max-width: 1199px) and (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .reg-figure {
			transform: translate(-50%, 26vh);
		}
		:global(html.stage-armed.stage-play) .reg-figure {
			animation-name: pult-in-up;
		}
	}
	@keyframes pult-in-up {
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

	@media (min-width: 1200px) {
		/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite 177,78 svh.
		   Rückzug HORIZONTAL nach rechts (--side), Einfahrt von rechts (Default). */
		.rail.pult-desk {
			left: calc(50vw + (var(--x, 50) - 50) * 1.7778svh);
			height: 38svh;
			bottom: calc(-0.05 * 38svh);
			transform: translateX(calc(var(--retreat, 0) * var(--side, 1) * 13vw));
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		/* Bild füllt die Breite (Ultrawide): Bildhöhe 56,25 vw ab top — Zonen in vw. */
		.rail.pult-desk {
			height: min(21vw, 38svh);
			bottom: calc(-0.05 * min(21vw, 38svh));
			left: calc(var(--x, 50) * 1vw);
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
