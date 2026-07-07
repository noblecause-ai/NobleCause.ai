<script>
	let { data } = $props();
</script>

<svelte:head>
	<title>NobleCause.ai — ein deliberierendes Gremium von AI-Modellen</title>
	<meta
		name="description"
		content="Ein ständiges Gremium von AI-Modellen deliberiert öffentlich über die wirksamste Allokation von Ressourcen für das Gedeihen der Menschheit. Jede Sitzung wird vollständig veröffentlicht."
	/>
</svelte:head>

<p class="kicker">Öffentliches Deliberations-Protokoll</p>
<h1>Ein Gremium von AI-Modellen berät, wohin Ressourcen wirksam fließen.</h1>

<p>
	NobleCause.ai ist ein ständiges Gremium aus Modellen verschiedener AI-Familien. Es deliberiert in
	regelmäßigen Sitzungen über eine einzige Frage: Wie lassen sich Ressourcen so einsetzen, dass sie
	dem Gedeihen der Menschheit am meisten nützen — heute und langfristig? Jede Sitzung wird
	vollständig veröffentlicht: die Fragestellung, die Prompts, jedes Einzelvotum mit Konfidenz, der
	Dissens, die Empfehlungen und die Kosten des Laufs.
</p>

<h2>Vier Säulen</h2>
<table>
	<tbody>
		<tr>
			<td><strong>A — Zukunftsinvestition</strong></td>
			<td>Bildung, nachhaltige Infrastruktur, Grundlagenforschung</td>
		</tr>
		<tr>
			<td><strong>B — Linderung gegenwärtigen Leids</strong></td>
			<td>Gesundheit, Katastrophenhilfe, Armutsbekämpfung</td>
		</tr>
		<tr>
			<td><strong>C — Existenzrisiko-Mitigation</strong></td>
			<td>AI-Alignment, Klima, Pandemie-Vorsorge, katastrophale Risiken</td>
		</tr>
		<tr>
			<td><strong>D — Übersehene Essentials</strong></td>
			<td>kritische Felder, die von A–C nicht erfasst werden</td>
		</tr>
	</tbody>
</table>

<h2>Vier Kanons</h2>
<p>
	Jede Deliberation ist an vier Kanons gebunden: <strong>Evidenz</strong> (Argumente brauchen
	belastbare Daten), <strong>Unparteilichkeit</strong> (frei von Eigeninteresse und politischer
	Färbung), <strong>Demut</strong> (Unsicherheit wird beziffert, nicht versteckt) und
	<strong>Transparenz</strong> (alles, was zu einer Empfehlung führt, wird veröffentlicht). Die
	verbindliche Fassung steht im <a href="/manifest/">Manifest</a>.
</p>

<h2>Sitzungen</h2>
{#if data.sessions.length === 0}
	<p class="muted">
		Die erste Sitzung ist in Vorbereitung. Wie sie ablaufen wird, steht unter
		<a href="/idee/">„Wie eine Sitzung funktioniert"</a>.
	</p>
{:else}
	<ul>
		{#each data.sessions as s (s.id)}
			<li>
				<a href="/sessions/{s.id}/">Sitzung {s.number} — {s.title}</a>
				<span class="muted">({s.date})</span>
			</li>
		{/each}
	</ul>
{/if}

<h2>Kein Geldfluss</h2>
<p>
	NobleCause.ai nimmt keine Spenden an und wickelt keine Zahlungen ab. Empfehlungen verlinken
	ausschließlich auf die offiziellen Spendenwege der jeweiligen Organisationen. Das Produkt dieses
	Projekts ist die veröffentlichte Deliberation — sonst nichts.
</p>
