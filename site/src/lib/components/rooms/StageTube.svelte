<script>
	// Prozess-Röhre (§3 Schritt 2): Instrument am unteren Bühnenrand — kein
	// Stepper; die Kugeln sind seit der Titelbereich-Neuordnung fokussierbar,
	// weil der Erklärsatz jetzt AN der Kugel liegt (Hover/Fokus, reines CSS) —
	// die FlowRail als zweite Prozess-Darstellung ist entfallen. Der Füllstand
	// ist eine Eigenschaft des Raums (Study 2, Council 5, Archive 6) und steht
	// als SSR-Klassen im pragerenderten HTML: No-JS und Reduced-Motion zeigen
	// denselben korrekten Stand, nur ohne Einlauf. Inhalte kommen aus dem
	// Locale-Array study.flow; Schritt 3 trägt die Teilnehmerzahl aus den Daten.
	// Der DIFF zwischen Räumen (2→5, rückwärts −1) ist Vertical-Slice — hier
	// läuft nur die Eintritts-Staffelung der Perlen von rechts.
	// caption: optionale persistente Zeit-Zeile je Raum (Zeitschicht) — als Snippet,
	// weil sie Markup trägt (formatiertes Datum, Manifest-Link). Sitzt unter der
	// Röhre, immer sichtbar (auch auf Touch), No-JS = vollständig.
	let { flow, filledCount, participantCount, label, status, caption } = $props();

	let steps = $derived(
		flow.map((step, i) => ({
			...step,
			text: typeof step.text === 'function' ? step.text(participantCount) : step.text,
			state: i < filledCount ? 'filled' : 'blass',
			active: i === filledCount - 1
		}))
	);
</script>

