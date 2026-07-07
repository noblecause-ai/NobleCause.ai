<script>
	let { children } = $props();
</script>

<div class="page">
	<header>
		<a class="brand" href="/">NobleCause.ai</a>
		<nav>
			<a href="/manifest/">Manifest</a>
			<a href="/idee/">Wie eine Sitzung funktioniert</a>
			<a href="/sessions/">Sitzungen</a>
		</nav>
	</header>

	<main>
		{@render children()}
	</main>

	<footer>
		<p>
			Alle Deliberationen werden vollständig veröffentlicht — Prompts, Rohantworten und Kosten.
			Durch dieses System fließt kein Geld.
		</p>
		<p class="fine">
			Inhalte <a href="https://creativecommons.org/licenses/by/4.0/deed.de">CC BY 4.0</a> ·
			Code <a href="https://github.com/noblecause-ai/NobleCause.ai">MIT, quelloffen</a> ·
			<a href="/impressum/">Impressum</a> ·
			ein Projekt von <a href="https://aion-lumen.ch">Aion Lumen</a>
		</p>
	</footer>
</div>

<style>
	:global(html) {
		background: #f4f1ea;
		color: #1a1916;
		font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
		line-height: 1.65;
		font-size: 17px;
	}
	:global(body) {
		margin: 0;
	}
	:global(h1, h2, h3) {
		font-weight: 600;
		letter-spacing: -0.01em;
		line-height: 1.25;
	}
	:global(h1) {
		font-size: 1.9rem;
		margin: 0 0 0.4rem;
	}
	:global(h2) {
		font-size: 1.25rem;
		margin: 2.2rem 0 0.6rem;
		padding-top: 1.2rem;
		border-top: 1px solid #d8d2c4;
	}
	:global(a) {
		color: #1a1916;
		text-decoration-color: #b0a892;
		text-underline-offset: 2px;
	}
	:global(a:hover) {
		text-decoration-color: #1a1916;
	}
	:global(hr) {
		border: 0;
		border-top: 1px solid #d8d2c4;
		margin: 2rem 0;
	}
	:global(table) {
		border-collapse: collapse;
		width: 100%;
		font-size: 0.92em;
	}
	:global(th, td) {
		text-align: left;
		padding: 0.45rem 0.7rem 0.45rem 0;
		border-bottom: 1px solid #e2ddd1;
		vertical-align: top;
	}
	:global(th) {
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #6f695c;
		font-weight: 600;
	}
	:global(code) {
		font-family: ui-monospace, 'SF Mono', Menlo, monospace;
		font-size: 0.85em;
		background: #ebe6da;
		padding: 0.08em 0.35em;
		border-radius: 3px;
	}
	:global(blockquote) {
		margin: 1rem 0;
		padding: 0.2rem 0 0.2rem 1rem;
		border-left: 3px solid #b0a892;
		color: #45413a;
	}
	:global(.muted) {
		color: #6f695c;
	}
	:global(.kicker) {
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 0.09em;
		color: #6f695c;
		margin: 0 0 0.6rem;
	}

	.page {
		max-width: 44rem;
		margin: 0 auto;
		padding: 0 1.2rem;
	}
	header {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem 1.4rem;
		align-items: baseline;
		padding: 1.6rem 0 1rem;
		border-bottom: 2px solid #1a1916;
		margin-bottom: 2.2rem;
	}
	.brand {
		font-weight: 700;
		font-size: 1.05rem;
		text-decoration: none;
		margin-right: auto;
	}
	nav {
		display: flex;
		gap: 1.1rem;
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.82rem;
	}
	nav a {
		text-decoration: none;
		color: #45413a;
	}
	nav a:hover {
		text-decoration: underline;
	}
	main {
		min-height: 55vh;
	}
	footer {
		margin-top: 3.5rem;
		padding: 1.2rem 0 2.5rem;
		border-top: 2px solid #1a1916;
		font-size: 0.85rem;
		color: #45413a;
	}
	.fine {
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.75rem;
		color: #6f695c;
	}
</style>
