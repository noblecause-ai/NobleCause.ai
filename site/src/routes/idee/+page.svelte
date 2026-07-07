<svelte:head>
	<title>Wie eine Sitzung funktioniert — NobleCause.ai</title>
	<meta
		name="description"
		content="Der Ablauf einer Gremium-Sitzung: drei Modellfamilien, zwei Runden, dokumentierter Dissens, veröffentlichte Kosten."
	/>
</svelte:head>

<p class="kicker">Die Idee</p>
<h1>Wie eine Sitzung funktioniert</h1>

<p>
	Eine Gremium-Sitzung ist kein Chat und keine Plattform, sondern ein dokumentierter Lauf: eine
	Fragestellung, mehrere Modelle, zwei Runden, ein Protokoll. Der Ablauf wird von einem
	deterministischen Skript orchestriert — kein Modell steuert den Prozess, Modelle liefern
	ausschließlich Voten.
</p>

<h2>1 · Einberufung</h2>
<p>
	Jede Sitzung beginnt mit einer präzisen Fragestellung, etwa: <em>„Welche drei Interventionen
	bieten pro 1'000 € die höchste erwartbare Wirkung je Säule?"</em> Einberufen werden Modelle aus
	drei verschiedenen AI-Familien (z. B. Anthropic, OpenAI, Google). Die Familien-Vielfalt ist
	Absicht: Sie verringert das Risiko, dass das Gremium nur das Echo einer einzigen Modelllinie
	produziert.
</p>

<h2>2 · Runde 1 — Einzelvotum</h2>
<p>
	Jedes Modell erhält dasselbe Material: das <a href="/manifest/">Manifest</a>, die Fragestellung
	und eine Liste von Referenzquellen. Es antwortet unabhängig — ohne die Voten der anderen zu
	kennen — mit einer begründeten Empfehlung je Säule und einer Konfidenzangabe (Kanon der Demut).
</p>

<h2>3 · Runde 2 — Gegenlese und Schlussvotum</h2>
<p>
	Jedes Modell liest die Erstvoten der beiden anderen und gibt ein Schlussvotum ab: Wo revidiert es
	seine Position, wo hält es an ihr fest, und warum? Verbleibende Uneinigkeit wird nicht
	weggemittelt, sondern in einem eigenen <strong>Dissens-Abschnitt</strong> des Protokolls
	festgehalten.
</p>

<h2>4 · Protokoll und Veröffentlichung</h2>
<p>
	Aus beiden Runden entsteht das Sitzungsprotokoll: Fragestellung, Teilnehmer-Modelle mit exakten
	Versionen, die wörtlichen Prompts, alle Einzelvoten mit Konfidenzen, der Dissens, die
	Empfehlungen mit Begründung — und die Kosten des Laufs in Euro, auf den Cent. Auch die
	unbearbeiteten Rohantworten der Modelle werden mitveröffentlicht. Das Protokoll wird in das
	öffentliche <a href="https://github.com/noblecause-ai/NobleCause.ai">Repository</a> übernommen;
	diese Site rendert es automatisch.
</p>

<h2>Was dieses Projekt nicht tut</h2>
<p>
	Es nimmt kein Geld an. Empfehlungen verlinken auf die offiziellen Spendenwege der jeweiligen
	Organisationen — wer einer Empfehlung folgen will, tut das direkt bei der Organisation, ohne
	Umweg über dieses Projekt. Es gibt kein Konto, keinen Login, keine Kommentare und keinen
	Newsletter.
</p>

<h2>Warum radikale Transparenz?</h2>
<p>
	AI-generierte Empfehlungen verdienen erst dann Vertrauen, wenn jeder Schritt nachprüfbar ist.
	Deshalb ist hier nichts kuratiert, was nicht auch im Rohzustand einsehbar wäre: Wer den Prompts
	misstraut, liest die Prompts. Wer der Zusammenfassung misstraut, liest die Rohantworten. Wer dem
	Projekt misstraut, liest den Quellcode.
</p>
