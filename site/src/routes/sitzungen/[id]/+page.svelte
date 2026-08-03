<script>
	import { PILLARS, PILLAR_ORDER } from '$lib/pillars.js';
	import { companyName, modelName } from '$lib/model-display.js';

	let { data } = $props();
	const s = $derived(data.session);
	const participants = $derived(data.participants);
	const tracks = $derived(data.tracks);
	const pillars = $derived(data.pillars);

	const MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
	function fmtDate(iso) {
		const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? '');
		return m ? `${+m[3]}. ${MONTHS[+m[2] - 1]} ${m[1]}` : (iso ?? '');
	}
	const kicker = $derived(
		['Protokoll', s.designation, `Sitzung ${s.number}`, fmtDate(s.date)].filter(Boolean).join(' · ')
	);
	const rowFor = (model, pillar) =>
		tracks.find((t) => t.model === model)?.rows.find((r) => r.pillar === pillar) ?? null;
	const voteHtml = (model, kind) =>
		s.rounds.find((r) => r.kind === kind)?.votes?.find((v) => v.model === model)?.content_html ?? null;
</script>

<svelte:head>
	<title>Sitzung {s.number}: {s.title} — NobleCause.ai</title>
	<meta name="description" content={s.summary || s.question} />
</svelte:head>

<p class="kicker">{kicker}</p>
<h1>{s.title}</h1>
<blockquote class="question">{s.question}</blockquote>

