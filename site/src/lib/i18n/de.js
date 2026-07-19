// Deutsche UI-Texte der drei Räume. Einzige Quelle für Beschriftungen, Alt-Texte
// und Tür-Definitionen — Daten-Namen (Bereichsnamen aus homepage.js, Organisations-
// namen aus der Registry) stehen hier bewusst NICHT, sie kommen aus der Datenschicht.
// Spiegel-Datei: en.js MUSS dieselbe Struktur haben (Schlüssel für Schlüssel).

// Zahlwörter 1–12 (deutsche Konvention, am Satzanfang groß); darüber Ziffern.
// Dient der generischen Teilnehmerzahl — der Council kann wachsen (x von N aus Daten).
const ZAHLWORT = [
	'',
	'Ein',
	'Zwei',
	'Drei',
	'Vier',
	'Fünf',
	'Sechs',
	'Sieben',
	'Acht',
	'Neun',
	'Zehn',
	'Elf',
	'Zwölf'
];
const zahlwort = (n) => (n >= 1 && n <= 12 ? ZAHLWORT[n] : String(n));

export const de = {
	lang: 'de',
	common: {
		brand: 'NobleCause.ai',
		siteNav: [
			{ href: '/manifest/', label: 'Manifest' },
			{ href: '/idee/', label: 'Wie eine Sitzung funktioniert' },
			{ href: '/sessions/', label: 'Sitzungen' },
			{ href: '/journal/', label: 'Journal des Warts' }
		],
		moneyFlow: 'NobleCause nimmt kein Geld an. Spendenlinks führen direkt zu den Organisationen.',
		doorsTitle: 'Türen',
		donate: 'Direkt spenden (extern) ↗',
		noDonate: 'Kein kuratierter Spendenweg.',
		// Trennwort im Zählstand („2 von 3“) — EN: „of“.
		ofWord: 'von',
		// Vermerk bei publiziertem Protokoll — nur im EN-Modus nötig (siehe en.js).
		recordNote: null,
		// Hinweis, wenn eine Organisationsbeschreibung nur auf Deutsch vorliegt.
		langHint: null,
		switchLabel: 'English version',
		switchTo: 'EN',
		navLabel: 'Weitere Bereiche der Seite',
		noSession: 'Derzeit ist keine Sitzung veröffentlicht.',
		// Anzeigenamen der Modellfamilien (Eigennamen, in beiden Sprachen gleich).
		// Die Daten liefern die Familie klein („anthropic“); unbekannte Familien
		// fallen bei einer Council-Erweiterung auf den Rohwert zurück, bis hier
		// ein Anzeigename ergänzt wird.
		familyNames: { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' }
	},

	// Raum- und Akteur-Namen sind in beiden Sprachen englische Eigennamen;
	// der deutsche Gloss erscheint nur hier.
	rooms: {
		study: { name: 'The Study', gloss: 'das Vorzimmer' },
		council: { name: 'The Council', gloss: 'der Ratssaal' },
		archive: { name: 'The Archive', gloss: 'das Archiv' }
	},

	// Die vier Bereiche — Alltagswort (Verfassungssprache) + Emblem.
	pillars: {
		A: { label: 'Zukunft', src: '/media/pillars/pillar-future-display.jpg' },
		B: { label: 'Leid lindern', src: '/media/pillars/pillar-relieve-suffering-display.jpg' },
		C: { label: 'Große Gefahren', src: '/media/pillars/pillar-major-risks-display.jpg' },
		D: { label: 'Was sonst übersehen wird', src: '/media/pillars/pillar-overlooked-display.jpg' }
	},

	study: {
		eyebrow: 'The Study · das Vorzimmer',
		title: 'Wo hilft meine Spende am meisten?',
		// families: deduplizierte Familienliste aus den Daten (Intl.ListFormat-gejoint).
		lead: (families) =>
			`Je ein KI-Modell der Familien ${families} prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.`,
		boardTitle: 'Die Antwort dieser Sitzung',
		flowTitle: 'So läuft es',
		// Die Ablauf-Leiste: alle sechs kanonischen Schritte als gerichteter Prozess.
		// Schritt 3 trägt die Teilnehmerzahl aus den Daten (Funktion von n) — das Label
		// „Drei Antworten" ist bewusst hartkodiert (bekannter Touchpoint: bei einer
		// Council-Erweiterung Label + Emblem inhaltlich neu fassen).
		flow: [
			{
				name: 'Die Frage',
				text: 'Eine Frage pro Sitzung — vier Bereiche, je eine Empfehlung.',
				src: '/media/process/process-question-display.jpg'
			},
			{
				name: 'Die Belege',
				text: 'Der Späher sammelt Studien, Kosten-Wirksamkeit und Finanzierungslücken.',
				src: '/media/process/process-evidence-display.jpg'
			},
			{
				name: 'Drei Antworten',
				text: (n) => `${zahlwort(n)} Modelle antworten getrennt — jedes Votum öffentlich.`,
				src: '/media/process/process-three-answers-display.jpg'
			},
			{
				name: 'Umdenken',
				text: 'Sie lesen einander und dürfen ihre Empfehlung ändern.',
				src: '/media/process/process-reconsider-display.jpg'
			},
			{
				name: 'Zählen',
				text: 'Ein einfaches Programm zählt nur die Nennungen.',
				src: '/media/process/process-count-display.jpg'
			},
			{
				name: 'Veröffentlichen',
				text: 'Der Wart veröffentlicht alles — Empfehlungen, Uneinigkeit, Kosten.',
				src: '/media/process/process-publish-display.jpg'
			}
		],
		dossiersTitle: 'Dossiers',
		// Sichtbarer Klartext-Kontext (kuratierter Protokolltext aus den Daten),
		// darunter die rohe Frage als Zitat-Beleg hinter Ausklapp.
		questionContext: 'Worum es ging',
		questionSummary: 'Frage wörtlich aus dem Protokoll',
		researchSummary: 'Recherche zeigen',
		researchNote: 'Suchanfragen des Spähers, wörtlich:',
		dossierLink: 'Dossier öffnen →',
		readProtocol: 'Vollständig lesen →',
		head: {
			title: 'NobleCause — Wo hilft meine Spende am meisten?',
			description: (n) =>
				`${zahlwort(n)} KI-Modelle prüfen dieselben Belege. NobleCause veröffentlicht Empfehlungen, Änderungen, Uneinigkeit und Kosten.`
		},
		doors: [
			{
				href: '/ratssaal/',
				img: '/media/scene-thumbnails/doorway-display.jpg',
				width: 640,
				height: 360,
				sub: 'Durch die große Tür',
				label: 'The Council',
				alt: 'Geöffnete zweiflügelige Tür mit Blick in den warm erleuchteten Ratssaal'
			},
			{
				href: '/archiv/',
				img: '/media/doors/door-study-archive-display.jpg',
				width: 480,
				height: 640,
				sub: 'Die schlichte Tür',
				label: 'The Archive',
				alt: 'Schlichte Holztür zwischen Karteischränken unter einem Wandlämpchen — zum Archiv'
			}
		]
	},

	council: {
		eyebrow: 'The Council · der Ratssaal',
		// h1 des Raums — die Teilnehmerzahl kommt aus den Daten (Zahlwort im Satz klein).
		title: (n) => `Wie ${zahlwort(n).toLowerCase()} Modelle entscheiden`,
		sessionPrefix: 'Sitzung',
		recTitle: 'Vier Empfehlungen',
		noConsensus: 'Noch keine Einigkeit',
		noConsensusText: 'Keine zwei gleichen Nennungen.',
		reservation: 'Unter Vorbehalt',
		machineTitle: 'Zählwerk',
		machineText: 'Das Programm zählt nur gleiche Nennungen.',
		machineSame: 'gleich',
		machineSplit: 'getrennt',
		pulpitsTitle: 'Voten je Modell — erst und nach dem Gegenlesen',
		allVotes: 'Alle Voten zeigen',
		initial: 'Erst',
		final: 'Schluss',
		noVote: 'kein Votum',
		readVotes: 'Voten lesen →',
		revisionsTitle: 'Änderungen nach dem Gegenlesen',
		revisionLead: (count) =>
			count === 1
				? 'Nach dem Gegenlesen änderte ein Modell seine Empfehlung.'
				: `Nach dem Gegenlesen änderten ${count} Modelle ihre Empfehlung.`,
		revisionInitial: 'Erstvotum',
		revisionChangedTo: 'geändert zu',
		head: {
			title: 'NobleCause — The Council',
			description:
				'Vier Empfehlungen nach öffentlicher Beratung: Zählstände, Vorbehalte, Erst- und Schlussvoten, Revisionen und direkte Spendenlinks.'
		},
		doors: [
			{
				href: '/',
				img: '/media/scene-thumbnails/antechamber-display.jpg',
				width: 640,
				height: 274,
				sub: 'Zurück durch die Tür',
				label: 'The Study',
				alt: 'Vorzimmer mit großer Schiefertafel, Schreibtischen und Lampen'
			},
			{
				href: '/archiv/',
				img: '/media/doors/door-council-archive-display.jpg',
				width: 480,
				height: 640,
				sub: 'Die schlichte Tür',
				label: 'The Archive',
				alt: 'Unauffällige Seitentür zwischen dunklen Steinsäulen mit schmaler Lichtfuge — zum Archiv'
			}
		]
	},

	archive: {
		eyebrow: 'The Archive · das Archiv',
		title: 'The Archive',
		sessionsTitle: 'Sitzungsarchiv',
		sessionLabel: (number) => `Sitzung ${number}`,
		allAreas: 'Empfehlungen in allen Bereichen',
		dissentIn: (areas) => `Noch keine Einigkeit: ${areas}`,
		costsTitle: 'Kosten',
		costsLead: (total) => `Kosten dieser Sitzung: ${total}.`,
		costsModel: 'Modell',
		costsAmount: 'Kosten',
		correctionTitle: 'Korrekturhinweis',
		dissentTitle: 'Noch keine Einigkeit',
		dissentHighlightsTitle: 'Auszug aus dem Protokoll',
		dissentFull: 'Vollständiger Wortlaut',
		protocolLink: 'Vollständiges Protokoll öffnen →',
		protocolNote: null,
		head: {
			title: 'NobleCause — The Archive',
			description:
				'Alle Sitzungen vollständig veröffentlicht: Empfehlungen, Uneinigkeit im Wortlaut, Korrekturhinweise und Kosten.'
		},
		doors: [
			{
				href: '/',
				img: '/media/scene-thumbnails/antechamber-display.jpg',
				width: 640,
				height: 274,
				sub: 'Zurück',
				label: 'The Study',
				alt: 'Vorzimmer mit großer Schiefertafel, Schreibtischen und Lampen'
			},
			{
				href: '/ratssaal/',
				img: '/media/scene-thumbnails/hall-display.jpg',
				width: 640,
				height: 360,
				sub: 'Zurück',
				label: 'The Council',
				alt: 'Kreisrunder Ratssaal mit drei Pulten und der Zählmaschine in der Mitte'
			}
		]
	}
};
