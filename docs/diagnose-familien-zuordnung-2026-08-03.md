# Diagnose — Familien-Zuordnung Sitzung 2026-07c

**Von:** Claude Code (Mac-CC) · **Datum:** 2026-08-03
**Auftrag:** Diagnose vor Sitzung 4 — erbt sie den Befund? · **nur gelesen**, `sessions/**` unverändert.

## Der Befund
Das unter „Claude Opus" gelistete Votum von 2026-07c schreibt in Runde 1 **und** Runde 2
„Verfasst von einem Modell der GPT-/OpenAI-Familie" und verlangt selbst, ein Listungsfehler sei
„vor Protokollierung zu bereinigen — die Befangenheitsregel steht und fällt mit korrekter
Zuordnung". Protokolliert wurde trotzdem.

## Die Messung — drei Quellen, alle deckungsgleich

| Rohantwort | `response.model` | Rekord (`participants[].model` / family) | Config-Sitz (Sitzung-3-Zeit, `33c1bb6^`) |
|---|---|---|---|
| `r1/r2-anthropic.json` | **claude-opus-4-8** (Anthropic) | claude-opus-4-8 / anthropic | anthropic → claude-opus-4-8, „Claude Opus" |
| `r1/r2-openai.json` | gpt-5.2-2025-12-11 (OpenAI) | gpt-5.2 / openai | openai → gpt-5.2, „GPT" |
| `r1/r2-google.json` | gemini-2.5-pro (Google) | gemini-2.5-pro / google | google → gemini-2.5-pro, „Gemini Pro" |

Alle drei Spalten stimmen je Sitz überein: API-Bedienung, Rekord-Zuordnung und Config-Besetzung
nennen für jeden Sitz **dieselbe Familie**.

## Drei ausschließende Belege
1. **Schlüsselbasierte Zuordnung, nicht index-basiert:** `CALLERS[spec["family"]]` wählt den Aufrufer,
   die Rohantwort wird als `<tag>-<family>.json` gespeichert, jedes Votum trägt sein eigenes `{**spec}`
   (model/family/label). → keine Index-Fehlzuordnung (A ausgeschlossen).
2. **Generisches System-Prompt:** `SYSTEM_WITH_CONFLICT` enthält keinen `{family}`/`{label}`-Platzhalter
   und geht identisch an alle drei Modelle. Die Maschine sagt keinem Modell, welcher Familie es
   angehört. → die Fehl-Deklaration ist spontan, nicht injiziert.
3. **Config-Sitz zum Sitzungszeitpunkt:** der Sitz „Claude Opus" nannte ein Anthropic-Modell
   (`claude-opus-4-8`), kein OpenAI-Modell (C ausgeschlossen).

## Ergebnis: Hypothese B
Ein **Anthropic-Modell (`claude-opus-4-8`) hielt sich in seinem eigenen Text für ein OpenAI/GPT-Modell.**
Bekannter Fehlermodus. **Der Mechanismus ist korrekt. Rekord-Befund, kein Code-Befund.**
(Das r2-GPT-Votum sagt korrekt „GPT-Familie" — kein Problem.)

## Die eine Frage: erbt Sitzung 4 den Fehler? — **NEIN.**
Es ist B, nicht A/C. Die Familien-Zuordnung im Rekord kommt aus der Config, nicht aus dem Modelltext;
Sitzung 4 (neue Besetzung, `33c1bb6`) wird über denselben schlüsselbasierten Weg korrekt
besetzt/bedient/protokolliert. Es gibt keinen Mechanismus-Fehler zu erben.
*Vorbehalt:* ob ein Sitzung-4-Modell sich im Text erneut fehl-deklariert, ist Modellverhalten
(unvorhersehbar) — es beträfe wieder nur den Text, nicht die Zuordnung und nicht den Zählstand.

## Bestätigung zu Frage 3 (Zählstand / Enthaltung)
Der Zählstand ist **unverfälscht** — die falsche Selbstaussage berührt keine gezählte Größe. Die
Enthaltung in Säule C war inhaltlich richtig, egal welche Familie: Anthropic wie OpenAI sind
AI-Labore, der Interessenkonflikt bestand in beiden Fällen. **Kein Rekord muss zurückgezogen werden.**

## Nebenbefund (0.4.1, kein Handlungsbedarf) — P12
Der Runde-2-Loop nutzt `zip(config["models"], r1)` — ordnungsbasiert. Hier ungefährlich, weil die
Votum-Identität mit dem Spec reist, nicht mit dem Index. Dritte Stelle mit Reihenfolge-Abhängigkeit
nach B1 und P3; ein Key-Join wäre robuster.
