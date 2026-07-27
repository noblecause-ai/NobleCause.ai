// §6 Phase 1 — Echter Türdurchgang Archiv → Study (CSS-3D-Kamerafahrt).
//
// Eine Übergangsebene, die beim Klick entsteht und nach der Fahrt verschwindet.
// Parallaxe mit korrekter Perspektive: der Browser macht die Perspektivteilung,
// animiert wird im Kern nur EINE Größe — translateZ des Kamerawagens.
//
// Modell (Handoff bei Skalierung 1,0, §6.3): die ferne Ebene (Ziel-Plate) ist
// NICHT gegenskaliert; sie sitzt bei z = -Z_FAR (klein, hinter der Wand verborgen)
// und die Kamera fährt genau C = Z_FAR nach vorn, sodass die ferne Ebene am
// Fahrtende in Cover-Skalierung 1,0 steht = deckungsgleich mit dem realen Study-
// Plate. Die nahe Wand (z=0) wächst schnell und blendet aus, bevor sie die Kamera
// erreicht (C = P). Das Türöffnen ist ein Dissolve der geschlossenen Wand
// (archive-display) auf die Wand-mit-Loch (archive-wall-hole) — dahinter wird die
// ferne Study-Ebene durch das Loch frei.
//
// §0: nur Desktop ≥1200 px und View-Transitions-fähiger Browser (Gate wie der
// Türhotspot); reduced-motion/No-JS fahren gar nicht hier durch.

import { goto, preloadData } from '$app/navigation';

const Z_FAR = 1400; // Tiefe der fernen Ebene (Betrag) = Fahrtstrecke der Kamera
const RIDE_MS = 1250; // Gesamtdauer (Zusatz: 1500–1600, falls nach 1–3 noch flach)
const DOOR_MS = 450; // Türöffnen (Flügel-Spreizung)
const LEAF_SPREAD = 58; // px, Spreizung je Flügel zur Laibung
const NAV_AT = 0.82; // Anteil von RIDE_MS, bei dem goto() feuert (gegen Fahrtende)
const DECODE_CAP = 300; // Wartedeckel fürs Ziel-Plate
const RIDE_EASE = 'cubic-bezier(.5,0,.75,.4)'; // langsam an, spät beschleunigend

let active = false;
let abortCurrent = null;
export function passageActive() {
	return active;
}
// Bricht eine laufende Fahrt ab (z. B. Zurück-Taste mitten drin).
export function abortPassage() {
	if (abortCurrent) abortCurrent();
}

const delay = (ms) => new Promise((r) => setTimeout(r, ms));
// Reflow-Warten robust auch im hintergründigen Tab (rAF pausiert dort).
const nextFrame = () => delay(24);

function mkImg(src, cls) {
	const img = document.createElement('img');
	img.src = src;
	img.className = cls;
	img.alt = '';
	img.setAttribute('aria-hidden', 'true');
	img.decoding = 'async';
	return img;
}

async function prepareTarget(href, plateSrc) {
	const jobs = [];
	try {
		jobs.push(preloadData(href));
	} catch {
		/* preloadData kann werfen, wenn die Route schon lädt — unkritisch */
	}
	const plate = new Image();
	plate.src = plateSrc;
	jobs.push(plate.decode().catch(() => {}));
	await Promise.race([Promise.all(jobs), delay(DECODE_CAP)]);
}

