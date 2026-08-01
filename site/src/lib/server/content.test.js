import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { md } from './content.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const read = (file) => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));

// Sichtbaren Text gewinnen: Tags entfernen, HTML-Entities zurückdecodieren.
// Damit ist prüfbar, ob der LESER denselben Text sieht, unabhängig davon, wie
// das Markup escaped/attributiert ist.
function visibleText(html) {
	return html
		.replace(/<[^>]*>/g, '')
		.replace(/&lt;/g, '<')
		.replace(/&gt;/g, '>')
		.replace(/&quot;/g, '"')
		.replace(/&#39;/g, "'")
		.replace(/&amp;/g, '&');
}

// --- Teil A: synthetisches Fixture (Opus-5-Auftrag §5) ---
// Roh-HTML · javascript:-Link · onerror-Attribut · <script> · gewöhnlicher https-Link.

const FIXTURE = [
	'Ein gewöhnlicher Beleglink: [Helen Keller International](https://helenkellerintl.org/donate/).',
	'',
	'Ein untergeschobener Link: [jetzt spenden](javascript:alert(1)).',
	'',
	'Roh-HTML mittendrin: <script>alert("xss")</script> und <img src=x onerror=alert(1)>.',
	'',
	'Ein Bild mit bösem Schema: ![Spendenlogo](javascript:alert(2)).'
].join('\n');

test('Teil A — gewöhnlicher Link bleibt klickbar und trägt die rel-Attribute', () => {
	const out = md(FIXTURE);
	assert.match(out, /<a href="https:\/\/helenkellerintl\.org\/donate\/"/);
	assert.match(out, /rel="nofollow noopener noreferrer ugc"/);
	assert.match(out, />Helen Keller International<\/a>/);
});

test('Teil A — javascript:-Link ist nicht navigierbar, Text bleibt sichtbar', () => {
	const out = md(FIXTURE);
	assert.doesNotMatch(out, /href="javascript:/i);
	assert.ok(visibleText(out).includes('jetzt spenden'), 'Linktext bleibt erhalten');
});

test('Teil A — Roh-HTML wird escaped, kein <script>, kein lebendiger Event-Handler', () => {
	const out = md(FIXTURE);
	assert.doesNotMatch(out, /<script/i, 'kein lebendiges script-Tag');
	assert.doesNotMatch(out, /<img[^>]*onerror/i, 'kein lebendiges img mit onerror');
	// Escaped und damit als Text sichtbar:
	assert.ok(out.includes('&lt;script&gt;'), 'script als Text sichtbar');
	assert.ok(visibleText(out).includes('alert("xss")'), 'script-Inhalt bleibt lesbar');
	assert.ok(visibleText(out).includes('onerror=alert(1)'), 'img-Roh-HTML bleibt als Text lesbar');
});

test('Teil A — Bild mit javascript:-Quelle lädt nicht, Alt-Text bleibt sichtbar', () => {
	const out = md(FIXTURE);
	assert.doesNotMatch(out, /<img[^>]*src="javascript:/i);
	assert.ok(visibleText(out).includes('Spendenlogo'), 'Alt-Text bleibt erhalten');
});

test('Teil A — kein einziges gefährliches Schema in irgendeinem href/src', () => {
	const out = md(FIXTURE);
	assert.doesNotMatch(out, /(?:href|src)="\s*(?:javascript|data|vbscript):/i);
});

test('Teil A — verschleierte Schemata (Tab, Groß/Klein, Leerzeichen) greifen nicht', () => {
	const cases = [
		'[a](javascript:alert(1))',
		'[b](jAvAsCrIpT:alert(1))',
		'[c](java\tscript:alert(1))',
		'[d]( javascript:alert(1))',
		'[e](vbscript:msgbox(1))',
		'[f](data:text/html,<script>alert(1)</script>)'
	].join('\n\n');
	const out = md(cases);
	assert.doesNotMatch(out, /href="[^"]*(?:javascript|vbscript|data):/i);
	// Die sichtbaren Linktexte bleiben alle erhalten (nichts still entfernt):
	for (const label of ['a', 'b', 'c', 'd', 'e', 'f']) {
		assert.ok(visibleText(out).includes(label), `Linktext "${label}" bleibt erhalten`);
	}
});

// --- Teil B: echter Rekordtext (§5) — die Darstellung darf sich nicht verändern ---
// 2026-07c enthält kein Roh-HTML und keine Markdown-Links (geprüft): die
// Renderer-Overrides greifen nicht, also muss die Ausgabe Byte-für-Byte der
// unkonfigurierten marked-Ausgabe entsprechen. Stärkster Beleg für „unverändert".

test('Teil B — Sitzungs-Dissens rendert unverändert (byte-identisch zu marked)', () => {
	const s = read('sessions/2026-07c/session.json');
	assert.equal(md(s.dissent_md), marked.parse(s.dissent_md));
});

test('Teil B — Wart-Dossier rendert unverändert (byte-identisch zu marked)', () => {
	const s = read('sessions/2026-07c/session.json');
	assert.ok(s.wart_dossier?.content_md, 'Dossier-Text vorhanden');
	assert.equal(md(s.wart_dossier.content_md), marked.parse(s.wart_dossier.content_md));
});

test('Teil B — Journal-Eintrag rendert unverändert (byte-identisch zu marked)', () => {
	const j = read('journal/2026-07-24/entry.json');
	assert.equal(md(j.content_md), marked.parse(j.content_md));
});

// --- Teil B (Breite): der gesamte lebende Rekord bleibt frei von ausführbaren Vektoren ---

function allRecordTexts() {
	const texts = [];
	const sessionsDir = path.join(ROOT, 'sessions');
	for (const e of fs.readdirSync(sessionsDir, { withFileTypes: true })) {
		if (!e.isDirectory()) continue;
		const file = path.join(sessionsDir, e.name, 'session.json');
		if (!fs.existsSync(file)) continue;
		const s = JSON.parse(fs.readFileSync(file, 'utf8'));
		for (const t of [
			s.dissent_md,
			s.wart_opening_md,
			s.wart_moderation_md,
			s.wart_dossier?.content_md,
			s.correction_notice?.text
		])
			if (t) texts.push([`sessions/${e.name}`, t]);
		for (const r of s.rounds ?? [])
			for (const v of r.votes ?? []) if (v.content_md) texts.push([`sessions/${e.name}/${r.kind}/${v.model}`, v.content_md]);
		for (const rec of s.recommendations ?? [])
			if (rec.rationale_md) texts.push([`sessions/${e.name}/rec/${rec.pillar}`, rec.rationale_md]);
	}
	const journalDir = path.join(ROOT, 'journal');
	for (const e of fs.readdirSync(journalDir, { withFileTypes: true })) {
		if (!e.isDirectory() || !/^\d{4}-\d{2}-\d{2}[a-z]?$/.test(e.name)) continue;
		const file = path.join(journalDir, e.name, 'entry.json');
		if (!fs.existsSync(file)) continue;
		const j = JSON.parse(fs.readFileSync(file, 'utf8'));
		if (j.content_md) texts.push([`journal/${e.name}`, j.content_md]);
	}
	texts.push(['manifest.md', fs.readFileSync(path.join(ROOT, 'manifest.md'), 'utf8')]);
	return texts;
}

test('Teil B (Breite) — kein Rekordtext erzeugt einen ausführbaren Vektor', () => {
	for (const [label, text] of allRecordTexts()) {
		const out = md(text);
		assert.doesNotMatch(out, /<script/i, `${label}: kein script-Tag`);
		assert.doesNotMatch(out, /(?:href|src)="\s*(?:javascript|data|vbscript):/i, `${label}: kein gefährliches Schema`);
		assert.doesNotMatch(out, /<[a-z][^>]*\son\w+\s*=/i, `${label}: kein lebendiger Event-Handler`);
	}
});
