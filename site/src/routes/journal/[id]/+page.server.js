import {
	getCommission,
	getJournalEntry,
	getModelsRegistry,
	listJournalEntries,
	md
} from '$lib/server/content.js';

export function entries() {
	return listJournalEntries().map((e) => ({ id: e.id }));
}

export function load({ params }) {
	const e = getJournalEntry(params.id);
	const entry = {
		...e,
		content_html: e.content_md ? md(e.content_md) : null
	};

	// Kommissions-Eintrag (Konzept §6): die Bestellung als eigener Typ, mit den
	// Aufträgen (Motiv/Begründung je Modell, within_limits) + Medaillon aus dem
	// Register. Nicht als Sitzung gezählt.
	let commission = null;
	if (e.type === 'commission' && e.commission_ref) {
		const c = getCommission(e.commission_ref);
		if (c) {
			const models = getModelsRegistry();
			commission = {
				convened: c.convened ?? null,
				ordered: c.ordered ?? null,
				dry_run: c.dry_run ?? null,
				orders: (c.orders ?? []).map((o) => {
					const reg = models.get(o.model);
					return {
						model: o.model,
						label: o.label ?? reg?.model_label ?? o.model,
						family: o.family ?? null,
						motiv: o.motiv ?? null,
						begruendung: o.begruendung ?? null,
						within_limits: o.within_limits ?? null,
						medallion: reg?.asset ? reg.asset.replace(/\.avif$/, '-lo.avif') : null
					};
				})
			};
		}
	}

	return { entry, commission };
}