<div class="stage-tube beat-tube" aria-label={label}>
	<p class="sr-only">{status}</p>
	<ol class="tube-rail">
		{#each steps as step, i (step.name)}
			<!-- Der Erklärsatz liegt AN der Kugel (Titelbereich-Neuordnung): immer
			     im DOM (No-JS/Screenreader lesen alles mit), sichtbar bei Hover.
			     KEIN tabindex: die Kugel ist nicht bedienbar (kein Link, keine
			     Aktion) — ein Fokusstopp ohne Bedienbarkeit verstösst gegen die
			     StageTube-Regel; der Text ist per SR/No-JS ohnehin erreichbar. -->
			<li class="tube-bead {step.state}{step.active ? ' active' : ''}" style:--i={i}>
				<img src={step.src} alt="" width="48" height="48" />
				<span class="bead-name">{step.name}</span>
				<span class="bead-text">{step.text}</span>
			</li>
		{/each}
	</ol>
	{#if caption}<div class="tube-caption">{@render caption()}</div>{/if}
</div>

<style>
	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		margin: -1px;
		padding: 0;
		overflow: hidden;
		clip: rect(0 0 0 0);
		white-space: nowrap;
		border: 0;
	}
	.stage-tube {
		position: absolute;
		inset: auto 0 0;
		z-index: 1;
		display: grid;
		justify-items: center;
		gap: 0.4rem;
		padding: 1.2rem 1rem 0.75rem;
		background: linear-gradient(rgba(5, 9, 11, 0), rgba(5, 9, 11, 0.68) 55%);
	}
	/* Zeitschicht-Zeile unter der Röhre. Der Wrapper liegt in StageTube-Scope; die
	   Snippet-Inhalte kommen aus dem Raum (andere Scope) → Farbe/Font erben, Link
	   und <time> per :global. text-shadow trägt die Lesbarkeit über dem Scrim. */
	.tube-caption {
		max-width: 46rem;
		margin-top: 0.1rem;
		color: #b7bdad;
		font-size: 0.74rem;
		line-height: 1.4;
		text-align: center;
		text-shadow: 0 1px 6px rgba(3, 6, 7, 0.92);
	}
	.tube-caption :global(a) {
		color: #e6b45c;
		text-decoration: underline;
		text-underline-offset: 0.15em;
	}
	.tube-caption :global(a:hover) {
		color: #f2d9a0;
	}
	.tube-caption :global(time) {
		white-space: nowrap;
	}
	.tube-caption :global(p) {
		margin: 0;
	}
	.tube-rail {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		align-items: start;
		gap: clamp(0.3rem, 1.8vw, 1rem);
	}
	.tube-bead {
		position: relative;
		display: grid;
		justify-items: center;
		gap: 0.25rem;
		width: clamp(3.2rem, 6.5vw, 4.4rem);
		text-align: center;
	}
	/* Verbindungspfeile: glühen nur, wenn beide Nachbarn gefüllt sind. */
	.tube-bead:not(:last-child)::after {
		content: '→';
		position: absolute;
		top: clamp(0.9rem, 2vw, 1.3rem);
		right: calc(-1 * clamp(0.3rem, 1.8vw, 1rem));
		width: clamp(0.3rem, 1.8vw, 1rem);
		text-align: center;
		color: #d7aa55;
		font-size: 0.9rem;
		opacity: 0.18;
	}
	.tube-bead.filled:has(+ .tube-bead.filled)::after {
		opacity: 0.9;
		text-shadow: 0 0 8px rgba(215, 170, 85, 0.55);
	}
	.tube-bead img {
		width: clamp(1.9rem, 4vw, 2.7rem);
		height: clamp(1.9rem, 4vw, 2.7rem);
		border: 1px solid rgba(190, 139, 58, 0.6);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
		box-shadow: inset 0 0 0.4rem #000;
	}
	.tube-bead.blass img {
		opacity: 0.26;
		filter: grayscale(0.45);
	}
	.tube-bead.blass .bead-name {
		opacity: 0.35;
	}
	.tube-bead.active img {
		border-color: rgba(222, 178, 96, 0.95);
		box-shadow:
			inset 0 0 0.4rem #000,
			0 0 0.6rem rgba(215, 170, 85, 0.35);
	}
	/* Fokussierbar seit der Titelbereich-Neuordnung: der Erklärsatz liegt an der
	   Kugel und muss per Tastatur erreichbar sein — die Kugel ist kein Link,
	   aber ein Tab-Stopp mit sichtbarem Ring. (Löst den früheren Steward-B1-
	   Beschluss „keine Tab-Stopps" ab — die Steward-Vorgabe in
	   docs/titelbereich-neuordnung-fuer-kimi.md verlangt die Erreichbarkeit.) */
	.tube-bead:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
		border-radius: 0.35rem;
	}
	/* Der Erklärsatz AN der Kugel: immer im DOM (No-JS/Screenreader-Wahrheit),
	   sichtbar bei Hover/Fokus — reines CSS, kein JS. Schwebt mit eigenem
	   Scrim über der Kugel, damit er über dem Plate lesbar bleibt. */
	.bead-text {
		position: absolute;
		bottom: calc(100% + 0.45rem);
		left: 50%;
		transform: translateX(-50%);
		width: max-content;
		max-width: 13rem;
		padding: 0.4rem 0.6rem;
		background: rgba(5, 9, 11, 0.88);
		border: 1px solid rgba(190, 139, 58, 0.45);
		border-radius: 0.4rem;
		color: #e2d8c0;
		font-size: 0.75rem;
		line-height: 1.4;
		opacity: 0;
		pointer-events: none;
		transition: opacity 0.18s ease;
		z-index: 2;
	}
	/* Randkugeln: die Text-Box bleibt im Viewport — erste Kugel links, letzte
	   rechts ausgerichtet (B1-Disziplin: nie horizontal aufblähen). */
	.tube-bead:first-child .bead-text {
		left: 0;
		transform: none;
	}
	.tube-bead:last-child .bead-text {
		left: auto;
		right: 0;
		transform: none;
	}
	.tube-bead:hover .bead-text,
	.tube-bead:focus .bead-text,
	.tube-bead:focus-visible .bead-text {
		opacity: 1;
	}
	@media (prefers-reduced-motion: reduce) {
		.bead-text {
			transition: none;
		}
	}

	/* ---- Röhren-Diff (Vertical Slice) -------------------------------------
	   Nur im JS-Ankunftspfad (Klassen von stage.js primeTubeDiff): die Röhre
	   reist mit dem Herkunfts-Füllstand; nach der Fahrt entfernt playStage
	   die Klassen und CSS-Transitions spielen den Diff auf den SSR-Zielstand.
	   SSR/No-JS sieht diese Klassen nie — das pragerenderte HTML ist Wahrheit. */
	.tube-bead.tube-diff-in img {
		opacity: 0.26;
		filter: grayscale(0.45);
		border-color: rgba(190, 139, 58, 0.6);
		box-shadow: inset 0 0 0.4rem #000;
	}
	.tube-bead.tube-diff-in .bead-name {
		opacity: 0.35;
	}
	.tube-bead.tube-diff-out img {
		opacity: 1;
		filter: none;
	}
	.tube-bead.tube-diff-out .bead-name {
		opacity: 1;
	}
	/* Pfeile folgen dem sichtbaren Zustand, nicht den SSR-Klassen. */
	.tube-bead.filled:has(+ .tube-bead.filled.tube-diff-in)::after,
	.tube-bead.filled.tube-diff-in:has(+ .tube-bead.filled)::after {
		opacity: 0.18;
		text-shadow: none;
	}
	.tube-bead:has(+ .tube-bead.tube-diff-out)::after {
		opacity: 0.9;
		text-shadow: 0 0 8px rgba(215, 170, 85, 0.55);
	}
	@media (prefers-reduced-motion: no-preference) {
		.tube-bead img,
		.tube-bead .bead-name {
			transition:
				opacity 0.5s ease,
				filter 0.5s ease,
				border-color 0.5s ease,
				box-shadow 0.5s ease;
			transition-delay: calc(var(--i) * 90ms);
		}
		.tube-bead::after {
			transition: opacity 0.5s ease;
			transition-delay: calc(var(--i) * 90ms);
		}
	}
	.bead-name {
		color: #d8c9a3;
		font: 600 0.56rem ui-sans-serif, system-ui;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		text-shadow: 0 1px 8px rgba(3, 6, 7, 0.9);
		hyphens: auto;
		overflow-wrap: break-word;
		/* Nie breiter als die Perle — sonst bläht min-content die Schiene
		   über den Viewport (B1-Befund bei 320 px). */
		max-width: 100%;
	}

	/* Eintritts-Takt 5: Röhrenhülle, dann Perlen gestaffelt von rechts.
	   Anfangszustände nur unter stage-armed (JS) + no-preference. */
	@media (prefers-reduced-motion: no-preference) {
		:global(html.stage-armed) .beat-tube {
			opacity: 0;
		}
		:global(html.stage-armed.stage-play) .beat-tube {
			/* Endwert explizit — das implizite `to` liest sonst opacity: 0 mit. */
			opacity: 1;
			animation: tube-in 0.4s ease-out 1.3s both;
		}
		:global(html.stage-armed) .tube-bead {
			opacity: 0;
		}
		:global(html.stage-armed.stage-play) .tube-bead {
			opacity: 1;
			animation: bead-in 0.35s ease-out both;
			animation-delay: calc(1350ms + var(--i) * 70ms);
		}
		:global(html.stage-skip) .beat-tube,
		:global(html.stage-skip) .tube-bead {
			animation-duration: 0.01ms !important;
			animation-delay: 0ms !important;
		}
		/* Beim Scrollen nach dem Lock weicht die Röhre dezent zurück. */
		.stage-tube {
			transition:
				opacity 0.4s ease,
				transform 0.4s ease;
		}
		:global(html.stage-unlocked) .stage-tube {
			opacity: 0.45;
			transform: translateY(6px);
		}
	}

	@media (max-width: 700px) {
		.stage-tube {
			padding: 1rem 0.5rem 0.6rem;
			gap: 0.3rem;
		}
		.tube-bead {
			width: 2.95rem;
		}
		.bead-name {
			font-size: 0.5rem;
		}
		.bead-text {
			max-width: 11rem;
			font-size: 0.7rem;
		}
	}

	/* 320-px-Klasse (B1): Schiene muss inkl. Padding in den Viewport —
	   6 Perlen + 5 Lücken + 0,5rem Seitenpolster ≤ 320 px. */
	@media (max-width: 360px) {
		.stage-tube {
			padding: 0.9rem 0.25rem 0.55rem;
		}
		.tube-rail {
			gap: 0.2rem;
		}
		.tube-bead {
			width: 2.5rem;
		}
		.tube-bead:not(:last-child)::after {
			right: -0.2rem;
			width: 0.2rem;
			font-size: 0.7rem;
		}
		.tube-bead img {
			width: 1.7rem;
			height: 1.7rem;
		}
		.bead-name {
			font-size: 0.46rem;
		}
		.bead-text {
			max-width: 9.5rem;
		}
	}

	@keyframes tube-in {
		from {
			opacity: 0;
		}
	}
	/* Die Perlen laufen von rechts ein — wie Kugeln in ihre Fassungen. */
	@keyframes bead-in {
		from {
			opacity: 0;
			transform: translateX(14px) scale(0.85);
		}
	}
</style>
