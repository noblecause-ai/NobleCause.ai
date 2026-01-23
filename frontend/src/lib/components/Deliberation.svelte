<script lang="ts">
	import {
		deliberationStore,
		transcriptByRound,
		isDeliberating
	} from '../stores/deliberationStore';
	import { websocketService } from '../services/websocketService';

	let topic = '';

	function handleStart() {
		if (topic.trim()) {
			websocketService.startDeliberation(topic.trim());
		}
	}

	function handleCancel() {
		websocketService.cancelDeliberation();
	}

	function handleReset() {
		deliberationStore.reset();
		topic = '';
	}

	// Round colors for visual distinction
	const roundColors: Record<number, string> = {
		1: '#4CAF50', // Green for Propose
		2: '#FF9800', // Orange for Critique
		3: '#2196F3' // Blue for Synthesize
	};
</script>

<div class="deliberation-container">
	<!-- Topic Input Section -->
	<div class="input-section">
		<label for="topic-input">Deliberation Topic</label>
		<textarea
			id="topic-input"
			bind:value={topic}
			placeholder="Enter the topic for the Gremium to deliberate on..."
			disabled={$isDeliberating}
			rows="3"
		></textarea>

		<div class="button-group">
			{#if $deliberationStore.status === 'idle'}
				<button
					class="primary-button"
					onclick={handleStart}
					disabled={!topic.trim()}
					data-testid="start-button"
				>
					Start Deliberation
				</button>
			{:else if $isDeliberating}
				<button class="cancel-button" onclick={handleCancel} data-testid="cancel-button">
					Cancel
				</button>
			{:else}
				<button class="reset-button" onclick={handleReset} data-testid="reset-button">
					New Deliberation
				</button>
			{/if}
		</div>
	</div>

	<!-- Status Bar -->
	{#if $deliberationStore.status !== 'idle'}
		<div
			class="status-bar"
			class:connecting={$deliberationStore.status === 'connecting'}
			class:deliberating={$deliberationStore.status === 'deliberating'}
			class:completed={$deliberationStore.status === 'completed'}
			class:error={$deliberationStore.status === 'error'}
			data-testid="status-bar"
		>
			{#if $deliberationStore.status === 'connecting'}
				<span class="spinner"></span>
				Connecting...
			{:else if $deliberationStore.status === 'deliberating'}
				<span class="spinner"></span>
				Round {$deliberationStore.currentRound}: {$deliberationStore.currentRoundName}
				{#if $deliberationStore.currentAgent}
					<span class="agent-indicator">- {$deliberationStore.currentAgent} is thinking...</span>
				{/if}
			{:else if $deliberationStore.status === 'completed'}
				Deliberation Complete
				{#if $deliberationStore.consensusReached}
					<span class="consensus-badge">Consensus Reached</span>
				{/if}
			{:else if $deliberationStore.status === 'error'}
				Error: {$deliberationStore.errorMessage}
			{/if}
		</div>
	{/if}

	<!-- Transcript Section -->
	<div class="transcript-section" data-testid="transcript-area">
		{#each Object.entries($transcriptByRound) as [roundNum, roundData]}
			<div class="round-section" style="--round-color: {roundColors[Number(roundNum)] || '#666'}">
				<h3 class="round-header">
					Round {roundNum}: {roundData.round_name}
				</h3>

				{#each roundData.responses as response}
					<div class="response-card">
						<div class="response-header">
							<span class="agent-name">{response.agent_name}</span>
							<span class="timestamp">
								{new Date(response.timestamp).toLocaleTimeString()}
							</span>
						</div>
						<div class="response-content">
							{response.content}
						</div>
					</div>
				{/each}
			</div>
		{/each}

		{#if $deliberationStore.transcript.length === 0 && $deliberationStore.status === 'idle'}
			<p class="placeholder-text">
				Enter a topic above to begin a 3-round deliberation with the AI Gremium.
			</p>
		{/if}
	</div>

	<!-- Completion Section -->
	{#if $deliberationStore.status === 'completed' && $deliberationStore.finalRecommendation}
		<div class="completion-section" data-testid="completion-section">
			<h3>Final Recommendation</h3>
			<div class="recommendation-content">
				{$deliberationStore.finalRecommendation}
			</div>
		</div>
	{/if}
</div>

<style>
	.deliberation-container {
		max-width: 900px;
		margin: 0 auto;
		padding: 1rem;
	}

	.input-section {
		margin-bottom: 1.5rem;
	}

	.input-section label {
		display: block;
		font-weight: 600;
		margin-bottom: 0.5rem;
		color: #333;
	}

	textarea {
		width: 100%;
		padding: 0.75rem;
		border: 2px solid #e0e0e0;
		border-radius: 8px;
		font-size: 1rem;
		resize: vertical;
		font-family: inherit;
	}

	textarea:focus {
		outline: none;
		border-color: #2196f3;
	}

	textarea:disabled {
		background-color: #f5f5f5;
		cursor: not-allowed;
	}

	.button-group {
		margin-top: 1rem;
		display: flex;
		gap: 0.5rem;
	}

	button {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 6px;
		font-size: 1rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
	}

	.primary-button {
		background-color: #2196f3;
		color: white;
	}

	.primary-button:hover:not(:disabled) {
		background-color: #1976d2;
	}

	.primary-button:disabled {
		background-color: #bdbdbd;
		cursor: not-allowed;
	}

	.cancel-button {
		background-color: #f44336;
		color: white;
	}

	.cancel-button:hover {
		background-color: #d32f2f;
	}

	.reset-button {
		background-color: #4caf50;
		color: white;
	}

	.reset-button:hover {
		background-color: #388e3c;
	}

	.status-bar {
		padding: 0.75rem 1rem;
		border-radius: 8px;
		margin-bottom: 1.5rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-weight: 500;
	}

	.status-bar.connecting {
		background-color: #fff3e0;
		color: #e65100;
	}

	.status-bar.deliberating {
		background-color: #e3f2fd;
		color: #1565c0;
	}

	.status-bar.completed {
		background-color: #e8f5e9;
		color: #2e7d32;
	}

	.status-bar.error {
		background-color: #ffebee;
		color: #c62828;
	}

	.spinner {
		width: 16px;
		height: 16px;
		border: 2px solid currentColor;
		border-top-color: transparent;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.agent-indicator {
		font-style: italic;
		opacity: 0.8;
	}

	.consensus-badge {
		margin-left: auto;
		background-color: #4caf50;
		color: white;
		padding: 0.25rem 0.75rem;
		border-radius: 20px;
		font-size: 0.875rem;
	}

	.transcript-section {
		min-height: 200px;
	}

	.round-section {
		margin-bottom: 2rem;
		border-left: 4px solid var(--round-color, #666);
		padding-left: 1rem;
	}

	.round-header {
		color: var(--round-color, #666);
		margin: 0 0 1rem 0;
		font-size: 1.25rem;
	}

	.response-card {
		background-color: #fafafa;
		border-radius: 8px;
		padding: 1rem;
		margin-bottom: 1rem;
		border: 1px solid #e0e0e0;
	}

	.response-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 0.5rem;
	}

	.agent-name {
		font-weight: 600;
		color: #333;
	}

	.timestamp {
		color: #757575;
		font-size: 0.875rem;
	}

	.response-content {
		color: #444;
		line-height: 1.6;
		white-space: pre-wrap;
	}

	.placeholder-text {
		color: #757575;
		text-align: center;
		padding: 2rem;
		font-style: italic;
	}

	.completion-section {
		background-color: #f3e5f5;
		border-radius: 8px;
		padding: 1.5rem;
		margin-top: 2rem;
		border: 2px solid #9c27b0;
	}

	.completion-section h3 {
		color: #7b1fa2;
		margin: 0 0 1rem 0;
	}

	.recommendation-content {
		color: #333;
		line-height: 1.6;
		white-space: pre-wrap;
	}
</style>
