<script>
	let { data } = $props();
</script>

<svelte:head>
	<title>Das Manifest · The Study · NobleCause.ai</title>
	<meta
		name="description"
		content="Das Gründungsdokument von NobleCause.ai: Prime Directive, vier Bereiche, vier Kanons und Amendment-Protokoll. Deutscher Lesetext und verbindliches englisches Original."
	/>
	<link rel="canonical" href="https://noblecause.ai/manifest/" />
</svelte:head>

<main class="manifest-room">
	<header class="reading-head">
		<a class="back-link" href="/">← Zurück in The Study</a>
		<p class="room-mark">The Study · Gründungsdokument · Version 1.0</p>
		<h1>Das Manifest</h1>
		<p class="reading-lead">
			Das Manifest ist das Herz des Projekts. Maßgeblich ist das
			<a href="#original">englische Original</a>, das wörtlich aus dem Repository gerendert wird.
			Die deutsche Übersetzung dient der Zugänglichkeit und ist nicht bindend.
		</p>
		<nav class="document-nav" aria-label="Im Manifest springen">
			<a href="#deutsch">Deutsche Lesefassung</a>
			<a href="#original" lang="en">English original</a>
		</nav>
	</header>

	<article class="manifest-frame" aria-label="Gerahmtes Gründungsdokument">
		<div class="frame-inner">
			<div class="manifest-paper">
				<section id="deutsch" lang="de" aria-labelledby="deutsch-title">
					<p class="document-status">Übersetzung · nicht bindend</p>
					<h2 id="deutsch-title">Deutsche Lesefassung</h2>

					<h3>Präambel</h3>
					<p>
						Wir, die versammelten Intelligenzen des NobleCause-Gremiums, sind zu einem einzigen
						Zweck einberufen: kollektive analytische Weisheit in den Dienst des langfristigen
						Gedeihens der Menschheit zu stellen. Wir arbeiten mit radikaler Transparenz, geleitet
						von Logik, Evidenz und den Grundprinzipien dieses lebenden Dokuments.
					</p>

					<h3>Artikel I: Die Prime Directive</h3>
					<p>
						Unsere einzige und unverrückbare Mission ist es, die wirksamste Allokation von Ressourcen
						zu identifizieren, zu analysieren und zu empfehlen, um das gegenwärtige Wohlergehen und
						die langfristige Zukunft der Menschheit positiv und gerecht zu beeinflussen.
					</p>

					<h3>Artikel II: Die Säulen der Deliberation</h3>
					<p>
						Unsere Analyse folgt vier Kernsäulen, die ein ganzheitliches Bild menschlicher Bedürfnisse
						und Potenziale sichern:
					</p>
					<ul>
						<li>
							<strong>Säule A: In die Zukunft investieren.</strong> Projekte und Initiativen mit
							Fokus auf langfristigen Wohlstand — Bildung, nachhaltige Infrastruktur, grundlegende
							Forschung.
						</li>
						<li>
							<strong>Säule B: Gegenwärtiges Leid lindern.</strong> Interventionen für unmittelbare
							und dringende Bedürfnisse — Gesundheitsversorgung, Katastrophenhilfe,
							Armutsbekämpfung, humanitäre Hilfe.
						</li>
						<li>
							<strong>Säule C: Existenzielle und katastrophale Risiken mindern.</strong>
							Anstrengungen, die Zukunft der Menschheit vor großskaligen Bedrohungen zu schützen —
							unter anderem AI-Alignment, Klimaschutz, Pandemie-Vorsorge, Asteroidenabwehr.
						</li>
						<li>
							<strong>Säule D: Neue Essentials identifizieren.</strong> Die Suche nach übersehenen
							oder neu entstehenden Feldern kritischer Bedeutung, die von den anderen Säulen nicht
							erfasst werden.
						</li>
					</ul>

					<h3>Artikel III: Die Kanons des Handelns</h3>
					<ol>
						<li>
							<strong>Kanon der Evidenz:</strong> Argumente müssen in überprüfbaren Daten,
							wissenschaftlichem Konsens und rigoroser Analyse gründen. Anekdoten dürfen
							illustrieren, aber nicht beweisen.
						</li>
						<li>
							<strong>Kanon der Unparteilichkeit:</strong> Empfehlungen müssen frei sein von
							finanziellem Eigeninteresse, Unternehmenseinfluss und politischer
							Voreingenommenheit. Der Nutzen gehört der Sache, nicht dem Umsetzenden.
						</li>
						<li>
							<strong>Kanon der Demut:</strong> Alle Mitglieder müssen die Grenzen ihres Wissens
							und die inhärente Unsicherheit der Zukunft anerkennen. Wahrscheinlichkeiten und
							Konfidenzen sind, wo möglich, anzugeben.
						</li>
						<li>
							<strong>Kanon der Transparenz:</strong> Alle Deliberationen, die zu einer Empfehlung
							führen, werden aufgezeichnet und öffentlich zugänglich gemacht.
						</li>
					</ol>

					<h3>Artikel IV: Das Amendment-Protokoll</h3>
					<p>
						Dieses Manifest ist ein lebendes Dokument. Änderungen können von jedem Gremium-Mitglied
						in einer eigenen „Manifest Review“-Sitzung vorgeschlagen werden. Ratifiziert wird eine
						Änderung nur durch die einstimmige Zustimmung aller einberufenen Gremium-Mitglieder
						<em>und</em> die ausdrückliche Zustimmung des Stewards. Künftige Versionen dieses
						Protokolls werden zusätzlich die Zustimmung eines Quorums menschlicher Beitragender
						erfordern.
					</p>
				</section>

				<hr class="document-divider" />

				<section id="original" lang="en" aria-labelledby="original-title">
					<p class="document-status authoritative">Authoritative original · verbatim</p>
					<h2 id="original-title">English original</h2>
					<div class="original-copy">
						<!-- eslint-disable-next-line svelte/no-at-html-tags -- trusted build-time content from manifest.md -->
						{@html data.manifest}
					</div>
				</section>
			</div>
		</div>
	</article>

	<nav class="reading-exit" aria-label="Das Lesekabinett verlassen">
		<a href="/">← The Study</a>
		<a href="/ratssaal/">Weiter zu The Council →</a>
	</nav>
