<script>
	import StageHero from '$lib/components/rooms/StageHero.svelte';
	import enUi from '$lib/cases/amf-ui.en.json';
	import { amfPaths } from '$lib/cases/amf-paths.js';

	let { caseData, room = 'study', lang = 'de' } = $props();
	const t = (text) => {
		if (lang === 'de') return text;
		if (!Object.hasOwn(enUi, text)) throw new Error('Missing AMF UI translation: ' + text);
		return enUi[text];
	};
	let rooms = $derived({
		study: { name: 'The Study', action: t('Den Fall verstehen'), path: amfPaths.study[lang], scene: 'antechamber', lead: '' },
		council: { name: 'The Council', action: t('Die Stimmen lesen'), path: amfPaths.council[lang], scene: 'hall', lead: t('Fünf dokumentierte Positionen vom 21. Oktober 2026.') },
		archive: { name: 'The Archive', action: t('Die Belege prüfen'), path: amfPaths.archive[lang], scene: 'archive', lead: t('Von der Aussage zum Original.') }
	});
	let current = $derived(rooms[room]);
	const evidence = (id) => amfPaths.archive[lang] + '#beleg-' + id;
	let homePath = $derived(lang === 'en' ? '/en/' : '/');
	let councilPath = $derived(lang === 'en' ? '/en/council/' : '/ratssaal/');
	const verdict = (vote) => vote.decision === 'abstain' ? t('Enthaltung') : t('Bedingte Empfehlung');
</script>

<svelte:head>
	<title>AMF · {current.name} · NobleCause.ai</title>
	<meta name="description" content={t("Malariaschutz durch die Against Malaria Foundation. Eine datierte Empfehlung, fünf historische Ratspositionen und die geprüften Belege zu Wirkung, Kosten und Zusatzbedarf.")} />
	<link rel="canonical" href={'https://noblecause.ai' + current.path} />
	<link rel="alternate" hreflang="de" href={'https://noblecause.ai' + amfPaths[room].de} />
	<link rel="alternate" hreflang="en" href={'https://noblecause.ai' + amfPaths[room].en} />
	<link rel="alternate" hreflang="x-default" href={'https://noblecause.ai' + amfPaths[room].de} />
</svelte:head>

