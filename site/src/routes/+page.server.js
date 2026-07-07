import { getLatestSession, getSchedule, listSessions } from '$lib/server/content.js';

function formatStaticCountdown(iso) {
	if (!iso) return null;
	const target = new Date(iso);
	const now = new Date();
	const diff = target - now;
	if (diff <= 0) return 'bald';
	const days = Math.floor(diff / 86400000);
	const hours = Math.floor((diff % 86400000) / 3600000);
	if (days > 0) return `in ${days} T ${hours} h`;
	return `in ${hours} h`;
}

export function load() {
	const latest = getLatestSession();
	const schedule = getSchedule();
	return {
		sessions: listSessions(),
		schedule,
		scheduleStatic: schedule
			? {
					research: formatStaticCountdown(schedule.next_research),
					session: formatStaticCountdown(schedule.next_session),
					researchDate: schedule.next_research
						? new Date(schedule.next_research).toLocaleDateString('de-CH')
						: null,
					sessionDate: schedule.next_session
						? new Date(schedule.next_session).toLocaleDateString('de-CH')
						: null
				}
			: null,
		latest: latest
			? {
					id: latest.id,
					number: latest.number,
					date: latest.date,
					title: latest.title,
					summary: latest.summary ?? null,
					recommendations: latest.recommendations ?? []
				}
			: null
	};
}
