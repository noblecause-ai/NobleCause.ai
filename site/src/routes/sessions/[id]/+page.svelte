<script>
	let { data } = $props();
	const s = data.session;
	const pillarNames = {
		A: 'Zukunftsinvestition',
		B: 'Linderung gegenwärtigen Leids',
		C: 'Existenzrisiko-Mitigation',
		D: 'Übersehene Essentials'
	};
	const roundTitles = {
		initial_vote: 'Einzelvotum (unabhängig)',
		final_vote: 'Schlussvotum (nach Gegenlese)'
	};
	const labelOf = (model) => s.participants.find((p) => p.model === model)?.label ?? model;
</script>

<svelte:head>
	<title>Sitzung {s.number}: {s.title} — NobleCause.ai</title>
	<meta name="description" content={s.question} />
</svelte:head>

<p class="kicker">Protokoll · Sitzung {s.number} · {s.date}</p>
<h1>{s.title}</h1>

<h2>Fragestellung</h2>
<blockquote>{s.question}</blockquote>

<h2>Teilnehmer</h2>
<table>
	<thead>
		<tr><th>Familie</th><th>Modell (API-Version)</th></tr>
	</thead>
	<tbody>
		{#each s.participants as p (p.model)}
			<tr>
				<td>{p.family}</td>
				<td><strong>{p.label}</strong> · <code>{p.model}</code></td>
			</tr>
		{/each}
	</tbody>
</table>

<h2>Prompts</h2>
<p class="muted">Wörtlich, wie an die APIs gesendet.</p>
{#each [['System', s.prompts.system], ['Runde 1', s.prompts.round1], ['Runde 2', s.prompts.round2]] as [name, text] (name)}
	{#if text}
		<details>
			<summary>{name}-Prompt</summary>
			<pre>{text}</pre>
		</details>
	{/if}
{/each}

{#each s.rounds as round (round.round)}
	<h2>Runde {round.round} — {roundTitles[round.kind] ?? round.kind}</h2>
	{#each round.votes as vote (vote.model)}
		<details open={round.kind === 'final_vote'}>
			<summary>
				<strong>{labelOf(vote.model)}</strong>
				{#if vote.confidence != null}
					<span class="muted">· Konfidenz {Math.round(vote.confidence * 100)} %</span>
				{/if}
			</summary>
			<div class="vote">
				<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
				{@html vote.content_html}
			</div>
		</details>
	{/each}
{/each}

<h2>Dissens</h2>
<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
{@html s.dissent_html}

<h2>Empfehlungen</h2>
{#each s.recommendations as rec, i (i)}
	<div class="rec">
		<p class="kicker">Säule {rec.pillar} — {pillarNames[rec.pillar] ?? ''}</p>
		<h3>
			{rec.title}
			{#if rec.confidence != null}
				<span class="muted conf">Konfidenz {Math.round(rec.confidence * 100)} %</span>
			{/if}
		</h3>
		<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
		{@html rec.rationale_html}
		{#if rec.donation_url}
			<p>
				<a href={rec.donation_url}>Offizieller Spendenweg: {rec.organization}</a>
				<span class="muted">(externer Link — durch NobleCause.ai fließt kein Geld)</span>
			</p>
		{/if}
	</div>
{/each}

<h2>Kosten</h2>
<table>
	<thead>
		<tr><th>Modell</th><th>Input-Tokens</th><th>Output-Tokens</th><th>USD</th><th>EUR</th></tr>
	</thead>
	<tbody>
		{#each s.costs.by_model as c (c.model)}
			<tr>
				<td>{labelOf(c.model)}</td>
				<td>{c.input_tokens.toLocaleString('de-CH')}</td>
				<td>{c.output_tokens.toLocaleString('de-CH')}</td>
				<td>{c.usd.toFixed(4)}</td>
				<td>{c.eur.toFixed(4)}</td>
			</tr>
		{/each}
		<tr>
			<td><strong>Gesamt</strong></td>
			<td></td>
			<td></td>
			<td></td>
			<td><strong>{s.costs.total.toFixed(2)} €</strong></td>
		</tr>
	</tbody>
</table>
<p class="muted">
	Umrechnungskurs USD→EUR: {s.costs.fx_rate_usd_eur}. Rohantworten aller API-Calls:
	<a href="https://github.com/noblecause-ai/NobleCause.ai/tree/master/sessions/{s.id}/raw"
		>sessions/{s.id}/raw im Repository</a
	>.
</p>

<style>
	details {
		border: 1px solid #d8d2c4;
		background: #faf8f3;
		padding: 0.55rem 0.9rem;
		margin: 0.6rem 0;
	}
	summary {
		cursor: pointer;
	}
	pre {
		white-space: pre-wrap;
		font-family: ui-monospace, 'SF Mono', Menlo, monospace;
		font-size: 0.78rem;
		line-height: 1.55;
		margin: 0.7rem 0 0.3rem;
	}
	.vote {
		margin-top: 0.5rem;
		border-top: 1px solid #e2ddd1;
		padding-top: 0.3rem;
	}
	.rec {
		border-left: 3px solid #1a1916;
		padding-left: 1rem;
		margin: 1.4rem 0;
	}
	.rec h3 {
		margin: 0 0 0.3rem;
		font-size: 1.05rem;
	}
	.conf {
		font-size: 0.8rem;
		font-weight: 400;
		margin-left: 0.5rem;
	}
</style>
