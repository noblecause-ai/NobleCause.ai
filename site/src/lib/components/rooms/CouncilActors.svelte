<script>
	// The Council — zweite Ebene (Szene-Kantenprinzip, docs/szene-kantenprinzip-fuer-kimi.md):
	// N Lesepulte nehmen von UNTEN ihre Plätze ein („die Beteiligten treten auf" —
	// dieselbe Grammatik wie die Study-Akteure). N und die Beschriftung kommen aus
	// den DATEN (modelTracks — Amendment-Regel: niemals eine feste Zahl); EIN
	// Lectern-Cutout steht für alle N (pro-Modell-Kunst würde die N-Skalierung
	// brechen). KANTENPRINZIP „von unten": die Basislinie des Cutouts (88,7 % der
	// Bildhöhe) steht an bzw. unter der Viewport-Unterkante (Anschnitt ~5 % der
	// Box — die Pulte stehen in der ersten Reihe). Einfahrt per translateY
	// (1,7 s sichtbares Gleiten, 100 ms Staffelung je Pult), Rückzug vertikal
	// über die globale --retreat-Scrub (stage.js — kein eigener Mechanismus).
	// KEEP-OUT: Türachse (x≈45–56 %) und Zählmaschine (x≈42–58 %) bleiben frei —
	// flankierende Paar-Slots; bei ungeradem N steht der Mittel-Slot tiefer im
	// Raum (s 0,78), damit die Trommeln der Maschine darüber lesbar bleiben.
	// Ausnahme mit Begründung (Scout-Präzedenz): ab 1200 px belegt die fixe
	// Ergebnis-Tafel die linke Kante — die linke Flanke steht dann an der
	// Tafelkante (max() im CSS) statt auf ihrem Plate-Slot; ihr Rückzug
	// gleitet hinter die Tafel wie hinter eine Wand.
	// Ruheposition steht im pragerenderten HTML; Anfangszustände nur unter
	// html.stage-armed + no-preference; reduced-motion/No-JS = statischer
	// Endzustand (§0).
	let { t, tracks = [] } = $props();

	// Slot-Plan in Plate-Prozent (x) + Höhen-Faktor (s). Paare flankieren die
	// Mitte; bei ungeradem N zuerst der (tiefere) Mittel-Slot, dann Paare in
	// Reihenfolge; N>9: gleichmäßiger Fallback (Council-Erweiterung, generisch).
	const CENTER = { x: 50, s: 0.78 };
	const PAIRS = [
		[
			{ x: 26, s: 1 },
			{ x: 74, s: 1 }
		],
		[
			{ x: 38, s: 0.92 },
			{ x: 62, s: 0.92 }
		],
		[
			{ x: 17, s: 0.92 },
			{ x: 83, s: 0.92 }
		],
		[
			{ x: 32, s: 0.85 },
			{ x: 68, s: 0.85 }
		]
	];
	function spotsFor(n) {
		if (n <= 0) return [];
		if (n > 9) {
			return Array.from({ length: n }, (_, i) => ({ x: 17 + (66 * i) / (n - 1), s: 0.85 }));
		}
		const spots = n % 2 === 1 ? [CENTER] : [];
		for (const pair of PAIRS) {
			if (spots.length >= n) break;
			spots.push(...pair.slice(0, n - spots.length));
		}
		return spots.slice(0, n).sort((a, b) => a.x - b.x);
	}
	let spots = $derived(spotsFor(tracks.length));
	// Zuordnung stabil von links nach rechts (tracks[i] ↔ x-sortierter Slot i;
	// --i = Staffelungs-Welle von links). Gemalt wird tiefste Ebene zuerst —
	// kleinere (fernere) Pulte hinter größeren, damit Überlappung sich als
	// Staffel-Tiefe liest, nicht als Fehler.
	let assignments = $derived(
		spots
			.map((spot, xi) => ({ spot, track: tracks[xi], xi }))
			.sort((a, b) => a.spot.s - b.spot.s || a.spot.x - b.spot.x)
	);
	let role = $derived(t.council.actors.pult.role);
	const familyName = (track) => t.common.familyNames[track.family] ?? track.family;
</script>

