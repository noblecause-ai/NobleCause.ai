const PILLARS = {
	A: 'Investition in die Zukunft',
	B: 'Linderung von Leid',
	C: 'Schutz vor großen Gefahren',
	D: 'Übersehenes'
};

export function normalizeHighlights(value) {
	if (Array.isArray(value)) return value;
	if (typeof value === 'string' && value.trim()) return [value];
	return [];
}

export function registryMap(registry) {
	return new Map((registry.organizations ?? []).map((organization) => [organization.id, organization]));
}

export function resolveOrganization(id, registry) {
	const organization = registry.get(id);
	if (!organization) throw new Error(`Unbekannte organization_id: ${id}`);
	return {
		id: organization.id,
		name: organization.canonical_name,
		description: organization.beschreibung,
		donationUrl: organization.donation_url ?? null
	};
}

function resolveVote(vote, registry) {
	const organization = resolveOrganization(vote.organization_id, registry);
	if (vote.organization && vote.organization !== organization.name) {
		throw new Error(
			`Widersprüchlicher Organisationsname für ${vote.organization_id}: ${vote.organization}`
		);
	}
	return {
		...vote,
		organization
	};
}

export function buildModelTracks(session, registry) {
	const initial = session.rounds.find((round) => round.kind === 'initial_vote');
	const final = session.rounds.find((round) => round.kind === 'final_vote');
	const initialByModel = new Map((initial?.votes ?? []).map((vote) => [vote.model, vote]));
	const finalByModel = new Map((final?.votes ?? []).map((vote) => [vote.model, vote]));

	return session.participants.map((participant) => {
		const initialVote = initialByModel.get(participant.model);
		const finalVote = finalByModel.get(participant.model);
		const initialRecommendations = (initialVote?.recommendations ?? []).map((vote) =>
			resolveVote(vote, registry)
		);
		const finalRecommendations = (finalVote?.recommendations ?? []).map((vote) =>
			resolveVote(vote, registry)
		);
		const rows = ['A', 'B', 'C', 'D'].map((pillar) => {
			const before = initialRecommendations.find((vote) => vote.pillar === pillar) ?? null;
			const after = finalRecommendations.find((vote) => vote.pillar === pillar) ?? null;
			return {
				pillar,
				pillarName: PILLARS[pillar],
				initial: before,
				final: after,
				changed: Boolean(before && after && before.organization.id !== after.organization.id)
			};
		});
		return {
			...participant,
			initialContent: initialVote?.content_md ?? null,
			finalContent: finalVote?.content_md ?? null,
			rows
		};
	});
}

export function buildRecommendations(session, registry) {
	return session.recommendations.map((recommendation) => {
		if (recommendation.has_consensus) {
			const organization = resolveOrganization(recommendation.organization_id, registry);
			if (recommendation.organization !== organization.name) {
				throw new Error(`Widersprüchlicher Organisationsname für ${recommendation.organization_id}`);
			}
			return {
				pillar: recommendation.pillar,
				pillarName: PILLARS[recommendation.pillar],
				hasConsensus: true,
				title: recommendation.title,
				organization,
				confidence: recommendation.confidence,
				count: recommendation.convergence.count,
				total: recommendation.convergence.total,
				conditionalCount: recommendation.convergence.conditional_count,
				reservations: recommendation.convergence.votes.filter((vote) => vote.conditional)
			};
		}

		return {
			pillar: recommendation.pillar,
			pillarName: PILLARS[recommendation.pillar],
			hasConsensus: false,
			title: recommendation.title,
			votes: (recommendation.individual_votes ?? []).map((vote) => ({
				...vote,
				organization: resolveOrganization(vote.organization_id, registry)
			}))
		};
	});
}

// Übersicht des Explorers (/sessions): je Sitzung ein Bereichs-Kurzstatus
// (Zählstand + genannte Organisation). Auflösung LENIENT wie das Archiv — der
// Explorer läuft über ALLE Sitzungen, eine alte Organisation kann aus der
// Registry gefallen sein; niemals werfen (das strikte resolveOrganization gilt
// nur für die aktuelle Sitzung der Räume).
export function buildSessionSummaries(sessions, registry) {
	const organizations = registryMap(registry);
	return sessions.map((session) => ({
		id: session.id,
		number: session.number,
		date: session.date,
		title: session.title,
		question: session.question,
		total_eur: session.costs?.total ?? null,
		pillars: ['A', 'B', 'C', 'D'].map((pillar) => {
			const recommendation = (session.recommendations ?? []).find((r) => r.pillar === pillar);
			if (!recommendation) return { pillar, status: 'missing', name: null, count: null, total: null };
			if (!recommendation.has_consensus) {
				return { pillar, status: 'open', name: null, count: null, total: null };
			}
			const organization = organizations.get(recommendation.organization_id);
			return {
				pillar,
				status: 'consensus',
				name: organization?.canonical_name ?? recommendation.organization ?? null,
				organization_id: recommendation.organization_id ?? null,
				count: recommendation.convergence?.count ?? null,
				total: recommendation.convergence?.total ?? null
			};
		})
	}));
}

