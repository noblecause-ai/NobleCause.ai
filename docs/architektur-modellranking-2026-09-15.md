# NobleCause.ai — Modellranking und Vorschlag für den Fünfer-Rat

**Stand:** 15. September 2026  
**Rolle:** Architektur  
**Status:** Auswahlvorschlag; noch keine Änderung der produktiven Besetzung

## Entscheidungsregel

Für den Rat zählt nicht Coding-Leistung, sondern belastbares Urteilen über
Evidenz, Organisationen, Risiken und lange Dokumente. Deshalb wird für jedes
Modell derselbe arithmetische Mittelwert aus sieben getrennten
Artificial-Analysis-Messwerten gebildet:

1. AA-Briefcase (agentische Wissensarbeit), auf 0–100 normiert als
   `(Elo - 500) / 20`;
2. GDPval-AA v2 (reale Wissensarbeit), gleich normiert;
3. AutomationBench-AA (Werkzeug- und Prozessarbeit, Prozent);
4. Humanity's Last Exam (allgemeines Schlussfolgern und Wissen, Prozent);
5. GDP.pdf (professionelle Dokumentanalyse, Prozent);
6. AA-Omniscience (Wissen minus Halluzination, Wertebereich −100 bis 100),
   auf 0–100 normiert als `(Wert + 100) / 2`;
7. AA-LCR v1.1 (Long-Context-Reasoning, Prozent).

Terminal-Bench, SciCode und CritPt bleiben draußen: Coding und reine
Physikleistung sind für die Ratsaufgabe keine tragenden Auswahlkriterien. Alle
sieben aufgenommenen Werte sind gleich gewichtet; der Mittelwert ist damit
nachrechenbar und enthält keine verdeckte Architektengewichtung.

Quelle für Messwerte und Methodik:

- <https://artificialanalysis.ai/leaderboards/models>
- <https://artificialanalysis.ai/methodology/intelligence-benchmarking>
- modellweise Vergleichstabellen unter
  <https://artificialanalysis.ai/models/comparisons/>

## Ranking — stärkstes gemessenes Modell je Anbieterfamilie

| Rang | Modell | Familie | NC-Mittel | AA-Index | Produktionsstatus |
|---:|---|---|---:|---:|---|
| 1 | Claude Fable 5.1 (max) | Anthropic | **60,26** | 53 | aktiv, Claude API |
| 2 | GPT-6 Astra (max) | OpenAI | **59,09** | 53 | aktiv, Responses API |
| 3 | Muse Spark 1.3 (max) | Meta | **56,30** | 48 | Public Preview |
| 4 | Grok 4.6 (high) | SpaceXAI | **54,41** | 44 | produktive API |
| 5 | Kimi K3 (max) | Moonshot/Kimi | **54,15** | 44 | produktive API |
| 6 | GLM-5.3 (max) | Z AI | **51,51** | 45 | produktive API |
| 7 | Gemini 3.8 Flash (high) | Google | **51,19** | 41 | GA, produktive API |
| 8 | Qwen3.8 Max | Alibaba | **48,91** | 40 | produktive API |

### Nachrechnung der sieben 0–100-Werte

| Modell | Briefcase | GDPval | Automation | HLE | GDP.pdf | Omniscience | LCR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude Fable 5.1 | 58,1 | 63,2 | 59 | 59 | 26 | 71,5 | 85 |
| GPT-6 Astra | 53,1 | 54,0 | 68 | 55 | 31 | 71,5 | 81 |
| Muse Spark 1.3 | 54,5 | 60,1 | 58 | 49 | 27 | 62,5 | 83 |
| Grok 4.6 | 51,7 | 57,1 | 67 | 43 | 17 | 65,0 | 80 |
| Kimi K3 | 49,6 | 53,5 | 58 | 47 | 22 | 60,0 | 89 |
| GLM-5.3 | 50,5 | 58,0 | 62 | 42 | 11 | 57,0 | 80 |
| Gemini 3.8 Flash | 35,1 | 48,2 | 60 | 48 | 21 | 65,0 | 81 |
| Qwen3.8 Max | 44,4 | 56,5 | 49 | 43 | 20 | 51,5 | 78 |

## Vorschlag für die neue Besetzung

Die bestehende Policy schließt Preview-Modelle aus. Muse Spark 1.3 ist zwar
gemessen Dritter, wird aber wegen seines Public-Preview-Status nicht produktiv
besetzt. Damit lautet der derzeit belastbar betreibbare Fünfer-Rat:

1. **Anthropic — Claude Fable 5.1** (`claude-fable-5-1`)
2. **OpenAI — GPT-6 Astra** (`gpt-6-astra`)
3. **SpaceXAI — Grok 4.6** (`grok-4.6`)
4. **Moonshot/Kimi — Kimi K3** (`kimi-k3`)
5. **Z AI — GLM-5.3** (`glm-5.3`)

Google scheidet nicht wegen mangelnder Betriebsreife aus, sondern landet nach
der sachbezogenen Mittelwertbildung knapp hinter GLM-5.3. Gemini 3.8 Flash ist
dadurch eine gute zweite Scout-Familie: produktiv, schnell, Search Grounding,
mit bereits vorhandenem NobleCause-Providerzugang und außerhalb dieses Rates.

## Betriebsreife vor einer Umbesetzung

Die Auswahl ist noch keine Freigabe zum Umschalten. Vor dem ersten echten Lauf
mit fünf Sitzen sind genau diese Nachweise nötig:

- API-Zugänge/Secrets für SpaceXAI, Kimi und Z AI;
- je ein minimaler Preflight-Canary und ein Council-Caller über die jeweilige
  offizielle API;
- ein isolierter Dry-run mit fünf Ratsmodellen und Budgetdeckel;
- additive Modellregistratur/Commission für neue Modell-IDs;
- Medaillons über die bestehende Commission-Kette; der neutrale Fallback hält
  den Deploy bis dahin funktionsfähig;
- DE/EN-Anzeigenamen und familienagnostische Teilnehmerdarstellung prüfen.

Es wird kein Multi-Provider-Gateway als neue Zwischenarchitektur eingeführt.
Die drei neuen Provider werden, wie die bestehenden drei, direkt und mit
kleinen expliziten Adaptern angebunden.

## Primärquellen zur API-Eignung

- Claude Fable 5.1: <https://platform.claude.com/docs/en/models/fable-5-1/overview>
- GPT-6 Astra: <https://developers.openai.com/api/docs/models/gpt-6-astra>
- Muse Spark / Meta Model API: <https://ai.meta.com/llama>
- Grok 4.6: <https://docs.x.ai/developers/models/grok-4.6>
- Kimi API: <https://www.kimi.ai/help/kimi-api/api-overview>
- GLM Chat Completion: <https://docs.z.ai/api-reference/llm/chat-completion>
- Gemini 3.8 Flash: <https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash>