<div class="scene2">
	{#each assignments as { spot, track, xi } (track.model)}
		<div
			class="rail pult"
			data-side={spot.x < 50 ? 'left' : 'right'}
			style="--x: {spot.x}; --s: {spot.s}; --i: {xi}"
		>
			<figure class="pult-figure">
				<img
					src="/media/actors/lectern.avif"
					alt="{track.label} ({familyName(track)}): {role}"
					width="1024"
					height="1536"
					decoding="async"
				/>
				<!-- Prise Leben: das Pult-Lämpchen flackert leise (zwei Glow-Ebenen,
				     teilerfremde Perioden, Desync je Pult über --i — wie in der Study). -->
				<span class="lamp" aria-hidden="true"
					><span class="lamp-a"></span><span class="lamp-b"></span></span
				>
				<figcaption>
					<strong>{track.label}</strong>
					<span class="gloss">{familyName(track)}</span>
					<span class="role">{role}</span>
				</figcaption>
			</figure>
		</div>
	{/each}
</div>

<style>
	.scene2 {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	/* ---- Schiene -----------------------------------------------------------
	   Dieselbe Grammatik wie die Study-Rails: die .rail trägt Position und
	   Rückzug (--retreat, schreibt stage.js als Scroll-Scrub bzw. 1 beim
	   Bühnen-Räumen), die Figur darauf die Einfahrt. Rückzug VERTIKAL (die
	   Pulte tauchen nach unten ab — Richtung der Einfahrt); die Transition
	   liegt nur auf stage-clearing, der Scrub selbst ist transitionslos. */
	.rail {
		position: fixed;
		pointer-events: none;
		transform: translateY(calc(var(--retreat, 0) * 18vh));
	}
	:global(html.stage-clearing) .rail {
		transition: transform 0.38s ease-in;
	}

	/* ---- Pult --------------------------------------------------------------
	   Höhe über --s gestaffelt (vordere Reihe größer); die Basislinie des
	   Cutouts liegt bei 88,7 % der Box — die Schiene steht um 11,3 % + ~5 %
	   Anschnitt unter der Viewport-Unterkante (erste Reihe, Kantenprinzip). */
	.pult-figure {
		position: absolute;
		left: 0;
		bottom: 0;
		height: 100%;
		margin: 0;
		transform: translateX(-50%);
		pointer-events: auto;
	}
	.pult-figure > img {
		display: block;
		height: 100%;
		width: auto;
		position: relative;
		z-index: 1;
	}
	/* Kontaktschatten an der Basislinie (88,7 % → ~11 % über der Box-Unterkante). */
	.pult-figure::before {
		content: '';
		position: absolute;
		left: 50%;
		bottom: 8%;
		width: 108%;
		height: 7%;
		transform: translateX(-50%);
		background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0) 68%);
	}

	/* ---- Lämpchen (Prise Leben) --------------------------------------------
	   Warme Glow-Ellipse über dem gemalten Schirm (Lampenmitte ≈ 16 % der
	   Bildhöhe), screen-Blend; zwei Ebenen mit teilerfremden Perioden
	   (6,7 s × 10,9 s), Desync je Pult über --i. */
	.lamp {
		position: absolute;
		z-index: 2;
		pointer-events: none;
		mix-blend-mode: screen;
		left: 38%;
		top: 8%;
		width: 24%;
		height: 16%;
	}
	.lamp > span {
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
			animation-delay: calc(var(--i, 0) * -2.3s);
		}
		.lamp-b {
			animation: flicker-b 10.9s linear infinite;
			animation-delay: calc(var(--i, 0) * -3.7s);
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.lamp-a,
		.lamp-b {
			opacity: 0.14;
		}
	}
	@keyframes flicker-a {
		0% {
			opacity: 0.16;
		}
		11% {
			opacity: 0.24;
		}
		23% {
			opacity: 0.1;
		}
		37% {
			opacity: 0.3;
		}
		49% {
			opacity: 0.14;
		}
		61% {
			opacity: 0.26;
		}
		73% {
			opacity: 0.08;
		}
		86% {
			opacity: 0.22;
		}
		100% {
			opacity: 0.16;
		}
	}
	@keyframes flicker-b {
		0% {
			opacity: 0.1;
		}
		13% {
			opacity: 0.2;
		}
		29% {
			opacity: 0.06;
		}
		43% {
			opacity: 0.24;
		}
		57% {
			opacity: 0.12;
		}
		71% {
			opacity: 0.28;
		}
		83% {
			opacity: 0.09;
		}
		100% {
			opacity: 0.1;
		}
	}

	/* Namens-Plakette: Hover-Zugabe — dieselbe Information steht im alt-Text;
	   kein Tab-Stopp auf einem nicht-interaktiven Element (StageTube-Regel).
	   ÜBER DER PULT-OBERKANTE (Runde B §4.2, wie Scout/Warden c87cb97): verankert
	   an der Oberkante des Pults (Messinglampe ≈ 13 % der Box, am AVIF gemessen),
	   z-index 2 hebt sie über das Bild (.pult-figure > img trägt z-index: 1 — die
	   Falle: sonst sticht das Bild durch den Text). Schwebende Vignette statt
	   Kasten (wie .room-plaque / die Study-Plaketten) — ein Rahmen läse über der
	   Bühne als aufgeklebtes UI. Reine Anzeige, kein Ziel für den Zeiger. */
	.pult-figure figcaption {
		position: absolute;
		left: 50%;
		bottom: auto;
		top: 13%;
		transform: translate(-50%, calc(-100% - 0.4rem));
		z-index: 2;
		width: max-content;
		max-width: 15rem;
		padding: 0.35rem 0.95rem 0.45rem;
		text-align: center;
		background: radial-gradient(ellipse 82% 94% at 50% 50%, rgba(3, 6, 7, 0.84), rgba(3, 6, 7, 0) 76%);
		text-shadow: 0 1px 7px rgba(3, 6, 7, 0.95);
		pointer-events: none;
		opacity: 0;
		transition: opacity 0.35s ease;
	}
	.pult-figure:hover figcaption {
		opacity: 1;
	}
	.pult-figure figcaption strong {
		display: block;
		color: #f0d899;
		font-size: 0.8rem;
		font-weight: 600;
		letter-spacing: 0.04em;
	}
	.pult-figure figcaption .gloss {
		display: block;
		color: #c9ab6e;
		font-size: 0.68rem;
		font-style: italic;
	}
	.pult-figure figcaption .role {
		display: block;
		margin-top: 0.2rem;
		color: #d9cfb6;
		font-size: 0.72rem;
		line-height: 1.35;
	}

	/* ---- Eintritts-Takt (0,55 s + Staffelung): Einfahrt von unten ----------
	   Einheitlich vertikal (alle Viewports): 1,7 s sichtbares Gleiten,
	   100 ms Staffelung je Pult über --i. Spielt bei fresh UND arrival; nur
	   die Plate und die Tafel sind fresh-only. Endwerte in den Keyframes. */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .pult-figure {
			opacity: 0;
			transform: translate(-50%, 26vh);
		}
		:global(html.stage-armed.stage-play) .pult-figure {
			opacity: 1;
			animation: pult-in-up 1.7s cubic-bezier(0.16, 0.6, 0.24, 1) both;
			animation-delay: calc(0.55s + var(--i, 0) * 0.1s);
		}
		:global(html.stage-skip) .pult-figure {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
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

	/* ---- Positionierung: drei Fälle wie die Study-Schienen -----------------
	   x liegt in Plate-Prozent in --x, die Höhen-Staffelung in --s. */
	/* Mobil + Tablet (< 1200 px): Hochformat-Plate 2:3, cover center top —
	   Bildbreite = 66,67 svh, Bildmitte bei 50 vw. */
	.rail.pult {
		height: calc(34svh * var(--s, 1));
		bottom: calc(-0.163 * 34svh * var(--s, 1));
		left: calc(50vw + (var(--x, 50) - 50) * 0.6667svh);
	}
	@media (min-width: 1200px) {
		/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite
		   177,78 svh um die Mitte; Zonen in svh um 50 vw. Pult-Höhe 40 svh
		   ≈ 80 % der Türhöhe (Maßstab ist die Raumarchitektur, wie bei den
		   Study-Akteuren). */
		.rail.pult {
			height: calc(40svh * var(--s, 1));
			bottom: calc(-0.163 * 40svh * var(--s, 1));
			left: calc(50vw + (var(--x, 50) - 50) * 1.7778svh);
		}
		/* Linke Flanke: nie hinter die fixe Ergebnis-Tafel — Scout-Präzedenz
		   aus der Study: Box-L steht exakt an der Tafelkante (23,5 rem), der
		   Rückzug gleitet hinter sie wie hinter eine Wand. Halbe Box-Breite
		   = 0,3333 × Höhe (Cutout 2:3). Aufrechterhaltung der N-Symmetrie ist
		   hier bewusst zweitrangig — die Tafel belegt die linke Kante. */
		.rail.pult[data-side='left'] {
			left: max(
				calc(50vw + (var(--x, 50) - 50) * 1.7778svh),
				calc(23.5rem + 0.3333 * 40svh * var(--s, 1))
			);
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		/* Bild füllt die Breite (Ultrawide): Bildhöhe 56,25 vw ab top — Zonen
		   in vw; die Pult-Größe folgt der Bild-Skalierung (vw), die Basis
		   bleibt an der Viewport-Unterkante (erste Reihe der Bühne). */
		.rail.pult {
			height: calc(min(22.5vw, 40svh) * var(--s, 1));
			bottom: calc(-0.163 * min(22.5vw, 40svh) * var(--s, 1));
			left: calc(var(--x, 50) * 1vw);
		}
		.rail.pult[data-side='left'] {
			left: max(
				calc(var(--x, 50) * 1vw),
				calc(23.5rem + 0.3333 * min(22.5vw, 40svh) * var(--s, 1))
			);
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.pult-figure figcaption {
			transition: none;
		}
	}
</style>
