import { getLatestSession, listSessions } from '$lib/server/content.js';

export function load() {
	const latest = getLatestSession();
	return {
		sessions: listSessions(),
		latest: latest
			? {
					id: latest.id,
					number: latest.number,
					date: latest.date,
					title: latest.title,
					summary: latest.summary ?? null,
					recommendations: latest.recommendations ?? []
				}
			: null
	};
}