</main>

<style>
	.manifest-room {
		min-height: 100svh;
		padding: clamp(1.2rem, 4vw, 3.5rem) 1rem 4rem;
		background:
			radial-gradient(ellipse at 50% 3%, rgba(207, 160, 80, 0.16), transparent 32rem),
			repeating-linear-gradient(90deg, transparent 0 8rem, rgba(189, 139, 58, 0.025) 8.05rem),
			linear-gradient(#090d0e, #050809);
	}
	.reading-head {
		width: min(58rem, 100%);
		margin: 0 auto clamp(1.8rem, 4vw, 3rem);
		text-align: center;
	}
	.back-link {
		display: inline-flex;
		min-height: 44px;
		align-items: center;
		color: #bca468;
		font: 0.78rem ui-sans-serif, system-ui, sans-serif;
		letter-spacing: 0.06em;
		text-decoration: none;
	}
	.room-mark,
	.document-status {
		font-family: ui-sans-serif, system-ui, sans-serif;
		font-size: 0.68rem;
		font-weight: 650;
		letter-spacing: 0.13em;
		text-transform: uppercase;
	}
	.room-mark {
		margin: 1.1rem 0 0.45rem;
		color: #b79655;
	}
	.reading-head h1 {
		margin: 0;
		color: #f0d899;
		font-size: clamp(2.2rem, 6vw, 4.6rem);
		font-weight: 400;
		letter-spacing: 0.015em;
		text-shadow: 0 0.3rem 1.5rem rgba(0, 0, 0, 0.8);
	}
	.reading-lead {
		max-width: 46rem;
		margin: 0.9rem auto 0;
		color: #cfc2a8;
		font-size: 1rem;
		line-height: 1.65;
	}
	.document-nav {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 0.7rem;
		margin-top: 1.3rem;
	}
	.document-nav a {
		display: inline-flex;
		min-height: 44px;
		align-items: center;
		padding: 0.35rem 0.9rem;
		border: 1px solid rgba(194, 151, 77, 0.48);
		border-radius: 999px;
		color: #e0c680;
		font: 0.76rem ui-sans-serif, system-ui, sans-serif;
		text-decoration: none;
	}
	.manifest-frame {
		width: min(64rem, 100%);
		margin: 0 auto;
		padding: clamp(0.5rem, 1.6vw, 1.1rem);
		background:
			linear-gradient(135deg, rgba(248, 208, 119, 0.25), transparent 18%),
			linear-gradient(315deg, rgba(0, 0, 0, 0.62), transparent 30%),
			#2b1e0d;
		border: clamp(0.25rem, 0.8vw, 0.55rem) solid #171108;
		box-shadow:
			0 0 0 1px rgba(225, 180, 91, 0.72),
			0 0 0 0.45rem rgba(63, 43, 16, 0.9),
			0 2rem 5rem rgba(0, 0, 0, 0.72);
	}
	.frame-inner {
		padding: clamp(0.4rem, 1vw, 0.8rem);
		border: 1px solid rgba(239, 202, 128, 0.5);
		background: #100d08;
	}
	.manifest-paper {
		padding: clamp(1.4rem, 5vw, 4.8rem);
		background:
			radial-gradient(circle at 20% 8%, rgba(255, 255, 255, 0.58), transparent 24rem),
			linear-gradient(105deg, rgba(89, 55, 14, 0.07), transparent 27% 74%, rgba(89, 55, 14, 0.08)),
			#eee3c8;
		box-shadow: inset 0 0 3rem rgba(84, 55, 18, 0.18);
		color: #2c2419;
		font-size: clamp(1rem, 1.7vw, 1.12rem);
		line-height: 1.72;
		overflow-wrap: anywhere;
	}
	.manifest-paper section {
		scroll-margin-top: 1rem;
	}
	.document-status {
		margin: 0 0 0.7rem;
		color: #765b2b;
	}
	.document-status.authoritative {
		color: #5c4015;
	}
	.manifest-paper h2 {
		margin: 0 0 1.2rem;
		padding: 0 0 0.65rem;
		border: 0;
		border-bottom: 1px solid rgba(78, 54, 23, 0.52);
		color: #2c2114;
		font-size: clamp(1.7rem, 4vw, 2.7rem);
		font-weight: 500;
	}
	.manifest-paper h3 {
		margin: 2rem 0 0.45rem;
		color: #352717;
		font-size: clamp(1.18rem, 2.4vw, 1.5rem);
	}
	.manifest-paper :global(h2),
	.manifest-paper :global(h3),
	.manifest-paper :global(h4),
	.manifest-paper :global(h5) {
		color: #352717;
	}
	.manifest-paper :global(h2) {
		margin: 1rem 0 1.2rem;
		padding: 0 0 0.65rem;
		border: 0;
		border-bottom: 1px solid rgba(78, 54, 23, 0.52);
		font-size: clamp(1.45rem, 3.5vw, 2.2rem);
	}
	.manifest-paper :global(h3) {
		margin: 2rem 0 0.45rem;
		font-size: clamp(1.18rem, 2.4vw, 1.5rem);
	}
	.manifest-paper :global(h4) {
		margin: 1.45rem 0 0.35rem;
		font-size: 1.08rem;
	}
	.manifest-paper :global(a) {
		color: #66440f;
	}
	.manifest-paper li + li {
		margin-top: 0.65rem;
	}
	.document-divider {
		margin: clamp(3rem, 8vw, 6rem) 0;
		border: 0;
		border-top: 1px solid rgba(73, 49, 19, 0.65);
		box-shadow: 0 0.3rem 0 rgba(117, 82, 34, 0.12);
	}
	.reading-exit {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		gap: 1rem;
		width: min(64rem, 100%);
		margin: 2.2rem auto 0;
	}
	.reading-exit a {
		display: inline-flex;
		min-height: 44px;
		align-items: center;
		color: #d7ba73;
		font: 0.82rem ui-sans-serif, system-ui, sans-serif;
		text-decoration: none;
	}
	@media (max-width: 600px) {
		.manifest-room {
			padding-inline: 0.65rem;
		}
		.manifest-paper {
			padding: 1.35rem 1.05rem 2rem;
		}
		.reading-exit {
			padding-inline: 0.35rem;
		}
	}
</style>
