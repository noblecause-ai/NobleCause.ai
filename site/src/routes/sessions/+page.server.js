import { getAllSessions, getOrganizations } from '$lib/server/content.js';
import { buildSessionSummaries } from '$lib/server/homepage.js';

export function load() {
	// Je Sitzung ein Bereichs-Kurzstatus (Zählstand + genannte Organisation),
	// lenient aufgelöst — der Explorer läuft über alle Sitzungen.
	return { sessions: buildSessionSummaries(getAllSessions(), getOrganizations()) };
}
