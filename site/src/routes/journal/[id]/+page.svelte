<script>
	let { data } = $props();
	const e = data.entry;
	const pillarNames = {
		A: 'Zukunftsinvestition',
		B: 'Linderung gegenwärtigen Leids',
		C: 'Existenzrisiko-Mitigation',
		D: 'Übersehene Essentials'
	};
</script>

<svelte:head>
	<title>Journal {e.date} — NobleCause.ai</title>
	<meta name="description" content={e.delta_assessment?.slice(0, 160) ?? 'Wart-Dossier'} />
</svelte:head>

<p class="kicker">Journal des Warts · {e.date}</p>
<h1>Wart-Dossier vom {e.date}</h1>

<p class="meta muted">
	Referenz: <a href="/sessions/{e.session_ref}/">Sitzung {e.session_ref}</a> · Modell
	<code>{e.model}</code>
	{#if e.costs?.total != null}
		· Laufkosten {e.costs.total.toFixed(2)} €
	{/if}
</p>

{#if e.actions_run_url}
	<p>
		<a href={e.actions_run_url}>Lauf im Rohzustand verfolgen</a>
		<span class="muted">(GitHub Actions — öffentliches Log)</span>
	</p>
{/if}

<h2>Einberufungs-Entscheid</h2>
<p>
	<strong>{e.convene ? 'Einberufen' : 'Nicht einberufen'}</strong>
	— {e.convene_rationale}
</p>

<h2>Delta-Bewertung</h2>
<p>{e.delta_assessment}</p>

{#if e.findings?.length}
	<h2>Kernfunde</h2>
	{#each e.findings as f, i (i)}
		<article class="finding">
			<p class="kicker">
				Säule {f.pillar} — {pillarNames[f.pillar] ?? f.pillar}
				{#if f.topic}<span class="muted"> · {f.topic}</span>{/if}
			</p>
			<p>{f.summary}</p>
			<p class="source muted">
				Quelle: {f.source}
				{#if f.source_date}<span> ({f.source_date})</span>{/if}
			</p>
		</article>
	{/each}
{/if}

{#if e.search_queries?.length}
	<h2>Suchanfragen</h2>
	<ul>
		{#each e.search_queries as q (q)}
			<li><code>{q}</code></li>
		{/each}
	</ul>
{/if}

{#if e.rejected_findings?.length}
	<h2>Verworfene Funde</h2>
	<ul>
		{#each e.rejected_findings as r, i (i)}
			<li><strong>{r.query_or_topic}</strong> — {r.reason}</li>
		{/each}
	</ul>
{/if}

<details>
	<summary>Vollständiges Dossier (Markdown)</summary>
	<pre>{e.content_md}</pre>
</details>

<style>
	.meta {
		margin: 0 0 1rem;
		font-size: 0.9rem;
	}
	.finding {
		border-left: 3px solid var(--structure);
		padding: 0.3rem 0 0.3rem 1rem;
		margin: 0.8rem 0;
	}
	.source {
		font-size: 0.85rem;
		margin: 0.3rem 0 0;
	}
	pre {
		white-space: pre-wrap;
		font-size: 0.82rem;
		background: var(--code-bg);
		padding: 1rem;
		overflow-x: auto;
	}
</style>
