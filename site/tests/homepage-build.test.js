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
		'Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu.', // Raum-Lead
		'Je ein KI-Modell verschiedener Familien prüft dieselben Belege', // Pitch (ohne Familiennamen/Zahl)
		'Warum so umständlich? ▸', // Verfahrens-Ausklapp im stabilen Kopf
		'Ein einzelnes Modell kann irren oder eine blinde Stelle haben.',
		// Prozess-Röhre: alle sechs kanonischen Schritte mit Name + Klartext-Satz
		// AN der Kugel (die FlowRail „So läuft es" ist entfallen)
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
		// Klartext-Antwort (§3.3): die publizierte plain-Schicht trägt jede Zeile —
		// wortgleich aus den Daten (Bereich, Org und Warum stecken im Feld,
		// das Frontend setzt nichts zusammen).
		'Die Empfehlungen dieser Sitzung',
		'Zukunft → Helen Keller International, weil ihre Wirkung besser belegt ist',
		'Leid lindern → Against Malaria Foundation, weil imprägnierte Moskitonetze',
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'giving.helenkellerintl.org', // Spendenlink in der Klartext-Zeile (Registry)
		// Dossiers (§3.4): Klartext-Frage sichtbar (plain.question), Wortlaut an der Kennzeichnung
		'Dossiers',
		'Die Frage dieser Sitzung',
		'Bereich Zukunft: Ist Kindergesundheit (Helen Keller) oder Bildung (Pratham/TaRL) besser belegt?', // plain.question, wortgleich
		'Die Frage im Wortlaut ▸',
		'<blockquote',
		'Suchanfragen des Spähers ▸',
		'Helen Keller International vitamin A supplementation', // Suchanfrage, wörtlich
		'#wart-dossier', // Dossier-Verweis
		'/ratssaal/', // Tür zu The Council
		'/archiv/', // Tür zu The Archive
		// Das Board trägt die Antwort — pragerendert, ohne JS im HTML.
		'Die Antwort der letzten Sitzung',
		'3 von 3',
		// Tür-Hotspot im Raumbild — pragerenderter Link, trägt ohne JS.
		// (Klasse trägt im Build den Svelte-Scope-Hash: class="door-hotspot svelte-…")
		'door-hotspot',
		'aria-label="Durch die große Tür: The Council"'
	]);
	// Dynamischer Raumteil: EIN Wort + Raum-Lead (Titelbereich-Neuordnung).
	assert.ok(html.includes('room-word'), 'Raumwort-Element fehlt');
	assert.match(html, />Study<\/p>/, 'Raumwort „Study" fehlt');
	assert.ok(!html.includes('The Study · das Vorzimmer'), 'alte Eyebrow noch sichtbar');
	assert.ok(!html.includes('So läuft es'), 'entfallene FlowRail noch sichtbar');
	assert.ok(!html.includes('>Dissens (vollständiger Wortlaut)<'), 'unerklärter Fachbegriff im Einstieg');
	assert.ok(!html.includes('The Scout (der Späher)'), 'Doppelnennung Späher — Variante B verletzt');
	assert.ok(!html.includes('Recherche-Spur'), 'Amtssprache im Einstieg');
	assert.ok(!html.includes('So läuft eine Sitzung'), 'alte Prozess-Legende noch sichtbar');
	assert.ok(!html.includes('href="#antwort"'), 'Self-Link der Prozess-Leiste noch vorhanden');
	assert.ok(!html.includes('Worum es ging'), 'alter Fachtext-Titel noch sichtbar');
	assert.ok(!html.includes('Recherche zeigen'), 'alte Ausklapp-Grammatik noch sichtbar');
	assert.ok(
		!html.includes('Je ein KI-Modell der Familien Anthropic'),
		'Familiennamen-Hardcode im Fließtext — der Pitch trägt bewusst keine Namen'
	);
	// Klartext-Schicht ist publiziert: kein Vermerk, keine Doppelung, kein Fallback.
	assert.ok(!html.includes('Klartext folgt'), 'Vermerk trotz publizierter Klartext-Schicht noch sichtbar');
	assert.ok(
		!html.includes('International, Zukunft →'),
		'Bereichs-Label gedoppelt — die plain-Zeile darf nicht erneut zusammengesetzt werden'
	);
	assert.ok(
		!html.includes('>Gegenstand der Sitzung'),
		'Fallback Protokoll-Kontext trotz vorhandener plain.question noch sichtbar'
	);
	// Das Board steht im Dokument VOR der Lese-Fassung — die Antwort begrüßt den Eingang.
	assert.ok(
		html.indexOf('Die Antwort der letzten Sitzung') < html.indexOf('Die Empfehlungen dieser Sitzung'),
		'Antwort-Board steht nicht mehr vor der Lese-Fassung'
	);
});

