import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { getAmfCase } from '../src/lib/server/amf.js';

const built = path.resolve('build');
const root = path.resolve('..');
const read = (file) => fs.readFileSync(path.join(built, file), 'utf8');
const caseData = getAmfCase();
const pages = ['fall/amf/index.html', 'fall/amf/rat/index.html', 'fall/amf/belege/index.html'];
const escapeHtml = (text) => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

test('AMF zeigt die fünf ursprünglichen B-Schlussvoten und ihre Originalgründe', () => {
	const session = JSON.parse(fs.readFileSync(path.join(root, 'sessions/2026-10-21-regular/session.json')));
	const votes = session.rounds.find((round) => round.kind === 'final_vote').votes;
	assert.equal(caseData.voices.length, 5);
	const html = read(pages[1]);
	for (const voice of caseData.voices) {
		const original = votes.find((vote) => vote.model === voice.model).recommendations.find((vote) => vote.pillar === 'B');
		assert.deepEqual(voice.vote, original);
		assert.ok(html.includes(escapeHtml(voice.reason)), voice.label + ' hat einen abweichenden Grund');
		assert.ok(html.includes(voice.medallion));
		assert.ok(html.includes(voice.protocolHref));
	}
	assert.equal(caseData.session.result.votes_abstained, 3);
	assert.equal(caseData.session.result.individual_votes.length, 2);
	assert.equal(caseData.session.result.has_consensus, false);
	assert.ok(html.includes('Die November-Belege wurden erst später nachrecherchiert.'));
	assert.ok(html.includes(escapeHtml(session.question)));
});

test('Jede tragende Fallaussage hat eine erreichbare Belegkarte mit Provenienz', () => {
	const archive = read(pages[2]);
	for (const card of caseData.cards) {
		assert.ok(archive.includes('id="beleg-' + card.id + '"'));
		for (const field of ['claim', 'limit', 'publisher', 'period', 'retrieved', 'locator']) {
			assert.ok(archive.includes(escapeHtml(card[field])), card.id + ' fehlt ' + field);
		}
		for (const source of card.sources) assert.ok(archive.includes(escapeHtml(source.url)));
	}
	for (const page of pages) {
		for (const match of read(page).matchAll(/href="\/fall\/amf\/belege\/#beleg-([a-z]+)"/g)) {
			assert.ok(caseData.cards.some((card) => card.id === match[1]), 'Unbekannte Belegkarte ' + match[1]);
		}
	}
});

test('Die Veröffentlichungskandidaten enthalten die Korrekturen und keine privaten Daten', () => {
	const archive = read(pages[2]);
	assert.ok(archive.includes('4,85 USD'));
	assert.ok(archive.includes('90,2 %'));
	assert.ok(archive.includes('87,1 %'));
	assert.ok(archive.includes('61,0 %'));
	assert.ok(archive.includes('52,5 %'));
	assert.ok(archive.includes('24,2 %'));
	assert.ok(archive.includes('17,2 %'));
	const monitoring = caseData.cards.find((card) => card.id === 'monitoring');
	assert.ok(archive.includes(escapeHtml(monitoring.presenceDefinition)));
	assert.ok(archive.includes(escapeHtml(monitoring.conditionDefinition)));
	assert.ok(monitoring.presenceDefinition.includes('laut befragten Haushalten ursprünglich erhaltenen AMF-Netze'));
	assert.ok(monitoring.conditionDefinition.includes('Vermisste Netze sind aus dieser Bezugsgröße ausgeschlossen'));
	assert.ok(monitoring.conditionDefinition.includes('als zerrissen entsorgte Netze bleiben enthalten'));

	assert.ok(archive.includes('kein aktueller Entscheidungswert'));
	assert.ok(archive.includes('Evaluator-Modell'));
	for (const page of pages) {
		const html = read(page);
		assert.ok(html.includes('Ratsberatung und automatische Recherche sind pausiert.'));
		assert.doesNotMatch(html, /<meta[^>]+name="robots"[^>]+noindex/);
		assert.ok(html.includes('rel="canonical" href="https://noblecause.ai/' + page.replace('index.html', '') + '"'));
		assert.ok(html.includes(caseData.organization.donation_url));
		assert.doesNotMatch(html, /\/Users\/|packet_sha256|OPENROUTER_API_KEY|mirhamed@yahoo|sk-or-v1-/);
		assert.doesNotMatch(html, /<iframe|<input|<form/);
	}
});

