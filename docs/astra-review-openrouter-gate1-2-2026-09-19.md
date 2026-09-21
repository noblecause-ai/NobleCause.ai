# Astra — unabhängiges Review OpenRouter Gate 1–2

Stand: 19.09.2026. Ausgang: `b501a50b1e7e1eb921dde9d43a0b63d5e101ee83`.
Neuer Branch: `codex/openrouter-gate1-2-20260919`.
Worktree: `/private/tmp/nc-openrouter-gate1-2-20260919`.

## Befund und Bauentscheidung

**Phase A grün für den begrenzten Offline-Bau Gate 1–2. Keine Freigabe für
Inferenz, Commission, Rosterwechsel, Publikation oder Gate 3–6.**
Die unten genannten Abweichungen sind überprüft und innerhalb des bereits
beauftragten Archiv-/Budget-/Provenienz-/Barrieren-Slices behandelbar. Kein
Zielmodell muss ersetzt, keine Rekordregel gelockert und keine zweite Maschine
gebaut werden. Die noch nicht per Canary belegten Anbieterantworten bleiben
Gegenstand von Gate 3; synthetische Tests ersetzen diesen Nachweis nicht.
Dieser Befund wurde vor dem ersten Produktcode-Diff erstellt.

## 1. Git- und Worktree-Wahrheit

`git ls-remote` bestätigt Remote-master `b7289ebab477682887d6ca85b421f2131cb7f696`
und Remote-Upgrade `b501a50b1e7e1eb921dde9d43a0b63d5e101ee83`.
Lokaler master `274b437f9122f6eac7ae43cc824d114c15550c5e` ist sauber und elf
Commits hinter origin/master. Upgrade ist zwei Commits vor origin/master,
kein divergierender Commit. nc-sanitize steht auf `348d202`, Branch
`docs/p13-medaillon-befund`, acht Commits hinter origin/master: sechs fremde
Site-Dateien geändert (18 Einfügungen/41 Löschungen), 13 untracked Dokumente.
Nichts davon wurde übernommen oder verändert. Kein Fetch, Prune oder Reset.

**Korrektur der Übergabe:** Die zwei alten Worktrees werden wegen fehlender
`.git`-Verknüpfung als prunable geführt, ihre Verzeichnisse existieren jedoch
noch. In `/private/tmp/nc-maint-ssh-agent-20260913` sind insbesondere der
Anthropic-Adapter und seine Tests tatsächlich lesbar. Auch die drei ausdrücklich
dokumentierten temporären Preflight-/Canary-/Isolations-Verzeichnisse existieren.
Diese konkret benannten NC-Reste wurden nur lesend inventarisiert; keine
anderen Projekte oder persönlichen Harness-Sitzungen durchsucht.

Kein Stash vorhanden. `git fsck --full --no-reflogs --unreachable` findet 19
Commits, 47 Trees, 42 Blobs; keiner der 42 Blobs enthält die untersuchten
Pilotkennungen. Reachable Objektpfade und alte Worktree-Indizes enthalten keine
benannten Subscription-/Harness-/Pilotdateien. Daher: Quellcode aus vorhandenen
Dateien sicherbar, **kein existierender Archiv-Commit**, keine Behauptung einer
vollständigen Wiederherstellung des damaligen Arbeitsbaums.

## 2. Maschine, Kosten, Barrieren und Commission

`gremium/run_session.py:356` ist der gemeinsame Ratscaller; Commission importiert
ihnen denselben `call_model`-Pfad (`run_commission.py:37,268`). Die bisherige
Dispatcher-Tabelle hat Anthropic, OpenAI und Google. Ein expliziter
`transport: openrouter_api`-Zweig vor dem bisherigen Retry-Loop genügt.
HTTP kann über Python-Standardbibliothek laufen; keine neue SDK-Abhängigkeit.
Prompts, Parser, Organisationsregistratur und Aggregator bleiben gemeinsam.

