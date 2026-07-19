<script>
	// Eine Tür: Bild-Kachel als echter Link in einen anderen Raum.
	// Rahmen und Beschriftung tragen die Anklickbarkeit (auch bei dunklem Bild).
	let { door } = $props();
</script>

<a class="door" href={door.href}>
	<img src={door.img} alt={door.alt} width={door.width} height={door.height} loading="lazy" />
	<span class="door-label">
		<small>{door.sub}</small>
		<strong>{door.label} →</strong>
	</span>
</a>

<style>
	.door {
		display: grid;
		grid-template-rows: 1fr auto;
		overflow: hidden;
		border: 1px solid rgba(166, 123, 61, 0.55);
		background: #0a0e0f;
		text-decoration: none;
		box-shadow: 0 1rem 2.5rem rgba(0, 0, 0, 0.45);
		transition:
			transform 0.25s ease,
			border-color 0.25s ease,
			box-shadow 0.25s ease;
	}
	.door:hover,
	.door:focus-visible {
		transform: translateY(-3px);
		border-color: #d7aa55;
		box-shadow: 0 1.2rem 3rem rgba(0, 0, 0, 0.6), 0 0 1.2rem rgba(215, 170, 85, 0.28);
	}
	.door:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	img {
		width: 100%;
		height: 100%;
		min-height: 12rem;
		max-height: 17rem;
		object-fit: cover;
		display: block;
	}
	.door-label {
		display: grid;
		gap: 0.15rem;
		min-height: 44px;
		padding: 0.7rem 0.9rem;
		background: linear-gradient(rgba(15, 20, 21, 0.98), rgba(10, 14, 15, 0.98));
		border-top: 1px solid rgba(166, 123, 61, 0.4);
	}
	small {
		color: #a99062;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	strong {
		color: #e7c881;
		font-size: 1.02rem;
	}
</style>
