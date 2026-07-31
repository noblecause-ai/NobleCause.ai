<script>
	import { PILLARS, PILLAR_ORDER } from '$lib/pillars.js';

	let { data } = $props();

	const MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
	function fmtDate(iso) {
		const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? '');
		return m ? `${+m[3]}. ${MONTHS[+m[2] - 1]} ${m[1]}` : (iso ?? '');
	}
</script>

<svelte:head>
	<title>Sitzungen — NobleCause.ai</title>
	<meta name="description" content="Alle veröffentlichten Deliberations-Protokolle des NobleCause-Gremiums." />
</svelte:head>

<p class="kicker">Protokolle</p>
<h1>Sitzungen</h1>
<p class="lead">
	Jede Sitzung im Wortlaut — die vier Bereiche mit Zählstand und genannter Organisation. Neueste
	zuerst.
</p>

<nav class="jumpbar" aria-label="Zu einem Bereich springen">
	{#each PILLAR_ORDER as p (p)}
		<a class="jumplink" href="#b-{PILLARS[p].slug}">
			<img class="emblem" src={PILLARS[p].emblem} alt="" width="40" height="40" loading="lazy" />
			{PILLARS[p].label}
		</a>
	{/each}
</nav>

{#if data.sessions.length === 0}
	<p class="muted">
		Noch keine Sitzung veröffentlicht. Die erste Sitzung ist in Vorbereitung — der Ablauf ist unter
		<a href="/idee/">„Wie eine Sitzung funktioniert"</a> beschrieben, das Protokoll-Format liegt im
		<a href="https://github.com/noblecause-ai/NobleCause.ai/tree/master/sessions">Repository</a> fest.
	</p>
{:else}
	<ol class="session-list">
		{#each data.sessions as s, si (s.id)}
			<li>
				<a class="session-head" href="/sitzungen/{s.id}/">
					<span class="session-no">Sitzung {s.number}</span>
					<span class="session-title">{s.title}</span>
					<time class="session-date" datetime={s.date}>{fmtDate(s.date)}</time>
				</a>
				<ul class="pillars">
					{#each PILLAR_ORDER as p (p)}
						{@const cell = s.pillars.find((x) => x.pillar === p)}
						<li class="pillar" id={si === 0 ? `b-${PILLARS[p].slug}` : undefined}>
							<img class="emblem" src={PILLARS[p].emblem} alt="" width="40" height="40" loading="lazy" />
							<span class="rec-area">{PILLARS[p].label}</span>
							{#if cell?.status === 'consensus'}
								<span class="pillar-org">{cell.name}</span>
								{#if cell.count != null}
									<span class="rec-tally">{cell.count} von {cell.total}</span>
								{/if}
							{:else if cell?.status === 'open'}
								<span class="rec-tally split">getrennt</span>
							{:else}
								<span class="mark-none">—</span>
							{/if}
						</li>
					{/each}
				</ul>
				<p class="session-cost">
					{s.total_eur != null ? `${s.total_eur.toFixed(2)} € an API-Aufrufen` : '—'}
				</p>
			</li>
		{/each}
	</ol>
{/if}

<style>
	.lead {
		margin: 0 0 1.4rem;
		color: #c7bca7;
	}
	.session-list {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.session-list > li {
		padding: 1.6rem 0;
	}
	.session-list > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.28);
	}
	.session-head {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.3rem 0.9rem;
		text-decoration: none;
	}
	.session-no {
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.session-title {
		color: #f0d899;
		font-size: 1.15rem;
	}
	.session-head:hover .session-title {
		text-decoration: underline;
		text-underline-offset: 3px;
	}
	.session-date {
		margin-left: auto;
		color: #9e927f;
		font-size: 0.85rem;
	}
	.pillars {
		margin: 1rem 0 0;
		padding: 0;
		list-style: none;
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.7rem 1.4rem;
	}
	@media (min-width: 52rem) {
		.pillars {
			grid-template-columns: repeat(4, minmax(0, 1fr));
		}
	}
	.pillar {
		display: grid;
		grid-template-columns: auto 1fr;
		grid-template-rows: auto auto auto;
		column-gap: 0.6rem;
		align-content: start;
		scroll-margin-top: 6rem;
	}
	.pillar .emblem {
		grid-row: 1 / 3;
		width: 2rem;
		height: 2rem;
		border: 1px solid rgba(190, 139, 58, 0.6);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	/* Adressierung über :target (ohne JS): die angesprungene Zelle leuchtet. */
	.pillar:target .emblem {
		border-color: #e7c881;
		box-shadow:
			0 0 0 1px rgba(213, 166, 87, 0.5),
			0 0 12px rgba(213, 166, 87, 0.3);
	}
	.pillar .rec-area {
		align-self: end;
	}
	.pillar-org {
		grid-column: 2;
		color: #e6dbc4;
		font-size: 0.92rem;
	}
	.pillar .rec-tally,
	.pillar .rec-tally.split,
	.pillar .mark-none {
		grid-column: 2;
		font-size: 0.8rem;
	}
	.session-cost {
		margin: 1rem 0 0;
		color: #9e927f;
		font-size: 0.82rem;
		font-family: ui-sans-serif, system-ui, sans-serif;
	}
</style>
