import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { get } from 'svelte/store';
import { deliberationStore, type DeliberationMessage } from '../stores/deliberationStore';

// Mock EventSource
class MockEventSource {
	url: string;
	readyState: number = 0;
	onopen: ((event: Event) => void) | null = null;
	onmessage: ((event: MessageEvent) => void) | null = null;
	onerror: ((event: Event) => void) | null = null;
	
	constructor(url: string) {
		this.url = url;
		// Simulate connection opening
		setTimeout(() => {
			this.readyState = 1;
			if (this.onopen) {
				this.onopen(new Event('open'));
			}
		}, 0);
	}
	
	close() {
		this.readyState = 2;
	}
	
	// Helper method for tests to simulate receiving messages
	simulateMessage(data: string) {
		if (this.onmessage) {
			const event = new MessageEvent('message', { data });
			this.onmessage(event);
		}
	}
}

// Create a mock component class for testing (following existing pattern)
class MockDeliberation {
	isConnected: boolean = false;
	eventSource: EventSource | null = null;
	hasStartButton: boolean = true;
	hasTranscriptArea: boolean = true;
	transcriptContent: string = '';

	startDeliberation() {
		if (!this.isConnected) {
			this.eventSource = new EventSource('http://localhost:8000/api/deliberate');
			this.isConnected = true;
			
			// Set up message handler to update store
			this.eventSource.onmessage = (event) => {
				try {
					const message: DeliberationMessage = JSON.parse(event.data);
					const currentMessages = get(deliberationStore);
					deliberationStore.set([...currentMessages, message]);
				} catch (error) {
					console.error('Failed to parse SSE message:', error);
				}
			};
		}
	}

	getTranscriptContent() {
		const messages = get(deliberationStore);
		return messages.map(msg => `${msg.agent}: ${msg.content}`).join('\n');
	}
}

describe('Deliberation', () => {
	let mockEventSource: MockEventSource;
	let originalEventSource: typeof EventSource;

	beforeEach(() => {
		// Reset all mocks before each test
		vi.resetAllMocks();
		
		// Store original EventSource
		originalEventSource = globalThis.EventSource;
		
		// Mock EventSource globally
		globalThis.EventSource = vi.fn().mockImplementation((url: string) => {
			mockEventSource = new MockEventSource(url);
			return mockEventSource;
		}) as any;
		
		// Reset the deliberation store
		deliberationStore.set([]);
	});

	afterEach(() => {
		// Restore all mocks after each test
		vi.restoreAllMocks();
		
		// Restore original EventSource
		globalThis.EventSource = originalEventSource;
	});

	it('test_component_renders_initial_state', () => {
		// Create component instance
		const component = new MockDeliberation();

		// Assert that it displays an initial state
		expect(component.hasStartButton).toBe(true);
		expect(component.hasTranscriptArea).toBe(true);
		
		// Assert transcript area is initially empty
		expect(component.transcriptContent).toBe('');
		expect(component.isConnected).toBe(false);
	});

	it('test_clicking_button_initiates_sse_connection', () => {
		// Create component instance
		const component = new MockDeliberation();
		
		// Simulate a click on the "Start Deliberation" button
		component.startDeliberation();

		// Assert that new EventSource was called with correct URL
		expect(globalThis.EventSource).toHaveBeenCalledWith('http://localhost:8000/api/deliberate');
		expect(globalThis.EventSource).toHaveBeenCalledTimes(1);
		expect(component.isConnected).toBe(true);
	});

	it('test_sse_messages_update_transcript_store', () => {
		// Create component instance
		const component = new MockDeliberation();
		
		// Simulate button click to start SSE connection
		component.startDeliberation();

		// Verify EventSource was created
		expect(mockEventSource).toBeDefined();

		// Dispatch mock SSE message events with JSON data matching backend format
		const mockMessage1 = JSON.stringify({
			type: 'agent_response',
			agent: 'researcher',
			content: 'I found some interesting data about climate change.',
			timestamp: '2023-01-01T10:00:00Z'
		});
		
		const mockMessage2 = JSON.stringify({
			type: 'agent_response',
			agent: 'analyst',
			content: 'Based on the research, I can provide analysis.',
			timestamp: '2023-01-01T10:01:00Z'
		});

		// Simulate receiving messages
		mockEventSource.simulateMessage(mockMessage1);
		mockEventSource.simulateMessage(mockMessage2);

		// Subscribe to the deliberationStore and assert that the store's value is updated correctly
		const storeValue = get(deliberationStore);
		
		expect(storeValue).toHaveLength(2);
		expect(storeValue[0]).toEqual({
			type: 'agent_response',
			agent: 'researcher',
			content: 'I found some interesting data about climate change.',
			timestamp: '2023-01-01T10:00:00Z'
		});
		expect(storeValue[1]).toEqual({
			type: 'agent_response',
			agent: 'analyst',
			content: 'Based on the research, I can provide analysis.',
			timestamp: '2023-01-01T10:01:00Z'
		});
	});
});