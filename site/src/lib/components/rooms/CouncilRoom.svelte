<script>
	// The Council: Saal-Plates (quer/hoch, geschlossen/offen — Nachtrag-Serie
	// 24.07.), zweite Ebene CouncilActors (N Lesepulte fahren von unten ein,
	// Szene-Kantenprinzip), Ergebnis-Tafel (betonter Zählstand), Zähl-Block
	// „Wie gezählt wurde" (je Bereich Modell-Marken mit Erst-/Schlussvotum),
	// volle Voten-Matrix hinter Ausklapp, Türen. Sprache als Prop; orgEn =
	// optionale englische
	// Organisationsbeschreibungen (Registry-Feld beschreibung_en, aufgelöst im
	// Layout-Load) — derzeit ohne Anzeigefläche im Raum (Mechanismus lebt in
	// RecommendationCard.svelte, Beschreibungen in Registry/Sitzungsseite).
	// Vorbehalte sind publizierter Rekord und bleiben deutsch — im EN-Modus mit
	// recordNote. Der Prozess läuft nur noch über die Röhre (StageTube) — die
	// FlowRail ist mit der Titelbereich-Neuordnung entfallen; der Kopf ist der
	// stabile, auf allen Räumen identische Block. Die Teilnehmerzahl steckt in
	// den Datenpfaden (modelTracks, Röhren-Schritt 3), nicht in der Copy.
	import CouncilActors from './CouncilActors.svelte';
	import CouncilMachine from './CouncilMachine.svelte';
	import Door from './Door.svelte';
	import ModelPulpits from './ModelPulpits.svelte';
	import ResultBoard from './ResultBoard.svelte';
	import StageHero from './StageHero.svelte';
	import StageTube from './StageTube.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';
	import { formatDate } from '$lib/format.js';
	import { TUBE_FILLED } from '$lib/stage.js';
	import { DOOR_PASSAGES } from '$lib/door-passages.js';

	let { home, lang = 'de', orgEn = {} } = $props();
	void orgEn; // Prop bleibt verdrahtet (Mechanismus), hat hier keine Anzeigefläche.

	let t = $derived(locales[lang]);
	// Die große Tür im Saal-Plate führt WEITER ins Archiv — Daten wie bei der
	// Tür-Karte (sub/label). Der Rundgang läuft Study → Council → Archive.
	let archiveDoor = $derived(t.council.doors.find((door) => door.label === 'The Archive'));

	// Zoom-Ursprung der Raumfahrt auf die Türmitte legen (Tastatur/Kartenrand) —
	// reine progressive Enhancement; ohne JS bleibt der Link ein Link.
	function setDoorOrigin(event) {
		const rect = event.currentTarget.getBoundingClientRect();
		document.documentElement.style.setProperty(
			'--vt-origin',
			`${rect.left + rect.width / 2}px ${rect.top + rect.height / 2}px`
		);
	}
	// Zeitschicht: das geplante Sitzungsdatum wird server-gerendert (No-JS = voll).
	// Ob es verstrichen ist, entscheidet NUR der Client relativ zum Betrachtungs-
	// zeitpunkt — kein buildTime, kein Überfällig-Zustand. $effect läuft client-only.
	let nextSessionPast = $state(false);
	$effect(() => {
		const iso = home?.schedule?.nextSession;
		nextSessionPast = iso ? new Date(iso).getTime() < Date.now() : false;
	});
	let tracks = $derived(home?.modelTracks ?? []);
	let participantCount = $derived(tracks.length);
	// Vorbehalte und Voten sind publizierter Rekord (deutsch) — im EN-Modus markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
	// §4.2 „Wie gezählt wurde": je Bereich eine Zeile, darin je Teilnehmer eine
	// Marke mit seiner Nennung — generisch aus modelTracks, skaliert mit N
	// (kein festes Drei-Spalten-Raster). Revisionen leben in der Marke selbst
	// (Erstvotum durchgestrichen, Schlussvotum darunter).
	let countRows = $derived(
		(home?.recommendations ?? []).map((rec) => ({
			rec,
			marks: tracks.map((track) => ({
				label: track.label,
				model: track.model,
				row: track.rows.find((row) => row.pillar === rec.pillar) ?? null
			}))
		}))
	);
