// Bühnen-Gerüst (§3 Schritt 2 des Bühnenspiel-Umlaufs): Eintritts-Choreografie
// über dem VOLLSTÄNDIGEN Dokument. Das pragerenderte HTML ist der Endzustand —
// versteckt/animiert wird nur unter html.stage-armed (JS-only) und nur ohne
// Reduced-Motion (CSS-Media-Query). Dieses Modul ist die EINZige Stelle, die
// Eintrittsarten kennt (Route = Wahrheit; Kamera, Tafel und Röhre bekommen keine
// eigene Navigationslogik — sie reagieren später auf dieselbe Klassifikation).
//
// Modi: fresh (Direktaufruf/Hard-Reload/von außerhalb) · arrival (Raum→Raum
// derselben Sprache, auch Browser Back/Forward) · language (Schwester-Route —
// kein Raumwechsel: keine Sequenz, nur Texte tauschen).
import { afterNavigate } from '$app/navigation';
import { langOfPath, roomPaths, siblingPath } from './i18n/index.js';

const root = () => document.documentElement;

const STAGE_CLASSES = [
	'stage-armed',
	'stage-play',
	'stage-locked',
	'stage-unlocked',
	'stage-skip',
	'stage-clearing',
	'mode-fresh',
	'mode-arrival',
	'mode-language'
];

// Raum → Szenen-Plate für das Intent-Preload (mobile = Hochformat-Variante,
// null = Slot, die Querformat-Plate gilt überall).
const SCENES = {
	study: {
		desktop: '/media/scenes/antechamber-display.avif',
		mobile: '/media/scenes/antechamber-portrait-display.avif',
		mobile800: '/media/scenes/antechamber-portrait-800.avif'
	},
	council: {
		desktop: '/media/scenes/hall-display.avif',
		mobile: '/media/scenes/hall-portrait-display.avif',
		mobile800: '/media/scenes/hall-portrait-800.avif'
	},
	archive: {
		desktop: '/media/scenes/archive-display.avif',
		mobile: '/media/scenes/archive-portrait-display.avif',
		mobile800: '/media/scenes/archive-portrait-800.avif'
	}
};

const roomOfPath = (pathname) => {
	for (const [room, paths] of Object.entries(roomPaths)) {
		if (paths.de === pathname || paths.en === pathname) return room;
	}
	return null;
};

// Füllstand der Prozess-Röhre je Raum — EINZige Quelle (Räume rendern daraus
// per SSR, der Slice-Diff liest dieselbe Map; niemals doppelt buchen).
export const TUBE_FILLED = { study: 2, council: 5, archive: 6 };
export { roomOfPath };

// Eintrittsart aus from→to. null = gleiche Seite, nichts zu tun.
export function classifyEntry(from, to) {
	if (!from || !to || from === to) return null;
	if (siblingPath(from) === to) return 'language';
	if (roomOfPath(from) && roomOfPath(to) && langOfPath(from) === langOfPath(to)) {
		return 'arrival';
	}
	return 'fresh';
}

// Setzt den Modus als Klassen — VOR dem DOM-Wechsel der Zielroute bzw. in der
// View-Transition nach der alten Capture. Idempotent.
export function applyEntryMode(mode) {
	const el = root();
	el.classList.remove(...STAGE_CLASSES);
	// Schienen-Rückzug gehört zur verlassenen Szene — der neue Raum startet
	// mit eingerückten Elementen (Scrub koppelt danach wieder an den Scroll).
	el.style.removeProperty('--retreat');
	if (!mode) return;
	if (mode === 'language') {
		// Kein Raumwechsel: Szene bleibt stehen (unarmed = vollständiges Dokument).
		el.classList.add('mode-language');
		return;
	}
	el.classList.add('stage-armed', `mode-${mode}`);
	if (mode === 'fresh') {
		// Frischer Aufruf: Sequenz startet sofort.
		el.classList.add('stage-play');
		scheduleLock();
	}
	// arrival: stage-play kommt erst nach transition.finished (playStage) — die
	// Sequenz beginnt, wenn die Kamerafahrt abgeschlossen ist.
}

let lockTimer = 0;
let watchdogTimer = 0;

