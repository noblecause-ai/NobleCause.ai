// i18n-Grundlage: Deutsch ist Default (unveränderte URLs), Englisch unter /en/…
// gespiegelt. Die Räume bekommen ihre Sprache als Prop (`lang`) und lesen über
// `locales[lang]` — kein stiller Globalimport mehr.
import { de } from './de.js';
import { en } from './en.js';
import { liveCopy } from '../live-council.js';

export const locales = { de, en };

// Historical editions keep their original procedure wording.
export function localeForProcedure(lang, version) {
	const base = locales[lang];
	if (version !== '0.6') return base;
	const copy = liveCopy[lang];
	const english = lang === 'en';
	const flow = base.study.flow.map((step, index) => ({ ...step,
		...(index === 1 ? { text: english ? 'Three Scouts independently research evidence, counterevidence and funding gaps.' : 'Drei Scouts recherchieren unabhängig Belege, Gegenbelege und Finanzierungslücken.' } : {}),
		...(index === 2 ? { name: english ? 'Five initial votes' : 'Fünf Erstvoten', text: english ? 'Five models prepare their initial votes independently; all are then revealed together.' : 'Fünf Modelle erstellen ihre Erstvoten unabhängig; danach werden alle gemeinsam offengelegt.' } : {}),
		...(index === 3 ? { name: english ? 'Discussion' : 'Beratung', text: english ? 'The rotating chair guides the conversation. Each member has two contributions and one final vote.' : 'Der wechselnde Vorsitz führt das Gespräch. Jedes Mitglied hat zwei Sachbeiträge und eine Schlussstimme.' } : {}),
		...(index === 4 ? { text: copy.majorityRule } : {}),
		...(index === 5 ? { text: english ? 'The conversation, votes, sources and costs remain publicly available.' : 'Gespräch, Voten, Quellen und Kosten bleiben öffentlich zugänglich.' } : {})
	}));
	return { ...base,
		common: { ...base.common, heroPitch: copy.intro, whyBody: copy.procedure,
			familyNames: { ...base.common.familyNames, spacexai:'SpaceXAI', moonshotai:'Moonshot AI', 'z-ai':'Z.ai' } },
		study: { ...base.study, flow, actors: { ...base.study.actors,
			warden: { ...base.study.actors.warden, sentence: english ? 'reviews the procedure when consulted. The rotating chair guides Council meetings.' : 'prüft das Verfahren bei Rückfragen. Den Rat leitet sein wechselnder Vorsitz.' } } },
		council: { ...base.council, lead: copy.lead,
			abstentions: n => english ? `${n} abstentions · no recommendation` : `${n} Enthaltungen · keine Empfehlung`,
			actors: { ...base.council.actors, machine: { ...base.council.actors.machine, rule: copy.majorityRule } } }
	};
}

// Die drei Räume in beiden Sprachen. Alle übrigen Routen (sitzungen, journal,
// manifest, idee, impressum) bleiben deutsch-only — sie sind der Rekord.
export const roomPaths = {
	study: { de: '/', en: '/en/' },
	council: { de: '/ratssaal/', en: '/en/council/' },
	archive: { de: '/archiv/', en: '/en/archive/' }
};

// Schwester-Route für den Sprachumschalter: gleicher Raum, andere Sprache.
// null, wenn der Pfad kein Raum ist (dann zeigt das Layout keinen Umschalter).
export function siblingPath(pathname) {
	for (const paths of Object.values(roomPaths)) {
		if (paths.de === pathname) return paths.en;
		if (paths.en === pathname) return paths.de;
	}
	return null;
}

export function langOfPath(pathname) {
	return pathname === '/en' || pathname.startsWith('/en/') ? 'en' : 'de';
}