test('The Council (/ratssaal/) trägt Zählwerk, Voten, Revisionen in der Marke, Spendenlinks', (context) => {
	const html = readBuilt(PAGES.council);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Council', [
		// Stabiler Kopf — auf allen drei Raum-Seiten identisch (Titelbereich-Neuordnung)
		'Wo hilft meine Spende am meisten?', // h1 — die Leitfrage überall
		'Je ein KI-Modell verschiedener Familien prüft dieselben Belege', // Pitch
		'Warum so umständlich? ▸', // inline-Ausklapp im Kopf
		'Getrennt abgestimmt, dann öffentlich gezählt. Was mehrfach genannt wird, wird Empfehlung.', // Raum-Lead
		'Drei Antworten', // Röhren-Kugel (Name)
		// „Wie gezählt wurde" — ein Block statt drei (§4.2)
		'Wie gezählt wurde',
		'Das Programm zählt nur gleiche Nennungen.',
		'Helen Keller International', // Nennung in den Marken
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'3 von 3', // Zählung Konsens (aus convergence)
		'2 von 3', // Zählung 2-von-3 (aus convergence)
		// Modell-Marken generisch aus modelTracks
		'Claude Opus',
		'Gemini Pro',
		// Revisionen leben in der Marke: Erstvotum durchgestrichen
		// (Svelte-Scope-Hash am <del>: nur Inhalt + Tag-Ende vergleichen)
		'>TaRL Africa</del>',
		'Vorbehalt ▸', // Vorbehalt-Ausklapp in der Zeile
		'Alle Voten im Wortlaut ▸', // volle Matrix am Blockende
		'Erst ', // Erstvotum (ModelPulpits)
		'Schluss ', // Schlussvotum
		'NobleCause nimmt kein Geld an.', // Geldfluss-Hinweis
		'giving.helenkellerintl.org' // direkter Spendenlink (Tafel, Registry)
	]);
	// Raumwort + entfallener alter Kopf.
	assert.match(html, />Council<\/p>/, 'Raumwort „Council" fehlt');
	assert.ok(!html.includes('Wie drei Modelle entscheiden'), 'alter dynamischer h1 noch sichtbar');
	assert.ok(!html.includes('The Council · der Ratssaal'), 'alte Eyebrow mit Sitzungs-Nr. noch sichtbar');
	assert.ok(!html.includes('So läuft es'), 'entfallene FlowRail noch sichtbar');
	// Entfallene Blöcke und alte Copy bleiben draußen.
	assert.ok(!html.includes('Vier Empfehlungen'), 'alter Empfehlungs-Block noch sichtbar');
	assert.ok(!html.includes('Änderungen nach dem Gegenlesen'), 'Revisions-Abschnitt nicht in die Marke überführt');
	assert.ok(!html.includes('Zählwerk'), 'alter Zählwerk-Block noch sichtbar');
	assert.ok(!html.includes('Alle Voten zeigen'), 'alte Ausklapp-Grammatik noch sichtbar');
	assert.ok(!html.includes('Unter Vorbehalt'), 'altes Vorbehalt-Label noch sichtbar');
	assert.ok(
		!html.includes('Je ein KI-Modell der Familien'),
		'mit The Study identischer Lead noch sichtbar'
	);
	// Ordnung: der Zähl-Block trägt, die volle Matrix hängt am Blockende.
	assert.ok(
		html.indexOf('Wie gezählt wurde') < html.indexOf('Alle Voten im Wortlaut'),
		'Voten-Matrix steht nicht am Blockende'
	);
});

