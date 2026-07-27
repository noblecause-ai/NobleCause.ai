<script>
	// The Archive — zweite Ebene (Szene-Kantenprinzip, wie CouncilActors/StudyActors):
	// zwei Karteikästen nehmen von UNTEN ihre Plätze an den unteren Ecken ein.
	// ANDERS als die Council-Pulte: KEINE Datenbindung — ein Karteikasten bedeutet
	// keine Sitzung, er ENTHÄLT Sitzungen (die Zahl der Sitzungen steht mit Datum am
	// Regal). Reine Kulisse, feste Zahl, NUR Randpaar (kein Mittelslot): die Mitte
	// trägt Röhre, Tafel und Text (Kantenprinzip). Ein Register-Cutout steht für beide.
	// KANTENPRINZIP „von unten": die Basislinie (~100 % der bbox-getrimmten Box) steht
	// knapp unter der Viewport-Unterkante (~5 % Anschnitt). Einfahrt per translateY
	// (1,7 s Gleiten, 100 ms Staffelung), Rückzug vertikal über die globale
	// --retreat-Scrub (stage.js). Ruheposition steht im pragerenderten HTML;
	// Anfangszustände nur unter html.stage-armed + no-preference; reduced-motion/
	// No-JS = statischer Endzustand (§0).
	let { t } = $props();

	// Zwei feste Randslots, Mitte frei. x in Plate-Prozent, s = Höhen-Faktor.
	const spots = [
		{ x: 19, s: 1, i: 0 },
		{ x: 81, s: 1, i: 1 }
	];
</script>

<div class="scene2">
	{#each spots as spot (spot.x)}
		<div
			class="rail register"
			data-side={spot.x < 50 ? 'left' : 'right'}
			style="--x: {spot.x}; --s: {spot.s}; --i: {spot.i}"
		>
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
	{/each}
</div>

<!-- Mobil: warmer Türschimmer am Hochformat-Plate (eigene Koordinaten — die
     Study-Werte passen nicht). Immer-an-Ambiente, kein Hover, klickdurchlässig. -->
<span class="door-shimmer" aria-hidden="true"></span>

<style>
	.scene2 {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	/* ---- Schiene: dieselbe Grammatik wie die Council-Rails — die .rail trägt
	   Position und Rückzug (--retreat, stage.js), die Figur darauf die Einfahrt.
	   Rückzug VERTIKAL (die Kästen tauchen nach unten ab). ------------------- */
	.rail {
		position: fixed;
		pointer-events: none;
		transform: translateY(calc(var(--retreat, 0) * 18vh));
	}
	:global(html.stage-clearing) .rail {
		transition: transform 0.38s ease-in;
	}

	/* ---- Karteikasten ------------------------------------------------------
	   bbox-getrimmter Cutout → Basislinie ≈ 100 % der Box; die Schiene steht
	   um ~5 % Anschnitt unter der Viewport-Unterkante (erste Reihe). */
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
	   x in Plate-Prozent (--x), Höhen-Staffelung (--s). Register-Cutout 1064×1338
	   (Verhältnis ≈ 0,795) → halbe Box-Breite = 0,3975 × Höhe. */
	/* Mobil + Tablet (< 1200 px): Hochformat-Plate 2:3 (cover), Bildbreite
	   = 66,67 svh, Bildmitte bei 50 vw. Kästen kleiner, damit die Mitte frei bleibt. */
	.rail.register {
		height: calc(28svh * var(--s, 1));
		bottom: calc(-0.05 * 28svh * var(--s, 1));
		left: calc(50vw + (var(--x, 50) - 50) * 0.6667svh);
	}
	@media (min-width: 1200px) {
		/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite 177,78 svh
		   um die Mitte; Zonen in svh um 50 vw. */
		.rail.register {
			height: calc(34svh * var(--s, 1));
			bottom: calc(-0.05 * 34svh * var(--s, 1));
			left: calc(50vw + (var(--x, 50) - 50) * 1.7778svh);
		}
		/* Linke Flanke: nie hinter die fixe Ergebnis-Tafel (23,5 rem) — wie die
		   Scout-/Pult-Präzedenz; halbe Box-Breite = 0,3975 × Höhe. */
		.rail.register[data-side='left'] {
			left: max(
				calc(50vw + (var(--x, 50) - 50) * 1.7778svh),
				calc(23.5rem + 0.3975 * 34svh * var(--s, 1))
			);
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		/* Bild füllt die Breite (Ultrawide): Bildhöhe 56,25 vw ab top — Zonen in vw. */
		.rail.register {
			height: calc(min(19vw, 34svh) * var(--s, 1));
			bottom: calc(-0.05 * min(19vw, 34svh) * var(--s, 1));
			left: calc(var(--x, 50) * 1vw);
		}
		.rail.register[data-side='left'] {
			left: max(
				calc(var(--x, 50) * 1vw),
				calc(23.5rem + 0.3975 * min(19vw, 34svh) * var(--s, 1))
			);
		}
	}

	/* ---- Mobiler Türschimmer (Hochformat-Plate) ---------------------------
	   Warme Öffnung an der gemalten Tür; Koordinaten am archive-portrait-Plate
	   gemessen. Nur < 1200 px (Desktop hat den Hotspot-Crossfade). */
	.door-shimmer {
		display: none;
	}
	@media (max-width: 1199px) {
		.door-shimmer {
			display: block;
			position: fixed;
			z-index: 0;
			/* Am Hochformat-Plate (bgPosMobile „right top") sitzt die gemalte Tür
			   links der Mitte: Bildmitte-Tür (x ≈ 40–59 % von 1024) landet nach dem
			   Right-Crop bei ≈ 27 vw; vertikal y ≈ 32–60 %. Am Plate gemessen. */
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
