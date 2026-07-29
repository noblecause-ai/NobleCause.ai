import assert from 'node:assert/strict';
import test from 'node:test';

import { ORBIT, TAU, orbitRest, orbitStateAt } from './orbit.js';

const approx = (a, b, eps = 1e-6) => Math.abs(a - b) <= eps;
const SETTLED = ORBIT.flyDelay + ORBIT.flyDur; // Einflug fertig, circT=0
const TH0 = Math.PI / 2; // ein Beispiel-Startwinkel (vorn/unten)

test('vor dem Einflug: unsichtbar, maximal versetzt, θ = θ0', () => {
	const s = orbitStateAt(0, TH0);
	assert.equal(s.opacity, 0);
	assert.ok(approx(s.fly, ORBIT.flyFrom), 'voller Einflug-Versatz');
	assert.ok(approx(s.theta, TH0), 'noch nicht gekreist');
});

test('Einflug: rückt von unten herein und blendet auf', () => {
	// Früh im Einflug (vor dem Überschwingen): noch unter der Bahn, teil-sichtbar.
	const early = orbitStateAt(ORBIT.flyDelay + ORBIT.flyDur * 0.15, TH0);
	assert.ok(early.fly > 0 && early.fly < ORBIT.flyFrom, `early.fly ${early.fly}`);
	assert.ok(early.opacity > 0 && early.opacity < 0.3, `early.opacity ${early.opacity}`);
	// Back-out-Ease schwingt bewusst leicht über die Bahn (fly < 0), bevor es ruht.
	const over = orbitStateAt(ORBIT.flyDelay + ORBIT.flyDur * 0.55, TH0);
	assert.ok(over.fly < 0, `Überschwingen erwartet, fly ${over.fly}`);
});

test('nach dem Einflug (settled): voll sichtbar, kein Versatz, θ = θ0', () => {
	const s = orbitStateAt(SETTLED, TH0);
	assert.ok(approx(s.opacity, 1));
	assert.ok(approx(s.fly, 0, 1e-9), 'Überschwingen endet bei 0');
	assert.ok(approx(s.theta, TH0), 'circT = 0');
	// orbitRest liefert denselben Zustand
	const r = orbitRest(TH0);
	assert.ok(approx(r.theta, s.theta) && approx(r.scale, s.scale) && r.opacity === s.opacity);
});

test('θ ist zeitbasiert: eine Vierteldrehung nach period/4', () => {
	const s = orbitStateAt(SETTLED + ORBIT.period / 4, TH0);
	assert.ok(approx(s.theta, TH0 + TAU / 4), `θ ${s.theta}`);
});

test('ABNAHME: Transformwerte laufen über 1 s auseinander (Bewegung)', () => {
	const a = orbitStateAt(SETTLED + 3000, TH0);
	const b = orbitStateAt(SETTLED + 4000, TH0);
	// cos/sin (→ Position) und Tiefe ändern sich messbar zwischen den Messungen.
	assert.ok(Math.abs(a.cos - b.cos) > 1e-3, `cos Δ ${Math.abs(a.cos - b.cos)}`);
	assert.ok(Math.abs(a.sin - b.sin) > 1e-3, `sin Δ ${Math.abs(a.sin - b.sin)}`);
	assert.notEqual(a.theta, b.theta);
});

test('Tiefe → Skalierung/Helligkeit/Blur (0,62 → 1,0)', () => {
	const front = orbitStateAt(SETTLED, Math.PI / 2); // sin=1 → d=1 (vorn)
	assert.ok(approx(front.depth, 1) && approx(front.scale, 1.0) && approx(front.blur, 0));
	const rear = orbitStateAt(SETTLED, -Math.PI / 2); // sin=-1 → d=0 (hinten)
	assert.ok(approx(rear.depth, 0) && approx(rear.scale, 0.62) && approx(rear.blur, 1.1));
});

test('Kopie-Sichtbarkeit kippt an d = 0,5 (die unsichtbare Umschaltstelle)', () => {
	const front = orbitStateAt(SETTLED, Math.PI / 2); // d=1
	assert.equal(front.frontVisible, true);
	assert.equal(front.rearVisible, false);
	const rear = orbitStateAt(SETTLED, -Math.PI / 2); // d=0
	assert.equal(rear.rearVisible, true);
	assert.equal(rear.frontVisible, false);
});

test('widen weitet cos/sin proportional (--retreat)', () => {
	const base = orbitStateAt(SETTLED + 1000, TH0, 1);
	const wide = orbitStateAt(SETTLED + 1000, TH0, 1.5);
	assert.ok(approx(wide.cos, base.cos * 1.5) && approx(wide.sin, base.sin * 1.5));
	assert.ok(approx(wide.depth, base.depth), 'Tiefe bleibt (aus rohem sin)');
});
