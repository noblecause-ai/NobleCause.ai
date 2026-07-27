<script>
	// Eine Empfehlung: Konsens und Nicht-Konsens gleichwertig.
	// Zählstand kommt aus convergence (Zählwerk der Sitzung) — hier nur Anzeige.
	// Texte kommen als t-Prop (Locale); die Organisationsbeschreibung nutzt im
	// EN-Modus beschreibung_en (orgEn), falls vorhanden — sonst deutscher Text + Hinweis.
	let { rec, t, lang = 'de', orgEn = {} } = $props();

	let emblem = $derived(t.pillars[rec.pillar]);
	let hasEnglishDescription = $derived(lang === 'en' && Boolean(orgEn?.[rec.organization.id]));
	let description = $derived(
		hasEnglishDescription ? orgEn[rec.organization.id] : rec.organization.description
	);
</script>

<article class="rec-card">
	<header>
		<img src={emblem?.src} alt="" width="48" height="48" loading="lazy" />
		<div>
			<p class="rec-area">{emblem?.label ?? rec.pillarName}</p>
			<h3>{rec.hasConsensus ? rec.organization.name : t.council.noConsensus}</h3>
		</div>
		{#if rec.hasConsensus}<span class="rec-count">{rec.count} {t.common.ofWord} {rec.total}</span>{/if}
	</header>

	{#if rec.hasConsensus}
		<p class="rec-desc" lang={lang === 'en' && !hasEnglishDescription ? 'de' : undefined}>{description}</p>
		{#if lang === 'en' && !hasEnglishDescription && t.common.langHint}
			<small class="rec-lang-hint">{t.common.langHint}</small>
		{/if}
		{#if rec.conditionalCount}
			{#each rec.reservations as reservation (reservation.model)}
				<p class="rec-reservation" lang={lang === 'en' ? 'de' : undefined}>
					{t.council.reservation} ({reservation.model}): {reservation.reservation}
				</p>
			{/each}
			{#if t.common.recordNote}
				<small class="rec-record-note">{t.common.recordNote}</small>
			{/if}
		{/if}
		{#if rec.organization.donationUrl}
			<a class="rec-donate" href={rec.organization.donationUrl}>{t.common.donate}</a>
		{:else}
			<small class="rec-no-donate">{t.common.noDonate}</small>
		{/if}
	{:else}
		<p class="rec-desc">{t.council.noConsensusText}</p>
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
</article>

<style>
	.rec-card {
		display: grid;
		gap: 0.55rem;
		align-content: start;
		padding: 1.1rem 1.2rem;
		background: rgba(13, 18, 19, 0.94);
		border: 1px solid rgba(166, 123, 61, 0.5);
		box-shadow: 0 1rem 2.5rem rgba(0, 0, 0, 0.4);
	}
	header {
		display: grid;
		grid-template-columns: 2.6rem 1fr auto;
		gap: 0.7rem;
		align-items: center;
	}
	header img {
		width: 2.6rem;
		height: 2.6rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		object-fit: cover;
	}
	.rec-area {
		margin: 0;
		color: #a9997d;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	h3 {
		margin: 0.1rem 0 0;
		color: #ead8ae;
		font-size: 1.05rem;
		line-height: 1.25;
	}
	.rec-count {
		color: #dfbd70;
		font: 600 0.85rem ui-sans-serif, system-ui;
		white-space: nowrap;
	}
	.rec-desc {
		margin: 0;
		color: #c7bca7;
		font-size: 0.88rem;
	}
	.rec-lang-hint,
	.rec-record-note {
		color: #9e927f;
		font-size: 0.72rem;
		font-style: italic;
	}
	.rec-reservation {
		margin: 0;
		color: #e0c07f;
		font-size: 0.82rem;
	}
	.rec-donate {
		justify-self: start;
		min-height: 44px;
		display: inline-flex;
		align-items: center;
		color: #e6b45c;
	}
	.rec-no-donate {
		color: #9e927f;
	}
	.rec-votes {
		margin: 0;
		padding-left: 1.2rem;
		color: #c7bca7;
		font-size: 0.88rem;
	}
	.rec-votes a {
		color: #e6b45c;
	}
</style>
