// A read-only projection. Voting and cost aggregation remain in the backend.
const KINDS = new Set(['started', 'checkpoint', 'waiting', 'initial_votes', 'moderation',
	'contribution', 'debate_closed', 'final_votes', 'summary', 'completed', 'aborted', 'resumed']);
const HASH = /^[a-f0-9]{64}$/;
const simpleId = /^[A-Za-z0-9][A-Za-z0-9_-]*$/;
const canonical = (value) => JSON.stringify(value, (_, v) => v && typeof v === 'object' && !Array.isArray(v)
	? Object.fromEntries(Object.keys(v).sort().map((key) => [key, v[key]])) : v);
const fail = () => { throw new Error('invalid_live_feed'); };

export function validateSnapshot(snapshot, previous = null) {
	if (snapshot?.schema_version !== 1 || !['live', 'pilot', 'replay'].includes(snapshot.mode)
		|| !Number.isFinite(Date.parse(snapshot.published_at))) fail();
	const session = snapshot.session;
	if (!session || !simpleId.test(session.id) || session.procedure_version !== '0.6'
		|| !Number.isInteger(session.number) || session.number < 1
		|| !['title', 'question', 'date'].every(k => typeof session[k] === 'string' && session[k])
		|| !Array.isArray(session.participants) || session.participants.length !== 5) fail();
	const ids = session.participants.map(m => m.model);
	if (new Set(ids).size !== 5 || !ids.includes(session.chair?.model)) fail();
	for (const m of session.participants) {
		if (!['model', 'label', 'family', 'endpoint', 'provider_name', 'quantization'].every(k => typeof m[k] === 'string' && m[k])) fail();
		if (m.medallion && !/^\/media\/medallions\/[a-zA-Z0-9._-]+\.avif$/.test(m.medallion)) fail();
	}
	const record = snapshot.record;
	if (record?.session_id !== session.id || record.procedure_version !== '0.6' || !Array.isArray(record.events)) fail();
	let hash = '0'.repeat(64);
	for (const [index, e] of record.events.entries()) {
		if (e.seq !== index + 1 || e.session_id !== session.id || !KINDS.has(e.kind)
			|| typeof e.content_md !== 'string' || !Number.isFinite(Date.parse(e.at))
			|| !['system', 'chair', 'member'].includes(e.role)
			|| !['setup', 'initial', 'debate', 'final', 'summary', 'terminal'].includes(e.phase)
			|| !e.data || typeof e.data !== 'object' || Array.isArray(e.data)
			|| (e.model !== null && !ids.includes(e.model))
			|| !HASH.test(e.sha256) || !HASH.test(e.content_sha256) || e.previous_sha256 !== hash) fail();
		hash = e.sha256;
		if (e.kind === 'moderation') {
			let original;
			try { original = JSON.parse(e.content_md); } catch { fail(); }
			if (typeof e.data.question !== 'string' || !ids.includes(e.data.next_model_id)
				|| original.question !== e.data.question || original.next_model_id !== e.data.next_model_id) fail();
		}
		if (['initial_votes', 'final_votes'].includes(e.kind)) {
			if (!Array.isArray(e.data.votes) || e.data.votes.length !== 5
				|| new Set(e.data.votes.map(v => v.model)).size !== 5
				|| e.data.votes.some(v => !ids.includes(v.model) || typeof v.content_md !== 'string')) fail();
			// Initial votes also carry the combined transcript; the established final
			// reveal carries votes in data only. Its full hash is checked by the publisher.
			if (e.kind === 'initial_votes' && e.content_md !== e.data.votes.map(v => `### ${v.model}\n${v.content_md}`).join('\n\n')) fail();
		}
	}
	if (previous) {
		if (canonical(previous.session) !== canonical(session) || previous.mode !== snapshot.mode
			|| previous.record.events.length > record.events.length) fail();
		for (let i = 0; i < previous.record.events.length; i++) {
			if (canonical(previous.record.events[i]) !== canonical(record.events[i])) fail();
		}
	}
	const costs = snapshot.costs;
	if (!costs || !Array.isArray(costs.by_model) || !Number.isFinite(Number(costs.total_usd))
		|| Number(costs.total_usd) < 0 || !Number.isFinite(Number(costs.unassigned_usd))
		|| Number(costs.unassigned_usd) < 0 || costs.by_model.some(c => !ids.includes(c.model)
			|| !Number.isFinite(Number(c.usd)) || Number(c.usd) < 0)) fail();
	return snapshot;
}

// Compare content hashes as well as the immutable prefix. Python owns the whole
// event hash (its number encoding differs from JSON.stringify for e.g. 1.0).
export async function verifyContent(snapshot, previous = null, crypto = globalThis.crypto) {
	if (!crypto?.subtle) throw new Error('integrity_unavailable');
	await Promise.all(snapshot.record.events.slice(previous?.record.events.length ?? 0).map(async e => {
		const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(e.content_md));
		const hash = [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, '0')).join('');
		if (hash !== e.content_sha256) fail();
	}));
}

