<script>
	// The Archive (DE) — Inhalt in $lib/components/rooms/ArchiveRoom.svelte.
	import ArchiveRoom from '$lib/components/rooms/ArchiveRoom.svelte';

	let { data } = $props();
</script>

<ArchiveRoom home={data.home} lang="de" />
