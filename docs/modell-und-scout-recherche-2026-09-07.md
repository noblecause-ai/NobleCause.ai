# NobleCause.ai — Modell- und Scout-Recherche

Stand: 7. September 2026 · nur offizielle Anbieterquellen und kostenlose
Metadatenprüfungen · keine Generations- oder Suchläufe ausgelöst

## Entscheidungsmaßstab

Der bestehende Rat folgt `strongest_production_model_per_family`; Preview-Modelle
sind ausgeschlossen (`gremium/config.json`). Diese Regel ist nicht identisch mit
„neueste sichtbare Modell-ID“. Für einen Sitz zählen daher:

1. vom Anbieter als produktiv bzw. allgemein verfügbar ausgewiesen;
2. höchste belegte allgemeine Leistungsposition innerhalb der Familie;
3. API-Zugang im vorhandenen Konto;
4. Kompatibilität mit langem deutschen Text, strukturiertem Schlussvotum und
   dem vorhandenen Fehler-/Kostenvertrag;
5. projektspezifischer Probe-Durchlauf vor dem scharfen Wechsel.

Scouts werden getrennt bewertet. Dort sind Websuche, Quellenbelege,
Nicht-Verweigerung und sichtbare Suchanfragen wichtiger als maximale allgemeine
Modellstärke.

## Bestehende Ratsfamilien

| Familie | Heute konfiguriert | Offizieller Kandidat | Belegter Stand | Preis je 1 Mio. Token, Input/Output | Architektururteil |
|---|---|---|---|---|---|
| Anthropic | `claude-fable-5` | `claude-fable-5-1` | Anthropic nennt Fable 5.1 sein leistungsfähigstes breit veröffentlichtes Modell und das Frontier-Modell für anspruchsvolle, lang laufende Forschung. API-Status: aktiv/aktuell. | $10 / $50 | Klarer Aktualisierungskandidat, aber erst Probe mit NobleCause-Schema. Anthropic dokumentiert Safety-Classifier und empfiehlt Refusal-Fallbacks; die Stärkeentscheidung beseitigt dieses Betriebsrisiko nicht. |
| OpenAI | `gpt-5.6-sol` | `gpt-6-astra` | OpenAI bezeichnet Astra als sein leistungsfähigstes Modell und Flaggschiff für komplexes Reasoning und Research; Structured Outputs werden unterstützt. | $10 / $50 | Klarer Aktualisierungskandidat für den bestehenden OpenAI-Sitz; vor Wechsel Prompt-/Schema-Probe und neuer Budgetdeckel. |
| Google | `gemini-3.7-flash` | `gemini-3.8-flash` | 3.8 Flash ist GA, stabil und laut Google das intelligenteste Flash-Modell. Die Modellliste führt daneben Gemini 3.1 Pro nur als Preview; es ist nach der bestehenden Policy nicht sitzfähig. | bis 31.12.2026 $0,75 / $3,75; danach $1,50 / $7,50 | Unter der bestehenden **Produktiv-plus-keine-Preview**-Regel ist 3.8 Flash der belegte Aktualisierungskandidat. Das ist keine Behauptung, Flash sei stärker als jedes Google-Preview-Modell. |

Kostenlose API-Metadatenprüfungen mit den bereits vorhandenen Schlüsseln haben
am Stichtag die IDs `claude-fable-5-1`, `gpt-6-astra` und
`gemini-3.8-flash` als verfügbar bestätigt. Das waren keine Generationen und
keine Qualitätsmessungen.

## Zusätzliche Familien für Scouts bzw. spätere Zulassungsproben

| Familie | Offiziell aktuelles Modell | Websuche und Struktur | Preis | Befund für NobleCause |
|---|---|---|---|---|
| xAI | `grok-4.6` | xAI nennt es sein intelligentestes allgemeines Modell; Structured Outputs und serverseitige Web-/X-Suche sind dokumentiert. | $2 / $6 | Stärkster derzeit belegter **Scout-Kandidat außerhalb des Rates**. Im Projekt fehlen aber `XAI_API_KEY`, Caller, Kostenadapter und jede NobleCause-Probe. Keine Vorentscheidung. |
| Moonshot/Kimi | `kimi-k3` | Kimi nennt K3 sein leistungsfähigstes Flaggschiff; 1M Kontext, striktes JSON-Schema. Offizielle Websuche existiert, wird laut derselben Dokumentation derzeit überarbeitet und kurzfristig nicht für Produktion empfohlen. | Die öffentlich gerenderte Preisseite lieferte im abrufbaren Stand keine Zahlen; vor Probe im Konto verifizieren. | Der historische Kimi-K2-Vorschlag ist überholt; K2 ist eingestellt. K3 bleibt Zulassungskandidat, ist wegen des eigenen Websuche-Warnhinweises heute kein bevorzugter Produktions-Scout. |
| Mistral | `mistral-large-2512` / Alias `mistral-large-latest` | GA, 256k Kontext, Structured Outputs und Function Calling. Eine für den jetzigen Scout-Vertrag gleichwertige, nachvollziehbar protokollierte serverseitige Websuche ist in den geprüften Modellunterlagen nicht hinreichend belegt. | $0,50 / $1,50 | Günstiger Kandidat für Council-/Shadow-Proben. Als Scout erst nach belegtem Suchadapter und Quellenvertrag. |

