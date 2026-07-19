<script>
	// The Study (DE) — Inhalt in $lib/components/rooms/StudyRoom.svelte.
	import StudyRoom from '$lib/components/rooms/StudyRoom.svelte';

	let { data } = $props();
</script>

<StudyRoom home={data.home} lang="de" />
