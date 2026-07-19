<script>
	// The Study: Ergebnis-Tafel (eigenständiges Schiefer-Panel, ab 1200 px fix —
	// siehe ResultBoard.svelte), Prozess-Leiste (geteilte FlowRail-Komponente),
	// Dossiers mit sichtbarem Klartext-Kontext + Zitat-Beleg, Türen.
	// Sprache kommt als Prop; Texte aus locales[lang]. Teilnehmerzahl und Familien
	// kommen aus den Daten (modelTracks) — nichts davon steht fest in der Copy.
	// Publizierte Rekordtexte (Sitzungs-Kontext, Frage, Suchanfragen) bleiben
	// deutsch; im EN-Modus kennzeichnet sie common.recordNote. Die Tafel zeigt
	// die vier Empfehlungen aus home.recommendations — gelesen, niemals neu
	// gezählt; Spendenlinks kommen registry-aufgelöst aus den Daten.
	import Door from './Door.svelte';
	import FlowRail from './FlowRail.svelte';
	import ResultBoard from './ResultBoard.svelte';
	import RoomHero from './RoomHero.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';

	let { home, lang = 'de' } = $props();

	let t = $derived(locales[lang]);
	let tracks = $derived(home?.modelTracks ?? []);
	let participantCount = $derived(tracks.length);
	// Anzeigenamen der Familien kommen aus der Locale; unbekannte Familien
	// fallen auf den Rohwert aus den Daten zurück.
	let families = $derived(
		new Intl.ListFormat(lang === 'de' ? 'de' : 'en', { type: 'conjunction' }).format([
			...new Set(tracks.map((track) => t.common.familyNames?.[track.family] ?? track.family))
		])
	);
	// Rekordtexte (Sitzungs-Kontext, Frage, Suchanfragen) sind deutsch — im
	// EN-Modus markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
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
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.study.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.study.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.study.de}" />
</svelte:head>

