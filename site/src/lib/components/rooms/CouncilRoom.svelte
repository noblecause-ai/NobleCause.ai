<script>
	// The Council: Saal-Plates (quer/hoch, geschlossen/offen — Nachtrag-Serie
	// 24.07.), zweite Ebene CouncilActors (N Lesepulte fahren von unten ein,
	// Szene-Kantenprinzip), Ergebnis-Tafel (betonter Zählstand), Zähl-Block
	// „Wie gezählt wurde" (je Bereich Modell-Marken mit Erst-/Schlussvotum),
	// volle Voten-Matrix hinter Ausklapp, Türen. Sprache als Prop; orgEn =
	// optionale englische
	// Organisationsbeschreibungen (Registry-Feld beschreibung_en, aufgelöst im
	// Layout-Load) — derzeit ohne Anzeigefläche im Raum (Mechanismus lebt in
	// RecommendationCard.svelte, Beschreibungen in Registry/Sitzungsseite).
	// Vorbehalte sind publizierter Rekord und bleiben deutsch — im EN-Modus mit
	// recordNote. Der Prozess läuft nur noch über die Röhre (StageTube) — die
	// FlowRail ist mit der Titelbereich-Neuordnung entfallen; der Kopf ist der
	// stabile, auf allen Räumen identische Block. Die Teilnehmerzahl steckt in
	// den Datenpfaden (modelTracks, Röhren-Schritt 3), nicht in der Copy.
	import CouncilActors from './CouncilActors.svelte';
	import Door from './Door.svelte';
	import ModelPulpits from './ModelPulpits.svelte';
	import ResultBoard from './ResultBoard.svelte';
	import StageHero from './StageHero.svelte';
	import StageTube from './StageTube.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';
	import { formatDate } from '$lib/format.js';
	import { TUBE_FILLED } from '$lib/stage.js';

	let { home, lang = 'de', orgEn = {} } = $props();
	void orgEn; // Prop bleibt verdrahtet (Mechanismus), hat hier keine Anzeigefläche.

	let t = $derived(locales[lang]);
	// Zeitschicht: das geplante Sitzungsdatum wird server-gerendert (No-JS = voll).
	// Ob es verstrichen ist, entscheidet NUR der Client relativ zum Betrachtungs-
	// zeitpunkt — kein buildTime, kein Überfällig-Zustand. $effect läuft client-only.
	let nextSessionPast = $state(false);
	$effect(() => {
		const iso = home?.schedule?.nextSession;
		nextSessionPast = iso ? new Date(iso).getTime() < Date.now() : false;
	});
	let tracks = $derived(home?.modelTracks ?? []);
	let participantCount = $derived(tracks.length);
	// Vorbehalte und Voten sind publizierter Rekord (deutsch) — im EN-Modus markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
	// §4.2 „Wie gezählt wurde": je Bereich eine Zeile, darin je Teilnehmer eine
	// Marke mit seiner Nennung — generisch aus modelTracks, skaliert mit N
	// (kein festes Drei-Spalten-Raster). Revisionen leben in der Marke selbst
	// (Erstvotum durchgestrichen, Schlussvotum darunter).
	let countRows = $derived(
		(home?.recommendations ?? []).map((rec) => ({
			rec,
			marks: tracks.map((track) => ({
				label: track.label,
				row: track.rows.find((row) => row.pillar === rec.pillar) ?? null
			}))
		}))
	);
</script>

<svelte:head>
	<title>{t.council.head.title}</title>
	<meta name="description" content={t.council.head.description} />
	<link rel="preload" as="image" href="/media/scenes/hall-display.avif" media="(min-width: 1200px)" />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.council.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.council.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.council.de}" />
</svelte:head>

