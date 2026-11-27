// Editorial website copy, separate from the verbatim council record.
export const studyCopy = {
	de: {
		skip: 'Zum Inhalt',
		caseEyebrow: 'Offene Fallstudie · Deutsch und Englisch',
		caseTitle: 'Geprüfte Fallstudie: Malariaschutz durch AMF',
		caseRecommendation: 'Empfehlung und Grenzen der Belege verstehen.',
		casePositions: (count) => `${count} dokumentierte Modellpositionen vergleichen.`,
		caseEvidence: (count) => `${count} datierte Belegkarten mit Originalquellen prüfen.`,
		openCase: 'AMF-Fallstudie öffnen',
		caseRouteLabel: 'Die Frage im Fall',
		casePrompt: 'AMF wird empfohlen. Was trägt die Empfehlung – und was bleibt für zusätzliches Geld offen?',
		statusLabel: 'Betriebsstatus',
		pilot: 'Pilotstand',
		bothPaused: 'Aktive Rats- und Rechercheläufe sind derzeit pausiert.',
		councilPaused: 'Aktive Ratsläufe sind derzeit pausiert.',
		researchPaused: 'Automatische Rechercheläufe sind derzeit pausiert.',
		notPaused: 'Rats- und Rechercheläufe sind nicht pausiert.',
		openRecords: (count) => `Alle ${count} Sitzungsprotokolle und die AMF-Fallstudie bleiben vollständig als offene Arbeitsprobe zugänglich.`,
		methodEyebrow: 'Nachvollziehbar vom Beleg bis zur Veröffentlichung',
		architectureTitle: 'Architektur & Verfahren',
		methods: [
			{
				title: 'Fünf Modelle, eine Regel',
				body: 'Unabhängige Erstvoten, gemeinsame Beratung, danach Schlussvoten. Eine Empfehlung braucht 3 von 5 Schlussstimmen. Enthaltungen verkleinern den Nenner nicht.',
				href: '/ratssaal/', link: 'Voten und Entscheidungsregel'
			},
			{
				title: 'Versionierte, prüfbare Records',
				body: 'JSON-Records in Git, ein Schema-Gate vor der Veröffentlichung und SHA-256-gesicherte Ereignisse. Der Python-Ablauf kann nach Abbrüchen wiederaufgenommen werden.',
				href: 'https://github.com/noblecause-ai/NobleCause.ai/tree/master/gremium', link: 'Ablauf und Prüfungen im Code'
			},
			{
				title: 'Offener Code, direkte Wege',
				body: 'SvelteKit liefert statische Seiten. Code und Protokolle sind offen; NobleCause nimmt keine Spenden an. Spendenlinks führen direkt zu den Organisationen.',
				href: 'https://github.com/noblecause-ai/NobleCause.ai', link: 'Open-Source-Repository'
			}
		],
		lastSessionLabel: 'Ergebnis der letzten Sitzung',
		readSession: 'Vollständiges Sitzungsprotokoll',
		voteDetails: 'Begründungen und Einzelstimmen im Wortlaut ▸',
		dossiersSummary: 'Dossiers: Sitzungsfrage und Recherchegrundlage ▸',
		verbatimQuestion: 'Die Frage im Wortlaut',
		searchQueries: 'Suchanfragen des Spähers',
		onwardTitle: 'Das Projekt weiter erkunden',
		navigation: [
			{ title: 'The Council', description: 'Modelle, Voten und die gemeinsame Entscheidungsregel.', href: '/ratssaal/' },
			{ title: 'The Archive', description: 'Alle Sitzungen mit Protokollen, Quellen und Kosten.', href: '/archiv/' },
			{ title: 'Manifest', description: 'Die Ziele und Grundsätze hinter NobleCause.', href: '/manifest/' },
			{ title: 'GitHub-Repository', description: 'Quellcode, Daten und Prüfungen offen nachlesen.', href: 'https://github.com/noblecause-ai/NobleCause.ai' }
		]
	},
	en: {
		skip: 'Skip to content',
		caseEyebrow: 'Open case study · English and German',
		caseTitle: 'Reviewed Case Study: Malaria protection with AMF',
		caseRecommendation: 'Understand the recommendation and the limits of its evidence.',
		casePositions: (count) => `Compare ${count} documented model positions.`,
		caseEvidence: (count) => `Check ${count} dated evidence cards with links to original sources.`,
		openCase: 'Open the AMF case study',
		caseRouteLabel: 'The question in this case',
		casePrompt: 'AMF is recommended. What supports the recommendation – and what remains open for additional funding?',
		statusLabel: 'Operating status',
		pilot: 'Pilot release',
		bothPaused: 'Automated council and research runs are currently paused.',
		councilPaused: 'Automated council runs are currently paused.',
		researchPaused: 'Automated research runs are currently paused.',
		notPaused: 'Council and research runs are not paused.',
		openRecords: (count) => `All ${count} session records and the AMF case study remain publicly accessible.`,
		methodEyebrow: 'Traceable from evidence to publication',
		architectureTitle: 'Architecture & procedure',
		methods: [
			{
				title: 'Five models, one rule',
				body: 'Independent initial votes, a shared discussion, then final votes. A recommendation needs 3 of 5 final votes. Abstentions do not reduce the denominator.',
				href: '/en/council/', link: 'Votes and decision rule'
			},
			{
				title: 'Versioned, verifiable records',
				body: 'JSON records in Git, a schema gate before publication and SHA-256-protected events. The Python workflow can resume after interruptions.',
				href: 'https://github.com/noblecause-ai/NobleCause.ai/tree/master/gremium', link: 'Workflow and checks in the code'
			},
			{
				title: 'Open code, direct links',
				body: 'SvelteKit serves static pages. Code and records are open; NobleCause does not accept donations. Donation links go directly to the organisations.',
				href: 'https://github.com/noblecause-ai/NobleCause.ai', link: 'Open-source repository'
			}
		],
		lastSessionLabel: 'Last session result',
		readSession: 'Read the full session record',
		voteDetails: 'Reasoning and individual votes, verbatim ▸',
		dossiersSummary: 'Dossiers: session question and research basis ▸',
		verbatimQuestion: 'The question verbatim',
		searchQueries: 'The Scout’s search queries',
		onwardTitle: 'Explore the project',
		navigation: [
			{ title: 'The Council', description: 'Models, votes and the shared decision rule.', href: '/en/council/' },
			{ title: 'The Archive', description: 'Every session, with records, sources and costs.', href: '/en/archive/' },
			{ title: 'Manifest', description: 'The goals and principles behind NobleCause. German reading version and English original.', href: '/manifest/' },
			{ title: 'GitHub repository', description: 'Inspect the source code, data and checks.', href: 'https://github.com/noblecause-ai/NobleCause.ai' }
		]
	}
};
