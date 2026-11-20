<script>
	let { children } = $props();
</script>

<div class="case-shell">{@render children()}</div>

<style>
	:global(.page:has(.case-shell)) { max-width: none; padding: 0; }
	:global(.page:has(.case-shell) > header), :global(.page:has(.case-shell) > footer) { display: none; }
	:global(.page:has(.case-shell) > main) { margin: 0; padding: 0; max-width: none; }
	.case-shell { position: relative; color: #e7dcc4; background: #05090b; }
</style>
