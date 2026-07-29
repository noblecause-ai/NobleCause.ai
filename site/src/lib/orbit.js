// §7 Medaillon-Orbit — die Bahnberechnung als REINE Funktion der Zeit.
//
// Warum ausgelagert: der Orbit läuft über requestAnimationFrame; ein
// Automations-/Headless-Tab meldet dauerhaft document.hidden und drosselt rAF
// auf 0 — dort ist das Kreisen prinzipiell nicht sichtbar. Damit die MATHEMATIK
// trotzdem belegt ist (nicht nur „läuft die Schleife?"), steht sie hier als
// pure Funktion und wird per Unit-Test bei mehreren t geprüft (tests/orbit.test.js).
// Die Komponente ruft dieselbe Funktion je Frame; offen bleibt allein, ob die
// Schleife tickt — und die tickt in jedem sichtbaren Browser.
//
// θ ist ZEITBASIERT (aus t abgeleitet), nicht Frame für Frame aufsummiert:
// dann ist jede Pause (verdeckt/weggescrollt/hidden) folgenlos, egal wie lang —
// beim nächsten Frame steht θ wieder korrekt zur echten Zeit.

export const TAU = Math.PI * 2;

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
// Back-out-Überschwingen: leichtes Übersteuern bei der Ankunft des Einflugs.
const overshoot = (p) => {
	const k = 1.6;
	return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2;
};

// Timing/Bahn-Konstanten (ms bzw. svh). period = Umdrehungsdauer.
export const ORBIT = {
	period: 52000,
	flyDelay: 2450, // Einflug nach dem Pult-Eintrittstakt
	flyDur: 1150,
	flyFrom: 34 // svh unter der Bahn (außerhalb des Bildrands)
};

// Reiner Bahnzustand eines Medaillons zur Zeit t (ms seit Effekt-Start), für den
// Startwinkel theta0 und einen Weitungsfaktor widen (--retreat). Liefert alles,
// was Frame UND SSR-Ruhezustand brauchen: die Richtungs-Cosinus/Sinus (×widen,
// gehen in die CSS-Positionsrechnung), die Tiefe d=(sinθ+1)/2 und die daraus
// abgeleiteten Größen sowie Einflug-Versatz/Opazität und die Kopie-Sichtbarkeit.
export function orbitStateAt(t, theta0, widen = 1, cfg = ORBIT) {
	const since = t - cfg.flyDelay;
	const introP = clamp(since / cfg.flyDur, 0, 1);
	const circT = Math.max(0, since - cfg.flyDur);
	const theta = theta0 + (TAU / cfg.period) * circT;
	const c = Math.cos(theta);
	const s = Math.sin(theta);
	const d = (s + 1) / 2; // 0 hinten (oben) … 1 vorn (unten)
	return {
		theta,
		depth: d,
		cos: c * widen,
		sin: s * widen,
		scale: 0.62 + 0.38 * d,
		bright: 0.6 + 0.4 * d,
		blur: (1 - d) * 1.1,
		fly: (1 - overshoot(introP)) * cfg.flyFrom, // svh; 0 nach dem Einflug
		opacity: introP,
		rearVisible: d < 0.5,
		frontVisible: d >= 0.5
	};
}

// Ruhezustand (SSR/§0): Einflug abgeschlossen, noch nicht gekreist (circT=0) —
// also t = flyDelay + flyDur. Dieselbe Funktion, damit SSR und Frame nie
// auseinanderlaufen.
export function orbitRest(theta0, cfg = ORBIT) {
	return orbitStateAt(cfg.flyDelay + cfg.flyDur, theta0, 1, cfg);
}
