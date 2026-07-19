// i18n-Grundlage: Deutsch ist Default (unveränderte URLs), Englisch unter /en/…
// gespiegelt. Die Räume bekommen ihre Sprache als Prop (`lang`) und lesen über
// `locales[lang]` — kein stiller Globalimport mehr.
import { de } from './de.js';
import { en } from './en.js';

export const locales = { de, en };

// Die drei Räume in beiden Sprachen. Alle übrigen Routen (sessions, journal,
// manifest, idee, impressum) bleiben deutsch-only — sie sind der Rekord.
export const roomPaths = {
	study: { de: '/', en: '/en/' },
	council: { de: '/ratssaal/', en: '/en/council/' },
	archive: { de: '/archiv/', en: '/en/archive/' }
};

// Schwester-Route für den Sprachumschalter: gleicher Raum, andere Sprache.
// null, wenn der Pfad kein Raum ist (dann zeigt das Layout keinen Umschalter).
export function siblingPath(pathname) {
	for (const paths of Object.values(roomPaths)) {
		if (paths.de === pathname) return paths.en;
		if (paths.en === pathname) return paths.de;
	}
	return null;
}

export function langOfPath(pathname) {
	return pathname === '/en' || pathname.startsWith('/en/') ? 'en' : 'de';
}