## Vorhandener Acht-Fragen-Vergleich

Der Vergleichskatalog muss nicht neu erfunden werden. Die acht veröffentlichten
Suchanfragen stehen in `journal/2026-07-08c/entry.json`:

1. `Helen Keller International vitamin A funding 2026`
2. `TaRL Africa Pratham funding gap 2026`
3. `Against Malaria Foundation funding 2026 GiveWell`
4. `Lead Exposure Elimination Project LEEP funding 2026`
5. `NTI biosecurity funding 2026 pandemic preparedness`
6. `TaRL Africa room for more funding 2025 2026`
7. `LEEP donate 2026 funding gap`
8. `Helen Keller International USAID cuts 2026`

Der Wart-Entscheid vom 3. August verlangt ausdrücklich dieselben acht Anfragen
gegen GPT und Gemini, ohne Rekordschreibung, bevor ein Scout-Sitz gewechselt
wird (`docs/wart-entscheid-verweigerung-im-rekord-2026-08-03.md`, Zeilen
64–65 und 91–96). Die Übergabe vom 7. August verlangt danach zwei Scouts und
mindestens eine Familie außerhalb des Rates.

## Empfohlener Messlauf — noch nicht freigegeben

Ein fairer heutiger Vergleich sollte die acht Anfragen **wortgleich** und ohne
Zugriff auf die Antworten anderer Kandidaten ausführen. Vorgeschlagene
Kandidaten: bestehender Anthropic-Scout als Basislinie, Astra, Gemini 3.8 Flash,
Grok 4.6, Kimi K3 und Mistral Large 3 — letzterer nur, wenn ein gleichwertiger
Suchadapter belegt ist.

Vor einem bezahlten Lauf werden separat vorgelegt:

- konkrete Modell-IDs und API-Verfügbarkeit im jeweiligen Konto;
- je Kandidat genau ein Dossier-Call, höchstens acht Suchanfragen und ein
  identischer Outputdeckel;
- Anbieterpreise für Token **und** Suche, inklusive maximaler Gesamtkosten;
- Bewertungsraster: Quellenabdeckung, Datumsnähe, falsche oder unbelegte Zahlen,
  `rejected_findings`, Refusal/Abbruch, JSON-Vertrag und Laufzeit;
- keine Aufzeichnung in `journal/` und keine Konfigurationsänderung.

Erst dieses Ergebnis rechtfertigt die konkrete Zweierbesetzung. Die heute
belegbare Vorhypothese lautet lediglich: Grok 4.6 verdient wegen dokumentierter
Websuche und Außenfamilie einen Platz im Vergleich; Kimi K3 verdient trotz
allgemeiner Stärke wegen der eigenen Websuche-Warnung keinen automatischen
Produktionsplatz.

## Offizielle Quellen

- OpenAI: <https://developers.openai.com/api/docs/models/gpt-6-astra>
- Anthropic Modellwahl: <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
- Anthropic Fable 5.1: <https://platform.claude.com/docs/en/models/fable-5-1/overview>
- Google Modellliste: <https://ai.google.dev/gemini-api/docs/models>
- Google Gemini 3.8 Flash: <https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash>
- Google Preise: <https://ai.google.dev/gemini-api/docs/pricing>
- xAI Modelle: <https://docs.x.ai/developers/models>
- Kimi Modellliste: <https://platform.kimi.ai/docs/models>
- Kimi K3: <https://platform.kimi.ai/docs/guide/kimi-k3-quickstart>
- Kimi Websuche: <https://platform.kimi.ai/docs/guide/use-web-search>
- Mistral Large 3: <https://docs.mistral.ai/models/mistral-large-3-25-12>
- Mistral Preise: <https://docs.mistral.ai/inference/pricing>
