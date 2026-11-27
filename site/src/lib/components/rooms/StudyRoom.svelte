<script>
	// Website-only reading layer. Votes and record wording are rendered from the
	// existing server view model; the current record remains unchanged.
	import ResultBoard from './ResultBoard.svelte';
	import StageHero from './StageHero.svelte';
	import StageTube from './StageTube.svelte';
	import { studyCopy } from '$lib/i18n/study.js';
	import StudyActors from './StudyActors.svelte';
	import { localeForProcedure, roomPaths } from '$lib/i18n/index.js';
	import { formatDate } from '$lib/format.js';
	import { TUBE_FILLED } from '$lib/stage.js';
	import { DOOR_PASSAGES } from '$lib/door-passages.js';

	let { home, lang = 'de' } = $props();

	let t = $derived(localeForProcedure(lang, home?.currentSession?.procedureVersion));
	let copy = $derived(studyCopy[lang]);
	let tracks = $derived(home?.modelTracks ?? []);
	let participantCount = $derived(tracks.length);
	// Rekordtexte (Frage, Suchanfragen, Rats-Wortlaut) sind deutsch — im
	// EN-Modus markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
	// Klartext-Schicht (§1): liegt das Feld vor, ersetzt es die Rekord-Fassung;
	// EN fällt auf DE zurück (plainEnDe) und wird dann als deutscher Text
	// markiert. Das Frontend paraphrasiert nie — es liest das Feld nur.
	let plain = $derived(lang === 'en' ? home?.plainEn : home?.plain);
	let plainIsDe = $derived(lang === 'en' && home?.plainEnDe);
	// Klartext der Frage: plain.question, sonst ohne Prozesshinweis der
	// kuratierte Protokoll-Kontext (session.summary).
	let questionText = $derived(plain?.question ?? home?.questionSummary ?? null);
	let hasVoteDetails = $derived(home.recommendations.some((rec) => rec.hasConsensus || rec.votes.length > 0));
	// Die große Tür im Plate führt in den Council — Daten wie bei der Tür-Karte.
	let councilDoor = $derived(t.study.doors.find((door) => door.label === 'The Council'));

	// Zoom-Ursprung der Raumfahrt auf die Türmitte legen — deckt Tastatur ab
	// (clientX=0) und läuft nach dem globalen pointerdown-Listener. Reine
	// progressive Enhancement: ohne JS bleibt der Link ein gewöhnlicher Link.
	function setDoorOrigin(event) {
		const rect = event.currentTarget.getBoundingClientRect();
		document.documentElement.style.setProperty(
			'--vt-origin',
			`${rect.left + rect.width / 2}px ${rect.top + rect.height / 2}px`
		);
	}
</script>

<svelte:head>
	<title>{t.study.head.title}</title>
	<meta name="description" content={t.study.head.description(participantCount)} />
	<link rel="canonical" href="https://noblecause.ai{roomPaths.study[lang]}" />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.study.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.study.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.study.de}" />
</svelte:head>

