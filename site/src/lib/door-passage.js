// §6/§C — Echter Türdurchgang (CSS-3D-Kamerafahrt), config-getrieben je Tür.
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
const LEAF_SPREAD = 58; // px, Offen-Position je Flügel zur Laibung (= Hover-Spreizung)
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

// Läuft die Kamerafahrt Quellraum → Zielraum.
// Config je Tür (door-passages.js): wallHole/leafLeft/leafRight = Ebenen aus dem
// Quell-Plate, far = Ziel-Plate (volle Auflösung), origin = gemessene Aperturmitte
// (perspective-origin). href = Zielpfad; onNavigate() setzt das Passage-Flag im
// room-transitions-Zweig (dort läuft dann KEINE eigene VT-Fahrt), onDone() ruft
// extern playStage() nach der Übergabe.
export async function runDoorPassage({
	href,
	wallHole,
	leafLeft: leafLeftSrc,
	leafRight: leafRightSrc,
	far: farSrc,
	origin,
	onNavigate,
	onDone
}) {
	if (active) return;
	active = true;

	const shell = document.querySelector('.rooms-shell') ?? document.body;

	const layer = document.createElement('div');
	layer.className = 'passage-layer';
	// Unsichtbar starten: die Ebene wird gleich angehängt, aber erst NACH dem
	// prepareTarget-Warten eingeblendet. Ohne dieses opacity:0 stünde sie ab dem
	// Anhängen bei Default-opacity 1 (deckt die Bühne sofort dunkel ab), und das
	// spätere animate([{opacity:0},...]) risse sie kurz auf 0 zurück — die Bühne
	// blitzte auf ("Blinzeln"), der Schienen-Rückzug liefe unsichtbar darunter.
	// Mit opacity:0 bleibt die Bühne sichtbar (Akteure/Maschine weichen zurück),
	// dann blendet die Passage weich darüber.
	layer.style.opacity = '0';
	// perspective-origin je Tür (die Kamera zielt auf DIESE Apertur, §6-Nachtrag
	// Ursache 2) — inline statt CSS-fest, weil je Tür verschieden.
	if (origin) layer.style.perspectiveOrigin = origin;
	const dolly = document.createElement('div');
	dolly.className = 'passage-dolly';
	const far = mkImg(farSrc, 'p-plane p-far');
	const leafLeft = mkImg(leafLeftSrc, 'p-plane p-leaf');
	const leafRight = mkImg(leafRightSrc, 'p-plane p-leaf');
	const nearHole = mkImg(wallHole, 'p-plane p-near-hole');
	// Die Flügel starten OFFEN (±LEAF_SPREAD) — genau wie sie der Ruhe-Stapel beim
	// Hover zeigt. Auf Desktop ist ein Klick immer gehovert; so gibt es keinen
	// Zuschnapp zwischen Ruhebild (offen) und Frame 1 der Fahrt. Der Hover HAT die
	// Tür geöffnet, der Klick fährt hindurch.
	leafLeft.style.transform = `translateZ(0) translateX(-${LEAF_SPREAD}px)`;
	leafRight.style.transform = `translateZ(0) translateX(${LEAF_SPREAD}px)`;
	// Maldistanz: far (hinten) → Flügel → Wand-mit-Loch (vorn; ihre opake Laibung
	// deckt die zur Seite gleitenden Flügel ab). Frame 1 = Ruhe-Stapel (offen).
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

	// Der ganze Fahrt-Körper steht in try/catch (Runde G): würfe eine .animate()-
	// Stufe (o. Ä.), bliebe `active` sonst dauerhaft true und JEDER Folgeklick fiele
	// auf die Blende (State-Leak, exakt das „Durchgang ist weg"-Bild aus anderer
	// Ursache). finish() setzt `active` in jedem Fall zurück und entfernt die Ebene;
	// die Bühne holt der Watchdog (passGuard) zurück.
	try {
		// Ziel vorbereiten, DANN erst fahren (Handoff §6.3).
		await prepareTarget(href, farSrc);
		if (aborted) return finish();

		// Ebene weich einblenden — jetzt als sichtbarer Übergang (§Freeze-Runde): die
		// Bühne (Akteure/Maschine) weicht auf ihren Schienen zurück und löst sich
		// über diese Blende in die Passage auf, statt hart abgedeckt zu werden. 320 ms
		// statt 90, damit der Rückzug durch die noch halbtransparente Passage sichtbar
		// bleibt (Frame 1 gleicht ohnehin dem Ruhe-Stapel — kein Zuschnapp).
		layer.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 320, fill: 'forwards' });
		await nextFrame();

		// Die Flügel stehen offen und bleiben stehen (§6-Nachtrag: sie sitzen näher,
		// müssen die Wand früher verlassen) — keine Spreiz-Animation mehr, nur der
		// leafFade unten (früher als die Wand). Ihr translateX steht als inline-Style.

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
	} catch (e) {
		// Härtung: aktive Fahrt in jedem Fall sauber beenden — sonst hinge active.
		console.error('Passage: Fahrt fehlgeschlagen, Ebene wird abgebaut:', e);
		finish();
	}
}
