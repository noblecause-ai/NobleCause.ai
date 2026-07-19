<script>
	// Ergebnis-Tafel: eigenständiges Schiefer-Panel, trägt die Antwort der Sitzung
	// in The Study und The Council. Ab 1200 px fix oben links (dort sitzt die
	// gemalte Tafel des Vorzimmers bei gängigen Verhältnissen), darunter statisch
	// im Fluss (Mobil: scrollt normal mit). Bewusst NICHT an Bildpixel gekettet —
	// durchgehend rem. Inhalt unverändert aus home.recommendations gelesen (nie
	// neu gezählt); Spendenlinks kommen registry-aufgelöst aus den Daten.
	// Kreide-Duktus für Bereich/Titel, klare Type für Organisation + Spendenlink.
	let { home, t, emphasizeCount = false } = $props();
</script>

<section
	class="result-board"
	class:emphasize-count={emphasizeCount}
	id="antwort"
	aria-labelledby="result-board-title"
>
	<h2 id="result-board-title">{t.study.boardTitle}</h2>
	<ol>
		{#each home.recommendations as rec (rec.pillar)}
			<li>
				<img src={t.pillars[rec.pillar]?.src} alt="" width="64" height="64" />
				<span class="board-area">{t.pillars[rec.pillar]?.label ?? rec.pillarName}</span>
				{#if rec.hasConsensus}
					<strong
						>{rec.organization.name}<span class="board-count">
							· {rec.count} {t.common.ofWord} {rec.total}</span
						></strong
					>
					{#if rec.organization.donationUrl}
						<a class="board-donate" href={rec.organization.donationUrl}>{t.common.donate}</a>
					{/if}
				{:else}
					<strong>{t.council.noConsensus}</strong>
				{/if}
			</li>
		{/each}
	</ol>
</section>

<style>
	/* Schiefer-Panel: dunkler Stein-Gradient, Messing-Kante, ruhiger Schatten. */
	.result-board {
		width: min(26rem, calc(100% - 2rem));
		margin: 2.2rem auto 0;
		padding: 1rem 1.3rem 0.4rem;
		background: linear-gradient(160deg, rgba(19, 26, 27, 0.93), rgba(8, 12, 13, 0.95));
		border: 1px solid rgba(166, 123, 61, 0.6);
		box-shadow:
			0 1rem 2.5rem rgba(0, 0, 0, 0.5),
			inset 0 0 2.5rem rgba(0, 0, 0, 0.4);
	}
	h2 {
		margin: 0 0 0.4rem;
		color: #dde4d6;
		font-size: 0.95rem;
		font-weight: 600;
		letter-spacing: 0.06em;
		text-transform: uppercase;
	}
	ol {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
	}
	li {
		display: grid;
		grid-template-columns: auto 1fr;
		column-gap: 0.8rem;
		align-content: start;
		padding: 0.55rem 0;
	}
	li + li {
		border-top: 1px solid rgba(120, 132, 118, 0.25);
	}
	img {
		grid-row: span 3;
		width: 2.6rem;
		height: 2.6rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.board-area {
		color: #c9ab6e;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	strong {
		color: #f5eeda;
		font-size: 1.02rem;
		font-weight: 600;
		line-height: 1.25;
	}
	/* Zählstand direkt bei der Organisation — klare Type, ruhiger als der Name. */
	.board-count {
		color: #cfd8cc;
		font-size: 0.8em;
		font-weight: 400;
		white-space: nowrap;
	}
	/* Council: der Zählstand ist die Schlagzeile der Tafel. */
	.emphasize-count .board-count {
		color: #dfbd70;
		font-size: 0.95em;
		font-weight: 600;
	}
	.board-donate {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e6b45c;
		font-size: 0.9rem;
		text-decoration: underline;
		text-underline-offset: 0.15em;
	}
	.board-donate:hover {
		color: #f2d9a0;
	}

	/* Ab 1200 px steht die Tafel fix oben links — dort sitzt die gemalte Tafel
	   bei gängigen Verhältnissen; die Textspalte weicht ihr aus (+layout.svelte). */
	@media (min-width: 1200px) {
		.result-board {
			position: fixed;
			top: 1.25rem;
			left: 1.25rem;
			z-index: 2;
			width: 22rem;
			margin: 0;
		}
	}
	/* Kurze Viewports: kompaktere Dichte, damit die Tafel nicht in die
	   Hero-Plakette ragt. Tippzielhöhe der Links bleibt 44 px. */
	@media (min-width: 1200px) and (max-height: 740px) {
		.result-board {
			padding: 0.7rem 1rem 0.2rem;
		}
		h2 {
			margin-bottom: 0.25rem;
			font-size: 0.82rem;
		}
		li {
			padding: 0.35rem 0;
		}
		img {
			width: 2.1rem;
			height: 2.1rem;
		}
		strong {
			font-size: 0.92rem;
		}
		.board-donate {
			font-size: 0.82rem;
		}
	}
</style>
