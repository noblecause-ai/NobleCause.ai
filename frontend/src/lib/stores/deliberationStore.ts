import { writable } from 'svelte/store';

export interface DeliberationMessage {
	type: string;
	agent: string;
	content: string;
	timestamp: string;
}

// Create a writable store to hold the deliberation transcript
export const deliberationStore = writable<DeliberationMessage[]>([]);