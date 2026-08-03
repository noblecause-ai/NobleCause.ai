import { getModelsRegistry, getSession, listSessions, md } from '$lib/server/content.js';

export function entries() {
	return listSessions().map((s) => ({ id: s.id }));
}

const PILLAR_ORDER = ['A', 'B', 'C', 'D'];

export function load({ params }) {
	const s = getSession(params.id);
	const models = getModelsRegistry();

	// Teilnehmer + Selbstdarstellung/Medaillon aus models.json (Konzept §4).
	// Frühere Modelle ohne Register-Eintrag: kein Medaillon (Name trägt allein).
	const participants = s.participants.map((p) => {
		const reg = models.get(p.model) ?? null;
		return {
			...p,
			medallion: reg?.asset ? reg.asset.replace(/\.avif$/, '-lo.avif') : null,
			person: reg?.person ?? null,
			motiv: reg?.motiv ?? null,
			begruendung: reg?.begruendung ?? null
		};
	});

	// Rohdaten LENIENT lesen (nie werfen) — der `organization`-String und die
	// convergence sind im Protokoll bereits registry-aufgelöst festgehalten.
	const initialRound = s.rounds.find((r) => r.kind === 'initial_vote');
	const finalRound = s.rounds.find((r) => r.kind === 'final_vote');
	const initialByModel = new Map((initialRound?.votes ?? []).map((v) => [v.model, v]));
	const finalByModel = new Map((finalRound?.votes ?? []).map((v) => [v.model, v]));
	const recOf = (vote, pillar) =>
		(vote?.recommendations ?? []).find((r) => r.pillar === pillar) ?? null;
	const markOf = (rec) =>
		rec
			? {
					org: rec.organization,
					orgId: rec.organization_id ?? null,
					conditional: !!rec.conditional,
					reservation: rec.reservation
				}
			: null;

	// Je Teilnehmer die Marken pro Bereich (Erst-/Schlussvotum, geändert).
	const tracks = participants.map((p) => {
		const iv = initialByModel.get(p.model);
		const fv = finalByModel.get(p.model);
		const rows = PILLAR_ORDER.map((pillar) => {
			const before = recOf(iv, pillar);
			const after = recOf(fv, pillar);
			return {
				pillar,
				initial: markOf(before),
				final: markOf(after),
				changed: Boolean(before && after && before.organization_id !== after.organization_id)
			};
		});
		return { ...p, rows };
	});

	// Je Bereich der Zählstand + genannte Organisation (aus der aggregierten Liste).
	const pillars = PILLAR_ORDER.map((pillar) => {
		const rec = (s.recommendations ?? []).find((r) => r.pillar === pillar) ?? null;
		return {
			pillar,
			hasConsensus: rec?.has_consensus ?? false,
			organization: rec?.organization ?? null,
			organizationId: rec?.organization_id ?? null,
			count: rec?.convergence?.count ?? null,
			total: rec?.convergence?.total ?? null,
			reservations: (rec?.convergence?.votes ?? []).filter((v) => v.conditional),
			rationale_html: rec?.rationale_md ? md(rec.rationale_md) : null
		};
	});

	return {
		session: {
			id: s.id,
			number: s.number,
			date: s.date,
			title: s.title,
			question: s.question,
			summary: s.summary ?? null,
			designation: s.designation ?? null,
			led_by: s.led_by ?? null,
			prompts: s.prompts ?? null,
			costs: s.costs,
			dissent_highlights: s.dissent_highlights ?? [],
			dissent_html: md(s.dissent_md),
			corrections: (s.correction_notice ?? []).map((c) => ({ date: c.date, html: md(c.text) })),
			wart_dossier: s.wart_dossier ?? null,
			wart_dossier_html: s.wart_dossier ? md(s.wart_dossier.content_md) : null,
			wart_opening_html: s.wart_opening_md ? md(s.wart_opening_md) : null,
			wart_moderation_html: s.wart_moderation_md ? md(s.wart_moderation_md) : null,
			// Wortlaut je Runde/Modell — ungekürzt (Konzept §5).
			rounds: s.rounds.map((r) => ({
				...r,
				votes: (r.votes ?? []).map((v) => ({ ...v, content_html: md(v.content_md) }))
			}))
		},
		participants,
		tracks,
		pillars
	};
}
