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

// --- Datenvertrag: datenabhängige Erwartungen aus der AKTUELLEN Sitzung ableiten,
// nicht auf eine bestimmte Sitzung hart kodieren. Quelle der Wahrheit ist dieselbe
// deterministische Nummernwahl wie in content.js (getLatestSession) plus die
// Registry und der über schedule.last_journal aufgelöste Research-Lauf. So bleibt
// die Datei bei einem legitimen nächsten Sitzungsrekord grün. Stabile UI-/
// Sicherheitsverträge bleiben separat hart geprüft. */
const ROOT = path.resolve(SITE, '..');
const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

const currentData = () => {
	const dir = path.join(ROOT, 'sessions');
	const sessions = fs
		.readdirSync(dir, { withFileTypes: true })
		.filter((e) => e.isDirectory())
		.map((e) => readJson(path.join(dir, e.name, 'session.json')))
		.sort((a, b) => (b.number ?? 0) - (a.number ?? 0) || (a.date < b.date ? 1 : -1));
	const session = sessions[0];
	const registry = readJson(path.join(ROOT, 'organizations.json'));
	const orgById = new Map((registry.organizations ?? []).map((o) => [o.id, o]));
	const FAMILY = { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' };
	const nameOf = (rec) => orgById.get(rec.organization_id)?.canonical_name ?? rec.organization;
	const consensus = (session.recommendations ?? []).filter((r) => r.has_consensus);
	const round = (k) => (session.rounds ?? []).find((r) => r.kind === k);
	const initial = new Map((round('initial_vote')?.votes ?? []).map((v) => [v.model, v]));
	const final = new Map((round('final_vote')?.votes ?? []).map((v) => [v.model, v]));
	const revisions = [];
	for (const p of session.participants ?? []) {
		const iv = initial.get(p.model);
		const fv = final.get(p.model);
		for (const pillar of ['A', 'B', 'C', 'D']) {
			const a = (iv?.recommendations ?? []).find((x) => x.pillar === pillar);
			const b = (fv?.recommendations ?? []).find((x) => x.pillar === pillar);
			if (a && b && a.organization_id !== b.organization_id) {
				revisions.push({ model: p.label, fromName: nameOf(a), toName: nameOf(b) });
			}
		}
	}
	const schedule = readJson(path.join(ROOT, 'schedule.json'));
	const lastId = (schedule.last_journal ?? '').replace(/^\/?journal\//, '').replace(/\/$/, '');
	const lastResearch = lastId ? readJson(path.join(ROOT, 'journal', lastId, 'entry.json')) : null;
	return {
		session,
		nameOf,
		orgById,
		FAMILY,
		consensus,
		revisions,
		lastResearch,
		plain: session.plain ?? null,
		dossier: session.wart_dossier ?? null,
		dossierRefusal: session.wart_dossier_refusal ?? null,
		participants: session.participants ?? []
	};
};
const DATA = currentData();
// Zählstände der Konsens-Bereiche als „N von M" (DE) bzw. „N of M" (EN).
const tally = (of) => [...new Set(DATA.consensus.map((r) => `${r.convergence.count} ${of} ${r.convergence.total}`))];
// Organisationsnamen + direkte Spendenlinks der Konsens-Empfehlungen (Registry).
const consensusOrgNames = DATA.consensus.map((r) => DATA.nameOf(r));
const consensusDonations = [
	...new Set(DATA.consensus.map((r) => DATA.orgById.get(r.organization_id)?.donation_url).filter(Boolean))
];

test('The Study (/) trägt Einstieg, Mechanismus, Legenden, Akteure und Belege', (context) => {
	const html = readBuilt(PAGES.study);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	// Stabiler, sitzungsunabhängiger Kopf + Mechanismus (harte UI-Verträge).
	requireAll(html, 'The Study', [
		'Wo hilft meine Spende am meisten?', // h1 / Leitfrage
		'Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu.', // Raum-Lead
		'Je ein KI-Modell verschiedener Familien prüft dieselben Belege', // Pitch (ohne Familiennamen/Zahl)
		'Warum so umständlich? ▸', // Verfahrens-Ausklapp im stabilen Kopf
		'Ein einzelnes Modell kann irren oder eine blinde Stelle haben.',
		// Prozess-Röhre: alle sechs kanonischen Schritte mit Name + Klartext-Satz
		'Die Frage',
		'Die Belege',
		'Drei Antworten',
		'Umdenken',
		'Zählen',
		'Veröffentlichen',
		'Eine Frage pro Sitzung — vier Bereiche, je eine Empfehlung.',
		'Der Späher sammelt Studien, Kosten-Wirksamkeit und Finanzierungslücken.',
		'Drei Modelle antworten getrennt — jedes Votum öffentlich.',
		'Ein einfaches Programm zählt nur die Nennungen.',
		'Der Wart veröffentlicht alles — Empfehlungen, Uneinigkeit, Kosten.',
		'Die Empfehlungen dieser Sitzung', // answerTitle
		// Dossiers (§3.4): Kennzeichnungs-Ausklapp + Wortlaut-Beleg (stabil).
		'Dossiers',
		'Die Frage dieser Sitzung', // questionTitle (questionText liegt immer vor)
		'Die Frage im Wortlaut ▸',
		'<blockquote',
		'/ratssaal/', // Tür zu The Council
		'/archiv/', // Tür zu The Archive
		'Die Antwort der letzten Sitzung', // Board
		'door-hotspot',
		'aria-label="Durch die große Tür: The Council"'
	]);
	// Datenabhängig aus der aktuellen Sitzung: Konsens-Organisationen (Registry),
	// ihre Zählstände und mindestens ein direkter Spendenlink.
	for (const name of consensusOrgNames) {
		assert.ok(html.includes(name), `The Study fehlt Konsens-Org: ${name}`);
	}
	for (const t of tally('von')) {
		assert.ok(html.includes(t), `The Study fehlt Zählstand: ${t}`);
	}
	assert.ok(
		consensusDonations.length === 0 || consensusDonations.some((url) => html.includes(url)),
		'The Study fehlt ein registry-aufgelöster Spendenlink'
	);
	// Klartext-Schicht (§3.3): liegt session.plain vor, tragen die Zeilen die
	// publizierte Fassung WORTGLEICH und der Vermerk entfällt; sonst steht der
	// publizierende Fallback „Klartext folgt" mit unverändertem Rekordinhalt.
	if (DATA.plain?.recommendations) {
		assert.ok(!html.includes('Klartext folgt'), 'Vermerk trotz publizierter Klartext-Schicht sichtbar');
		for (const line of Object.values(DATA.plain.recommendations)) {
			assert.ok(html.includes(line), `The Study fehlt Klartext-Zeile: ${line}`);
		}
	} else {
		assert.ok(html.includes('Klartext folgt'), 'Klartext-Fallback fehlt trotz fehlender plain-Schicht');
	}
	// Frage-Kontext: plain.question, sonst der kuratierte Protokoll-Kontext (summary).
	const questionText = DATA.plain?.question ?? DATA.session.summary ?? '';
	assert.ok(
		questionText.length === 0 || html.includes(questionText.slice(0, 48)),
		'The Study fehlt Frage-Kontext (plain.question bzw. summary)'
	);
	// Research-Ausklapp NUR, wenn die aktuelle Sitzung ein Dossier mit Suchanfragen
	// bereitstellt. Bei wart_dossier_refusal keine erfundenen Scout-Suchanfragen.
	if (DATA.dossier?.search_queries?.length) {
		assert.ok(html.includes('Suchanfragen des Spähers ▸'), 'Scout-Suchanfragen-Ausklapp fehlt');
		assert.ok(html.includes(DATA.dossier.search_queries[0]), 'erste Scout-Suchanfrage fehlt');
		assert.ok(html.includes('#wart-dossier'), 'Dossier-Verweis fehlt');
	} else {
		assert.ok(!html.includes('Suchanfragen des Spähers'), 'Scout-Suchanfragen trotz fehlendem Dossier');
	}
	if (DATA.dossierRefusal) {
		requireAll(html, 'The Study Dossier-Verweigerung', [
			'Wart-Dossier nicht erstellt',
			'Es wurde kein Ersatzdossier erzeugt',
			'#wart-dossier-refusal'
		]);
	}
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
	// Keine Doppel-Komposition der Klartext-Zeile (das „Klartext folgt" gegen die
	// plain-Schicht prüft bereits der datenabhängige Zweig oben).
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

test('Aktuelle Sitzungsseite kennzeichnet eine Wart-Dossier-Verweigerung', (context) => {
	const html = readBuilt(`sitzungen/${DATA.session.id}/index.html`);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	if (DATA.dossierRefusal) {
		requireAll(html, 'Sitzungsseite Dossier-Verweigerung', [
			'id="wart-dossier-refusal"',
			'Wart-Dossier nicht erstellt',
			'Es wurde kein Ersatzdossier',
			DATA.dossierRefusal.raw_artifact
		]);
	} else {
		assert.ok(!html.includes('id="wart-dossier-refusal"'), 'Verweigerungsmarke ohne Rekordfeld');
	}
});

test('The Council (/ratssaal/) trägt Zählwerk, Voten, Revisionen in der Marke, Spendenlinks', (context) => {
	const html = readBuilt(PAGES.council);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	// Stabiler Kopf + Zähl-Block-Gerüst (sitzungsunabhängig).
	requireAll(html, 'The Council', [
		'Wo hilft meine Spende am meisten?', // h1 — die Leitfrage überall
		'Je ein KI-Modell verschiedener Familien prüft dieselben Belege', // Pitch
		'Warum so umständlich? ▸', // inline-Ausklapp im Kopf
		'Getrennt abgestimmt, dann öffentlich gezählt. Was mehrfach genannt wird, wird Empfehlung.', // Raum-Lead
		'Drei Antworten', // Röhren-Kugel (Name)
		'Wie gezählt wurde', // §4.2 ein Block statt drei
		'Das Programm zählt nur gleiche Nennungen.',
		'Alle Voten im Wortlaut ▸', // volle Matrix am Blockende
		'Erst ', // Erstvotum (ModelPulpits)
		'Schluss ', // Schlussvotum
		'NobleCause nimmt kein Geld an.' // Geldfluss-Hinweis
	]);
	// Datenabhängig: Konsens-Orgs, Zählstände, Modell-Marken (labels), Spendenlink.
	for (const name of consensusOrgNames) {
		assert.ok(html.includes(name), `The Council fehlt Konsens-Org: ${name}`);
	}
	for (const t of tally('von')) {
		assert.ok(html.includes(t), `The Council fehlt Zählstand: ${t}`);
	}
	for (const p of DATA.participants) {
		assert.ok(html.includes(p.label), `The Council fehlt Modell-Marke: ${p.label}`);
	}
	assert.ok(
		consensusDonations.length === 0 || consensusDonations.some((url) => html.includes(url)),
		'The Council fehlt ein registry-aufgelöster Spendenlink'
	);
	// Revisionen leben in der Marke (Erstvotum durchgestrichen): NUR wenn die
	// aktuelle Sitzung eine Organisationsänderung zwischen Erst- und Schlussvotum
	// trägt. Gibt es keine, darf auch kein <del>-Erstvotum erscheinen.
	if (DATA.revisions.length) {
		assert.ok(html.includes('Vorbehalt ▸') || html.includes('changedMark'), 'Council: Revisionsmarke fehlt');
		for (const rev of DATA.revisions) {
			assert.ok(html.includes(`>${rev.fromName}</del>`), `Council fehlt Revision-Erstvotum: ${rev.fromName}`);
		}
	} else {
		assert.ok(!/<del>[^<]/.test(html.split('all-votes')[0] ?? html), 'Council: <del>-Revision ohne Datenbasis');
	}
	// Vorbehalt-Ausklapp: nur wenn ein Konsens-Bereich bedingte Voten trägt.
	if (DATA.consensus.some((r) => (r.convergence?.conditional_count ?? 0) > 0)) {
		assert.ok(html.includes('Vorbehalt ▸'), 'Council: Vorbehalt-Ausklapp fehlt trotz bedingter Voten');
	}
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
		'Dissens und Vorbehalte', // Archiv-Dissens-Überschrift (P5: benennt den Abschnitt, behauptet keinen Rekordstand)
		'Wortlaut des Rates ▸', // aufklappbarer Dissens (gerendert, nicht roh)
		'Nachträge zum Rekord', // neutrale Überschrift (behauptet keine Korrektur; hält Korrektur + Einordnung)
		'Kosten dieser Sitzung',
		'/sitzungen/2026-07c/' // Link zum vollständigen Protokoll
	]);
	assert.match(html, />Archive<\/p>/, 'Raumwort „Archive" fehlt');
	assert.ok(!html.includes('The Archive · das Archiv'), 'alte Eyebrow noch sichtbar');
	assert.ok(!html.includes('Empfehlungen in allen Bereichen'), 'alte Zeilen-Zusammenfassung noch sichtbar');
});

test('The Study (/en/) zeigt englische Chrome — Rekordfrage bleibt deutsch mit Vermerk', (context) => {
	const html = readBuilt(PAGES.studyEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	// Stable English chrome + process (session-independent).
	requireAll(html, 'The Study (EN)', [
		'Where does my donation help the most?',
		'Every session begins here — with a question and the evidence for it.', // room lead
		'One AI model each from different families reviews the same evidence', // pitch (no names/count)
		'Why so elaborate? ▸', // process toggle in the plaque
		'A single model can be wrong or have a blind spot.',
		'Three AI models review the same evidence', // head description
		'The question', 'The evidence', 'Three answers', 'Second thoughts', 'The count', 'Publication',
		'The Scout gathers studies, cost-effectiveness and funding gaps.',
		'Three models answer separately — every vote public.',
		'The Warden publishes everything — recommendations, disagreement, costs.',
		"This session's recommendations",
		'Dossiers',
		"This session's question",
		'The question verbatim ▸',
		'<blockquote',
		'/en/council/', // Tür zu The Council (EN)
		'/en/archive/', // Tür zu The Archive (EN)
		'Original protocol in German.', // Rekord-Vermerk bei der aktuellen Frage
		'lang="de"', // Rekordtext maschinell als deutsch markiert
		"The last session's answer", // Board
		'door-hotspot',
		'aria-label="Through the grand door: The Council"'
	]);
	// Data-derived: consensus orgs, tallies (EN word), donation link.
	for (const name of consensusOrgNames) {
		assert.ok(html.includes(name), `The Study (EN) fehlt Konsens-Org: ${name}`);
	}
	for (const t of tally('of')) {
		assert.ok(html.includes(t), `The Study (EN) fehlt Zählstand: ${t}`);
	}
	assert.ok(
		consensusDonations.length === 0 || consensusDonations.some((url) => html.includes(url)),
		'The Study (EN) fehlt ein registry-aufgelöster Spendenlink'
	);
	// Die publizierte Frage steht unverändert (deutsch) im EN-Dokument — der
	// tatsächliche Wortlaut der aktuellen Sitzung, nicht ein fester String.
	assert.ok(
		html.includes(DATA.session.question.slice(0, 48)),
		'deutsche Rekordfrage der aktuellen Sitzung fehlt im EN-Raum'
	);
	// Klartext-Schicht: liegt session.plain vor, kein pending-Vermerk und die
	// (deutschen, markierten) plain-Zeilen; sonst der publizierende Fallback.
	if (DATA.plain?.recommendations) {
		assert.ok(!html.includes('Plain-language version pending'), 'pending note despite published plain layer');
		for (const line of Object.values(DATA.plain.recommendations)) {
			assert.ok(html.includes(line), `The Study (EN) fehlt Klartext-Zeile: ${line}`);
		}
	} else {
		assert.ok(html.includes('Plain-language version pending'), 'EN plain fallback missing');
	}
	// Research-Ausklapp nur bei vorhandenem Dossier mit Suchanfragen.
	if (DATA.dossier?.search_queries?.length) {
		assert.ok(html.includes("The Scout's search queries ▸"), "Scout's search queries toggle missing");
	} else {
		assert.ok(!html.includes("The Scout's search queries"), 'Scout search queries without dossier data');
	}
	if (DATA.dossierRefusal) {
		requireAll(html, 'The Study EN dossier refusal', [
			'Warden dossier not produced',
			'No substitute dossier was generated',
			'#wart-dossier-refusal'
		]);
	}
	assert.match(html, />Study<\/p>/, 'room word "Study" missing (EN)');
	assert.ok(!html.includes('How it works'), 'removed process rail still visible');
	assert.ok(!html.includes('The Scout and The Warden'), 'Doppelblock Akteure noch sichtbar');
	assert.ok(!html.includes('Show the research trail'), 'alte Ausklapp-Grammatik noch sichtbar');
	assert.ok(!html.includes('What this session was about'), 'alter Fachtext-Titel noch sichtbar');
});

test('The Council (/en/council/) zeigt englische Chrome, deutsche Vorbehalte mit Vermerk', (context) => {
	const html = readBuilt(PAGES.councilEn);
	if (html === null) return context.skip('zuerst npm run build ausführen');
	// Stable head + block scaffold (session-independent).
	requireAll(html, 'The Council (EN)', [
		'Where does my donation help the most?', // h1 — the core question everywhere
		'One AI model each from different families reviews the same evidence', // pitch
		'Why so elaborate? ▸', // inline toggle in the head
		'Voted separately, then counted publicly.', // room lead
		'Three answers', // tube bead (name)
		'How the votes were counted', // §4.2 one block
		'The program only counts matching mentions.',
		'All votes, verbatim ▸', // full matrix at the end of the block
		'Original protocol in German.', // Rekord-Vermerk (Vorbehalte bleiben deutsch)
		'First ', // Erstvotum
		'Final ', // Schlussvotum
		'NobleCause does not handle money' // Geldfluss-Hinweis
	]);
	// Data-derived from the current session: consensus orgs + tallies (EN word) +
	// model marks; revisions/reservations only when the data actually carries them.
	for (const name of consensusOrgNames) {
		assert.ok(html.includes(name), `The Council (EN) fehlt Konsens-Org: ${name}`);
	}
	for (const t of tally('of')) {
		assert.ok(html.includes(t), `The Council (EN) fehlt Zählstand: ${t}`);
	}
	for (const p of DATA.participants) {
		assert.ok(html.includes(p.label), `The Council (EN) fehlt Modell-Marke: ${p.label}`);
	}
	if (DATA.revisions.length) {
		for (const rev of DATA.revisions) {
			assert.ok(html.includes(`>${rev.fromName}</del>`), `Council (EN) fehlt Revision: ${rev.fromName}`);
		}
	}
	if (DATA.consensus.some((r) => (r.convergence?.conditional_count ?? 0) > 0)) {
		assert.ok(html.includes('Reservation ▸'), 'Council (EN): reservation toggle missing');
	}
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
		'Dissent and reservations',
		"The council's wording ▸",
		'Record addenda',
		'Cost of this session',
		'/sitzungen/2026-07c/',
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
		// §1 Archiv-Ruhe-Stapel (statt Auf-Plate): Wand-mit-Loch + Flügel + ferne
		// Kleinauflösung (der Spalt zeigt den Zielraum bei Kamera 0).
		'scenes/archive-wall-hole.avif',
		'scenes/antechamber-display-lo.avif',
		'actors/door-leaf-left.avif',
		'actors/door-leaf-right.avif',
		// §2 Study-Ruhe-Stapel/Durchgang (Freischnitt aus antechamber-display,
		// Ziel hall): Wand-mit-Loch + Flügel + ferne Kleinauflösung des Councils.
		'scenes/antechamber-wall-hole.avif',
		'scenes/hall-display-lo.avif',
		'actors/antechamber-leaf-left.avif',
		'actors/antechamber-leaf-right.avif',
		// §2 Council-Ruhe-Stapel/Durchgang (Freischnitt aus hall-display,
		// Ziel archive): Wand-mit-Loch + Flügel + ferne Kleinauflösung des Archivs.
		'scenes/hall-wall-hole.avif',
		'scenes/archive-display-lo.avif',
		'actors/hall-leaf-left.avif',
		'actors/hall-leaf-right.avif',
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
	// Scout-Sitz aus den Daten (lastResearch.model). Zwischen „Aktuell:" und dem
	// Modell steht Template-Whitespace — Präfix und Modell-ID getrennt geprüft.
	assert.ok(studyHtml.includes('Aktuell:'), 'study: Scout-Sitz-Präfix „Aktuell:" fehlt');
	assert.ok(
		Boolean(DATA.lastResearch?.model) && studyHtml.includes(DATA.lastResearch.model),
		'study: Scout-Sitz-Modell (lastResearch.model) fehlt'
	);
	assert.ok(
		studyHtml.includes('sucht die wirksamsten Organisationen'),
		'study: Scout-Satz fehlt (DE)'
	);
	assert.ok(studyHtml.includes('alt="Zukunft"'), 'study: Bereichs-Emblemreihe (alt=label) fehlt');
	assert.ok(!studyHtml.includes('der Späher'), 'study: Gloss nicht mehr entfernt');
	// Warden-Entscheid + „letzte Prüfung" aus den Daten — zugleich Beleg, dass der
	// versöhnte Rekord hereingezogen ist: die Wart-Recherche journal/2026-07-27
	// (27. Juli 2026) ist der jüngste Lauf, neuer als master allein (20. Juli).
	// lastResearch-Datum als Beleg des Rekord-Zugs: das ISO-Datum steht im
	// datetime-Attribut (die formatierte Anzeige ist locale-abhängig).
	assert.ok(
		Boolean(DATA.lastResearch?.date) && studyHtml.includes(`datetime="${DATA.lastResearch.date}"`),
		'study: lastResearch-Datum (datetime-Attribut) fehlt'
	);
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
			DATA.participants.length,
			`${room}: erwartet ein Pult je Teilnehmer (modelTracks)`
		);
		assert.ok(
			!/class="pult-figure[^"]*"[^>]*tabindex/.test(html),
			`${room}: Pult-Figur trägt tabindex (nicht-interaktiv = kein Tab-Stopp)`
		);
	}
	// Beschriftung aus den Daten (participant.label + Anzeigename der Familie),
	// Rolle aus i18n — kein historischer Label-Hardcode (z. B. „Gemini Pro").
	for (const p of DATA.participants) {
		const alt = `${p.label} (${DATA.FAMILY[p.family]}): antwortet getrennt`;
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
		'scenes/hall-portrait-800.avif'
		// hall-door-open-display entfällt: Council nutzt den Ruhe-Stapel
		// (hall-wall-hole + Flügel), nicht mehr das Auf-Plate (Runde C §2).
	]) {
		assert.ok(fs.existsSync(path.join(SITE, 'build', 'media', asset)), `Deploy fehlt: ${asset}`);
	}
});