<div class="case-page" lang={lang} class:council={room === 'council'}>
	<a class="skip" href="#fallinhalt">{t("Zum Inhalt")}</a>
	<header class="case-bar">
		<a class="brand" href={homePath}>NobleCause.ai</a>
		<span>{t("AMF · Fallansicht")}</span>
		<nav class="case-language" aria-label={t("Sprache")}><a href={amfPaths[room].de} lang="de" hreflang="de" aria-current={lang === "de" ? "page" : undefined}>DE</a><a href={amfPaths[room].en} lang="en" hreflang="en" aria-current={lang === "en" ? "page" : undefined}>EN</a></nav>
		<a class="back" href={councilPath}>{t("Zum Ratsraum")}</a>
	</header>

	<StageHero
		scene={'/media/scenes/' + current.scene + '-display.avif'}
		sceneMobile={'/media/scenes/' + current.scene + '-portrait-display.avif'}
		sceneMobile800={'/media/scenes/' + current.scene + '-portrait-800.avif'}
		title={t("Malariaschutz mit AMF")}
		pitch={t("Against Malaria Foundation finanziert Moskitonetze zum Schutz vor Malaria.")}
		roomWord={room === 'study' ? '' : current.name}
		roomLead={current.lead}
		bgPos="center top"
	>
		{#snippet scene2()}
			{#if room === 'study'}
				<div class="case-actors" aria-hidden="true">
					<img class="scout" src="/media/actors/scout.avif" alt="" />
					<img class="warden" src="/media/actors/warden.avif" alt="" />
				</div>
			{:else if room === 'archive'}
				<div class="case-actors" aria-hidden="true"><img class="lectern" src="/media/actors/lectern.avif" alt="" /></div>
			{/if}
		{/snippet}
	</StageHero>

	<div class="case-content">
		<nav class="room-nav" aria-label={t("AMF-Rundgang")}>
			{#each Object.entries(rooms) as [key, entry]}
				<a href={entry.path} aria-current={room === key ? 'page' : undefined}>
					<strong>{entry.name}</strong><span>{entry.action}</span>
				</a>
			{/each}
		</nav>

		<div class="case-main" id="fallinhalt" tabindex="-1">
			{#if room === 'study'}
				<section class="opening" aria-labelledby="leitfrage">
					<p class="dateline">{t("Belege geprüft am")} {caseData.evidenceDate}</p>
					<h2 id="leitfrage">{t("AMF wird empfohlen.")}<br />{t("Was trägt die Empfehlung?")}</h2>
				</section>
				<div class="two-levels">
					<section class="finding supported" aria-labelledby="wirkung">
						<p class="eyebrow">{t("Intervention und Organisation")}</p>
						<h3 id="wirkung">{t("Eine begründete Empfehlung")}</h3>
						<ul class="key-points">
							<li><strong>{t("Empfohlen:")}</strong> {t("GiveWell zählt AMF zu seinen Top Charities.")}</li>
							<li><strong>{t("Basis:")}</strong> {t("Studien zu Netzen, Kostenmodelle und Umsetzung.")}</li>
							<li><strong>{t("Grenzen:")}</strong> {t("Qualität der Nachkontrollen; Annahmen zu anderen Geldgebern.")}</li>
						</ul>
						<a class="text-link" href={evidence('empfehlung')}>{t("Empfehlung und Einschränkungen prüfen")}</a>
					</section>
					<section class="finding uncertain" aria-labelledby="zusatz">
						<p class="eyebrow">{t("Untersuchter Einsatz · Ituri 2027")}</p>
						<h3 id="zusatz">{t("Die zusätzliche Zuweisung bleibt offen")}</h3>
						<ul class="key-points">
							<li><strong>{t("Global:")}</strong> {t("AMF meldet weiteren Finanzierungsbedarf.")}</li>
							<li><strong>{t("Belegt:")}</strong> {t("Für Ituri 2027 sind bereits Mittel gebunden.")}</li>
							<li><strong>{t("Offen für 2027:")}</strong> {t("Zusätzlicher Betrag und passende aktuelle Kosten.")}</li>
						</ul>
						<a class="text-link" href={evidence('bedarf')}>{t("Bedarf und gebundene Mittel prüfen")}</a>
					</section>
				</div>
				<section class="path-panel">
					<div><p class="eyebrow">{t("Eine Frage, unterschiedliche Maßstäbe")}</p><h2>{t("Wann reicht ein Beleg für ein Urteil?")}</h2>
					<div class="vote-summary" role="group" aria-label={t("AMF-Schlussvotum zu Säule B")}>
						<span class="ballot-dots" aria-hidden="true">{#each caseData.voices as voice (voice.model)}<span class="ballot-dot" class:abstain={voice.vote.decision === 'abstain'}></span>{/each}</span>
						<span class="vote-counts"><strong>{t("2× Bedingt Ja")}</strong><span class="separator"> · </span><span>{t("3× Enthaltung")}</span></span>
						<time datetime="2026-10-21">{t("Sitzung 21.10.2026")}</time>
					</div>
					<p class="vote-explanation">{t("Der Nutzen zusätzlichen Geldes blieb im Dossier unklar.")}</p></div>
					<a class="button" href={amfPaths.council[lang]}>{t("Die fünf Positionen öffnen")}</a>
				</section>
				<section class="observation">
					<p class="eyebrow">{t("Später geprüfter Befund · November 2026")}</p>
					<h2>{t("Eine Nachkontrolle zeigt auch den Rückgang")}</h2>
					<p>{t("Im Ituri-Bericht zur Kampagne 2023/24 sank der Anteil brauchbarer Netze von")} <strong>{t("87,1 % nach 9 Monaten")}</strong> {t("auf")} <strong>{t("17,2 % nach 27 Monaten")}</strong>.</p>
					<p class="small">{t("Nachkontrollen 2024–2026. Vermisste Netze sind ausgenommen; zerrissen entsorgte zählen mit.")}</p>
					<a class="text-link" href={evidence('monitoring')}>{t("Messwerte und ihre Grenzen lesen")}</a>
				</section>
			{:else if room === 'council'}
				<section class="opening">
					<p class="dateline">{t("Historische Beratung · 21. Oktober 2026")}</p>
					<h2>{t("Zwei bedingte Empfehlungen.")}<br />{t("Drei Enthaltungen.")}</h2>
					<p class="intro">{t("Der Dissens betraf, welche Begründung vor einer Empfehlung bereits geprüft sein muss.")}</p>
					<p class="temporal">{t("Die November-Belege wurden erst später nachrecherchiert. Die hier gezeigten Stimmen beziehen sich auf das damalige Dossier.")}</p>
					<details class="question"><summary>{t("Die damalige Frage im Wortlaut")}</summary><p>{lang === "en" ? caseData.session.questionTranslation : caseData.session.question}</p>{#if lang === "en"}<details class="original-record"><summary>German original question</summary><p lang="de">{caseData.session.question}</p></details>{/if}</details>
					{#if lang === "en"}<p class="translation-note">English translations of the German record by Codex nc 2 (GPT-6). The original question and statements remain available below.</p>{/if}
				</section>
				<div class="voices">
					{#each caseData.voices as voice, i (voice.model)}
						<details class="voice" name="ratsposition" open={i === 0} id={'stimme-' + voice.family}>
							<summary>
								<img src={voice.medallion} alt="" width="84" height="84" />
								<div class="voice-title"><strong>{voice.label}</strong><span>{voice.heading}</span></div>
								<span class="vote" class:abstain={voice.vote.decision === 'abstain'}>{verdict(voice.vote)}</span>
							</summary>
							<div class="voice-body">
								<p>{voice.summary}</p>
								<p class="attribution">{lang === "en" ? "Final vote on pillar B · English translation" : t("Schlussvotum zu Säule B · Originalwortlaut des Modells")}</p>
								<blockquote>{lang === "en" ? voice.reasonTranslation : voice.reason}</blockquote>
								{#if lang === "en"}<details class="original-record"><summary>German original</summary><blockquote lang="de">{voice.reason}</blockquote></details>{/if}
								<p class="initial">{t("Erstvotum")} <strong>{verdict(voice.initialVote)}</strong> {t("· Schlussvotum")} <strong>{verdict(voice.vote)}</strong></p>
								<a href={voice.protocolHref}>{t("Begründung, Diskussion und damalige Quellen im Protokoll")}</a>
							</div>
						</details>
					{/each}
				</div>
				<section class="editorial">
					<p class="eyebrow">{t("Redaktionelle Einordnung · Belegstand 18. November")}</p>
					<h2>{t("Was die Nachrecherche ergänzt")}</h2>
					<p>{t("Ein konkreter Monitoringbericht ist hinzugekommen. Die Kostentabelle lässt sich der Ituri-Spalte zuordnen. Der für Ituri 2027 noch offene Zusatzbetrag und die dort aktuell geltenden Kosten bleiben im geprüften Material ungeklärt.")}</p>
					<p>{t("Die Modellkarten wurden von Qwen3.8-27B erzeugt und durch Codex nc 2 (GPT-6) am Original geprüft. Vier von acht Karten brauchten Korrekturen, darunter eine Länderzuordnung und vertauschte Prozentwerte.")}</p>
					<div class="link-row"><a href={evidence('monitoring')}>{t("Erhobene Ergebnisse")}</a><a href={evidence('kosten')}>{t("Modellierte Kosten")}</a><a href={evidence('bedarf')}>{t("Finanzierung")}</a></div>
				</section>
			{:else}
				<section class="opening">
					<p class="dateline">{t("Belegstand")} {caseData.evidenceDate} {t("· Links geprüft am")} {caseData.linkCheckDate}</p>
					<h2>{t("Jede Aussage hat einen Ursprung.")}</h2>
					<p class="intro">{t("Erhebungsbericht, Modell und Selbstauskunft beantworten unterschiedliche Fragen. Die Karten zeigen den Stand und die Grenzen jeder Aussage.")}</p>
				</section>
				<div class="evidence-grid">
					{#each caseData.cards as card (card.id)}
						<article class="evidence-card" id={'beleg-' + card.id}>
							<p class="eyebrow">{card.kind}</p><h3>{card.title}</h3>
							<p>{card.claim}</p>
							{#if card.id === 'monitoring'}
								<div class="table-scroll"><table><caption>{t("Ituri 2023/24 · Angaben des AMF-Berichts")}</caption><thead><tr><th>{t("Nach")}</th><th>{t("Vorhanden")}</th><th>{t("Brauchbar")}</th></tr></thead><tbody><tr><th>{t("9 Monate")}</th><td>{t("90,2 %")}</td><td>{t("87,1 %")}</td></tr><tr><th>{t("18 Monate")}</th><td>{t("61,0 %")}</td><td>{t("52,5 %")}</td></tr><tr><th>{t("27 Monate")}</th><td>{t("24,2 %")}</td><td>{t("17,2 %")}</td></tr></tbody></table></div>
								<p class="small">{card.presenceDefinition}</p>
								<p class="small">{card.conditionDefinition}</p>
								<p class="small">{t("16.829, 18.747 und 18.913 befragte Haushalte von jeweils 20.622 vorgesehenen. Nachkontrollen 2024–2026.")}</p>
							{/if}
							<p class="limit">{card.limit}</p>
							<dl><dt>{t("Herausgeber")}</dt><dd>{card.publisher}</dd><dt>{t("Bezugsstand")}</dt><dd>{card.period}</dd><dt>{t("Abgerufen")}</dt><dd>{card.retrieved}</dd><dt>{t("Fundstelle")}</dt><dd>{card.locator}</dd></dl>
							<div class="source-links">{#each card.sources as source}<a href={source.url} rel="external">{source.label}</a>{/each}</div>
						</article>
					{/each}
				</div>
				<p class="review-note">{t("Die November-Karten wurden durch lokale Modellrecherche mit Qwen3.8-27B vorbereitet und von Codex nc 2 (GPT-6) am Original gegengeprüft. Die Links führen zu den Herausgebern, deren Seiten sich weiterentwickeln können. Zwei GiveWell-Grantseiten waren beim Nachrecherchelauf blockiert.")}</p>
			{/if}

			<section class="next-step" aria-labelledby="weiter">
				<h2 id="weiter">{t("Mit dieser Einordnung weitergehen")}</h2>
				<div class="donation-paths">
					<div><h3>{t("Direkt bei AMF")}</h3><p>{t("Allgemeine Spende an AMF, ohne feste Zusage für Ituri 2027.")}</p><a class="button secondary" href={caseData.organization.donation_url} rel="external">{t("AMF-Spendenseite öffnen")}</a></div>
					<div><h3>{t("Zuweisung durch GiveWell")}</h3><p>{t("GiveWell verteilt Fondsmittel flexibel nach aktuellem Forschungsstand.")}</p><a class="button secondary" href="https://www.givewell.org/top-charities-fund" rel="external">{t("Top Charities Fund ansehen")}</a></div>
				</div>
			</section>
		</div>
		<footer class="case-footer">
			<p>{#if caseData.paused}{t("Ratsberatung und automatische Recherche sind pausiert.")}{/if} {t("Diese Fallansicht dokumentiert den geprüften Stand.")}</p>
			<nav aria-label={t("Weitere Inhalte")}><a href={homePath}>NobleCause</a><a href="/sitzungen/2026-10-21-regular/">{t("Originalsitzung")}</a><a href="/manifest/">{t("Manifest")}</a><a href="/impressum/">{t("Impressum")}</a></nav>
		</footer>
	</div>
</div>

<style>
	.case-page { position: relative; isolation: isolate; }
	.case-bar { position: relative; z-index: 2; display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap; padding: 1rem 3vw; background: rgba(5,9,11,.8); border-bottom: 1px solid #74603b; font: .85rem system-ui, sans-serif; }
	.case-bar a { color: #ebd7ad; text-decoration: none; min-height: 44px; display: inline-flex; align-items: center; }
	.case-bar .brand { font-family: Georgia, serif; font-size: 1.2rem; letter-spacing: .02em; }
	.case-bar span { color: #b3b8b2; }
	.case-bar .back { margin-left: auto; }
	.case-language { display: flex; gap: .2rem; margin-left: auto; }
	.case-language a { min-width: 44px; justify-content: center; border: 1px solid #74603b; }
	.case-language [aria-current="page"] { background: #263236; border-color: #dcbb79; }
	.original-record { margin-top: 1rem; }
	.original-record summary { cursor: pointer; color: #d3c29d; padding: .5rem 0; }
	.translation-note { color: #bdc9c7; font-size: .9rem; }
	.skip { position: absolute; top: -100px; left: 1rem; z-index: 10; background: #111b1f; padding: 1rem; }
	.skip:focus { top: 1rem; }
	.case-page :global(.room-hero) { min-height: 25rem; }
	.case-page :global(.room-overlay) { padding-top: 2.4rem; }
	.case-page :global(.room-plaque) { width: min(45rem, calc(100% - 2rem)); padding: 1.5rem 2rem; background: radial-gradient(ellipse 72% 95% at 50% 62%,rgba(3,6,7,.92),rgba(3,6,7,0) 85%); }
	.case-page :global(.room-plaque h1) { font-size: clamp(2rem,4vw,3rem); }
	.case-page :global(.pitch-block) { font-size: 1rem; max-width: 32rem; margin: .8rem auto 0; }
	.case-page :global(.room-word) { font-size: .8rem; }
	.case-page :global(.room-lead) { font-size: 1rem; }
	.case-actors { position: absolute; inset: 0; pointer-events: none; }
	.case-actors img { position: absolute; width: 15rem; bottom: -8rem; opacity: .95; }
	.scout { left: 5%; } .warden { right: 5%; } .lectern { left: 8%; width: 12rem !important; }
	.case-content { position: relative; z-index: 1; width: min(67rem, calc(100% - 3rem)); margin: -3rem auto 0; }
	.room-nav { display: grid; grid-template-columns: repeat(3,1fr); background: #101a1d; border: 1px solid #8d6e3e; box-shadow: 0 10px 40px #0008; }
	.room-nav a { padding: 1.15rem 1.35rem; text-decoration: none; border-right: 1px solid #55472e; color: #c5bda9; min-width: 0; }
	.room-nav a:last-child { border: 0; }
	.room-nav strong { display: block; font-size: 1.2rem; font-weight: 400; color: #efd8a5; }
	.room-nav span { display: block; margin-top: .15rem; font: .85rem/1.4 system-ui,sans-serif; }
	.room-nav [aria-current='page'] { background: #263236; box-shadow: inset 0 3px #dcbb79; }
	.case-main { padding: 2.5rem; background: rgba(7,14,17,.965); border: 1px solid #5e4e34; border-top: 0; }
	h2 { color: #eddbb7; font-size: clamp(1.55rem,3.5vw,2.15rem); font-weight: 400; }
	h3 { color: #eddbb7; font-size: 1.25rem; font-weight: 400; }
	p { margin: .7rem 0 1rem; }
	.opening { max-width: 48rem; margin-bottom: 2rem; }
	.dateline, .eyebrow, .attribution { font: .82rem/1.6 system-ui,sans-serif; letter-spacing: .025em; color: #b9b5a6; }
	.eyebrow { color: #d1b77e; margin-top: 0; }
	.intro { font-size: 1.12rem; color: #cec6b3; max-width: 45rem; }
	.two-levels { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
	.finding { padding: 1.6rem; border: 1px solid #485d60; background: linear-gradient(135deg,#1b2b30,#111d20); }
	.finding.uncertain { background: linear-gradient(135deg,#29271e,#181e1d); border-color: #796339; }
	.key-points { margin: .9rem 0 .6rem; padding-left: 1.1rem; font-size: 1rem; line-height: 1.5; }
	.key-points li { padding-left: .15rem; margin-bottom: .65rem; }
	.key-points li::marker { color: #bba16e; }
	.key-points strong { color: #eddbb7; }
	.finding h3 { margin-top: .2rem; font-size: 1.5rem; }
	a { color: #e8c37c; text-underline-offset: .22em; }
	a:hover { color: #fff0c4; }
	.case-page :global(a:focus-visible), .case-page :global(summary:focus-visible) { outline: 3px solid #f4ce79; outline-offset: 5px; }
	.text-link { display: inline-block; padding: .5rem 0; }
	.path-panel { display: flex; align-items: center; gap: 2rem; border-block: 1px solid #4d4b3e; padding: 2rem 0; margin: 2rem 0; }
	.path-panel h2 { font-size: 1.65rem; }
	.path-panel p { max-width: 39rem; }
	.button { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: .75rem 1.15rem; background: #d8ba7e; color: #172024; border: 1px solid #d8ba7e; text-decoration: none; text-align: center; font: 600 .9rem/1.45 system-ui,sans-serif; flex-shrink: 0; }
	.button:hover { background: #efd5a3; color: #172024; }
	.secondary { background: #202b2d; color: #ecd6a7; border-color: #907645; }
	.observation { max-width: 45rem; }
	.vote-summary { display: flex; align-items: center; flex-wrap: wrap; gap: .55rem .8rem; margin: 1rem 0 .55rem; font: .9rem/1.5 system-ui,sans-serif; }
	.ballot-dots { display: inline-flex; gap: .35rem; }
	.ballot-dot { width: .65rem; height: .65rem; border-radius: 50%; background: #eac780; border: 1px solid #f4d898; }
	.ballot-dot.abstain { background: #a8c1cb; border-color: #c4d6dd; }
	.vote-counts { color: #c4d6dd; }
	.vote-counts strong { color: #eac780; font-weight: 600; }
	.vote-counts .separator { color: #b9b5a6; padding-inline: .25rem; }
	.vote-summary time { padding-left: .8rem; border-left: 1px solid #657476; color: #b9b5a6; font-size: .875rem; }
	.vote-explanation { margin: .55rem 0 0; }
	.observation h2 { font-size: 1.65rem; }
	.temporal { border-left: 2px solid #aa8b52; padding: .4rem 0 .4rem 1rem; color: #c9c1ae; }
	.question { border-bottom: 1px solid #3e4948; padding-bottom: .7rem; }
	.question summary { cursor: pointer; color: #d3c29d; padding: .5rem 0; }
	.voices { display: grid; gap: .85rem; }
	.voice { background: #111d20; border: 1px solid #5e573e; }
	.voice > summary { display: grid; grid-template-columns: 4.8rem 1fr auto; gap: 1rem; align-items: center; padding: 1.1rem 1.3rem; cursor: pointer; list-style: none; }
	.voice > summary::-webkit-details-marker { display: none; }
	.voice > summary img { width: 4.8rem; height: 4.8rem; object-fit: contain; border-radius: 50%; }
	.voice-title strong { display: block; color: #eddbb7; font-size: 1.2rem; font-weight: 400; }
	.voice-title span { display: block; font: .85rem/1.5 system-ui,sans-serif; color: #bfbda9; }
	.voice:not([open]) .voice-title span::after { content: ' · öffnen'; color: #dec48d; }
	.case-page[lang='en'] .voice:not([open]) .voice-title span::after { content: ' · open'; }
	.vote { display: inline-block; max-width: 11rem; font: .85rem/1.4 system-ui,sans-serif; color: #eac780; border-bottom: 1px solid #8e7343; padding-bottom: .2rem; }
	.vote.abstain { color: #b2c7cf; border-color: #496875; }
	.voice[open] { border-color: #b18c50; background: #18282c; }
	.voice-body { padding: 0 1.5rem 1.4rem; border-top: 1px solid #4e503c; }
	blockquote { border-left: 2px solid #a3874c; padding: 0 0 0 1rem; margin: .7rem 0 1rem; color: #ded9ca; font-size: .95rem; }
	.initial { font: .82rem/1.7 system-ui,sans-serif; color: #aebfc1; }
	.editorial { margin-top: 2.2rem; border: 1px solid #756445; padding: 1.6rem; background: #24271f; }
	.editorial h2 { font-size: 1.6rem; }
	.link-row { display: flex; flex-wrap: wrap; gap: 1rem; }
	.evidence-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1.25rem; }
	.evidence-card { min-width: 0; overflow-wrap: anywhere; border: 1px solid #536062; background: #152226; padding: 1.6rem; scroll-margin-top: 1.25rem; }
	.evidence-card:target { border: 2px solid #e0b86b; }
	.evidence-card h3 { font-size: 1.5rem; margin-top: 0; }
	.limit { border-left: 2px solid #bba16e; padding-left: 1rem; color: #c5c1b2; }
	dl { display: grid; grid-template-columns: 7rem 1fr; gap: .35rem 1rem; font: .85rem/1.6 system-ui,sans-serif; }
	dt { color: #a6bdc1; } dd { margin: 0; overflow-wrap: anywhere; }
	.source-links { display: flex; flex-wrap: wrap; gap: .6rem 1.5rem; margin-top: 1.1rem; }
	.table-scroll { max-width: 100%; overflow-x: auto; }
	table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-variant-numeric: tabular-nums; font-size: .95rem; }
	caption { text-align: left; color: #b9c9c6; font-size: .85rem; padding: .4rem 0; }
	th, td { text-align: left; padding: .6rem; border-bottom: 1px solid #51605b; }
	.small, .review-note { font-size: .88rem; color: #b9c3ba; }
	.next-step { margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid #79623b; }
	.next-step h2 { font-size: 1.7rem; }
	.donation-paths { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
	.donation-paths h3 { font-size: 1.25rem; }
	.donation-paths p { color: #c5c1b4; }
	.case-footer { position: relative; padding: 1.5rem 1rem 2rem; font-size: .82rem; background: #071115ee; text-align: center; }
	.case-footer p { margin: 0 0 1rem; color: #c9bd9f; }
	.case-footer nav { display: flex; justify-content: center; gap: 1.2rem; flex-wrap: wrap; }
	@media (max-width: 800px) {
		.case-page :global(.room-hero) { min-height: 22rem; }
		.case-actors .scout { left: -3rem; width: 12rem; bottom: -6rem; }
		.case-actors .warden { right: -3rem; width: 12rem; bottom: -6rem; }
		.case-bar { gap: .8rem; padding: .6rem 1rem; }
		.case-bar span { display: none; }
		.case-content { width: calc(100% - 1.5rem); margin-top: -2rem; }
		.case-main { padding: 1.5rem; }
		.room-nav a { padding: .9rem .65rem; }
		.room-nav strong { font-size: 1rem; }
		.room-nav span { font-size: .8rem; }
		.two-levels, .donation-paths { grid-template-columns: 1fr; }
		.path-panel { display: block; }
		.voice > summary { grid-template-columns: 3.7rem 1fr; gap: .55rem .8rem; padding: 1rem; }
		.voice > summary img { width: 3.7rem; height: 3.7rem; grid-row: span 2; }
		.voice-title strong { font-size: 1.1rem; }
		.vote { grid-column: 2; max-width: none; width: fit-content; }
		.voice-body { padding: 0 1rem 1rem; }
		.evidence-card { padding: 1.2rem; }
		dl { grid-template-columns: 1fr; gap: .15rem; }
		dd { margin-bottom: .6rem; }
		th, td { padding: .5rem .25rem; }
		th { font: 600 .82rem/1.4 system-ui, sans-serif; letter-spacing: 0; text-transform: none; }
		.case-page[lang='en'] th { font-size: .75rem; white-space: nowrap; overflow-wrap: normal; }
	}
	@media (max-width: 420px) {
		.case-main { padding: 1.25rem 1rem; }
		.room-nav span { display: none; }
		.room-nav a { text-align: center; padding: 1rem .25rem; }
		.finding { padding: 1.2rem; }
		.case-bar .back { font-size: .8rem; }
	}
</style>
