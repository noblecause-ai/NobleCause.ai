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
			{ href: '/sitzungen/', label: 'Sitzungen' },
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
		// Kennzeichnung der Klartext-Schicht (§1): sie IST die summary-Zeile des
		// Ausklapps zum Rats-Wortlaut, kein separater Disclaimer. Die Frage trägt
		// eine eigene Variante (study.questionKlartextNote).
		klartextNote: 'Vereinfachte Fassung, verantwortet vom Wart · Wortlaut des Rates ▸',
		// Fehlt die Freigabe des Klartexts, erscheint die Rekord-Schicht mit
		// diesem Vermerk — Verständlichkeit darf die Publikation nie verhindern.
		klartextPending: 'Klartext folgt — bis zur Freigabe steht hier der Wortlaut des Rates.',
		// Stabiler Kopf auf ALLEN drei Raum-Seiten (Titelbereich-Neuordnung):
		// die Leitfrage als h1, darunter der Verfahrenssatz (Pitch) in derselben
		// Schrift/Farbe — „Warum so umständlich?" ist die inline-Fortsetzung
		// desselben Satzes. Bewusst ohne Familiennamen und ohne Zahl:
		// „verschiedener Familien" hält die Council-Erweiterung aus.
		heroTitle: 'Wo hilft meine Spende am meisten?',
		heroPitch:
			'Je ein KI-Modell verschiedener Familien prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.',
		// Count-agnostisch („mehrere", „je mehr") — rahmt Wachstum als Gewinn.
		whySummary: 'Warum so umständlich? ▸',
		whyBody:
			'Ein einzelnes Modell kann irren oder eine blinde Stelle haben. Deshalb urteilen mehrere unabhängige Modelle getrennt über dieselben Belege, lesen einander, und ein einfaches Programm zählt nur, worauf sie sich einigen — veröffentlicht wird alles, auch die Uneinigkeit. Je mehr unabhängige Stimmen mitentscheiden, desto belastbarer die Empfehlung. Der Scout läuft wöchentlich, der Council tagt nach festem Rhythmus — und früher, wenn der Wart aus den Belegen genug Neues sieht. Zwischen den Läufen entscheidet kein Mensch.',
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
		familyNames: { anthropic: 'Anthropic', openai: 'OpenAI', google: 'Google' },
		// Modellbezeichnung + Version des aktuellen Sitzinhabers (Eigennamen, in
		// beiden Sprachen gleich). Schlüssel = participant.model (wie der Medaillon-
		// Dateiname); unbekannte Modelle fallen auf das Kurz-Label zurück.
		modelNames: {
			'claude-opus-4-8': 'Claude Opus 4.8',
			'gpt-5.2': 'GPT-5.2',
			'gemini-2.5-pro': 'Gemini 2.5 Pro'
		}
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
		A: { label: 'Zukunft', src: '/media/pillars/pillar-future-display.avif' },
		B: { label: 'Leid lindern', src: '/media/pillars/pillar-relieve-suffering-display.avif' },
		C: { label: 'Große Gefahren', src: '/media/pillars/pillar-major-risks-display.avif' },
		D: { label: 'Was sonst übersehen wird', src: '/media/pillars/pillar-overlooked-display.avif' }
	},

	// Prozess-Röhre (StageTube): Name und Screenreader-Status des Instruments.
	// Füllstand kommt aus der Route (Study 2, Council 5, Archive 6), die
	// Schritt-Inhalte aus study.flow — hier steht nur die Chrome.
	tube: {
		label: 'Verfahrensstand',
		status: (n, total) => `Schritt ${n} von ${total} erreicht`
	},

	study: {
		// Dynamischer Raumteil unter dem stabilen Kopf (Titelbereich-Neuordnung):
		// EIN Wort (englischer Eigenname, ohne „The"/Gloss) + Raum-Lead.
		roomWord: 'Study',
		lead: 'Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu.',
		boardTitle: 'Die Antwort der letzten Sitzung',
		// Datenzeile unter dem Tafeltitel: Nummer MUSS mit — alle drei Sitzungen
		// tragen dasselbe Datum, ein Datum allein wäre mehrdeutig.
		boardSession: (number) => `Sitzung ${number}`,
		// Zeitschicht-Zeile unter der Röhre (Study): Rhythmus + letzter belegter
		// Lauf + Manifest. Der Termin lebt im Rhythmus (nächster Montag), nicht in
		// schedule.json — kann so nie überfällig sein.
		rhythm: 'Der Scout läuft jeden Montagmorgen, 06:00 UTC.',
		lastCheck: (dateStr) => `Letzte Prüfung: ${dateStr}.`,
		manifestLead: 'Die Bereiche und Kanons:',
		manifestLink: 'Das Manifest ▸',
		// §3.3: die Lese-Fassung der Tafel — gleiche Embleme und Reihenfolge
		// (visueller Reim), begründet die Tafel, wiederholt sie nicht.
		answerTitle: 'Die Empfehlungen dieser Sitzung',
		// Akteure der zweiten Ebene (StudyActors): englische Eigennamen (kein Gloss).
		// Der Sitzinhaber (Modell) kommt aus den Daten, nicht aus der Copy. Die vier
		// Bereichsembleme stehen als Reihe unter dem Scout-Satz (nicht im Satz).
		actors: {
			sitzPrefix: 'Aktuell:',
			deputyPrefix: 'In Vertretung:',
			scout: {
				name: 'The Scout',
				sentence:
					'sucht die wirksamsten Organisationen fürs Wohl der Menschheit — in vier Bereichen.'
			},
			warden: {
				name: 'The Warden',
				sentence:
					'entscheidet anhand der Belege, ob der Council tagt, leitet dann die Sitzung und veröffentlicht alles.',
				lastPrefix: 'Zuletzt:',
				convened: 'einberufen',
				notConvened: 'nicht einberufen'
			}
		},
		// Die Ablauf-Leiste: alle sechs kanonischen Schritte als gerichteter Prozess.
		// Schritt 3 trägt die Teilnehmerzahl aus den Daten (Funktion von n) — das Label
		// „Drei Antworten" ist bewusst hartkodiert (bekannter Touchpoint: bei einer
		// Council-Erweiterung Label + Emblem inhaltlich neu fassen).
		flow: [
			{
				name: 'Die Frage',
				text: 'Eine Frage pro Sitzung — vier Bereiche, je eine Empfehlung.',
				src: '/media/process/process-question-display.avif'
			},
			{
				name: 'Die Belege',
				text: 'Der Späher sammelt Studien, Kosten-Wirksamkeit und Finanzierungslücken.',
				src: '/media/process/process-evidence-display.avif'
			},
			{
				name: 'Drei Antworten',
				text: (n) => `${zahlwort(n)} Modelle antworten getrennt — jedes Votum öffentlich.`,
				src: '/media/process/process-three-answers-display.webp'
			},
			{
				name: 'Umdenken',
				text: 'Sie lesen einander und dürfen ihre Empfehlung ändern.',
				src: '/media/process/process-reconsider-display.avif'
			},
			{
				name: 'Zählen',
				text: 'Ein einfaches Programm zählt nur die Nennungen.',
				src: '/media/process/process-count-display.avif'
			},
			{
				name: 'Veröffentlichen',
				text: 'Der Wart veröffentlicht alles — Empfehlungen, Uneinigkeit, Kosten.',
				src: '/media/process/process-publish-display.avif'
			}
		],
		dossiersTitle: 'Dossiers',
		// §3.4: Der Dossier-Block öffnet mit der Frage dieser Sitzung in Klartext
		// (plain.question aus den Daten; Fallback: der kuratierte Protokoll-
		// Kontext session.summary + „Klartext folgt"). Der Wortlaut hängt an der
		// Kennzeichnungs-Summary (eine Tiefe, Regel 2.1).
		questionTitle: 'Die Frage dieser Sitzung',
		questionKlartextNote: 'Vereinfachte Fassung, verantwortet vom Wart · Die Frage im Wortlaut ▸',
		researchSummary: 'Suchanfragen des Spähers ▸',
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
				img: '/media/scene-thumbnails/doorway-display.avif',
				width: 640,
				height: 360,
				sub: 'Durch die große Tür',
				label: 'The Council',
				alt: 'Geöffnete zweiflügelige Tür mit Blick in den warm erleuchteten Ratssaal'
			},
			{
				href: '/archiv/',
				img: '/media/doors/door-study-archive-display.avif',
				width: 480,
				height: 640,
				sub: 'Die schlichte Tür',
				label: 'The Archive',
				alt: 'Schlichte Holztür zwischen Karteischränken unter einem Wandlämpchen — zum Archiv'
			}
		]
	},

	council: {
		roomWord: 'Council',
		lead: 'Getrennt abgestimmt, dann öffentlich gezählt. Was mehrfach genannt wird, wird Empfehlung.',
		// Zeitschicht-Zeile unter der Röhre (Council): Sitzungstakt als Plan. Datum
		// aus schedule.next_session; verstrichenes Datum wird clientseitig entfernt.
		rhythm: 'Der Council tagt, wenn genug Neues vorliegt.',
		nextSession: (dateStr) => `Laut Terminplan: ${dateStr}.`,
		// Zweite Ebene (CouncilActors): die Lesepulte tragen die Teilnehmer aus
		// den Daten (label/family) — die i18n-Schicht gibt nur die Rolle,
		// gespiegelt an Röhren-Schritt 3 („… antworten getrennt — jedes Votum
		// öffentlich").
		actors: {
			pult: {
				role: 'antwortet getrennt — jedes Votum öffentlich.'
			},
			// Die Zählmaschine (§8): die Plakette nennt die Aggregationsregel —
			// eine Prozessaussage, kein Ergebnis (die Datennaht bleibt versiegelt).
			machine: {
				rule: 'Zwei gleiche Nennungen ergeben eine Empfehlung.'
			}
		},
		// §4.2 „Wie gezählt wurde" — ein Block ersetzt drei (Empfehlungen /
		// Revisionen / Zählwerk). Revisionen leben in der Modell-Marke selbst
		// (Erstvotum durchgestrichen, Schlussvotum darunter), der Zählstand-
		// Slot sagt bei Uneinigkeit „getrennt" statt „x von N".
		countTitle: 'Wie gezählt wurde',
		countIntro: 'Das Programm zählt nur gleiche Nennungen.',
		jumpToArea: 'Bereich für die Zählmaschine wählen',
		countAreaCue: '— Bereich wählbar über die vier Embleme:',
		chosenPrefix: 'gewählt:',
		changedMark: 'geändert',
		countSplit: 'getrennt',
		noConsensus: 'Noch keine Einigkeit',
		reservation: 'Vorbehalt ▸',
		allVotesVerbatim: 'Alle Voten im Wortlaut ▸',
		initial: 'Erst',
		final: 'Schluss',
		noVote: 'kein Votum',
		readVotes: 'Voten lesen →',
		head: {
			title: 'NobleCause — The Council',
			description:
				'Wie die Empfehlungen zustande kommen: Nennungen je Modell, Zählstände, Vorbehalte, Erst- und Schlussvoten im Wortlaut und direkte Spendenlinks.'
		},
		doors: [
			{
				href: '/',
				img: '/media/scene-thumbnails/antechamber-display.avif',
				width: 640,
				height: 274,
				sub: 'Zurück durch die Tür',
				label: 'The Study',
				alt: 'Vorzimmer mit großer Schiefertafel, Schreibtischen und Lampen'
			},
			{
				href: '/archiv/',
				img: '/media/doors/door-council-archive-display.avif',
				width: 480,
				height: 640,
				sub: 'Die schlichte Tür',
				label: 'The Archive',
				alt: 'Unauffällige Seitentür zwischen dunklen Steinsäulen mit schmaler Lichtfuge — zum Archiv'
			}
		]
	},

	archive: {
		roomWord: 'Archive',
		lead: 'Jede Sitzung, vollständig und unverändert — Empfehlungen, Uneinigkeit, Kosten.',
		// Alt-Text des Möbels (zweite Ebene): reine Kulisse, kein Datenbezug.
		pultAlt: 'Archivpult mit Leseleuchte und aufgeschlagenem Folianten',
		sessionsTitle: 'Sitzungsarchiv',
		sessionLabel: (number) => `Sitzung ${number}`,
		// Chip-Markierung eines offenen Bereichs in der Sitzungszeile (§5.2).
		noConsensusNote: 'keine Einigung',
		costsTitle: 'Kosten',
		costsLead: (total) => `Kosten dieser Sitzung: ${total}.`,
		costsModel: 'Modell',
		costsAmount: 'Kosten',
		correctionTitle: 'Korrekturhinweis',
		dissentTitle: 'Dissens und Vorbehalte',
		dissentFull: 'Wortlaut des Rates ▸',
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
				img: '/media/scene-thumbnails/antechamber-display.avif',
				width: 640,
				height: 274,
				sub: 'Zurück',
				label: 'The Study',
				alt: 'Vorzimmer mit großer Schiefertafel, Schreibtischen und Lampen'
			},
			{
				href: '/ratssaal/',
				img: '/media/scene-thumbnails/hall-display.avif',
				width: 640,
				height: 360,
				sub: 'Zurück',
				label: 'The Council',
				alt: 'Kreisrunder Ratssaal mit drei Pulten und der Zählmaschine in der Mitte'
			}
		]
	}
};