export function buildHomepageViewModel({ session, sessions, registry }) {
	if ((session.unresolved_votes ?? []).length) {
		throw new Error(`Sitzung ${session.id} enthält unaufgelöste Stimmen`);
	}
	const organizations = registryMap(registry);
	const modelTracks = buildModelTracks(session, organizations);
	// Klartext-Schicht (§1 des Raum-Content): laienverständliche Übersetzung als
	// eigenes, vom Wart freigegebenes Datenfeld. Liegt noch in KEINER Sitzung
	// vor — bis dahin sind die Felder null und die Räume zeigen die
	// Rekord-Schicht mit dem Vermerk „Klartext folgt" (Publikation wird nie
	// verzögert). EN fällt auf DE zurück (plainEnDe markiert das), bis
	// plain_en im selben Freigabe-Verfahren nachkommt. Das Frontend
	// paraphrasiert nie — es liest das Feld nur, wenn es existiert.
	const plain = session.plain ?? null;
	const plainEn = session.plain_en ?? plain;
	return {
		currentSession: {
			id: session.id,
			number: session.number,
			date: session.date,
			title: session.title,
			question: session.question,
			// Sitzinhaber des Warden-Amts, wörtlich aus led_by (versiegelte Datennaht).
			ledBy: session.led_by ?? null
		},
		plain,
		plainEn,
		plainEnDe: Boolean(plain && !session.plain_en),
		recommendations: buildRecommendations(session, organizations),
		modelTracks,
		revisions: modelTracks.flatMap((track) =>
			track.rows.filter((row) => row.changed).map((row) => ({ model: track.label, ...row }))
		),
		correction: session.correction_notice ?? null,
		dissent: session.dissent_md,
		dissentHighlights: normalizeHighlights(session.dissent_highlights),
		// Offene Bereiche der aktuellen Sitzung mit ihren Klartext-Zeilen
		// (§5.3 — Tatsache/Gegenstand des Dissenses; die Argumente bleiben
		// Wortlaut im Ausklapp). Ohne plain-Feld ist plain je Zeile null.
		dissentOpen: (session.recommendations ?? [])
			.filter((recommendation) => !recommendation.has_consensus)
			.map((recommendation) => ({
				pillar: recommendation.pillar,
				pillarName: PILLARS[recommendation.pillar],
				plain: plain?.dissent?.[recommendation.pillar] ?? null,
				plainEn: plainEn?.dissent?.[recommendation.pillar] ?? null
			})),
		costs: session.costs,
		wartDossier: session.wart_dossier ?? null,
		archive: sessions.map((item) => ({
			...item,
			nonConsensusPillars: (item.recommendations ?? [])
				.filter((recommendation) => !recommendation.has_consensus)
				.map((recommendation) => recommendation.pillar),
			// Ergebnis-Chips je Bereich (§5.2 — das Regal zeigt Ergebnisse,
			// keine Dateinamen). Auflösung Registry zuerst (kanonischer Name),
			// bei Miss der protokollierte String — NIE werfen: das Archiv läuft
			// über alle Sitzungen, eine alte Organisation kann aus der Registry
			// gefallen sein. (Das strikte resolveOrganization mit throw gilt
			// weiterhin nur für die aktuelle Sitzung.)
			chips: ['A', 'B', 'C', 'D'].map((pillar) => {
				const recommendation = (item.recommendations ?? []).find((r) => r.pillar === pillar);
				if (!recommendation) return { pillar, status: 'missing', name: null };
				if (!recommendation.has_consensus) return { pillar, status: 'open', name: null };
				const organization = organizations.get(recommendation.organization_id);
				return {
					pillar,
					status: 'consensus',
					name: organization?.canonical_name ?? recommendation.organization ?? null
				};
			})
		}))
	};
}

export { PILLARS };
