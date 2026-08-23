import { manifestHtml } from '$lib/server/content.js';

export function load() {
	// manifest.md bleibt die einzige Inhaltsquelle. Nur die HTML-
	// Überschriftenebenen rücken für die Einbettung unter das Seiten-h1 um eine
	// Stufe nach unten; Text und Reihenfolge bleiben unverändert.
	const manifest = manifestHtml().replace(
		/<(\/?)h([1-5])(\b[^>]*)>/g,
		(_match, closing, level, rest) => `<${closing}h${Number(level) + 1}${rest}>`
	);
	return { manifest };
}
