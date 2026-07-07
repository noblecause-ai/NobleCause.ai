<script>
	import ResultCard from '$lib/components/ResultCard.svelte';

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
	<meta name="description" content={s.summary ?? s.question} />
</svelte:head>

<p class="kicker">Protokoll · Sitzung {s.number} · {s.date}</p>
<h1>{s.title}</h1>
<blockquote class="question">{s.question}</blockquote>

<h2>Ergebnis</h2>
{#each s.recommendations as rec (rec.pillar)}
	<ResultCard {rec} pillarName={pillarNames[rec.pillar] ?? ''} />
{/each}

{#if s.summary}
	<h2>Kurzfassung</h2>
	<p class="summary">{s.summary}</p>
{/if}

{#if s.dissent_highlights?.length}
	<h2>Dissens im Kern</h2>
	<ul class="highlights">
		{#each s.dissent_highlights as point (point)}
			<li>{point}</li>
		{/each}
	</ul>
{/if}

<h2>Vollprotokoll</h2>
<p class="muted">Standardmäßig eingeklappt — vollständige Transparenz auf Wunsch.</p>

<details>
	<summary>Fragestellung & Teilnehmer</summary>
	<blockquote>{s.question}</blockquote>
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
</details>

<details>
	<summary>Prompts (wörtlich)</summary>
	{#each [['System', s.prompts.system], ['Runde 1', s.prompts.round1], ['Runde 2', s.prompts.round2]] as [name, text] (name)}
		{#if text}
			<h3>{name}</h3>
			<pre>{text}</pre>
		{/if}
	{/each}
</details>

{#each s.rounds as round (round.round)}
	<details>
		<summary>Runde {round.round} — {roundTitles[round.kind] ?? round.kind}</summary>
		{#each round.votes as vote (vote.model)}
			<h3>
				{labelOf(vote.model)}
				{#if vote.confidence != null}
					<span class="muted">· Konfidenz {Math.round(vote.confidence * 100)} %</span>
				{/if}
			</h3>
			<div class="vote">
				<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
				{@html vote.content_html}
			</div>
		{/each}
	</details>
{/each}

<details>
	<summary>Dissens (Rohfassung)</summary>
	<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
	{@html s.dissent_html}
</details>

<p class="footnote">
	Diese Sitzung kostete {s.costs.total.toFixed(2)} € an API-Aufrufen — vollständige Aufschlüsselung
	und Rohantworten im
	<a href="https://github.com/noblecause-ai/NobleCause.ai/tree/master/sessions/{s.id}"
		>Repository (sessions/{s.id}/)</a
	>.
</p>

<style>
	.question {
		margin: 0.5rem 0 1.5rem;
		font-size: 0.95rem;
	}
	.summary {
		margin: 0;
	}
	.highlights {
		margin: 0.5rem 0 0;
		padding-left: 1.2rem;
	}
	.highlights li {
		margin: 0.5rem 0;
	}
	details {
		border: 1px solid var(--line);
		background: var(--card-bg);
		padding: 0.55rem 0.9rem;
		margin: 0.6rem 0;
	}
	summary {
		cursor: pointer;
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.88rem;
	}
	h3 {
		margin: 1rem 0 0.3rem;
		font-size: 0.95rem;
	}
	pre {
		white-space: pre-wrap;
		font-family: ui-monospace, 'SF Mono', Menlo, monospace;
		font-size: 0.78rem;
		line-height: 1.55;
		margin: 0.5rem 0;
	}
	.vote {
		margin: 0.3rem 0 0.8rem;
		border-top: 1px solid var(--line);
		padding-top: 0.3rem;
		font-size: 0.92rem;
	}
	.footnote {
		margin-top: 2.5rem;
		padding-top: 1rem;
		border-top: 1px solid var(--line);
		font-size: 0.82rem;
		color: var(--muted);
		font-family: ui-sans-serif, system-ui, sans-serif;
	}
</style>