// Startet die Sequenz nachträglich (Ankunft nach der Fahrt). Doppeltaufruf
// ist harmlos. Der Watchdog garantiert §0: Selbst wenn ein erwartetes
// transition.finished ausbleibt, bleibt kein Beat dauerhaft versteckt.
export function playStage() {
	const el = root();
	if (!el.classList.contains('stage-armed') || el.classList.contains('stage-play')) return;
	el.classList.add('stage-play');
	scheduleLock();
	clearTubeDiff(350);
}

// ---- Röhren-Diff (Vertical Slice) ----------------------------------------
// Bei Ankunft (Raum→Raum) reist die Röhre mit dem Füllstand des HERKUNFTS-
// raums und expandiert/schrumpft erst nach der Fahrt auf den SSR-Zielstand.
// Die Diff-Klassen leben nur im JS-Pfad (SSR bleibt die Wahrheit); die
// Animation steckt in CSS-Transitions (StageTube), bei Reduced-Motion gibt
// es kein Priming — der Zielstand gilt sofort.
export function primeTubeDiff(tubeFrom) {
	if (tubeFrom == null) return;
	const beads = document.querySelectorAll('.tube-bead');
	if (!beads.length) return;
	const filled = document.querySelectorAll('.tube-bead.filled').length;
	beads.forEach((bead, i) => {
		if (tubeFrom < filled && i >= tubeFrom && i < filled) bead.classList.add('tube-diff-in');
		if (tubeFrom > filled && i < tubeFrom && bead.classList.contains('blass')) {
			bead.classList.add('tube-diff-out');
		}
	});
}

let tubeDiffTimer = 0;
export function clearTubeDiff(delay = 0) {
	clearTimeout(tubeDiffTimer);
	const clear = () => {
		document
			.querySelectorAll('.tube-diff-in, .tube-diff-out')
			.forEach((bead) => bead.classList.remove('tube-diff-in', 'tube-diff-out'));
	};
	if (delay > 0) tubeDiffTimer = setTimeout(clear, delay);
	else clear();
}

function scheduleLock() {
	clearTimeout(lockTimer);
	clearTimeout(watchdogTimer);
	// Sequenzende ~1,9 s nach stage-play, plus Puffer.
	lockTimer = setTimeout(() => {
		const el = root();
		if (!el.classList.contains('stage-armed')) return;
		el.classList.add('stage-locked');
		maybePreload();
	}, 2100);
	// §0-Sicherung: läuft stage-play aus irgendeinem Grund nicht an, wird das
	// Dokument spätestens hier vollständig sichtbar geschaltet.
	watchdogTimer = setTimeout(playStage, 3500);
}

let installed = false;

// §Fix Rückwärts-Stabilität: DIE Stelle, die den Bühnen-Eintritt bei JEDEM
// Betreten eines Raums neu herstellt — frischer Load, Klick-Nav, Zurück/Vorwärts
// (afterNavigate feuert für alle) und bfcache (pageshow-Guard oben ruft dasselbe
// Prinzip). Grund: SvelteKit-Scroll-Restoration stellt beim Zurück die alte
// Scrollposition wieder her. Liegt sie UNTER dem Hero-Band, maxt der Scrub
// --retreat sofort (Schienen eingerückt), die Orbit-Schleife pausiert (scrollY ≥
// 1,1·vh → kein Kreisen) und die nächste Fahrt liest als Blende (Tür außer Sicht,
// gescrollte VT-Capture) — beide Symptome aus EINER Ursache. Darum beginnt jeder
// Raum am Hero. Sprachwechsel (Schwesterroute, kein Raumwechsel) bleibt stehen.
// Die gerastete --retreat wird hier gelöscht; die Übergangs-Klassen (stage-*,
// passageActive, dataset.portal/navDir) räumt der Übergangs-Flow selbst
// (room-transitions/door-passage) — der Eintritt fasst nur den Scroll-/Scrub-Grund.
function resetStageOnEntry(navigation) {
	const mode = classifyEntry(navigation?.from?.url.pathname, navigation?.to?.url.pathname);
	if (mode !== 'language') {
		window.scrollTo(0, 0);
		root().style.removeProperty('--retreat');
	}
	observeDoors();
}

