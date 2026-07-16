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

export function buildHomepageViewModel({ session, sessions, registry }) {
	if ((session.unresolved_votes ?? []).length) {
		throw new Error(`Sitzung ${session.id} enthält unaufgelöste Stimmen`);
	}
	const organizations = registryMap(registry);
	const modelTracks = buildModelTracks(session, organizations);
	return {
		currentSession: {
			id: session.id,
			number: session.number,
			date: session.date,
			title: session.title,
			question: session.question
		},
		recommendations: buildRecommendations(session, organizations),
		modelTracks,
		revisions: modelTracks.flatMap((track) =>
			track.rows.filter((row) => row.changed).map((row) => ({ model: track.label, ...row }))
		),
		correction: session.correction_notice ?? null,
		dissent: session.dissent_md,
		dissentHighlights: normalizeHighlights(session.dissent_highlights),
		costs: session.costs,
		wartDossier: session.wart_dossier ?? null,
		archive: sessions.map((item) => ({
			...item,
			nonConsensusPillars: (item.recommendations ?? [])
				.filter((recommendation) => !recommendation.has_consensus)
				.map((recommendation) => recommendation.pillar)
		}))
	};
}

export { PILLARS };
