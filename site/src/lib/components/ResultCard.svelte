<script>
	import PillarBadge from './PillarBadge.svelte';
	import ConvergenceDots from './ConvergenceDots.svelte';
	import ConfidenceBar from './ConfidenceBar.svelte';

	let { rec, pillarName, compact = false } = $props();
</script>

{#if rec.has_consensus}
	<article class="result-card" class:compact>
		<div class="card-head">
			<PillarBadge pillar={rec.pillar} />
			<div class="card-meta">
				<p class="kicker">Säule {rec.pillar} — {pillarName}</p>
				{#if rec.convergence}
					<ConvergenceDots count={rec.convergence.count} total={rec.convergence.total} />
				{/if}
			</div>
		</div>
		<h3>{rec.title}</h3>
		<p class="org">{rec.organization}</p>
		{#if rec.confidence != null}
			<ConfidenceBar confidence={rec.confidence} />
		{/if}
		{#if rec.convergence?.conditional_count}
			<p class="conditional-note">
				{rec.convergence.conditional_count} von {rec.convergence.count} Voten konditional
				(Vorbehalt, kein Widerruf der Empfehlung):
			</p>
			<ul class="reservations">
				{#each (rec.convergence.votes ?? []).filter((v) => v.conditional) as v (v.model)}
					<li><strong>{v.model}:</strong> {v.reservation}</li>
				{/each}
			</ul>
		{/if}
		{#if rec.donation_url && !compact}
			<p class="donate">
				<a href={rec.donation_url}>Offizieller Spendenweg</a>
				<span class="muted">(extern — durch NobleCause.ai fließt kein Geld)</span>
			</p>
		{:else if !rec.donation_url && !compact}
			<p class="donate muted">Kein offizieller Spendenweg auffindbar.</p>
		{/if}
	</article>
{:else}
	<div class="split-row" class:compact>
		<div class="split-label">
			<PillarBadge pillar={rec.pillar} />
			<span>Säule {rec.pillar} — {pillarName}</span>
		</div>
		<div class="split-votes">
			{#each rec.individual_votes ?? [] as vote (vote.model)}
				<div class="split-vote">
					<strong>{vote.organization}</strong> — {vote.title}
					<span class="muted">({vote.model}{#if vote.confidence != null}, {Math.round(vote.confidence * 100)} %{/if})</span>
				</div>
			{/each}
		</div>
	</div>
{/if}

<style>
	.result-card {
		border: 1px solid var(--line);
		padding: 1rem 1.1rem;
		margin: 0.8rem 0;
		background: var(--card-bg);
	}
	.result-card.compact {
		padding: 0.85rem 1rem;
		margin: 0.5rem 0;
	}
	.card-head {
		display: flex;
		gap: 0.7rem;
		align-items: flex-start;
		margin-bottom: 0.5rem;
		color: var(--structure);
	}
	.card-meta {
		flex: 1;
	}
	.card-meta .kicker {
		margin: 0 0 0.25rem;
	}
	h3 {
		margin: 0 0 0.25rem;
		font-size: 1.05rem;
	}
	.org {
		margin: 0 0 0.5rem;
		color: var(--muted);
		font-size: 0.92rem;
	}
	.donate {
		margin: 0.6rem 0 0;
		font-size: 0.85rem;
	}
	.conditional-note {
		margin: 0.5rem 0 0.2rem;
		font-size: 0.85rem;
		color: var(--structure);
	}
	.reservations {
		margin: 0 0 0.2rem;
		padding-left: 1.1rem;
		font-size: 0.85rem;
		color: var(--muted);
	}
	.reservations li {
		margin: 0.2rem 0;
	}
	.split-row {
		border-left: 3px solid var(--line-strong);
		padding: 0.6rem 0 0.6rem 1rem;
		margin: 0.8rem 0;
	}
	.split-label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.78rem;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: var(--muted);
		margin-bottom: 0.4rem;
	}
	.split-vote {
		font-size: 0.92rem;
		margin: 0.35rem 0;
	}
</style>