test('Der reguläre Einstieg kennzeichnet die Pause und verlinkt den Fall in seiner Sprache', () => {
    const german = read('index.html');
    const english = read('en/index.html');
    assert.ok(german.includes('Aktive Rats- und Rechercheläufe sind derzeit pausiert.'));
    assert.ok(english.includes('Automated council and research runs are currently paused.'));
    assert.ok(german.includes('href="/fall/amf/"'));
    assert.ok(english.includes('href="/en/case/amf/"'));
    assert.ok(english.includes('Open the AMF case study'));
    assert.ok(english.includes('Reviewed Case Study: Malaria protection with AMF'));
    assert.ok(!english.includes('Explore the case in German'));
});


const englishCase = getAmfCase('en');
const englishPages = ['en/case/amf/index.html', 'en/case/amf/council/index.html', 'en/case/amf/evidence/index.html'];

test('EN übersetzt alle sieben Belegkarten ohne Quellenwechsel und erhält die Monitoring-Grundmengen', () => {
	const html = read(englishPages[2]);
	assert.equal(englishCase.cards.length, 7);
	for (const original of caseData.cards) {
		const card = englishCase.cards.find((entry) => entry.id === original.id);
		assert.deepEqual(card.sources.map((source) => source.url), original.sources.map((source) => source.url));
		for (const field of ['title', 'kind', 'claim', 'limit', 'publisher', 'period', 'retrieved', 'locator']) {
			assert.ok(card[field]);
			assert.ok(html.includes(escapeHtml(card[field])), card.id + ' lacks English ' + field);
		}
	}
	for (const value of ['90.2%', '87.1%', '61.0%', '52.5%', '24.2%', '17.2%']) assert.ok(html.includes(value));
	assert.ok(html.includes('Missing nets are excluded from this denominator'));
	assert.ok(html.includes('nets discarded because they were torn remain included'));
	assert.ok(html.includes('as reported by surveyed households'));
	assert.ok(html.includes('USD 4.85'));
	assert.ok(html.includes('Evaluator model'));
	assert.ok(html.includes('Organisation self-report'));
});

test('EN kennzeichnet alle fünf historischen Übersetzungen und bewahrt Originalgründe und Stimmen', () => {
	const html = read(englishPages[1]);
	assert.equal(englishCase.voices.length, 5);
	assert.equal((html.match(/>German original</g) || []).length, 5);
	assert.equal((html.match(/Final vote on pillar B · English translation/g) || []).length, 5);
	assert.ok(html.includes('English translations of the German record by Codex nc 2 (GPT-6).'));
	assert.ok(html.includes(escapeHtml(englishCase.session.questionTranslation)));
	assert.ok(html.includes(escapeHtml(caseData.session.question)));
	for (const voice of englishCase.voices) {
		const original = caseData.voices.find((entry) => entry.model === voice.model);
		assert.deepEqual(voice.vote, original.vote);
		assert.deepEqual(voice.initialVote, original.initialVote);
		assert.equal(voice.reason, original.reason);
		assert.ok(voice.reasonTranslation && voice.reasonTranslation !== voice.reason);
		assert.ok(html.includes(escapeHtml(voice.reasonTranslation)));
		assert.ok(html.includes(escapeHtml(original.reason)));
		assert.ok(html.includes(voice.protocolHref));
	}
	assert.deepEqual(englishCase.session.result, caseData.session.result);
});

test('Alle sechs Fallrouten haben passende Dokumentsprache und gegenseitige Sprachverweise', () => {
	for (const [index, page] of pages.entries()) {
		for (const [lang, file] of [['de', page], ['en', englishPages[index]]]) {
			const html = read(file);
			const route = '/' + file.replace('index.html', '');
			assert.ok(html.includes('<html lang="' + lang + '"'));
			assert.ok(html.includes('rel="canonical" href="https://noblecause.ai' + route + '"'));
			for (const [targetLang, targetFile] of [['de', page], ['en', englishPages[index]]]) {
				const target = '/' + targetFile.replace('index.html', '');
				assert.ok(html.includes('hreflang="' + targetLang + '" href="https://noblecause.ai' + target + '"'));
				assert.ok(html.includes('href="' + target + '" lang="' + targetLang + '"'));
			}
			assert.doesNotMatch(html, /<meta[^>]+name="robots"[^>]+noindex/);
			assert.doesNotMatch(html, /\/Users\/|OPENROUTER_API_KEY|sk-or-v1-/);
		}
	}
});