// Einmalig vom Raum-Layout installiert: Scroll-Skip (bewusstes Scrollen während
// des Aufbaus springt in den Endzustand — keine Sperre, keine Queue) und das
// beidseitige Unlock-Toggling nach dem Lock. Dazu das Tür-Preload (Codex §8).
export function installStage() {
	if (installed) return;
	installed = true;
	const el = root();
	const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
	// Boot-Fall (harter Seitenaufruf): das Inline-Script in app.html hat bereits
	// gespielt — nur den Lock nachplanen.
	if (el.classList.contains('stage-armed') && el.classList.contains('stage-play')) {
		scheduleLock();
	}
	window.addEventListener(
		'scroll',
		() => {
			const y = window.scrollY;
			// Schienen-Scrub: die Seitenelemente weichen dem nachrückenden Text
			// proportional zum Scrollweg aus (0..1 über 75 % der Viewporthöhe).
			// Transitionslos — direkte Kopplung; Reduced-Motion bleibt statisch.
			if (!reducedMotion.matches) {
				el.style.setProperty('--retreat', Math.min(1, y / (window.innerHeight * 0.75)).toFixed(3));
			}
			if (
				y > 48 &&
				el.classList.contains('stage-armed') &&
				!el.classList.contains('stage-locked')
			) {
				el.classList.add('stage-skip', 'stage-locked');
				clearTubeDiff();
				maybePreload();
				return;
			}
			if (el.classList.contains('stage-locked')) {
				el.classList.toggle('stage-unlocked', y > 48);
			}
		},
		{ passive: true }
	);
	// bfcache-Rückkehr während/eines Bühnen-Räumens: Szene wiederherstellen,
	// sonst blieben die Schienen dauerhaft ausgefahren.
	window.addEventListener('pageshow', (event) => {
		if (!event.persisted) return;
		el.classList.remove('stage-clearing');
		el.style.removeProperty('--retreat');
		window.scrollTo(0, 0);
	});
	afterNavigate(resetStageOnEntry);
}

// ---- Tür-Preload (Codex §8) ---------------------------------------------
// Zielraum-Plate vorbereiten, wenn eine Tür zu ≥60 % sichtbar ist UND die Szene
// gelockt ist — per Idle-Task, nie bei saveData/2g, niemals navigationskritisch.
const preloaded = new Set();
let observer = null;

function connectionSlow() {
	const c = navigator.connection;
	return !!(c?.saveData || c?.effectiveType === '2g' || c?.effectiveType === 'slow-2g');
}

function sceneFor(href) {
	const room = roomOfPath(href ?? '');
	if (!room) return null;
	const scenes = SCENES[room];
	const desktop = matchMedia('(min-width: 1200px)').matches;
	if (desktop) return scenes.desktop;
	// Dieselbe Stufen-Logik wie das Hero-srcset: kleine Viewports × DPR
	// bekommen die 800er-Plate (A3) — Preload spiegelt die echte Auswahl.
	if (scenes.mobile800 && window.innerWidth * (window.devicePixelRatio || 1) <= 800) {
		return scenes.mobile800;
	}
	return scenes.mobile ?? scenes.desktop;
}

function preloadScene(href) {
	const url = sceneFor(href);
	if (!url || preloaded.has(url) || connectionSlow()) return;
	preloaded.add(url);
	const idle = window.requestIdleCallback ?? ((cb) => setTimeout(cb, 400));
	idle(() => {
		const img = new Image();
		img.src = url;
	});
}

// Direkte Sichtbarkeitsprüfung (beim Lock, für schon im Viewport stehende Türen)
// — dieselbe 60-%-Schwelle wie der IntersectionObserver.
function maybePreload() {
	if (connectionSlow()) return;
	document.querySelectorAll('.door-hotspot, .door-gallery a[href]').forEach((el) => {
		const rect = el.getBoundingClientRect();
		if (!rect.height) return;
		const visible = Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0);
		if (visible >= rect.height * 0.6) preloadScene(el.getAttribute('href'));
	});
}

function observeDoors() {
	observer?.disconnect();
	if (connectionSlow()) return;
	const doors = document.querySelectorAll('.door-hotspot, .door-gallery a[href]');
	if (!doors.length) return;
	observer = new IntersectionObserver(
		(entries) => {
			for (const entry of entries) {
				if (!entry.isIntersecting) continue;
				if (!root().classList.contains('stage-locked')) continue;
				preloadScene(entry.target.getAttribute('href'));
				observer.unobserve(entry.target);
			}
		},
		{ threshold: 0.6 }
	);
	doors.forEach((el) => observer.observe(el));
}