test('The Archive (/archiv/) trägt Sitzungen mit Ergebnis-Chips, Kosten, Korrektur, Dissens', (context) => {
	const html = readBuilt(PAGES.archive);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Archive', [
		// Stabiler Kopf — auf allen drei Raum-Seiten identisch (Titelbereich-Neuordnung)
		'Wo hilft meine Spende am meisten?',
		'Je ein KI-Modell verschiedener Familien prüft dieselben Belege',
		'Warum so umständlich? ▸',
		'Jede Sitzung, vollständig und unverändert — Empfehlungen, Uneinigkeit, Kosten.', // Raum-Lead
		'Sitzungsarchiv',
		'Sitzung 1 · 2026-07-07', // Archiv-Eintrag mit Datum
		// Ergebnis-Chips (§5.2): registry-aufgelöste Namen, offener Bereich markiert
		'Malaria Consortium',
		'Centre for the Governance of AI',
		'keine Einigung',
		'Noch keine Einigkeit', // alltagssprachlicher Dissens-Zugang
		'Wortlaut des Rates ▸', // aufklappbarer Dissens (gerendert, nicht roh)
		'Korrekturhinweis',
		'Kosten dieser Sitzung',
		'/sessions/2026-07c/' // Link zum vollständigen Protokoll
	]);
	assert.match(html, />Archive<\/p>/, 'Raumwort „Archive" fehlt');
	assert.ok(!html.includes('The Archive · das Archiv'), 'alte Eyebrow noch sichtbar');
	assert.ok(!html.includes('Empfehlungen in allen Bereichen'), 'alte Zeilen-Zusammenfassung noch sichtbar');
});

test('The Study (/en/) zeigt englische Chrome — Rekordfrage bleibt deutsch mit Vermerk', (context) => {
	const html = readBuilt(PAGES.studyEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Study (EN)', [
		'Where does my donation help the most?',
		'Every session begins here — with a question and the evidence for it.', // room lead
		'One AI model each from different families reviews the same evidence', // pitch (no names/count)
		'Why so elaborate? ▸', // process toggle in the plaque
		'A single model can be wrong or have a blind spot.',
		'Three AI models review the same evidence', // head description
		// The process tube: all six canonical steps, plain-language sentences
		// on the beads (the "How it works" rail is gone)
		'The question',
		'The evidence',
		'Three answers',
		'Second thoughts',
		'The count',
		'Publication',
		'The Scout gathers studies, cost-effectiveness and funding gaps.',
		'Three models answer separately — every vote public.', // number word from the data
		'The Warden publishes everything — recommendations, disagreement, costs.',
		// Plain-language answer (§3.3): the published German plain layer shows with a
		// language marker (plainEnDe fallback) — never machine-translated.
		"This session's recommendations",
		'Zukunft → Helen Keller International, weil ihre Wirkung besser belegt ist',
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'giving.helenkellerintl.org',
		// Dossiers (§3.4)
		'Dossiers',
		"This session's question",
		'Bereich Zukunft: Ist Kindergesundheit (Helen Keller) oder Bildung (Pratham/TaRL) besser belegt?', // plain.question (German, marked)
		'The question verbatim ▸',
		'<blockquote',
		"The Scout's search queries ▸",
		'/en/council/', // Tür zu The Council (EN)
		'/en/archive/', // Tür zu The Archive (EN)
		'Original protocol in German.', // Rekord-Vermerk bei der aktuellen Frage
		'lang="de"', // Rekordtext maschinell als deutsch markiert
		// Das Board trägt die Antwort — pragerendert, ohne JS im HTML.
		"The last session's answer",
		'3 of 3',
		// Tür-Hotspot im Raumbild — pragerenderter Link, trägt ohne JS.
		// (Klasse trägt im Build den Svelte-Scope-Hash: class="door-hotspot svelte-…")
		'door-hotspot',
		'aria-label="Through the grand door: The Council"'
	]);
	// Die publizierte Frage steht unverändert (deutsch) im EN-Dokument.
	assert.ok(
		html.includes('Auflösung des Säule-A-Dissens'),
		'deutsche Rekordfrage fehlt im EN-Raum'
	);
	assert.ok(
		!html.includes('Plain-language version pending'),
		'pending note still visible although the plain layer is published'
	);
	assert.match(html, />Study<\/p>/, 'room word "Study" missing (EN)');
	assert.ok(!html.includes('How it works'), 'removed process rail still visible');
	assert.ok(!html.includes('The Scout and The Warden'), 'Doppelblock Akteure noch sichtbar');
	assert.ok(!html.includes('Show the research trail'), 'alte Ausklapp-Grammatik noch sichtbar');
	assert.ok(!html.includes('What this session was about'), 'alter Fachtext-Titel noch sichtbar');
});

