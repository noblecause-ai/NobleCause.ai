// English UI copy — kuratierte Übersetzung der deutschen Chrome (de.js).
// Spiegel-Datei: MUSS dieselbe Struktur wie de.js haben (Schlüssel für Schlüssel).
// Raum- und Akteur-Namen bleiben in beiden Sprachen englische Eigennamen (hier ohne Gloss).
// Der publizierte Rekord (Sitzungsprosa, Dissens, Korrekturhinweise, Voten-Texte)
// wird NIEMALS übersetzt — EN-Seiten kennzeichnen ihn über common.recordNote.
// Bild-Pfade (src/img/width/height) sind sprachunabhängig und identisch zu de.js.

// Number words 1–12 (sentence-initial capital); digits above that.
// Keeps the participant count data-driven — the council can grow (x of N from data).
const NUMWORD = [
	'',
	'One',
	'Two',
	'Three',
	'Four',
	'Five',
	'Six',
	'Seven',
	'Eight',
	'Nine',
	'Ten',
	'Eleven',
	'Twelve'
];
const numWord = (n) => (n >= 1 && n <= 12 ? NUMWORD[n] : String(n));

export const en = {
	lang: 'en',
	common: {
		brand: 'NobleCause.ai',
		siteNav: [
			{ href: '/manifest/', label: 'Manifest' },
			{ href: '/idee/', label: 'How a session works' },
			{ href: '/sessions/', label: 'Sessions' },
			{ href: '/journal/', label: "The Warden's journal" }
		],
		moneyFlow:
			'NobleCause does not handle money. Donation links lead directly to the organisations.',
		doorsTitle: 'Doors',
		donate: 'Donate directly (external) ↗',
		noDonate: 'No curated donation channel.',
		ofWord: 'of',
		// Vermerk überall dort, wo deutscher Rekordtext auf einer EN-Seite erscheint.
		recordNote: 'Original protocol in German.',
		// Hinweis, wenn eine Organisationsbeschreibung nur auf Deutsch vorliegt.
		langHint:
			'Organisation description in German — an English translation is being prepared.',
		switchLabel: 'Deutsche Fassung',
		switchTo: 'DE',
		navLabel: 'More sections of the site',
		noSession: 'No session is published at the moment.',
		// Display names of the model families (proper names, identical in both
		// languages). Data carries the family in lower case (“anthropic”); an
		// unknown family falls back to the raw value until a display name is added.
		familyNames: { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' }
	},

	rooms: {
		study: { name: 'The Study', gloss: null },
		council: { name: 'The Council', gloss: null },
		archive: { name: 'The Archive', gloss: null }
	},

	pillars: {
		A: { label: 'Future', src: '/media/pillars/pillar-future-display.jpg' },
		B: { label: 'Relieve suffering', src: '/media/pillars/pillar-relieve-suffering-display.jpg' },
		C: { label: 'Major risks', src: '/media/pillars/pillar-major-risks-display.jpg' },
		D: { label: 'Easily overlooked', src: '/media/pillars/pillar-overlooked-display.jpg' }
	},

	study: {
		eyebrow: 'The Study',
		title: 'Where does my donation help the most?',
		// families: deduplicated family list from the data (joined via Intl.ListFormat).
		lead: (families) =>
			`One AI model each from ${families} reviews the same evidence and publicly recommends where a donation is likely to achieve the most.`,
		boardTitle: "This session's answer",
		flowTitle: 'How it works',
		// The process rail: all six canonical steps as a directed flow.
		// Step 3 carries the participant count from the data (function of n) — the
		// label "Three answers" is deliberately hardcoded (known touchpoint: revisit
		// label + emblem when the council grows).
		flow: [
			{
				name: 'The question',
				text: 'One question per session — four areas, one recommendation each.',
				src: '/media/process/process-question-display.jpg'
			},
			{
				name: 'The evidence',
				text: 'The Scout gathers studies, cost-effectiveness and funding gaps.',
				src: '/media/process/process-evidence-display.jpg'
			},
			{
				name: 'Three answers',
				text: (n) => `${numWord(n)} models answer separately — every vote public.`,
				src: '/media/process/process-three-answers-display.jpg'
			},
			{
				name: 'Second thoughts',
				text: 'They read each other and may change their recommendation.',
				src: '/media/process/process-reconsider-display.jpg'
			},
			{
				name: 'The count',
				text: 'A simple program only counts the mentions.',
				src: '/media/process/process-count-display.jpg'
			},
			{
				name: 'Publication',
				text: 'The Warden publishes everything — recommendations, disagreement, costs.',
				src: '/media/process/process-publish-display.jpg'
			}
		],
		dossiersTitle: 'Dossiers',
		// Visible plain-language context (curated protocol text from the data),
		// with the raw question below as a verbatim quote behind a toggle.
		questionContext: 'What this session was about',
		questionSummary: 'The question — verbatim from the protocol',
		researchSummary: 'Show the research trail',
		researchNote: "The Scout's search queries, verbatim:",
		dossierLink: 'Open the dossier →',
		readProtocol: 'Read in full →',
		head: {
			title: 'NobleCause — Where does my donation help the most?',
			description: (n) =>
				`${numWord(n)} AI models review the same evidence. NobleCause publishes recommendations, changes of mind, disagreement and costs.`
		},
		doors: [
			{
				href: '/en/council/',
				img: '/media/scene-thumbnails/doorway-display.jpg',
				width: 640,
				height: 360,
				sub: 'Through the grand door',
				label: 'The Council',
				alt: 'Opened double doors with a view into the warmly lit council hall'
			},
			{
				href: '/en/archive/',
				img: '/media/doors/door-study-archive-display.jpg',
				width: 480,
				height: 640,
				sub: 'The plain door',
				label: 'The Archive',
				alt: 'Plain wooden door between card catalogues under a wall lamp — to the archive'
			}
		]
	},

	council: {
		eyebrow: 'The Council',
		// Room h1 — the participant count comes from the data (number word, lower case).
		title: (n) => `How ${numWord(n).toLowerCase()} models decide`,
		sessionPrefix: 'Session',
		recTitle: 'Four recommendations',
		noConsensus: 'No agreement yet',
		noConsensusText: 'No two matching mentions.',
		reservation: 'With reservation',
		machineTitle: 'The counting machine',
		machineText: 'The program only counts matching mentions.',
		machineSame: 'matching',
		machineSplit: 'split',
		pulpitsTitle: 'Votes by model — first and after cross-reading',
		allVotes: 'Show all votes',
		initial: 'First',
		final: 'Final',
		noVote: 'no vote',
		readVotes: 'Read the votes →',
		revisionsTitle: 'Changes after cross-reading',
		revisionLead: (count) =>
			count === 1
				? 'After cross-reading, one model changed its recommendation.'
				: `After cross-reading, ${count} models changed their recommendation.`,
		revisionInitial: 'First vote',
		revisionChangedTo: 'changed to',
		head: {
			title: 'NobleCause — The Council',
			description:
				'Four recommendations after public deliberation: tallies, reservations, first and final votes, revisions and direct donation links.'
		},
		doors: [
			{
				href: '/en/',
				img: '/media/scene-thumbnails/antechamber-display.jpg',
				width: 640,
				height: 274,
				sub: 'Back through the door',
				label: 'The Study',
				alt: 'Antechamber with a large slate board, desks and lamps'
			},
			{
				href: '/en/archive/',
				img: '/media/doors/door-council-archive-display.jpg',
				width: 480,
				height: 640,
				sub: 'The plain door',
				label: 'The Archive',
				alt: 'Unobtrusive side door between dark stone columns with a narrow gap of light — to the archive'
			}
		]
	},

	archive: {
		eyebrow: 'The Archive',
		title: 'The Archive',
		sessionsTitle: 'Session archive',
		sessionLabel: (number) => `Session ${number}`,
		allAreas: 'Recommendations in all areas',
		dissentIn: (areas) => `No agreement yet: ${areas}`,
		costsTitle: 'Costs',
		costsLead: (total) => `Cost of this session: ${total}.`,
		costsModel: 'Model',
		costsAmount: 'Cost',
		correctionTitle: 'Correction notice',
		dissentTitle: 'No agreement yet',
		dissentHighlightsTitle: 'Excerpt from the protocol',
		dissentFull: 'Full text',
		protocolLink: 'Open the full protocol →',
		protocolNote: 'The full protocol is published in German.',
		head: {
			title: 'NobleCause — The Archive',
			description:
				'Every session fully published: recommendations, verbatim disagreement, correction notices and costs.'
		},
		doors: [
			{
				href: '/en/',
				img: '/media/scene-thumbnails/antechamber-display.jpg',
				width: 640,
				height: 274,
				sub: 'Back',
				label: 'The Study',
				label: 'The Study',
				alt: 'Antechamber with a large slate board, desks and lamps'
			},
			{
				href: '/en/council/',
				img: '/media/scene-thumbnails/hall-display.jpg',
				width: 640,
				height: 360,
				sub: 'Back',
				label: 'The Council',
				label: 'The Council',
				alt: 'Circular council hall with three pulpits and the counting machine at its centre'
			}
		]
	}
};