{#if home}
<div class="study-page" lang={lang}>
	<a class="study-skip" href="#study-content">{copy.skip}</a>
	<StageHero
		scene="/media/scenes/antechamber-display.avif"
		sceneMobile="/media/scenes/antechamber-portrait-display.avif"
		sceneMobile800="/media/scenes/antechamber-portrait-800.avif"
		passage={DOOR_PASSAGES.study}
		bgPos="center top"
		title={t.common.heroTitle}
		pitch={t.study.introPitch}
		whySummary={t.common.whySummary}
		whyBody={t.common.whyBody}
		roomWord={t.study.roomWord}
		roomLead={t.study.lead}
	>
		{#snippet overlay()}
			<!-- Das freie Wandfeld links wird zum Gründungsdokument. Der Rahmen
			     besteht aus HTML/CSS auf der vorhandenen Szene: kein zweites Plate,
			     kein Bildasset. Mobil bleibt der Textlink unter der Prozessröhre der
			     auffindbare Weg, weil das Hochformat die linke Wand abschneidet. -->
			<a
				class="manifest-frame"
				href="/manifest/"
				aria-label={t.study.manifestFrameLabel}
				title={t.study.manifestFrameLabel}
			>
				<span class="manifest-sheet" aria-hidden="true">
					<span class="manifest-house">NOBLECAUSE.AI</span>
					<span class="manifest-title">MANIFEST</span>
					<span class="manifest-rule"></span>
					<span class="manifest-lines"></span>
					<span class="manifest-seal">I</span>
				</span>
				<span class="manifest-plaque" aria-hidden="true">{t.study.manifestFramePlaque}</span>
			</a>
			{#if councilDoor}
				<!-- Die Tür IM Raumbild: atmosphärischer Hotspot auf der gemalten
				     Doppeltür. Echter Link — trägt ohne JS und per Tastatur; die
				     Tür-Karte unten bleibt der auffindbare Weg. -->
				<a
					class="door-hotspot"
					href={councilDoor.href}
					aria-label="{councilDoor.sub}: {councilDoor.label}"
					title="{councilDoor.sub}: {councilDoor.label}"
					onclick={setDoorOrigin}
				></a>
			{/if}
		{/snippet}
		{#snippet scene2()}
			<!-- Zweite Ebene: Wolkenzug im Fenster + die Akteure (Einfahr-Beat).
			     Sitzinhaber (Scout = letzter Research-Lauf, Warden = led_by) und der
			     Warden-Entscheid kommen aus den Daten, wörtlich durchgereicht. -->
			<StudyActors {t} lastResearch={home?.lastResearch} ledBy={home?.currentSession?.ledBy} />
		{/snippet}
		{#snippet tube()}
			<!-- Prozess-Röhre: The Study zeigt Frage + Belege (Stand 2 von 6). -->
			<StageTube
				flow={t.study.flow}
				filledCount={TUBE_FILLED.study}
				{participantCount}
				label={t.tube.label}
				status={t.tube.status(2, t.study.flow.length)}
			>
				{#snippet caption()}
					<!-- Zeitschicht (Study): Rhythmus + letzter belegter Lauf + Manifest.
					     Absolutes Datum server-gerendert (No-JS vollständig); der Termin
					     lebt im Rhythmus, nicht in schedule.json. -->
					<p>
						{#if !home.schedule?.researchHeld}{t.study.rhythm}{' '}{/if}{#if home?.lastResearch?.date}{' '}{t.study.lastCheck(
								formatDate(home.lastResearch.date, t.lang)
							)}{/if}{' '}{t.study.manifestLead}
						<a href="/manifest/">{t.study.manifestLink}</a>
					</p>
				{/snippet}
			</StageTube>
		{/snippet}
	</StageHero>


	<main class="study-content" id="study-content" tabindex="-1">
		<section class="case-showcase" aria-labelledby="amf-showcase-title">
			<div>
				<p class="eyebrow">{copy.caseEyebrow}</p>
				<h2 id="amf-showcase-title">{copy.caseTitle}</h2>
				<ul class="case-points">
					<li>{copy.caseRecommendation}</li>
					<li>{copy.casePositions(home.caseStudy.positions)}</li>
					<li>{copy.caseEvidence(home.caseStudy.evidenceCards)}</li>
				</ul>
				<a class="primary-link" href={lang === 'en' ? '/en/case/amf/' : '/fall/amf/'}>{copy.openCase}</a>
			</div>
			<aside class="case-reading" aria-label={copy.caseRouteLabel}>
				<p>{copy.casePrompt}</p>
				<span>The Study <span aria-hidden="true">·</span> The Council <span aria-hidden="true">·</span> The Archive</span>
			</aside>
		</section>

		<aside class="operation-status" aria-label={copy.statusLabel}>
			<p class="status-heading">{copy.pilot}{#if home.currentSession.procedureVersion}{' '}v{home.currentSession.procedureVersion}{/if}</p>
			<p>{#if home.schedule?.sessionHeld && home.schedule?.researchHeld}{copy.bothPaused}{:else if home.schedule?.sessionHeld}{copy.councilPaused}{:else if home.schedule?.researchHeld}{copy.researchPaused}{:else}{copy.notPaused}{/if} {copy.openRecords(home.sessionCount)}</p>
		</aside>

		<section class="study-section architecture" aria-labelledby="architecture-title">
			<p class="eyebrow">{copy.methodEyebrow}</p>
			<h2 id="architecture-title">{copy.architectureTitle}</h2>
			<div class="method-grid">
				{#each copy.methods as method}
					<article>
						<h3>{method.title}</h3>
						<p>{method.body}</p>
						<a href={method.href}>{method.link}</a>
					</article>
				{/each}
			</div>
		</section>

		<section class="study-section session-section" aria-label={copy.lastSessionLabel}>
			<ResultBoard {home} {t} inline />
			<p class="session-link"><a href="/sitzungen/{home.currentSession.id}/">{copy.readSession}</a>{#if t.common.recordNote} <span class="record-note">{t.common.recordNote}</span>{/if}</p>
			{#if hasVoteDetails}
				<details class="dossier vote-details">
					<summary>{copy.voteDetails}</summary>
					{#each home.recommendations as rec (rec.pillar)}
						{@const why = plain?.recommendations?.[rec.pillar] ?? null}
						{#if rec.hasConsensus || rec.votes.length}
							<h3>{t.pillars[rec.pillar]?.label ?? rec.pillarName}</h3>
							{#if rec.hasConsensus}
								{#if why}<p lang={plainIsDe ? 'de' : undefined}>{why}</p>{/if}
								<p lang={recordLang}>{rec.title} — {rec.count} {t.common.ofWord} {rec.total}</p>
								{#each rec.reservations as reservation (reservation.model)}
									<p lang={recordLang}>{reservation.model}: {reservation.reservation}</p>
								{/each}
							{:else}
								<ul lang={recordLang}>{#each rec.votes as vote (vote.model)}<li>{vote.model}: {vote.organization.name}{#if vote.organization.donationUrl} <a href={vote.organization.donationUrl}>{t.common.donate}</a>{/if}</li>{/each}</ul>
							{/if}
						{/if}
					{/each}
					{#if t.common.recordNote}<p class="record-note">{t.common.recordNote}</p>{/if}
				</details>
			{/if}
			<details class="dossier session-dossiers">
				<summary>{copy.dossiersSummary}</summary>
				<div class="dossier-content">
					{#if questionText}
						<h3>{t.study.questionTitle}</h3>
						<p lang={plain?.question ? (plainIsDe ? 'de' : undefined) : recordLang}>{questionText}</p>
					{/if}
					<h3>{copy.verbatimQuestion}</h3>
					<blockquote class="question" lang={recordLang}><p>{home.currentSession.question}</p></blockquote>
					{#if t.common.recordNote}<p class="record-note">{t.common.recordNote}</p>{/if}
					{#if home.wartDossier?.search_queries?.length}
						<h3>{copy.searchQueries}</h3>
						<p>{t.study.researchNote}</p>
						<ul class="scout-queries" lang={recordLang}>{#each home.wartDossier.search_queries as query (query)}<li><code>{query}</code></li>{/each}</ul>
						<a href="/sitzungen/{home.currentSession.id}/#wart-dossier">{t.study.dossierLink}</a>
					{/if}
					{#if home.wartDossierRefusal}
						<aside class="dossier-refusal" aria-labelledby="dossier-refusal-title">
							<h3 id="dossier-refusal-title">{t.study.dossierRefusalTitle}</h3>
							<p>{t.study.dossierRefusalText}</p>
							<a href="/sitzungen/{home.currentSession.id}/#wart-dossier-refusal">{t.study.readProtocol}</a>
						</aside>
					{/if}
				</div>
			</details>
		</section>

		<nav class="study-section onward" aria-labelledby="onward-title">
			<h2 id="onward-title">{copy.onwardTitle}</h2>
			<div class="navigation-grid">
				{#each copy.navigation as link}
					<a href={link.href}><strong>{link.title}</strong><span>{link.description}</span></a>
				{/each}
			</div>
		</nav>
	</main>
</div>
{/if}

<style>
	/* ---- Tür-Hotspot ------------------------------------------------------
	   Tür-Zone der 1b-Plate (1672×941, Tür ZENTRAL: x 40–60 %, y 17–82 %).
	   object-position:center top → die Mitte überlebt jeden cover-Crop, der
	   Hotspot ist ab 1200 px immer wirksam (das war der Sinn der zentrierten
	   Tür). Zwei Fälle je nach Viewport-Ratio gegenüber dem Bild-Ratio 16/9:
	   breiter → Bild füllt die Breite (Vertikaler-Crop, Zone in vw);
	   schmaler → Bild füllt die Höhe (Horizontal-Crop um die Mitte, Zone in
	   svh um 50 vw). Hover/Fokus öffnet die Tür (Crossfade in StageHero);
	   die Tür-Karten unten bleiben der auffindbare Weg. */
	.door-hotspot {
		display: none;
	}
	@media (min-width: 1200px) {
		.door-hotspot {
			display: block;
			position: absolute;
			border-radius: 6px;
			cursor: pointer;
			pointer-events: auto;
		}
	}
	/* Bild füllt die Höhe (Viewport schmaler als 16/9): Bildbreite = 177,78 svh,
	   Mitte bei 50 vw → Tür x 40–60 % = 50 vw ± 17,78 svh; y direkt in svh. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.door-hotspot {
			left: calc(50vw - 17.78svh);
			top: 17svh;
			width: 35.56svh;
			height: 65svh;
		}
	}
	/* Bild füllt die Breite (Viewport breiter als 16/9): Bildhöhe = 56,25 vw,
	   Vertikal-Crop ab top → Tür-Zone komplett in vw. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.door-hotspot {
			left: 40vw;
			top: 9.56vw;
			width: 20vw;
			height: 36.56vw;
		}
	}
	.door-hotspot:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 2px;
	}

	/* ---- Manifest an der linken Wand --------------------------------------
	   Dokumentfläche im Study-Plate: x ≈ 11–26 %, y ≈ 22–53 %. Dieselbe
	   Cover-Rechnung wie beim Tür-Hotspot hält den CSS-Rahmen auf dem gemalten
	   Wandfeld. Unter 1200 px ist die Hochformat-Szene aktiv und schneidet die
	   Wand ab; dort bleibt der gewöhnliche Manifest-Link unter der Röhre. */
	.manifest-frame {
		display: none;
	}
	@media (min-width: 1200px) {
		.manifest-frame {
			display: flex;
			position: absolute;
			z-index: 1;
			align-items: center;
			justify-content: center;
			/* Keine Prozent-Paddings: bei absolut positionierten Elementen beziehen
			   sie sich auf den Viewport-Containing-Block und würden das Blatt auf
			   wenige Pixel zusammendrücken. */
			width: clamp(7rem, 10vw, 9rem);
			height: clamp(3.5rem, 4.7vw, 4.25rem);
			top: clamp(10.6rem, 21svh, 10.8rem);
			padding: 0.35rem;
			border: 0.28rem solid #493617;
			border-radius: 0.15rem;
			background:
				linear-gradient(135deg, rgba(236, 198, 113, 0.16), transparent 24%),
				linear-gradient(315deg, rgba(0, 0, 0, 0.55), transparent 35%),
				#19150e;
			box-shadow:
				0 0 0 1px rgba(207, 159, 70, 0.68),
				0 0 0 0.5rem rgba(10, 8, 5, 0.78),
				0.8rem 1.2rem 2rem rgba(0, 0, 0, 0.62),
				inset 0 0 1.3rem rgba(0, 0, 0, 0.72);
			color: #2b2114;
			text-decoration: none;
			pointer-events: auto;
			transform: perspective(50rem) rotateY(1.5deg) rotateZ(-0.35deg);
			transition:
				filter 0.25s ease,
				box-shadow 0.25s ease;
		}
		.manifest-frame:hover,
		.manifest-frame:focus-visible {
			filter: brightness(1.13);
			box-shadow:
				0 0 0 1px rgba(231, 197, 123, 0.9),
				0 0 0 0.5rem rgba(10, 8, 5, 0.82),
				0 0 2.1rem rgba(215, 170, 85, 0.28),
				0.8rem 1.2rem 2rem rgba(0, 0, 0, 0.68),
				inset 0 0 1.3rem rgba(0, 0, 0, 0.72);
		}
		.manifest-frame:focus-visible {
			outline: 2px solid #efd28c;
			outline-offset: 0.7rem;
		}
		.manifest-sheet {
			position: relative;
			display: flex;
			flex-direction: column;
			align-items: center;
			width: 100%;
			height: 100%;
			padding: 9% 8%;
			background:
				radial-gradient(circle at 25% 18%, rgba(255, 255, 255, 0.48), transparent 28%),
				linear-gradient(110deg, rgba(94, 63, 22, 0.08), transparent 30% 72%, rgba(82, 54, 17, 0.11)),
				#dfd0ad;
			border: 1px solid rgba(239, 218, 167, 0.72);
			box-shadow: inset 0 0 1rem rgba(65, 41, 12, 0.2);
			overflow: hidden;
		}
		.manifest-house,
		.manifest-title,
		.manifest-plaque {
			font-family: ui-sans-serif, system-ui, sans-serif;
		}
		.manifest-house {
			font-size: clamp(0.28rem, 0.36vw, 0.48rem);
			font-weight: 700;
			letter-spacing: 0.2em;
		}
		.manifest-title {
			margin-top: 6%;
			font-size: clamp(0.52rem, 0.72vw, 0.96rem);
			font-weight: 700;
			letter-spacing: 0.12em;
		}
		.manifest-rule {
			width: 72%;
			margin-top: 8%;
			border-top: 1px solid rgba(66, 45, 19, 0.62);
		}
		.manifest-lines {
			width: 86%;
			height: 22%;
			margin-top: 8%;
			background: repeating-linear-gradient(
				to bottom,
				rgba(58, 42, 23, 0.52) 0 1px,
				transparent 1px 14%
			);
			opacity: 0.55;
		}
		.manifest-seal {
			display: grid;
			place-items: center;
			width: 18%;
			aspect-ratio: 1;
			margin-top: 6%;
			border: 1px solid #7b5522;
			border-radius: 50%;
			color: #684818;
			font-size: clamp(0.4rem, 0.6vw, 0.8rem);
		}
		.manifest-plaque {
			display: none;
		}
	}
	/* Bild füllt die Höhe: x = 12 % des zentrierten 16:9-Plates. Vertikal
	   bleibt das Dokument bewusst oberhalb der fixen Ergebnis-Tafel. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.manifest-frame {
			left: max(1.5rem, calc(50vw - 67.56svh));
		}
	}
	/* Bild füllt die Breite: x = 12 % des Plates. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.manifest-frame {
			left: 12vw;
		}
	}

	.study-skip { position: fixed; left: 1rem; top: -8rem; z-index: 6; padding: .7rem 1rem; background: #ead3a0; color: #101719; }
	.study-skip:focus { top: 1rem; }
	.study-content { position: relative; width: min(67rem, calc(100% - 2rem)); margin: 0 auto; padding: 2.5rem 2.5rem 3rem; background: #0b1417 !important; border-inline: 1px solid #52452e; }
	.study-content :is(h2, h3) { margin: 0; padding: 0; border: 0; color: #ead8ae; font-weight: 400; }
	.study-content h2 { font-size: clamp(1.65rem, 3vw, 2.2rem); line-height: 1.2; }
	.study-content h3 { font-size: 1.25rem; }
	.study-content p { margin: .8rem 0; }
	.study-content a { color: #e8c582; text-underline-offset: .2em; }
	.study-content a:focus-visible, .study-content summary:focus-visible { outline: 2px solid #f4d597; outline-offset: 5px; }
	.study-content .eyebrow { margin: 0 0 .65rem; color: #b4c7c8; font: 600 .85rem/1.5 system-ui, sans-serif; letter-spacing: .08em; text-transform: uppercase; }
	.case-showcase { display: grid; grid-template-columns: minmax(0, 1.65fr) minmax(0, 1fr); gap: 2rem; padding: 2rem; border: 1px solid #b89557; background: linear-gradient(120deg, #202b2b, #111e22); box-shadow: 0 1rem 2.5rem #0004; }
	.case-points { padding-left: 1.1rem; margin: 1.2rem 0 1.4rem; display: grid; gap: .45rem; color: #e2dccd; }
	.case-points li::marker { color: #d7b477; }
	.study-content .primary-link { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: .6rem 1.1rem; border: 1px solid #e1bf7d; background: #dfbd7c; color: #10191b; font: 600 1rem/1.4 system-ui, sans-serif; text-decoration: none; }
	.study-content .primary-link:hover { background: #f0d49b; }
	.case-reading { display: flex; flex-direction: column; justify-content: center; border-left: 1px solid #a58a57; padding-left: 1.5rem; }
	.case-reading p { color: #ebd7b3; font-size: 1.5rem; line-height: 1.4; }
	.case-reading > span { color: #b8cacc; font: .875rem/1.7 system-ui, sans-serif; }
	.operation-status { margin-top: 1.25rem; padding: 1rem 1.25rem; border: 1px solid #4d666b; background: #142126; color: #cbd9d9; font: .95rem/1.65 system-ui, sans-serif; }
	.operation-status .status-heading { margin: 0 0 .3rem; color: #e9d4a7; font-weight: 600; }
	.operation-status p:last-child { margin: 0; }
	.study-section { margin-top: 2.75rem; }
	.method-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin-top: 1.4rem; }
	.method-grid article { min-width: 0; padding: 1.25rem; border: 1px solid #495556; background: #142024; display: flex; flex-direction: column; }
	.method-grid p { color: #cbd1c9; font-size: 1rem; line-height: 1.7; }
	.method-grid a { margin-top: auto; padding-top: .5rem; font: .9rem/1.5 system-ui, sans-serif; }
	.session-section { padding: 1.5rem; border: 1px solid #68583c; background: #111c20; }
	.session-link { font-size: .95rem; }
	.session-link .record-note { display: block; margin-top: .25rem; }
	.record-note { color: #bdc7c4; font-size: .875rem; }
	.dossier { border-top: 1px solid #546162; margin-top: .9rem; }
	.dossier summary { cursor: pointer; padding: .85rem 0; min-height: 48px; color: #e9cc92; font-size: 1.05rem; }
	.dossier-content { padding-bottom: .5rem; }
	.dossier h3 { margin-top: 1.3rem; }
	.dossier-content > h3:first-child { margin-top: .3rem; }
	.question { margin: 1rem 0; padding: 0 0 0 1rem; border-left: 2px solid #ba9b61; }
	.dossier p, .dossier li { color: #d0d7d1; }
	.dossier code { font-size: .875rem; overflow-wrap: anywhere; }
	.dossier-refusal { border-left: 2px solid #9fbac2; padding-left: 1rem; }
	.navigation-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin-top: 1.4rem; }
	.navigation-grid a { display: grid; gap: .35rem; padding: 1.25rem; border: 1px solid #786440; background: #1b282b; text-decoration: none; }
	.navigation-grid a:hover { background: #27373a; border-color: #dfbd7c; }
	.navigation-grid strong { color: #f0d7a5; font-size: 1.3rem; font-weight: 400; }
	.navigation-grid span { color: #ced8d5; font: .95rem/1.6 system-ui, sans-serif; }
	@media (max-width: 900px) {
		.study-content { padding: 1.5rem; }
		.case-showcase { gap: 1.5rem; padding: 1.5rem; }
		.method-grid { grid-template-columns: 1fr; }
	}
	@media (max-width: 600px) {
		.study-content { width: calc(100% - 1rem); padding: 1.5rem .75rem 2rem; }
		.case-showcase { grid-template-columns: 1fr; padding: 1.25rem; gap: 1.4rem; }
		.case-reading { padding: 1rem 0 0; border-left: 0; border-top: 1px solid #a58a57; }
		.case-reading p { font-size: 1.25rem; margin-top: 0; }
		.session-section { padding: 1rem; }
		.navigation-grid { grid-template-columns: 1fr; }
	}
</style>
