import { getSession, listSessions, md } from '$lib/server/content.js';

export function entries() {
	return listSessions().map((s) => ({ id: s.id }));
}

export function load({ params }) {
	const s = getSession(params.id);
	return {
		session: {
			...s,
			dissent_html: md(s.dissent_md),
			wart_dossier_html: s.wart_dossier ? md(s.wart_dossier.content_md) : null,
			rounds: s.rounds.map((r) => ({
				...r,
				votes: (r.votes ?? []).map((v) => ({ ...v, content_html: md(v.content_md) }))
			})),
			recommendations: (s.recommendations ?? []).map((rec) => ({
				...rec,
				rationale_html: md(rec.rationale_md)
			}))
		}
	};
}
