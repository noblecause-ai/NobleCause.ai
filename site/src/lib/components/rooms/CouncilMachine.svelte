<script>
	import { orbitRest, orbitStateAt } from '$lib/orbit.js';

	// The Council — die Zählmaschine als eigene Ebene (§1, Runde H).
	//
	// P10 (Maschine + rundes Podest, freigestellt) liegt DECKUNGSGLEICH über der
	// gemalten Maschine im hall-Plate und ersetzt sie optisch. Die gemalte bleibt
	// im Plate darunter als Rückfallebene (deckt die Silhouette an einer Kante
	// nicht ganz, tritt die gemalte durch — kein Loch).
	//
	// Register (am gerenderten AVIF gemessen, Plate 1672×941): das Asset ist
	// bereits in Plate-Koordinaten gebacken — Maschine skaliert (s≈0,378) und an
	// die Position der gemalten Maschine gesetzt (Trommelmitte ≈ (840,673),
	// Podest x[664,1011], Unterkante ≈867). Damit deckt eine Ebene mit
	// IDENTISCHER Cover-Geometrie zur Plate (fixed, inset:0, 100svh, cover,
	// center top) die gemalte Maschine ohne Nachrechnen — dieselbe Cover-Teilung
	// des Browsers trägt beide.
	//
	// Nur Desktop ≥1200 px: dort wird das Landscape-hall-Plate ausgeliefert
	// (StageHero <source media="(min-width:1200px)">), auf das dieses Asset
	// gebacken ist; das Portrait-Plate (mobil) hat eine andere Komposition und
	// zeigt die gemalte Maschine. Dieselbe Grenze wie Türhotspot/Ruhe-Stapel.
	//
	// Ab jetzt ist dies die ZWEITE Ebene, die §7 (Verdeckung der Medaillons) und
	// §8 (Zähl-Ruck) trägt — sie darf sich bewegen. §1 setzt nur die Ebene.
	//
	// §8 Hover-Kern: eine Maschinenzone (Drum, x≈42–58 %, y≈63,8–76 % des Plate,
	// Two-Case-svh/vw wie der Türhotspot) fängt den Hover; darin ein Aufwach-Licht
	// (screen-Blend-Glow über der Trommel wie die Pult-Lampe) und eine Plakette
	// mit der Aggregationsregel (schwebende Vignette, Grammatik der Pult-Plakette).
	// KEIN Klickziel (Protokoll-Explorer kommt später); der Hotspot ist reine
	// Hover-Fläche. Die Regel steht als echtes DOM (kein title) — ohne JS/mit
	// Tastatur lesbar; §0 trägt über reines CSS-:hover (kein Skript).
	//
	// §8 Zähl-Ruck: P11 (nur die Trommel, freigestellt) liegt deckungsgleich über
	// P10s Trommel. Die feste Trommel-Silhouette kommt als CSS-mask auf den
	// Container (steht), die Oberfläche darin rollt beim Hover vertikal um eine
	// Ringhöhe (Schlag ≈ 240 ms, leicht überschwingend, zurück in Ruhe). Was am
	// Ober-/Unterrand freigelegt wird, zeigt P10s identische Trommel darunter —
	// deshalb bleibt der Übergang unsichtbar, die Kanten stehen. State-Guard
	// (rucking): ein Hover ein Ruck; schnelles Hin und Her schaukelt nicht auf.
	// §0: unter reduced-motion/No-JS bleibt der Ruck aus (Plakette steht).
	//
	// §7 Medaillon-Orbit: drei Modell-Medaillons kreisen auf einer Billboard-
	// Ellipse (b≪a, Aufsicht leicht von oben) um die Maschinenmitte. Aus dem
	// Winkel folgt die Tiefe d=(sinθ+1)/2 → Skalierung, Helligkeit, Blur. Die
	// hintere Hälfte liegt UNTER P10, die vordere darüber — echte Verdeckung.
	// Trick statt z-index-Chirurgie: jedes Medaillon existiert ZWEIMAL — eine
	// „hinten"-Kopie (DOM vor cm-plate → unter P10) und eine „vorn"-Kopie (DOM
	// nach cm-drum → über P10); der rAF blendet je nach Tiefe die passende Kopie
	// ein. Umgeschaltet wird an den Ellipsen-Seiten (d=0,5), wo beide Kopien
	// deckungsgleich sind und nichts von P10 verdeckt wird → unsichtbar.
	// Position: CSS-Two-Case (svh/vw wie der Türhotspot) aus den Custom-Props
	// --mcos/--msin — im SSR gesetzt (§0: still an den Bahnpunkten ohne JS), vom
	// rAF je Frame aktualisiert. Eine rAF-Schleife (40–60 s/Umdrehung), pausiert
	// bei document.hidden und außerhalb des Viewports. Einflug nach dem Pult-
	// Takt, von unten mit leichtem Überschwingen. Modellname immer am Medaillon.
	let { t, tracks = [] } = $props();

	let rucking = $state(false);
	function ruck() {
		if (rucking) return;
		// reduced-motion respektieren (der Ruck ist Zugabe, kein Träger von Sinn).
		if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return;
		rucking = true;
	}

	// ---- §7 Orbit ----------------------------------------------------------
	// Bahnmathematik: reine Zeit-Funktion in $lib/orbit.js (unit-getestet). θ ist
	// ZEITBASIERT — jede Pause bleibt folgenlos, θ steht beim nächsten Frame
	// wieder korrekt zur echten Zeit.
	const TAU = Math.PI * 2;
	const familyName = (track) => t.common?.familyNames?.[track.family] ?? track.family;
	// Modellbezeichnung + Version des aktuellen Sitzinhabers (Fallback: Kurz-Label).
	const modelName = (track) => t.common?.modelNames?.[track.model] ?? track.label;
	// Startwinkel 120° versetzt; θ0=90° setzt eins vorn-unten, zwei hinten.
	const medallions = $derived(
		tracks.map((track, i) => ({
			track,
			theta0: Math.PI / 2 + (i * TAU) / Math.max(tracks.length, 1)
		}))
	);
	// SSR-Ruhezustand je Kopie aus orbitRest (§0: ohne JS still an den Bahnpunkten).
	function restVars(theta0, copy) {
		const s = orbitRest(theta0);
		const vis = copy === 'rear' ? s.rearVisible : s.frontVisible;
		return (
			`--mcos:${s.cos.toFixed(4)};--msin:${s.sin.toFixed(4)};` +
			`--mscale:${s.scale.toFixed(3)};--mbright:${s.bright.toFixed(3)};` +
			`--mblur:${s.blur.toFixed(2)}px;--mfly:0svh;opacity:${vis ? 1 : 0};` +
			// nur die sichtbare Kopie fängt den Zeiger (Doppel-Render-Falle)
			`pointer-events:${vis ? 'auto' : 'none'};`
		);
	}
	function writeOne(el, s, vis) {
		const st = el.style;
		st.setProperty('--mcos', s.cos.toFixed(4));
		st.setProperty('--msin', s.sin.toFixed(4));
		st.setProperty('--mscale', s.scale.toFixed(3));
		st.setProperty('--mbright', s.bright.toFixed(3));
		st.setProperty('--mblur', s.blur.toFixed(2) + 'px');
		st.setProperty('--mfly', s.fly.toFixed(2) + 'svh');
		st.opacity = vis ? s.opacity.toFixed(2) : '0';
		// nur die sichtbare Kopie ist hoverbar — sonst fängt die verdeckte mit.
		st.pointerEvents = vis ? 'auto' : 'none';
	}

	let rearEls = $state([]);
	let frontEls = $state([]);

	$effect(() => {
		if (typeof window === 'undefined') return;
		// §0-Gate: nur Desktop, nur bei Bewegungswunsch. Sonst bleibt der SSR-
		// Ruhezustand stehen (still an den Bahnpunkten, keine rAF).
		if (!window.matchMedia('(min-width: 1200px)').matches) return;
		if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
		const rear = rearEls.filter(Boolean);
		const front = frontEls.filter(Boolean);
		if (rear.length !== medallions.length || front.length !== medallions.length) return;

		const t0 = performance.now();
		let raf = 0;
		// Die Schleife läuft IMMER und plant IMMER den nächsten Frame (erste Zeile).
		// „Pausiert" heißt nur: nichts rechnen/schreiben (früher return) — ein
		// rAF-Tick mit return kostet nichts. KEIN stop/start an Events
		// (scroll/visibility): so gibt es keinen Zustand ohne Rückweg (Lehre wie
		// bei passageActive). Weggescrollt → Leerlauf; sobald der Raum wieder oben
		// steht, rechnet der ohnehin geplante nächste Frame weiter — es braucht
		// kein Ereignis zum Wiederanlauf (scrollTo(0,0) feuert bei bereits 0 keins).
		// Verdeckt/hidden drosselt der Browser rAF selbst und nimmt es selbst
		// wieder auf. Abbruch NUR beim Unmount.
		const frame = (now) => {
			raf = requestAnimationFrame(frame);
			if (window.scrollY >= window.innerHeight * 1.1) return; // weggescrollt: Leerlauf
			const widen =
				1 + (parseFloat(getComputedStyle(rear[0]).getPropertyValue('--retreat')) || 0) * 0.5;
			const elapsed = now - t0;
			for (let i = 0; i < medallions.length; i++) {
				const s = orbitStateAt(elapsed, medallions[i].theta0, widen);
				writeOne(rear[i], s, s.rearVisible);
				writeOne(front[i], s, s.frontVisible);
			}
		};
		raf = requestAnimationFrame(frame);
		return () => cancelAnimationFrame(raf);
	});
