import caseContent from '../cases/amf.json' with { type: 'json' };
import { getModelsRegistry, getOrganizations, getSchedule, getSession } from './content.js';

export function getAmfCase() {
	const session = getSession(caseContent.sessionId);
	const organizations = getOrganizations().organizations;
	const organization = organizations.find((entry) => entry.id === caseContent.organizationId);
	if (!organization) throw new Error('AMF fehlt in der Organisationsregistratur');
	const models = getModelsRegistry();
	const final = session.rounds.find((round) => round.kind === 'final_vote');
	const initial = session.rounds.find((round) => round.kind === 'initial_vote');
	const result = session.recommendations.find((entry) => entry.pillar === 'B');
	const voices = session.participants.map((participant) => {
		const ballot = final.votes.find((vote) => vote.model === participant.model);
		const before = initial.votes.find((vote) => vote.model === participant.model);
		const vote = ballot.recommendations.find((entry) => entry.pillar === 'B');
		const initialVote = before.recommendations.find((entry) => entry.pillar === 'B');
		const registry = models.get(participant.model);
		if (!registry?.asset || !caseContent.positions[participant.model]) {
			throw new Error('AMF-Fall benötigt die dokumentierten fünf Sitzinhaber');
		}
		return {
			...participant,
			...caseContent.positions[participant.model],
			medallion: registry.asset,
			vote,
			initialVote,
			reason: vote.decision === 'abstain' ? vote.abstention_reason : vote.reservation,
			protocolHref: '/sitzungen/' + session.id + '/#' + participant.model
		};
	});
	const schedule = getSchedule();
	return {
		...caseContent,
		organization,
		voices,
		session: { id: session.id, date: session.date, question: session.question, result },
		paused: Boolean(schedule?.regular_operation?.session_hold && schedule?.regular_operation?.research_hold)
	};
}