export async function readSnapshot(previous = null, { fetcher = fetch, signal } = {}) {
	const response = await fetcher('/live/current.json', { cache: 'no-store', signal, headers: { Accept: 'application/json' } });
	if (response.status === 404 && !previous) return null;
	if (!response.ok) throw new Error('feed_unavailable');
	const candidate = await response.json();
	// A different session is offered explicitly; never overwrite an open history.
	const same = previous?.session.id === candidate?.session?.id ? previous : null;
	validateSnapshot(candidate, same);
	await verifyContent(candidate, same);
	return candidate;
}

export function feedIsStale(snapshot, now = Date.now()) {
	return snapshot.mode !== 'replay' && !['completed', 'aborted'].includes(snapshot.record.events.at(-1)?.kind)
		&& now - Date.parse(snapshot.published_at) > 75000;
}

export function splitRecordText(text) {
	const match = /\n?```json\s*\n([\s\S]*?)\n```\s*$/.exec(text);
	if (!match) return { prose: text, structure: null };
	try { JSON.parse(match[1]); } catch { return { prose: text, structure: null }; }
	return { prose: text.slice(0, match.index), structure: match[1] };
}

export function conversation(record) {
	return record.events.filter(e => e.kind !== 'waiting' && e.kind !== 'checkpoint').map(e => {
		const parts = splitRecordText(e.content_md);
		if (e.kind === 'moderation') return { ...e, prose: e.data.question, structure: e.content_md };
		if (e.kind === 'summary' && parts.structure) {
			const summary = JSON.parse(parts.structure);
			if (typeof summary.summary === 'string') return { ...e, prose: summary.summary, structure: e.content_md };
		}
		return { ...e, ...parts };
	});
}

export const nearBottom = (element) => element.scrollHeight - element.scrollTop - element.clientHeight < 60;

export const memberShort = (m) => ({
	'anthropic/claude-fable-5.1': 'Fable 5.1', 'openai/gpt-6-astra': 'Astra',
	'x-ai/grok-4.6': 'Grok 4.6', 'moonshotai/kimi-k3': 'Kimi K3', 'z-ai/glm-5.3': 'GLM 5.3'
}[m.model] ?? m.label);
export const memberSymbol = m => m.model === 'z-ai/glm-5.3' ? 'Z' : memberShort(m).slice(0, 1);

