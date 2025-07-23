<script lang="ts">
	import { onMount } from 'svelte';
	import HealthCheck from '$lib/components/HealthCheck.svelte';
	import Deliberation from '$lib/components/Deliberation.svelte';

	let monologue: string = 'Loading...';
	let status: string = 'loading';

	async function fetchStewardStatus() {
		try {
			const response = await fetch('/api/status');
			if (response.ok) {
				const data = await response.json();
				status = data.status;
				monologue = data.inner_monologue;
			} else {
				status = 'error';
				monologue = 'Failed to fetch status';
			}
		} catch (error) {
			status = 'error';
			monologue = 'Network error';
		}
	}

	onMount(() => {
		fetchStewardStatus();
	});
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<div>
	<h2>Steward Status</h2>
	<p>Status: {status}</p>
	<p data-testid="steward-monologue">{monologue}</p>
</div>

<HealthCheck />
<Deliberation />
