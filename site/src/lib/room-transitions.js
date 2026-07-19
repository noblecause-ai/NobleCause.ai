// Raum-Übergänge: nur zwischen den drei Räumen, nur mit View-Transitions-API,
// nur ohne Reduced-Motion. Sonst bleibt es beim sofortigen Standardwechsel —
// die Historie läuft in jedem Fall über echte URLs, nie über eigenen Zustand.
import { onNavigate } from '$app/navigation';

// DE- und EN-Räume bilden je eine eigene Folge — Übergänge nur innerhalb einer
// Sprache; der Sprachwechsel selbst ist ein schlichter, sofortiger Wechsel.
const ORDERS = [
	['/', '/ratssaal/', '/archiv/'],
	['/en/', '/en/council/', '/en/archive/']
];

export function installRoomTransitions() {
	// Letzter Klickpunkt als Zoom-Ursprung: die Fahrt geht in die angeklickte Tür
	// hinein (Fallback in CSS: center). Progressive Enhancement, kein Zustand.
	window.addEventListener(
		'pointerdown',
		(event) => {
			document.documentElement.style.setProperty(
				'--vt-origin',
				`${event.clientX}px ${event.clientY}px`
			);
		},
		{ passive: true }
	);

	onNavigate((navigation) => {
		const from = navigation.from?.url.pathname;
		const to = navigation.to?.url.pathname;
		if (!from || !to || from === to) return;
		const order = ORDERS.find((candidate) => candidate.includes(from) && candidate.includes(to));
		if (!order) return;
		if (typeof document.startViewTransition !== 'function') return;
		if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

		const dir = order.indexOf(to) < order.indexOf(from) ? 'back' : 'forward';
		document.documentElement.dataset.navDir = dir;
		return new Promise((resolve) => {
			try {
				const transition = document.startViewTransition(async () => {
					resolve();
					await navigation.complete;
				});
				transition.finished.finally(() => {
					delete document.documentElement.dataset.navDir;
				});
			} catch {
				resolve();
				delete document.documentElement.dataset.navDir;
			}
		});
	});
}
