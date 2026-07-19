<script>
	// The Council (DE) — Inhalt in $lib/components/rooms/CouncilRoom.svelte.
	import CouncilRoom from '$lib/components/rooms/CouncilRoom.svelte';

	let { data } = $props();
</script>

<CouncilRoom home={data.home} lang="de" orgEn={data.orgEn} />
