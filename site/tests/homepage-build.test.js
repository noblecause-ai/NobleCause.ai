import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const built = path.join(SITE, 'build', 'index.html');

test('prerendered Homepage enthält die fachliche Wahrheit ohne JavaScript', (context) => {
	if (!fs.existsSync(built)) return context.skip('zuerst npm run build ausführen');
	const html = fs.readFileSync(built, 'utf8');
	for (const value of [
		'Wo hilft meine Spende am meisten?',
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'3/3',
		'2/3',
		'Drei Modelle antworten getrennt',
		'Zählwerk',
		'Kosten:',
		'/sessions/2026-07c/'
	]) assert.ok(html.includes(value), `fehlender prerendered Inhalt: ${value}`);
	assert.ok(html.includes('giving.helenkellerintl.org'));
	assert.match(html, /<del[^>]*>TaRL Africa<\/del>/);
	for (const scene of ['arrival', 'recommendations', 'door-opening', 'antechamber', 'initial', 'revision', 'count', 'archive']) {
		assert.ok(html.includes(`id="${scene}"`), `fehlender Szenenanker: ${scene}`);
	}
});
