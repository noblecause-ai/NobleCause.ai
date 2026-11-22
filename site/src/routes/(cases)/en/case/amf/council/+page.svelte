<script>
	import AmfCase from '$lib/components/cases/AmfCase.svelte';
	let { data } = $props();
</script>

<AmfCase caseData={data.amf} room="council" lang="en" />
