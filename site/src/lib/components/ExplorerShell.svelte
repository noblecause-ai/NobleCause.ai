<script>
	// Protokoll-Explorer — die gemeinsame Gestalt für /sessions und /journal
	// (Konzept §4). Die Räume erzählen den Vorgang, der Explorer hält den Rekord:
	// gleiche Welt/Farben/Schrift, aber die Bühne steht still — keine Bewegung,
	// kein Übergang. Kein Weiß, keine Kästen/Karten; ein Lichtkegel ersetzt jede
	// Rahmung, Vignetten und Hairlines statt Boxen. Deutsch-only (der Rekord).
	// Von sessions/+layout und journal/+layout umschlossen.
	let { children } = $props();
</script>

<div class="explorer">
	{@render children()}
</div>

<style>
	/* Das gerahmte Top-Level-main entrahmen (der Lichtkegel trägt die Fläche) —
	   dieselbe :has-Technik wie die Räume-Shell; gilt NUR für die Explorer-Seiten. */
	:global(.page:has(.explorer) > main) {
		min-height: 0;
		padding: 0;
		background: transparent;
		border: 0;
		box-shadow: none;
	}

	/* Lichtkegel: warmes Papier im Lampenlicht, die Ränder dunkeln ab. Fixe Ebene
	   hinter dem Inhalt — die einzige „Rahmung". */
	.explorer {
		position: relative;
		padding: clamp(1.4rem, 3vw, 2.6rem) clamp(0.2rem, 2vw, 1.4rem) 2rem;
		color: #e7dcc4;
	}
	.explorer::before {
		content: '';
		position: fixed;
		inset: 0;
		z-index: -1;
		pointer-events: none;
		background:
			radial-gradient(ellipse 72% 62% at 50% 20%, rgba(74, 55, 26, 0.5), rgba(74, 55, 26, 0) 60%),
			radial-gradient(ellipse 130% 105% at 50% 34%, rgba(4, 6, 8, 0), rgba(3, 5, 7, 0.94) 100%),
			#06090b;
	}

	/* ---- Rekord-Typografie -------------------------------------------------- */
	.explorer :global(h1) {
		color: #f0d899;
		font-size: 1.85rem;
		letter-spacing: 0;
	}
	.explorer :global(h2) {
		margin: 2.4rem 0 0.7rem;
		padding-top: 1rem;
		border-top: 1px solid rgba(166, 123, 61, 0.28);
		color: #ead8ae;
		font-size: 1.2rem;
		font-weight: 400;
		letter-spacing: 0.02em;
	}
	.explorer :global(.kicker) {
		color: #9e927f;
	}
	.explorer :global(.question) {
		margin: 0.4rem 0 1.6rem;
		border-left: 3px solid rgba(166, 123, 61, 0.45);
		color: #c7bca7;
		font-style: italic;
	}

	/* ---- Bereichs-/Rekordzeilen (kein Kasten, Hairline-getrennt) ------------ */
	.explorer :global(.rec-rows) {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.explorer :global(.rec-rows > li) {
		padding: 1.1rem 0;
	}
	.explorer :global(.rec-rows > li + li) {
		border-top: 1px solid rgba(166, 123, 61, 0.28);
	}
	.explorer :global(.rec-head) {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.4rem 0.75rem;
	}
	.explorer :global(.rec-head .emblem) {
		width: 2.5rem;
		height: 2.5rem;
		flex: none;
		border: 1px solid rgba(190, 139, 58, 0.6);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.explorer :global(.rec-area) {
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.explorer :global(.rec-tally) {
		color: #dfbd70;
		font: 600 0.9rem ui-sans-serif, system-ui, sans-serif;
		white-space: nowrap;
	}
	.explorer :global(.rec-tally.split) {
		color: #c7bca7;
		font-weight: 400;
	}

	/* ---- Marke: ein Votum als Absatz mit Kopfzeile (Medaillon + Modellname) -- */
	.explorer :global(.marks) {
		display: grid;
		gap: 0.85rem;
		margin-top: 0.85rem;
	}
	.explorer :global(.mark) {
		display: grid;
		grid-template-columns: 2.1rem 1fr;
		gap: 0.05rem 0.7rem;
		align-items: start;
	}
	.explorer :global(.mark .med) {
		grid-row: 1 / 3;
		width: 2.1rem;
		height: 2.1rem;
		border-radius: 50%;
		filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.7));
	}
	.explorer :global(.mark .med-none) {
		grid-row: 1 / 3;
		width: 2.1rem;
	}
	.explorer :global(.mark-model) {
		color: #f0d899;
		font: 600 0.64rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.07em;
		text-transform: uppercase;
	}
	.explorer :global(.mark-company) {
		color: #9e927f;
		font-style: italic;
	}
	.explorer :global(.mark-org) {
		color: #e6dbc4;
	}
	.explorer :global(.mark del) {
		color: #8f866f;
		text-decoration-color: rgba(197, 145, 60, 0.8);
		margin-right: 0.35rem;
	}
	.explorer :global(.mark-none) {
		color: #8f866f;
	}
	.explorer :global(.mark-note) {
		color: #e0c07f;
		font-size: 0.86rem;
	}

	/* ---- Aufklapper (Wortlaut/Dossier) — Hairline, kein Kärtchen ------------- */
	.explorer :global(details) {
		border-top: 1px solid rgba(166, 123, 61, 0.22);
		padding: 0.35rem 0;
	}
	.explorer :global(summary) {
		cursor: pointer;
		min-height: 44px;
		display: flex;
		align-items: center;
		color: #d7aa55;
		font: 0.82rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.02em;
	}
	.explorer :global(summary:hover) {
		color: #e7c881;
	}
	.explorer :global(a:focus-visible),
	.explorer :global(summary:focus-visible) {
		outline: 2px solid #d5a657;
		outline-offset: 2px;
	}

	/* ---- Fließtext (ungekürzt, gerendertes Markdown) ------------------------ */
	.explorer :global(.verbatim) {
		margin: 0.4rem 0 0.6rem;
		font-size: 0.95rem;
		color: #e2d8c2;
	}
	.explorer :global(.verbatim :is(h1, h2, h3, h4)) {
		border: 0;
		padding: 0;
		margin: 1rem 0 0.3rem;
		color: #ead8ae;
		font-size: 1rem;
	}
	.explorer :global(pre) {
		white-space: pre-wrap;
		overflow-wrap: break-word;
		font-family: ui-monospace, 'SF Mono', Menlo, monospace;
		font-size: 0.78rem;
		line-height: 1.55;
	}

	/* ---- §2 Adressierbare Filter (Links, kein Zustand) ---------------------- */
	.explorer :global(.filterbar) {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem 0.5rem;
		margin: 0 0 0.7rem;
	}
	.explorer :global(.filterlink) {
		display: inline-flex;
		align-items: center;
		min-height: 34px;
		padding: 0.3rem 0.7rem;
		border: 1px solid rgba(166, 123, 61, 0.4);
		border-radius: 999px;
		color: #c9ab6e;
		font: 600 0.68rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		text-decoration: none;
	}
	.explorer :global(.filterlink:hover) {
		border-color: #a67b3d;
		color: #e7c881;
	}
	.explorer :global(.filterlink.active) {
		background: rgba(213, 166, 87, 0.16);
		border-color: #a67b3d;
		color: #f0d899;
	}
	.explorer :global(.filternote) {
		margin: 0 0 1.2rem;
		color: #9e927f;
		font-size: 0.85rem;
	}
	.explorer :global(.rec-area),
	.explorer :global(.mark-model),
	.explorer :global(.voice-name) {
		text-decoration: none;
	}
	.explorer :global(.rec-area:hover),
	.explorer :global(.mark-model:hover),
	.explorer :global(.voice-name:hover) {
		color: #e7c881;
	}
	.explorer :global(.mark-org),
	.explorer :global(.tally-org),
	.explorer :global(.pillar-org) {
		color: inherit;
		text-decoration-color: rgba(166, 123, 61, 0.45);
	}
	.explorer :global(.mark-org) {
		font-weight: 600;
	}
	/* Hervorheben: der nicht adressierte Slice dimmt, die volle Liste bleibt. */
	.explorer :global(.dim) {
		opacity: 0.32;
		transition: opacity 0.25s ease;
	}
	@media (prefers-reduced-motion: reduce) {
		.explorer :global(.dim) {
			transition: none;
		}
	}
</style>