</script>

<svelte:head>
	<title>{t.council.head.title}</title>
	<meta name="description" content={t.council.head.description} />
	<link rel="preload" as="image" href="/media/scenes/hall-display.avif" media="(min-width: 1200px)" />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.council.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.council.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.council.de}" />
</svelte:head>

{#if home}
	<StageHero
		scene="/media/scenes/hall-display.avif"
		sceneMobile="/media/scenes/hall-portrait-display.avif"
		sceneMobile800="/media/scenes/hall-portrait-800.avif"
		passage={DOOR_PASSAGES.council}
		bgPos="center top"
		title={t.common.heroTitle}
		pitch={t.common.heroPitch}
		whySummary={t.common.whySummary}
		whyBody={t.common.whyBody}
		roomWord={t.council.roomWord}
		roomLead={t.council.lead}
	>
		{#snippet overlay()}
			{#if archiveDoor}
				<!-- Die Tür IM Saal-Bild: Hotspot auf der gemalten Doppeltür, führt
				     weiter ins Archiv. Echter Link (No-JS/Tastatur); die Tür-Karte
				     unten bleibt der auffindbare Weg. Ratssaal-eigene Türgeometrie
				     (s. CSS) — Unterkante über der Zählmaschine. -->
				<a
					class="door-hotspot"
					href={archiveDoor.href}
					aria-label="{archiveDoor.sub}: {archiveDoor.label}"
					title="{archiveDoor.sub}: {archiveDoor.label}"
					onclick={setDoorOrigin}
				></a>
			{/if}
		{/snippet}
		{#snippet scene2()}
			<!-- Zweite Ebene: die Zählmaschine (P10, deckungsgleich über der
			     gemalten) — hinter den Pulten, trägt später §7-Verdeckung/§8-Ruck. -->
			<CouncilMachine {t} {tracks} />
			<!-- Zweite Ebene: die Lesepulte der Teilnehmer nehmen von unten ihre
			     Plätze ein (Kantenprinzip) — generisch aus modelTracks, N Pulte
			     im Saal; Türachse und Zählmaschine bleiben frei. -->
			<CouncilActors {t} {tracks} />
		{/snippet}
		{#snippet tube()}
			<!-- Prozess-Röhre: The Council steht bei Zählen (Stand 5 von 6). -->
			<StageTube
				flow={t.study.flow}
				filledCount={TUBE_FILLED.council}
				{participantCount}
				label={t.tube.label}
				status={t.tube.status(5, t.study.flow.length)}
			>
				{#snippet caption()}
					<!-- Zeitschicht (Council): Sitzungstakt als Bedingung + Termin als
					     Zitat aus schedule.next_session. Datum server-gerendert (No-JS =
					     voll); verstrichen → entfällt clientseitig (nextSessionPast). -->
					<p>
						{t.council.rhythm}{#if home?.schedule?.nextSession && !nextSessionPast}{' '}{t.council.nextSession(
								formatDate(home.schedule.nextSession, t.lang)
							)}{/if}
					</p>
				{/snippet}
			</StageTube>
		{/snippet}
	</StageHero>

	<main>
		<!-- Dieselbe Tafel wie in The Study, hier mit betontem Zählstand. -->
		<ResultBoard {home} {t} emphasizeCount />

		<!-- §4.2 „Wie gezählt wurde" — ein Block ersetzt drei (Empfehlungen /
		     Revisionen / Zählwerk): je Bereich eine Zeile, darin je Teilnehmer
		     eine Marke mit seiner Nennung. Die Tafel oben trägt das Was; hier
		     steht ausschließlich das Zustandekommen. -->
		<section class="room-section" aria-labelledby="count-title">
			<h2 id="count-title">{t.council.countTitle}</h2>
			<p class="count-intro">{t.council.countIntro}</p>
			<!-- Fokus-Auswahl als CSS-Radiogruppe: der Klick auf ein Emblem aktualisiert
			     NUR den Trichter (Maschinenergebnis), kein Sprung — kein Fragment, kein
			     Scroll. Jedes Radio liegt IN seinem Label und füllt es unsichtbar (bleibt
			     im Blick → kein Fokus-Scroll). Reveal über .room-section:has(:checked).
			     Vorgabe: erster Bereich (Zukunft). Kein JS; tastaturbedienbar. -->
			<div class="count-jump" role="radiogroup" aria-label={t.council.jumpToArea}>
				{#each countRows as { rec }, i (rec.pillar)}
					<label class="count-jumplink">
						<input class="cf-radio" type="radio" name="cf-focus" id="cf-{rec.pillar}" checked={i === 0} />
						<img src={t.pillars[rec.pillar]?.src} alt="" width="40" height="40" loading="lazy" />
						{t.pillars[rec.pillar]?.label ?? rec.pillarName}
					</label>
				{/each}
			</div>
			<!-- 2b: der Zählstrang als senkrechter Trichter — drei Pulte → Trichter →
			     Trommel, EIN Bereich im Fokus (Vorgabe Zukunft; Auswahl über die
			     Embleme via :target/:has, kein JS). Kastenlos: Vignette + Haarlinie.
			     Eigener dunkler Schleier hinter dem Block, damit der Trichter für sich
			     steht (nicht die Szenenmaschine dahinter). aria-hidden — die
			     Vier-Bereiche-Liste darunter ist der vollständige, lesbare Rekord. -->
			<div class="counting-funnel" aria-hidden="true">
				<div class="cf-columns">
					{#each tracks as track (track.model)}
						<div class="cf-col">
							<img class="cf-med" src="/media/medallions/{track.model}-lo.avif" alt="" width="256" height="256" loading="lazy" />
							<span class="cf-model">{track.label}</span>
							<span class="cf-votes">
								{#each track.rows as row (row.pillar)}
									<span class="cf-vote" data-b={row.pillar}>
										{#if row.changed}<del>{row.initial.organization.name}</del> <strong>{row.final.organization.name}</strong> <em class="cf-changed">{t.council.changedMark}</em>{:else if row.final}<strong>{row.final.organization.name}</strong>{:else}<span class="mark-none">{t.council.noVote}</span>{/if}
									</span>
								{/each}
							</span>
						</div>
					{/each}
				</div>
				<!-- Der Trichter: Haarlinien aus den Spaltenmitten laufen auf einen Punkt
				     mittig unten zusammen. non-scaling-stroke hält die Linie hauchdünn. -->
				<svg class="cf-lines" viewBox="0 0 100 40" preserveAspectRatio="none">
					{#each tracks as _track, i (i)}
						<line
							x1={(((i + 0.5) / tracks.length) * 100).toFixed(2)}
							y1="0"
							x2="50"
							y2="40"
							vector-effect="non-scaling-stroke"
						/>
					{/each}
				</svg>
				<div class="cf-machine">
					<div class="cf-cutout"></div>
					{#each countRows as { rec } (rec.pillar)}
						<div class="cf-plaque" data-b={rec.pillar}>
							<img class="cf-plaque-emblem" src={t.pillars[rec.pillar]?.src} alt="" width="40" height="40" loading="lazy" />
							{#if rec.hasConsensus}
								<span class="cf-plaque-count">{rec.count} {t.common.ofWord} {rec.total}</span>
								<span class="cf-plaque-org">{rec.organization.name}</span>
							{:else}
								<span class="cf-plaque-count split">{t.council.countSplit}</span>
							{/if}
						</div>
					{/each}
				</div>
			</div>
			<ol class="count-rows">
				{#each countRows as { rec, marks } (rec.pillar)}
					<li>
						<div class="count-head">
							<img src={t.pillars[rec.pillar]?.src} alt="" width="40" height="40" loading="lazy" />
							<span class="count-area">{t.pillars[rec.pillar]?.label ?? rec.pillarName}</span>
							{#if rec.hasConsensus}
								<span class="count-tally">→ {rec.count} {t.common.ofWord} {rec.total}</span>
							{:else}
								<span class="count-tally split">→ {t.council.countSplit}</span>
							{/if}
						</div>
						<div class="count-marks">
							{#each marks as mark (mark.label)}
								<span class="mark">
									<span class="mark-model">{mark.label}</span>
									{#if mark.row?.changed}
										<del>{mark.row.initial.organization.name}</del>
										<strong>{mark.row.final.organization.name}</strong>
									{:else if mark.row?.final}
										<strong>{mark.row.final.organization.name}</strong>
									{:else}
										<span class="mark-none">{t.council.noVote}</span>
									{/if}
								</span>
							{/each}
						</div>
						{#if rec.hasConsensus && rec.conditionalCount}
							<details class="count-reservation">
								<summary>{t.council.reservation}</summary>
								{#each rec.reservations as reservation (reservation.model)}
									<p lang={recordLang}>{reservation.model}: {reservation.reservation}</p>
								{/each}
								{#if t.common.recordNote}
									<small class="record-note">{t.common.recordNote}</small>
								{/if}
							</details>
						{/if}
					</li>
				{/each}
			</ol>
			<!-- §4.3: die volle Matrix — ein Anker am Blockende, nicht je Zeile. -->
			<details class="all-votes">
				<summary>{t.council.allVotesVerbatim}</summary>
				<ModelPulpits tracks={home.modelTracks} sessionId={home.currentSession.id} {t} />
			</details>
			<p class="money-flow">{t.common.moneyFlow}</p>
		</section>

		<section class="room-section" aria-labelledby="doors-title">
			<h2 id="doors-title">{t.common.doorsTitle}</h2>
			<div class="door-gallery">
				{#each t.council.doors as door (door.href)}
					<Door {door} />
				{/each}
			</div>
		</section>
	</main>
{/if}

<style>
	/* ---- Tür-Hotspot (Ratssaal-eigene Werte) ------------------------------
	   Türzone des hall-Plate (1672×941, 16:9), am gerenderten Plate gemessen
	   x ≈ 43,5–57,9 %, y ≈ 18,3–65,9 %. Unterkante bewusst bei 66 %, NICHT
	   tiefer — sonst liegt der Hotspot über der Zählmaschine auf ihrem Sockel
	   und schluckt sie. object-position center top → die Mitte überlebt jeden
	   cover-Crop; ab 1200 px immer wirksam. Zwei Fälle je Viewport-Ratio ggü.
	   16:9 (wie Study/Archive). Hover/Fokus öffnet die Tür (Crossfade in
	   StageHero); die Blende liest ihr Rechteck beim Klick aus
	   getBoundingClientRect(). */
	.door-hotspot {
		display: none;
	}
	@media (min-width: 1200px) {
		.door-hotspot {
			display: block;
			position: absolute;
			border-radius: 6px;
			cursor: pointer;
			pointer-events: auto;
		}
	}
	/* Bild füllt die Höhe (Viewport schmaler als 16:9): Bildbreite = 177,78 svh,
	   Mitte bei 50 vw → Türzone in svh um 50 vw; y direkt in svh. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.door-hotspot {
			left: calc(50vw - 11.56svh);
			top: 18.3svh;
			width: 25.6svh;
			height: 47.6svh;
		}
	}
	/* Bild füllt die Breite (Viewport breiter als 16:9): Bildhöhe = 56,25 vw,
	   Vertikal-Crop ab top → Türzone komplett in vw. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.door-hotspot {
			left: 43.5vw;
			top: 10.29vw;
			width: 14.4vw;
			height: 26.78vw;
		}
	}
	.door-hotspot:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 2px;
	}

	/* „Wie gezählt wurde": je Bereich eine Zeile — Kopf mit Emblem, Bereich und
	   Zählstand, darunter die Modell-Marken mit den Nennungen (Revisionen in
	   der Marke: Erstvotum durchgestrichen, Schlussvotum darunter). */
	.count-intro {
		margin: 0 0 0.7rem;
		color: #c7bca7;
		font-size: 0.95rem;
	}
	/* Sprungleiste: Anker mit Säulen-Emblem, Vignette statt Kasten (wie im Explorer). */
	.count-jump {
		display: flex;
		flex-wrap: wrap;
		gap: 0.3rem 0.6rem;
		margin: 0 0 1rem;
	}
	.count-jumplink {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		min-height: 44px;
		padding: 0.3rem 0.85rem 0.3rem 0.35rem;
		border-radius: 999px;
		color: #c9ab6e;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		text-decoration: none;
		background: radial-gradient(ellipse 88% 100% at 26% 50%, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0) 72%);
	}
	.count-jumplink img {
		width: 1.8rem;
		height: 1.8rem;
		border: 1px solid rgba(190, 139, 58, 0.6);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.count-jumplink:hover {
		color: #e7c881;
	}
	.count-jumplink:hover img {
		border-color: #a67b3d;
	}
	.count-jumplink {
		position: relative;
		cursor: pointer;
	}
	/* Das Radio füllt sein Label unsichtbar — der Klick trifft es direkt, der Fokus
	   bleibt im sichtbaren Bereich (kein Scroll). Fokussierbar (Tastatur). */
	.cf-radio {
		position: absolute;
		inset: 0;
		margin: 0;
		opacity: 0;
		cursor: pointer;
	}
	/* Gewähltes Emblem leuchtet; Tastatur-Fokus als Ring am Label. */
	.count-jumplink:has(.cf-radio:checked) {
		color: #f0d899;
	}
	.count-jumplink:has(.cf-radio:checked) img {
		border-color: #e7c881;
		box-shadow:
			0 0 0 1px rgba(213, 166, 87, 0.5),
			0 0 12px rgba(213, 166, 87, 0.3);
	}
	.count-jumplink:has(.cf-radio:focus-visible) {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	/* ---- 2b: der senkrechte Zählstrang (Trichter) ---------------------------
	   Drei Modell-Spalten → Haarlinien laufen nach unten auf einen Punkt zusammen
	   → größeres Maschinen-Cutout mit Plakette → „wandert auf die Tafel". EIN
	   Bereich im Fokus (Vorgabe A/Zukunft, Auswahl via :has()+:target). Kastenlos:
	   Vignette + Haarlinie. Eigener dunkler Schleier (Lichtkegel-Logik), damit der
	   Trichter für sich steht. isolation:isolate hält den Schleier über der fixen
	   Szene, unter dem Blockinhalt. Kein JS, bewegungslos. */
	.counting-funnel {
		position: relative;
		isolation: isolate;
		margin: 0.4rem 0 1.6rem;
		padding: 1.4rem 1.1rem 1.1rem;
		/* Ein weicher Rand fasst den Block, der Grund bleibt halbtransparent (die
		   Szene dahinter schimmert durch, ist aber gedämpft). */
		border: 1px solid rgba(166, 123, 61, 0.34);
		border-radius: 7px;
	}
	.counting-funnel::before {
		content: '';
		position: absolute;
		inset: 0;
		z-index: -1;
		pointer-events: none;
		border-radius: inherit;
		background: radial-gradient(
			ellipse 94% 90% at 50% 46%,
			rgba(2, 4, 6, 0.66),
			rgba(2, 4, 6, 0.5) 68%,
			rgba(2, 4, 6, 0.28) 100%
		);
	}
	/* Drei Spalten: Medaillon, Versalien-Name, Votum (nur der Fokus-Bereich). */
	.cf-columns {
		display: flex;
		gap: 1rem;
		align-items: start;
	}
	.cf-col {
		flex: 1 1 0;
		min-width: 0;
		display: grid;
		justify-items: center;
		gap: 0.3rem;
		text-align: center;
	}
	.cf-med {
		width: 3.2rem;
		height: 3.2rem;
		border-radius: 50%;
		filter: drop-shadow(0 1px 4px rgba(0, 0, 0, 0.75));
	}
	.cf-model {
		color: #d5a657;
		font: 600 0.64rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.cf-votes {
		margin-top: 0.15rem;
	}
	/* Votum als Vignette, kein Kasten. Nur der Fokus-Bereich ist sichtbar. */
	.cf-vote {
		display: none;
		padding: 0.4rem 0.7rem 0.5rem;
		color: #e6dbc4;
		font-size: 0.95rem;
		line-height: 1.35;
		background: radial-gradient(ellipse 92% 100% at 50% 45%, rgba(3, 6, 7, 0.72), rgba(3, 6, 7, 0) 82%);
	}
	.cf-vote del {
		display: block;
		color: #8f866f;
		font-size: 0.84rem;
		text-decoration-color: rgba(197, 145, 60, 0.8);
	}
	.cf-vote strong {
		font-weight: 600;
	}
	.cf-changed {
		margin-left: 0.35rem;
		color: #dfbd70;
		font: 600 0.58rem ui-sans-serif, system-ui;
		font-style: normal;
		letter-spacing: 0.09em;
		text-transform: uppercase;
		white-space: nowrap;
	}
	/* Der Trichter: Haarlinien aus den Spaltenmitten auf einen Punkt mittig unten. */
	.cf-lines {
		display: block;
		width: 100%;
		height: 2.6rem;
		margin: 0.1rem 0 0;
		overflow: visible;
	}
	.cf-lines line {
		stroke: rgba(190, 139, 58, 0.62);
		stroke-width: 1;
	}
	/* Der Zielpunkt: das Cutout, deutlich größer, zentriert; die Plakette daran. */
	.cf-machine {
		position: relative;
		width: max-content;
		max-width: 100%;
		margin: 0 auto;
	}
	/* Nur die Maschine + Podest aus dem großen, registrierten Plate-Asset (die
	   Maschine sitzt dort unten-mittig in einem meist leeren Frame) — per
	   Background-Crop freigestellt, deutlich größer als eine Randnotiz. */
	.cf-cutout {
		width: clamp(12rem, 30vw, 16rem);
		aspect-ratio: 320 / 305;
		background-image: url(/media/actors/council-machine.avif);
		background-repeat: no-repeat;
		background-size: 522% auto;
		background-position: 51% 92%;
		filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.6));
	}
	.cf-plaque {
		display: none;
		position: absolute;
		left: 50%;
		bottom: 6%;
		transform: translateX(-50%);
		width: max-content;
		max-width: 94%;
		text-align: center;
		padding: 0.45rem 1.4rem 0.6rem;
		background: radial-gradient(ellipse 84% 98% at 50% 50%, rgba(3, 6, 7, 0.92), rgba(3, 6, 7, 0) 78%);
		text-shadow: 0 1px 8px rgba(3, 6, 7, 0.96);
	}
	/* Statt der Textzeile „Trommel · <Säule>" das Säulen-Emblem über dem Zählstand. */
	.cf-plaque-emblem {
		display: block;
		width: 2rem;
		height: 2rem;
		margin: 0 auto 0.15rem;
		border: 1px solid rgba(190, 139, 58, 0.7);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.cf-plaque-count {
		display: block;
		margin: 0.1rem 0 0.05rem;
		color: #f0d899;
		font: 400 1.7rem Georgia, 'Times New Roman', serif;
		letter-spacing: 0.03em;
	}
	.cf-plaque-count.split {
		font-size: 1.05rem;
		color: #c7bca7;
	}
	.cf-plaque-org {
		display: block;
		color: #e6dbc4;
		font-size: 0.92rem;
	}
	/* Fokus-Steuerung über die Radiogruppe: nur der gewählte Bereich ist sichtbar.
	   Vorgabe A ist per checked gesetzt. :has() auf dem Abschnitt entkoppelt die
	   DOM-Position der Radios — reines CSS, kein JS, kein Fragment/Scroll. */
	:global(.room-section:has(#cf-A:checked)) .cf-vote[data-b='A'],
	:global(.room-section:has(#cf-B:checked)) .cf-vote[data-b='B'],
	:global(.room-section:has(#cf-C:checked)) .cf-vote[data-b='C'],
	:global(.room-section:has(#cf-D:checked)) .cf-vote[data-b='D'],
	:global(.room-section:has(#cf-A:checked)) .cf-plaque[data-b='A'],
	:global(.room-section:has(#cf-B:checked)) .cf-plaque[data-b='B'],
	:global(.room-section:has(#cf-C:checked)) .cf-plaque[data-b='C'],
	:global(.room-section:has(#cf-D:checked)) .cf-plaque[data-b='D'] {
		display: block;
	}
	@media (max-width: 34rem) {
		.cf-columns {
			gap: 0.5rem;
		}
		.cf-med {
			width: 2.5rem;
			height: 2.5rem;
		}
		.cf-vote {
			font-size: 0.85rem;
		}
		.cf-cutout {
			width: clamp(10rem, 60vw, 14rem);
		}
	}
	.count-rows {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
	}
	.count-rows > li {
		padding: 0.7rem 0;
	}
	.count-rows > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.3);
	}
	.count-head {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.35rem 0.7rem;
	}
	.count-head img {
		width: 2.2rem;
		height: 2.2rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.count-area {
		color: #c9ab6e;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.count-tally {
		color: #dfbd70;
		font: 600 0.85rem ui-sans-serif, system-ui;
		white-space: nowrap;
	}
	.count-tally.split {
		color: #c7bca7;
		font-weight: 400;
	}
	/* Die Marken: generisch eine je Teilnehmer — flex-wrap statt festem
	   Drei-Spalten-Raster, skaliert mit der Council-Größe. */
	.count-marks {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-top: 0.55rem;
	}
	.mark {
		display: grid;
		gap: 0.1rem;
		align-content: start;
		min-width: min(11rem, 100%);
		flex: 1 1 min(11rem, 100%);
		padding: 0.55rem 0.7rem;
		background: #0b1011;
		border: 1px solid #7a5a2f;
		color: #e6dbc4;
		font-size: 0.85rem;
	}
	.mark-model {
		color: #d5a657;
		font: 600 0.62rem ui-sans-serif, system-ui;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.mark del {
		color: #8f866f;
		font-size: 0.8rem;
		text-decoration-color: rgba(197, 145, 60, 0.8);
	}
	.mark strong {
		font-weight: 600;
	}
	.mark-none {
		color: #8f866f;
	}
	.count-reservation {
		margin-top: 0.4rem;
	}
	.count-reservation summary {
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e0c07f;
		font-size: 0.85rem;
	}
	.count-reservation summary:hover {
		color: #f2d9a0;
	}
	.count-reservation summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.count-reservation p {
		margin: 0 0 0.4rem;
		color: #e0c07f;
		font-size: 0.85rem;
	}
	.record-note {
		display: block;
		margin: -0.2rem 0 0.4rem;
		color: #9e927f;
		font-size: 0.72rem;
		font-style: italic;
	}
	.money-flow {
		margin: 0.9rem 0 0;
		color: #9e927f;
		font: 0.72rem ui-sans-serif, system-ui;
	}

	/* Volle Voten-Matrix hinter Ausklapp am Blockende. */
	.all-votes {
		margin-top: 0.9rem;
	}
	.all-votes summary {
		cursor: pointer;
		min-height: 44px;
		display: inline-flex;
		align-items: center;
		color: #e7c881;
		font-size: 0.98rem;
	}
	.all-votes summary:hover {
		color: #f2d9a0;
	}
	.all-votes summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.all-votes[open] summary {
		margin-bottom: 0.9rem;
	}
</style>
