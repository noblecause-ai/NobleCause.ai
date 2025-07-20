<script lang="ts">
	import { onMount } from 'svelte';
	
	let status: 'Loading...' | 'OK' | 'Error' = 'Loading...';
	
	export async function checkHealth() {
		try {
			const response = await fetch('http://localhost:8000/health');
			if (response.ok) {
				await response.json();
				status = 'OK';
			} else {
				status = 'Error';
			}
		} catch (error) {
			status = 'Error';
		}
	}
	
	// Only call onMount if we're in a browser environment
	if (typeof window !== 'undefined') {
		onMount(checkHealth);
	}
</script>

<div>
	<h2>Health Check</h2>
	<p>Status: {status}</p>
</div>