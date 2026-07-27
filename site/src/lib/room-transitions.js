// Raum-Übergänge: nur zwischen den drei Räumen, nur mit View-Transitions-API,
// nur ohne Reduced-Motion. Sonst bleibt es beim sofortigen Standardwechsel —
// die Historie läuft in jedem Fall über echte URLs, nie über eigenen Zustand.
// Bühnen-Wiring (§3 Schritt 2): jede Navigation wird hier in einen Eintritts-
// Modus übersetzt (classifyEntry) und der Bühne bekanntgegeben — die Route ist
// die Wahrheit, keine Teilmechanik hat eigene Navigationslogik. Bei Ankunft
// (Raum→Raum) startet die Eintrittssequenz erst nach transition.finished;
// Sprachwechsel ist kein Raumwechsel (kein Ride, keine Sequenz — wie bisher).
//
// Vertical Slice: Türfahrt (Zoom in die angeklickte Tür), Tafel-Reise
// (view-transition-name am ResultBoard + board-traveling-Zustand) und der
// Röhren-Diff (primeTubeDiff — die Röhre reist mit dem Herkunfts-Füllstand
// und expandiert/schrumpft erst nach der Fahrt auf den SSR-Zielstand).
import { goto, onNavigate } from '$app/navigation';
import {
	applyEntryMode,
	classifyEntry,
	playStage,
	primeTubeDiff,
	roomOfPath,
	TUBE_FILLED
} from './stage.js';
import { langOfPath } from './i18n/index.js';
import { runDoorPassage, passageActive } from './door-passage.js';
import { DOOR_PASSAGES, passageOrigin } from './door-passages.js';

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

	// Tür-Links setzen den Zoom-Ursprung auf die KARTENMITTE (nicht den exakten
	// Klickpunkt) — so zielt die Fahrt auch bei Tastatur-Auslösung (Enter feuert
	// click) und bei Treffer am Kartenrand sauber in die Tür.
	// Ausserdem: BÜHNEN-RÄUMEN vor der Fahrt — die Seitenelemente fahren auf
	// ihren Schienen zurück (--retreat: 1, weich über .stage-clearing) und die
	// Tür öffnet sich, DANN erst geht die Kamera durch die Tür. Nur bei echter
	// Raum-zu-Raum-Navigation derselben Sprache mit verfügbarer View-Transition;
	// alles andere (Reduced-Motion, Modifier-Klicks, Sprachwechsel, Nicht-Raum-
	// Ziele) bleibt der normale Link bzw. der sofortige Wechsel.
	window.addEventListener(
		'click',
		(event) => {
			const door = event.target?.closest?.('.door-gallery a[href], .door-hotspot[href]');
			if (!door) return;
			const rect = door.getBoundingClientRect();
			document.documentElement.style.setProperty(
				'--vt-origin',
				`${Math.round(rect.left + rect.width / 2)}px ${Math.round(rect.top + rect.height / 2)}px`
			);
			// Türrechteck als inset() für die Portal-Blende (§B): der Zielraum wird
			// aus GENAU dieser Kontur aufgezogen — dieselbe Geometrie, die auch
			// --vt-origin trägt. Greift für .door-hotspot (Desktop) UND
			// .door-gallery a (Mobil/Fallback), beides echte Rechtecke.
			const el = document.documentElement;
			// Gemeinsame Klemme statt vier Einzel-Klemmen: garantiert ≥24 px
			// Startfläche. Sonst kann auf Mobil (Tipp auf die obere Kartenhälfte,
			// Unterkante unter der Falz) --door-bottom auf 0 klemmen, während
			// --door-top gross bleibt → top+bottom > Viewporthöhe → inset() leer →
			// der Zielraum wäre die ersten Frames unsichtbar statt in der Türöffnung.
			const vw = window.innerWidth;
			const vh = window.innerHeight;
			const t = Math.min(Math.max(0, Math.round(rect.top)), Math.max(0, vh - 24));
			const l = Math.min(Math.max(0, Math.round(rect.left)), Math.max(0, vw - 24));
			const b = Math.min(Math.max(0, Math.round(vh - rect.bottom)), Math.max(0, vh - t - 24));
			const r = Math.min(Math.max(0, Math.round(vw - rect.right)), Math.max(0, vw - l - 24));
			el.style.setProperty('--door-top', `${t}px`);
			el.style.setProperty('--door-right', `${r}px`);
			el.style.setProperty('--door-bottom', `${b}px`);
			el.style.setProperty('--door-left', `${l}px`);
			if (event.defaultPrevented || el.classList.contains('stage-clearing')) return;
			if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
			if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
			if (typeof document.startViewTransition !== 'function') return;
			const from = window.location.pathname;
			const to = new URL(door.href, window.location.href).pathname;
			if (from === to || !roomOfPath(from) || !roomOfPath(to)) return;
			if (langOfPath(from) !== langOfPath(to)) return;
			// §C Türdurchgang: jede in-Szene-Passage-Tür (Config je Quellraum in
			// door-passages.js), nur Desktop ≥1200 px → echte Kamerafahrt statt
			// Portalblende. door-passage baut die Übergangsebene aus derselben Config
			// wie der Ruhe-Stapel, navigiert selbst und ruft playStage() nach der
			// Übergabe. Fällt eines der Kriterien, läuft unverändert die Blende
			// darunter (return unten).
			const passage = DOOR_PASSAGES[roomOfPath(from)];
			if (
				passage &&
				roomOfPath(to) === passage.target &&
				window.innerWidth >= 1200 &&
				!passageActive()
			) {
				event.preventDefault();
				el.classList.add('stage-clearing');
				el.style.setProperty('--retreat', '1');
				const clearPassage = () => {
					el.classList.remove('stage-clearing');
					el.style.removeProperty('--retreat');
				};
				const passGuard = setTimeout(clearPassage, 3200);
				runDoorPassage({
					href: to,
					wallHole: passage.wallHole,
					leafLeft: passage.leafLeft,
					leafRight: passage.leafRight,
					far: passage.farHi,
					// Origin zur Laufzeit aus der Cover-Rechnung (Council: aus
					// aperturePlate; Study/Archiv: feste Konstante) — korrekter
					// Viewport ist der beim Klick.
					origin: passageOrigin(passage),
					onDone: () => {
						clearTimeout(passGuard);
						clearPassage();
						playStage();
					}
				});
				return;
			}
			event.preventDefault();
			el.classList.add('stage-clearing');
			el.style.setProperty('--retreat', '1');
			// Portal-Fahrt: erst hier gesetzt, wo die Fahrt sicher läuft (nach allen
			// Guards) — Back/Forward ohne Türklick behält das bisherige Verhalten (§B).
			el.dataset.portal = '';
			// §0-Sicherung (§B3): bleibt die Navigation aus (abgebrochen, Fehler,
			// offline), holt der Watchdog die Bühne zurück, statt sie dauerhaft
			// ausgeräumt stehen zu lassen — der pageshow-Guard fängt nur bfcache.
			const guard = setTimeout(() => {
				el.classList.remove('stage-clearing');
				el.style.removeProperty('--retreat');
				delete el.dataset.portal;
			}, 1800);
			// A7 (revidiert 2026-07-24): Fahrt ≤200 ms nach dem Klick — das
			// Schienen-Räumen (0,38 s) läuft IN die Fahrt hinein, statt ihr 480 ms
			// voranzugehen (kein hängender-Link-Leerlauf mehr).
			setTimeout(() => goto(to).finally(() => clearTimeout(guard)), 140);
		},
		{ passive: false, capture: true }
	);

	onNavigate((navigation) => {
		const from = navigation.from?.url.pathname;
		const to = navigation.to?.url.pathname;
		if (!from || !to || from === to) return;
		const mode = classifyEntry(from, to);
		// §6: läuft der Türdurchgang, IST die Übergangsebene der Übergang — keine
		// eigene VT-Fahrt, kein Block. Zielraum nur ARMEN (nicht spielen); die
		// Passage ruft playStage() nach der Übergabe (arrival-Deferral).
		if (passageActive()) {
			applyEntryMode(mode);
			return;
		}
		const order = ORDERS.find((candidate) => candidate.includes(from) && candidate.includes(to));
		const tubeFrom = mode === 'arrival' ? TUBE_FILLED[roomOfPath(from)] : null;
		const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
		if (!order || typeof document.startViewTransition !== 'function' || reduced) {
			// Kein Ride (Sprachwechsel, Quereinstieg, fehlende API, Reduced-Motion):
			// Modus sofort anwenden — fresh spielt direkt, arrival ebenfalls
			// (applyEntryMode lässt arrival ungespielt, darum hier nachziehen),
			// language bleibt stehen. Bei Reduced-Motion kein Tube-Priming: der
			// SSR-Zielstand gilt sofort (sofortiger Wechsel ohne jede Animation).
			applyEntryMode(mode);
			if (mode === 'arrival') {
				if (!reduced && tubeFrom != null) primeTubeDiff(tubeFrom);
				playStage();
			}
			return;
		}

		const dir = order.indexOf(to) < order.indexOf(from) ? 'back' : 'forward';
		document.documentElement.dataset.navDir = dir;
		document.documentElement.classList.add('board-traveling');
		return new Promise((resolve) => {
			try {
				const transition = document.startViewTransition(async () => {
					// Modus erst NACH der Capture der alten Seite anwenden — sonst
					// verliert die ausgehende Szene ihre Endzustands-Klassen.
					applyEntryMode(mode);
					resolve();
					await navigation.complete;
					// Nach dem DOM-Wechsel, vor der neuen Capture: die Röhre zeigt
					// den Herkunfts-Füllstand (der Diff spielt nach der Fahrt).
					if (tubeFrom != null) primeTubeDiff(tubeFrom);
				});
				transition.finished.finally(() => {
					delete document.documentElement.dataset.navDir;
					delete document.documentElement.dataset.portal;
					document.documentElement.classList.remove('board-traveling');
					playStage();
				});
			} catch {
				applyEntryMode(mode);
				resolve();
				delete document.documentElement.dataset.navDir;
				delete document.documentElement.dataset.portal;
				document.documentElement.classList.remove('board-traveling');
				playStage();
			}
		});
	});
}
