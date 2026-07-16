<script>
	import { onMount } from 'svelte';

	let { data } = $props();
	let home = $derived(data.home);
	// Revisionen vollständig datengetrieben: Anzahl abgeleitet, alle Säulen, kein Hardcode.
	let revisions = $derived(home?.revisions ?? []);
	let revisedModelCount = $derived(new Set(revisions.map((revision) => revision.model)).size);
	let scene = $state('arrival');
	const scenes = ['arrival', 'recommendations', 'door-opening', 'antechamber', 'initial', 'revision', 'count', 'archive'];
	const steps = [
		['Frage', 'arrival', '/media/process/question-display.jpg'],
		['Belege', 'door-opening', '/media/process/evidence-display.jpg'],
		['Drei Antworten', 'initial', '/media/process/three-answers-display.jpg'],
		['Umdenken', 'revision', '/media/process/review-and-revise-display.jpg'],
		['Zählen', 'count', '/media/process/count-display.jpg'],
		['Veröffentlichen', 'archive', '/media/process/publish-display.jpg']
	];
	const pillarImages = { A: '/media/pillars/future-display.jpg', B: '/media/pillars/suffering-display.jpg', C: '/media/pillars/global-risks-display.jpg', D: '/media/pillars/overlooked-display.jpg' };
	const lecternAnchors = [
		{ x: 23, y: 38 }, { x: 77, y: 38 }, { x: 50, y: 82 }
	];

	onMount(() => {
		const root = document.documentElement;
		const cues = [...document.querySelectorAll('.scene-cue')];
		const activate = (next) => {
			if (!scenes.includes(next)) return;
			scene = next;
			history.replaceState(null, '', `#${next}`);
		};
		const observer = new IntersectionObserver((entries) => {
			const active = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
			if (active) activate(active.target.dataset.scene);
		}, { rootMargin: '-42% 0px -42%', threshold: [0, .2, .6] });
		cues.forEach((cue) => observer.observe(cue));
		root.classList.add('stage-ready');
		const initial = location.hash.slice(1);
		if (scenes.includes(initial)) {
			scene = initial;
			document.querySelector(`[data-scene="${initial}"]`)?.scrollIntoView();
		}
		const onHash = () => {
			const next = location.hash.slice(1);
			if (scenes.includes(next)) {
				scene = next;
				document.querySelector(`[data-scene="${next}"]`)?.scrollIntoView();
			}
		};
		addEventListener('hashchange', onHash);
		return () => {
			observer.disconnect();
			removeEventListener('hashchange', onHash);
			root.classList.remove('stage-ready');
		};
	});

	const currentStep = () => ({ arrival: 0, recommendations: 0, 'door-opening': 1, antechamber: 1, initial: 2, revision: 3, count: 4, archive: 5 })[scene] ?? 0;
	const money = (value, currency = 'EUR') => new Intl.NumberFormat('de-CH', { style: 'currency', currency }).format(value);
</script>

<svelte:head>
	<title>NobleCause — Wo hilft meine Spende am meisten?</title>
	<meta name="description" content="Drei KI-Modelle prüfen dieselben Belege. NobleCause veröffentlicht Empfehlungen, Änderungen, Uneinigkeit und Kosten." />
	<link rel="preload" as="image" href="/media/scenes/hall-display.jpg" />
</svelte:head>

