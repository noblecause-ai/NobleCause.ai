<script>
	// The Archive: Ergebnis-Tafel (dieselbe eine Instanz wie in den anderen
	// Räumen — die Antwort reist durchs Haus), Sitzungsliste, Kosten,
	// Korrekturhinweis, Dissens im Wortlaut, Türen.
	// Sprache als Prop. Korrekturhinweis, Dissens und Protokoll sind publizierter
	// Rekord und bleiben deutsch — im EN-Modus mit recordNote/protocolNote markiert.
	import ArchiveActors from './ArchiveActors.svelte';
	import Door from './Door.svelte';
	import ResultBoard from './ResultBoard.svelte';
	import StageHero from './StageHero.svelte';
	import StageTube from './StageTube.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';
	import { TUBE_FILLED } from '$lib/stage.js';

	let { home, lang = 'de' } = $props();

	let t = $derived(locales[lang]);
	// Die große Tür im Archiv-Plate führt ZURÜCK in die Study — der Rundgang
	// schließt sich (Study → Council → Archive → Study), und der Study steht die
	// Antwort samt Spendenlinks. Daten wie bei der Tür-Karte (sub/label).
	let studyDoor = $derived(t.archive.doors.find((door) => door.label === 'The Study'));

	// Zoom-Ursprung der Raumfahrt auf die Türmitte legen (Tastatur/Kartenrand) —
	// reine progressive Enhancement; ohne JS bleibt der Link ein Link.
	function setDoorOrigin(event) {
		const rect = event.currentTarget.getBoundingClientRect();
		document.documentElement.style.setProperty(
			'--vt-origin',
			`${rect.left + rect.width / 2}px ${rect.top + rect.height / 2}px`
		);
	}
	// Rekordtexte sind deutsch — im EN-Modus maschinell als solche markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
	// Klartext-Zeilen zu offenen Bereichen (§5.3): nur Tatsache und Gegenstand
	// des Dissenses aus plain.dissent — die Argumente bleiben Wortlaut im
	// Ausklapp. EN fällt auf DE zurück (plainEnDe) und wird markiert.
	let dissentLines = $derived(
		(home?.dissentOpen ?? [])
			.map((entry) => ({ ...entry, text: (lang === 'en' ? entry.plainEn : entry.plain) }))
			.filter((entry) => entry.text)
	);
	let plainIsDe = $derived(lang === 'en' && home?.plainEnDe);

	const money = (value, currency = 'EUR') =>
		new Intl.NumberFormat(lang === 'en' ? 'en-GB' : 'de-CH', {
			style: 'currency',
			currency
		}).format(value);
</script>

<svelte:head>
	<title>{t.archive.head.title}</title>
	<meta name="description" content={t.archive.head.description} />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.archive.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.archive.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.archive.de}" />
</svelte:head>

