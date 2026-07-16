import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import {
	buildHomepageViewModel,
	normalizeHighlights,
	registryMap,
	resolveOrganization
} from './homepage.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const read = (file) => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));
const registry = read('organizations.json');
const session = (id) => read(`sessions/${id}/session.json`);
const sessions = ['2026-07', '2026-07b', '2026-07c'].map(session);

test('neueste Sitzung wird nach number gewählt', () => {
	const latest = [...sessions].sort((a, b) => b.number - a.number)[0];
	assert.equal(latest.id, '2026-07c');
});

test('Registry ist alleinige Quelle für Identität und Spendenlink', () => {
	const map = registryMap(registry);
	const hki = resolveOrganization('helen-keller-international', map);
	assert.equal(hki.name, 'Helen Keller International');
	assert.equal(hki.donationUrl, 'https://giving.helenkellerintl.org/page/FUNUYQRJGHG');
	assert.throws(() => resolveOrganization('nicht-vorhanden', map), /Unbekannte/);
	assert.equal(resolveOrganization('tarl-africa', map).donationUrl, null);
});

test('Highlights normalisieren Array und String', () => {
	assert.deepEqual(normalizeHighlights(['a']), ['a']);
	assert.deepEqual(normalizeHighlights('a'), ['a']);
});

test('2026-07c trägt vier Konsense, Vorbehalt, 2-von-3 und Revisionen', () => {
	const home = buildHomepageViewModel({ session: session('2026-07c'), sessions, registry });
	assert.equal(home.recommendations.filter((item) => item.hasConsensus).length, 4);
	assert.equal(home.recommendations.find((item) => item.pillar === 'A').conditionalCount, 1);
	assert.equal(home.recommendations.find((item) => item.pillar === 'B').count, 2);
	assert.ok(home.revisions.some((item) => item.model === 'GPT' && item.pillar === 'A'));
	assert.ok(home.modelTracks.every((track) => track.rows.length === 4));
});

test('2026-07 zeigt Säule A ohne Sieger und mit drei Registrylinks', () => {
	const home = buildHomepageViewModel({ session: session('2026-07'), sessions, registry });
	const pillar = home.recommendations.find((item) => item.pillar === 'A');
	assert.equal(pillar.hasConsensus, false);
	assert.equal(pillar.votes.length, 3);
	assert.equal(pillar.votes.filter((vote) => vote.organization.donationUrl).length, 3);
	assert.equal(new Set(pillar.votes.map((vote) => vote.organization.id)).size, 3);
});

test('Runden ohne votes werden toleriert, unresolved votes schlagen fehl', () => {
	const clean = structuredClone(session('2026-07c'));
	clean.rounds.unshift({ kind: 'wart_dossier', round: 0 });
	assert.doesNotThrow(() => buildHomepageViewModel({ session: clean, sessions, registry }));
	clean.unresolved_votes = [{ pillar: 'A', organization: 'X', model: 'Y' }];
	assert.throws(() => buildHomepageViewModel({ session: clean, sessions, registry }), /unaufgelöste/);
});
