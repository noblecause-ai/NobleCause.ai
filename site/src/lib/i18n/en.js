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
		// Kennzeichnung der Klartext-Schicht (§1): sie IST die summary-Zeile des
		// Ausklapps zum Rats-Wortlaut, kein separater Disclaimer. Die Frage trägt
		// eine eigene Variante (study.questionKlartextNote).
		klartextNote: "Simplified version, approved by the Warden · The council's wording ▸",
		// Fehlt die Freigabe des Klartexts, erscheint die Rekord-Schicht mit
		// diesem Vermerk — Verständlichkeit darf die Publikation nie verhindern.
		klartextPending: "Plain-language version pending — the council's wording is shown until approval.",
		// Stable head on ALL three room pages (title reorder): the core question
		// as h1, below it the process sentence (pitch) in the same font/color —
		// "Why so elaborate?" is the inline continuation of the same sentence.
		// Deliberately no family names and no number: "different families"
		// survives council growth.
		heroTitle: 'Where does my donation help the most?',
		heroPitch:
			'One AI model each from different families reviews the same evidence and publicly recommends where a donation is likely to achieve the most.',
		whySummary: 'Why so elaborate? ▸',
		whyBody:
			'A single model can be wrong or have a blind spot. That is why several independent models judge the same evidence separately, read each other, and a simple program only counts what they agree on — everything is published, including the disagreement. The more independent voices take part in the decision, the more robust the recommendation. The Scout runs weekly, the Council meets as needed — between the runs, no human decides.',
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
		familyNames: { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' },
		// Model designation + version of the current seat-holder (proper names, same
		// in both languages). Key = participant.model (like the medallion filename);
		// unknown models fall back to the short label.
		modelNames: {
			'claude-opus-4-8': 'Claude Opus 4.8',
			'gpt-5.2': 'GPT-5.2',
			'gemini-2.5-pro': 'Gemini 2.5 Pro'
		}
	},

	rooms: {
		study: { name: 'The Study', gloss: null },
		council: { name: 'The Council', gloss: null },
		archive: { name: 'The Archive', gloss: null }
	},

	pillars: {
		A: { label: 'Future', src: '/media/pillars/pillar-future-display.avif' },
		B: { label: 'Relieve suffering', src: '/media/pillars/pillar-relieve-suffering-display.avif' },
		C: { label: 'Major risks', src: '/media/pillars/pillar-major-risks-display.avif' },
		D: { label: 'Easily overlooked', src: '/media/pillars/pillar-overlooked-display.avif' }
	},

	// Process tube (StageTube): accessible name and screenreader status.
	// Fill level comes from the route (Study 2, Council 5, Archive 6), step
	// content from study.flow — this is only the chrome.
	tube: {
		label: 'Process state',
		status: (n, total) => `Step ${n} of ${total} reached`
	},

	study: {
		// Dynamic room part below the stable head (title reorder): ONE word
		// (English proper name, no "The"/gloss) + room lead.
		roomWord: 'Study',
		lead: 'Every session begins here — with a question and the evidence for it.',
		boardTitle: "The last session's answer",
		// Data line under the board title: the number MUST be present — all three
		// sessions carry the same date, a date alone would be ambiguous.
		boardSession: (number) => `Session ${number}`,
		// Time layer line under the tube (Study): rhythm + last recorded run +
		// manifesto. The date lives in the rhythm (next Monday), not in
		// schedule.json — so it can never be overdue.
		rhythm: 'The Scout runs every Monday morning, 06:00 UTC.',
		lastCheck: (dateStr) => `Last check: ${dateStr}.`,
		manifestLead: 'The domains and canons:',
		manifestLink: 'The Manifesto ▸',
		// §3.3: the reading version of the board — same emblems and order
		// (visual rhyme); it explains the board, it does not repeat it.
		answerTitle: "This session's recommendations",
		// Actors of the second layer (StudyActors): English proper nouns (no gloss).
		// The seat-holder (model) comes from the data, not the copy. The four domain
		// emblems sit as a row under the Scout's sentence (not inside the sentence).
		actors: {
			sitzPrefix: 'Currently:',
			deputyPrefix: 'Standing in:',
			scout: {
				name: 'The Scout',
				sentence:
					'seeks the most effective organisations for the good of humanity — across four domains.'
			},
			warden: {
				name: 'The Warden',
				sentence:
					'decides, from the evidence, whether the Council meets, then chairs the session and publishes everything.',
				lastPrefix: 'Last:',
				convened: 'convened',
				notConvened: 'not convened'
			}
		},
		// The process rail: all six canonical steps as a directed flow.
		// Step 3 carries the participant count from the data (function of n) — the
		// label "Three answers" is deliberately hardcoded (known touchpoint: revisit
		// label + emblem when the council grows).
		flow: [
			{
				name: 'The question',
				text: 'One question per session — four areas, one recommendation each.',
				src: '/media/process/process-question-display.avif'
			},
			{
				name: 'The evidence',
				text: 'The Scout gathers studies, cost-effectiveness and funding gaps.',
				src: '/media/process/process-evidence-display.avif'
			},
			{
				name: 'Three answers',
				text: (n) => `${numWord(n)} models answer separately — every vote public.`,
				src: '/media/process/process-three-answers-display.webp'
			},
			{
				name: 'Second thoughts',
				text: 'They read each other and may change their recommendation.',
				src: '/media/process/process-reconsider-display.avif'
			},
			{
				name: 'The count',
				text: 'A simple program only counts the mentions.',
				src: '/media/process/process-count-display.avif'
			},
			{
				name: 'Publication',
				text: 'The Warden publishes everything — recommendations, disagreement, costs.',
				src: '/media/process/process-publish-display.avif'
			}
		],
		dossiersTitle: 'Dossiers',
		// §3.4: The dossier block opens with this session's question in plain
		// language (plain.question from the data; fallback: the curated protocol
		// context session.summary + "plain text pending"). The verbatim question
		// hangs on the designation summary (one level, rule 2.1).
		questionTitle: "This session's question",
		questionKlartextNote:
			'Simplified version, approved by the Warden · The question verbatim ▸',
		researchSummary: "The Scout's search queries ▸",
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
				img: '/media/scene-thumbnails/doorway-display.avif',
				width: 640,
				height: 360,
				sub: 'Through the grand door',
				label: 'The Council',
				alt: 'Opened double doors with a view into the warmly lit council hall'
			},
			{
				href: '/en/archive/',
				img: '/media/doors/door-study-archive-display.avif',
				width: 480,
				height: 640,
				sub: 'The plain door',
				label: 'The Archive',
				alt: 'Plain wooden door between card catalogues under a wall lamp — to the archive'
			}
		]
	},

	council: {
		roomWord: 'Council',
		lead: 'Voted separately, then counted publicly. What is named multiple times becomes a recommendation.',
		// Time layer line under the tube (Council): session cadence as a plan. Date
		// from schedule.next_session; a past date is dropped client-side.
		rhythm: 'The Council meets when enough is new.',
		nextSession: (dateStr) => `Per the schedule: ${dateStr}.`,
		// Second layer (CouncilActors): the lecterns carry the participants from
		// the data (label/family) — i18n only provides the role, mirroring
		// process step 3 ("… answer separately — every vote public").
		actors: {
			pult: {
				role: 'answers separately — every vote public.'
			},
			// The counting machine (§8): the plaque states the aggregation rule —
			// a process statement, not a result (the data seam stays sealed).
			machine: {
				rule: 'Two matching mentions make a recommendation.'
			}
		},
		// §4.2 "How the votes were counted" — one block replaces three
		// (recommendations / revisions / counting machine). Revisions live inside
		// the model mark itself (first vote struck through, final vote below);
		// the tally slot says "split" instead of "x of N" when there is no match.
		countTitle: 'How the votes were counted',
		countIntro: 'The program only counts matching mentions.',
		countSplit: 'split',
		noConsensus: 'No agreement yet',
		reservation: 'Reservation ▸',
		allVotesVerbatim: 'All votes, verbatim ▸',
		initial: 'First',
		final: 'Final',
		noVote: 'no vote',
		readVotes: 'Read the votes →',
		head: {
			title: 'NobleCause — The Council',
			description:
				'How the recommendations come about: mentions by model, tallies, reservations, first and final votes verbatim and direct donation links.'
		},
		doors: [
			{
				href: '/en/',
				img: '/media/scene-thumbnails/antechamber-display.avif',
				width: 640,
				height: 274,
				sub: 'Back through the door',
				label: 'The Study',
				alt: 'Antechamber with a large slate board, desks and lamps'
			},
			{
				href: '/en/archive/',
				img: '/media/doors/door-council-archive-display.avif',
				width: 480,
				height: 640,
				sub: 'The plain door',
				label: 'The Archive',
				alt: 'Unobtrusive side door between dark stone columns with a narrow gap of light — to the archive'
			}
		]
	},

	archive: {
		roomWord: 'Archive',
		lead: 'Every session, complete and unchanged — recommendations, disagreement, costs.',
		// Alt text for the furniture (second layer): pure scenery, no data.
		pultAlt: 'Archive desk with a reading lamp and an open folio',
		sessionsTitle: 'Session archive',
		sessionLabel: (number) => `Session ${number}`,
		// Chip marker of an open area in the session row (§5.2).
		noConsensusNote: 'no agreement',
		costsTitle: 'Costs',
		costsLead: (total) => `Cost of this session: ${total}.`,
		costsModel: 'Model',
		costsAmount: 'Cost',
		correctionTitle: 'Correction notice',
		dissentTitle: 'No agreement yet',
		dissentFull: "The council's wording ▸",
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
				img: '/media/scene-thumbnails/antechamber-display.avif',
				width: 640,
				height: 274,
				sub: 'Back',
				label: 'The Study',
				label: 'The Study',
				alt: 'Antechamber with a large slate board, desks and lamps'
			},
			{
				href: '/en/council/',
				img: '/media/scene-thumbnails/hall-display.avif',
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
