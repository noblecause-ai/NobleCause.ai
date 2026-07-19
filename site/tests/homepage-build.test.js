import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const readBuilt = (rel) => {
	const file = path.join(SITE, 'build', rel);
	return fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
};

// Die Startseite besteht aus drei Räumen, je eine eigene vollständig pragerenderte
// Seite — zweisprachig: Deutsch (Default, unveränderte URLs) und Englisch unter
// /en/…. Ohne JavaScript steht die ganze Wahrheit im HTML dieser sechs Dokumente —
// es gibt keinen per JS versteckten Wahrheitsblock mehr (und keine Scroll-Bühne).
// Deshalb wird je Raum und Sprache gegen die gebaute Datei geprüft.
const PAGES = {
	study: 'index.html',
	council: 'ratssaal/index.html',
	archive: 'archiv/index.html',
	studyEn: 'en/index.html',
	councilEn: 'en/council/index.html',
	archiveEn: 'en/archive/index.html'
};

const requireAll = (html, page, required) => {
	for (const value of required) {
		assert.ok(html.includes(value), `${page} fehlt: ${value}`);
	}
};

test('The Study (/) trägt Einstieg, Mechanismus, Legenden, Akteure und Belege', (context) => {
	const html = readBuilt(PAGES.study);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Study', [
		'Wo hilft meine Spende am meisten?', // h1 / Leitfrage
		'Je ein KI-Modell der Familien Anthropic, OpenAI und Google', // Familien aus den Daten
		// Ablauf-Leiste: alle sechs kanonischen Schritte, Klartext-Sätze
		'So läuft es',
		'Die Frage',
		'Die Belege',
		'Drei Antworten',
		'Umdenken',
		'Zählen',
		'Veröffentlichen',
		'Eine Frage pro Sitzung — vier Bereiche, je eine Empfehlung.',
		'Der Späher sammelt Studien, Kosten-Wirksamkeit und Finanzierungslücken.',
		'Drei Modelle antworten getrennt — jedes Votum öffentlich.', // Zahlwort aus der Datenlage
		'Ein einfaches Programm zählt nur die Nennungen.',
		'Der Wart veröffentlicht alles — Empfehlungen, Uneinigkeit, Kosten.',
		// Dossiers: rohe Rekord-Details hinter Ausklapp (eingeklappt im Erstkontakt)
		'Dossiers',
		'Recherche zeigen',
		'Suchanfragen des Spähers, wörtlich:',
		'Helen Keller International vitamin A supplementation', // Suchanfrage, wörtlich
		'#wart-dossier', // Dossier-Verweis
		'/ratssaal/', // Tür zu The Council
		'/archiv/', // Tür zu The Archive
		// Das Board trägt die Antwort — pragerendert, ohne JS im HTML.
		'Die Antwort dieser Sitzung',
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'3 von 3',
		'giving.helenkellerintl.org',
		// Klartext-Kontext sichtbar, Frage als Zitat-Beleg hinter Ausklapp
		'Worum es ging',
		'Gegenstand der Sitzung', // kuratierter Protokoll-Kontext, wörtlich
		'Frage wörtlich aus dem Protokoll',
		'<blockquote',
		// Tür-Hotspot im Raumbild — pragerenderter Link, trägt ohne JS.
		// (Klasse trägt im Build den Svelte-Scope-Hash: class="door-hotspot svelte-…")
		'door-hotspot',
		'aria-label="Durch die große Tür: The Council"'
	]);
	assert.ok(!html.includes('>Dissens (vollständiger Wortlaut)<'), 'unerklärter Fachbegriff im Einstieg');
	assert.ok(!html.includes('The Scout (der Späher)'), 'Doppelnennung Späher — Variante B verletzt');
	assert.ok(!html.includes('Recherche-Spur'), 'Amtssprache im Einstieg');
	assert.ok(!html.includes('So läuft eine Sitzung'), 'alte Prozess-Legende noch sichtbar');
	assert.ok(!html.includes('href="#antwort"'), 'Self-Link der Prozess-Leiste noch vorhanden');
	// Das Board steht im Hero VOR dem Prozess — die Antwort begrüßt den Eingang.
	assert.ok(
		html.indexOf('Die Antwort dieser Sitzung') < html.indexOf('So läuft es'),
		'Antwort-Board steht nicht mehr vor dem Prozess'
	);
});

