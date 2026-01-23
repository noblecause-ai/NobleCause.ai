import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { get } from 'svelte/store';
import {
	deliberationStore,
	transcriptByRound,
	isDeliberating,
	type WebSocketMessage
} from '../stores/deliberationStore';

// Mock WebSocket
class MockWebSocket {
	url: string;
	readyState: number = 0;
	onopen: ((event: Event) => void) | null = null;
	onmessage: ((event: MessageEvent) => void) | null = null;
	onerror: ((event: Event) => void) | null = null;
	onclose: ((event: CloseEvent) => void) | null = null;

	static CONNECTING = 0;
	static OPEN = 1;
	static CLOSING = 2;
	static CLOSED = 3;

	constructor(url: string) {
		this.url = url;
		// Simulate connection opening
		setTimeout(() => {
			this.readyState = MockWebSocket.OPEN;
			if (this.onopen) {
				this.onopen(new Event('open'));
			}
		}, 0);
	}

	send(data: string) {
		// Mock send - do nothing
	}

	close() {
		this.readyState = MockWebSocket.CLOSED;
		if (this.onclose) {
			this.onclose(new CloseEvent('close'));
		}
	}

	// Helper method for tests to simulate receiving messages
	simulateMessage(data: WebSocketMessage) {
		if (this.onmessage) {
			const event = new MessageEvent('message', { data: JSON.stringify(data) });
			this.onmessage(event);
		}
	}

	// Helper to simulate error
	simulateError() {
		if (this.onerror) {
			this.onerror(new Event('error'));
		}
	}
}

describe('DeliberationStore', () => {
	beforeEach(() => {
		// Reset the deliberation store before each test
		deliberationStore.reset();
	});

	it('test_initial_state', () => {
		const state = get(deliberationStore);

		expect(state.status).toBe('idle');
		expect(state.currentRound).toBe(0);
		expect(state.currentRoundName).toBe('');
		expect(state.currentAgent).toBeNull();
		expect(state.transcript).toEqual([]);
		expect(state.consensusReached).toBe(false);
		expect(state.finalRecommendation).toBeNull();
		expect(state.sessionId).toBeNull();
		expect(state.errorMessage).toBeNull();
	});

	it('test_handles_round_start_message', () => {
		const message: WebSocketMessage = {
			type: 'round_start',
			round: 1,
			round_name: 'Propose'
		};

		deliberationStore.handleMessage(message);

		const state = get(deliberationStore);
		expect(state.status).toBe('deliberating');
		expect(state.currentRound).toBe(1);
		expect(state.currentRoundName).toBe('Propose');
	});

	it('test_handles_agent_start_message', () => {
		const message: WebSocketMessage = {
			type: 'agent_start',
			agent_id: 'claude',
			agent_name: 'Claude',
			round: 1,
			round_name: 'Propose'
		};

		deliberationStore.handleMessage(message);

		const state = get(deliberationStore);
		expect(state.currentAgent).toBe('Claude');
	});

	it('test_handles_agent_response_message', () => {
		const message: WebSocketMessage = {
			type: 'agent_response',
			agent_id: 'claude',
			agent_name: 'Claude',
			round: 1,
			round_name: 'Propose',
			content: 'This is my proposal.',
			timestamp: '2024-01-01T00:00:00Z'
		};

		deliberationStore.handleMessage(message);

		const state = get(deliberationStore);
		expect(state.transcript).toHaveLength(1);
		expect(state.transcript[0].agent_name).toBe('Claude');
		expect(state.transcript[0].content).toBe('This is my proposal.');
		expect(state.currentAgent).toBeNull();
	});

	it('test_handles_deliberation_complete_message', () => {
		const message: WebSocketMessage = {
			type: 'deliberation_complete',
			session_id: 'test-session-123',
			consensus_reached: true,
			final_recommendation: 'We recommend...'
		};

		deliberationStore.handleMessage(message);

		const state = get(deliberationStore);
		expect(state.status).toBe('completed');
		expect(state.sessionId).toBe('test-session-123');
		expect(state.consensusReached).toBe(true);
		expect(state.finalRecommendation).toBe('We recommend...');
	});

	it('test_handles_error_message', () => {
		const message: WebSocketMessage = {
			type: 'error',
			message: 'Connection failed'
		};

		deliberationStore.handleMessage(message);

		const state = get(deliberationStore);
		expect(state.status).toBe('error');
		expect(state.errorMessage).toBe('Connection failed');
	});

	it('test_reset_returns_to_initial_state', () => {
		// First, modify the state
		deliberationStore.handleMessage({
			type: 'round_start',
			round: 1,
			round_name: 'Propose'
		});

		// Then reset
		deliberationStore.reset();

		const state = get(deliberationStore);
		expect(state.status).toBe('idle');
		expect(state.currentRound).toBe(0);
		expect(state.transcript).toEqual([]);
	});
});

