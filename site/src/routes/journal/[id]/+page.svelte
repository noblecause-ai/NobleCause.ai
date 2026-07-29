<script>
	import { PILLARS } from '$lib/pillars.js';
	import { companyName, modelName } from '$lib/model-display.js';

	let { data } = $props();
	const e = $derived(data.entry);
	const commission = $derived(data.commission);

	const MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
	function fmtDate(iso) {
		const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? '');
		return m ? `${+m[3]}. ${MONTHS[+m[2] - 1]} ${m[1]}` : (iso ?? '');
	}
	const isCommission = $derived(e.type === 'commission');
	const heading = $derived(isCommission ? 'Bestellung der Selbstdarstellungen' : `Wart-Dossier vom ${fmtDate(e.date)}`);
</script>

<svelte:head>
	<title>Journal {fmtDate(e.date)} — NobleCause.ai</title>
	<meta name="description" content={(e.delta_assessment ?? e.convene_rationale ?? 'Wart-Dossier')?.slice(0, 160)} />
</svelte:head>

<p class="kicker">Journal des Warts · {fmtDate(e.date)}{#if isCommission} · Kommission{/if}</p>
<h1>{heading}</h1>

<p class="meta">
	{#if e.model}Modell <code>{e.model}</code>{:else if isCommission}Bestell-Kommission{:else}Steward{/if}
	{#if e.costs?.total != null} · Laufkosten {e.costs.total.toFixed(2)} €{/if}
	{#if e.session_ref} · Referenz <a href="/sessions/{e.session_ref}/">Sitzung {e.session_ref}</a>{/if}
</p>
{#if e.deputation_note}
	<p class="deputation">{e.deputation_note}</p>
{/if}
{#if e.actions_run_url}
	<p class="meta">
		<a href={e.actions_run_url}>Lauf im Rohzustand verfolgen</a> — GitHub Actions, öffentliches Log.
	</p>
{/if}

<h2>Einberufungs-Entscheid</h2>
<p>
	<strong class="verdict" class:yes={e.convene}>{e.convene ? 'Einberufen' : 'Nicht einberufen'}</strong>
	{#if e.convene_rationale}— {e.convene_rationale}{/if}
</p>

{#if e.delta_assessment}
	<h2>Delta-Bewertung</h2>
	<p>{e.delta_assessment}</p>
{/if}

{#if commission}
	<h2>Die Bestellung</h2>
	<p class="muted small">
		Jedes Modell entwarf sein eigenes Messing-Medaillon — Motiv und Begründung, unverändert
		festgehalten.
	</p>
	<ol class="orders">
		{#each commission.orders as o (o.model)}
			<li>
				<div class="order-head">
					{#if o.medallion}
						<img class="med" src={o.medallion} alt="" width="256" height="256" loading="lazy" />
					{:else}
						<span class="med med-none"></span>
					{/if}
					<span class="order-name">{modelName(o.model, o.label)}</span>
					<span class="order-company">{o.family ? companyName(o.family) : ''}{#if o.within_limits === false} · über den Grenzwerten (angenommen){/if}</span>
				</div>
				{#if o.motiv}<p class="order-motiv">{o.motiv}</p>{/if}
				{#if o.begruendung}<p class="order-begr">{o.begruendung}</p>{/if}
			</li>
		{/each}
	</ol>
{/if}

{#if e.findings?.length}
	<h2>Kernfunde</h2>
	<ol class="findings">
		{#each e.findings as f, i (i)}
			<li>
				<p class="finding-head">
					{#if PILLARS[f.pillar]}
						<img class="emblem" src={PILLARS[f.pillar].emblem} alt="" width="40" height="40" loading="lazy" />
						<span class="rec-area">{PILLARS[f.pillar].label}</span>
					{/if}
					{#if f.topic}<span class="finding-topic">{f.topic}</span>{/if}
				</p>
				<p class="finding-summary">{f.summary}</p>
				<p class="finding-source">Quelle: {f.source}{#if f.source_date} ({f.source_date}){/if}</p>
			</li>
		{/each}
	</ol>
{/if}

{#if e.search_queries?.length}
	<h2>Suchanfragen</h2>
	<ul class="queries">
		{#each e.search_queries as q (q)}<li><code>{q}</code></li>{/each}
	</ul>
{/if}

{#if e.rejected_findings?.length}
	<h2>Verworfene Funde</h2>
	<ul class="rejected">
		{#each e.rejected_findings as r, i (i)}
			<li><strong>{r.query_or_topic}</strong> — {r.reason}</li>
		{/each}
	</ul>
{/if}

{#if e.content_html}
	<h2>Vollständiges Dossier</h2>
	<details>
		<summary>Wortlaut (Markdown gerendert)</summary>
		<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
		<div class="verbatim">{@html e.content_html}</div>
	</details>
{/if}

<style>
	.meta {
		margin: 0 0 0.6rem;
		color: #9e927f;
		font-size: 0.9rem;
	}
	.deputation {
		margin: 0 0 0.8rem;
		color: #9e927f;
		font-size: 0.88rem;
		font-style: italic;
	}
	.verdict {
		color: #c7bca7;
	}
	.verdict.yes {
		color: #e7c881;
	}
	.small {
		font-size: 0.9rem;
	}

	/* ---- Kommissions-Bestellungen (Medaillon-Selbstdarstellung) ------------- */
	.orders {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.orders > li {
		padding: 1.2rem 0;
	}
	.orders > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.28);
	}
	.order-head {
		display: grid;
		grid-template-columns: 3rem 1fr;
		column-gap: 0.8rem;
		align-items: center;
	}
	.order-head .med {
		grid-row: 1 / 3;
		width: 3rem;
		height: 3rem;
		border-radius: 50%;
		filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.7));
	}
	.order-head .med-none {
		grid-row: 1 / 3;
		width: 3rem;
	}
	.order-name {
		align-self: end;
		color: #f0d899;
		font-size: 1.1rem;
	}
	.order-company {
		align-self: start;
		color: #9e927f;
		font-size: 0.85rem;
		font-style: italic;
	}
	.order-motiv {
		margin: 0.5rem 0 0.3rem;
		color: #e2d8c2;
	}
	.order-begr {
		margin: 0.3rem 0;
		color: #c7bca7;
		font-size: 0.94rem;
	}

	/* ---- Kernfunde (kein Kasten, Hairline) --------------------------------- */
	.findings {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.findings > li {
		padding: 1rem 0;
	}
	.findings > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.22);
	}
	.finding-head {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.3rem 0.6rem;
		margin: 0 0 0.35rem;
	}
	.finding-head .emblem {
		width: 1.9rem;
		height: 1.9rem;
		border: 1px solid rgba(190, 139, 58, 0.6);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.finding-topic {
		color: #c7bca7;
		font-style: italic;
	}
	.finding-summary {
		margin: 0;
		color: #e6dbc4;
	}
	.finding-source {
		margin: 0.3rem 0 0;
		color: #9e927f;
		font-size: 0.85rem;
	}

	.queries {
		margin: 0.3rem 0;
		padding-left: 1.2rem;
		font-size: 0.85rem;
	}
	.queries li {
		margin: 0.25rem 0;
	}
	.rejected {
		margin: 0.3rem 0;
		padding-left: 1.2rem;
	}
	.rejected li {
		margin: 0.4rem 0;
		color: #c7bca7;
	}
</style>
