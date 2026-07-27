<script>
	import { passageOrigin } from '$lib/door-passages.js';
	// Bühnen-Hero (§3 Schritt 2): RoomHero-Funktionalität (feste Vollbild-Bildebene,
	// Plakette, Overlay-Slot) plus Choreografie-Slots und die Prozess-Röhre unten.
	// Plakette (Titelbereich-Neuordnung, docs/titelbereich-neuordnung-fuer-kimi.md):
	// STABILER Kopf auf allen drei Raum-Seiten identisch — h1 = die Leitfrage,
	// darunter der Pitch in derselben Schrift/Farbe (nur kleiner) mit dem
	// „Warum so umständlich?"-Ausklapp als inline-Satzfortsetzung; darunter der
	// DYNAMISCHE Raumteil (ein Wort + Raum-Lead, pro Raum wechselnd).
	// Die Choreografie lebt als Beat-Klassen: Anfangszustände existieren NUR unter
	// html.stage-armed (JS-only, gesetzt durch app.html-Boot bzw. stage.js) und nur
	// ohne Reduced-Motion — das pragerenderte HTML ist der vollständige Endzustand.
	// Der Animationsstart hängt an html.stage-play (Ankunft wartet transition.finished).
	let {
		scene,
		sceneMobile = null,
		sceneMobile800 = null,
		sceneOpen = null,
		passage = null,
		bgPos = 'left top',
		bgPosMobile = null,
		title,
		pitch = '',
		whySummary = '',
		whyBody = '',
		roomWord = '',
		roomLead = '',
		overlay,
		tube,
		scene2 = null
	} = $props();

	// Ruhe-Stapel-Origin (Runde E §2): Türen mit aperturePlate (Council) leiten die
	// perspective-origin zur Laufzeit aus der Cover-Rechnung ab und führen sie bei
	// resize nach — eine Quelle mit der Fahrt. Türen mit fester `origin` (Study/
	// Archiv) bleiben unangetastet. SSR/ohne JS steht die Konstante bzw. der
	// CSS-Fallback; sichtbar wird die Origin ohnehin erst beim Hover (JS-Gate).
	let restOrigin = $state(passage?.origin ?? null);
	$effect(() => {
		if (!passage?.aperturePlate) return;
		const update = () => {
			restOrigin = passageOrigin(passage);
		};
		update();
		window.addEventListener('resize', update);
		return () => window.removeEventListener('resize', update);
	});
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
		<!-- 800-w-Stufe (A3): 390 px × DPR 2 = 780 braucht keine 1024er-Plate. -->
		<img
			class="beat-plate"
			src={sceneMobile ?? scene}
			srcset={sceneMobile && sceneMobile800 ? `${sceneMobile800} 800w, ${sceneMobile} 1024w` : undefined}
			sizes={sceneMobile && sceneMobile800 ? '100vw' : undefined}
			alt=""
			fetchpriority="high"
		/>
	</picture>
	{#if passage}
		<!-- §1 Ruhe-Stapel: der Spalt zeigt den Zielraum schon im Ruhezustand.
		     Void → farLo (Ferne, klein) → Flügel → Wand-mit-Loch, statisch bei
		     Kamera 0 — DERSELBE Stapel, den door-passage.js zur Fahrt beschleunigt
		     (Frame 1 = dieses Ruhebild, konstruktiv, §C). Beim Hover spreizen die
		     Flügel und geben das Ziel frei. Nur Desktop; Spreizung nur mit JS +
		     ohne Reduced-Motion (§0). -->
		<div class="rest-stack" aria-hidden="true" style:--rest-origin={restOrigin}>
			<div class="rest-dolly">
				<img class="rs-plane rs-far" src={passage.farLo} alt="" decoding="async" />
				<img class="rs-plane rs-leaf rs-leaf-l" src={passage.leafLeft} alt="" decoding="async" />
				<img class="rs-plane rs-leaf rs-leaf-r" src={passage.leafRight} alt="" decoding="async" />
				<img class="rs-plane rs-wall" src={passage.wallHole} alt="" decoding="async" />
			</div>
		</div>
	{:else if sceneOpen}
		<!-- Tür-offen-Ebene: Komposit, das ausserhalb der Tür pixelgleich mit
		     dem Basis-Plate ist — der Crossfade (CSS :has, ohne JS) öffnet
		     die Tür mit gemaltem Licht. Nur Desktop: der Hotspot existiert
		     erst ab 1200 px. -->
		<img class="room-bg-open" src={sceneOpen} alt="" aria-hidden="true" decoding="async" />
	{/if}
	{@render scene2?.()}
	<div class="room-overlay">
		<!-- Plakette zuerst im DOM (h1 vor etwaigen Overlay-Überschriften);
		     raumspezifische Overlays sind absolut positioniert — die Reihenfolge
		     ändert nichts am Bild. -->
		<div class="room-plaque">
			<!-- STABILER Kopf (Masthead): h1 + Pitch + Why-Ausklapp stehen auf
			     allen drei Raum-Seiten identisch GANZ OBEN und bleiben über den
			     Raumwechsel stabil — view-transition-name: masthead, die Gruppen-
			     Regel steht neben der Tafel-Regel in +layout.svelte. Der Kopf ist
			     fester Rahmen und kein Choreografie-Beat: er ist sofort da, auch
			     im neuen Snapshot der View-Transition (kein beat-title). -->
			<div class="stable-head">
				<h1>{title}</h1>
				{#if pitch}
					<!-- Pitch und „Warum so umständlich?" bilden EINEN
					     Absatz — der Ausklapp ist die Fortsetzung desselben Satzes
					     (inline, natives details: ohne JS und per Tastatur bedienbar).
					     details ist Flow-Content und darf nicht in <p> stehen — deshalb
					     div + display:inline statt verschachteltem Absatz. -->
					<div class="pitch-block">
						<span class="pitch-text">{pitch}</span>
						{#if whySummary}
							<details class="why-inline">
								<summary>{whySummary}</summary>
								<p class="why-body">{whyBody}</p>
							</details>
						{/if}
					</div>
				{/if}
			</div>
			{#if roomWord}
				<!-- Dynamischer Raumteil: ein Wort (Rollenschild, untergeordnet —
				     kein h2; genau ein h1 je Seite bleibt) + Raum-Lead. Fade-in im
				     Duktus der Prozess-Schritte (beat-room, s. Choreografie unten). -->
				<div class="room-tag beat-room">
					<p class="room-word">{roomWord}</p>
					{#if roomLead}<p class="room-lead">{roomLead}</p>{/if}
				</div>
			{/if}
		</div>
		{@render overlay?.()}
	</div>
	{@render tube?.()}
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
	   Scrim und decken das Bild beim Scrollen ab; s. +layout.svelte).
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
	/* Tür-offen-Ebene: gleiche Geometrie wie das Basis-Plate, liegt darüber
	   (später im DOM, gleicher z-index) und bleibt unsichtbar, bis der
	   Tür-Hotspot Hover/Fokus bekommt. Rein dekorativ — der Link bleibt
	   ohnehin ein Link; ohne :has-Support bleibt die Tür einfach zu. */
	.room-bg-open {
		position: fixed;
		inset: 0;
		z-index: 0;
		width: 100%;
		height: 100svh;
		object-fit: cover;
		object-position: var(--bg-pos, left top);
		opacity: 0;
		transition: opacity 0.55s ease;
		pointer-events: none;
	}
	@media (max-width: 1199px) {
		.room-bg-open {
			display: none;
		}
	}
	:global(.room-hero:has(.door-hotspot:hover) .room-bg-open),
	:global(.room-hero:has(.door-hotspot:focus-visible) .room-bg-open),
	:global(html.stage-clearing .room-bg-open) {
		opacity: 1;
	}
	/* Tür-auf VOR der Fahrt: mit dem verkürzten Vorlauf (140 ms, A7) muss die
	   Türöffnung bis zur VT-Capture offen sein — sonst fliegen Tastatur- und
	   Touch-Auslösung in eine erst zu ~25 % offene Tür (Hover ist am Desktop
	   längst offen, verdeckt das dort). 0,14 s deckt den Vorlauf, ohne A7 zu
	   verletzen. */
	:global(html.stage-clearing) .room-bg-open {
		transition-duration: 0.14s;
	}
	@media (prefers-reduced-motion: reduce) {
		.room-bg-open {
			transition: none;
		}
	}
	/* §1 Ruhe-Stapel: fixe z-index:0-Perspektivebene hinter der UI (wie .room-bg),
	   STATISCH bei Kamera 0 — dieselbe Geometrie wie die Fahrt-Übergangsebene
	   (.passage-layer in +layout.svelte). Frame 1 der Fahrt = dieses Ruhebild,
	   damit konstruktiv statt gemessen (§C). Nur Desktop ≥1200 px. */
	.rest-stack {
		position: fixed;
		inset: 0;
		z-index: 0;
		overflow: hidden;
		pointer-events: none;
		perspective: 850px;
		perspective-origin: var(--rest-origin, 48.8% 41%);
		/* Void: die Ferne wächst beim Spreizen aus dem Schwarz, der Ausgangsraum
		   scheint nicht in den Rändern durch. */
		background: #05090b;
		display: none;
	}
	@media (min-width: 1200px) {
		.rest-stack {
			display: block;
		}
	}
	.rest-dolly {
		position: absolute;
		inset: 0;
		transform-style: preserve-3d;
	}
	.rest-stack .rs-plane {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100svh;
		object-fit: cover;
		object-position: center top;
		backface-visibility: hidden;
	}
	/* Ferne NICHT gegenskaliert (Handoff-Deckungsgleichheit, §6.3): bei Kamera 0
	   erscheint sie klein (≈0,38 × Cover) hinter dem Loch. */
	.rs-far {
		transform: translateZ(-1400px);
	}
	.rs-wall {
		transform: translateZ(0);
	}
	/* Flügel geschlossen im Ruhezustand (Tür zu = heutiges Plate). Die Spreizung
	   gibt erst das Ziel frei — sie läuft NUR mit JS (html.js) UND ohne
	   Reduced-Motion; ohne beides steht die geschlossene Tür (§0). */
	.rs-leaf {
		transform: translateZ(0);
	}
	@media (prefers-reduced-motion: no-preference) {
		.rs-leaf {
			transition: transform 0.5s cubic-bezier(0.4, 0, 0.5, 1);
		}
		:global(html.js .room-hero:has(.door-hotspot:hover) .rs-leaf-l),
		:global(html.js .room-hero:has(.door-hotspot:focus-visible) .rs-leaf-l) {
			transform: translateZ(0) translateX(-58px);
		}
		:global(html.js .room-hero:has(.door-hotspot:hover) .rs-leaf-r),
		:global(html.js .room-hero:has(.door-hotspot:focus-visible) .rs-leaf-r) {
			transform: translateZ(0) translateX(58px);
		}
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
	   Bühne; raumspezifische Overlays (Tür-Hotspot) bleiben absolut. Das Overlay
	   selbst ist klickdurchlässig — nur Plakette und Overlay-Kinder fangen Zeiger.
	   Der stabile Kopf steht GANZ OBEN (Nachtrag 24.07.): align-content start +
	   padding-top; unten bleibt die Bühne frei für die Prozess-Röhre. */
	.room-overlay {
		position: absolute;
		inset: 0;
		display: grid;
		align-content: start;
		justify-items: center;
		padding-top: 1.1rem;
		pointer-events: none;
	}
	/* Der Kopf zentriert IMMER auf die volle Viewport-Breite — nicht im
	   Restraum neben der fixen Tafel. Die Tafel (oben links, ab 1200 px)
	   beginnt UNTER dem Kopf-Streifen inkl. Raumteil (top: 15.5 rem,
	   Bemessung s. ResultBoard.svelte). */
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
	/* Masthead: der stabile Kopf bekommt wie die Tafel einen eigenen
	   view-transition-name, damit er über den Raumwechsel pixelstabil
	   stehen bleibt (Gruppen-Regel in +layout.svelte). */
	.stable-head {
		view-transition-name: masthead;
	}
	/* Stabiler Kopf: EINE Typo-Familie für den ganzen Block — h1, Pitch und
	   Why-Summary teilen Schriftart und Farbe (#f0d899), nur die Größe fällt
	   ab (Titelbereich-Neuordnung: kein Grau/Creme, kein zweiter Font). */
	h1 {
		margin: 0;
		color: #f0d899;
		font-size: clamp(1.45rem, 3.4vw, 2.2rem);
		font-weight: 400;
		line-height: 1.15;
		text-shadow: 0 2px 14px rgba(3, 6, 7, 0.9);
	}
	.pitch-block {
		margin: 0.55rem 0 0;
		color: #f0d899;
		font-size: 0.92rem;
		line-height: 1.5;
		text-shadow: 0 1px 10px rgba(3, 6, 7, 0.9);
	}
	/* Der Ausklapp steht inline als Fortsetzung des Pitch-Satzes — dezent
	   unterstrichen statt Gold-Link-Look, keine eigene Zeile. Natives
	   details/summary: ohne JS und per Tastatur bedienbar (Inline-Satzglied,
	   Tippziel-Ausnahme wie bei Textlinks). Das ▸ steht im i18n-String —
	   die nativen Marker bleiben aus. */
	.why-inline {
		display: inline;
	}
	.why-inline summary {
		display: inline;
		cursor: pointer;
		color: #f0d899;
		text-decoration: underline dotted rgba(240, 216, 153, 0.6);
		text-underline-offset: 0.2em;
	}
	.why-inline summary::marker {
		content: none;
	}
	.why-inline summary::-webkit-details-marker {
		display: none;
	}
	.why-inline summary:hover {
		color: #f7e7bd;
		text-decoration-color: rgba(247, 231, 189, 0.85);
	}
	.why-inline summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	/* Geöffnet bricht der Body als eigener ruhiger Absatz unter den Satz —
	   mit eigenem Scrim: der Kopf steht oben, der geöffnete Ausklapp kann
	   über die Szene (und bei ~1200 px Richtung Tafel) wachsen. */
	.why-body {
		max-width: 34rem;
		margin: 0.5rem auto 0.2rem;
		padding: 0.55rem 0.8rem;
		font-size: 0.88rem;
		line-height: 1.5;
		text-align: left;
		background: rgba(3, 6, 7, 0.72);
		border-radius: 0.5rem;
	}
	/* Dynamischer Raumteil: ein Wort (Rollenschild im Duktus der
	   Prozess-Schritte) + Raum-Lead — wechselt pro Raum den Inhalt. */
	.room-tag {
		margin-top: 0.95rem;
	}
	.room-word {
		margin: 0;
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		text-shadow: 0 1px 10px rgba(3, 6, 7, 0.9);
	}
	.room-lead {
		margin: 0.35rem 0 0;
		color: #e2d8c0;
		font-size: 1rem;
		text-shadow: 0 1px 10px rgba(3, 6, 7, 0.9);
	}
	@media (max-width: 1199px) {
		.room-bg img {
			object-position: var(--bg-pos-mobile, var(--bg-pos, left top));
		}
		/* Der Sprach-Schalter liegt fixed oben rechts — der Kopf rückt unter ihn. */
		.room-overlay {
			padding-top: 3.4rem;
		}
	}

	/* ---- Eintritts-Choreografie -------------------------------------------
	   Takte (§2 des Umlaufs, ~2 s, ~50 ms überlappend): Plate settle →
	   [Zweite-Ebene-Slot scene2: StudyActors — Wolkenzug still, Akteure
	   0,55–1,2 s Schienen-Einfahrt] → Tafel 0,8–1,2 s (nur fresh,
	   s. ResultBoard.svelte) → Raumteil 1,25–1,75 s (beat-room: Fade-in im
	   Duktus der Prozess-Schritte) → Röhre 1,3–1,9 s (s. StageTube.svelte)
	   → Lock. Der stabile Kopf (Masthead) ist KEIN Beat mehr: fester Rahmen,
	   sofort sichtbar, über den Raumwechsel per view-transition stabil
	   (Nachtrag 24.07.). Anfangs- und Endzustände stehen in den Keyframes
	   (fill: both); html.stage-skip lässt alles in den Endzustand
	   springen (bewusstes Scrollen während des Aufbaus).
	   Plate und Tafel spielen NUR beim frischen Aufruf: bei der Ankunft durch
	   die Tür ist der Raum (Plate) mit der Fahrt bereits erschienen und die
	   Tafel mitgereist — beides darf kein zweites Mal aufbauen (und die
	   View-Transition braucht den Zielraum komplett in der Capture). */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed.mode-fresh) .beat-plate {
			opacity: 0;
		}
		:global(html.stage-armed.mode-fresh.stage-play) .beat-plate {
			/* Endwert explizit — das implizite `to` liest sonst opacity: 0 mit. */
			opacity: 1;
			animation: plate-in 0.5s ease-out both;
		}
		/* Dynamischer Raumteil: eigener Fade-in-Takt vor der Röhre (1,3 s) —
		   wie ein Rollenschild, das eingeblendet wird. */
		:global(html.stage-armed) .beat-room {
			opacity: 0;
		}
		:global(html.stage-armed.stage-play) .beat-room {
			opacity: 1;
			animation: title-in 0.5s ease-out 1.25s both;
		}
		:global(html.stage-skip) .beat-plate,
		:global(html.stage-skip) .beat-room {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
		}
		/* Nach dem Lock beruhigt sich die Plakette beim Scrollen dezent. */
		:global(html.stage-unlocked) .room-plaque {
			opacity: 0.88;
		}
		.room-plaque {
			transition: opacity 0.4s ease;
		}
	}
	@keyframes plate-in {
		from {
			opacity: 0;
			transform: scale(1.035);
			filter: brightness(0.82);
		}
	}
	@keyframes title-in {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
	}
</style>