Abweichungen zum angenommenen Vorzustand:

- Im Commit warnt `check_budget` (818–823) nur. Der echte Abbruch plus
  Einzelaufruf-Prüfstellen ist ausschließlich in den wiedergefundenen Dateien.
  Er ist unabhängig vom Abo und im Bau zu erhalten; die zusätzliche
  OpenRouter-Reservierung muss den nächsten Call vorab begrenzen.
- Bisher werden Listenpreise aus Tokenzahlen berechnet, kein billed-Nachweis.
  Billed darf nur aus abgeglichener Antwort-/Generation-Usage entstehen;
  Rundung der Anzeige darf den Budgetvergleich nicht steuern.
- `call_model` wiederholt bisher jede Exception zweimal. Dieser Loop darf
  OpenRouter nie umschließen. Unklarer Abrechnungsstatus stoppt den Lauf.
- Key-Preflight verlangt derzeit immer drei Keys; Rat und Commission brauchen
  konfigurationsabhängige Keys vor der ersten Dateianlage.
- Die 0.5-Maschine sammelt ungültige/nicht verfügbare Erwiderungen und läuft
  weiter. Strikte Phasenbarrieren bestehen nur im Abo-Dateirest. Im neuen
  Transport sind vollständige gültige Erstvoten/Erwiderungen/Schlussvoten
  erforderlich; bestehende direkte Rekordsemantik bleibt unverändert.
- `wart_step_result` schützt Anthropic-Zulieferungen mit `end_turn`; er ist
  kein universeller Rats-Refusal-Klassifikator. Native unbekannte/fehlende
  OpenRouter-Stops müssen invalid bleiben. Rohantworten gehen vor Ableitungen.

## 3. Modelle und Parameter — aktuelle öffentliche Metadaten

Ohne Key und ohne Inferenz wurden GET /api/v1/models sowie die fünf
GET /api/v1/models/{author}/{slug}/endpoints abgerufen. Alle fünf festen Slugs
sind vorhanden. Webseiten und API zählen Anbieter und Endpunktvarianten
unterschiedlich; der aktuelle API-Snapshot hat 4/5/5/20/34 Endpunktzeilen
(bei GLM auch doppelte Tags). Zahlen aus der Übergabe sind kein Pinningbeleg.

| Slug | kanonische Revision | Reasoning-Efforts | Katalog-Outputmaximum |
|---|---|---|---:|
| anthropic/claude-fable-5.1 | 20260831 | max, xhigh, high, medium, low | 128000 |
| openai/gpt-6-astra | 20260903 | max, xhigh, high, medium, low | 128000 |
| x-ai/grok-4.6 | 20260810 | xhigh, high, medium, low | 450000 |
| moonshotai/kimi-k3 | 20260715 | max, high, low | 943718 |
| z-ai/glm-5.3 | 20260816 | max, high, low | 131072 |

Alle führen reasoning/max_tokens/response_format/structured_outputs im
Modellkatalog; **das ist keine Endpunktgarantie**. Beispielsweise fehlt
structured_outputs bei Anthropic/Azure und Kimi/BaseTen; Kimi/DeepInfra bf16
hat nur 16384 Outputtokens. Astra/Azure nutzt max_completion_tokens statt
max_tokens. Deshalb muss die konkrete Konfiguration gegen den konkreten
Endpunkt geprüft werden. Bestehende gemischte Prosa-plus-JSON-Prompts dürfen
nicht still in reinen JSON-Modus gezwungen werden.

Aktuelle Metadaten bieten geeignete, explizite Endpunkte einschließlich
bekannter Präzision bei Kimi/GLM. Die Auswahl für Offline-Testkonfigurationen
ist ein Vorschlag, keine produktive Besetzung und keine Budgetfreigabe.
Native Stop-/Usage-Werte sind erst mit Gate 3 empirisch je Sitz belegbar;
API-Vertrag dokumentiert beide Stopwerte und native Tokenzahlen allgemein.