test('The Council (/en/council/) zeigt englische Chrome, deutsche Vorbehalte mit Vermerk', (context) => {
	const html = readBuilt(PAGES.councilEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Council (EN)', [
		// Stable head — identical on all three room pages (title reorder)
		'Where does my donation help the most?', // h1 — the core question everywhere
		'One AI model each from different families reviews the same evidence', // pitch
		'Why so elaborate? ▸', // inline toggle in the head
		'Voted separately, then counted publicly.', // room lead
		'Three answers', // tube bead (name)
		// "How the votes were counted" — one block instead of three (§4.2)
		'How the votes were counted',
		'The program only counts matching mentions.',
		'Helen Keller International',
		'Against Malaria Foundation',
		'Nuclear Threat Initiative',
		'Lead Exposure Elimination Project',
		'3 of 3', // Zählung Konsens (Trennwort aus der Locale)
		'2 of 3',
		'>TaRL Africa</del>', // revision inside the mark (Svelte scope hash on <del>)
		'Reservation ▸', // reservation toggle in the row
		'All votes, verbatim ▸', // full matrix at the end of the block
		'Original protocol in German.', // Rekord-Vermerk beim Vorbehalt
		'First ', // Erstvotum
		'Final ', // Schlussvotum
		'NobleCause does not handle money' // Geldfluss-Hinweis
	]);
	assert.match(html, />Council<\/p>/, 'room word "Council" missing (EN)');
	assert.ok(!html.includes('How three models decide'), 'old dynamic h1 still visible');
	// Organisationsbeschreibungen (und ihr orgEn-Fallback) haben im entrümpelten
	// Council keine Anzeigefläche mehr — der Mechanismus lebt in
	// RecommendationCard.svelte weiter (derzeit unreferenziert).
});

test('The Archive (/en/archive/) zeigt englische Chrome — Rekord bleibt deutsch mit Vermerk', (context) => {
	const html = readBuilt(PAGES.archiveEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	requireAll(html, 'The Archive (EN)', [
		// Stable head — identical on all three room pages (title reorder)
		'Where does my donation help the most?',
		'One AI model each from different families reviews the same evidence',
		'Why so elaborate? ▸',
		'Every session, complete and unchanged — recommendations, disagreement, costs.', // room lead
		'Session archive',
		'Session 1 · 2026-07-07',
		'Malaria Consortium', // Ergebnis-Chip (registry-aufgelöst)
		'no agreement', // offener Bereich als Chip-Markierung
		'No agreement yet',
		"The council's wording ▸",
		'Correction notice',
		'Cost of this session',
		'/sessions/2026-07c/',
		'Original protocol in German.', // Rekord-Vermerk (Korrektur/Dissens)
		'The full protocol is published in German.', // Hinweis am Protokoll-Link
		'lang="de"', // Rekordtexte maschinell als deutsch markiert
		'Korrektur vom 14.07.2026' // publizierter Rekord: unverändert deutsch
	]);
	assert.match(html, />Archive<\/p>/, 'room word "Archive" missing (EN)');
});

test('Ausklapp-Disziplin: maximal eine Tiefe, jede Summary benennt den Inhalt mit ▸', (context) => {
	// §2 der Raum-Content-Regeln: nie ein <details> im <details>; jede
	// <summary> benennt im Meta-Register, was innen liegt, mit ▸ am Ende.
	// Der externe Protokoll-Link ist Navigation, kein Ausklapp.
	for (const [room, rel] of Object.entries(PAGES)) {
		const html = readBuilt(rel);
		if (html === null) return context.skip('zuerst npm run build ausführen');
		// Tiefe: ein simpler Stack über die details-Tags.
		let depth = 0;
		for (const match of html.matchAll(/<\/?details[\s>]/g)) {
			depth += match[0].startsWith('</') ? -1 : 1;
			assert.ok(depth <= 1, `${room}: verschachteltes <details> (Tiefe > 1)`);
			assert.ok(depth >= 0, `${room}: unausgeglichene <details>-Tags`);
		}
		assert.equal(depth, 0, `${room}: ungeschlossenes <details>`);
		// Grammatik: jede Summary endet auf ▸ ( nach dem Trimmen von Tags/Whitespace).
		const summaries = [...html.matchAll(/<summary[^>]*>([\s\S]*?)<\/summary>/g)].map((m) =>
			m[1].replace(/<[^>]+>/g, '').trim()
		);
		assert.ok(summaries.length > 0, `${room}: kein Ausklapp gefunden (Testläufer-Check)`);
		for (const text of summaries) {
			assert.ok(text.endsWith('▸'), `${room}: Summary ohne ▸ am Ende: „${text}"`);
		}
	}
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
		'pillars/pillar-future-display.avif',
		'pillars/pillar-relieve-suffering-display.avif',
		'pillars/pillar-major-risks-display.avif',
		'pillars/pillar-overlooked-display.avif',
		'process/process-question-display.avif',
		'process/process-evidence-display.avif',
		'process/process-three-answers-display.webp',
		'process/process-reconsider-display.avif',
		'process/process-count-display.avif',
		'process/process-publish-display.avif',
		'doors/door-study-archive-display.avif',
		'doors/door-council-archive-display.avif',
		'scenes/antechamber-display.avif',
		'scenes/antechamber-portrait-display.avif',
		'scenes/antechamber-portrait-800.avif',
		'scenes/hall-display.avif',
		'scenes/archive-display.avif',
		'scenes/archive-portrait-display.avif',
		'scenes/archive-portrait-800.avif',
		'scenes/archive-door-open-display.avif',
		'actors/pult-lamp.avif'
	];
	for (const asset of assets) {
		assert.ok(html.includes(`/media/${asset}`), `kein Raum referenziert ${asset}`);
		assert.ok(fs.existsSync(path.join(SITE, 'build', 'media', asset)), `Deploy fehlt ${asset}`);
	}
});

