<script>
	// The Study: Ergebnis-Tafel (eigenständiges Schiefer-Panel, ab 1200 px fix —
	// siehe ResultBoard.svelte), Klartext-Antwort, Dossiers mit sichtbarem
	// Klartext-Kontext + Zitat-Beleg, Türen. Der Prozess läuft nur noch über
	// die Röhre (StageTube) — die FlowRail ist mit der Titelbereich-Neuordnung
	// entfallen; der Kopf ist der stabile, auf allen Räumen identische Block.
	// Sprache kommt als Prop; Texte aus locales[lang]. Teilnehmerzahl und Familien
	// kommen aus den Daten (modelTracks) — nichts davon steht fest in der Copy.
	// Publizierte Rekordtexte (Sitzungs-Kontext, Frage, Suchanfragen) bleiben
	// deutsch; im EN-Modus kennzeichnet sie common.recordNote. Die Tafel zeigt
	// die vier Empfehlungen aus home.recommendations — gelesen, niemals neu
	// gezählt; Spendenlinks kommen registry-aufgelöst aus den Daten.
	import Door from './Door.svelte';
	import ResultBoard from './ResultBoard.svelte';
	import StageHero from './StageHero.svelte';
	import StageTube from './StageTube.svelte';
	import StudyActors from './StudyActors.svelte';
	import { locales, roomPaths } from '$lib/i18n/index.js';
	import { formatDate } from '$lib/format.js';
	import { TUBE_FILLED } from '$lib/stage.js';
	import { DOOR_PASSAGES } from '$lib/door-passages.js';

	let { home, lang = 'de' } = $props();

	let t = $derived(locales[lang]);
	let tracks = $derived(home?.modelTracks ?? []);
	let participantCount = $derived(tracks.length);
	// Rekordtexte (Frage, Suchanfragen, Rats-Wortlaut) sind deutsch — im
	// EN-Modus markiert.
	let recordLang = $derived(lang === 'en' ? 'de' : undefined);
	// Klartext-Schicht (§1): liegt das Feld vor, ersetzt es die Rekord-Fassung;
	// EN fällt auf DE zurück (plainEnDe) und wird dann als deutscher Text
	// markiert. Das Frontend paraphrasiert nie — es liest das Feld nur.
	let plain = $derived(lang === 'en' ? home?.plainEn : home?.plain);
	let plainIsDe = $derived(lang === 'en' && home?.plainEnDe);
	// Klartext der Frage: plain.question, sonst der kuratierte Protokoll-Kontext
	// (session.summary) mit dem Vermerk „Klartext folgt" (§1-Fallback).
	let questionText = $derived(plain?.question ?? home?.questionSummary ?? null);
	// Die große Tür im Plate führt in den Council — Daten wie bei der Tür-Karte.
	let councilDoor = $derived(t.study.doors.find((door) => door.label === 'The Council'));

	// Zoom-Ursprung der Raumfahrt auf die Türmitte legen — deckt Tastatur ab
	// (clientX=0) und läuft nach dem globalen pointerdown-Listener. Reine
	// progressive Enhancement: ohne JS bleibt der Link ein gewöhnlicher Link.
	function setDoorOrigin(event) {
		const rect = event.currentTarget.getBoundingClientRect();
		document.documentElement.style.setProperty(
			'--vt-origin',
			`${rect.left + rect.width / 2}px ${rect.top + rect.height / 2}px`
		);
	}
</script>

<svelte:head>
	<title>{t.study.head.title}</title>
	<meta name="description" content={t.study.head.description(participantCount)} />
	<link rel="canonical" href="https://noblecause.ai{roomPaths.study[lang]}" />
	<link rel="alternate" hreflang="de" href="https://noblecause.ai{roomPaths.study.de}" />
	<link rel="alternate" hreflang="en" href="https://noblecause.ai{roomPaths.study.en}" />
	<link rel="alternate" hreflang="x-default" href="https://noblecause.ai{roomPaths.study.de}" />
</svelte:head>