describe('Derived Stores', () => {
	beforeEach(() => {
		deliberationStore.reset();
	});

	it('test_transcript_by_round_groups_responses', () => {
		// Add responses from multiple rounds
		deliberationStore.handleMessage({
			type: 'agent_response',
			agent_id: 'claude',
			agent_name: 'Claude',
			round: 1,
			round_name: 'Propose',
			content: 'Round 1 content',
			timestamp: '2024-01-01T00:00:00Z'
		});

		deliberationStore.handleMessage({
			type: 'agent_response',
			agent_id: 'gpt4',
			agent_name: 'GPT-4',
			round: 1,
			round_name: 'Propose',
			content: 'Also round 1',
			timestamp: '2024-01-01T00:01:00Z'
		});

		deliberationStore.handleMessage({
			type: 'agent_response',
			agent_id: 'claude',
			agent_name: 'Claude',
			round: 2,
			round_name: 'Critique',
			content: 'Round 2 content',
			timestamp: '2024-01-01T00:02:00Z'
		});

		const byRound = get(transcriptByRound);

		expect(Object.keys(byRound)).toHaveLength(2);
		expect(byRound[1].round_name).toBe('Propose');
		expect(byRound[1].responses).toHaveLength(2);
		expect(byRound[2].round_name).toBe('Critique');
		expect(byRound[2].responses).toHaveLength(1);
	});

	it('test_is_deliberating_reflects_status', () => {
		// Initially should be false
		expect(get(isDeliberating)).toBe(false);

		// Set to connecting
		deliberationStore.setConnecting();
		expect(get(isDeliberating)).toBe(true);

		// Set to deliberating
		deliberationStore.handleMessage({
			type: 'round_start',
			round: 1,
			round_name: 'Propose'
		});
		expect(get(isDeliberating)).toBe(true);

		// Set to completed
		deliberationStore.handleMessage({
			type: 'deliberation_complete',
			session_id: 'test',
			consensus_reached: true,
			final_recommendation: null
		});
		expect(get(isDeliberating)).toBe(false);
	});
});

describe('WebSocket Integration', () => {
	let mockWebSocket: MockWebSocket;
	let originalWebSocket: typeof WebSocket;

	beforeEach(() => {
		// Reset store
		deliberationStore.reset();

		// Store original WebSocket
		originalWebSocket = globalThis.WebSocket;

		// Mock WebSocket globally
		globalThis.WebSocket = vi.fn().mockImplementation((url: string) => {
			mockWebSocket = new MockWebSocket(url);
			return mockWebSocket;
		}) as unknown as typeof WebSocket;

		// Add static properties
		(globalThis.WebSocket as unknown as typeof MockWebSocket).CONNECTING = MockWebSocket.CONNECTING;
		(globalThis.WebSocket as unknown as typeof MockWebSocket).OPEN = MockWebSocket.OPEN;
		(globalThis.WebSocket as unknown as typeof MockWebSocket).CLOSING = MockWebSocket.CLOSING;
		(globalThis.WebSocket as unknown as typeof MockWebSocket).CLOSED = MockWebSocket.CLOSED;
	});

	afterEach(() => {
		vi.restoreAllMocks();
		globalThis.WebSocket = originalWebSocket;
	});

	it('test_websocket_creates_connection_with_correct_url', async () => {
		// Import the service (after mocking WebSocket)
		const { websocketService } = await import('../services/websocketService');

		// Start deliberation
		websocketService.startDeliberation('Test topic');

		// Wait for async connection
		await new Promise((resolve) => setTimeout(resolve, 10));

		// Verify WebSocket was created with correct URL pattern
		expect(globalThis.WebSocket).toHaveBeenCalled();
		const callUrl = (globalThis.WebSocket as ReturnType<typeof vi.fn>).mock.calls[0][0];
		expect(callUrl).toContain('/ws/deliberate');
	});

	it('test_full_deliberation_flow_updates_store', async () => {
		const { websocketService } = await import('../services/websocketService');

		websocketService.startDeliberation('Should we fund this?');

		// Wait for connection
		await new Promise((resolve) => setTimeout(resolve, 10));

		// Simulate full deliberation flow
		mockWebSocket.simulateMessage({
			type: 'round_start',
			round: 1,
			round_name: 'Propose'
		});

		let state = get(deliberationStore);
		expect(state.status).toBe('deliberating');
		expect(state.currentRound).toBe(1);

		mockWebSocket.simulateMessage({
			type: 'agent_response',
			agent_id: 'claude',
			agent_name: 'Claude',
			round: 1,
			round_name: 'Propose',
			content: 'My proposal...',
			timestamp: '2024-01-01T00:00:00Z'
		});

		state = get(deliberationStore);
		expect(state.transcript).toHaveLength(1);

		mockWebSocket.simulateMessage({
			type: 'deliberation_complete',
			session_id: 'test-123',
			consensus_reached: true,
			final_recommendation: 'Final recommendation'
		});

		state = get(deliberationStore);
		expect(state.status).toBe('completed');
		expect(state.consensusReached).toBe(true);
	});
});