{#if home}
	<RoomHero
		scene="/media/scenes/antechamber-display.jpg"
		sceneMobile="/media/scenes/antechamber-portrait-display.jpg"
		bgPos="left top"
		eyebrow={t.study.eyebrow}
		title={t.study.title}
		lead={t.study.lead(families)}
	>
		{#snippet overlay()}
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
	</RoomHero>

	<main>
		<!-- Die Tafel trägt die Antwort — pragerendert, No-JS liest sie am Eingang. -->
		<ResultBoard {home} {t} />

		<FlowRail flow={t.study.flow} {participantCount} title={t.study.flowTitle} />

		<section class="room-section" aria-labelledby="dossiers-title">
			<h2 id="dossiers-title">{t.study.dossiersTitle}</h2>
			{#if home.questionSummary}
				<!-- Sichtbar zuerst: der kuratierte Protokoll-Kontext, wörtlich aus
				     den Daten durchgereicht (keine Frontend-Paraphrase). -->
				<div class="question-context">
					<h3>{t.study.questionContext}</h3>
					<p lang={recordLang}>{home.questionSummary}</p>
					{#if t.common.recordNote}
						<small class="record-note">{t.common.recordNote}</small>
					{/if}
				</div>
			{/if}
			<details class="dossier">
				<summary>{t.study.questionSummary}</summary>
				<blockquote class="question" lang={recordLang}>
					<p>{home.currentSession.question}</p>
				</blockquote>
				{#if t.common.recordNote}
					<small class="record-note">{t.common.recordNote}</small>
				{/if}
				<a href="/sessions/{home.currentSession.id}/">{t.study.readProtocol}</a>
			</details>
			{#if home.wartDossier?.search_queries?.length}
				<details class="dossier">
					<summary>{t.study.researchSummary}</summary>
					<p class="research-note">{t.study.researchNote}</p>
					<ul class="scout-queries" lang={recordLang}>
						{#each home.wartDossier.search_queries as query (query)}
							<li><code>{query}</code></li>
						{/each}
					</ul>
					<a href="/sessions/{home.currentSession.id}/#wart-dossier">{t.study.dossierLink}</a>
				</details>
			{/if}
		</section>

		<section class="room-section" aria-labelledby="doors-title">
			<h2 id="doors-title">{t.common.doorsTitle}</h2>
			<div class="door-gallery">
				{#each t.study.doors as door (door.href)}
					<Door {door} />
				{/each}
			</div>
		</section>
	</main>
{/if}

<style>
	/* ---- Tür-Hotspot ------------------------------------------------------
	   Tür-Zone der Landscape-Plate: x 86,5–99,5 %, y 5–82 %. Nur sichtbar,
	   wenn die Tür im cover-Ausschnitt liegt (object-position:left top →
	   Seitenverhältnis ≥ 2,1); darunter tragen die Tür-Karten die Navigation.
	   Reine Deko — die Pixelkette an die gemalte Tür ist hier der Zweck. */
	.door-hotspot {
		display: none;
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 21/10) {
		.door-hotspot {
			display: block;
			position: absolute;
			left: 201.75svh;
			top: 5svh;
			width: 30.32svh;
			height: 77svh;
			border-radius: 6px;
			cursor: pointer;
			opacity: 0;
			pointer-events: auto;
			background:
				radial-gradient(
					ellipse 62% 55% at 50% 45%,
					rgba(255, 202, 128, 0.52),
					rgba(255, 182, 98, 0.22) 55%,
					rgba(255, 182, 98, 0) 78%
				),
				radial-gradient(
					ellipse 110% 100% at 50% 50%,
					rgba(255, 190, 110, 0.12),
					rgba(255, 190, 110, 0) 70%
				);
			mix-blend-mode: screen;
			transition: opacity 0.45s ease;
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 1600/686) {
		.door-hotspot {
			left: 86.5vw;
			top: 2.14vw;
			width: 13vw;
			height: 33.01vw;
		}
	}
	.door-hotspot:hover,
	.door-hotspot:focus-visible {
		opacity: 1;
	}
	.door-hotspot:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 2px;
	}
	@media (prefers-reduced-motion: reduce) {
		.door-hotspot {
			transition: none;
		}
	}

	/* ---- Frage-Kontext ------------------------------------------------------
	   Sichtbarer Klartext-Einstieg ins Dossier (kuratierter Protokolltext aus
	   den Daten); der wörtliche Wortlaut folgt als Zitat-Beleg hinter Ausklapp. */
	.question-context {
		margin-bottom: 1rem;
	}
	.question-context h3 {
		margin: 0 0 0.3rem;
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}
	.question-context p {
		margin: 0 0 0.2rem;
		max-width: 46rem;
		color: #e2d8c0;
		font-size: 1rem;
	}

	/* ---- Dossiers ---------------------------------------------------------
	   Rohe Rekord-Details hinter Ausklapp — eingeklappt im Erstkontakt,
	   ohne JS und per Tastatur voll bedienbar. */
	.dossier {
		border-top: 1px solid rgba(166, 123, 61, 0.4);
		padding: 0.35rem 0 0.9rem;
	}
	.dossier summary {
		cursor: pointer;
		min-height: 44px;
		display: flex;
		align-items: center;
		color: #e7c881;
		font-size: 0.98rem;
	}
	.dossier summary:hover {
		color: #f2d9a0;
	}
	.dossier summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.question {
		margin: 0.3rem 0 0.6rem;
		padding-left: 0.9rem;
		border-left: 3px solid rgba(197, 145, 60, 0.55);
		font-style: italic;
	}
	.question p {
		margin: 0;
		font-size: 1rem;
	}
	.record-note {
		display: block;
		margin: -0.2rem 0 0.4rem;
		color: #9e927f;
		font-size: 0.72rem;
		font-style: italic;
	}
	.research-note {
		margin: 0.2rem 0 0.6rem;
		color: #a9997d;
		font-size: 0.85rem;
	}
	.scout-queries {
		margin: 0 0 0.8rem;
		padding-left: 1.2rem;
		display: grid;
		gap: 0.3rem;
	}
	.scout-queries code {
		font-size: 0.8rem;
		overflow-wrap: break-word;
	}
	a {
		color: #e6b45c;
	}
	.dossier > a {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
	}
</style>
