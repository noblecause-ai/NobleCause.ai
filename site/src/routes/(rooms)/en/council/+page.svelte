<script>
	// The Council (EN) — gleiche Komponente wie die deutsche Schwester-Route (/ratssaal/).
	import CouncilRoom from '$lib/components/rooms/CouncilRoom.svelte';

	let { data } = $props();
</script>

<CouncilRoom home={data.home} lang="en" orgEn={data.orgEn} />