{#if home}
	<StageHero
		scene="/media/scenes/hall-display.avif"
		sceneMobile="/media/scenes/hall-portrait-display.avif"
		sceneMobile800="/media/scenes/hall-portrait-800.avif"
		sceneOpen="/media/scenes/hall-door-open-display.avif"
		bgPos="center top"
		title={t.common.heroTitle}
		pitch={t.common.heroPitch}
		whySummary={t.common.whySummary}
		whyBody={t.common.whyBody}
		roomWord={t.council.roomWord}
		roomLead={t.council.lead}
	>
		{#snippet scene2()}
			<!-- Zweite Ebene: die Lesepulte der Teilnehmer nehmen von unten ihre
			     Plätze ein (Kantenprinzip) — generisch aus modelTracks, N Pulte
			     im Saal; Türachse und Zählmaschine bleiben frei. -->
			<CouncilActors {t} {tracks} />
		{/snippet}
		{#snippet tube()}
			<!-- Prozess-Röhre: The Council steht bei Zählen (Stand 5 von 6). -->
			<StageTube
				flow={t.study.flow}
				filledCount={TUBE_FILLED.council}
				{participantCount}
				label={t.tube.label}
				status={t.tube.status(5, t.study.flow.length)}
			>
				{#snippet caption()}
					<!-- Zeitschicht (Council): Sitzungstakt als Bedingung + Termin als
					     Zitat aus schedule.next_session. Datum server-gerendert (No-JS =
					     voll); verstrichen → entfällt clientseitig (nextSessionPast). -->
					<p>
						{t.council.rhythm}{#if home?.schedule?.nextSession && !nextSessionPast}{' '}{t.council.nextSession(
								formatDate(home.schedule.nextSession, t.lang)
							)}{/if}
					</p>
				{/snippet}
			</StageTube>
		{/snippet}
	</StageHero>

	<main>
		<!-- Dieselbe Tafel wie in The Study, hier mit betontem Zählstand. -->
		<ResultBoard {home} {t} emphasizeCount />

		<!-- §4.2 „Wie gezählt wurde" — ein Block ersetzt drei (Empfehlungen /
		     Revisionen / Zählwerk): je Bereich eine Zeile, darin je Teilnehmer
		     eine Marke mit seiner Nennung. Die Tafel oben trägt das Was; hier
		     steht ausschließlich das Zustandekommen. -->
		<section class="room-section" aria-labelledby="count-title">
			<h2 id="count-title">{t.council.countTitle}</h2>
			<p class="count-intro">{t.council.countIntro}</p>
			<ol class="count-rows">
				{#each countRows as { rec, marks } (rec.pillar)}
					<li>
						<div class="count-head">
							<img src={t.pillars[rec.pillar]?.src} alt="" width="40" height="40" loading="lazy" />
							<span class="count-area">{t.pillars[rec.pillar]?.label ?? rec.pillarName}</span>
							{#if rec.hasConsensus}
								<span class="count-tally">→ {rec.count} {t.common.ofWord} {rec.total}</span>
							{:else}
								<span class="count-tally split">→ {t.council.countSplit}</span>
							{/if}
						</div>
						<div class="count-marks">
							{#each marks as mark (mark.label)}
								<span class="mark">
									<span class="mark-model">{mark.label}</span>
									{#if mark.row?.changed}
										<del>{mark.row.initial.organization.name}</del>
										<strong>{mark.row.final.organization.name}</strong>
									{:else if mark.row?.final}
										<strong>{mark.row.final.organization.name}</strong>
									{:else}
										<span class="mark-none">{t.council.noVote}</span>
									{/if}
								</span>
							{/each}
						</div>
						{#if rec.hasConsensus && rec.conditionalCount}
							<details class="count-reservation">
								<summary>{t.council.reservation}</summary>
								{#each rec.reservations as reservation (reservation.model)}
									<p lang={recordLang}>{reservation.model}: {reservation.reservation}</p>
								{/each}
								{#if t.common.recordNote}
									<small class="record-note">{t.common.recordNote}</small>
								{/if}
							</details>
						{/if}
					</li>
				{/each}
			</ol>
			<!-- §4.3: die volle Matrix — ein Anker am Blockende, nicht je Zeile. -->
			<details class="all-votes">
				<summary>{t.council.allVotesVerbatim}</summary>
				<ModelPulpits tracks={home.modelTracks} sessionId={home.currentSession.id} {t} />
			</details>
			<p class="money-flow">{t.common.moneyFlow}</p>
		</section>

		<section class="room-section" aria-labelledby="doors-title">
			<h2 id="doors-title">{t.common.doorsTitle}</h2>
			<div class="door-gallery">
				{#each t.council.doors as door (door.href)}
					<Door {door} />
				{/each}
			</div>
		</section>
	</main>
{/if}

<style>
	/* „Wie gezählt wurde": je Bereich eine Zeile — Kopf mit Emblem, Bereich und
	   Zählstand, darunter die Modell-Marken mit den Nennungen (Revisionen in
	   der Marke: Erstvotum durchgestrichen, Schlussvotum darunter). */
	.count-intro {
		margin: 0 0 0.7rem;
		color: #c7bca7;
		font-size: 0.95rem;
	}
	.count-rows {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
	}
	.count-rows > li {
		padding: 0.7rem 0;
	}
	.count-rows > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.3);
	}
	.count-head {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.35rem 0.7rem;
	}
	.count-head img {
		width: 2.2rem;
		height: 2.2rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.count-area {
		color: #c9ab6e;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.count-tally {
		color: #dfbd70;
		font: 600 0.85rem ui-sans-serif, system-ui;
		white-space: nowrap;
	}
	.count-tally.split {
		color: #c7bca7;
		font-weight: 400;
	}
	/* Die Marken: generisch eine je Teilnehmer — flex-wrap statt festem
	   Drei-Spalten-Raster, skaliert mit der Council-Größe. */
	.count-marks {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-top: 0.55rem;
	}
	.mark {
		display: grid;
		gap: 0.1rem;
		align-content: start;
		min-width: min(11rem, 100%);
		flex: 1 1 min(11rem, 100%);
		padding: 0.55rem 0.7rem;
		background: #0b1011;
		border: 1px solid #7a5a2f;
		color: #e6dbc4;
		font-size: 0.85rem;
	}
	.mark-model {
		color: #d5a657;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.mark del {
		color: #8f866f;
		font-size: 0.8rem;
		text-decoration-color: rgba(197, 145, 60, 0.8);
	}
	.mark strong {
		font-weight: 600;
	}
	.mark-none {
		color: #8f866f;
	}
	.count-reservation {
		margin-top: 0.4rem;
	}
	.count-reservation summary {
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e0c07f;
		font-size: 0.85rem;
	}
	.count-reservation summary:hover {
		color: #f2d9a0;
	}
	.count-reservation summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.count-reservation p {
		margin: 0 0 0.4rem;
		color: #e0c07f;
		font-size: 0.85rem;
	}
	.record-note {
		display: block;
		margin: -0.2rem 0 0.4rem;
		color: #9e927f;
		font-size: 0.72rem;
		font-style: italic;
	}
	.money-flow {
		margin: 0.9rem 0 0;
		color: #9e927f;
		font: 0.72rem ui-sans-serif, system-ui;
	}

	/* Volle Voten-Matrix hinter Ausklapp am Blockende. */
	.all-votes {
		margin-top: 0.9rem;
	}
	.all-votes summary {
		cursor: pointer;
		min-height: 44px;
		display: inline-flex;
		align-items: center;
		color: #e7c881;
		font-size: 0.98rem;
	}
	.all-votes summary:hover {
		color: #f2d9a0;
	}
	.all-votes summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.all-votes[open] summary {
		margin-bottom: 0.9rem;
	}
</style>
