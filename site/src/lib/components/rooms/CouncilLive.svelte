<script>
	import { onMount, tick, untrack } from 'svelte';
	import CouncilMessage from './CouncilMessage.svelte';
	import { conversation, feedIsStale, liveCopy, memberShort, memberSymbol, nearBottom, readSnapshot } from '$lib/live-council.js';
	import { orbitStateAt, ORBIT, TAU } from '$lib/orbit.js';

	let { lang = 'de', feed = $bindable(null), open = $bindable(false) } = $props();
	let root = $state(null), log = $state(null), dock = $state(null), windowElement = $state(null);
	let connectionError = $state(false), pending = $state(null), following = $state(true);
	let announce = $state(false), memberNotice = $state(''), now = $state(Date.now());
	let lastContributionAt = $state(0);
	let copy = $derived(liveCopy[lang]);
	let messages = $derived(feed ? conversation(feed.record) : []);
	let members = $derived(feed?.session.participants ?? []);
	let sessionId = $derived(feed?.session.id ?? null);
	let tail = $derived(feed?.record.events.at(-1));
	let stale = $derived(feed ? feedIsStale(feed, now) : false);
	let interrupted = $derived(connectionError || stale);
	let activeModel = $derived(!interrupted && (tail?.kind === 'waiting' || now - lastContributionAt < 8000)
		&& ['waiting', 'moderation', 'contribution', 'summary'].includes(tail?.kind) ? tail.model : null);
	let activeMember = $derived(members.find(m => m.model === activeModel));
	let waiting = $derived(tail?.kind === 'waiting');
	let status = $derived(interrupted ? (stale ? copy.stale : copy.error)
		: memberNotice || (tail?.kind === 'completed' ? copy.completed : tail?.kind === 'aborted' ? copy.aborted
			: activeMember ? `${memberShort(activeMember)} ${waiting ? copy.waiting : copy.speaking}`
				: tail?.model ? `${copy.last}: ${memberShort(memberById(tail.model))}` : copy.phases[tail?.phase]));
	let modeLabel = $derived(feed ? copy[feed.mode] : '');
	let money = $derived(new Intl.NumberFormat(lang, { minimumFractionDigits: 2, maximumFractionDigits: 4 }));
	const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	const memberById = id => members.find(m => m.model === id);

	function toLatest(smooth = false) {
		if (!log) return;
		following = true;
		log.scrollTo({ top: log.scrollHeight, behavior: smooth && !reduced() ? 'smooth' : 'instant' });
	}
	async function accept(snapshot) {
		const first = !feed;
		const follow = following;
		if (snapshot.record.events.at(-1)?.seq !== feed?.record.events.at(-1)?.seq) lastContributionAt = Date.now();
		feed = snapshot;
		connectionError = false;
		memberNotice = '';
		await tick();
		if (first) { positionCoins(); open = true; }
		if (first || follow) toLatest();
		announce = true;
	}
	onMount(() => {
		let disposed = false, timer, request;
		const clock = setInterval(() => { now = Date.now(); }, 5000);
		async function poll() {
			request = new AbortController();
			const timeout = setTimeout(() => request.abort(), 10000);
			try {
				const snapshot = await readSnapshot(feed, { signal: request.signal });
				if (disposed) return;
				if (snapshot && feed && snapshot.session.id !== feed.session.id) { pending = snapshot; connectionError = false; }
				else if (snapshot) await accept(snapshot);
				else connectionError = false;
			} catch {
				if (!disposed) connectionError = true;
			} finally {
				clearTimeout(timeout);
				if (!disposed) timer = setTimeout(poll, document.hidden ? 15000 : 3000);
			}
		}
		poll();
		return () => { disposed = true; clearInterval(clock); clearTimeout(timer); request?.abort(); };
	});

	async function toggleOpen(value) {
		open = value;
		await tick();
		if (value && following) toLatest();
		root.querySelector(value ? '.chat-close' : '.chat-open')?.focus({ preventScroll: true });
	}
	async function jumpToMember(id) {
		if (!open) { open = true; await tick(); }
		const candidates = [...root.querySelectorAll('[data-message-model]')].filter(el => el.dataset.messageModel === id);
		const last = candidates.at(-1);
		if (!last) { memberNotice = `${memberById(id).label}: ${copy.noSpeech}`; return; }
		if (last.closest('.vote-round')) {
			last.closest('.vote-round').open = true;
			last.open = true;
		}
		following = false;
		log.scrollTo({ top: log.scrollTop + last.getBoundingClientRect().top - log.getBoundingClientRect().top - 10,
			behavior: 'instant' });
	}

	let orbitStarted = 0;
	function positionCoins(time = performance.now()) {
		if (!root || !dock || !windowElement) return;
		const coins = root.querySelectorAll('.chat-member');
		const box = root.getBoundingClientRect();
		const width = window.innerWidth, height = window.innerHeight;
		const scale = Math.max(width / 1672, height / 941);
		const desktop = width >= 1200;
		const cx = desktop ? (width - 1672 * scale) / 2 + 843 * scale : width / 2;
		const cy = desktop ? 677.5 * scale : height * .69;
		const a = desktop ? 251 * scale : Math.min(width * .29, 220);
		const b = desktop ? 66 * scale : 55;
		coins.forEach((coin, index) => {
			let x, y, size = 1;
			if (open) {
				x = windowElement.offsetLeft + dock.offsetLeft + dock.clientWidth * (index + .5) / coins.length - coin.offsetWidth / 2;
				y = windowElement.offsetTop + dock.offsetTop + 6;
			} else {
				const t = reduced() ? ORBIT.flyDelay + ORBIT.flyDur : time - orbitStarted + ORBIT.flyDelay + ORBIT.flyDur;
				const orbit = orbitStateAt(t, Math.PI / 2 + index * TAU / coins.length);
				x = cx + a * orbit.cos - box.left - coin.offsetWidth / 2;
				y = cy + b * orbit.sin - box.top - coin.offsetHeight / 2;
				size = .78 + .2 * orbit.depth;
			}
			coin.style.transform = `translate(${x}px,${y}px) scale(${size})`;
		});
	}
	function measure() {
		if (!root) return;
		const hero = root.closest('.room-hero');
		const box = root.getBoundingClientRect();
		root.style.setProperty('--chat-top', `${box.top + window.scrollY}px`);
		hero.style.setProperty('--live-stage-height', `${root.offsetTop + root.offsetHeight + 35}px`);
		positionCoins();
	}
	$effect(() => {
		if (!root || !sessionId) return;
		let raf, stopped = false;
		orbitStarted = performance.now();
		const observer = new ResizeObserver(measure);
		observer.observe(root);
		const header = root.closest('.room-hero').querySelector('.room-plaque');
		observer.observe(header);
		const frame = time => {
			if (stopped) return;
			if (!document.hidden && root.closest('.room-hero').getBoundingClientRect().bottom > 0) positionCoins(time);
			raf = requestAnimationFrame(frame);
		};
		untrack(measure);
		raf = requestAnimationFrame(frame);
		window.addEventListener('resize', measure);
		return () => { stopped = true; cancelAnimationFrame(raf); observer.disconnect(); window.removeEventListener('resize', measure); };
	});
	$effect(() => {
		const isOpen = open;
		if (!root) return;
		const coins = root.querySelectorAll('.chat-member');
		coins.forEach(coin => { coin.style.transition = reduced() ? 'none' : 'transform .8s cubic-bezier(.22,.75,.22,1)'; });
		positionCoins();
		const timer = setTimeout(() => { coins.forEach(coin => { coin.style.transition = 'none'; }); }, 850);
		if (isOpen) tick().then(measure);
		return () => clearTimeout(timer);
	});
