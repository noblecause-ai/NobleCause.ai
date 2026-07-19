<script>
	// The Archive: Sitzungsliste, Kosten, Korrekturhinweis, Dissens im Wortlaut, Türen.
	// Sprache als Prop. Korrekturhinweis, Dissens und Protokoll sind publizierter
	// Rekord und bleiben deutsch — im EN-Modus mit recordNote/protocolNote markiert.
	import Door from './Door.svelte';
	import RoomHero from './RoomHero.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';

	let { home, lang = 'de' } = $props();

	let t = $derived(locales[lang]);
	// Rekordtexte sind deutsch — im EN-Modus maschinell als solche markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);

	const money = (value, currency = 'EUR') =>
		new Intl.NumberFormat(lang === 'en' ? 'en-GB' : 'de-CH', {
			style: 'currency',
			currency
		}).format(value);
	const areaNames = (pillars) =>
		pillars.map((pillar) => t.pillars[pillar]?.label ?? pillar).join(', ');
</script>

<svelte:head>
	<title>{t.archive.head.title}</title>
	<meta name="description" content={t.archive.head.description} />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.archive.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.archive.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.archive.de}" />
</svelte:head>

{#if home}
	<RoomHero
		scene="/media/scenes/archive-display.jpg"
		sceneMobile="/media/scenes/archive-portrait-display.jpg"
		bgPos="center"
		bgPosMobile="right top"
		eyebrow={t.archive.eyebrow}
		title={t.archive.title}
	/>

	<main>
		<section class="room-section" aria-labelledby="sessions-title">
			<h2 id="sessions-title">{t.archive.sessionsTitle}</h2>
			<ol class="session-list">
				{#each home.archive as item (item.id)}
					<li>
						<a href="/sessions/{item.id}/">
							<span>{t.archive.sessionLabel(item.number)}</span>
							<strong>
								{item.nonConsensusPillars.length
									? t.archive.dissentIn(areaNames(item.nonConsensusPillars))
									: t.archive.allAreas}
							</strong>
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
			{#if t.common.recordNote}
				<small class="record-note">{t.common.recordNote}</small>
			{/if}
			{#if home.dissentHighlights.length}
				<blockquote class="room-panel dissent-highlights" lang={recordLang}>
					<p class="highlights-label">{t.archive.dissentHighlightsTitle}</p>
					<ul>
						{#each home.dissentHighlights as highlight (highlight)}
							<li>{highlight}</li>
						{/each}
					</ul>
				</blockquote>
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
		gap: 0.2rem;
		padding: 0.85rem 1.1rem;
		text-decoration: none;
	}
	.session-list a:hover strong {
		color: #e7c881;
	}
	.session-list span {
		color: #9b8b72;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.session-list strong {
		color: #c8bca6;
		font-size: 0.95rem;
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
	.highlights-label {
		margin: 0 0 0.5rem;
		color: #a99062;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.dissent-highlights ul {
		margin: 0;
		padding-left: 1.2rem;
		display: grid;
		gap: 0.45rem;
		color: #c7bca7;
		font-size: 0.88rem;
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