## 4. Routing und Provenienz

Festes Modell, genau ein Endpunkt, `allow_fallbacks=false`,
`require_parameters=true`, `data_collection=deny`, keine Tools/Plugins/
Presets/Antwort-Caches. ZDR nur mit positivem Eignungsbeleg, nicht aus einem
fehlenden Feld ableiten. Keine Modellliste oder Router-/latest-/online-/free-/
nitro-/floor-Variante. **Basis-Provider-Slugs matchen mehrere Varianten**:
Metadaten-Preflight muss Mehrdeutigkeit abweisen bzw. exakte Varianten pinnen.
Providername ist von Endpoint-Tag zu unterscheiden. Quantisierung `unknown`
ist keine behauptete Präzision; bekannte Werte und Änderungen sichtbar halten.

Request-Hülle ohne Secret, unveränderte Antwortbytes und Generation-Antwort
getrennt sichern, erst dann auswerten. requested/reported/model aus Generation,
Provider, Generation-ID, normalisierter/nativer Stop und Usage müssen stimmen.
Kein stilles Modell-Alias-Normalisieren. Fehlender nativer Stop: invalid.
Native Verweigerung nur mit Rohantwort und passendem nativen Marker; sonst
invalid, einschließlich Trunkierung und unbekannter Stops.

Usage-Prompt/Completion mit `native_tokens_prompt/completion` vergleichen,
nicht mit eventuell anderen normalisierten Zählern; Reasoning/Cachedetails
mitprüfen, sofern ausgewiesen. `usage.cost == generation.total_cost` ist die
Voraussetzung für billed, kein Mittelwert, keine Listenpreis-Substitution.
`provider.max_price` erwartet USD pro Million, Katalogpreise USD pro Token.
Preis-Overrides (z.B. Astra ab 272000, Grok ab 200000 Prompttokens) und
Reasoning als Outputverbrauch gehören in die Kostenobergrenze. Tokenlimits
und Restbudget müssen vor dem nächsten Aufruf zusammen geprüft werden.

## 5. Research, Schema, Site und Workflows

Wart/Scouts bleiben direkt; ihre Suchqueries stammen aus beobachteten
Toolaufrufen, nicht aus Promptbehauptungen. Keine Websearch-Migration.
`two_scouts` und `deliberation_0_5` sind false, Rat bleibt Fable 5/Sol/Gemini.
Session-Schema hat noch keinen Stimm-Provenienzvertrag. kosten.schema.json
ist ausdrücklich ein nicht erzwungener Vorschlag, nicht der Kosten-Schreibweg.
OpenRouter-Felder müssen optional für Bestandsrekorde und streng für neue
OpenRouter-Voten sein; Fables DE/EN-Verfahrenstext ausschließlich bedingt.

session.yml führt echte Key-Canaries, echte Sitzung und bei erfolgreichem
Nicht-dry-run Commit/Push/Deploy aus. Diese Workflows wurden nur gelesen;
auch workflow dry_run ist ausdrücklich kein Offline-Test. Keine Ausführung.

## 6. Recoverbare Pilot-Dateien (nur Abweichungen vom Upgrade-Commit)

Bytes und SHA-256 direkt aus dem vorhandenen Dateirest, keine Rekonstruktion
von Quelltext aus Befundprosa:

| Datei unter altem temporärem Pfad | Bytes | SHA-256 |
|---|---:|---|
| `gremium/README.md` | 10836 | `7ef67768d622f39741c7ac472745a320485dfdf3575d4dacfc3a44e6feb2c536` |
| `gremium/anthropic_subscription.py` | 11256 | `158d83622f498b8265c3538579a2d26671067283d3aed7a5d82ea0b3b9d1607b` |
| `gremium/config.json` | 2695 | `1fc2d7336d7abb9347955a1add591c0253f417aa60f5071c85f8d71c6b97ec8f` |
| `gremium/process_config.py` | 11256 | `fcae5a5f00805fdb236c11fe73e90c692947b3ad9d59266851c958bb9c63b42e` |
| `gremium/run_session.py` | 61292 | `33d48f4ef7ff164414eee420dbb362e5af5bb9b5e28bdf7b1d43527bb5c54e0c` |
| `gremium/tests/test_anthropic_subscription.py` | 16457 | `941036e215c6001045e1d29376ac2d2b1130bf013470432cab29e82dc86a34f9` |
| `gremium/tests/test_budget_cap.py` | 970 | `aa5c8bf9533945c9f3509ddf5495211f66d27c8345e65bc726bc1f18596cb105` |
| `gremium/tests/test_process_config.py` | 8791 | `0403777258cbf5812e3770e2454cbcff1701e53e49819c440d0432e73415cf1b` |
| `gremium/tests/test_schema_gate.py` | 3298 | `fec60e489df27f01b7a173887822cb498523e1147bc79ccef4df5f0d40a8d385` |
| `schema/session.schema.json` | 14535 | `a2854cb79db67545c94b031a28a5430a81d1ab8a3faa00b19a8122d58a3c0fec` |
| `site/src/lib/components/rooms/ArchiveRoom.svelte` | 13397 | `c494d171a2e4fd4e5014939e96e7210eda1845d659283d7bd2c1074e8b6d667f` |
| `site/src/lib/i18n/de.js` | 14921 | `3d7f0f6a459b8a69e7ac8996fdb1cafab011c71f1263b843dbf11e0fbdf2e4e0` |
| `site/src/lib/i18n/en.js` | 14480 | `f10065f7acb730ff1460579e79a6c08b1aef262e48633fa6d4d627195830064a` |
| `site/src/routes/sitzungen/[id]/+page.svelte` | 14121 | `daa22a5714b3cbda2ba2396e2eb5572407dc93fbf3ae09bb1b73b2d49aca4c80` |
| `site/tests/homepage-build.test.js` | 49258 | `b77b35c1a4d4062e56e8c74b23bb699b619ba21608ca8f1ba0dd1179dd46e730` |

Zusätzlich vorhanden: die Pflichtlektüre/Pilotentscheide in nc-sanitize/docs
und im alten Rest sowie die dokumentierten Canary-/Offline-Artefakte. Gate 1
soll diese explizit inventarisieren und lokal vorbereiten, aber keinen
Archiv-Branch committen. Fehlende Dateien nicht erfinden; alte Testzahlen
184/46 sind historische Befunde und keine Tests dieses HEAD.

## 7. Unabhängige Baseline

- Python: **109 passed**, socket.connect/create_connection gesperrt,
  API-Key-/Auth-Token-Umgebungsvariablen entfernt, CI=true, kein Bytecodecache.
- Schema-Tor all: **5 Sitzungen, 15 Journal-Einträge gültig**.
- Site npm test: **45 passed**, einschließlich statischem pretest-Build.
  Abhängigkeiten nur lesend aus nc-sanitize in den neuen Worktree kopiert.
- Kein Modellaufruf, kein Workflow gestartet; keine Rekord-/Roster-/Secretänderung.

## Primärquellen (19.09.2026)

- https://openrouter.ai/api/v1/models
- https://openrouter.ai/api/v1/models/anthropic/claude-fable-5.1/endpoints
- https://openrouter.ai/api/v1/models/openai/gpt-6-astra/endpoints
- https://openrouter.ai/api/v1/models/x-ai/grok-4.6/endpoints
- https://openrouter.ai/api/v1/models/moonshotai/kimi-k3/endpoints
- https://openrouter.ai/api/v1/models/z-ai/glm-5.3/endpoints
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/docs/api/reference/overview
- https://openrouter.ai/docs/api/api-reference/generations/get-generation
- https://openrouter.ai/docs/use-cases/usage-accounting
- https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
