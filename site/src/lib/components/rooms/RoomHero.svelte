<script>
	// Raum-Einstieg: Szenen-Plate als FESTE Vollbild-Bildebene hinter dem scrollenden
	// Inhalt — position:fixed + 100svh + object-fit:cover (bewusst NICHT
	// background-attachment:fixed, das iOS Safari ignoriert). Das Bild steht, der
	// Inhalt zieht darüber; die Seiten-View-Transition bleibt unberührt.
	// Quellenabhängiges Laden: Querformat-Plate ab dem Desktop-Breakpoint, Hochformat
	// darunter (sceneMobile) — ohne sceneMobile gilt die Querformat-Plate überall
	// (Slot für spätere Plates, z. B. Ratssaal-Hochformat). object-position pro Raum
	// steuerbar (bgPos/bgPosMobile): Bei cover ist der sichtbare Ausschnitt damit
	// deterministic — Voraussetzung für raumspezifische Overlays in Bildeinheiten
	// (Tafel-Board und Tür-Hotspot in The Study, in svh/vw gerechnet).
	// Die Szene ist dekoratives Ambiente (alt="") — die Information tragen Plakette,
	// Overlay und Seiteninhalt.
	let {
		scene,
		sceneMobile = null,
		bgPos = 'left top',
		bgPosMobile = null,
		eyebrow,
		title,
		lead = '',
		overlay
	} = $props();
</script>

<header
	class="room-hero"
	style:--bg-pos={bgPos}
	style:--bg-pos-mobile={bgPosMobile ?? bgPos}
>
	<picture class="room-bg" aria-hidden="true">
		{#if sceneMobile}
			<source media="(min-width: 1200px)" srcset={scene} />
		{/if}
		<img src={sceneMobile ?? scene} alt="" fetchpriority="high" />
	</picture>
	<div class="room-overlay">
		<!-- Plakette zuerst im DOM (h1 vor etwaigen Overlay-Überschriften);
		     raumspezifische Overlays sind absolut positioniert — die Reihenfolge
		     ändert nichts am Bild. -->
		<div class="room-plaque">
			<p class="eyebrow">{eyebrow}</p>
			<h1>{title}</h1>
			{#if lead}<p class="lead">{lead}</p>{/if}
		</div>
		{@render overlay?.()}
	</div>
</header>

<style>
	.room-hero {
		position: relative;
		min-height: 100svh;
		overflow: hidden;
	}
	/* Die feste Bildebene: position:fixed + z-index:0 — malt ÜBER dem
	   Shell-Hintergrund (nicht-positioniert), aber UNTER den nachfolgenden
	   positionierten Inhalten (main/Footer tragen position:relative +
	   #05090b und decken das Bild beim Scrollen ab; s. +layout.svelte).
	   Kein z-index:-1: das Bild gehört zum Root-Stacking-Context (fixed =
	   Viewport-Containing-Block) und würde dort hinter dem Shell-Hintergrund
	   verschwinden. */
	.room-bg img {
		position: fixed;
		inset: 0;
		z-index: 0;
		width: 100%;
		height: 100svh;
		object-fit: cover;
		object-position: var(--bg-pos, left top);
	}
	/* Weicher Übergang vom stehenden Bild in den scrollenden Inhalt — zielt auf
	   die Scrim-Farbe des Inhalts (rgba(5,9,11,.55), s. +layout.svelte). */
	.room-hero::after {
		content: '';
		position: absolute;
		inset: auto 0 0;
		height: 18svh;
		background: linear-gradient(rgba(5, 9, 11, 0), rgba(5, 9, 11, 0.55) 92%);
		pointer-events: none;
	}
	/* Fließ-Overlay: Titelblock liegt als normaler Text (Lesereihenfolge) über der
	   Bühne; raumspezifische Overlays (Tafel-Board, Tür-Hotspot) bleiben absolut.
	   Das Overlay selbst ist klickdurchlässig — nur Plakette und Overlay-Kinder
	   fangen Zeiger. */
	.room-overlay {
		position: absolute;
		inset: 0;
		display: grid;
		align-content: end;
		justify-items: center;
		pointer-events: none;
	}
	/* Schwebende Plakette: weiche Vignette statt opaker Kasten. */
	.room-plaque {
		position: relative;
		z-index: 1;
		padding: 1.6rem 1.6rem 1.2rem;
		width: min(46rem, calc(100% - 2rem));
		text-align: center;
		background: radial-gradient(
			ellipse 72% 95% at 50% 62%,
			rgba(3, 6, 7, 0.74),
			rgba(3, 6, 7, 0) 76%
		);
		pointer-events: auto;
	}
	.eyebrow {
		margin: 0 0 0.4rem;
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		text-shadow: 0 1px 10px rgba(3, 6, 7, 0.9);
	}
	h1 {
		margin: 0;
		color: #f0d899;
		font-size: clamp(1.7rem, 4.5vw, 2.9rem);
		font-weight: 400;
		line-height: 1.15;
		text-shadow: 0 2px 14px rgba(3, 6, 7, 0.9);
	}
	.lead {
		margin: 0.6rem 0 0;
		color: #e2d8c0;
		font-size: 1rem;
		text-shadow: 0 1px 10px rgba(3, 6, 7, 0.9);
	}
	@media (max-width: 1199px) {
		.room-bg img {
			object-position: var(--bg-pos-mobile, var(--bg-pos, left top));
		}
	}
</style>