test('Bühne: zweite Ebene Archiv — Pult mit Leuchte + Tür-Hotspot (DE+EN)', (context) => {
	// No-JS-Wahrheit: das Möbel ist Teil des statischen Dokuments. Übergabe §7.1: der
	// Möbelkörper ist jetzt der Eingang zum Protokoll (Link auf die aktuelle Sitzung,
	// aria-label), das Bild dekorativ (alt=""). Die FIGUR selbst trägt keinen tabindex
	// (der native Anker ist der Tab-Stopp). Runde B §2: nur EIN Möbel (das Pult mit
	// Leuchte, rechts) — das Regal ist ersatzlos entfallen. Tür-Hotspot → zurück Study.
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
	// Übergabe §7.1: der Möbelkörper ist jetzt der Eingang zum Protokoll — das Pult
	// trägt einen Link auf die aktuelle Sitzung, das Bild ist dekorativ (alt=""),
	// der Name steht im aria-label. DE/EN gespiegelt. Kein generisches Bild-alt mehr.
	for (const [html, room, ariaStart, oldAlt] of [
		[archiveHtml, 'archive', 'Vollständiges Protokoll öffnen', 'Archivpult mit Leseleuchte'],
		[archiveEnHtml, 'archiveEn', 'Open the full protocol', 'Archive desk with a reading lamp']
	]) {
		assert.ok(
			/class="pult-link[^"]*"\s+href="\/sitzungen\//.test(html),
			`${room}: Pult-Eingang (pult-link → /sitzungen/) fehlt`
		);
		assert.ok(
			html.includes(`aria-label="${ariaStart}`),
			`${room}: aria-label des Pult-Eingangs (Protokoll + Sitzung) fehlt`
		);
		assert.ok(!html.includes(oldAlt), `${room}: Bild ist dekorativ (alt=""), kein generisches Pult-alt mehr`);
	}
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