{#if home}
	<StageHero
		scene="/media/scenes/archive-display.avif"
		sceneMobile="/media/scenes/archive-portrait-display.avif"
		sceneMobile800="/media/scenes/archive-portrait-800.avif"
		sceneOpen="/media/scenes/archive-door-open-display.avif"
		bgPos="center top"
		bgPosMobile="right top"
		title={t.common.heroTitle}
		pitch={t.common.heroPitch}
		whySummary={t.common.whySummary}
		whyBody={t.common.whyBody}
		roomWord={t.archive.roomWord}
		roomLead={t.archive.lead}
	>
		{#snippet overlay()}
			{#if studyDoor}
				<!-- Die Tür IM Archiv-Bild: Hotspot auf der gemalten Doppeltür,
				     führt zurück in die Study. Echter Link (No-JS/Tastatur); die
				     Tür-Karte unten bleibt der auffindbare Weg. Archiv-eigene
				     Türgeometrie (kleiner + zentral, s. CSS). -->
				<a
					class="door-hotspot"
					href={studyDoor.href}
					aria-label="{studyDoor.sub}: {studyDoor.label}"
					title="{studyDoor.sub}: {studyDoor.label}"
					onclick={setDoorOrigin}
				></a>
			{/if}
		{/snippet}
		{#snippet scene2()}
			<!-- Zweite Ebene: zwei Karteikästen an den unteren Ecken (reine Kulisse). -->
			<ArchiveActors {t} />
		{/snippet}
		{#snippet tube()}
			<!-- Prozess-Röhre: The Archive ist voll (Stand 6 von 6). -->
			<StageTube
				flow={t.study.flow}
				filledCount={TUBE_FILLED.archive}
				participantCount={(home?.modelTracks ?? []).length}
				label={t.tube.label}
				status={t.tube.status(6, t.study.flow.length)}
			/>
		{/snippet}
	</StageHero>

	<main>
		<!-- Dieselbe eine Tafel wie in den anderen Räumen — die Antwort steht
		     auch im Archiv am Eingang (Grammatik §2 des Umlaufs). -->
		<ResultBoard {home} {t} />

		<section class="room-section" aria-labelledby="sessions-title">
			<h2 id="sessions-title">{t.archive.sessionsTitle}</h2>
			<ol class="session-list">
				{#each home.archive as item (item.id)}
					<li>
						<a href="/sessions/{item.id}/">
							<span class="session-meta">{t.archive.sessionLabel(item.number)} · {item.date}</span>
							<!-- Ergebnis-Chips (§5.2): das Regal zeigt Ergebnisse, keine
							     Dateinamen. Namen registry-aufgelöst (Fallback: der
							     protokollierte String), offene Bereiche markiert. -->
							<span class="chips">
								{#each item.chips as chip (chip.pillar)}
									{#if chip.status !== 'missing'}
										<span class="chip" class:open={chip.status === 'open'}>
											<img
												src={t.pillars[chip.pillar]?.src}
												alt={t.pillars[chip.pillar]?.label ?? chip.pillar}
												width="24"
												height="24"
												loading="lazy"
											/>
											{chip.status === 'open' ? t.archive.noConsensusNote : chip.name}
										</span>
									{/if}
								{/each}
							</span>
						</a>
					</li>
				{/each}
			</ol>
		</section>

		<section class="room-section" aria-labelledby="costs-title">
			<h2 id="costs-title">{t.archive.costsTitle}</h2>
			<div class="room-panel">
				<p class="costs-lead">{t.archive.costsLead(money(home.costs.total, home.costs.currency))}</p>
				<table>
					<thead>
						<tr>
							<th scope="col">{t.archive.costsModel}</th>
							<th scope="col">{t.archive.costsAmount}</th>
						</tr>
					</thead>
					<tbody>
						{#each home.costs.by_model as row (row.model)}
							<tr>
								<td>{row.label}</td>
								<td>{money(row.eur, home.costs.currency)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>

		{#if home.correctionHtml}
			<aside class="room-section" aria-labelledby="correction-title">
				<h2 id="correction-title">{t.archive.correctionTitle}</h2>
				{#if t.common.recordNote}
					<small class="record-note">{t.common.recordNote}</small>
				{/if}
				<div class="room-panel correction" lang={recordLang}>
					<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
					{@html home.correctionHtml}
				</div>
			</aside>
		{/if}

		<section class="room-section" aria-labelledby="dissent-title">
			<h2 id="dissent-title">{t.archive.dissentTitle}</h2>
			{#if dissentLines.length}
				<!-- §5.3: je offenem Bereich eine Klartext-Zeile — nur Tatsache und
				     Gegenstand; die Argumente bleiben Wortlaut im Ausklapp unten. -->
				<div class="dissent-plain">
					{#each dissentLines as line (line.pillar)}
						<p lang={plainIsDe ? 'de' : undefined}>
							<strong>{t.pillars[line.pillar]?.label ?? line.pillarName}</strong>: {line.text}
						</p>
					{/each}
					{#if plainIsDe && t.common.recordNote}
						<small class="record-note">{t.common.recordNote}</small>
					{/if}
				</div>
			{:else}
				{#if home.dissentOpen.length}
					<small class="record-note pending">{t.common.klartextPending}</small>
				{/if}
				{#if home.dissentHighlights.length}
					<blockquote class="room-panel dissent-highlights" lang={recordLang}>
						<ul>
							{#each home.dissentHighlights as highlight (highlight)}
								<li>{highlight}</li>
							{/each}
						</ul>
					</blockquote>
				{/if}
				{#if t.common.recordNote}
					<small class="record-note">{t.common.recordNote}</small>
				{/if}
			{/if}
			<details class="room-panel dissent-full">
				<summary>{t.archive.dissentFull}</summary>
				<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
				<div class="dissent-body" lang={recordLang}>{@html home.dissentHtml}</div>
			</details>
		</section>

		<section class="room-section">
			<a class="protocol-link" href="/sessions/{home.currentSession.id}/">{t.archive.protocolLink}</a>
			{#if t.archive.protocolNote}
				<small class="record-note">{t.archive.protocolNote}</small>
			{/if}
		</section>

		<section class="room-section" aria-labelledby="doors-title">
			<h2 id="doors-title">{t.common.doorsTitle}</h2>
			<div class="door-gallery">
				{#each t.archive.doors as door (door.href)}
					<Door {door} />
				{/each}
			</div>
		</section>
	</main>
{/if}

<style>
	/* ---- Tür-Hotspot (Archiv-eigene Werte) --------------------------------
	   Tür-Zone des archive-Plate (1672×941, 16:9). Die Tür steht ZENTRAL, aber
	   kleiner als in Study/Council: am gerenderten Plate gemessen x ≈ 43–54,5 %,
	   y ≈ 19,5–62,5 % (Study-Richtwert war 40–60/17–82). object-position center
	   top → die Mitte überlebt jeden cover-Crop; ab 1200 px immer wirksam. Zwei
	   Fälle je Viewport-Ratio ggü. 16:9 (wie StudyRoom): schmaler → Bild füllt
	   die Höhe (Zone in svh um 50 vw); breiter → Bild füllt die Breite (Zone in
	   vw, Crop ab top). Hover/Fokus öffnet die Tür (Crossfade in StageHero); die
	   Blende liest ihr Rechteck beim Klick aus getBoundingClientRect(). */
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
	/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite = 177,78 svh,
	   Mitte bei 50 vw → Tür x 43–54,5 % = 50 vw + (x−50) · 1,7778 svh; y in svh. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.door-hotspot {
			left: calc(50vw - 12.44svh);
			top: 19.5svh;
			width: 20.44svh;
			height: 43svh;
		}
	}
	/* Bild füllt die Breite (Viewport breiter als 16:9): Bildhöhe = 56,25 vw,
	   Vertikal-Crop ab top → Tür-Zone komplett in vw. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.door-hotspot {
			left: 43vw;
			top: 10.97vw;
			width: 11.5vw;
			height: 24.19vw;
		}
	}
	.door-hotspot:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 2px;
	}

	.session-list {
		margin: 0;
		padding: 0;
		list-style: none;
		background: rgba(13, 18, 19, 0.94);
		border: 1px solid rgba(166, 123, 61, 0.5);
	}
	.session-list li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.3);
	}
	.session-list a {
		display: grid;
		gap: 0.45rem;
		padding: 0.85rem 1.1rem;
		text-decoration: none;
	}
	.session-list a:hover .chip {
		color: #e7c881;
	}
	.session-meta {
		color: #9b8b72;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	/* Ergebnis-Chips: Emblem + registry-aufgelöster Name je Bereich;
	   offene Bereiche gedämpft und als „keine Einigung" markiert. */
	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem 1rem;
	}
	.chip {
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		color: #c8bca6;
		font-size: 0.88rem;
	}
	.chip img {
		width: 1.4rem;
		height: 1.4rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.chip.open {
		color: #9b8b72;
		font-style: italic;
	}
	.costs-lead {
		margin: 0 0 0.7rem;
		font-size: 1rem;
	}
	table {
		font-size: 0.85rem;
	}
	th,
	td {
		border-color: rgba(71, 56, 32, 0.8);
	}
	.correction {
		border-left: 3px solid #c89644;
		/* Der Diff-Hash im Korrekturtext ist ein umbrechbares Token. */
		overflow-wrap: break-word;
	}
	.correction :global(p) {
		margin: 0.3rem 0;
	}
	.record-note {
		display: block;
		margin: 0 0 0.5rem;
		color: #9e927f;
		font-size: 0.72rem;
		font-style: italic;
	}
	.dissent-highlights {
		margin-bottom: 0.8rem;
	}
	.dissent-highlights ul {
		margin: 0;
		padding-left: 1.2rem;
		display: grid;
		gap: 0.45rem;
		color: #c7bca7;
		font-size: 0.88rem;
	}
	/* Klartext-Zeilen zu offenen Bereichen (§5.3) — Tatsache/Gegenstand,
	   die Argumente bleiben Wortlaut im Ausklapp. */
	.dissent-plain {
		margin-bottom: 0.8rem;
	}
	.dissent-plain p {
		margin: 0 0 0.45rem;
		color: #e2d8c0;
		font-size: 0.95rem;
		line-height: 1.45;
	}
	.dissent-plain strong {
		color: #c9ab6e;
	}
	.pending {
		margin: 0 0 0.7rem;
	}
	.dissent-full summary {
		cursor: pointer;
		min-height: 44px;
		display: flex;
		align-items: center;
		color: #e0b75d;
	}
	/* Geschlossene Details per content-visibility behalten ihr Layout — die langen
	   Codezeilen im Dissens würden sonst die Viewport-Breite aufblähen (mobil). */
	.dissent-full:not([open]) .dissent-body {
		display: none;
	}
	.dissent-body {
		max-height: 26rem;
		overflow: auto;
		font-size: 0.85rem;
	}
	.dissent-body :global(pre) {
		overflow-x: auto;
	}
	.protocol-link {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e6b45c;
		font-size: 1.02rem;
	}
</style>
