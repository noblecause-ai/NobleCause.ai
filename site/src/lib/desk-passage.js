// Lesetisch-Übergang (Hinweg Archiv → Explorer). Der Tisch mit der Leuchte fährt
// von unten herein und füllt den unteren Bildrand, das Lampenlicht weitet sich,
// der Raum dahinter sinkt in Unschärfe/Dunkel → Navigation zur vorgerenderten
// Explorer-Seite (deren Lampenlicht-Gestalt die Ankunft „auf dem Tisch" trägt).
//
// KEIN Rückweg (gestrichen, nicht vertagt): der Lesetisch verbindet einen Ort mit
// einem Text, nicht zwei Orte. Der Rückweg läuft meist über den Zurück-Button;
// dort Zustand anzuhängen wäre die Fehlerklasse aus der Rückwärts-Stabilität.
//
// Muster aus dem Türdurchgang (door-passage.js), drei Auflagen:
//  1) Der Zustand fällt IMMER zurück — try/catch um den ganzen Ablauf; finish()
//     löst den Riegel (active) in jedem Fall, auch bei einem Wurf.
//  2) Ziel vorher prefetchen/dekodieren, Deckel 300 ms — danach startet die
//     Bewegung ohnehin (lieber kurzes Nachladen als hängender Klick).
//  3) Der Zurück-Button bleibt unberührt: onNavigate bricht bei FREMDER Navigation
//     (Zurück/Vor) ab und räumt die Ebene; die eigene goto() wird durchgelassen.
//
// §0: ohne JS, bei reduced-motion und bei Modifier-Klick bleibt es der normale
// Link auf die vorgerenderte Seite. Der Tisch ist Zierde, nie Zugang.

import { goto, onNavigate, preloadData } from '$app/navigation';

const RISE_MS = 520; // Tisch fährt herein, Raum sinkt ab
const FADE_MS = 280; // Ebene löst sich auf, gibt den Explorer frei
const DECODE_CAP = 300; // Wartedeckel fürs Ziel
const EASE = 'cubic-bezier(.33, 0, .2, 1)';
const DESK_SRC = '/media/actors/pult-lamp.avif';

let active = false;
let abortCurrent = null;
let ownNav = false; // markiert die eigene goto(), damit onNavigate sie durchlässt

export function deskActive() {
	return active;
}

const delay = (ms) => new Promise((r) => setTimeout(r, ms));
// Reflow-Warten robust auch im hintergründigen Tab (rAF pausiert dort).
const nextFrame = () => delay(24);

async function prepareTarget(href) {
	try {
		await Promise.race([preloadData(href), delay(DECODE_CAP)]);
	} catch {
		/* preloadData kann werfen, wenn die Route schon lädt — unkritisch */
	}
}

async function runDeskPassage(href) {
	if (active) return;
	active = true;

	// Auf document.body (nicht in die Rooms-Shell) — die Ebene muss den
	// Layoutwechsel Archiv → Explorer überleben, bis sie sich auflöst.
	const layer = document.createElement('div');
	layer.className = 'desk-layer';
	layer.setAttribute('aria-hidden', 'true');
	const scrim = document.createElement('div');
	scrim.className = 'desk-scrim';
	const glow = document.createElement('div');
	glow.className = 'desk-glow';
	const desk = document.createElement('img');
	desk.className = 'desk-img';
	desk.src = DESK_SRC;
	desk.alt = '';
	desk.decoding = 'async';
	layer.append(scrim, glow, desk);
	document.body.appendChild(layer);

	let aborted = false;
	abortCurrent = () => {
		aborted = true;
		layer.style.opacity = '0'; // sofort unsichtbar, falls Abbruch zwischen den Stufen
	};
	// Der Riegel wird in JEDEM Fall gelöst (Auflage 1).
	const finish = () => {
		layer.remove();
		active = false;
		abortCurrent = null;
		ownNav = false;
	};

	try {
		// Auflage 2: Ziel vorbereiten, Deckel 300 ms, DANN fahren.
		await prepareTarget(href);
		if (aborted) return finish();

		layer.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 100, fill: 'forwards' });
		await nextFrame();

		// Der Tisch fährt von unten herein und füllt den unteren Bildrand.
		desk.animate(
			[{ transform: 'translate(-50%, 100%)' }, { transform: 'translate(-50%, 26%)' }],
			{ duration: RISE_MS, easing: EASE, fill: 'forwards' }
		);
		// Das Lampenlicht weitet sich.
		glow.animate(
			[
				{ opacity: 0, transform: 'translate(-50%, 0) scale(0.55)' },
				{ opacity: 1, transform: 'translate(-50%, 0) scale(1)' }
			],
			{ duration: RISE_MS, easing: EASE, fill: 'forwards' }
		);
		// Der Raum dahinter sinkt in Unschärfe/Dunkel (Blur steht statisch im CSS,
		// die Deckung fährt über die Opazität hoch — kein Animieren von backdrop-filter).
		scrim.animate([{ opacity: 0 }, { opacity: 1 }], {
			duration: RISE_MS,
			easing: EASE,
			fill: 'forwards'
		});

		await delay(RISE_MS);
		if (aborted) return finish();

		// Navigieren (Ziel ist vorgeladen). Die eigene goto() lässt onNavigate durch.
		ownNav = true;
		try {
			await goto(href);
		} catch {
			/* Navigation abgebrochen */
		}
		if (aborted) return finish();

		// Die Ebene löst sich auf und gibt die Explorer-Seite frei — der Rekord
		// liegt „auf dem Tisch". Danach in jedem Fall abbauen.
		layer.animate([{ opacity: 1 }, { opacity: 0 }], {
			duration: FADE_MS,
			easing: 'ease-out',
			fill: 'forwards'
		});
		await delay(FADE_MS + 30);
		finish();
	} catch (e) {
		// Härtung: aktiven Übergang in jedem Fall sauber beenden — sonst hinge active.
		console.error('Lesetisch: Übergang fehlgeschlagen, Ebene wird abgebaut:', e);
		finish();
	}
}

export function installDeskPassage() {
	// Nur die als .desk-link markierten Archiv→Explorer-Links werden verstärkt.
	window.addEventListener(
		'click',
		(event) => {
			const link = event.target?.closest?.('a.desk-link[href]');
			if (!link) return;
			// §0-Gates: Modifier/Mittelklick, Reduced-Motion, bereits laufender Übergang
			// oder ein bereits verhinderter Klick bleiben der normale Link.
			if (event.defaultPrevented) return;
			if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
				return;
			}
			if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
			if (active) return;
			const url = new URL(link.href, location.href);
			if (url.origin !== location.origin) return;
			if (url.pathname === location.pathname) return;
			event.preventDefault();
			runDeskPassage(url.pathname + url.search + url.hash);
		},
		{ capture: true }
	);

	// Auflage 3 (Zurück-Sicherheit): eine FREMDE Navigation (Zurück/Vor) während der
	// Bewegung bricht ab und räumt die Ebene; die eigene goto() wird durchgelassen.
	onNavigate(() => {
		if (!active) return;
		if (ownNav) {
			ownNav = false;
			return;
		}
		if (abortCurrent) abortCurrent();
	});
}
