<script>
	let { data } = $props();

	const MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
	function fmtDate(iso) {
		const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? '');
		return m ? `${+m[3]}. ${MONTHS[+m[2] - 1]} ${m[1]}` : (iso ?? '');
	}
	// Lauf-Typ (Konzept §6): die Bestell-Kommission erscheint als EIGENER Typ,
	// nicht als Sitzung gezählt. Steward-Einberufungen und Vertretungsläufe
	// ebenso kenntlich.
	function kind(e) {
		if (e.type === 'commission') return { slug: 'commission', label: 'Kommission' };
		if (e.model === null && e.convene) return { slug: 'steward', label: 'Einberufung' };
		if (e.deputation) return { slug: 'deputation', label: 'Vertretung' };
		return { slug: 'research', label: 'Recherche' };
	}
	const title = (e) =>
		e.model_label ??
		(e.type === 'commission' ? 'Selbstdarstellungen bestellt' : 'Einberufung durch den Steward');
</script>

<svelte:head>
	<title>Journal des Warts — NobleCause.ai</title>
	<meta
		name="description"
		content="Zeitleiste der Wart-Läufe: Suchanfragen, Kernfunde, Delta-Bewertung und Einberufungs-Entscheidungen."
	/>
</svelte:head>

<p class="kicker">Wart · Wöchentliche Evidenzprüfung</p>
<h1>Journal des Warts</h1>
<p class="lead">
	Der Wart (Fable, <code>claude-fable-5</code>) prüft wöchentlich per Web-Recherche die Evidenzlage
	zu den jüngsten Empfehlungen. Jeder Lauf dokumentiert Suchanfragen, Kernfunde mit Quellen,
	verworfene Funde und den Einberufungs-Entscheid — vollständig veröffentlicht. Die Bestell-Kommission
	steht hier als eigener Typ, nicht als Sitzung gezählt.
</p>

{#if data.entries.length === 0}
	<p class="muted">Noch kein Journal-Eintrag veröffentlicht.</p>
{:else}
	<ol class="journal-list">
		{#each data.entries as e (e.id)}
			{@const k = kind(e)}
			<li>
				<a class="entry-head" href="/journal/{e.id}/">
					<span class="entry-type type-{k.slug}">{k.label}</span>
					<span class="entry-title">{title(e)}</span>
					<time class="entry-date" datetime={e.date}>{fmtDate(e.date)}</time>
				</a>
				<p class="entry-meta">
					{#if e.convene}
						<span class="convene-yes">Einberufung empfohlen</span>
					{:else}
						keine Einberufung
					{/if}
					{#if e.findings_count}· {e.findings_count} Fund{e.findings_count === 1 ? '' : 'e'}{/if}
					{#if e.queries_count}· {e.queries_count} Suchanfrage{e.queries_count === 1 ? '' : 'n'}{/if}
					{#if e.session_ref}· zu <a href="/sessions/{e.session_ref}/">Sitzung {e.session_ref}</a>{/if}
				</p>
				{#if e.convene_rationale}
					<p class="entry-rationale">{e.convene_rationale}</p>
				{/if}
			</li>
		{/each}
	</ol>
{/if}

<style>
	.lead {
		margin: 0 0 1.8rem;
		color: #c7bca7;
	}
	.journal-list {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.journal-list > li {
		padding: 1.3rem 0;
	}
	.journal-list > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.28);
	}
	.entry-head {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.4rem 0.8rem;
		text-decoration: none;
	}
	.entry-type {
		padding: 0.12rem 0.5rem;
		border: 1px solid rgba(166, 123, 61, 0.45);
		border-radius: 999px;
		color: #c9ab6e;
		font: 600 0.6rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.09em;
		text-transform: uppercase;
	}
	.type-commission {
		border-color: rgba(139, 183, 202, 0.6);
		color: #8bb7ca;
	}
	.type-steward {
		border-color: rgba(215, 170, 85, 0.6);
		color: #e7c881;
	}
	.entry-title {
		color: #f0d899;
		font-size: 1.08rem;
	}
	.entry-head:hover .entry-title {
		text-decoration: underline;
		text-underline-offset: 3px;
	}
	.entry-date {
		margin-left: auto;
		color: #9e927f;
		font-size: 0.85rem;
	}
	.entry-meta {
		margin: 0.5rem 0 0;
		color: #9e927f;
		font-size: 0.9rem;
	}
	.convene-yes {
		color: #e7c881;
	}
	.entry-rationale {
		margin: 0.35rem 0 0;
		color: #c7bca7;
		font-size: 0.94rem;
	}
</style>
