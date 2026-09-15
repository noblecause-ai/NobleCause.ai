# NobleCause.ai — Anschlussauftrag neue Ratsbesetzung

**Stand:** 15. September 2026  
**Status:** vorbereitet; Ausführung erst nach Bereitstellung der drei Secrets und
ausdrücklicher Freigabe des bezahlten Preflights

## Zielbesetzung

1. Anthropic — Claude Fable 5.1 (`claude-fable-5-1`)
2. OpenAI — GPT-6 Astra (`gpt-6-astra`)
3. SpaceXAI — Grok 4.6 (`grok-4.6`)
4. Moonshot/Kimi — Kimi K3 (`kimi-k3`)
5. Z AI — GLM-5.3 (`glm-5.3`)

Die Auswahl folgt dem Architektur-Ranking vom 15.09.2026. Sie ist noch keine
produktive Umschaltfreigabe.

## 1 · Zugangsdaten durch den Steward

| Familie | lokales/GitHub-Secret | offizieller API-Endpunkt | Modell |
|---|---|---|---|
| SpaceXAI | `XAI_API_KEY` | `https://api.x.ai/v1` | `grok-4.6` |
| Moonshot/Kimi | `MOONSHOT_API_KEY` | `https://api.moonshot.ai/v1` | `kimi-k3` |
| Z AI | `ZAI_API_KEY` | `https://api.z.ai/api/paas/v4/` | `glm-5.3` |

Die Schlüssel werden ausschließlich lokal in der bestehenden `.env` und als
GitHub-Actions-Secrets hinterlegt. Sie gehören weder in diesen Auftrag noch in
Logs, Chat oder Git. Vor dem ersten Call je Anbieter: Konto aktivieren,
Pay-as-you-go-Guthaben bzw. Kreditlimit setzen und ein gemeinsames maximales
Preflight-Budget festlegen.

Bereits vorhanden und weiterverwendet: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`,
`GEMINI_API_KEY`.

## 2 · Kleiner Integrations-Slice

Keine neue Provider-Abstraktionsschicht und keine separaten Dienste bauen.
Statt drei kopierter Caller werden im bestehenden `run_session.py` zwei kleine
Transporthelfer verwendet:

- Responses-kompatibel für OpenAI und xAI, mit explizitem API-Key und
  `base_url`;
- Chat-Completions-kompatibel für Kimi und Z AI, ebenfalls mit explizitem Key
  und `base_url`.

Jede Familie behält dennoch ihre explizite Konfiguration für Modell-ID,
Reasoning-Parameter, Stop-Grund, Usage und Preis. Provider-Rohantworten werden
wie bisher vollständig gespeichert. Unbekannte Stop-Gründe, fehlende Usage oder
nicht parsebare Schlussvoten brechen laut ab; es gibt keinen stillen Fallback
auf ein anderes Modell.

Zusätzlich:

- Key-Preflight aus der tatsächlich konfigurierten Ratsbesetzung ableiten und
  vor jeder Verzeichnisanlage ausführen;
- aktuelle Input-/Outputpreise in `config.json` aufnehmen;
- ausschließlich gestubbte Adapter-, Kosten- und Refusal-Tests ergänzen;
- bestehende Rekorde und die ausgeschalteten Feature-Schalter nicht verändern.

## 3 · Schreibfreie Provider-Canaries

Nach Steward-Freigabe je Provider genau ein minimaler Call mit festem
Tokenlimit und gemeinsamem Budgetdeckel. Die Canaries prüfen nur:

1. Secret und Modellzugriff;
2. korrekte Modell-ID und Endpoint-Region;
3. strukturierte JSON-Ausgabe;
4. Stop-Grund und Usage-Felder;
5. tatsächliche Kosten gegen den Preisvertrag.

Die Canaries schreiben ausschließlich nach `/tmp`, niemals nach `sessions/`,
`journal/`, `models.json` oder `schedule.json`. Bei einem Fehler wird nicht zum
nächsten Prozessschritt weitergegangen.

## 4 · Registratur und Medaillons

Nach grünen Canaries wird die vorhandene additive Commission-Kette genau einmal
für die neuen Modell-IDs ausgeführt. Die Modelle bestellen ihr Motiv selbst;
danach werden nur die freigegebenen Master über die bestehende
Medaillon-Nachbearbeitung eingebaut. Keine zweite Bild- oder
Registratur-Infrastruktur anlegen.

## 5 · Ein gemeinsamer Verfahrens-Dry-run

Erst wenn alle fünf Council-Caller und die Commission grün sind:

- `two_scouts` nur im isolierten Dry-run aktivieren: Anthropic-Scout plus
  Google Search Grounding; Google liegt dann außerhalb des Rates;
- `deliberation_0_5` im selben Dry-run aktivieren;
- fünf Erstvoten, je genau eine adressierte Erwiderung und fünf Schlussvoten
  prüfen;
- getrennte Scout-Rohpfade, Divergenz, Refusals, Kosten und Site-Darstellung
  abnehmen;
- Ergebnis als Artefakt, kein Rekordcommit und kein automatischer Push.

Erst die Abnahme dieses einen Laufs erlaubt die dauerhafte Besetzungs- und
Feature-Umschaltung. Ein scharfer Sitzungslauf bleibt ein eigener,
ausdrücklich freizugebender Schritt.

## Offizielle Anschlussquellen

- xAI Quickstart: <https://docs.x.ai/developers/quickstart>
- Kimi API Overview: <https://platform.kimi.ai/docs/api/overview>
- Z AI API Introduction: <https://docs.z.ai/api-reference/introduction>
- Z AI GLM-5.3: <https://docs.z.ai/guides/llm/glm-5.3>
