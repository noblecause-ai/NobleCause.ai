<script>
	// The Council: Ergebnis-Tafel (betonter Zählstand), Prozess-Leiste (geteilte
	// FlowRail-Komponente), Empfehlungen als Zeilen-Liste, Revisionen, Zählwerk,
	// Pulte hinter Ausklapp, Türen. Sprache als Prop; orgEn = optionale englische
	// Organisationsbeschreibungen (Registry-Feld beschreibung_en, aufgelöst im
	// Layout-Load) — derzeit ohne Anzeigefläche im Raum (Mechanismus lebt in
	// RecommendationCard.svelte, Beschreibungen in Registry/Sitzungsseite).
	// Vorbehalte sind publizierter Rekord und bleiben deutsch — im EN-Modus mit
	// recordNote. h1 und Erklärtext tragen die Teilnehmerzahl/Familien aus den
	// Daten — nichts davon steht fest in der Copy.
	import Door from './Door.svelte';
	import FlowRail from './FlowRail.svelte';
	import ModelPulpits from './ModelPulpits.svelte';
	import ResultBoard from './ResultBoard.svelte';
	import RoomHero from './RoomHero.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';

	let { home, lang = 'de', orgEn = {} } = $props();
	void orgEn; // Prop bleibt verdrahtet (Mechanismus), hat hier keine Anzeigefläche.

	let t = $derived(locales[lang]);
	let tracks = $derived(home?.modelTracks ?? []);
	let participantCount = $derived(tracks.length);
	// Familienliste wie in The Study — der Erklärtext ist derselbe Einstieg.
	let families = $derived(
		new Intl.ListFormat(lang === 'de' ? 'de' : 'en', { type: 'conjunction' }).format([
			...new Set(tracks.map((track) => t.common.familyNames?.[track.family] ?? track.family))
		])
	);
	// Vorbehalte sind publizierter Rekord (deutsch) — im EN-Modus markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
	// Revisionen vollständig datengetrieben: Anzahl abgeleitet, alle Säulen, kein Hardcode.
	let revisions = $derived(home?.revisions ?? []);
	let revisedModelCount = $derived(new Set(revisions.map((revision) => revision.model)).size);
</script>

<svelte:head>
	<title>{t.council.head.title}</title>
	<meta name="description" content={t.council.head.description} />
	<link rel="preload" as="image" href="/media/scenes/hall-display.jpg" />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.council.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.council.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.council.de}" />
</svelte:head>

