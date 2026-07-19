<script>
	// The Study (EN) — gleiche Komponente wie die deutsche Schwester-Route (/).
	import StudyRoom from '$lib/components/rooms/StudyRoom.svelte';

	let { data } = $props();
</script>

<StudyRoom home={data.home} lang="en" />
