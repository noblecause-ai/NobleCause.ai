import { writable, derived } from 'svelte/store';

/**
 * Agent response from a deliberation round.
 */
export interface AgentResponse {
	agent_id: string;
	agent_name: string;
	round: number;
	round_name: string;
	content: string;
	timestamp: string;
}

/**
 * Overall deliberation state.
 */
export interface DeliberationState {
	status: 'idle' | 'connecting' | 'deliberating' | 'completed' | 'error';
	currentRound: number;
	currentRoundName: string;
	currentAgent: string | null;
	transcript: AgentResponse[];
	consensusReached: boolean;
	finalRecommendation: string | null;
	sessionId: string | null;
	errorMessage: string | null;
}

/**
 * WebSocket message types from backend.
 */
export type WebSocketMessage =
	| { type: 'round_start'; round: number; round_name: string }
	| { type: 'agent_start'; agent_id: string; agent_name: string; round: number; round_name: string }
	| {
			type: 'agent_response';
			agent_id: string;
			agent_name: string;
			round: number;
			round_name: string;
			content: string;
			timestamp: string;
	  }
	| { type: 'round_end'; round: number }
	| {
			type: 'deliberation_complete';
			session_id: string;
			consensus_reached: boolean;
			final_recommendation: string | null;
	  }
	| { type: 'error'; message: string };

/**
 * Initial state for the deliberation store.
 */
const initialState: DeliberationState = {
	status: 'idle',
	currentRound: 0,
	currentRoundName: '',
	currentAgent: null,
	transcript: [],
	consensusReached: false,
	finalRecommendation: null,
	sessionId: null,
	errorMessage: null
};

/**
 * Create the main deliberation store.
 */
function createDeliberationStore() {
	const { subscribe, set, update } = writable<DeliberationState>(initialState);

	return {
		subscribe,

		/**
		 * Reset to initial state.
		 */
		reset: () => set(initialState),

		/**
		 * Set status to connecting.
		 */
		setConnecting: () =>
			update((state) => ({
				...state,
				status: 'connecting',
				errorMessage: null
			})),

		/**
		 * Handle a WebSocket message and update state accordingly.
		 */
		handleMessage: (message: WebSocketMessage) => {
			update((state) => {
				switch (message.type) {
					case 'round_start':
						return {
							...state,
							status: 'deliberating',
							currentRound: message.round,
							currentRoundName: message.round_name,
							currentAgent: null
						};

					case 'agent_start':
						return {
							...state,
							currentAgent: message.agent_name
						};

					case 'agent_response':
						return {
							...state,
							transcript: [
								...state.transcript,
								{
									agent_id: message.agent_id,
									agent_name: message.agent_name,
									round: message.round,
									round_name: message.round_name,
									content: message.content,
									timestamp: message.timestamp
								}
							],
							currentAgent: null
						};

					case 'round_end':
						return {
							...state,
							currentAgent: null
						};

					case 'deliberation_complete':
						return {
							...state,
							status: 'completed',
							sessionId: message.session_id,
							consensusReached: message.consensus_reached,
							finalRecommendation: message.final_recommendation,
							currentAgent: null
						};

					case 'error':
						return {
							...state,
							status: 'error',
							errorMessage: message.message,
							currentAgent: null
						};

					default:
						return state;
				}
			});
		},

		/**
		 * Set error state with message.
		 */
		setError: (message: string) =>
			update((state) => ({
				...state,
				status: 'error',
				errorMessage: message,
				currentAgent: null
			}))
	};
}

/**
 * Main deliberation store instance.
 */
export const deliberationStore = createDeliberationStore();

/**
 * Derived store: transcript grouped by round.
 */
export const transcriptByRound = derived(deliberationStore, ($store) => {
	const byRound: Record<number, { round_name: string; responses: AgentResponse[] }> = {};

	for (const response of $store.transcript) {
		if (!byRound[response.round]) {
			byRound[response.round] = {
				round_name: response.round_name,
				responses: []
			};
		}
		byRound[response.round].responses.push(response);
	}

	return byRound;
});

/**
 * Derived store: is deliberation in progress?
 */
export const isDeliberating = derived(
	deliberationStore,
	($store) => $store.status === 'connecting' || $store.status === 'deliberating'
);
