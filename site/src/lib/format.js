// Datumsformatierung für die Zeitschicht — der EINZIGE Formatter im Projekt.
// Formatiert ein gespeichertes ISO-Datum (YYYY-MM-DD) in der Raumsprache. Das
// Datum ist Rekord-Datenfeld, keine Übersetzung — nur die Darstellung ist
// sprachabhängig. UTC-fest geparst (kein Zeitzonen-Versatz), damit SSR und
// Client bitidentisch formatieren (keine Hydration-Diskrepanz).
const LOCALE = { de: 'de-DE', en: 'en-US' };

export function formatDate(iso, lang) {
	if (!iso) return '';
	// Verträgt „YYYY-MM-DD" UND ISO-Datetime „YYYY-MM-DDThh:mm:ssZ" (schedule).
	const [y, m, d] = String(iso).slice(0, 10).split('-').map(Number);
	if (!y || !m || !d) return String(iso);
	const date = new Date(Date.UTC(y, m - 1, d));
	return new Intl.DateTimeFormat(LOCALE[lang] ?? LOCALE.de, {
		day: 'numeric',
		month: 'long',
		year: 'numeric',
		timeZone: 'UTC'
	}).format(date);
}
