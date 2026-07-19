<script>
	// The Archive (EN) — gleiche Komponente wie die deutsche Schwester-Route (/archiv/).
	import ArchiveRoom from '$lib/components/rooms/ArchiveRoom.svelte';

	let { data } = $props();
</script>

<ArchiveRoom home={data.home} lang="en" />