{#if home}
	<section class="home-fallback" aria-labelledby="fallback-title">
		<p class="eyebrow">Öffentliches Beratungsprotokoll</p>
		<h1 id="fallback-title">Wo hilft meine Spende am meisten?</h1>
		<p>Je ein KI-Modell von Anthropic, OpenAI und Google prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.</p>
		<p><strong>Drei Modelle antworten getrennt. Sie lesen einander. Sie dürfen umdenken. Ein einfaches Programm zählt nur die Nennungen.</strong></p>
		<div class="fallback-results">
			{#each home.recommendations as rec (rec.pillar)}
				<article><h2>{rec.pillar} · {rec.pillarName}</h2>
					{#if rec.hasConsensus}
						<strong>{rec.organization.name}</strong><span>{rec.count} von {rec.total}</span>
						<span class="fb-desc">{rec.organization.description}</span>
						{#if rec.conditionalCount}
							{#each rec.reservations as reservation (reservation.model)}<em class="fb-reservation">Unter Vorbehalt ({reservation.model}): {reservation.reservation}</em>{/each}
						{/if}
						{#if rec.organization.donationUrl}<a href={rec.organization.donationUrl}>Direkt spenden (extern) ↗</a>{:else}<small>Kein kuratierter Spendenweg.</small>{/if}
					{:else}
						<p>Keine zwei gleichen Nennungen.</p>
						{#each rec.votes as vote (vote.model)}<span>{vote.model}: {vote.organization.name}</span>{#if vote.organization.donationUrl}<a href={vote.organization.donationUrl}>Direkt spenden (extern) ↗</a>{/if}{/each}
					{/if}
				</article>
			{/each}
		</div>
		<p>NobleCause nimmt kein Geld an. Spendenlinks führen direkt zu den Organisationen.</p>

		{#if revisions.length}
			<section class="fb-block" aria-labelledby="fb-revisions">
				<h2 id="fb-revisions">Änderungen nach dem Gegenlesen</h2>
				<ul>
					{#each revisions as revision (revision.model + revision.pillar)}
						<li>{revision.model} · {revision.pillarName}: <del>{revision.initial.organization.name}</del> → <strong>{revision.final.organization.name}</strong></li>
					{/each}
				</ul>
			</section>
		{/if}

		<section class="fb-block" aria-labelledby="fb-protocol">
			<h2 id="fb-protocol">Voten je Modell — erst und nach dem Gegenlesen</h2>
			{#each home.modelTracks as track (track.model)}
				<div class="fb-track"><strong>{track.label}</strong>
					<ul>
						{#each track.rows as row (row.pillar)}
							<li>{row.pillar} · {row.pillarName}: Erst {row.initial?.organization.name ?? 'kein Votum'} · Schluss {row.final?.organization.name ?? 'kein Votum'}</li>
						{/each}
					</ul>
				</div>
			{/each}
		</section>

		<details class="fb-block fb-dissent-wrap">
			<summary>Dissens (vollständiger Wortlaut)</summary>
			<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
			<div class="fb-dissent">{@html home.dissentHtml}</div>
		</details>

		{#if home.correctionHtml}
			<aside class="fb-block fb-correction" aria-label="Korrekturhinweis">
				<strong>Korrekturhinweis</strong>
				<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content -->
				<div>{@html home.correctionHtml}</div>
			</aside>
		{/if}

		<section class="fb-block" aria-labelledby="fb-costs">
			<h2 id="fb-costs">Kosten</h2>
			<p>Kosten dieser Sitzung: {money(home.costs.total, home.costs.currency)}.</p>
		</section>

		<section class="fb-block" aria-labelledby="fb-archive">
			<h2 id="fb-archive">Sitzungsarchiv</h2>
			<ul>
				{#each home.archive as item (item.id)}
					<li><a href="/sessions/{item.id}/">Sitzung {item.number}: {item.nonConsensusPillars.length ? `Keine Einigung in ${item.nonConsensusPillars.join(', ')}` : 'Empfehlungen in allen Bereichen'}</a></li>
				{/each}
			</ul>
		</section>

		<a href="/sessions/{home.currentSession.id}/">Vollständiges Protokoll öffnen →</a>
	</section>

	<section class="council-stage" data-scene={scene} aria-label="NobleCause Ratssaal">
		<div class="world council-world" aria-hidden="true">
			<img src="/media/scenes/hall-display.jpg" alt="" width="1600" height="900" />
			<div class="world-shade"></div>
		</div>
		{#if scene === 'door-opening'}<div class="world doorway-world" aria-hidden="true">
			<img src="/media/scenes/doorway-display.jpg" alt="" width="1600" height="900" decoding="async" />
			<div class="world-shade"></div>
		</div>{/if}
		{#if scene === 'antechamber'}<div class="world antechamber-world" aria-hidden="true">
			<img src="/media/scenes/antechamber-display.jpg" alt="" width="1600" height="900" decoding="async" />
			<div class="world-shade"></div>
		</div>{/if}
		{#if scene === 'archive'}<div class="world archive-world" aria-hidden="true">
			<img src="/media/scenes/archive-display.jpg" alt="" width="1600" height="900" decoding="async" />
			<div class="world-shade"></div>
		</div>{/if}

		<header class="stage-brand">
			<a href="/">NobleCause</a><span>Öffentliches Protokoll der Beratung</span>
		</header>

		<aside class="recommendation-console" aria-labelledby="rec-console-title">
			<header><span>Sitzung {home.currentSession.number} · heute</span><h2 id="rec-console-title">Empfehlungen</h2></header>
			<div class="rec-register">
				{#each home.recommendations as rec (rec.pillar)}
					<details class="rec-row" open={scene === 'recommendations'}>
						<summary>
							<i><img src={pillarImages[rec.pillar]} alt="" width="320" height="320" loading="lazy" /></i><span><small>{rec.pillar} · {rec.pillarName}</small><strong>{rec.hasConsensus ? rec.organization.name : 'Keine Einigung'}</strong></span>
							<b>{rec.hasConsensus ? `${rec.count}/${rec.total}` : '≠'}</b>
						</summary>
						<div class="rec-detail">
							{#if rec.hasConsensus}
								<p>{rec.organization.description}</p>
								{#if rec.conditionalCount}<em>{rec.conditionalCount} Stimme unter Vorbehalt</em>{/if}
								{#if rec.organization.donationUrl}<a href={rec.organization.donationUrl}>Direkt spenden <span>extern ↗</span></a>{:else}<small>Kein kuratierter Spendenweg.</small>{/if}
							{:else}
								{#each rec.votes as vote (vote.model)}<p><b>{vote.model}</b> · {vote.organization.name} {#if vote.organization.donationUrl}<a href={vote.organization.donationUrl}>Spenden ↗</a>{/if}</p>{/each}
							{/if}
						</div>
					</details>
				{/each}
			</div>
			<p class="money-flow">Kein Geld fließt über NobleCause.</p>
		</aside>

		<aside class="antechamber-window">
			<img src="/media/scene-thumbnails/antechamber-display.jpg" alt="Vorzimmer mit Späher, Wart und Schiefertafel" width="640" height="360" loading="lazy" />
			<div><strong>Belege & Quellen</strong><a href="#door-opening">Zum Belegzimmer →</a></div>
		</aside>

		<section class="scene-plaque arrival-plaque">
			<h1>Wo hilft meine Spende am meisten?</h1>
			<strong>Drei Modelle prüfen dieselben Belege. Öffentlich und überprüfbar.</strong>
			<small>Für Menschen heute, unsere Zukunft, große Gefahren und Übersehenes.</small>
		</section>

		<section class="mechanism-plaque">
			<strong>Drei Modelle antworten getrennt. Sie lesen einander. Sie dürfen umdenken.</strong>
			<span>Ein einfaches Programm zählt nur die Nennungen.</span>
		</section>

		<section class="question-plaque">
			<span>Die aktuelle Frage</span><p>{home.currentSession.question}</p>
			<a href="/sessions/{home.currentSession.id}/">Vollständig lesen →</a>
		</section>

		<section class="antechamber-labels">
			<div><span>Späher</span><strong>Der Späher sammelt Belege.</strong></div>
			<div><span>Wart</span><strong>Der Wart ordnet das öffentliche Protokoll.</strong></div>
			<a href="/sessions/{home.currentSession.id}/#wart-dossier">Dossier öffnen →</a>
		</section>

		<section class="lectern-layer" aria-label="Drei gleichwertige Modellpulte">
			{#each home.modelTracks as track, index (track.model)}
			<details class="lectern-sign" style={`--anchor-x:${lecternAnchors[index].x}%;--anchor-y:${lecternAnchors[index].y}%`}>
					<summary><span>{track.family}</span><strong>{track.label}</strong></summary>
					<div>
						{#each track.rows as row (row.pillar)}<p><i>{row.pillar}</i>{row.initial?.organization.name ?? 'Kein Votum'}</p>{/each}
						<a href="/sessions/{home.currentSession.id}/#vollprotokoll">Voten lesen →</a>
					</div>
				</details>
			{/each}
		</section>

		{#if revisions.length}
		<section class="revision-layer">
			<header><strong>{revisedModelCount === 1 ? 'Nach dem Gegenlesen änderte ein Modell seine Empfehlung.' : `Nach dem Gegenlesen änderten ${revisedModelCount} Modelle ihre Empfehlung.`}</strong><span>Erstvoten bleiben sichtbar.</span></header>
			<div class="revision-notes">
				{#each revisions as revision (revision.model + revision.pillar)}
					<article><span>{revision.model} · {revision.pillarName}</span><small>Erstvotum</small><del>{revision.initial.organization.name}</del><small>geändert zu</small><strong>{revision.final.organization.name}</strong></article>
				{/each}
			</div>
		</section>
		{/if}

		<section class="counting-machine" aria-labelledby="machine-title">
			<h2 id="machine-title">Zählwerk</h2>
			<p>Das Programm zählt nur gleiche Nennungen.</p>
			<div class="machine-slots">
				{#each home.recommendations as rec (rec.pillar)}<span><i>{rec.pillar}</i>{rec.hasConsensus ? `${rec.count} gleich` : 'getrennt'}</span>{/each}
			</div>
		</section>

		<aside class="archive-console" aria-labelledby="archive-title">
			<div class="archive-door-visual" aria-hidden="true"><img src="/media/scene-thumbnails/archive-display.jpg" alt="" width="640" height="360" loading="lazy" /></div>
			<header><span>Sitzungsarchiv</span><h2 id="archive-title">Veröffentlicht</h2></header>
			<ol>
				{#each home.archive as item (item.id)}
					<li><a href="/sessions/{item.id}/"><span>Sitzung {item.number}</span><strong>{item.nonConsensusPillars.length ? `Keine Einigung in ${item.nonConsensusPillars.join(', ')}` : 'Empfehlungen in allen Bereichen'}</strong></a></li>
				{/each}
			</ol>
			<div class="archive-meta"><span>Kosten: {money(home.costs.total, home.costs.currency)}</span>{#if home.correction}<a href="/sessions/{home.currentSession.id}/">Korrekturhinweis</a>{/if}</div>
		</aside>

		<nav class="process-rail" aria-label="Ablauf der Beratung">
			{#each steps as step, index (step[0])}<a href="#{step[1]}" class:active={currentStep() === index}><i><img src={step[2]} alt="" width="320" height="320" loading={index < 2 ? 'eager' : 'lazy'} /></i><span>{step[0]}</span></a>{/each}
		</nav>
	</section>

	<div class="scene-track" aria-hidden="true">
		{#each scenes as item, index (item)}<div class="scene-cue" id={item} data-scene={item}><span>{index + 1}</span></div>{/each}
	</div>
{/if}

<style>
	:global(body:has(.council-stage)) { margin:0; background:#05090b; }
	:global(.page:has(.council-stage)) { max-width:none; padding:0; }
	:global(.page:has(.council-stage) > header), :global(.page:has(.council-stage) > footer) { display:none; }
	:global(.page:has(.council-stage) main) { min-height:0; }
	.home-fallback { width:min(70rem,calc(100% - 2rem)); margin:2rem auto; padding:2rem; color:#eee6d6; background:#101618; }
	.home-fallback h1 { font-size:clamp(2.5rem,7vw,6rem); }
	.fallback-results { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; }
	.fallback-results article { display:grid; gap:.4rem; padding:1rem; border:1px solid #8e6a34; }
	.fallback-results h2 { margin:0; font-size:1rem; }
	.fallback-results .fb-desc { color:#c7bca7; font-size:.85rem; }
	.fb-reservation { color:#e0c07f; font-style:normal; font-size:.82rem; }
	.home-fallback .fb-block { margin:1.5rem 0; }
	.home-fallback .fb-block h2 { font-size:1.15rem; margin:0 0 .5rem; }
	.home-fallback .fb-block ul { margin:.3rem 0; padding-left:1.2rem; }
	.home-fallback .fb-track { margin:.5rem 0; }
	.home-fallback .fb-correction { padding:1rem; border-left:3px solid #c89644; background:#161d20; }
	.home-fallback .fb-dissent { max-height:24rem; overflow:auto; font-size:.85rem; }
	.home-fallback .fb-dissent :global(pre) { overflow-x:auto; }
	.home-fallback summary { cursor:pointer; color:#e0b75d; }
	.home-fallback a { color:#e6b45c; }
	:global(.js) .home-fallback { display:block; }
	.council-stage { display:none; }
	:global(.stage-ready) .home-fallback { display:none; }
	:global(.stage-ready) .council-stage { display:grid; }

	.council-stage { --cx:0%; --cy:0%; --zoom:1; position:fixed; z-index:10; inset:0; grid-template-columns:minmax(15rem,23%) 1fr minmax(13rem,18%); grid-template-rows:4.2rem 1fr 11.5rem; overflow:hidden; color:#e7dcc4; background:#030607; font-family:Georgia,'Iowan Old Style',serif; }
	.world { position:absolute; z-index:-3; inset:0; overflow:hidden; opacity:0; transition:opacity .55s ease; }
	.world img { width:100%; height:100%; object-fit:cover; transform:translate(var(--cx),var(--cy)) scale(var(--zoom)); transform-origin:center; transition:transform .7s ease,filter .7s ease; }
	.world-shade { position:absolute; inset:0; background:radial-gradient(circle at 52% 52%,transparent 12%,rgba(1,4,5,.18) 58%,rgba(1,3,4,.76)); }
	.council-world { opacity:1; }
	.antechamber-world img,.doorway-world img,.archive-world img { object-position:center; }
	.stage-brand { grid-column:1; grid-row:1; align-self:center; z-index:8; padding:0 1rem; display:grid; border-bottom:1px solid rgba(199,146,62,.45); }
	.stage-brand a { color:#e7c881; font-size:1.35rem; text-decoration:none; letter-spacing:.04em; }
	.stage-brand span,.recommendation-console header span,.archive-console header span { color:#a99062; font:600 .62rem ui-sans-serif,system-ui; letter-spacing:.11em; text-transform:uppercase; }
	.recommendation-console { grid-column:1; grid-row:2; z-index:7; margin:.6rem; align-self:start; max-height:calc(100vh - 17rem); padding:.8rem; background:linear-gradient(100deg,rgba(12,16,16,.94),rgba(9,12,13,.82)); border:1px solid rgba(190,139,58,.48); box-shadow:0 1rem 3rem #000; overflow:auto; }
	.recommendation-console h2,.archive-console h2 { margin:.15rem 0 .55rem; color:#ead8ae; font-size:1.15rem; letter-spacing:.05em; }
	.rec-row { border-top:1px solid rgba(189,139,62,.3); }
	.rec-row summary { display:grid; grid-template-columns:2.35rem 1fr auto; gap:.55rem; align-items:center; min-height:3.45rem; cursor:pointer; list-style:none; }
	.rec-row summary::-webkit-details-marker { display:none; }
	.rec-row summary i { display:grid; place-items:center; width:2.15rem; height:2.15rem; overflow:hidden; border:1px solid #8c6935; border-radius:50%; background:#080c0d; box-shadow:inset 0 0 .7rem #000; }
	.rec-row summary i img { width:100%;height:100%;object-fit:cover;filter:saturate(.78) contrast(1.08); }
	.rec-row summary span { display:grid; min-width:0; }
	.rec-row summary small { color:#a9997d; font:600 .58rem ui-sans-serif,system-ui; text-transform:uppercase; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; }
	.rec-row summary strong { overflow:hidden; color:#e6dbc4; font-size:.78rem; white-space:nowrap; text-overflow:ellipsis; }
	.rec-row summary b { color:#dfbd70; font:.72rem ui-sans-serif,system-ui; }
	.rec-detail { padding:0 0 .7rem 2.7rem; font-size:.72rem; }
	.rec-detail p { margin:.25rem 0; color:#c7bca7; }
	.rec-detail em { display:block; color:#d8b76d; font-style:normal; }
	.rec-detail a { color:#e0b75d; }
	.rec-detail a span { font-size:.58rem; text-transform:uppercase; }
	.money-flow { margin:.7rem 0 0; color:#9e927f; font:.62rem ui-sans-serif,system-ui; }
	.antechamber-window { grid-column:1; grid-row:3; z-index:8; position:relative; margin:.2rem .6rem .6rem; overflow:hidden; border:1px solid rgba(190,139,58,.48); background:#050708; }
	.antechamber-window img { width:100%; height:100%; object-fit:cover; opacity:.8; }
	.antechamber-window::after { content:''; position:absolute; inset:0; background:linear-gradient(transparent 40%,rgba(2,4,5,.95)); }
	.antechamber-window div { position:absolute; z-index:2; inset:auto .7rem .55rem; display:flex; justify-content:space-between; gap:.5rem; font-size:.67rem; }
	.antechamber-window a { color:#d9b261; }
	.scene-plaque,.mechanism-plaque,.question-plaque { position:absolute; z-index:6; left:50%; transform:translateX(-50%); width:min(42rem,46vw); padding:.65rem 1.2rem; text-align:center; background:linear-gradient(90deg,rgba(7,10,11,.5),rgba(13,17,17,.92),rgba(7,10,11,.5)); border-block:1px solid rgba(197,145,60,.48); opacity:0; transition:opacity .45s,transform .55s; pointer-events:none; }
	.arrival-plaque { top:5.2rem; }
	.arrival-plaque h1 { margin:0; color:#f0d899; font-size:clamp(1.35rem,2.2vw,2.2rem); font-weight:400; line-height:1.12; }
	.arrival-plaque strong,.arrival-plaque small { display:block; margin:.25rem 0; }
	.arrival-plaque small { color:#b9ad97; }
	.mechanism-plaque { top:.7rem; opacity:1; width:min(46rem,48vw); }
	.mechanism-plaque strong,.mechanism-plaque span { display:block; }
	.mechanism-plaque span { color:#cdb57f; font-size:.78rem; }
	.question-plaque { top:20%; }
	.question-plaque span { color:#d6b264; font:.65rem ui-sans-serif,system-ui; text-transform:uppercase; letter-spacing:.1em; }
	.question-plaque p { margin:.4rem 0; font-size:.95rem; }
	.question-plaque a { color:#e1bb68; pointer-events:auto; }
	.antechamber-labels { position:absolute; z-index:6; inset:auto 22% 14rem 27%; display:flex; justify-content:center; gap:1rem; opacity:0; transition:opacity .4s; }
	.antechamber-labels div { padding:.65rem .8rem; background:rgba(9,12,12,.82); border:1px solid rgba(190,139,58,.4); }
	.antechamber-labels span { display:block; color:#c89b4e; font:.6rem ui-sans-serif,system-ui;text-transform:uppercase; }
	.antechamber-labels a { align-self:center; color:#e0b65e; }
	.lectern-layer { position:absolute; z-index:6; inset:0; opacity:0; pointer-events:none; transition:opacity .45s; }
	.lectern-sign { position:absolute; left:var(--anchor-x);top:var(--anchor-y);transform:translate(-50%,-105%);width:11rem;color:#e6dbc5;background:rgba(8,11,12,.88);border:1px solid rgba(205,153,69,.55);pointer-events:auto; }
	.lectern-sign summary { padding:.45rem .6rem; cursor:pointer; list-style:none; text-align:center; }
	.lectern-sign summary span { display:block;color:#c89b4e;font:.58rem ui-sans-serif,system-ui;text-transform:uppercase; }
	.lectern-sign div { padding:.25rem .65rem .65rem; border-top:1px solid rgba(190,139,58,.3); }
	.lectern-sign p { display:flex; gap:.35rem; margin:.25rem 0; font-size:.65rem; }
	.lectern-sign p i { color:#d1a657; font-style:normal; }
	.lectern-sign a { color:#ddb45e; font-size:.65rem; }
	.revision-layer { position:absolute; z-index:7; inset:4.5rem 19% 12rem 24%; opacity:0; pointer-events:none; transition:opacity .45s; }
	.revision-layer header { width:max-content; max-width:75%; margin:auto; padding:.45rem .8rem; text-align:center; background:rgba(7,10,11,.9); border:1px solid rgba(199,146,62,.45); }
	.revision-layer header span { display:block;color:#bcae94;font-size:.7rem; }
	.revision-notes { display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:13rem; }
	.revision-notes article { width:13rem; padding:.65rem; color:#20180e; background:#ded0b4; box-shadow:0 1rem 2rem #000; transform:rotate(-1deg); }
	.revision-notes span,.revision-notes small { display:block;font:.58rem ui-sans-serif,system-ui;text-transform:uppercase; }
	.revision-notes del,.revision-notes strong { display:block;margin:.15rem 0; }
	.counting-machine { position:absolute; z-index:8; left:51%; top:70%; width:min(25rem,34vw); transform:translate(-50%,-45%) translateY(1rem); padding:.7rem 1rem; display:grid; place-items:center; align-content:center; text-align:center; color:#eadbbd; background:linear-gradient(90deg,rgba(5,8,9,.35),rgba(8,12,12,.92),rgba(5,8,9,.35)); border-block:1px solid rgba(205,153,69,.55); opacity:0; transition:transform .7s,opacity .5s; pointer-events:none; }
	.counting-machine h2,.counting-machine p,.machine-slots { position:relative;z-index:1; }
	.counting-machine h2 { margin:0;color:#e5c274;font-size:1.15rem; }.counting-machine p{margin:.25rem;font-size:.67rem;}
	.machine-slots { position:absolute; top:100%; display:flex;gap:.3rem; }
	.machine-slots span { display:grid;padding:.3rem;background:#0b1011;border:1px solid #7a5a2f;font-size:.58rem;white-space:nowrap; }
	.machine-slots i { color:#d5a657;font-style:normal; }
	.archive-console { grid-column:3;grid-row:1/4;z-index:7;margin:.6rem;padding:1rem;background:linear-gradient(90deg,rgba(7,9,10,.75),rgba(11,13,13,.96));border:1px solid rgba(190,139,58,.35);box-shadow:-1rem 0 3rem #000;overflow:auto; }
	.archive-door-visual { height:28%;min-height:8rem;margin-bottom:.8rem;overflow:hidden;border:1px solid #76542c;box-shadow:inset 0 0 2rem #000; }
	.archive-door-visual img { width:100%;height:100%;object-fit:cover;object-position:center;opacity:.82; }
	.archive-console ol { list-style:none;padding:0;margin:0; }
	.archive-console li { border-top:1px solid rgba(190,139,58,.25); }
	.archive-console li a { display:grid;gap:.18rem;padding:.65rem 0;color:#c8bca6;text-decoration:none; }
	.archive-console li span { color:#9b8b72;font:.58rem ui-sans-serif,system-ui;text-transform:uppercase; }
	.archive-console li strong { font-size:.72rem; }
	.archive-meta { display:grid;gap:.35rem;margin-top:.8rem;color:#b7a98f;font-size:.67rem; }
	.archive-meta a { color:#dcb463; }
	.process-rail { grid-column:2;grid-row:3;z-index:9;align-self:end;display:grid;grid-template-columns:repeat(6,1fr);margin:.6rem;border:1px solid rgba(190,139,58,.48);background:rgba(7,10,11,.9); }
	.process-rail a { min-width:0;min-height:5.5rem;display:grid;place-items:center;align-content:center;gap:.25rem;color:#9e927e;text-decoration:none;border-right:1px solid rgba(190,139,58,.28);font:.65rem ui-sans-serif,system-ui;text-align:center; }
	.process-rail a:last-child{border:0}.process-rail i{display:grid;place-items:center;width:2.7rem;height:2.7rem;overflow:hidden;border:1px solid #79592f;border-radius:50%;background:#070b0c}.process-rail i img{width:100%;height:100%;object-fit:cover;filter:saturate(.7) contrast(1.12);opacity:.72}.process-rail a.active{color:#efd18d;background:linear-gradient(transparent,rgba(198,143,55,.15));box-shadow:inset 0 -2px #c89644}.process-rail a.active i{box-shadow:0 0 1rem rgba(220,164,72,.65)}.process-rail a.active i img{opacity:1;filter:saturate(.95) contrast(1.08)}
	.scene-track { position:relative;height:800vh; }
	.scene-cue { height:100vh; }

	.council-stage[data-scene='arrival'] { --zoom:1;--cx:0%;--cy:0%; }.council-stage[data-scene='arrival'] .arrival-plaque{opacity:1;transform:translateX(-50%) translateY(.3rem)}
	.council-stage[data-scene='recommendations'] { --zoom:1.06;--cx:2%;--cy:1%; }.council-stage[data-scene='recommendations'] .recommendation-console{box-shadow:0 0 2rem rgba(215,160,67,.25)}
	.council-stage[data-scene='door-opening'] { --zoom:1.08;--cx:-4%;--cy:0%; }.council-stage[data-scene='door-opening'] .council-world{opacity:0}.council-stage[data-scene='door-opening'] .doorway-world{opacity:1}.council-stage[data-scene='door-opening'] .question-plaque{opacity:1;transform:translateX(-50%) translateY(.4rem)}
	.council-stage[data-scene='antechamber'] .council-world{opacity:0}.council-stage[data-scene='antechamber'] .antechamber-world{opacity:1}.council-stage[data-scene='antechamber'] .counting-machine{opacity:0}.council-stage[data-scene='antechamber'] .antechamber-labels{opacity:1;pointer-events:auto}.council-stage[data-scene='antechamber'] .recommendation-console,.council-stage[data-scene='antechamber'] .archive-console,.council-stage[data-scene='antechamber'] .antechamber-window{opacity:.12}
	.council-stage[data-scene='initial'] { --zoom:1;--cx:0%;--cy:0%; }.council-stage[data-scene='initial'] .council-world img{object-fit:contain}.council-stage[data-scene='initial'] .lectern-layer{opacity:1}.council-stage[data-scene='initial'] .recommendation-console,.council-stage[data-scene='initial'] .archive-console{opacity:.3}
	.council-stage[data-scene='revision'] { --zoom:1.08;--cx:0%;--cy:2%; }.council-stage[data-scene='revision'] .revision-layer{opacity:1}.council-stage[data-scene='revision'] .lectern-layer{opacity:.2}
	.council-stage[data-scene='count'] { --zoom:1.28;--cx:0%;--cy:1%; }.council-stage[data-scene='count'] .counting-machine{opacity:1;transform:translate(-50%,-45%);pointer-events:auto}.council-stage[data-scene='count'] .recommendation-console,.council-stage[data-scene='count'] .archive-console{opacity:.28}
	.council-stage[data-scene='archive'] { --zoom:1.04;--cx:0%;--cy:0%; }.council-stage[data-scene='archive'] .council-world{opacity:0}.council-stage[data-scene='archive'] .archive-world{opacity:1}.council-stage[data-scene='archive'] .archive-console{box-shadow:0 0 2rem rgba(215,160,67,.3)}

	@media (max-width:800px) {
		.fallback-results{grid-template-columns:1fr}
		:global(.stage-ready) .council-stage{position:relative;inset:auto;display:flex;flex-direction:column;min-height:100vh;overflow:hidden;padding-bottom:1rem;background:#05090b}:global(.stage-ready) .scene-track{display:none}
		.world{position:relative;inset:auto;order:1;height:58vw;min-height:14rem;opacity:1!important}.world img{transform:none!important}.doorway-world,.antechamber-world,.archive-world{display:none}.stage-brand{order:0;padding:1rem;display:grid;border-bottom:1px solid rgba(190,139,58,.4)}
		.mechanism-plaque{position:relative;order:2;top:auto;left:auto;transform:none;width:auto;margin:.7rem;opacity:1}.arrival-plaque{position:relative;order:3;top:auto;left:auto;transform:none!important;width:auto;margin:.7rem;opacity:1;text-align:left}.recommendation-console{order:4;max-height:none;margin:.7rem;opacity:1!important}.antechamber-window{order:5;min-height:14rem;margin:.7rem}.process-rail{position:relative;order:6;display:flex;overflow-x:auto;margin:.7rem}.process-rail a{flex:0 0 7rem;min-height:5.25rem}.process-rail i{width:2.35rem;height:2.35rem}.question-plaque{position:relative;order:7;top:auto;left:auto;transform:none;width:auto;margin:.7rem;opacity:1;text-align:left}.antechamber-labels{position:relative;order:8;inset:auto;display:grid;margin:.7rem;opacity:1}.lectern-layer{position:relative;order:9;inset:auto;display:grid;grid-template-columns:1fr;gap:.6rem;margin:.7rem;opacity:1}.lectern-sign{position:relative;inset:auto!important;transform:none;width:auto}.revision-layer{position:relative;order:10;inset:auto;margin:.7rem;opacity:1}.revision-layer header{max-width:none;width:auto}.revision-notes{display:grid;margin-top:.7rem}.revision-notes article{width:auto}.counting-machine{position:relative;order:11;left:auto;top:auto;width:min(16rem,80vw);margin:2rem auto 5rem;transform:none!important;opacity:1}.archive-console{order:12;margin:.7rem;max-height:none;opacity:1!important}.archive-door-visual{height:12rem}.scene-plaque,.mechanism-plaque,.question-plaque{pointer-events:auto}
	}
	@media (prefers-reduced-motion:reduce){.world img,.counting-machine,*{transition-duration:.01ms!important;scroll-behavior:auto!important}}
</style>
