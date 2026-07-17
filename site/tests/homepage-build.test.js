import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const built = path.join(SITE, 'build', 'index.html');

test('No-JS-Fallback trägt die volle Wahrheit (nicht die per JS versteckte Bühne)', (context) => {
	if (!fs.existsSync(built)) return context.skip('zuerst npm run build ausführen');
	const html = fs.readFileSync(built, 'utf8');

	// Ohne JS ist NUR .home-fallback sichtbar; die reiche .council-stage ist display:none,
	// bis JS .stage-ready setzt. Deshalb wird GEGEN DEN FALLBACK-BLOCK geprüft, nicht gegen
	// das gesamte HTML — sonst falsche Sicherheit (die Strings stünden in der versteckten Bühne).
	const start = html.indexOf('class="home-fallback');
	const end = html.indexOf('class="council-stage');
	assert.ok(start !== -1 && end !== -1 && end > start, 'Fallback-Block nicht gefunden');
	const fallback = html.slice(start, end);

	// Alles, was der Plan (§7/§21) ohne JS verlangt, muss IM FALLBACK stehen:
	const required = [
		'Wo hilft meine Spende am meisten?', // h1 / Titel
		'Drei Modelle antworten getrennt', // Mechanismus in zwei Sätzen
		'Helen Keller International', // Empfehlung A
		'Against Malaria Foundation', // Empfehlung B
		'Nuclear Threat Initiative', // Empfehlung C
		'Lead Exposure Elimination Project', // Empfehlung D
		'3 von 3', // Zählung Konsens
		'2 von 3', // Zählung 2-von-3
		'giving.helenkellerintl.org', // direkter Spendenlink aus der Registry
		'Unter Vorbehalt', // Vorbehalt (konditionale Stimme)
		'Erst ', // Erstvotum
		'Schluss ', // Schlussvotum
		'Änderungen nach dem Gegenlesen', // sichtbare Revisionen
		'Noch keine Einigkeit', // alltagssprachlicher Zugang zum vollständigen Dissens
		'Korrekturhinweis', // Korrekturhinweis
		'Kosten dieser Sitzung', // Kosten
		'Sitzungsarchiv', // Archiv
		'Sitzung 1', // Archiv-Eintrag
		'/sessions/2026-07c/' // Link zum vollständigen Protokoll
	];
	for (const value of required) {
		assert.ok(fallback.includes(value), `Fallback (ohne JS) fehlt: ${value}`);
	}

	// Gegenprobe zu Blocker 1: der Revisions-Text ist datengetrieben, nicht hartkodiert.
	assert.ok(!fallback.includes('änderten zwei Modelle'), 'hartkodierter Revisions-Text im Fallback');
});

test('Bereichs- und Prozesszeichen sind im No-JS-Grundzustand und Deploy enthalten', (context) => {
	if (!fs.existsSync(built)) return context.skip('zuerst npm run build ausführen');
	const html = fs.readFileSync(built, 'utf8');
	const assets = [
		'pillars/pillar-future-display.jpg',
		'pillars/pillar-relieve-suffering-display.jpg',
		'pillars/pillar-major-risks-display.jpg',
		'pillars/pillar-overlooked-display.jpg',
		'process/process-question-display.jpg',
		'process/process-evidence-display.jpg',
		'process/process-three-answers-display.jpg',
		'process/process-reconsider-display.jpg',
		'process/process-count-display.jpg',
		'process/process-publish-display.jpg'
	];

	for (const asset of assets) {
		assert.ok(html.includes(`/media/${asset}`), `HTML referenziert ${asset} nicht`);
		assert.ok(fs.existsSync(path.join(SITE, 'build', 'media', asset)), `Deploy fehlt ${asset}`);
	}
	assert.ok(!html.includes('>Dissens (vollständiger Wortlaut)<'), 'unerklärter Fachbegriff im Einstieg');
});
