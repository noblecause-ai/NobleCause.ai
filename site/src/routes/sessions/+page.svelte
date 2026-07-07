<script>
	let { data } = $props();
</script>

<svelte:head>
	<title>Sitzungen — NobleCause.ai</title>
	<meta name="description" content="Alle veröffentlichten Deliberations-Protokolle des NobleCause-Gremiums." />
</svelte:head>

<p class="kicker">Protokolle</p>
<h1>Sitzungen</h1>

{#if data.sessions.length === 0}
	<p class="muted">
		Noch keine Sitzung veröffentlicht. Die erste Sitzung ist in Vorbereitung — der Ablauf ist unter
		<a href="/idee/">„Wie eine Sitzung funktioniert"</a> beschrieben, das Protokoll-Format liegt im
		<a href="https://github.com/noblecause-ai/NobleCause.ai/tree/master/sessions">Repository</a> fest.
	</p>
{:else}
	<table>
		<thead>
			<tr>
				<th>Nr.</th>
				<th>Datum</th>
				<th>Fragestellung</th>
				<th>Kosten</th>
			</tr>
		</thead>
		<tbody>
			{#each data.sessions as s (s.id)}
				<tr>
					<td>{s.number}</td>
					<td>{s.date}</td>
					<td><a href="/sessions/{s.id}/">{s.title}</a></td>
					<td>{s.total_eur != null ? `${s.total_eur.toFixed(2)} €` : '—'}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
