<script>
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
	let { t } = $props();
</script>

<div class="council-machine" aria-hidden="true">
	<img class="cm-plate" src="/media/actors/council-machine.avif" alt="" decoding="async" />
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
</style>
