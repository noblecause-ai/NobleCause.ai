import { listSessions } from '$lib/server/content.js';

export function load() {
	return { sessions: listSessions() };
}
