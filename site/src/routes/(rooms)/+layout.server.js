import { getAllSessions, getLatestSession, getOrganizations, md } from '$lib/server/content.js';
import { buildHomepageViewModel } from '$lib/server/homepage.js';

// Ein einziger Load für alle drei Räume — derselbe verifizierte Aufruf wie bisher
// auf der Startseite; jeder Raum rendert nur seine Scheibe des View-Models.
export function load() {
	const session = getLatestSession();
	if (!session) return { home: null };
	const registry = getOrganizations();
	const home = buildHomepageViewModel({
		session,
		sessions: getAllSessions(),
		registry
	});
	return {
		// Optionale englische Organisationsbeschreibungen (Registry-Feld
		// beschreibung_en). Derzeit bei keiner Organisation belegt — die Karten
		// fallen dann auf die deutsche Beschreibung plus Sprachhinweis zurück.
		orgEn: Object.fromEntries(
			(registry.organizations ?? []).map((organization) => [
				organization.id,
				organization.beschreibung_en ?? null
			])
		),
		home: {
			...home,
			// dissent/correction werden als Markdown gerendert (Wortlaut unverändert).
			correctionHtml: home.correction ? md(home.correction.text) : null,
			dissentHtml: md(home.dissent),
			// Kuratierter Klartext-Kontext fürs Frage-Dossier — wörtlich
			// durchgereicht, das Frontend paraphrasiert nichts.
			questionSummary: session.summary ?? null
		}
	};
}
