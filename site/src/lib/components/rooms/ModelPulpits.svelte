<script>
	// Die Pulte: Erst- und Schlussvotum je Bereich, aus den strukturierten Voten
	// (registry-aufgelöst) — geänderte Empfehlungen sind markiert. Anzahl der Pulte
	// = Anzahl der Teilnehmer in den Daten, nichts ist hartkodiert.
	// Texte kommen als t-Prop (Locale); Bereichsnamen sprachabhängig aus t.pillars.
	let { tracks, sessionId, t } = $props();

	// Zelle als ein Ausdruck, damit SSR „Erst <Name>" zusammenhängend ausgibt.
	const cell = (prefix, vote) => `${prefix} ${vote?.organization.name ?? t.council.noVote}`;
</script>

<div class="pulpits">
	{#each tracks as track (track.model)}
		<section class="pulpit" aria-label={track.label}>
			<header>
				<span>{track.family}</span>
				<h3>{track.label}</h3>
			</header>
			<table>
				<tbody>
					{#each track.rows as row (row.pillar)}
						<tr class:changed={row.changed}>
							<th scope="row">{t.pillars[row.pillar]?.label ?? row.pillarName}</th>
							<td>{cell(t.council.initial, row.initial)}</td>
							<td>{cell(t.council.final, row.final)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<a href="/sitzungen/{sessionId}/#vollprotokoll">{t.council.readVotes}</a>
		</section>
	{/each}
</div>

<style>
	.pulpits {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(min(17rem, 100%), 1fr));
		gap: 1rem;
	}
	.pulpit {
		display: grid;
		gap: 0.6rem;
		align-content: start;
		padding: 1rem 1.1rem;
		background: rgba(13, 18, 19, 0.94);
		border: 1px solid rgba(166, 123, 61, 0.5);
	}
	header {
		text-align: center;
	}
	header span {
		display: block;
		color: #c89b4e;
		font: 600 0.6rem ui-sans-serif, system-ui;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}
	h3 {
		margin: 0.15rem 0 0;
		color: #ead8ae;
		font-size: 1rem;
	}
	table {
		font-size: 0.78rem;
	}
	th,
	td {
		padding: 0.35rem 0.4rem 0.35rem 0;
		border-bottom: 1px solid rgba(71, 56, 32, 0.7);
	}
	th {
		color: #a9997d;
		font-weight: 600;
	}
	td {
		color: #c7bca7;
	}
	tr.changed td:last-child {
		color: #e0c07f;
	}
	/* Schmale Viewports: Erst/Schluss untereinander statt 3-Spalten-Mindestbreite. */
	@media (max-width: 560px) {
		table,
		tbody,
		tr,
		th,
		td {
			display: block;
			width: 100%;
		}
		tr {
			border-bottom: 1px solid rgba(71, 56, 32, 0.7);
			padding: 0.35rem 0;
		}
		th,
		td {
			border-bottom: 0;
			padding: 0.1rem 0;
		}
		td:last-child {
			padding-bottom: 0.3rem;
		}
	}
	a {
		justify-self: start;
		min-height: 44px;
		display: inline-flex;
		align-items: center;
		color: #ddb45e;
		font-size: 0.82rem;
	}
</style>
