<script>
	// Legende aus Emblem + Alltagswort (Säulen oder Prozessschritte).
	// Embleme sind hier dekorativ (alt=""), der sichtbare Begriff trägt die Information.
	let { items, label, cols = 4 } = $props();
</script>

<ul class="emblem-legend" style="--cols:{cols}" aria-label={label}>
	{#each items as item (item.label)}
		<li>
			<img src={item.src} alt="" width="48" height="48" />
			<strong>{item.label}</strong>
		</li>
	{/each}
</ul>

<style>
	.emblem-legend {
		display: grid;
		grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
		gap: 0.7rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	li {
		display: grid;
		justify-items: center;
		gap: 0.4rem;
		min-width: 0;
		text-align: center;
	}
	img {
		width: 3rem;
		height: 3rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
		box-shadow:
			inset 0 0 0.5rem #000,
			0 0 0.45rem rgba(205, 153, 69, 0.12);
	}
	strong {
		color: #d8c7a5;
		font: 600 0.72rem ui-sans-serif, system-ui;
		line-height: 1.25;
	}
	@media (max-width: 560px) {
		.emblem-legend {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}
</style>
