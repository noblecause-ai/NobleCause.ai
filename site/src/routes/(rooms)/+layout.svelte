<script>
	// Raum-Chrome für die drei Räume: Vollbild ohne Site-Header/Footer,
	// dezente Raum-Fußzeile, Übergänge nur als progressive Enhancement.
	// Sprachumschalter: schlichter Link auf die Schwester-Route — funktioniert
	// ohne JS (echte URLs), mit JS als normale SvelteKit-Navigation.
	import { browser } from '$app/environment';
	import { page } from '$app/state';
	import { installRoomTransitions } from '$lib/room-transitions.js';
	import { installStage } from '$lib/stage.js';
	import { langOfPath, locales, roomPaths, siblingPath } from '$lib/i18n/index.js';

	let { children, data } = $props();

	let lang = $derived(langOfPath(page.url.pathname));
	let t = $derived(locales[lang]);
	let sibling = $derived(siblingPath(page.url.pathname));
	let otherLang = $derived(lang === 'de' ? 'en' : 'de');
	let homePath = $derived(roomPaths.study[lang]);

	if (browser) {
		installRoomTransitions();
		installStage();
	}
</script>

<div class="rooms-shell">
	{#if sibling}
		<a class="lang-switch" href={sibling} hreflang={otherLang} aria-label={t.common.switchLabel}>
			{t.common.switchTo}
		</a>
	{/if}

	{#if data.home}
		{@render children()}
	{:else}
		<main class="room-section">
			<p>{t.common.noSession}</p>
		</main>
	{/if}

	<footer class="room-footer">
		<a class="room-brand" href={homePath}>{t.common.brand}</a>
		<nav aria-label={t.common.navLabel}>
			{#each t.common.siteNav as link (link.href)}
				<a href={link.href}>{link.label}</a>
			{/each}
		</nav>
	</footer>
</div>

<style>
	/* Die Räume verlassen den Dokumenten-Rahmen der übrigen Seite. */
	:global(.page:has(.rooms-shell)) {
		max-width: none;
		padding: 0;
	}
	:global(.page:has(.rooms-shell) > header),
	:global(.page:has(.rooms-shell) > footer) {
		display: none;
	}
	/* Nur das ÄUSSERE Template-main (direktes Kind von .page) wird entschärft —
	   die main-Elemente der Räume brauchen eigenen Hintergrund, damit der
	   scrollende Inhalt die feste Bildebene (z-index:0 im StageHero) deckt. */
	:global(.page:has(.rooms-shell) > main) {
		min-height: 0;
		padding: 0;
		background: transparent;
		border: 0;
		box-shadow: none;
	}
	.rooms-shell :global(main) {
		/* Positioniert + transluzenter Scrim statt Deckfarbe: der Inhalt scrollt
		   über die feste Bildebene (z-index:0) und lässt sie durchscheinen —
		   unten dichter (Lesbarkeit), oben offener (Anschluss an den Hero). */
		position: relative;
		background: linear-gradient(rgba(5, 9, 11, 0.55), rgba(5, 9, 11, 0.82));
	}

	.rooms-shell {
		position: relative;
		background: #05090b;
		color: #e7dcc4;
		font-family: Georgia, 'Iowan Old Style', serif;
	}

	.lang-switch {
		/* Fix: bleibt beim Scrollen erreichbar und liegt über der fixen Tafel. */
		position: fixed;
		top: 0.9rem;
		right: 1rem;
		z-index: 3;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 44px;
		min-height: 44px;
		padding: 0 0.9rem;
		background: rgba(5, 9, 11, 0.72);
		border: 1px solid rgba(213, 166, 87, 0.55);
		border-radius: 999px;
		color: #e7c881;
		font: 600 0.72rem ui-sans-serif, system-ui;
		letter-spacing: 0.12em;
		text-decoration: none;
	}
	.lang-switch:hover {
		border-color: #d5a657;
		color: #f2d9a0;
	}

	/* Gemeinsame Raum-Bausteine (Sektionen, Panels, Tür-Galerie). */
	.rooms-shell :global(.room-section) {
		width: min(70rem, calc(100% - 2rem));
		margin: 0 auto;
		padding: 2.6rem 1rem 0;
	}
	@media (min-width: 1200px) {
		/* Die Textspalte weicht der fixen Ergebnis-Tafel (links, 22 rem +
		   1,25 rem Abstand) aus; bei Ultrawide zentriert sie wieder. */
		.rooms-shell :global(.room-section) {
			width: min(70rem, calc(100% - 27rem));
			margin-left: max(calc(50% - 35rem), 25.5rem);
			margin-right: 1rem;
		}
	}
	.rooms-shell :global(.room-section > h2) {
		margin: 0 0 0.9rem;
		padding-top: 0;
		border-top: 0;
		color: #ead8ae;
		font-size: 1.3rem;
		font-weight: 400;
		letter-spacing: 0.03em;
	}
	.rooms-shell :global(.room-panel) {
		padding: 1.1rem 1.3rem;
		background: rgba(13, 18, 19, 0.94);
		border: 1px solid rgba(166, 123, 61, 0.5);
		box-shadow: 0 1rem 2.5rem rgba(0, 0, 0, 0.4);
	}
	.rooms-shell :global(.door-gallery) {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(min(15rem, 100%), 1fr));
		gap: 1rem;
		padding-bottom: 2.6rem;
	}
	/* Gerendertes Markdown (Dissens/Korrektur) darf die Raum-Breite nie sprengen. */
	.rooms-shell :global(pre) {
		max-width: 100%;
		overflow-x: auto;
	}
	.rooms-shell :global(.room-panel code) {
		overflow-wrap: break-word;
	}

	.room-footer {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem 1.4rem;
		align-items: baseline;
		width: min(70rem, calc(100% - 2rem));
		margin: 0 auto;
		padding: 1.1rem 1rem 2.2rem;
		border-top: 1px solid rgba(166, 123, 61, 0.4);
		/* Derselbe Scrim wie main — das feste Bild scheint auch am Seitenende durch. */
		position: relative;
		background: linear-gradient(rgba(5, 9, 11, 0.55), rgba(5, 9, 11, 0.82));
	}
	.room-brand {
		margin-right: auto;
		color: #e7c881;
		text-decoration: none;
	}
	.room-footer nav {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}
	.room-footer nav a {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #a89d8b;
		font: 0.82rem ui-sans-serif, system-ui;
		text-decoration: none;
	}
	.room-footer nav a:hover {
		color: #d7aa55;
	}

	/* Übergänge zwischen den Räumen (nur installiert, wenn API + no-preference). */
	@media (prefers-reduced-motion: no-preference) {
		::view-transition-old(root),
		::view-transition-new(root) {
			/* Zoom-Ursprung = Tür-Kartenmitte (Klick/Tastatur), Fallback Mitte. */
			transform-origin: var(--vt-origin, center);
		}
		::view-transition-old(root) {
			/* Türfahrt: die Szene fliegt IN die Tür hinein (starker Zoom, dunkelt
			   ab) — die neue Szene öffnet sich darunter. */
			animation: room-out 2s cubic-bezier(0.45, 0, 0.8, 0.6) both;
		}
		::view-transition-new(root) {
			animation: room-in 2s cubic-bezier(0.2, 0.7, 0.2, 1) both;
		}
		:root[data-nav-dir='back']::view-transition-old(root),
		:root[data-nav-dir='back']::view-transition-new(root) {
			animation-duration: 1.2s;
		}
		/* Die Ergebnis-Tafel reist als Shared Element im selben Tempo mit. */
		::view-transition-group(board) {
			animation-duration: 2s;
		}
		:root[data-nav-dir='back']::view-transition-group(board) {
			animation-duration: 1.2s;
		}
		/* Der stabile Kopf (Masthead) ebenso: gleiche Gruppen-Regel wie die
		   Tafel — er bleibt über den Raumwechsel pixelstabil stehen. */
		::view-transition-group(masthead) {
			animation-duration: 2s;
		}
		:root[data-nav-dir='back']::view-transition-group(masthead) {
			animation-duration: 1.2s;
		}
		@keyframes room-out {
			to {
				transform: scale(2.4);
				opacity: 0;
				filter: brightness(0.35);
			}
		}
		@keyframes room-in {
			from {
				transform: scale(1.06);
				opacity: 0;
			}
		}

		/* ---- Tür-Gegenprobe (Spike, §B): der Zielraum wird aus der Türkontur
		   aufgezogen, statt den ganzen Frame zu ersetzen. Nur bei echter Türfahrt
		   (data-portal, gesetzt im Klick-Handler nach allen Guards) — Back/Forward
		   und Quereinstiege behalten das bisherige room-out/room-in. Die
		   [data-portal]-Regeln sind spezifischer und überschreiben die obigen.
		   Fallback-Werte in var() greifen, falls die Geometrie fehlt (Blende aus
		   der Mitte). board/masthead haben eigene VT-Namen, liegen also außerhalb
		   der Blende und bleiben als fester Rahmen stehen, während der Raum wächst.
		   QUELLREIHENFOLGE-ABHÄNGIG: Die animation-duration der board/masthead-
		   Gruppen (1,1 s) hat DIESELBE Spezifität wie die :root[data-nav-dir='back']-
		   Gruppenregeln oben (1,2 s). Bei einem Türklick rückwärts (nav-dir=back +
		   data-portal) gewinnt die spätere Regel = diese hier (1,1 s). Dieser Block
		   MUSS nach den room-out/room-in- und den nav-dir-Regeln stehen bleiben —
		   beim Umsortieren kippt sonst die Dauer. */
		:root[data-portal]::view-transition-old(root) {
			animation: portal-out 1.1s cubic-bezier(0.45, 0, 0.8, 0.6) both;
		}
		:root[data-portal]::view-transition-new(root) {
			animation: portal-in 1.1s cubic-bezier(0.2, 0.7, 0.2, 1) both;
			/* N2: das UA-Stylesheet setzt mix-blend-mode: plus-lighter auf
			   ::view-transition-old/new — für einen Opacity-Crossfade korrekt
			   (Summe = 1). portal-in animiert aber KEINE Opacity: der Zielraum
			   steht ab Frame 0 voll deckend, portal-out noch bei 1 → in der
			   Türkontur würden alt+neu ADDIERT (leuchtender Saum, erste ~200 ms).
			   Wir wollen Deckung, nicht Addition — bewusste Entscheidung, nicht
			   UA-Default. */
			mix-blend-mode: normal;
		}
		:root[data-portal]::view-transition-group(board),
		:root[data-portal]::view-transition-group(masthead) {
			animation-duration: 1.1s;
		}
		@keyframes portal-out {
			to {
				/* schwächer als die alten 2.4 — der Frame fährt auf die Tür zu,
				   statt an ihr vorbeizuschießen; die Blende trägt jetzt den Effekt. */
				transform: scale(1.55);
				opacity: 0;
				filter: brightness(0.34);
			}
		}
		@keyframes portal-in {
			from {
				clip-path: inset(
					var(--door-top, 30%) var(--door-right, 40%) var(--door-bottom, 12%)
						var(--door-left, 40%) round 6px
				);
				transform: scale(1.14);
			}
			to {
				clip-path: inset(0 0 0 0 round 0);
				transform: none;
			}
		}
	}
</style>
