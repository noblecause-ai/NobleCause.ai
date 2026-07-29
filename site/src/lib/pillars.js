// Die vier Bereiche (Säulen A–D) für den Protokoll-Explorer. Deutsch-only (der
// Rekord bleibt deutsch, s. i18n/index.js) — darum eine eigene Konstante statt
// der i18n-Schicht `t.pillars`, mit denselben Labels und Emblem-Assets wie die
// Räume, damit die Welt gleich bleibt.
export const PILLARS = {
	A: { label: 'Zukunft', emblem: '/media/pillars/pillar-future-display.avif' },
	B: { label: 'Leid lindern', emblem: '/media/pillars/pillar-relieve-suffering-display.avif' },
	C: { label: 'Große Gefahren', emblem: '/media/pillars/pillar-major-risks-display.avif' },
	D: {
		label: 'Was sonst übersehen wird',
		emblem: '/media/pillars/pillar-overlooked-display.avif'
	}
};

export const PILLAR_ORDER = ['A', 'B', 'C', 'D'];