<nav class="jumpbar" aria-label="Zu einem Bereich springen">
	{#each PILLAR_ORDER as p (p)}
		<a class="jumplink" href="#bereich-{p}">
			<img class="emblem" src={PILLARS[p].emblem} alt="" width="40" height="40" loading="lazy" />
			{PILLARS[p].label}
		</a>
	{/each}
</nav>

{#if s.wart_opening_html}
	<h2>Eröffnung durch den Wart</h2>
	<p class="muted small">Sitzungsleitung: Der Wart · <code>{s.led_by?.model ?? 'claude-fable-5'}</code></p>
	<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
	<div class="verbatim">{@html s.wart_opening_html}</div>
{/if}

{#if s.corrections?.length}
	<aside class="correction" id="korrektur">
		<p class="correction-label">Nachträge zum Rekord</p>
		{#each s.corrections as c (c.date)}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
			<div class="verbatim">{@html c.html}</div>
		{/each}
	</aside>
{/if}

<h2>Die vier Bereiche</h2>
<p class="muted small">
	Je Bereich das Erst- und Schlussvotum jedes Modells (Änderungen und Vorbehalte gekennzeichnet),
	darüber der Zählstand. Das Programm zählt nur gleiche Nennungen: zwei gleiche ergeben eine
	Empfehlung.
</p>
<ol class="rec-rows">
	{#each PILLAR_ORDER as p (p)}
		{@const pil = pillars.find((x) => x.pillar === p)}
		<li id="bereich-{p}">
			<div class="rec-head">
				<img class="emblem" src={PILLARS[p].emblem} alt="" width="48" height="48" loading="lazy" />
				<span class="rec-area">{PILLARS[p].label}</span>
				{#if pil?.hasConsensus}
					<span class="rec-tally">{pil.organization} · {pil.count} von {pil.total}</span>
				{:else}
					<span class="rec-tally split">getrennt — keine Empfehlung</span>
				{/if}
			</div>
			<div class="marks">
				{#each participants as pt (pt.model)}
					{@const row = rowFor(pt.model, p)}
					<div class="mark">
						{#if pt.medallion}
							<img class="med" src={pt.medallion} alt="" width="256" height="256" loading="lazy" />
						{:else}
							<span class="med-none"></span>
						{/if}
						<span class="mark-model">
							{modelName(pt.model, pt.label)} <span class="mark-company">· {companyName(pt.family)}</span>
						</span>
						<span class="mark-vote">
							{#if row?.changed}
								<del>{row.initial.org}</del><strong class="mark-org">{row.final.org}</strong>
							{:else if row?.final}
								<strong class="mark-org">{row.final.org}</strong>
							{:else}
								<span class="mark-none">kein Votum</span>
							{/if}
							{#if row?.final?.conditional}<span class="mark-note"> · konditional</span>{/if}
						</span>
						{#if row?.final?.reservation}
							<span class="mark-reservation">Vorbehalt: {row.final.reservation}</span>
						{/if}
					</div>
				{/each}
			</div>
		</li>
	{/each}
</ol>

<h2 id="vollprotokoll">Die Stimmen im Wortlaut</h2>
<p class="muted small">Ungekürzt. Jede Stimme trägt ihr Medaillon; darunter die Selbstdarstellung.</p>
<ol class="voices">
	{#each participants as pt (pt.model)}
		<li id={pt.model}>
			<div class="voice-head">
				{#if pt.medallion}
					<img class="med-lg" src={pt.medallion} alt="" width="256" height="256" loading="lazy" />
				{:else}
					<span class="med-lg med-none"></span>
				{/if}
				<span class="voice-name">{modelName(pt.model, pt.label)}</span>
				<span class="voice-company">{companyName(pt.family)}{#if pt.person} · {pt.person}{/if}</span>
			</div>
			{#if pt.motiv || pt.begruendung}
				<details class="self">
					<summary>Selbstdarstellung des Medaillons</summary>
					{#if pt.motiv}<p class="self-motiv">{pt.motiv}</p>{/if}
					{#if pt.begruendung}<p class="self-begr">{pt.begruendung}</p>{/if}
				</details>
			{/if}
			{#if voteHtml(pt.model, 'initial_vote')}
				<details>
					<summary>Erstvotum (unabhängig)</summary>
					<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
					<div class="verbatim">{@html voteHtml(pt.model, 'initial_vote')}</div>
				</details>
			{/if}
			{#if voteHtml(pt.model, 'final_vote')}
				<details>
					<summary>Schlussvotum (nach Gegenlese)</summary>
					<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
					<div class="verbatim">{@html voteHtml(pt.model, 'final_vote')}</div>
				</details>
			{/if}
		</li>
	{/each}
</ol>

{#if s.dissent_highlights?.length || s.dissent_html}
	<h2>Dissens</h2>
	{#if s.dissent_highlights?.length}
		<ul class="highlights">
			{#each s.dissent_highlights as point (point)}<li>{point}</li>{/each}
		</ul>
	{/if}
	{#if s.dissent_html}
		<details>
			<summary>Dissens im Wortlaut</summary>
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
			<div class="verbatim">{@html s.dissent_html}</div>
		</details>
	{/if}
{/if}

{#if s.wart_dossier || s.wart_moderation_html}
	<h2>Der Wart</h2>
	{#if s.wart_dossier}
		<details id="wart-dossier">
			<summary>Wart-Dossier (Runde 0, Web-Recherche)</summary>
			{#if s.wart_dossier.search_queries?.length}
				<p class="kicker">Suchanfragen</p>
				<ul class="queries">
					{#each s.wart_dossier.search_queries as q (q)}<li><code>{q}</code></li>{/each}
				</ul>
			{/if}
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
			<div class="verbatim">{@html s.wart_dossier_html}</div>
		</details>
	{/if}
	{#if s.wart_moderation_html}
		<details>
			<summary>Moderationsnotiz (nach den Erstvoten)</summary>
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
			<div class="verbatim">{@html s.wart_moderation_html}</div>
		</details>
	{/if}
{/if}

<h2>Kosten</h2>
<p class="costs-total">{s.costs.total.toFixed(2)} € an API-Aufrufen</p>
{#if s.costs.by_model?.length}
	<ul class="costs">
		{#each s.costs.by_model as m (m.model)}
			<li>
				<span class="cost-model">{modelName(m.model, m.label)}</span>
				<span class="cost-eur">{m.eur != null ? `${m.eur.toFixed(2)} €` : '—'}</span>
			</li>
		{/each}
	</ul>
{/if}

<p class="footnote">
	Rohantworten und vollständige Aufschlüsselung im
	<a href="https://github.com/noblecause-ai/NobleCause.ai/tree/master/sessions/{s.id}"
		>Repository (sessions/{s.id}/)</a
	>.
</p>

<style>
	.small {
		font-size: 0.9rem;
	}
	.correction {
		margin: 1.6rem 0;
		padding: 0.2rem 0 0.2rem 1rem;
		border-left: 3px solid #8bb7ca;
		scroll-margin-top: 1.5rem;
	}
	.correction-label {
		margin: 0 0 0.3rem;
		color: #8bb7ca;
		font: 600 0.7rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	/* ---- Marke: Kopfzeile (Medaillon | Name) + Votum + Vorbehalt ------------- */
	.mark-vote {
		grid-column: 2;
		color: #e6dbc4;
		font-size: 0.95rem;
	}
	.mark-org {
		font-weight: 600;
	}
	.mark-reservation {
		grid-column: 2;
		margin-top: 0.15rem;
		color: #e0c07f;
		font-size: 0.84rem;
	}

	/* ---- Stimmen im Wortlaut ------------------------------------------------- */
	.voices {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.voices > li {
		padding: 1.2rem 0;
		scroll-margin-top: 1.5rem;
	}
	.voices > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.28);
	}
	.voice-head {
		display: grid;
		grid-template-columns: auto 1fr;
		column-gap: 0.8rem;
		align-items: center;
	}
	.med-lg {
		grid-row: 1 / 3;
		width: 3rem;
		height: 3rem;
		border-radius: 50%;
		filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.7));
	}
	.voice-name {
		align-self: end;
		color: #f0d899;
		font-size: 1.1rem;
	}
	.voice-company {
		align-self: start;
		color: #9e927f;
		font-size: 0.85rem;
		font-style: italic;
	}
	.self {
		margin-top: 0.3rem;
	}
	.self-motiv {
		margin: 0.4rem 0 0.3rem;
		color: #e2d8c2;
	}
	.self-begr {
		margin: 0.3rem 0;
		color: #c7bca7;
		font-size: 0.94rem;
	}

	/* ---- Dissens / Suchanfragen / Kosten ------------------------------------ */
	.highlights {
		margin: 0.4rem 0 0.8rem;
		padding-left: 1.2rem;
	}
	.highlights li {
		margin: 0.45rem 0;
	}
	.queries {
		margin: 0.3rem 0 0.8rem;
		padding-left: 1.2rem;
		font-size: 0.85rem;
	}
	.costs-total {
		margin: 0 0 0.6rem;
		color: #dfbd70;
		font: 600 1rem ui-sans-serif, system-ui, sans-serif;
	}
	.costs {
		margin: 0;
		padding: 0;
		list-style: none;
		max-width: 22rem;
	}
	.costs > li {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		padding: 0.3rem 0;
		border-top: 1px solid rgba(166, 123, 61, 0.18);
		font-size: 0.9rem;
	}
	.cost-model {
		color: #c7bca7;
	}
	.cost-eur {
		color: #e6dbc4;
		font-variant-numeric: tabular-nums;
	}
	.footnote {
		margin-top: 2.5rem;
		padding-top: 1rem;
		border-top: 1px solid rgba(166, 123, 61, 0.28);
		color: #9e927f;
		font-size: 0.82rem;
		font-family: ui-sans-serif, system-ui, sans-serif;
	}
</style>
