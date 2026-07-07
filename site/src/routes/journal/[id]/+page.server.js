import { getJournalEntry, listJournalEntries } from '$lib/server/content.js';

export function entries() {
	return listJournalEntries().map((e) => ({ id: e.id }));
}

export function load({ params }) {
	return { entry: getJournalEntry(params.id) };
}