export const liveCopy = {
	de: {
		procedure: 'Fünf KI-Modelle beraten über dieselben Belege. Erst- und Schlussvoten entstehen jeweils unabhängig und werden anschließend gemeinsam offengelegt. Dazwischen erhält jeder Redner den bisherigen Gesprächsverlauf. Der Vorsitz organisiert das Gespräch, beteiligt sich mit eigenen Beiträgen im gleichen Redekontingent und stimmt mit genau einer Stimme mit; seine Fragen können den Verlauf beeinflussen. Ein festes Programm zählt die Schlussvoten. Eine gemeinsame Empfehlung benötigt mindestens drei der fünf Stimmen. Beiträge, Quellen, Ausfälle und bestätigte Kosten je Modell bleiben nachvollziehbar. Die Scouts recherchieren getrennt und ohne vorgegebene frühere Ergebnisse; der historische Vergleich folgt danach. Die Anbieter liefern kein vollständiges Suchprotokoll. Lücken werden ausgewiesen, und von Modellen genannte Suchanfragen sind als Selbstauskunft gekennzeichnet.',
		procedureLabel: 'So berät der Rat',
		title: 'Der Rat im Gespräch', chair: 'Vorsitz', member: 'Ratsmitglied', council: 'Rat',
		open: 'Ratsgespräch öffnen', close: 'Saal ansehen', latest: 'Zum neuesten Beitrag ↓',
		live: 'Live · vorläufig', pilot: 'Testlauf · vorläufig', replay: 'Wiedergabe · Testlauf',
		completed: 'Sitzung abgeschlossen', aborted: 'Sitzung unterbrochen', resumed: 'Sitzung fortgesetzt',
		started: 'Die Sitzung beginnt.', debate_closed: 'Die Beratung ist beendet. Die Schlussvoten entstehen unabhängig voneinander.',
		initial_votes: 'Alle fünf Erstvoten liegen vor', final_votes: 'Alle fünf Schlussvoten liegen vor',
		summary: 'Leserfassung des Vorsitzes', waiting: 'denkt nach …', speaking: 'spricht', last: 'Letzter Beitrag',
		phases: { setup: 'Vorbereitung', initial: 'Unabhängige Erstvoten', debate: 'Beratung', final: 'Unabhängige Schlussvoten', summary: 'Leserfassung', terminal: 'Abschluss' },
		error: 'Übertragung unterbrochen. Der letzte bestätigte Verlauf bleibt sichtbar.',
		unavailable: 'Die Live-Ansicht ist derzeit nicht erreichbar.', stale: 'Seit längerer Zeit kein Lebenszeichen der Sitzung. Der letzte bestätigte Verlauf bleibt sichtbar.',
		raw: 'Original und Herkunft', original: 'Originalwortlaut', structure: 'Strukturierter Abschluss',
		credits: 'Credits bestätigt', costs: 'Kosten nach Modell', unassigned: 'Noch nicht einem veröffentlichten Beitrag zugeordnet',
		unresolved: 'Weitere Kosten sind noch ungeklärt.', unknown: 'unbekannt', sourceSymbol: 'Bildzeichen des Vorgängermodells',
		newSession: 'Neue Sitzung öffnen', noSpeech: 'Noch kein öffentlicher Beitrag dieses Mitglieds.',
		votesNote: 'Erst- und Schlussvoten werden jeweils erst nach Abschluss aller fünf Antworten gemeinsam sichtbar.',
		recordNote: 'Fünf Mitglieder · fünf gleiche Stimmen. Der Vorsitz führt das Gespräch und hat eine Stimme.',
		nojs: 'Die Live-Ansicht benötigt JavaScript. Abgeschlossene Sitzungen stehen weiter unten im Archiv.',
		intro: 'Fünf KI-Modelle beraten gemeinsam und geben anschließend unabhängig ihre Schlussvoten ab.',
		lead: 'Ein gemeinsames Gespräch. Fünf unabhängige Schlussvoten.', session: n => `Sitzung ${n}`,
		majorityRule: 'Mindestens drei der fünf Stimmen ergeben eine gemeinsame Empfehlung.',
		archive: 'Unveränderter Ereignisrekord', provenance: 'Sprecherzuordnung laut API; Selbstauskünfte bleiben im Original erhalten.'
	},
	en: {
		procedure: 'Five AI models consider the same evidence. Initial and final votes are each prepared independently and revealed together afterward. In between, each speaker receives the conversation so far. The chair organizes the discussion, contributes its own remarks within the same speaking quota, and has exactly one vote; its questions can shape the discussion. A fixed program counts the final votes. A shared recommendation requires at least three of the five votes. Contributions, sources, failures and confirmed costs by model remain traceable. The Scouts research separately without being given earlier findings; comparison with historical results follows afterward. Providers do not supply complete search logs. Gaps are disclosed, and search queries stated by models are labeled as self-reported.',
		procedureLabel: 'How the Council deliberates',
		title: 'The Council in conversation', chair: 'Chair', member: 'Council member', council: 'Council',
		open: 'Open the conversation', close: 'View the room', latest: 'Jump to latest ↓',
		live: 'Live · provisional', pilot: 'Pilot · provisional', replay: 'Replay · pilot',
		completed: 'Session completed', aborted: 'Session interrupted', resumed: 'Session resumed',
		started: 'The session begins.', debate_closed: 'The discussion has ended. Final votes are being prepared independently.',
		initial_votes: 'All five initial votes are available', final_votes: 'All five final votes are available',
		summary: 'The chair’s summary', waiting: 'is considering …', speaking: 'speaking', last: 'Latest contribution',
		phases: { setup: 'Preparation', initial: 'Independent initial votes', debate: 'Discussion', final: 'Independent final votes', summary: 'Summary', terminal: 'Conclusion' },
		error: 'Connection interrupted. The last confirmed conversation remains visible.',
		unavailable: 'The live view is currently unavailable.', stale: 'No recent heartbeat from the session. The last confirmed conversation remains visible.',
		raw: 'Original and provenance', original: 'Original wording', structure: 'Structured response',
		credits: 'confirmed credits', costs: 'Costs by model', unassigned: 'Not yet assigned to a published contribution',
		unresolved: 'Additional costs remain unresolved.', unknown: 'unknown', sourceSymbol: 'Predecessor model’s symbol',
		newSession: 'Open the new session', noSpeech: 'No public contribution from this member yet.',
		votesNote: 'Initial and final votes are each revealed together after all five answers are complete.',
		recordNote: 'Five members · five equal votes. The chair guides the conversation and has one vote.',
		nojs: 'The live view requires JavaScript. Completed sessions remain available in the archive below.',
		intro: 'Five AI models discuss the evidence together, then cast their final votes independently.',
		lead: 'One shared conversation. Five independent final votes.', session: n => `Session ${n}`,
		majorityRule: 'A shared recommendation requires at least three of the five votes.',
		archive: 'Unchanged event record', provenance: 'Speaker identity comes from the API; self-identification remains in the original text.'
	}
};
