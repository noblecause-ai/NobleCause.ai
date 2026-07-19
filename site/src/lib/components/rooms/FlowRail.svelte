<script>
	// Prozess-Leiste: die sechs kanonischen Schritte als gerichteter Fluss —
	// geteilt zwischen The Study und The Council. Schritt 3 trägt die
	// Teilnehmerzahl aus den Daten (das Locale liefert text als Funktion von n).
	let { flow, participantCount, title } = $props();

	let steps = $derived(
		flow.map((step) => ({
			...step,
			label: typeof step.text === 'function' ? step.text(participantCount) : step.text
		}))
	);
</script>

<section class="room-section" aria-labelledby="flow-title">
	<h2 id="flow-title">{title}</h2>
	<ol class="flow-steps">
		{#each steps as step (step.name)}
			<li class="flow-step">
				<img src={step.src} alt="" width="96" height="96" />
				<strong>{step.name}</strong>
				<span>{step.label}</span>
			</li>
		{/each}
	</ol>
</section>

<style>
	/* Sechs kanonische Schritte, gerichtet: Pfeile als ::after (Bernstein) —
	   Desktop horizontal, Mobil 3×2-Matrix mit Richtungswechsel „↓" zwischen
	   den Reihen. */
	.flow-steps {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		align-items: stretch;
		gap: 0.6rem;
	}
	.flow-step {
		position: relative;
		flex: 1;
		min-width: 0;
		display: grid;
		justify-items: center;
		align-content: start;
		gap: 0.5rem;
		padding: 0 0.9rem;
		text-align: center;
	}
	.flow-step::after {
		content: '→';
		position: absolute;
		right: -0.55rem;
		top: calc(3rem - 0.75em);
		color: #d7aa55;
		font-size: 1.4rem;
	}
	.flow-step:last-child::after {
		content: none;
	}
	.flow-step img {
		width: 6rem;
		height: 6rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
		box-shadow:
			inset 0 0 0.5rem #000,
			0 0 0.45rem rgba(205, 153, 69, 0.12);
	}
	.flow-step strong {
		color: #ead8ae;
		font-size: 0.98rem;
		font-weight: 600;
	}
	.flow-step span {
		color: #bfb49c;
		font-size: 0.84rem;
		line-height: 1.4;
	}

	@media (max-width: 700px) {
		.flow-steps {
			display: grid;
			grid-template-columns: repeat(3, 1fr);
			gap: 1.9rem 0.5rem;
		}
		.flow-step {
			padding: 0 0.25rem;
		}
		.flow-step img {
			width: 4.5rem;
			height: 4.5rem;
		}
		/* Schmale Spalten (~100 px): lange Wörter sauber brechen. */
		.flow-step span {
			font-size: 0.78rem;
			hyphens: auto;
			overflow-wrap: break-word;
		}
		.flow-step strong {
			font-size: 0.88rem;
			hyphens: auto;
			overflow-wrap: break-word;
		}
		.flow-step::after {
			right: -0.45rem;
			top: calc(2.25rem - 0.6em);
			font-size: 1.1rem;
		}
		/* Richtungswechsel am Reihenende: Schritt 3 zeigt nach unten. */
		.flow-step:nth-child(3)::after {
			content: '↓';
			right: auto;
			left: 50%;
			top: auto;
			bottom: -1.5rem;
			transform: translateX(-50%);
		}
	}
</style>
