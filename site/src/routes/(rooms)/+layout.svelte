<script>
	// Raum-Chrome für die drei Räume: Vollbild ohne Site-Header/Footer,
	// dezente Raum-Fußzeile, Übergänge nur als progressive Enhancement.
	// Sprachumschalter: schlichter Link auf die Schwester-Route — funktioniert
	// ohne JS (echte URLs), mit JS als normale SvelteKit-Navigation.
	import { browser } from '$app/environment';
	import { page } from '$app/state';
	import { installRoomTransitions } from '$lib/room-transitions.js';
	import { langOfPath, locales, roomPaths, siblingPath } from '$lib/i18n/index.js';

	let { children, data } = $props();

	let lang = $derived(langOfPath(page.url.pathname));
	let t = $derived(locales[lang]);
	let sibling = $derived(siblingPath(page.url.pathname));
	let otherLang = $derived(lang === 'de' ? 'en' : 'de');
	let homePath = $derived(roomPaths.study[lang]);

	if (browser) installRoomTransitions();
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
	   scrollende Inhalt die feste Bildebene (z-index:-1 im RoomHero) deckt. */
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
			/* Zoom-Ursprung = Klickpunkt (Tür), Fallback Mitte. */
			transform-origin: var(--vt-origin, center);
		}
		::view-transition-old(root) {
			animation: room-out 2s cubic-bezier(0.2, 0.7, 0.2, 1) both;
		}
		::view-transition-new(root) {
			animation: room-in 2s cubic-bezier(0.2, 0.7, 0.2, 1) both;
		}
		:root[data-nav-dir='back']::view-transition-old(root),
		:root[data-nav-dir='back']::view-transition-new(root) {
			animation-duration: 1.2s;
		}
		@keyframes room-out {
			to {
				transform: scale(1.3);
				opacity: 0;
				filter: brightness(0.5);
			}
		}
		@keyframes room-in {
			from {
				transform: scale(0.94);
				opacity: 0;
			}
		}
	}
</style>