test('The Council (/ratssaal/) trägt Empfehlungen, Zählungen, Voten, Revisionen, Spendenlinks', (context) => {
	const html = readBuilt(PAGES.council);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Council', [
		'Wie drei Modelle entscheiden', // h1 — Teilnehmerzahl aus den Daten
		'Je ein KI-Modell der Familien Anthropic, OpenAI und Google', // Erklärtext
		'So läuft es', // Prozess-Leiste auch im Council
		'Drei Antworten',
		'Helen Keller International', // Empfehlung A
		'Against Malaria Foundation', // Empfehlung B
		'Nuclear Threat Initiative', // Empfehlung C
		'Lead Exposure Elimination Project', // Empfehlung D
		'3 von 3', // Zählung Konsens (aus convergence)
		'2 von 3', // Zählung 2-von-3 (aus convergence)
		'giving.helenkellerintl.org', // direkter Spendenlink aus der Registry
		'Unter Vorbehalt', // Vorbehalt (konditionale Stimme)
		'Alle Voten zeigen', // volle Matrix hinter Ausklapp
		'Erst ', // Erstvotum
		'Schluss ', // Schlussvotum
		'Änderungen nach dem Gegenlesen', // Revisionen
		'NobleCause nimmt kein Geld an.', // Geldfluss-Hinweis
		'Das Programm zählt nur gleiche Nennungen.' // Zählwerk
	]);
	// Der Revisions-Text ist datengetrieben, nicht hartkodiert.
	assert.ok(!html.includes('änderten zwei Modelle'), 'hartkodierter Revisions-Text');
	// Voten-Ordnung: Revisionen zuerst, die volle Matrix hinter Ausklapp danach.
	assert.ok(
		html.indexOf('Änderungen nach dem Gegenlesen') < html.indexOf('Voten je Modell'),
		'Revisionen stehen nicht vor der Voten-Matrix'
	);
});

test('The Archive (/archiv/) trägt Sitzungen, Kosten, Korrekturhinweis und Dissens-Zugang', (context) => {
	const html = readBuilt(PAGES.archive);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Archive', [
		'Sitzungsarchiv',
		'Sitzung 1', // Archiv-Eintrag (Nicht-Konsens)
		'Noch keine Einigkeit', // alltagssprachlicher Dissens-Zugang
		'Vollständiger Wortlaut', // aufklappbarer Dissens (gerendert, nicht roh)
		'Korrekturhinweis',
		'Kosten dieser Sitzung',
		'/sessions/2026-07c/' // Link zum vollständigen Protokoll
	]);
});

test('The Study (/en/) zeigt englische Chrome — Rekordfrage bleibt deutsch mit Vermerk', (context) => {
	const html = readBuilt(PAGES.studyEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Study (EN)', [
		'Where does my donation help the most?',
		'One AI model each from Anthropic, OpenAI, and Google', // Familien aus den Daten
		'Three AI models review the same evidence', // head description
		// The process rail: all six canonical steps, plain-language sentences
		'How it works',
		'The question',
		'The evidence',
		'Three answers',
		'Second thoughts',
		'The count',
		'Publication',
		'The Scout gathers studies, cost-effectiveness and funding gaps.',
		'Three models answer separately — every vote public.', // number word from the data
		'The Warden publishes everything — recommendations, disagreement, costs.',
		// Dossiers hinter Ausklapp
		'Dossiers',
		'Show the research trail',
		'/en/council/', // Tür zu The Council (EN)
		'/en/archive/', // Tür zu The Archive (EN)
		'Original protocol in German.', // Rekord-Vermerk bei der aktuellen Frage
		'lang="de"', // Rekordtext maschinell als deutsch markiert
		// Das Board trägt die Antwort — pragerendert, ohne JS im HTML.
		"This session's answer",
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'3 of 3',
		'giving.helenkellerintl.org',
		// Plain-language context visible, question as verbatim quote behind a toggle
		'What this session was about',
		'Gegenstand der Sitzung', // curated protocol context stays German (record)
		'The question — verbatim from the protocol',
		'<blockquote',
		// Tür-Hotspot im Raumbild — pragerenderter Link, trägt ohne JS.
		// (Klasse trägt im Build den Svelte-Scope-Hash: class="door-hotspot svelte-…")
		'door-hotspot',
		'aria-label="Through the grand door: The Council"'
	]);
	// Die publizierte Frage steht unverändert (deutsch) im EN-Dokument.
	assert.ok(html.includes('Spende'), 'deutsche Rekordfrage fehlt im EN-Raum');
	assert.ok(!html.includes('The Scout and The Warden'), 'Doppelblock Akteure noch sichtbar');
});

