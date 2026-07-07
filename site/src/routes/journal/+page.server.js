import { listJournalEntries } from '$lib/server/content.js';

export function load() {
	return { entries: listJournalEntries() };
}
