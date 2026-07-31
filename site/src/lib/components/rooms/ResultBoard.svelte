<script>
	// Ergebnis-Tafel: eigenständiges Schiefer-Panel, trägt die Antwort der Sitzung
	// in The Study und The Council. Ab 1200 px fix oben links (dort sitzt die
	// gemalte Tafel des Vorzimmers bei gängigen Verhältnissen), darunter statisch
	// im Fluss (Mobil: scrollt normal mit). Bewusst NICHT an Bildpixel gekettet —
	// durchgehend rem. Inhalt unverändert aus home.recommendations gelesen (nie
	// neu gezählt); Spendenlinks kommen registry-aufgelöst aus den Daten.
	// Kreide-Duktus für Bereich/Titel, klare Type für Organisation + Spendenlink.
	import { formatDate } from '$lib/format.js';
	let { home, t, emphasizeCount = false } = $props();
</script>

<section
	class="result-board"
	class:emphasize-count={emphasizeCount}
	id="antwort"
	aria-labelledby="result-board-title"
>
	<h2 id="result-board-title">{t.study.boardTitle}</h2>
	{#if home.currentSession?.number}
		<!-- Zeitschicht: Identität der Tafel — welche Sitzung. Nummer + Datum, weil
		     alle Bestandssitzungen dasselbe Datum tragen (Datum allein mehrdeutig). -->
		<p class="board-session">
			{t.study.boardSession(home.currentSession.number)} ·
			<time datetime={home.currentSession.date}
				>{formatDate(home.currentSession.date, t.lang)}</time
			>
		</p>
	{/if}
	<ol>
		{#each home.recommendations as rec (rec.pillar)}
			<li>
				<img src={t.pillars[rec.pillar]?.src} alt="" width="64" height="64" loading="lazy" />
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
		/* Weg A (Tafel-Auftrag): schwebende Vignette statt opakem Kasten + Goldrahmen
		   (dieselbe Formsprache wie .room-plaque/StageHero, die die Akteur-Plaketten
		   schon tragen). Rahmen, Deckgrund und Messing-Schatten sind raus. Die Tafel
		   trägt die Antwort + Spendenlinks in ALLEN DREI Räumen an derselben Stelle —
		   Lesbarkeit ist Boden: kräftiger Scrim (bis 82 % deckend, dann weich aus) +
		   text-shadow, Kontrast gegen echte Pixel gemessen (§6.1). */
		background: radial-gradient(
			ellipse farthest-corner at 50% 46%,
			rgba(3, 6, 7, 0.9) 58%,
			rgba(3, 6, 7, 0.78) 100%
		);
		text-shadow: 0 1px 8px rgba(3, 6, 7, 0.95);
		/* Tafel-Reise (Vertical Slice): genau EINE Instanz je Route (per Test
		   garantiert) — die Tafel wandert als Shared Element durch die Fahrt.
		   view-transition-name BLEIBT (Weg A, Steward-Entscheid): die Übergangs-
		   Behinderung wird bewusst in Kauf genommen, Weg B ist ein Nachtrag. */
		view-transition-name: board;
	}
	h2 {
		margin: 0 0 0.2rem;
		color: #dde4d6;
		font-size: 0.95rem;
		font-weight: 600;
		letter-spacing: 0.06em;
		text-transform: uppercase;
	}
	/* Zeitschicht-Datenzeile: welche Sitzung — ruhig unter dem Titel. */
	.board-session {
		margin: 0 0 0.55rem;
		color: #aeb6a6;
		font-size: 0.7rem;
		letter-spacing: 0.03em;
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

	/* Ab 1200 px steht die Tafel fix oben links als 2×2-Raster: zwei Spalten,
	   ZEILENWEISE gefüllt (Zukunft/Leid lindern oben, Große Gefahren/Übersehen
	   unten — Quell-Reihenfolge = Lesereihenfolge). So stehen alle vier Einträge
	   samt Spendenlink ohne Scrollgeste, auch bei 1280×720 (Steward-Entscheid:
	   internes Scrollen entfällt). Die Textspalte weicht der breiteren Tafel aus
	   (+layout.svelte, 33 rem). KEIN max-height/overflow und KEINE Unterkanten-
	   Maske mehr — die Tafel überläuft nicht, also hätte die Maske nur die untere
	   Spendenzeile angeschnitten. Mobil (<1200) bleibt einspaltig im Fluss. */
	@media (min-width: 1200px) {
		.result-board {
			position: fixed;
			top: 15.5rem;
			left: 1.25rem;
			z-index: 2;
			width: 30rem;
			margin: 0;
			padding: 0.7rem 1.1rem 0.35rem;
		}
		ol {
			grid-template-columns: 1fr 1fr;
			column-gap: 1.2rem;
		}
		li {
			padding: 0.3rem 0;
			column-gap: 0.6rem;
		}
		/* Trennlinie nur zwischen den beiden REIHEN (3./4. Eintrag), nicht
		   zwischen den Spalten — sonst zöge sie eine Linie neben den Einträgen. */
		li + li {
			border-top: 0;
		}
		li:nth-child(n + 3) {
			border-top: 1px solid rgba(120, 132, 118, 0.25);
		}
		img {
			width: 1.8rem;
			height: 1.8rem;
		}
		.board-area {
			font-size: 0.56rem;
		}
		strong {
			font-size: 0.84rem;
			line-height: 1.15;
		}
		.board-donate {
			font-size: 0.8rem;
		}
	}

	/* ---- Eintritts-Takt 3 (nur frischer Aufruf) -----------------------------
	   Bei Ankunft durch die Tür steht die Tafel von Anfang an (mode-arrival
	   greift hier nicht ein) — die Ergebnisse erscheinen nie ein zweites Mal.
	   Anfangszustand nur unter stage-armed (JS) + no-preference: ohne JS und
	   bei Reduced-Motion ist die Tafel sofort vollständig da. */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed.mode-fresh) .result-board {
			opacity: 0;
		}
		:global(html.stage-armed.mode-fresh.stage-play) .result-board {
			/* Der Endwert muss explizit stehen — das implizite `to` des Keyframes
			   liest sonst die statische Versteck-Regel (opacity: 0) mit. */
			opacity: 1;
			animation: board-in 0.5s ease-out 0.85s both;
		}
		:global(html.stage-skip) .result-board {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
		}
	}
	@keyframes board-in {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
	}
</style>
