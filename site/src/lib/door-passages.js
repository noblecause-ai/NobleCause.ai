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
// `origin` = am gerenderten Cover-Crop gemessene Aperturmitte (perspective-origin,
// §6-Nachtrag Ursache 2), je Tür verschieden. `target` = Zielraum (roomOfPath).

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
	}
	// council (→ archive) folgt nach abgenommenem Study.
};