// Läuft die Kamerafahrt Archiv → Study.
// href = Zielpfad, farSrc = Ziel-Plate (Study), onNavigate() setzt das Passage-
// Flag im room-transitions-Zweig (dort läuft dann KEINE eigene VT-Fahrt),
// onDone() ruft extern playStage() nach der Übergabe.
export async function runArchiveToStudyPassage({ href, farSrc, onNavigate, onDone }) {
	if (active) return;
	active = true;

	const shell = document.querySelector('.rooms-shell') ?? document.body;

	const layer = document.createElement('div');
	layer.className = 'passage-layer';
	const dolly = document.createElement('div');
	dolly.className = 'passage-dolly';
	const far = mkImg(farSrc, 'p-plane p-far');
	const leafLeft = mkImg('/media/actors/door-leaf-left.avif', 'p-plane p-leaf');
	const leafRight = mkImg('/media/actors/door-leaf-right.avif', 'p-plane p-leaf');
	const nearHole = mkImg('/media/scenes/archive-wall-hole.avif', 'p-plane p-near-hole');
	// Maldistanz: far (hinten) → Flügel → Wand-mit-Loch (vorn; ihre opake Laibung
	// deckt die zur Seite gleitenden Flügel ab). Frame 1 = Wand + Flügel = Archiv zu.
	dolly.append(far, leafLeft, leafRight, nearHole);
	layer.append(dolly);
	shell.appendChild(layer);

	let aborted = false;
	abortCurrent = () => {
		aborted = true;
	};
	const finish = () => {
		layer.remove();
		active = false;
		abortCurrent = null;
	};

	// Ziel vorbereiten, DANN erst fahren (Handoff §6.3).
	await prepareTarget(href, farSrc);
	if (aborted) return finish();

	// Ebene sanft einblenden (kaschiert Hover→Frame-1, §6.4).
	layer.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 90, fill: 'forwards' });
	await nextFrame();

	// Tür öffnen: die gespreizten Flügel fahren zur Laibung auseinander (0–DOOR_MS);
	// der Teil, der über die Apertur hinausgleitet, verschwindet hinter der opaken
	// Laibung der Wand-mit-Loch. Kein Dissolve mehr.
	const spread = { duration: DOOR_MS, easing: 'cubic-bezier(.4,0,.5,1)', fill: 'forwards' };
	leafLeft.animate([{ transform: 'translateX(0px)' }, { transform: `translateX(-${LEAF_SPREAD}px)` }], spread);
	leafRight.animate([{ transform: 'translateX(0px)' }, { transform: `translateX(${LEAF_SPREAD}px)` }], spread);

	// Kamerafahrt: translateZ 0 → Z_FAR. Der einzige Kern-Antrieb.
	const ride = dolly.animate(
		[{ transform: 'translateZ(0px)' }, { transform: `translateZ(${Z_FAR}px)` }],
		{ duration: RIDE_MS, easing: RIDE_EASE, fill: 'forwards' }
	);

	// Die nahe Wand erst SPÄT ausblenden — sie soll riesig am Rand VORBEIZIEHEN,
	// nicht wegblenden. Blur hochziehen, während sie vorbeizieht (nur noch Textur).
	// Ausgeblendet, BEVOR sie zum Riesen-Blur wird (die Wand passiert die Kamera bei
	// ≈61 % der Strecke) — sonst deckt der Blur den Zielraum. Blur zieht vorher hoch.
	const nearFade = [
		{ opacity: 1, filter: 'blur(0px)', offset: 0 },
		{ opacity: 1, filter: 'blur(2px)', offset: 0.5 },
		{ opacity: 0.7, filter: 'blur(8px)', offset: 0.66 },
		{ opacity: 0, filter: 'blur(14px)', offset: 0.78 },
		{ opacity: 0, filter: 'blur(14px)', offset: 1 }
	];
	nearHole.animate(nearFade, { duration: RIDE_MS, easing: RIDE_EASE, fill: 'forwards' });
	// Die Flügel stehen vorn und verlassen die Wand etwas FRÜHER (vordere Tiefenstufe).
	const leafFade = [
		{ opacity: 1, filter: 'blur(0px)', offset: 0 },
		{ opacity: 1, filter: 'blur(4px)', offset: 0.5 },
		{ opacity: 0, filter: 'blur(10px)', offset: 0.66 },
		{ opacity: 0, filter: 'blur(10px)', offset: 1 }
	];
	leafLeft.animate(leafFade, { duration: RIDE_MS, easing: RIDE_EASE, fill: 'forwards' });
	leafRight.animate(leafFade, { duration: RIDE_MS, easing: RIDE_EASE, fill: 'forwards' });

	// Warmer Schwellen-Bloom an der Laibung im Moment des Durchtritts.
	layer.animate(
		[
			{ boxShadow: 'inset 0 0 0 rgba(255,196,118,0)', offset: 0 },
			{ boxShadow: 'inset 0 0 0 rgba(255,196,118,0)', offset: 0.68 },
			{ boxShadow: 'inset 0 0 42vw rgba(255,196,118,0.18)', offset: 0.88 },
			{ boxShadow: 'inset 0 0 0 rgba(255,196,118,0)', offset: 1 }
		],
		{ duration: RIDE_MS, fill: 'forwards' }
	);

	// Gegen Fahrtende navigieren; onNavigate() unterdrückt die VT-Fahrt.
	await delay(RIDE_MS * NAV_AT);
	if (aborted) return finish();
	onNavigate?.();
	try {
		await goto(href);
	} catch {
		/* Navigation abgebrochen */
	}

	// Fahrt auslaufen lassen (letzter Frame = ferne Ebene bei Cover 1,0), dann
	// abbauen: der reale Study-Raum steht bereits dahinter (deckungsgleich).
	await Promise.race([ride.finished.catch(() => {}), delay(RIDE_MS - RIDE_MS * NAV_AT + 400)]);
	await nextFrame();
	finish();
	onDone?.(); // playStage() extern
}
