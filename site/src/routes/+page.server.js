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
			// dissent/correction werden im No-JS-Fallback gerendert; je-Modell-content_md
			// (initialContentHtml/finalContentHtml) wurde nirgends gerendert -> entfernt.
			correctionHtml: home.correction ? md(home.correction.text) : null,
			dissentHtml: md(home.dissent)
		}
	};
}