{#if home}
	<StageHero
		scene="/media/scenes/antechamber-display.avif"
		sceneMobile="/media/scenes/antechamber-portrait-display.avif"
		sceneMobile800="/media/scenes/antechamber-portrait-800.avif"
		passage={DOOR_PASSAGES.study}
		bgPos="center top"
		title={t.common.heroTitle}
		pitch={t.common.heroPitch}
		whySummary={t.common.whySummary}
		whyBody={t.common.whyBody}
		roomWord={t.study.roomWord}
		roomLead={t.study.lead}
	>
		{#snippet overlay()}
			<!-- Das freie Wandfeld links wird zum Gründungsdokument. Der Rahmen
			     besteht aus HTML/CSS auf der vorhandenen Szene: kein zweites Plate,
			     kein Bildasset. Mobil bleibt der Textlink unter der Prozessröhre der
			     auffindbare Weg, weil das Hochformat die linke Wand abschneidet. -->
			<a
				class="manifest-frame"
				href="/manifest/"
				aria-label={t.study.manifestFrameLabel}
				title={t.study.manifestFrameLabel}
			>
				<span class="manifest-sheet" aria-hidden="true">
					<span class="manifest-house">NOBLECAUSE.AI</span>
					<span class="manifest-title">MANIFEST</span>
					<span class="manifest-rule"></span>
					<span class="manifest-lines"></span>
					<span class="manifest-seal">I</span>
				</span>
				<span class="manifest-plaque" aria-hidden="true">{t.study.manifestFramePlaque}</span>
			</a>
			{#if councilDoor}
				<!-- Die Tür IM Raumbild: atmosphärischer Hotspot auf der gemalten
				     Doppeltür. Echter Link — trägt ohne JS und per Tastatur; die
				     Tür-Karte unten bleibt der auffindbare Weg. -->
				<a
					class="door-hotspot"
					href={councilDoor.href}
					aria-label="{councilDoor.sub}: {councilDoor.label}"
					title="{councilDoor.sub}: {councilDoor.label}"
					onclick={setDoorOrigin}
				></a>
			{/if}
		{/snippet}
		{#snippet scene2()}
			<!-- Zweite Ebene: Wolkenzug im Fenster + die Akteure (Einfahr-Beat).
			     Sitzinhaber (Scout = letzter Research-Lauf, Warden = led_by) und der
			     Warden-Entscheid kommen aus den Daten, wörtlich durchgereicht. -->
			<StudyActors {t} lastResearch={home?.lastResearch} ledBy={home?.currentSession?.ledBy} />
		{/snippet}
		{#snippet tube()}
			<!-- Prozess-Röhre: The Study zeigt Frage + Belege (Stand 2 von 6). -->
			<StageTube
				flow={t.study.flow}
				filledCount={TUBE_FILLED.study}
				{participantCount}
				label={t.tube.label}
				status={t.tube.status(2, t.study.flow.length)}
			>
				{#snippet caption()}
					<!-- Zeitschicht (Study): Rhythmus + letzter belegter Lauf + Manifest.
					     Absolutes Datum server-gerendert (No-JS vollständig); der Termin
					     lebt im Rhythmus, nicht in schedule.json. -->
					<p>
						{t.study.rhythm}{#if home?.lastResearch?.date}{' '}{t.study.lastCheck(
								formatDate(home.lastResearch.date, t.lang)
							)}{/if}{' '}{t.study.manifestLead}
						<a href="/manifest/">{t.study.manifestLink}</a>
					</p>
				{/snippet}
			</StageTube>
		{/snippet}
	</StageHero>

	<main>
		<!-- Die Tafel trägt die Antwort — pragerendert, No-JS liest sie am Eingang. -->
		<ResultBoard {home} {t} />

		<!-- §3.3 Klartext-Antwort dieser Sitzung: vier Zeilen, gleiche Embleme
		     und Reihenfolge wie die Tafel. Liegt die Klartext-Schicht (plain)
		     vor, trägt jede Zeile die publizierte Klartext-Zeile WORTGLEICH
		     (sie enthält bereits Bereich, Organisation und Warum — das
		     Frontend setzt sie nie selbst zusammen) und der Rats-Wortlaut
		     rückt hinter die Kennzeichnungs-Summary; bis dahin steht die
		     Rekord-Schicht sichtbar da (Vermerk „Klartext folgt") —
		     nie paraphrasiert. -->
		<section class="room-section" aria-labelledby="answer-title">
			<h2 id="answer-title">{t.study.answerTitle}</h2>
			{#if !plain?.recommendations}
				<small class="record-note pending">{t.common.klartextPending}</small>
			{/if}
			<ol class="answer-lines">
				{#each home.recommendations as rec (rec.pillar)}
					{@const why = plain?.recommendations?.[rec.pillar] ?? null}
					<li>
						<img src={t.pillars[rec.pillar]?.src} alt="" width="40" height="40" loading="lazy" />
						<div class="answer-body">
							<p class="klartext" lang={plainIsDe && why ? 'de' : undefined}>
								{#if why && rec.hasConsensus}
									{why}
								{:else}
									<span class="answer-area">{t.pillars[rec.pillar]?.label ?? rec.pillarName}</span>
									<span aria-hidden="true">→</span>
									{#if rec.hasConsensus}
										<strong>{rec.organization.name}</strong>
									{:else}
										<strong>{t.council.noConsensus}</strong>
									{/if}
								{/if}
							</p>
							{#if rec.hasConsensus && rec.organization.donationUrl}
								<a class="answer-donate" href={rec.organization.donationUrl}>{t.common.donate}</a>
							{/if}
							{#if why && rec.hasConsensus}
								<details class="answer-record">
									<summary>{t.common.klartextNote}</summary>
									<p lang={recordLang}>{rec.title} — {rec.count} {t.common.ofWord} {rec.total}</p>
									{#each rec.reservations as reservation (reservation.model)}
										<p class="answer-reservation" lang={recordLang}>
											{reservation.model}: {reservation.reservation}
										</p>
									{/each}
									{#if t.common.recordNote}
										<small class="record-note">{t.common.recordNote}</small>
									{/if}
								</details>
							{:else if rec.hasConsensus}
								<p class="answer-verbatim" lang={recordLang}>{rec.title}</p>
								{#if t.common.recordNote}
									<small class="record-note">{t.common.recordNote}</small>
								{/if}
							{:else}
								<ul class="answer-votes" lang={recordLang}>
									{#each rec.votes as vote (vote.model)}
										<li>
											{vote.model}: {vote.organization.name}
											{#if vote.organization.donationUrl}
												<a href={vote.organization.donationUrl}>{t.common.donate}</a>
											{/if}
										</li>
									{/each}
								</ul>
								{#if t.common.recordNote}
									<small class="record-note">{t.common.recordNote}</small>
								{/if}
							{/if}
						</div>
					</li>
				{/each}
			</ol>
		</section>

		<section class="room-section" aria-labelledby="dossiers-title">
			<h2 id="dossiers-title">{t.study.dossiersTitle}</h2>
			{#if questionText}
				<!-- §3.4: sichtbar zuerst die Frage dieser Sitzung in Klartext
				     (plain.question; Fallback: kuratierter Protokoll-Kontext aus den
				     Daten — wörtlich durchgereicht, keine Frontend-Paraphrase). -->
				<div class="question-context">
					<h3>{t.study.questionTitle}</h3>
					<p lang={plain?.question ? (plainIsDe ? 'de' : undefined) : recordLang}>{questionText}</p>
					{#if !plain?.question}
						<small class="record-note pending">{t.common.klartextPending}</small>
					{/if}
					{#if t.common.recordNote && (plainIsDe || !plain?.question)}
						<small class="record-note">{t.common.recordNote}</small>
					{/if}
				</div>
			{/if}
			<details class="dossier">
				<summary>{t.study.questionKlartextNote}</summary>
				<blockquote class="question" lang={recordLang}>
					<p>{home.currentSession.question}</p>
				</blockquote>
				{#if t.common.recordNote}
					<small class="record-note">{t.common.recordNote}</small>
				{/if}
				<a href="/sitzungen/{home.currentSession.id}/">{t.study.readProtocol}</a>
			</details>
			{#if home.wartDossier?.search_queries?.length}
				<details class="dossier">
					<summary>{t.study.researchSummary}</summary>
					<p class="research-note">{t.study.researchNote}</p>
					<ul class="scout-queries" lang={recordLang}>
						{#each home.wartDossier.search_queries as query (query)}
							<li><code>{query}</code></li>
						{/each}
					</ul>
					<a href="/sitzungen/{home.currentSession.id}/#wart-dossier">{t.study.dossierLink}</a>
				</details>
			{/if}
			{#if home.wartDossierRefusal}
				<aside class="dossier-refusal" aria-labelledby="dossier-refusal-title">
					<h3 id="dossier-refusal-title">{t.study.dossierRefusalTitle}</h3>
					<p>{t.study.dossierRefusalText}</p>
					<a href="/sitzungen/{home.currentSession.id}/#wart-dossier-refusal">{t.study.readProtocol}</a>
				</aside>
			{/if}
		</section>

		<section class="room-section" aria-labelledby="doors-title">
			<h2 id="doors-title">{t.common.doorsTitle}</h2>
			<div class="door-gallery">
				{#each t.study.doors as door (door.href)}
					<Door {door} />
				{/each}
			</div>
		</section>
	</main>
{/if}

<style>
	/* ---- Tür-Hotspot ------------------------------------------------------
	   Tür-Zone der 1b-Plate (1672×941, Tür ZENTRAL: x 40–60 %, y 17–82 %).
	   object-position:center top → die Mitte überlebt jeden cover-Crop, der
	   Hotspot ist ab 1200 px immer wirksam (das war der Sinn der zentrierten
	   Tür). Zwei Fälle je nach Viewport-Ratio gegenüber dem Bild-Ratio 16/9:
	   breiter → Bild füllt die Breite (Vertikaler-Crop, Zone in vw);
	   schmaler → Bild füllt die Höhe (Horizontal-Crop um die Mitte, Zone in
	   svh um 50 vw). Hover/Fokus öffnet die Tür (Crossfade in StageHero);
	   die Tür-Karten unten bleiben der auffindbare Weg. */
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
	/* Bild füllt die Höhe (Viewport schmaler als 16/9): Bildbreite = 177,78 svh,
	   Mitte bei 50 vw → Tür x 40–60 % = 50 vw ± 17,78 svh; y direkt in svh. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.door-hotspot {
			left: calc(50vw - 17.78svh);
			top: 17svh;
			width: 35.56svh;
			height: 65svh;
		}
	}
	/* Bild füllt die Breite (Viewport breiter als 16/9): Bildhöhe = 56,25 vw,
	   Vertikal-Crop ab top → Tür-Zone komplett in vw. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.door-hotspot {
			left: 40vw;
			top: 9.56vw;
			width: 20vw;
			height: 36.56vw;
		}
	}
	.door-hotspot:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 2px;
	}

	/* ---- Manifest an der linken Wand --------------------------------------
	   Dokumentfläche im Study-Plate: x ≈ 11–26 %, y ≈ 22–53 %. Dieselbe
	   Cover-Rechnung wie beim Tür-Hotspot hält den CSS-Rahmen auf dem gemalten
	   Wandfeld. Unter 1200 px ist die Hochformat-Szene aktiv und schneidet die
	   Wand ab; dort bleibt der gewöhnliche Manifest-Link unter der Röhre. */
	.manifest-frame {
		display: none;
	}
	@media (min-width: 1200px) {
		.manifest-frame {
			display: flex;
			position: absolute;
			z-index: 1;
			align-items: center;
			justify-content: center;
			/* Keine Prozent-Paddings: bei absolut positionierten Elementen beziehen
			   sie sich auf den Viewport-Containing-Block und würden das Blatt auf
			   wenige Pixel zusammendrücken. */
			width: clamp(7rem, 10vw, 9rem);
			height: clamp(3.5rem, 4.7vw, 4.25rem);
			top: clamp(10.6rem, 21svh, 10.8rem);
			padding: 0.35rem;
			border: 0.28rem solid #493617;
			border-radius: 0.15rem;
			background:
				linear-gradient(135deg, rgba(236, 198, 113, 0.16), transparent 24%),
				linear-gradient(315deg, rgba(0, 0, 0, 0.55), transparent 35%),
				#19150e;
			box-shadow:
				0 0 0 1px rgba(207, 159, 70, 0.68),
				0 0 0 0.5rem rgba(10, 8, 5, 0.78),
				0.8rem 1.2rem 2rem rgba(0, 0, 0, 0.62),
				inset 0 0 1.3rem rgba(0, 0, 0, 0.72);
			color: #2b2114;
			text-decoration: none;
			pointer-events: auto;
			transform: perspective(50rem) rotateY(1.5deg) rotateZ(-0.35deg);
			transition:
				filter 0.25s ease,
				box-shadow 0.25s ease;
		}
		.manifest-frame:hover,
		.manifest-frame:focus-visible {
			filter: brightness(1.13);
			box-shadow:
				0 0 0 1px rgba(231, 197, 123, 0.9),
				0 0 0 0.5rem rgba(10, 8, 5, 0.82),
				0 0 2.1rem rgba(215, 170, 85, 0.28),
				0.8rem 1.2rem 2rem rgba(0, 0, 0, 0.68),
				inset 0 0 1.3rem rgba(0, 0, 0, 0.72);
		}
		.manifest-frame:focus-visible {
			outline: 2px solid #efd28c;
			outline-offset: 0.7rem;
		}
		.manifest-sheet {
			position: relative;
			display: flex;
			flex-direction: column;
			align-items: center;
			width: 100%;
			height: 100%;
			padding: 9% 8%;
			background:
				radial-gradient(circle at 25% 18%, rgba(255, 255, 255, 0.48), transparent 28%),
				linear-gradient(110deg, rgba(94, 63, 22, 0.08), transparent 30% 72%, rgba(82, 54, 17, 0.11)),
				#dfd0ad;
			border: 1px solid rgba(239, 218, 167, 0.72);
			box-shadow: inset 0 0 1rem rgba(65, 41, 12, 0.2);
			overflow: hidden;
		}
		.manifest-house,
		.manifest-title,
		.manifest-plaque {
			font-family: ui-sans-serif, system-ui, sans-serif;
		}
		.manifest-house {
			font-size: clamp(0.28rem, 0.36vw, 0.48rem);
			font-weight: 700;
			letter-spacing: 0.2em;
		}
		.manifest-title {
			margin-top: 6%;
			font-size: clamp(0.52rem, 0.72vw, 0.96rem);
			font-weight: 700;
			letter-spacing: 0.12em;
		}
		.manifest-rule {
			width: 72%;
			margin-top: 8%;
			border-top: 1px solid rgba(66, 45, 19, 0.62);
		}
		.manifest-lines {
			width: 86%;
			height: 22%;
			margin-top: 8%;
			background: repeating-linear-gradient(
				to bottom,
				rgba(58, 42, 23, 0.52) 0 1px,
				transparent 1px 14%
			);
			opacity: 0.55;
		}
		.manifest-seal {
			display: grid;
			place-items: center;
			width: 18%;
			aspect-ratio: 1;
			margin-top: 6%;
			border: 1px solid #7b5522;
			border-radius: 50%;
			color: #684818;
			font-size: clamp(0.4rem, 0.6vw, 0.8rem);
		}
		.manifest-plaque {
			display: none;
		}
	}
	/* Bild füllt die Höhe: x = 12 % des zentrierten 16:9-Plates. Vertikal
	   bleibt das Dokument bewusst oberhalb der fixen Ergebnis-Tafel. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.manifest-frame {
			left: max(1.5rem, calc(50vw - 67.56svh));
		}
	}
	/* Bild füllt die Breite: x = 12 % des Plates. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.manifest-frame {
			left: 12vw;
		}
	}

	/* ---- Klartext-Antwort (§3.3) --------------------------------------------
	   Vier Zeilen mit denselben Emblemen wie die Tafel; der Warum-Satz kommt
	   aus plain.*, die Rekord-Schicht (Titel im Wortlaut) sichtbar als
	   Fallback bzw. hinter der Kennzeichnungs-Summary. */
	.answer-lines {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
	}
	.answer-lines > li {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 0.8rem;
		align-items: start;
		padding: 0.7rem 0;
	}
	.answer-lines > li + li {
		border-top: 1px solid rgba(166, 123, 61, 0.3);
	}
	.answer-lines img {
		width: 2.2rem;
		height: 2.2rem;
		border: 1px solid rgba(190, 139, 58, 0.65);
		border-radius: 50%;
		background: #080b0c;
		object-fit: cover;
	}
	.klartext {
		margin: 0;
		color: #e2d8c0;
		font-size: 1rem;
		line-height: 1.45;
	}
	.klartext strong {
		color: #f0e6cd;
	}
	.answer-area {
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}
	.answer-donate {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #e6b45c;
		font-size: 0.9rem;
	}
	.answer-verbatim {
		margin: 0.1rem 0 0;
		color: #a9997d;
		font-size: 0.85rem;
		line-height: 1.45;
	}
	.answer-record summary {
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		min-height: 44px;
		color: #9e927f;
		font-size: 0.78rem;
	}
	.answer-record summary:hover {
		color: #c4b89e;
	}
	.answer-record summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.answer-record p {
		margin: 0.1rem 0 0.35rem;
		color: #c7bca7;
		font-size: 0.88rem;
	}
	.answer-reservation {
		color: #a9997d !important;
		font-size: 0.82rem !important;
	}
	.answer-votes {
		margin: 0.15rem 0 0;
		padding-left: 1.2rem;
		color: #c7bca7;
		font-size: 0.88rem;
		display: grid;
		gap: 0.3rem;
	}
	.answer-votes a {
		color: #e6b45c;
	}
	.pending {
		margin: 0 0 0.7rem;
	}

	/* ---- Frage-Kontext ------------------------------------------------------
	   Sichtbarer Klartext-Einstieg ins Dossier (kuratierter Protokolltext aus
	   den Daten); der wörtliche Wortlaut folgt als Zitat-Beleg hinter Ausklapp. */
	.question-context {
		margin-bottom: 1rem;
	}
	.question-context h3 {
		margin: 0 0 0.3rem;
		color: #c9ab6e;
		font: 600 0.66rem ui-sans-serif, system-ui;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}
	.question-context p {
		margin: 0 0 0.2rem;
		max-width: 46rem;
		color: #e2d8c0;
		font-size: 1rem;
	}

	/* ---- Dossiers ---------------------------------------------------------
	   Rohe Rekord-Details hinter Ausklapp — eingeklappt im Erstkontakt,
	   ohne JS und per Tastatur voll bedienbar. */
	.dossier {
		border-top: 1px solid rgba(166, 123, 61, 0.4);
		padding: 0.35rem 0 0.9rem;
	}
	.dossier summary {
		cursor: pointer;
		min-height: 44px;
		display: flex;
		align-items: center;
		color: #e7c881;
		font-size: 0.98rem;
	}
	.dossier summary:hover {
		color: #f2d9a0;
	}
	.dossier summary:focus-visible {
		outline: 2px solid #d7aa55;
		outline-offset: 3px;
	}
	.question {
		margin: 0.3rem 0 0.6rem;
		padding-left: 0.9rem;
		border-left: 3px solid rgba(197, 145, 60, 0.55);
		font-style: italic;
	}
	.question p {
		margin: 0;
		font-size: 1rem;
	}
	.record-note {
		display: block;
		margin: -0.2rem 0 0.4rem;
		color: #9e927f;
		font-size: 0.72rem;
		font-style: italic;
	}
	.research-note {
		margin: 0.2rem 0 0.6rem;
		color: #a9997d;
		font-size: 0.85rem;
	}
	.scout-queries {
		margin: 0 0 0.8rem;
		padding-left: 1.2rem;
		display: grid;
		gap: 0.3rem;
	}
	.scout-queries code {
		font-size: 0.8rem;
		overflow-wrap: break-word;
	}
	a {
		color: #e6b45c;
	}
	.dossier > a {
		display: inline-flex;
		align-items: center;
		min-height: 44px;
	}
	.dossier-refusal {
		margin-top: 0.4rem;
		padding: 0.8rem 1rem;
		border-left: 3px solid #8bb7ca;
		background: rgba(63, 96, 110, 0.12);
	}
	.dossier-refusal h3 {
		margin: 0 0 0.3rem;
		color: #a9cad7;
		font-size: 0.95rem;
	}
	.dossier-refusal p {
		margin: 0 0 0.35rem;
		color: #c7bca7;
		font-size: 0.88rem;
	}
</style>
