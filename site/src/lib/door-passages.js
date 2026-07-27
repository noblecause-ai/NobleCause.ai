// §C — Türdurchgang-Konfiguration je Quellraum.
//
// EINE Quelle für zwei Verbraucher, damit Frame 1 der Fahrt vom Ruhebild
// KONSTRUKTIV (nicht gemessen) gleich ist (§1):
//   1. Der Ruhe-Stapel in StageHero (Void → farLo → Flügel → Wand-mit-Loch bei
//      Kamera 0) — das Bild, das der Spalt beim Hover zeigt.
//   2. Die Kamerafahrt in door-passage.js (dieselben Ebenen, farHi, Kamera fährt).
//
// Beide tragen dieselbe Cover-Geometrie, dasselbe `perspective`/`origin` und
// dasselbe far-z — nur die Auflösung der fernen Ebene (Ruhe klein, Fahrt voll)
// und die Kamera (Ruhe 0, Fahrt 0→Z_FAR) unterscheiden sich.
//
// Origin je Tür: entweder `origin` = am Cover-Crop gemessene, feste Viewport-%
// (Study/Archiv — sie sitzen und werden nicht angefasst), ODER `aperturePlate` =
// Aperturmitte in PLATE-Koordinaten (Council). Aus aperturePlate wird die Origin
// zur LAUFZEIT über dieselbe Cover-Rechnung abgeleitet, die auch die Tür on-screen
// platziert — so wandert sie mit dem Cover-Crop mit, statt als feste % zu klaffen
// (Runde E §2: eine Quelle, keine zweite Konstante). `target` = Zielraum.

// Cover-Abbildung (object-fit:cover, object-position:center top) eines Punkts auf
// dem Plate (px,py) → Viewport-% als perspective-origin-String. Dieselbe Rechnung,
// die das StageHero-Plate rendert; nur Client (nutzt window).
export function coverOrigin(px, py, plateW = 1672, plateH = 941) {
	// clientWidth/Height statt innerWidth/Height: die fixe Bildebene füllt den
	// Viewport OHNE Scrollbar, und perspective-origin-% lösen gegen genau diese
	// Box auf — mit innerWidth klaffte sonst die Scrollbarbreite (~0,5 pt in x).
	const vw = document.documentElement.clientWidth;
	const vh = document.documentElement.clientHeight;
	const scale = Math.max(vw / plateW, vh / plateH);
	const xOff = (vw - plateW * scale) / 2; // center
	const yOff = 0; // top
	const sx = xOff + px * scale;
	const sy = yOff + py * scale;
	return `${((sx / vw) * 100).toFixed(2)}% ${((sy / vh) * 100).toFixed(2)}%`;
}

// Die zu benutzende Origin: abgeleitet, wenn aperturePlate gesetzt ist, sonst die
// feste Konstante. Einziger Ableitungsort für beide Verbraucher (Fahrt + Ruhe).
export function passageOrigin(cfg) {
	return cfg.aperturePlate ? coverOrigin(cfg.aperturePlate.x, cfg.aperturePlate.y) : cfg.origin;
}

export const DOOR_PASSAGES = {
	archive: {
		target: 'study',
		wallHole: '/media/scenes/archive-wall-hole.avif',
		leafLeft: '/media/actors/door-leaf-left.avif',
		leafRight: '/media/actors/door-leaf-right.avif',
		farHi: '/media/scenes/antechamber-display.avif',
		farLo: '/media/scenes/antechamber-display-lo.avif',
		origin: '48.8% 41%'
	},
	study: {
		target: 'council',
		wallHole: '/media/scenes/antechamber-wall-hole.avif',
		leafLeft: '/media/actors/antechamber-leaf-left.avif',
		leafRight: '/media/actors/antechamber-leaf-right.avif',
		farHi: '/media/scenes/hall-display.avif',
		farLo: '/media/scenes/hall-display-lo.avif',
		origin: '49.5% 55%'
	},
	council: {
		target: 'archive',
		wallHole: '/media/scenes/hall-wall-hole.avif',
		leafLeft: '/media/actors/hall-leaf-left.avif',
		leafRight: '/media/actors/hall-leaf-right.avif',
		farHi: '/media/scenes/archive-display.avif',
		farLo: '/media/scenes/archive-display-lo.avif',
		// Zielpunkt der Fahrt auf dem 1672×941-Plate = visuelle Türmitte: x = Naht
		// (wo man durchtritt; die Tür ist leicht asymmetrisch, darum nicht die
		// Rechteckmitte der Öffnung), y = Mitte der Öffnung [212,610]. Origin folgt
		// daraus zur Laufzeit über coverOrigin. (Schnitt-Apertur ist x[712,950].)
		aperturePlate: { x: 850, y: 411 }
	}
};
