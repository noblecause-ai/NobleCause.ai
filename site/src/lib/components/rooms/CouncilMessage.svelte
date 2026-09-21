<script>
	import { md } from '$lib/markdown.js';
	import { memberShort, memberSymbol, splitRecordText } from '$lib/live-council.js';
	let { event, members, copy, lang } = $props();
	let member = $derived(members.find(m => m.model === event.model));
	let voting = $derived(['initial_votes', 'final_votes'].includes(event.kind));
	let notice = $derived(['started', 'resumed', 'aborted', 'completed', 'debate_closed'].includes(event.kind));
	let proof = $derived(event.data.provenance);
	const time = value => new Intl.DateTimeFormat(lang, { hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }).format(new Date(value));
</script>

{#if notice}
	<p class="chat-notice" data-event-seq={event.seq} data-kind={event.kind}>
		{copy[event.kind]} <time datetime={event.at}>{time(event.at)} UTC</time>
		{#if event.data.procedure_amendment}
			<a href="https://github.com/noblecause-ai/NobleCause.ai/blob/master/sessions/{encodeURIComponent(event.session_id)}/{encodeURIComponent(event.data.procedure_amendment.path)}">{lang === 'en' ? 'Recorded session amendment' : 'Dokumentierter Sitzungsnachtrag'}</a>
		{/if}
	</p>
{:else if voting}
	<details class="vote-round" data-event-seq={event.seq}>
		<summary>{copy[event.kind]}</summary>
		<p class="vote-note">{copy.votesNote}</p>
		{#each event.data.votes as vote (vote.model)}
			{@const voter = members.find(m => m.model === vote.model)}
			<details class="individual-vote" data-message-model={vote.model}>
				<summary>{voter.label}</summary>
				<div class="chat-prose" lang="de">{@html md(splitRecordText(vote.content_md).prose)}</div>
				<details class="source"><summary>{copy.raw}</summary><p>{vote.model}</p><pre>{vote.content_md}</pre></details>
			</details>
		{/each}
	</details>
{:else}
	<article class="chat-message" data-event-seq={event.seq} data-message-model={event.model} data-role={event.role}>
		<span class="avatar" aria-hidden="true">
			{#if member?.medallion}<img src={member.medallion} alt="" width="28" height="28" />{:else}{member ? memberSymbol(member) : '·'}{/if}
		</span>
		<div class="message-body">
			<div class="message-author">{member ? memberShort(member) : copy.council}<span>{event.role === 'chair' ? copy.chair : copy.member}</span><time datetime={event.at}>{time(event.at)} UTC</time></div>
			{#if event.kind === 'summary'}<p class="summary-label">{copy.summary}</p>{/if}
			{#if event.data.word_limit_observation}
				<p class="summary-label">{lang === 'en' ? 'Word limit exceeded' : 'Wortgrenze überschritten'}: {event.data.word_limit_observation.word_count} / {event.data.word_limit_observation.limit}. {lang === 'en' ? 'Original retained under the recorded session amendment.' : 'Original gemäß dokumentiertem Sitzungsnachtrag erhalten.'}</p>
			{/if}
			<div class="chat-bubble chat-prose" lang="de">{@html md(event.prose)}</div>
			<details class="source">
				<summary>{copy.raw} · #{event.seq}</summary>
				<p>{member?.label} · {event.model}</p>
				{#if proof}<p>{proof.upstream_provider} · {proof.endpoint} · {proof.quantization === 'unknown' ? copy.unknown : proof.quantization}</p>{/if}
				<p>{copy.provenance}</p>
				{#if member?.medallion_source_model && member.medallion_source_model !== member.model}<p>{copy.sourceSymbol}: {member.medallion_source_model}</p>{/if}
				<pre lang="de">{event.content_md}</pre>
			</details>
		</div>
	</article>
{/if}

<style>
	.chat-message { display: grid; grid-template-columns: 28px minmax(0,1fr); gap: 9px; margin: 0 0 1.3rem; max-width: 96%; }
	.message-body { min-width: 0; }
	.avatar { width: 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; border: 1px solid #a4814e; overflow: hidden; color: #d0ac69; background: #202624; font-size: .8rem; margin-top: 3px; }
	.avatar img { width: 100%; height: 100%; object-fit: cover; }
	.message-author { display: flex; align-items: baseline; gap: .5rem; flex-wrap: wrap; font: 500 .75rem/1.5 system-ui,sans-serif; color: #d0ac69; margin-bottom: .4rem; }
	.message-author span, time { font: 400 .69rem/1.5 system-ui,sans-serif; color: #b6ac95; }
	.message-author time { margin-left: auto; }
	.chat-bubble { background: #1d2525; border-radius: 3px 13px 13px 13px; padding: .8rem 1rem; }
	[data-role='chair'] .chat-bubble { background: #29291f; }
	.chat-prose { color: #ece2cd; font: 400 1rem/1.6 Georgia,'Iowan Old Style',serif; overflow-wrap: anywhere; }
	.chat-prose :global(p) { margin: 0 0 .7rem; }
	.chat-prose :global(p:last-child) { margin-bottom: 0; }
	.chat-prose :global(strong) { font-weight: 600; color: #dec28b; }
	.chat-prose :global(h1), .chat-prose :global(h2), .chat-prose :global(h3) { font: 500 1.05rem/1.4 Georgia,serif; color: #dec28b; margin: 1rem 0 .5rem; padding: 0; border: 0; }
	.chat-prose :global(a) { color: #e2bd7a; text-underline-offset: .15em; }
	.chat-prose :global(img) { max-width: 100%; height: auto; }
	.chat-prose :global(pre) { white-space: pre-wrap; }
	.chat-prose :global(table) { display: block; overflow-x: auto; }
	.source { margin-top: .3rem; font: .69rem/1.5 system-ui,sans-serif; color: #b6ac95; }
	summary { cursor: pointer; padding: .35rem 0; min-height: 30px; }
	.source p { margin: .45rem 0; overflow-wrap: anywhere; }
	pre { white-space: pre-wrap; overflow-wrap: anywhere; font: .75rem/1.6 ui-monospace,monospace; color: #d5cbb7; }
	.chat-notice { color: #c7b898; text-align: center; font: .75rem/1.6 system-ui,sans-serif; margin: 1rem 0 1.3rem; }
	.chat-notice time { display: block; }
	.chat-notice[data-kind='aborted'] { color: #edc389; }
	.vote-round { margin: 1rem 0 1.4rem 37px; border-block: 1px solid #494436; color: #d0ac69; font: .8rem/1.5 system-ui,sans-serif; }
	.vote-round > summary { padding: .65rem 0; }
	.vote-note { color: #b6ac95; font-size: .75rem; }
	.individual-vote { margin: .5rem 0; }
	.summary-label { color: #d0ac69; margin: 0 0 .5rem; font-size: .8rem; }
	@media (max-width: 600px) {
		.chat-message { grid-template-columns: 23px minmax(0,1fr); gap: 7px; max-width: 100%; }
		.avatar { width: 23px; height: 23px; }
		.chat-bubble { padding: .7rem .75rem; }
		.vote-round { margin-left: 30px; }
		summary { min-height: 40px; }
	}
</style>
