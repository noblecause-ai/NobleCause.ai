import { deliberationStore, type WebSocketMessage } from '../stores/deliberationStore';

/**
 * WebSocket service for managing deliberation connections.
 */
class WebSocketService {
	private ws: WebSocket | null = null;
	private wsUrl: string;

	constructor() {
		// Use environment variable or default to localhost
		const apiUrl =
			typeof window !== 'undefined'
				? (import.meta.env?.VITE_API_URL as string | undefined) || 'http://localhost:8000'
				: 'http://localhost:8000';

		// Convert HTTP URL to WebSocket URL
		this.wsUrl = apiUrl.replace('http://', 'ws://').replace('https://', 'wss://');
	}

	/**
	 * Start a new deliberation session.
	 *
	 * @param topic - The topic to deliberate on.
	 */
	startDeliberation(topic: string): void {
		// Reset store and set connecting state
		deliberationStore.reset();
		deliberationStore.setConnecting();

		// Close any existing connection
		this.closeConnection();

		try {
			// Create WebSocket connection
			this.ws = new WebSocket(`${this.wsUrl}/ws/deliberate`);

			this.ws.onopen = () => {
				console.log('WebSocket connected');
				// Send start message
				this.ws?.send(
					JSON.stringify({
						type: 'start_deliberation',
						topic
					})
				);
			};

			this.ws.onmessage = (event) => {
				try {
					const message: WebSocketMessage = JSON.parse(event.data);
					deliberationStore.handleMessage(message);
				} catch (error) {
					console.error('Failed to parse WebSocket message:', error);
				}
			};

			this.ws.onerror = (error) => {
				console.error('WebSocket error:', error);
				deliberationStore.setError('WebSocket connection failed');
			};

			this.ws.onclose = (event) => {
				console.log('WebSocket closed:', event.code, event.reason);
				this.ws = null;
			};
		} catch (error) {
			console.error('Failed to create WebSocket:', error);
			deliberationStore.setError('Failed to connect to server');
		}
	}

	/**
	 * Cancel the current deliberation and close the connection.
	 */
	cancelDeliberation(): void {
		this.closeConnection();
		deliberationStore.reset();
	}

	/**
	 * Close the WebSocket connection if open.
	 */
	private closeConnection(): void {
		if (this.ws) {
			this.ws.close();
			this.ws = null;
		}
	}

	/**
	 * Check if a connection is currently open.
	 */
	isConnected(): boolean {
		return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
	}
}

/**
 * Singleton instance of the WebSocket service.
 */
export const websocketService = new WebSocketService();