</script>

<div class="council-machine">
	<!-- §7 Orbit, hintere Hälfte: DOM VOR cm-plate → liegt unter P10 (Verdeckung).
	     Jedes Medaillon hier UND in der vorderen Gruppe; der rAF zeigt je Tiefe
	     die passende Kopie. Ruhezustand (SSR) trägt §0. -->
	<div class="cm-orbit cm-orbit-rear" aria-hidden="true">
		{#each medallions as { track, theta0 }, i (track.model)}
			<div class="cm-medallion" bind:this={rearEls[i]} style={restVars(theta0, 'rear')}>
				<img class="cm-med-img" src="/media/medallions/{track.model}-lo.avif" alt="" width="256" height="256" decoding="async" />
				<span class="cm-med-plaque">
					<strong class="cm-med-name">{familyName(track)}</strong>
					<span class="cm-med-model">{modelName(track)}</span>
				</span>
			</div>
		{/each}
	</div>

	<img class="cm-plate" src="/media/actors/council-machine.avif" alt="" aria-hidden="true" decoding="async" />

	<!-- §8 Ruck-Ebene: die Trommel-Silhouette (P11-Alpha) als mask auf dem
	     Container — sie STEHT; die Oberfläche darin rollt beim Ruck. Über P10
	     (cm-plate), unter den Pulten. -->
	<div class="cm-drum" aria-hidden="true">
		<img
			class="cm-drum-surf"
			class:rucking
			src="/media/actors/council-drum.avif"
			alt=""
			decoding="async"
			onanimationend={() => (rucking = false)}
		/>
	</div>

	<!-- §7 Orbit, vordere Hälfte: DOM NACH cm-plate/cm-drum → liegt über P10. -->
	<div class="cm-orbit cm-orbit-front" aria-hidden="true">
		{#each medallions as { track, theta0 }, i (track.model)}
			<div class="cm-medallion" bind:this={frontEls[i]} style={restVars(theta0, 'front')}>
				<img class="cm-med-img" src="/media/medallions/{track.model}-lo.avif" alt="" width="256" height="256" decoding="async" />
				<span class="cm-med-plaque">
					<strong class="cm-med-name">{familyName(track)}</strong>
					<span class="cm-med-model">{modelName(track)}</span>
				</span>
			</div>
		{/each}
	</div>

	<!-- §8 Maschinenzone: Hotspot (Hover-Fläche, kein Ziel) + Aufwach-Licht +
	     Plakette. Reihenfolge im DOM: Hotspot zuerst, damit die Geschwister-
	     Selektoren (.cm-hotspot:hover ~ …) Licht und Plakette enthüllen.
	     onmouseenter löst den Ruck aus (Guard in ruck()). -->
	<div class="cm-zone">
		<div class="cm-hotspot" aria-hidden="true" onmouseenter={ruck}></div>
		<span class="cm-glow" aria-hidden="true"></span>
		<p class="cm-plaque">{t.council.actors.machine.rule}</p>
	</div>
</div>

<style>
	.council-machine {
		position: absolute;
		inset: 0;
		pointer-events: none;
		/* Nur Desktop ≥1200 px — dort liegt das Landscape-Plate, auf das P10
		   registriert ist (mobil: Portrait-Plate mit gemalter Maschine). */
		display: none;
	}
	@media (min-width: 1200px) {
		.council-machine {
			display: block;
		}
	}

	/* Deckungsgleich mit .room-bg img: fixed am Viewport, 100svh, cover, center
	   top. Das Asset ist in dieselbe 1672×941-Plate-Koordinaten gebacken wie
	   hall-display — identische Cover-Teilung legt P10 exakt über die gemalte
	   Maschine. z-index:0 (wie die Plate); später im DOM als scene2 → malt über
	   der Plate, unter der room-overlay-UI. */
	.cm-plate {
		position: fixed;
		inset: 0;
		z-index: 0;
		width: 100%;
		height: 100svh;
		object-fit: cover;
		object-position: center top;
	}

	/* ---- §8 Ruck-Ebene (P11) ----------------------------------------------
	   Der Container trägt die feste Trommel-Silhouette als CSS-mask (P11-Alpha,
	   cover/center-top wie die Plate → deckt P10s Trommel). Die Silhouette STEHT.
	   Darin rollt die Oberfläche (dasselbe Asset als <img>) beim Ruck vertikal.
	   z-index 0, im DOM nach cm-plate → über P10, unter den Pulten. */
	.cm-drum {
		position: fixed;
		inset: 0;
		z-index: 0;
		width: 100%;
		height: 100svh;
		pointer-events: none;
		overflow: hidden;
		-webkit-mask-image: url(/media/actors/council-drum.avif);
		mask-image: url(/media/actors/council-drum.avif);
		-webkit-mask-size: cover;
		mask-size: cover;
		-webkit-mask-position: center top;
		mask-position: center top;
		-webkit-mask-repeat: no-repeat;
		mask-repeat: no-repeat;
		mask-mode: alpha;
	}
	.cm-drum-surf {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100svh;
		object-fit: cover;
		object-position: center top;
		will-change: transform;
	}
	/* Der Ruck: einmal um eine Ringhöhe (--ring) hinab, leicht überschwingend,
	   zurück in Ruhe (translateY 0). Rückkehr auf 0 = keine Drift, bei Ruhe deckt
	   P11 P10 exakt; der freigelegte Rand während des Schlags zeigt P10 (identisch).
	   §0: nur unter no-preference. */
	@media (prefers-reduced-motion: no-preference) {
		.cm-drum-surf.rucking {
			animation: cm-ruck 240ms cubic-bezier(0.33, 0, 0.2, 1) both;
		}
	}
	@keyframes cm-ruck {
		0% {
			transform: translateY(0);
		}
		48% {
			transform: translateY(var(--ring, 1.7svh));
		}
		66% {
			transform: translateY(calc(var(--ring, 1.7svh) * 1.09));
		}
		100% {
			transform: translateY(0);
		}
	}

	/* ---- §8 Maschinenzone -------------------------------------------------
	   Fix am Viewport (wie die Plate) über der Trommel; Two-Case-Geometrie wie
	   der Türhotspot. Werte aus dem Register (Plate 1672×941): Trommel/Körper
	   x 42–58 %, y 63,8–76 %. Nur Desktop ≥1200 px (das ganze .council-machine
	   ist dort erst sichtbar). Container ohne Zeiger; nur der Hotspot fängt Hover. */
	/* z-index 3 hebt die Zone ÜBER die Lesepulte (die im DOM nach der Maschine
	   kommen und sonst mit dem Mittelpult den Hotspot verdecken). Trimm der
	   Oberkante auf y66 % hält sie knapp UNTER der Türhotspot-Unterkante (65,9 %),
	   damit der Zonen-Deckel nicht die Tür schluckt. */
	.cm-zone {
		position: fixed;
		pointer-events: none;
		z-index: 3;
	}
	.cm-hotspot {
		position: absolute;
		inset: 0;
		pointer-events: auto;
		/* Reine Hover-Fläche — kein Klickziel, kein Tab-Stopp (Explorer später). */
	}
	/* Bild füllt die Höhe (Viewport schmaler als 16:9): x in svh um 50 vw.
	   Zone x 42–58 %, y 66–78 % (Trommel + oberer Sockel). */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.cm-zone {
			left: calc(50vw - 14.22svh);
			top: 66svh;
			width: 28.44svh;
			height: 12svh;
		}
	}
	/* Bild füllt die Breite (Viewport breiter als 16:9): alles in vw ab top. */
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.cm-zone {
			left: 42vw;
			top: 37.13vw;
			width: 16vw;
			height: 6.75vw;
		}
	}

	/* ---- Aufwach-Licht -----------------------------------------------------
	   Warmes Radial-Glow über der Trommel (screen-Blend wie die Pult-Lampe),
	   auf Hover eingeblendet — die Maschine „erwacht". Trommelmitte ≈ 51 %/60 %
	   der Zone. Rein dekorativ. */
	.cm-glow {
		position: absolute;
		inset: -20% -8%;
		pointer-events: none;
		mix-blend-mode: screen;
		opacity: 0;
		transition: opacity 0.5s ease;
		background: radial-gradient(
			ellipse 46% 44% at 51% 60%,
			rgba(255, 202, 128, 0.55),
			rgba(255, 176, 92, 0.16) 52%,
			rgba(255, 176, 92, 0) 72%
		);
	}
	.cm-hotspot:hover ~ .cm-glow {
		opacity: 0.85;
	}

	/* ---- Plakette: die Aggregationsregel ----------------------------------
	   Schwebende Vignette über der Maschine (Grammatik der Pult-Plakette:
	   radial-gradient-Vignette statt Kasten, text-shadow gegen den Grund).
	   Prozessaussage, kein Ergebnis. Über der Zone verankert, nach oben gezogen. */
	.cm-plaque {
		position: absolute;
		left: 50%;
		top: 0;
		transform: translate(-50%, calc(-100% - 0.5rem));
		margin: 0;
		z-index: 1;
		width: max-content;
		max-width: 20rem;
		padding: 0.4rem 1.1rem 0.5rem;
		text-align: center;
		color: #ecdfc0;
		font-size: 0.86rem;
		line-height: 1.4;
		background: radial-gradient(ellipse 80% 96% at 50% 50%, rgba(3, 6, 7, 0.86), rgba(3, 6, 7, 0) 76%);
		text-shadow: 0 1px 8px rgba(3, 6, 7, 0.96);
		pointer-events: none;
		opacity: 0;
		transition: opacity 0.4s ease;
	}
	.cm-hotspot:hover ~ .cm-plaque {
		opacity: 1;
	}
	@media (prefers-reduced-motion: reduce) {
		.cm-glow,
		.cm-plaque {
			transition: none;
		}
	}

	/* ---- §7 Medaillon-Orbit -----------------------------------------------
	   Zwei Gruppen (rear/front) straddeln cm-plate im DOM → echte Verdeckung
	   ohne z-index-Chirurgie. Beide fix am Viewport, z-index 0 (unter der
	   room-overlay-UI z1). Die Medaillons darin absolut positioniert; Ort und
	   Tiefe kommen aus den Custom-Props (SSR-Ruhe, rAF je Frame). */
	.cm-orbit {
		position: fixed;
		inset: 0;
		z-index: 0;
		pointer-events: none;
	}
	.cm-medallion {
		position: absolute;
		aspect-ratio: 1;
		/* translate(-50%,-50%): der Ort (left/top) ist die Medaillon-MITTE.
		   translateY(--mfly): Einflug von unten. scale(--mscale): Tiefe. */
		transform: translate(-50%, -50%) translateY(var(--mfly, 0)) scale(var(--mscale, 1));
		filter: brightness(var(--mbright, 1)) blur(var(--mblur, 0px));
		will-change: transform, opacity, left, top;
	}
	.cm-med-img {
		display: block;
		width: 100%;
		height: 100%;
	}
	/* Plakette unter dem Bildnis (Pult-Grammatik, von den Pulten übernommen): der
	   Modellname steht IMMER (Schutz gegen „Nightingale empfiehlt"), Family + Rolle
	   erscheinen auf Hover, dazu eine schwebende Vignette (Schatten statt Kasten).
	   Die Plakette selbst fängt keinen Zeiger — das Medaillon-DIV trägt den Hover. */
	.cm-med-plaque {
		position: absolute;
		/* ÜBER dem Medaillon (statt darunter, wo die Prozess-Röhre sie verdeckte). */
		bottom: 100%;
		left: 50%;
		transform: translateX(-50%);
		margin: 0 0 0.24rem;
		padding: 0.18rem 0.84rem 0.34rem;
		width: max-content;
		max-width: 13rem;
		text-align: center;
		background: radial-gradient(ellipse 82% 94% at 50% 50%, rgba(3, 6, 7, 0), rgba(3, 6, 7, 0) 76%);
		transition: background 0.35s ease;
		pointer-events: none;
	}
	.cm-medallion:hover .cm-med-plaque {
		background: radial-gradient(ellipse 82% 94% at 50% 50%, rgba(3, 6, 7, 0.88), rgba(3, 6, 7, 0) 78%);
	}
	.cm-med-name {
		display: block;
		white-space: nowrap;
		color: #f0d899;
		font-size: 0.84rem;
		font-weight: 600;
		letter-spacing: 0.03em;
		text-shadow:
			0 1px 6px rgba(3, 6, 7, 0.96),
			0 0 3px rgba(3, 6, 7, 0.9);
	}
	/* Auf Hover: Modellbezeichnung + Version des aktuellen Sitzinhabers. */
	.cm-med-model {
		display: block;
		margin-top: 0.16rem;
		white-space: nowrap;
		opacity: 0;
		transition: opacity 0.35s ease;
		color: #c9ab6e;
		font-size: 0.74rem;
		letter-spacing: 0.01em;
		text-shadow: 0 1px 6px rgba(3, 6, 7, 0.95);
	}
	.cm-medallion:hover .cm-med-model {
		opacity: 1;
	}
	@media (prefers-reduced-motion: reduce) {
		.cm-med-plaque,
		.cm-med-model {
			transition: none;
		}
	}
	/* Position + Basisgröße: Two-Case wie der Türhotspot. Ellipsenmitte auf der
	   Maschinenmitte Plate x50,42 %, y72 % (≈ Trommelmitte); a=15 % (Breite),
	   b=7 % (Höhe, b≪a). So läuft die Rückseite (θ=270°, y65 %) HINTER die
	   Trommel (Verdeckung durch P10), die Vorderseite (y79 %) davor. */
	@media (min-width: 1200px) and (max-aspect-ratio: 16/9) {
		.cm-medallion {
			left: calc(50vw + (0.42 + 15 * var(--mcos, 0)) * 1.7778svh);
			top: calc((72 + 7 * var(--msin, 0)) * 1svh);
			width: 7.04svh;
		}
	}
	@media (min-width: 1200px) and (min-aspect-ratio: 16/9) {
		.cm-medallion {
			left: calc((50.42 + 15 * var(--mcos, 0)) * 1vw);
			top: calc((72 + 7 * var(--msin, 0)) * 0.5625vw);
			width: 3.96vw;
		}
	}
</style>