{#if home}
	<RoomHero
		scene="/media/scenes/hall-display.jpg"
		bgPos="center"
		eyebrow="{t.council.eyebrow} · {t.council.sessionPrefix} {home.currentSession.number}"
		title={t.council.title(participantCount)}
		lead={t.study.lead(families)}
	/>

	<main>
		<!-- Dieselbe Tafel wie in The Study, hier mit betontem Zählstand. -->
		<ResultBoard {home} {t} emphasizeCount />

		<FlowRail flow={t.study.flow} {participantCount} title={t.study.flowTitle} />

		<section class="room-section" aria-labelledby="rec-title">
			<h2 id="rec-title">{t.council.recTitle}</h2>
			<!-- Entrümpelt: die Tafel trägt die Ergebnisse, hier nur je eine Zeile —
			     Vorbehalte (publizierter Rekord) hinter Ausklapp in der Zeile. -->
			<ol class="rec-lines">
				{#each home.recommendations as rec (rec.pillar)}
					<li>
						<img src={t.pillars[rec.pillar]?.src} alt="" width="40" height="40" />
						<span class="rec-area">{t.pillars[rec.pillar]?.label ?? rec.pillarName}</span>
						{#if rec.hasConsensus}
							<strong>{rec.organization.name}</strong>
							<span class="rec-count">{rec.count} {t.common.ofWord} {rec.total}</span>
							{#if rec.organization.donationUrl}
								<a class="rec-donate" href={rec.organization.donationUrl}>{t.common.donate}</a>
							{/if}
							{#if rec.conditionalCount}
								<details class="rec-reservation">
									<summary>{t.council.reservation}</summary>
									{#each rec.reservations as reservation (reservation.model)}
										<p lang={recordLang}>
											{t.council.reservation} ({reservation.model}): {reservation.reservation}
										</p>
									{/each}
									{#if t.common.recordNote}
										<small class="record-note">{t.common.recordNote}</small>
									{/if}
								</details>
							{/if}
						{:else}
							<strong>{t.council.noConsensus}</strong>
							<ul class="rec-votes">
								{#each rec.votes as vote (vote.model)}
									<li>
										{vote.model}: {vote.organization.name}
										{#if vote.organization.donationUrl}
											<a href={vote.organization.donationUrl}>{t.common.donate}</a>
										{/if}
									</li>
								{/each}
							</ul>
						{/if}
					</li>
				{/each}
			</ol>
			<p class="money-flow">{t.common.moneyFlow}</p>
		</section>

		{#if revisions.length}
			<section class="room-section" aria-labelledby="revisions-title">
				<h2 id="revisions-title">{t.council.revisionsTitle}</h2>
				<div class="room-panel">
					<p class="revision-lead"><strong>{t.council.revisionLead(revisedModelCount)}</strong></p>
					<div class="revision-notes">
						{#each revisions as revision (revision.model + revision.pillar)}
							<article>
								<span>{revision.model} · {t.pillars[revision.pillar]?.label ?? revision.pillarName}</span>
								<small>{t.council.revisionInitial}</small>
								<del>{revision.initial.organization.name}</del>
								<small>{t.council.revisionChangedTo}</small>
								<strong>{revision.final.organization.name}</strong>
							</article>
						{/each}
					</div>
				</div>
			</section>
		{/if}

		<section class="room-section" aria-labelledby="machine-title">
			<h2 id="machine-title">{t.council.machineTitle}</h2>
			<div class="room-panel machine">
				<p>{t.council.machineText}</p>
				<ul class="machine-slots">
					{#each home.recommendations as rec (rec.pillar)}
						<li>
							<i>{t.pillars[rec.pillar]?.label ?? rec.pillarName}</i>
							{rec.hasConsensus ? `${rec.count} ${t.council.machineSame}` : t.council.machineSplit}
						</li>
					{/each}
				</ul>
			</div>
		</section>

		<section class="room-section" aria-labelledby="pulpits-title">
			<h2 id="pulpits-title">{t.council.pulpitsTitle}</h2>
			<!-- Die volle Matrix steht hinter Ausklapp — pragerendert im HTML,
			     ohne JS und per Tastatur voll bedienbar. -->
			<details class="all-votes">
				<summary>{t.council.allVotes}</summary>
				<ModelPulpits tracks={home.modelTracks} sessionId={home.currentSession.id} {t} />
			</details>
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
	/* Zeilen-Liste der Empfehlungen: Emblem, Bereich, Organisation, Zählstand,
	   Spendenlink — Vorbehalt hinter Ausklapp in der Zeile. */
	.rec-lines {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
	}
	.rec-lines > li {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.35rem 0.8rem;
		padding: 0.6rem 0;
	}
	.rec-lines > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.3);
	}
	.rec-lines img {
		width: 2.2rem;
		height: 2.2rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.rec-area {
		color: #c9ab6e;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.rec-lines strong {
		color: #f0e6cd;
		font-size: 1rem;
	}
	.rec-count {
		color: #dfbd70;
		font: 600 0.85rem ui-sans-serif, system-ui;
		white-space: nowrap;
	}
	.rec-donate {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e6b45c;
		font-size: 0.9rem;
	}
	.rec-reservation {
		flex-basis: 100%;
	}
	.rec-reservation summary {
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e0c07f;
		font-size: 0.85rem;
	}
	.rec-reservation summary:hover {
		color: #f2d9a0;
	}
	.rec-reservation summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.rec-reservation p {
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
	.rec-votes {
		flex-basis: 100%;
		margin: 0;
		padding-left: 1.2rem;
		color: #c7bca7;
		font-size: 0.88rem;
	}
	.rec-votes a {
		color: #e6b45c;
	}
	.money-flow {
		margin: 0.9rem 0 0;
		color: #9e927f;
		font: 0.72rem ui-sans-serif, system-ui;
	}

	/* Volle Voten-Matrix hinter Ausklapp. */
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

	.machine p {
		margin: 0 0 0.7rem;
		color: #c7bca7;
	}
	.machine-slots {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
		gap: 0.5rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.machine-slots li {
		display: grid;
		gap: 0.15rem;
		padding: 0.55rem 0.7rem;
		background: #0b1011;
		border: 1px solid #7a5a2f;
		color: #e6dbc4;
		font-size: 0.85rem;
	}
	.machine-slots i {
		color: #d5a657;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		font-style: normal;
	}
	.revision-lead {
		margin: 0 0 0.8rem;
		color: #e6dbc4;
	}
	.revision-notes {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(min(13rem, 100%), 1fr));
		gap: 1rem;
	}
	.revision-notes article {
		padding: 0.7rem 0.8rem;
		color: #20180e;
		background: #ded0b4;
		box-shadow: 0 0.8rem 1.6rem rgba(0, 0, 0, 0.5);
	}
	.revision-notes span,
	.revision-notes small {
		display: block;
		font: 600 0.58rem ui-sans-serif, system-ui;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.revision-notes del,
	.revision-notes strong {
		display: block;
		margin: 0.12rem 0;
	}
</style>
