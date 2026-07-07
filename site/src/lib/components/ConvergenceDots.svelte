<script>
	let { count = 0, total = 3 } = $props();
	const positions = [6, 21, 36];
</script>

<svg width="42" height="12" viewBox="0 0 42 12" role="img" aria-label="Konvergenz {count} von {total}">
	{#each positions.slice(0, total) as cx, i (cx)}
		{#if i < count}
			<circle {cx} cy="6" r="5" fill="var(--life)" />
		{:else}
			<circle {cx} cy="6" r="5" fill="none" stroke="var(--structure)" stroke-width="1.5" />
		{/if}
	{/each}
</svg>
