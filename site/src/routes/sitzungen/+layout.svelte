<script>
	import ExplorerShell from '$lib/components/ExplorerShell.svelte';
	let { children } = $props();
</script>

<ExplorerShell>{@render children()}</ExplorerShell>