</script>

{#if feed}
	<div class="live-council" data-open={open} data-mode={feed.mode} bind:this={root}>
		<section class="chat-window" aria-label={copy.title} aria-hidden={!open} inert={!open} bind:this={windowElement}>
			<header class="chat-head"><div><h2>{copy.title}</h2><p>{copy.session(feed.session.number)} · {copy.chair} {memberShort(memberById(feed.session.chair.model))}</p></div><button class="chat-close" type="button" onclick={() => toggleOpen(false)}>{copy.close}</button></header>
			<div class="chat-dock" bind:this={dock} aria-hidden="true"></div>
			<div class="chat-topic"><span>{copy.phases[tail?.phase]}<span class="chat-mode">{modeLabel}</span></span><details class="session-info"><summary>{feed.session.title}</summary><p lang="de">{feed.session.question}</p><p>{copy.recordNote}</p></details></div>
			{#if interrupted}<p class="connection-note" role="status">{stale ? copy.stale : copy.error}</p>{/if}
			{#if pending}<button class="new-session" type="button" onclick={() => { const next = pending; pending = null; following = true; accept(next); }}>{copy.newSession}: {pending.session.title}</button>{/if}
			<div class="chat-scroll-wrap">
				<div class="chat-log" bind:this={log} role="log" aria-label={copy.title} aria-live={announce && open ? 'polite' : 'off'} aria-relevant="additions" aria-atomic="false" onscroll={() => { following = nearBottom(log); }}>
					<p class="chat-date">{feed.session.date} · {modeLabel}</p>
					{#each messages as event (event.seq)}<CouncilMessage {event} {members} {copy} {lang} />{/each}
				</div>
				{#if !following}<button class="chat-jump" type="button" onclick={() => toLatest(true)}>{copy.latest}</button>{/if}
			</div>
			<footer class="chat-footer"><p class="chat-status" aria-live="polite"><span class:lit={!!activeModel} aria-hidden="true"></span>{status}</p><details class="chat-costs"><summary>{money.format(Number(feed.costs.total_usd))} {copy.credits}</summary><div class="cost-panel"><p>{copy.costs}</p>{#each feed.costs.by_model as cost (cost.model)}<p>{memberById(cost.model).label}<span>{money.format(Number(cost.usd))}</span></p>{/each}{#if Number(feed.costs.unassigned_usd) > .000001}<p>{copy.unassigned}<span>{money.format(Number(feed.costs.unassigned_usd))}</span></p>{/if}{#if feed.costs.unresolved}<p>{copy.unresolved}</p>{/if}<a href="/live/sessions/{feed.session.id}/events.json">{copy.archive}</a></div></details></footer>
		</section>
		<div class="chat-roster" aria-label={copy.recordNote}>
			{#each members as member (member.model)}<button class="chat-member" type="button" data-model={member.model} data-active={member.model === activeModel} data-waiting={waiting} aria-label={`${member.label} · ${member.model === feed.session.chair.model ? copy.chair : copy.member}`} onclick={() => jumpToMember(member.model)}><span class="chat-coin" aria-hidden="true">{#if member.medallion}<img src={member.medallion} alt="" width="53" height="53" />{:else}{memberSymbol(member)}{/if}</span><span class="chat-member-name">{memberShort(member)}</span><span class="chat-member-role">{member.model === activeModel ? (waiting ? copy.waiting : copy.speaking) : member.model === feed.session.chair.model ? copy.chair : ''}</span></button>{/each}
		</div>
		{#if !open}<button class="chat-open" type="button" onclick={() => toggleOpen(true)}>{copy.open}<span>{modeLabel}{#if interrupted} · {copy.aborted}{/if}</span></button>{/if}
	</div>
{:else if connectionError}
	<p class="feed-unavailable" role="status">{copy.unavailable}</p>
{/if}
<noscript><p class="no-live-js">{copy.nojs}</p></noscript>

<style>
	.live-council { --chat-top: 14rem; position: relative; z-index: 4; width: 100vw; max-width: 100%; min-width: 0; pointer-events: none; color: #ece2cd; font-family: Georgia,'Iowan Old Style',serif; margin-top: .9rem; }
	.live-council * { box-sizing: border-box; }
	button, summary { cursor: pointer; }
	button { font: inherit; }
	.chat-window { position: relative; width: min(44rem,calc(100% - 2rem)); height: clamp(30rem,calc(100svh - var(--chat-top) - 2.4rem),39rem); margin: 0 auto 1rem; pointer-events: auto; background: #11191a; border: 1px solid #ac844b; border-radius: 15px 15px 8px 8px; box-shadow: 0 0 0 4px #0b1011,0 0 0 5px #ac844b,0 28px 60px #000b; display: flex; flex-direction: column; transition: opacity .4s ease, transform .65s cubic-bezier(.22,.75,.22,1); transform-origin: 50% 90%; }
	.chat-window::before,.chat-window::after { content: '✦'; position: absolute; top: -12px; color: #d0ac69; font-size: 18px; line-height: 1; }
	.chat-window::before { left: 20px; }.chat-window::after { right: 20px; }
	[data-open='false'] .chat-window { opacity: 0; transform: translateY(100px) scale(.85); pointer-events: none; }
	.chat-head { padding: 1rem 1.25rem .6rem; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
	h2 { margin: 0; padding: 0; border: 0; font: 400 1.35rem/1.2 Georgia,serif; color: #ece2cd; }
	.chat-head p { margin: .3rem 0 0; font: .69rem/1.5 system-ui,sans-serif; color: #b6ac95; }
	.chat-close { color: #e0d5bd; border: 1px solid #494436; border-radius: 5px; background: transparent; padding: .5rem .65rem; min-height: 38px; font: .69rem/1.4 system-ui,sans-serif; white-space: nowrap; }
	.chat-dock { height: 104px; flex: none; margin: 0 20px; border-bottom: 1px solid #494436; }
	.chat-topic { min-width: 0; padding: .6rem 1.25rem; font: .69rem/1.5 system-ui,sans-serif; color: #b6ac95; flex: none; }
	.chat-topic > span { display: flex; justify-content: space-between; gap: 10px; }
	.chat-mode { color: #d0ac69; white-space: nowrap; }
	.session-info { margin-top: .2rem; color: #d8cbb1; }
	.session-info summary { white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }
	.session-info[open] summary { white-space: normal; }
	.session-info[open] { max-height: 8rem; overflow-y: auto; }
	.chat-scroll-wrap { position: relative; min-height: 0; flex: 1; }
	.chat-log { height: 100%; padding: .5rem 1.25rem 1.1rem; overflow-y: auto; overscroll-behavior-y: contain; overflow-anchor: none; scrollbar-width: thin; scrollbar-color: #a4814e transparent; }
	.chat-date { text-align: center; font: .69rem/1.5 system-ui,sans-serif; color: #b6ac95; margin: .2rem 0 1.2rem; }
	.chat-jump { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); border: 1px solid #ac844b; background: #11191a; color: #ece2cd; padding: .6rem .9rem; border-radius: 25px; font: .75rem/1.4 system-ui,sans-serif; box-shadow: 0 5px 18px #000b; white-space: nowrap; }
	.chat-footer { display: flex; align-items: center; justify-content: space-between; gap: 8px 14px; flex-wrap: wrap; padding: .7rem 1.1rem; border-top: 1px solid #494436; flex: none; min-height: 55px; }
	.chat-status { display: flex; align-items: center; gap: 8px; margin: 0; font: .75rem/1.5 system-ui,sans-serif; color: #b6ac95; flex: 1 1 180px; }
	.chat-status > span { width: 6px; height: 6px; flex: none; border-radius: 50%; background: #756d5d; }
	.chat-status .lit { background: #d0ac69; box-shadow: 0 0 10px #d0ac69; }
	.chat-costs { font: .69rem/1.5 system-ui,sans-serif; color: #d8cbb1; }
	.chat-costs summary { padding: .35rem 0; }
	.cost-panel { position: absolute; z-index: 8; bottom: 55px; right: 10px; width: min(320px,calc(100% - 20px)); max-height: 19rem; overflow-y: auto; background: #182020; padding: 1rem; border: 1px solid #ac844b; border-radius: 6px; box-shadow: 0 8px 28px #000b; }
	.cost-panel p { display: flex; justify-content: space-between; gap: 12px; margin: 0 0 .7rem; }
	.cost-panel span { white-space: nowrap; font-variant-numeric: tabular-nums; }
	.cost-panel a { color: #e2bd7a; }
	.chat-roster { position: absolute; inset: 0; pointer-events: none; z-index: 5; }
	.chat-member { position: absolute; top: 0; left: 0; width: 96px; height: 98px; padding: 0; display: flex; align-items: center; flex-direction: column; gap: 5px; border: 0; background: transparent; color: #ece2cd; pointer-events: auto; will-change: transform; }
	.chat-coin { width: 53px; height: 53px; flex: none; border: 2px solid #ac844b; border-radius: 50%; display: grid; place-items: center; background: radial-gradient(circle at 34% 27%,#d1b37f,#ac844b 37%,#362c1d); font: 400 24px Georgia,serif; color: #11191a; box-shadow: inset 0 0 0 2px #302a20,0 3px 9px #0008; filter: saturate(.65) brightness(.85); transition: filter .4s ease,box-shadow .4s ease; }
	.chat-coin img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
	.chat-member[data-active='true'] .chat-coin { filter: none; border-color: #dec28b; box-shadow: 0 0 0 3px #d0ac693d,0 0 28px #d0ac6980,0 2px 6px #0008; }
	.chat-member[data-active='true'][data-waiting='true'] .chat-coin { box-shadow: 0 0 0 2px #d0ac692b,0 0 17px #d0ac694d; }
	.chat-member-name { font: .75rem/1.3 system-ui,sans-serif; text-align: center; }
	.chat-member-role { font: .69rem/1.3 system-ui,sans-serif; color: #b6ac95; text-align: center; }
	.chat-member[data-active='true'] .chat-member-name { color: #dec28b; }
	[data-open='false'] .chat-member-name,[data-open='false'] .chat-member-role { text-shadow: 0 1px 5px #000,0 0 8px #000; }
	.chat-open { position: absolute; left: 50%; top: max(17rem,calc(83svh - var(--chat-top))); transform: translateX(-50%); pointer-events: auto; border: 1px solid #ac844b; border-radius: 5px; background: #11191a; color: #ece2cd; padding: .7rem 1rem; font: .95rem/1.4 Georgia,serif; white-space: nowrap; box-shadow: 0 6px 25px #000b; z-index: 6; }
	.chat-open span { display: block; font: .69rem/1.5 system-ui,sans-serif; color: #b6ac95; margin-top: .2rem; }
	.connection-note,.new-session { margin: 0; padding: .6rem 1rem; color: #edc389; background: #29291f; font: .75rem/1.5 system-ui,sans-serif; flex: none; }
	.new-session { border: 0; text-align: left; text-decoration: underline; }
	.feed-unavailable,.no-live-js { color: #d8cbb1; background: #11191a; padding: .8rem 1rem; font: .8rem/1.5 system-ui,sans-serif; pointer-events: auto; }
	@media (max-width: 600px) {
		.chat-window { width: calc(100% - 24px); height: 35rem; }
		.chat-head { padding: .85rem .75rem .6rem; gap: 7px; }
		h2 { font-size: 1.2rem; }
		.chat-close { padding: .45rem; min-height: 42px; }
		.chat-dock { margin: 0 8px; height: 100px; }
		.chat-member { width: 54px; height: 94px; gap: 5px; }
		.chat-coin { width: 43px; height: 43px; font-size: 20px; }
		.chat-member-name { font-size: .69rem; }
		.chat-topic { padding: .6rem .75rem; }
		.chat-log { padding: .4rem .65rem 1rem; }
		.chat-footer { padding: .6rem .75rem; }
		.chat-costs summary { min-height: 35px; }
		.chat-status { font-size: .69rem; }
	}
	@media (prefers-reduced-motion: reduce) { .chat-window,.chat-coin { transition: none; } }
</style>
