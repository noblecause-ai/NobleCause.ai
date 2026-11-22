import { createHash } from 'node:crypto';
import caseContent from '../cases/amf.json' with { type: 'json' };
import english from '../cases/amf.en.json' with { type: 'json' };
import { getModelsRegistry, getOrganizations, getSchedule, getSession } from './content.js';

const sha256 = (text) => createHash('sha256').update(text).digest('hex');

export function getAmfCase(lang = 'de') {
	if (!['de', 'en'].includes(lang)) throw new Error('Unsupported AMF language');
	const session = getSession(caseContent.sessionId);
	if (lang === 'en' && sha256(session.question) !== english.originalQuestionSha256) {
		throw new Error('AMF question translation does not match its original');
	}
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
		const reason = vote.decision === 'abstain' ? vote.abstention_reason : vote.reservation;
		const translated = english.positions[participant.model];
		if (lang === 'en' && (!translated || translated.originalReasonSha256 !== sha256(reason))) {
			throw new Error('AMF statement translation does not match its original');
		}
		return {
			...participant,
			...(lang === 'en' ? { heading: translated.heading, summary: translated.summary,
				reasonTranslation: translated.reason } : caseContent.positions[participant.model]),
			medallion: registry.asset,
			vote,
			initialVote,
			reason,
			protocolHref: '/sitzungen/' + session.id + '/#' + participant.model
		};
	});
	const cards = caseContent.cards.map((card) => {
		if (lang === 'de') return card;
		const translated = english.cards.find((entry) => entry.id === card.id);
		if (!translated || translated.sourceLabels.length !== card.sources.length) {
			throw new Error('Incomplete AMF evidence translation');
		}
		const { sourceLabels, ...content } = translated;
		return { ...card, ...content, sources: card.sources.map((source, i) => ({
			...source, label: sourceLabels[i]
		})) };
	});
	const schedule = getSchedule();
	return {
		...caseContent,
		lang,
		cards,
		...(lang === 'en' ? { evidenceDate: english.evidenceDate, linkCheckDate: english.linkCheckDate } : {}),
		organization,
		voices,
		session: { id: session.id, date: session.date, question: session.question, result, ...(lang === 'en' ? { questionTranslation: english.questionTranslation } : {}) },
		paused: Boolean(schedule?.regular_operation?.session_hold && schedule?.regular_operation?.research_hold)
	};
}