test('The Council (/en/council/) zeigt englische Chrome, deutsche Vorbehalte mit Vermerk', (context) => {
	const html = readBuilt(PAGES.councilEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Council (EN)', [
		'How three models decide', // h1 — participant count from the data
		'One AI model each from Anthropic, OpenAI, and Google', // explainer text
		'How it works', // process rail in the council too
		'Three answers',
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'3 of 3', // Zählung Konsens (Trennwort aus der Locale)
		'2 of 3',
		'With reservation', // Vorbehalt-Label (Chrome)
		'Show all votes', // full matrix behind a toggle
		'Original protocol in German.', // Rekord-Vermerk beim Vorbehalt
		'First ', // Erstvotum
		'Final ', // Schlussvotum
		'Changes after cross-reading', // Revisionen
		'NobleCause does not handle money', // Geldfluss-Hinweis
		'The program only counts matching mentions.' // Zählwerk
	]);
	// Organisationsbeschreibungen (und ihr orgEn-Fallback) haben im entrümpelten
	// Council keine Anzeigefläche mehr — der Mechanismus lebt in
	// RecommendationCard.svelte weiter (derzeit unreferenziert).
});

test('The Archive (/en/archive/) zeigt englische Chrome — Rekord bleibt deutsch mit Vermerk', (context) => {
	const html = readBuilt(PAGES.archiveEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Archive (EN)', [
		'Session archive',
		'Session 1',
		'No agreement yet',
		'Correction notice',
		'Full text',
		'Cost of this session',
		'/sessions/2026-07c/',
		'Original protocol in German.', // Rekord-Vermerk (Korrektur/Dissens)
		'The full protocol is published in German.', // Hinweis am Protokoll-Link
		'lang="de"', // Rekordtexte maschinell als deutsch markiert
		'Korrektur vom 14.07.2026' // publizierter Rekord: unverändert deutsch
	]);
});

test('Sprachumschalter verlinkt die Schwester-Route in allen sechs Räumen', (context) => {
	const expectations = {
		study: ['/en/', 'English version'],
		council: ['/en/council/', 'English version'],
		archive: ['/en/archive/', 'English version'],
		studyEn: ['/', 'Deutsche Fassung'],
		councilEn: ['/ratssaal/', 'Deutsche Fassung'],
		archiveEn: ['/archiv/', 'Deutsche Fassung']
	};
	for (const [room, [href, label]] of Object.entries(expectations)) {
		const html = readBuilt(PAGES[room]);
		if (html === null) return context.skip('zuerst npm run build ausführen');
		assert.ok(html.includes('lang-switch'), `${room}: Umschalter fehlt`);
		assert.ok(html.includes(`href="${href}"`), `${room}: Schwester-Link ${href} fehlt`);
		assert.ok(html.includes(`aria-label="${label}"`), `${room}: aria-label ${label} fehlt`);
	}
});

test('html lang und hreflang sind sprachrichtig gesetzt', (context) => {
	for (const [room, rel] of Object.entries(PAGES)) {
		const html = readBuilt(rel);
		if (html === null) return context.skip('zuerst npm run build ausführen');
		const isEn = room.endsWith('En');
		assert.ok(
			html.includes(`<html lang="${isEn ? 'en' : 'de'}">`),
			`${room}: <html lang> falsch`
		);
		// Jeder Raum verweist per hreflang auf beide Sprachen + x-default (DE).
		for (const code of ['de', 'en', 'x-default']) {
			assert.ok(html.includes(`hreflang="${code}"`), `${room}: hreflang ${code} fehlt`);
		}
	}
});

test('Jeder Raum hat genau ein wirksames h1', (context) => {
	for (const [room, rel] of Object.entries(PAGES)) {
		const html = readBuilt(rel);
		if (html === null) return context.skip('zuerst npm run build ausführen');
		const count = (html.match(/<h1[\s>]/g) ?? []).length;
		assert.equal(count, 1, `${room}: erwartet genau ein h1, gefunden ${count}`);
	}
});

test('Embleme, Szenen und Tür-Bilder sind referenziert und im Deploy enthalten', (context) => {
	const pages = Object.values(PAGES).map(readBuilt);
	if (pages.some((html) => html === null)) return context.skip('zuerst npm run build ausführen');
	const html = pages.join('\n');
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
		'process/process-publish-display.jpg',
		'doors/door-study-archive-display.jpg',
		'doors/door-council-archive-display.jpg',
		'scenes/antechamber-display.jpg',
		'scenes/antechamber-portrait-display.jpg',
		'scenes/hall-display.jpg',
		'scenes/archive-display.jpg',
		'scenes/archive-portrait-display.jpg'
	];
	for (const asset of assets) {
		assert.ok(html.includes(`/media/${asset}`), `kein Raum referenziert ${asset}`);
		assert.ok(fs.existsSync(path.join(SITE, 'build', 'media', asset)), `Deploy fehlt ${asset}`);
	}
});
