// Die vier Bereiche (Säulen A–D) für den Protokoll-Explorer. Deutsch-only (der
// Rekord bleibt deutsch, s. i18n/index.js) — darum eine eigene Konstante statt
// der i18n-Schicht `t.pillars`, mit denselben Labels und Emblem-Assets wie die
// Räume, damit die Welt gleich bleibt.
export const PILLARS = {
	A: { label: 'Zukunft', slug: 'zukunft', emblem: '/media/pillars/pillar-future-display.avif' },
	B: { label: 'Leid lindern', slug: 'leid', emblem: '/media/pillars/pillar-relieve-suffering-display.avif' },
	C: { label: 'Große Gefahren', slug: 'gefahren', emblem: '/media/pillars/pillar-major-risks-display.avif' },
	D: {
		label: 'Was sonst übersehen wird',
		slug: 'uebersehen',
		emblem: '/media/pillars/pillar-overlooked-display.avif'
	}
};

export const PILLAR_ORDER = ['A', 'B', 'C', 'D'];

// Adresse (?bereich=zukunft) ↔ Säule. Schritt 2: adressierbare Filter als Links.
export const pillarOfSlug = (slug) => PILLAR_ORDER.find((p) => PILLARS[p].slug === slug) ?? null;