test('Bühne: Röhren-Füllstand steht in jedem Raum (DE+EN) korrekt im pragerenderten HTML', (context) => {
	// Der Füllstand ist Raum-Eigenschaft und No-JS-Wahrheit: Study 2 gefüllt,
	// Council 5, Archive 6 — blass der Rest, genau eine aktive Perle.
	const cases = {
		study: [2, 4, 'Schritt 2 von 6 erreicht', 'Verfahrensstand'],
		council: [5, 1, 'Schritt 5 von 6 erreicht', 'Verfahrensstand'],
		archive: [6, 0, 'Schritt 6 von 6 erreicht', 'Verfahrensstand'],
		studyEn: [2, 4, 'Step 2 of 6 reached', 'Process state'],
		councilEn: [5, 1, 'Step 5 of 6 reached', 'Process state'],
		archiveEn: [6, 0, 'Step 6 of 6 reached', 'Process state']
	};
	for (const [room, [filled, blass, status, label]] of Object.entries(cases)) {
		const html = readBuilt(PAGES[room]);
		if (html === null) return context.skip('zuerst npm run build ausführen');
		assert.equal(
			(html.match(/tube-bead filled/g) ?? []).length,
			filled,
			`${room}: erwartet ${filled} gefüllte Perlen`
		);
		assert.equal(
			(html.match(/tube-bead blass/g) ?? []).length,
			blass,
			`${room}: erwartet ${blass} blasse Perlen`
		);
		assert.equal(
			(html.match(/tube-bead filled active/g) ?? []).length,
			1,
			`${room}: erwartet genau eine aktive Perle`
		);
		assert.ok(html.includes(status), `${room}: sr-Status „${status}" fehlt`);
		assert.ok(html.includes(`aria-label="${label}"`), `${room}: Röhren-Label fehlt`);
		// Erklärsätze AN den Kugeln (Titelbereich-Neuordnung): alle sechs im DOM
		// (No-JS-Wahrheit, SR liest sie), sichtbar bei Hover — aber KEIN Tab-Stopp:
		// die Kugel ist nicht bedienbar, ein Fokusstopp ohne Bedienbarkeit verstösst
		// gegen die StageTube-Regel (a11y-Fix 2026-07, keine lose Caption mehr).
		assert.equal(
			(html.match(/<li class="tube-bead[^"]*"[^>]*tabindex/g) ?? []).length,
			0,
			`${room}: Röhren-Kugeln dürfen keinen Tab-Stopp tragen`
		);
		assert.equal(
			(html.match(/class="bead-text/g) ?? []).length,
			6,
			`${room}: erwartet 6 Erklärtexte an den Kugeln`
		);
		// Zeitschicht-Zeile unter der Röhre: Study + Council tragen sie (Rhythmus +
		// letzter Lauf / Sitzungstermin), das Archiv nicht (keine Zukunft).
		const wantsCaption = /^(study|council)/.test(room);
		assert.equal(
			html.includes('tube-caption'),
			wantsCaption,
			`${room}: Zeitschicht-Röhrenzeile ${wantsCaption ? 'fehlt' : 'gehört nicht in diesen Raum'}`
		);
	}
});

test('Bühne: Dokument komplett ohne JS — Stage-Klassen nur per Script, genau eine Tafel je Route', (context) => {
	// §0: Das statische HTML trägt keinen Stage-Zustand im <html>-Tag (die
	// Klassen setzt ausschließlich das Boot-Script per classList) und jede Route
	// enthält genau EINE semantische ResultBoard-Instanz — auch das Archiv.
	const boardTitle = {
		study: 'Die Antwort der letzten Sitzung',
		council: 'Die Antwort der letzten Sitzung',
		archive: 'Die Antwort der letzten Sitzung',
		studyEn: "The last session's answer",
		councilEn: "The last session's answer",
		archiveEn: "The last session's answer"
	};
	for (const [room, rel] of Object.entries(PAGES)) {
		const html = readBuilt(rel);
		if (html === null) return context.skip('zuerst npm run build ausführen');
		const htmlTag = html.match(/<html[^>]*>/)?.[0] ?? '';
		assert.ok(!htmlTag.includes('stage-armed'), `${room}: stage-armed im statischen <html>-Tag`);
		assert.equal(
			(html.match(/class="result-board/g) ?? []).length,
			1,
			`${room}: erwartet genau eine ResultBoard-Instanz`
		);
		assert.equal(
			(html.match(/id="antwort"/g) ?? []).length,
			1,
			`${room}: erwartet genau einen Tafel-Anker`
		);
		assert.ok(html.includes(boardTitle[room]), `${room}: Tafel-Titel fehlt`);
	}
});

test('Bühne: zweite Ebene — Akteure und Wolkenzug stehen im pragerenderten HTML (DE+EN)', (context) => {
	// No-JS-Wahrheit: die zweite Ebene der Study (beide Akteure, Wolkenzug) ist
	// Teil des statischen Dokuments — Endzustand sichtbar, kein Tab-Stopp auf
	// nicht-interaktiven Figuren, Assets im Deploy. Council/Archive tragen den
	// Study-spezifischen Slot nicht.
	const studyHtml = readBuilt(PAGES.study);
	const studyEnHtml = readBuilt(PAGES.studyEn);
	if (studyHtml === null || studyEnHtml === null) {
		return context.skip('zuerst npm run build ausführen');
	}
	for (const [html, room] of [
		[studyHtml, 'study'],
		[studyEnHtml, 'studyEn']
	]) {
		assert.ok(html.includes('/media/actors/scout.avif'), `${room}: Scout-Cutout fehlt`);
		assert.ok(html.includes('/media/actors/warden.avif'), `${room}: Warden-Cutout fehlt`);
		assert.ok(html.includes('/media/ambient/clouds-study.avif'), `${room}: Wolkenzug fehlt`);
		assert.ok(
			!/class="actor[^"]*"[^>]*tabindex/.test(html),
			`${room}: Akteur-Figur trägt tabindex (nicht-interaktiv = kein Tab-Stopp)`
		);
	}
	// Name + Sitz (Modell aus den DATEN, keine Copy) + Satz je Sprache; die
	// Bereichs-Emblemreihe trägt die vier Bereiche (alt=label, nicht dekorativ).
	// Gloss ist entfallen.
	assert.ok(studyHtml.includes('The Scout'), 'study: Scout-Name fehlt (DE)');
	assert.ok(studyHtml.includes('Aktuell: claude-fable-5'), 'study: Sitz (Modell aus Daten) fehlt (DE)');
	assert.ok(
		studyHtml.includes('sucht die wirksamsten Organisationen'),
		'study: Scout-Satz fehlt (DE)'
	);
	assert.ok(studyHtml.includes('alt="Zukunft"'), 'study: Bereichs-Emblemreihe (alt=label) fehlt');
	assert.ok(!studyHtml.includes('der Späher'), 'study: Gloss nicht mehr entfernt');
	// Warden-Entscheid + „letzte Prüfung" aus den Daten — zugleich Beleg, dass
	// master hereingezogen ist (20. Juli 2026, nicht 8. Juli).
	assert.ok(studyHtml.includes('20. Juli 2026'), 'study: lastResearch-Datum (master-Zug) fehlt');
	assert.ok(studyEnHtml.includes('The Scout'), 'studyEn: Scout-Name fehlt (EN)');
	assert.ok(
		studyEnHtml.includes('seeks the most effective organisations'),
		'studyEn: Scout-Satz fehlt (EN)'
	);
	assert.ok(!studyEnHtml.includes('der Späher'), 'studyEn: deutscher Gloss darf EN nicht erscheinen');
	// Scout/Warden gehören nur in die Study; das Council trägt Lesepulte, das
	// Archiv trägt Karteikästen (register) — je eigener Test unten. Kein Raum
	// trägt die Cutouts eines anderen.
	const archiveHtml = readBuilt(PAGES.archive);
	if (archiveHtml === null) return context.skip('zuerst npm run build ausführen');
	assert.ok(
		!archiveHtml.includes('/media/actors/lectern.avif'),
		'archive: Lesepult gehört ins Council, nicht ins Archiv'
	);
	for (const room of ['council', 'archive']) {
		const html = readBuilt(PAGES[room]);
		assert.ok(!html.includes('/media/actors/scout.avif'), `${room}: Scout gehört nicht in diesen Raum`);
		assert.ok(!html.includes('/media/actors/warden.avif'), `${room}: Warden gehört nicht in diesen Raum`);
	}
	for (const asset of ['actors/scout.avif', 'actors/warden.avif', 'ambient/clouds-study.avif']) {
		assert.ok(fs.existsSync(path.join(SITE, 'build', 'media', asset)), `Deploy fehlt: ${asset}`);
	}
});

test('Bühne: zweite Ebene Council — N Lesepulte stehen im pragerenderten HTML (DE+EN)', (context) => {
	// No-JS-Wahrheit wie in der Study: die Lesepulte sind Teil des statischen
	// Dokuments — generisch N aus modelTracks (derzeit drei publizierte
	// Teilnehmer, vgl. die „3 von 3"-Erwartungen), kein Tab-Stopp auf den
	// Figuren, alle neuen Saal-Assets im Deploy.
	const councilHtml = readBuilt(PAGES.council);
	const councilEnHtml = readBuilt(PAGES.councilEn);
	if (councilHtml === null || councilEnHtml === null) {
		return context.skip('zuerst npm run build ausführen');
	}
	for (const [html, room] of [
		[councilHtml, 'council'],
		[councilEnHtml, 'councilEn']
	]) {
		assert.ok(html.includes('/media/actors/lectern.avif'), `${room}: Lesepult-Cutout fehlt`);
		assert.equal(
			(html.match(/class="rail pult/g) ?? []).length,
			3,
			`${room}: erwartet ein Pult je Teilnehmer (modelTracks)`
		);
		assert.ok(
			!/class="pult-figure[^"]*"[^>]*tabindex/.test(html),
			`${room}: Pult-Figur trägt tabindex (nicht-interaktiv = kein Tab-Stopp)`
		);
	}
	// Beschriftung aus den Daten (label + Anzeigename der Familie), Rolle aus i18n.
	for (const alt of [
		'Claude Opus (Anthropic): antwortet getrennt',
		'GPT (OpenAI): antwortet getrennt',
		'Gemini Pro (Google): antwortet getrennt'
	]) {
		assert.ok(councilHtml.includes(alt), `council: Pult-Beschriftung fehlt: ${alt}`);
	}
	assert.ok(
		councilEnHtml.includes('answers separately — every vote public.'),
		'councilEn: Pult-Rolle fehlt (EN)'
	);
	assert.ok(
		!councilEnHtml.includes('antwortet getrennt'),
		'councilEn: deutsche Rolle darf EN nicht erscheinen'
	);
	// Tür-Hotspot: die gemalte Saal-Tür führt weiter ins Archiv (Rundgang).
	assert.ok(councilHtml.includes('class="door-hotspot'), 'council: Tür-Hotspot fehlt');
	assert.ok(
		councilHtml.includes('aria-label="Die schlichte Tür: The Archive"'),
		'council: Tür-Hotspot-Ziel/aria (Die schlichte Tür: The Archive) fehlt'
	);
	assert.ok(
		councilEnHtml.includes('aria-label="The plain door: The Archive"'),
		'councilEn: Tür-Hotspot-Ziel/aria (The plain door: The Archive) fehlt'
	);
	for (const asset of [
		'actors/lectern.avif',
		'scenes/hall-portrait-display.avif',
		'scenes/hall-portrait-800.avif',
		'scenes/hall-door-open-display.avif'
	]) {
		assert.ok(fs.existsSync(path.join(SITE, 'build', 'media', asset)), `Deploy fehlt: ${asset}`);
	}
});

test('Bühne: zweite Ebene Archiv — Pult mit Leuchte + Tür-Hotspot (DE+EN)', (context) => {
	// No-JS-Wahrheit: das Möbel ist Teil des statischen Dokuments — REINE KULISSE
	// (keine Datenbindung, generisches alt), kein Tab-Stopp auf der Figur. Runde B §2:
	// nur EIN Möbel (das Pult mit Leuchte, rechts) — das Regal ist ersatzlos entfallen,
	// die linke Flanke bleibt leer. Der Tür-Hotspot führt zurück in die Study.
	const archiveHtml = readBuilt(PAGES.archive);
	const archiveEnHtml = readBuilt(PAGES.archiveEn);
	if (archiveHtml === null || archiveEnHtml === null) {
		return context.skip('zuerst npm run build ausführen');
	}
	for (const [html, room] of [
		[archiveHtml, 'archive'],
		[archiveEnHtml, 'archiveEn']
	]) {
		assert.ok(html.includes('/media/actors/pult-lamp.avif'), `${room}: Pult-Cutout fehlt`);
		assert.equal(
			(html.match(/class="rail pult-desk/g) ?? []).length,
			1,
			`${room}: erwartet genau EIN Pult mit Leuchte`
		);
		assert.ok(
			!html.includes('/media/actors/register.avif'),
			`${room}: Regal (register) ist ersatzlos entfallen (Runde B §2)`
		);
		assert.ok(
			!/class="reg-figure[^"]*"[^>]*tabindex/.test(html),
			`${room}: Möbel-Figur trägt tabindex (nicht-interaktiv = kein Tab-Stopp)`
		);
		assert.ok(html.includes('class="door-hotspot'), `${room}: Tür-Hotspot fehlt`);
	}
	// Alt-Text generisch (kein Datenbezug) — DE/EN gespiegelt.
	assert.ok(
		archiveHtml.includes('Archivpult mit Leseleuchte'),
		'archive: generisches Pult-alt fehlt'
	);
	assert.ok(
		archiveEnHtml.includes('Archive desk with a reading lamp'),
		'archiveEn: generisches Pult-alt fehlt (EN)'
	);
	// Der Tür-Hotspot führt zurück in die Study (Rundgang schließt sich).
	assert.ok(
		archiveHtml.includes('aria-label="Zurück: The Study"'),
		'archive: Tür-Hotspot-Ziel/aria (Zurück: The Study) fehlt'
	);
	assert.ok(
		archiveEnHtml.includes('aria-label="Back: The Study"'),
		'archiveEn: Tür-Hotspot-Ziel/aria (Back: The Study) fehlt'
	);
});

test('Zeitschicht: schedule.last_journal zeigt auf einen Research-Lauf (search_queries > 0)', () => {
	// Datenvertrag (Steward-Auflage): lastResearch wird über schedule.last_journal
	// aufgelöst, NICHT über das neueste Journal-Datum (das wäre der Klartext-
	// Bootstrap 2026-07-24, kein Research-Lauf). Strukturelles Signal ist
	// search_queries — kein Parsen von Prosa. Zeigt der Zeiger auf einen Nicht-
	// Research-Eintrag, muss der Build laut scheitern (Guard in (rooms)/+layout.server.js).
	const ROOT = path.resolve(SITE, '..');
	const schedule = JSON.parse(fs.readFileSync(path.join(ROOT, 'schedule.json'), 'utf8'));
	const id = schedule.last_journal.replace(/^\/?journal\//, '').replace(/\/$/, '');
	const entry = JSON.parse(fs.readFileSync(path.join(ROOT, 'journal', id, 'entry.json'), 'utf8'));
	assert.ok(
		(entry.search_queries?.length ?? 0) > 0,
		`schedule.last_journal (${id}) ist kein Research-Lauf (keine search_queries)`
	);
});
