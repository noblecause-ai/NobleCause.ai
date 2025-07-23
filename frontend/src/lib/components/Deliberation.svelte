<script lang="ts">
	import { deliberationStore, type DeliberationMessage } from '../stores/deliberationStore';
	
	let isConnected = false;
	let eventSource: EventSource | null = null;
	
	function startDeliberation() {
		if (!isConnected) {
			eventSource = new EventSource('http://localhost:8000/api/deliberate');
			isConnected = true;
			
			// Set up message handler to update store
			eventSource.onmessage = (event) => {
				try {
					const message: DeliberationMessage = JSON.parse(event.data);
					const currentMessages = $deliberationStore;
					deliberationStore.set([...currentMessages, message]);
				} catch (error) {
					console.error('Failed to parse SSE message:', error);
				}
			};
			
			eventSource.onerror = (error) => {
				console.error('SSE connection error:', error);
				isConnected = false;
			};
		}
	}
</script>

<div>
	<button on:click={startDeliberation} disabled={isConnected}>
		Start Deliberation
	</button>
	
	<div data-testid="transcript-area">
		{#each $deliberationStore as message}
			<div class="message">
				<strong>{message.agent}:</strong> {message.content}
				<small>({message.timestamp})</small>
			</div>
		{/each}
	</div>
</div>

<style>
	.message {
		margin: 0.5rem 0;
		padding: 0.5rem;
		border-left: 3px solid #007bff;
		background-color: #f8f9fa;
	}
	
	button {
		padding: 0.5rem 1rem;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}
	
	button:disabled {
		background-color: #6c757d;
		cursor: not-allowed;
	}
</style>