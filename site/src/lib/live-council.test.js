import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { conversation, feedIsStale, nearBottom, readSnapshot, splitRecordText, validateSnapshot, verifyContent } from './live-council.js';
import { md } from './markdown.js';

const hash = text => createHash('sha256').update(text).digest('hex');
const members = Array.from({ length: 5 }, (_, i) => ({ model: `test/${i}`, label: `Member ${i}`,
	family: `family${i}`, endpoint: 'test', provider_name: 'Test', quantization: 'unknown' }));
function fixture() {
	const record = { procedure_version: '0.6', session_id: 'test', events: [] };
	append(record, 'started');
	return { schema_version: 1, mode: 'live', published_at: '2026-09-21T10:00:00Z',
		session: { id: 'test', procedure_version: '0.6', number: 6, title: 'Fixture', question: 'Question',
			date: '2026-09-21', participants: structuredClone(members), chair: { model: members[0].model } },
		record, costs: { total_usd: '0', unassigned_usd: '0', by_model: [], unresolved: false } };
}
function append(record, kind, text = '', data = {}, model = null) {
	const seq = record.events.length + 1;
	const e = { seq, session_id: record.session_id, at: '2026-09-21T10:00:00Z', kind, phase: 'debate',
		model, role: model ? 'member' : 'system', content_md: text, data,
		content_sha256: hash(text), previous_sha256: record.events.at(-1)?.sha256 ?? '0'.repeat(64), sha256: hash(String(seq)) };
	record.events.push(e);
	return e;
}

test('accepts a contiguous append and verifies original UTF-8 wording', async () => {
	const old = fixture(), next = structuredClone(old);
	append(next.record, 'contribution', 'Wörtliche **Äußerung**.\nNoch eine Zeile.', {}, members[1].model);
	assert.equal(validateSnapshot(next, old), next);
	await verifyContent(next, old);
});

test('gaps, changed prefixes and regressions cannot replace the visible history', () => {
	const old = fixture(), next = structuredClone(old);
	append(next.record, 'contribution', 'Original', {}, members[1].model);
	const gap = structuredClone(next); gap.record.events[1].seq = 3;
	assert.throws(() => validateSnapshot(gap, old));
	const changed = structuredClone(next); changed.record.events[0].data.changed = true;
	assert.throws(() => validateSnapshot(changed, old));
	assert.throws(() => validateSnapshot(old, next));
	assert.equal(old.record.events.length, 1);
});

test('rejects incorrect model identity, remote medallions and changed session metadata', () => {
	const base = fixture();
	for (const change of [s => { s.session.participants[0].medallion = 'https://evil.test/a.svg'; },
		s => { s.session.chair.model = 'outsider'; }, s => { s.session.title = 'Rewritten'; }]) {
		const next = structuredClone(base); change(next);
		assert.throws(() => validateSnapshot(next, base));
	}
});

test('rejects content even if a forged envelope retains the old content hash', async () => {
	const s = fixture(); s.record.events[0].content_md = '<script>changed</script>';
	await assert.rejects(verifyContent(s));
});

test('only a complete independent voting group is displayed', () => {
	const s = fixture();
	append(s.record, 'initial_votes', '', { votes: members.slice(0, 4).map(m => ({ model: m.model, content_md: 'vote' })) });
	assert.throws(() => validateSnapshot(s));
	s.record.events[1].data.votes.push({ model: members[4].model, content_md: 'vote' });
	s.record.events[1].content_md = s.record.events[1].data.votes.map(v => `### ${v.model}\n${v.content_md}`).join('\n\n');
	s.record.events[1].content_sha256 = hash(s.record.events[1].content_md);
	validateSnapshot(s);
});

test('absent first feed is idle, later 404 and failed HTTP requests are errors', async () => {
	const fetcher = async () => ({ status: 404, ok: false });
	assert.equal(await readSnapshot(null, { fetcher }), null);
	await assert.rejects(readSnapshot(fixture(), { fetcher }));
	await assert.rejects(readSnapshot(null, { fetcher: async () => ({ status: 500, ok: false }) }));
});

test('final vote reveal follows the backend contract without inventing combined prose', () => {
	const s = fixture();
	append(s.record, 'final_votes', '', { votes: members.map(m => ({ model: m.model, content_md: 'Original final vote' })) });
	validateSnapshot(s);
	assert.equal(conversation(s.record).at(-1).data.votes.length, 5);
	assert.equal(s.record.events.at(-1).content_md, '');
});

test('reader requests uncached JSON and preserves previous data on bad response', async () => {
	const old = fixture(), next = structuredClone(old);
	append(next.record, 'contribution', 'New', {}, members[2].model);
	const result = await readSnapshot(old, { fetcher: async (url, options) => {
		assert.equal(url, '/live/current.json'); assert.equal(options.cache, 'no-store');
		return { ok: true, status: 200, json: async () => next };
	} });
	assert.equal(result.record.events.length, 2); assert.equal(old.record.events.length, 1);
});

test('heartbeat distinguishes interrupted publication from replay and completion', () => {
	const s = fixture(), now = Date.parse(s.published_at);
	assert.equal(feedIsStale(s, now + 50000), false);
	assert.equal(feedIsStale(s, now + 76000), true);
	s.mode = 'replay'; assert.equal(feedIsStale(s, now + 500000), false);
	s.mode = 'live'; append(s.record, 'completed'); assert.equal(feedIsStale(s, now + 500000), false);
});

test('conversation preserves original contributions and labels chair projections', () => {
	const s = fixture();
	append(s.record, 'waiting', '', {}, members[0].model);
	const raw = '{"question":"Frage?","next_model_id":"test/1"}';
	append(s.record, 'moderation', raw, { question: 'Frage?', next_model_id: members[1].model }, members[0].model);
	const speech = 'Ich stimme nicht zu.\n\n```json\n{"objection":true}\n```';
	append(s.record, 'contribution', speech, {}, members[1].model);
	const visible = conversation(s.record);
	assert.equal(visible.length, 3);
	assert.equal(visible[1].prose, 'Frage?'); assert.equal(visible[1].content_md, raw);
	assert.equal(visible[2].content_md, speech); assert.equal(visible[2].structure, '{"objection":true}');
	assert.ok(visible[2].prose.includes('Ich stimme nicht zu.'));
});

test('malformed JSON is never silently removed from the visible word record', () => {
	const raw = 'Text\n```json\nnot-json\n```';
	assert.deepEqual(splitRecordText(raw), { prose: raw, structure: null });
});

test('live Markdown uses the same escaping and URL policy as archived records', () => {
	const rendered = md('<img src=x onerror=alert(1)>\n\n[bad](javascript:alert)\n\n**Einwand**');
	assert.ok(rendered.includes('&lt;img')); assert.ok(!rendered.includes('href="javascript:'));
	assert.ok(rendered.includes('<strong>Einwand</strong>'));
});

test('scroll follow stays off while reading earlier contributions', () => {
	assert.equal(nearBottom({ scrollHeight: 2000, scrollTop: 1600, clientHeight: 400 }), true);
	assert.equal(nearBottom({ scrollHeight: 2000, scrollTop: 200, clientHeight: 400 }), false);
});
