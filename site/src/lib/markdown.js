import { Marked } from 'marked';

// Shared safe renderer for stored records and the live conversation.
function escapeHtml(value) {
	return String(value ?? '')
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#39;');
}

// Gefährliche URL-Schemata (javascript:, data:, vbscript:) neutralisieren, auch
// verschleiert („jAvA\tscript:", „ javascript:", prozentkodiert). Rückgabe: die
// unveränderte href, wenn unbedenklich; null, wenn zu blocken.
function cleanUrl(href) {
	if (typeof href !== 'string') return null;
	let decoded;
	try {
		decoded = decodeURIComponent(href);
	} catch {
		return null; // kaputte Prozentkodierung → als unsicher behandeln
	}
	const scheme = decoded.replace(/[^a-zA-Z0-9:]/g, '').toLowerCase();
	if (scheme.startsWith('javascript:') || scheme.startsWith('vbscript:') || scheme.startsWith('data:')) {
		return null;
	}
	return href;
}

const renderer = {
	// Roh-HTML aus Modelltext (Block wie inline) wird nicht als Markup interpretiert,
	// sondern als sichtbarer Text ausgegeben. Damit greifen weder <script> noch
	// Event-Handler-Attribute (onerror, onclick …), ohne dass etwas entfernt wird.
	html({ text }) {
		return escapeHtml(text);
	},
	// Links aus Modelltext bleiben klickbar (Quellenbelege sind der Zweck des Rekords),
	// tragen aber rel="nofollow noopener noreferrer ugc" und können kein gefährliches
	// Schema mehr tragen. Bei geblocktem Schema bleibt der sichtbare Linktext erhalten.
	link({ href, title, tokens }) {
		const inner = this.parser.parseInline(tokens);
		const clean = cleanUrl(href);
		if (clean === null) return inner;
		const titleAttr = title ? ` title="${escapeHtml(title)}"` : '';
		return `<a href="${escapeHtml(clean)}"${titleAttr} rel="nofollow noopener noreferrer ugc">${inner}</a>`;
	},
	// Bildquellen dürfen ebenfalls kein gefährliches Schema tragen; bei geblocktem
	// Schema bleibt der Alt-Text als sichtbarer Text erhalten.
	image({ href, title, text }) {
		const clean = cleanUrl(href);
		const alt = escapeHtml(text);
		if (clean === null) return alt;
		const titleAttr = title ? ` title="${escapeHtml(title)}"` : '';
		return `<img src="${escapeHtml(clean)}" alt="${alt}"${titleAttr}>`;
	}
};

// Eigene Instanz statt globalem marked.use(), damit die Konfiguration lokal bleibt
// und keine andere marked-Nutzung im Prozess mitverändert wird. Nicht angegebene
// Renderer-Methoden (Absätze, Listen, Betonung …) fallen auf die Vorgabe zurück.
const markedInstance = new Marked({ renderer });

export function md(text) {
	return markedInstance.parse(text ?? '');
}
