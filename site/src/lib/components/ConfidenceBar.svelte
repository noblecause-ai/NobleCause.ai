<script>
	let { confidence = 0 } = $props();
	const pct = Math.round(confidence * 100);
	const barWidth = Math.round(confidence * 120);
</script>

<svg width="140" height="10" viewBox="0 0 140 10" role="img" aria-label="Konfidenz {pct} Prozent">
	<rect x="0" y="2" width="120" height="6" rx="3" fill="currentColor" opacity="0.15" />
	<rect x="0" y="2" width={barWidth} height="6" rx="3" fill="currentColor" />
	<text x="126" y="9" font-size="9" fill="currentColor">{pct}%</text>
</svg>
