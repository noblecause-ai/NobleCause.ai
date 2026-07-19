// Setzt das lang-Attribut des Dokuments passend zur Route: die Räume gibt es
// deutsch (/, /ratssaal/, /archiv/) und englisch (/en/, /en/council/, /en/archive/);
// alle übrigen Routen sind deutsch (publizierter Rekord).
export const handle = ({ event, resolve }) =>
	resolve(event, {
		transformPageChunk: ({ html }) =>
			html.replace(
				'%lang%',
				event.url.pathname === '/en' || event.url.pathname.startsWith('/en/') ? 'en' : 'de'
			)
	});
