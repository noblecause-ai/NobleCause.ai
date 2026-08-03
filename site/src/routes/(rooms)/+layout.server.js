import {
	getAllSessions,
	getJournalEntry,
	getLatestSession,
	getOrganizations,
	getSchedule,
	md
} from '$lib/server/content.js';
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
	// Zeitschicht-Leser: der LETZTE RESEARCH-Lauf trägt den Scout-Sitz und die
	// „letzte Prüfung". Autoritativer Zeiger ist schedule.last_journal — nicht das
	// neueste Journal-Datei nach Datum (das wäre der Klartext-Bootstrap 2026-07-24,
	// kein Research-Lauf). Der Termin kommt aus dem Rhythmus, NICHT aus
	// schedule.next_research. Alles wörtlich durchgereicht.
	const schedule = getSchedule();
	const lastId = schedule?.last_journal?.replace(/^\/?journal\//, '').replace(/\/$/, '') || null;
	const last = lastId ? getJournalEntry(lastId) : null;
	// Auflage (Steward): der aufgelöste Eintrag MUSS ein Research-Lauf sein.
	// Strukturelles Signal ist search_queries — KEIN Parsen von convene_rationale-
	// Prosa (Datenvertrag). Ist es kein Research-Lauf, ist schedule.last_journal
	// falsch gesetzt → LAUT scheitern (Build bricht), NICHT stillschweigend auf ein
	// anderes Journal zurückfallen. Ein Datenproblem gehört gemeldet, nicht geglättet.
	if (last && !(last.search_queries?.length > 0)) {
		throw new Error(
			`lastResearch: journal/${lastId} hat keine search_queries — kein Research-Lauf. schedule.last_journal prüfen.`
		);
	}
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
			// text_en wird BEWUSST NICHT gerendert: der Rekord (inkl. Korrekturhinweise)
			// bleibt deutsch (Konvention en.js:5, Test erzwingt sie). text_en hält den
			// Wart-Wortlaut treu im Rekord, ohne ihn anzuzeigen — nicht "reparieren".
			corrections: (home.correction ?? []).map((c) => ({ date: c.date, html: md(c.text) })),
			dissentHtml: md(home.dissent),
			// Kuratierter Klartext-Kontext fürs Frage-Dossier — wörtlich
			// durchgereicht, das Frontend paraphrasiert nichts.
			questionSummary: session.summary ?? null,
			// Zeitschicht: letzter Research-Lauf (Scout-Sitz, „letzte Prüfung",
			// Warden-Entscheid, Vertretung) + Sitzungstermin als Plan.
			lastResearch: last && {
				date: last.date,
				model: last.model ?? null,
				deputationNote: last.deputation_note ?? null,
				convene: last.convene ?? false
			},
			schedule: { nextSession: schedule?.next_session ?? null }
		}
	};
}
