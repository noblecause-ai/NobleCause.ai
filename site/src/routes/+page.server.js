import { getAllSessions, getLatestSession, getOrganizations } from '$lib/server/content.js';
import { buildHomepageViewModel } from '$lib/server/homepage.js';
import { md } from '$lib/server/content.js';

export function load() {
	const session = getLatestSession();
	if (!session) return { home: null };
	const home = buildHomepageViewModel({
		session,
		sessions: getAllSessions(),
		registry: getOrganizations()
	});
	return {
		home: {
			...home,
			correctionHtml: home.correction ? md(home.correction.text) : null,
			dissentHtml: md(home.dissent),
			modelTracks: home.modelTracks.map((track) => ({
				...track,
				initialContentHtml: md(track.initialContent),
				finalContentHtml: md(track.finalContent)
			}))
		}
	};
}
