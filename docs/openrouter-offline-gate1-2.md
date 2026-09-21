# OpenRouter — Offline-Slice Gate 1–2

Stand: 19.09.2026. Inaktiv; kein Canary, keine Commission und kein Ratslauf
freigegeben. Die aktive Besetzung steht unverändert in gremium/config.json.

## Pilotarchiv

Der Abo-Pilot wird nicht als produktiver Transport übernommen. Der neue
Produktpfad akzeptiert `api` und `openrouter_api`, keine Harness-Kanäle.
Die vollständige Herkunftsinventur des wiedergefundenen Dateirests und der
belegten Pilotdokumente liegt lokal unter `.review/subscription-pilot-inventory.json`,
das vorbereitete Archiv unter `.review/subscription-pilot-recovery.tar.gz`.
Beides ist ein lokales Übergabeartefakt, kein Produktcode und kein Archiv-Commit.
Die Quellpfade bleiben unangetastet. Kein Archiv-Branch wurde veröffentlicht.

Entscheidgrundlage sind der Steward-Auftrag und Fables Wart-Review vom
19.09.2026 im Meta-Baum. Der Pilot scheiterte als einheitlicher produktiver Weg
an der nicht einheitlich belegbaren Identität, Isolation, Stop-/Usage-Semantik
und Kostenbasis. Seine Befunddokumente werden nicht als Quellcode ausgegeben.
Adapter, Tests, Konfiguration, Schema und Site-Anteile sind tatsächlich
recoverbar; Vollständigkeit des damaligen Arbeitsbaums ist nicht behauptet.
Unabhängige Budgetabbruch- und Phasenbarrieren wurden aus den lesbaren
Vorarbeiten übernommen und auf den neuen Transport begrenzt bzw. gehärtet.

## Gemeinsamer Aufrufpfad

`run_session.call_model` dispatcht den neuen Transport vor dem alten
Direkt-API-Retry-Loop. Commission verwendet denselben Caller und erhält einen
Budgetdeckel. `gremium/openrouter.py` nutzt ausschließlich Python-HTTP,
keine zusätzliche Abhängigkeit und keine eigene Sitzungsorchestrierung.

`openrouter-candidates.json` ist eine **nicht geladene** Offline-Konfiguration.
Sie ist kein bewilligter Preisvertrag und keine produktive Upstream-Auswahl.
Ihre fünf Slugs und Endpunktparameter stammen aus dem öffentlichen Katalog vom
19.09.2026. Vor Gate 3 sind Auswahl, Limits und Budget ausdrücklich abzunehmen.
Das Produktionsconfig, beide Feature-Schalter und die Modellregistratur
wurden nicht verändert.

Rat verlangt entweder den bestehenden API-Modus oder genau fünf feste
OpenRouter-Sitze. Modelllisten, automatische Routen, Abo-Transporte und
Mischbesetzungen werden abgewiesen. Die direkten Research-/Redaktionspfade
bleiben separat. Ihre Schlüssel werden zusätzlich benötigt, wenn sie im
konkreten Lauf verwendet werden. Es wird kein Secret angelegt oder kopiert.

Preflight vor Dateianlage: Konfiguration, erforderliche Keys, verfügbares
Key-/Kontoguthaben, feste Modell-ID, Reasoning-Effort, eindeutiger Endpunkt,
Parameter, Outputlimit, Status, Präzision und Preis. Jeder Request verlangt
`allow_fallbacks=false`, `require_parameters=true`, `data_collection=deny`;
kein Tool/Plugin/Preset, kein Antwortcache. ZDR ist nicht pauschal als bewiesen
behauptet. Bekannte Quantisierung wird geprüft, `unknown` bleibt unbekannt.

Bestehende Prompts enthalten Prosa und einen JSON-Block. Daher wird keine
neue response_format-Vorgabe eingeschoben; Parser und Promptvertrag bleiben
bestehen. Endpunktunterstützung für strukturierte Ausgabe wurde im Review
separat geprüft, ist kein Anlass, den Prompt still in JSON-only zu ändern.

## Kosten und Fehler

Vor jedem OpenRouter-Inferenzrequest wird konservativ der **gesamte
Katalogkontext** zum Input-Höchstpreis plus das begrenzte Output zum
Output-Höchstpreis reserviert. Das ist absichtlich strenger als eine geschätzte
Prompttokenzahl und kann einen bezahlbaren Call verweigern. Höherpreisige
Long-Context-Tiers werden durch max_price ausgeschlossen; die Preisgrenze
wird nicht automatisch angehoben. Dieser Mechanismus darf später nur gegen
einen belegbaren engeren Input-Bound ersetzt werden.

Diese Vorabreservierung gilt für den neuen OpenRouter-Transport. Direkte
Wart-/Scout-/Redaktionskosten bleiben wie bisher Listenpreis-Schätzungen;
ihr vorhandener Budgetdeckel wurde zum harten Abbruch nach gemessenem
Verbrauch korrigiert. Das ist keine Behauptung einer kontoseitigen harten
Ausgabensperre für direkte Anbieter. Für spätere vollständige Sitzungsbudgets
sind diese getrennten Rollen im Budgetvertrag mitzuberücksichtigen.

Antwort- und Generationsmetadaten müssen Modell, Upstream, ID, Stops,
native Input-/Outputtokens, ausgewiesene Reasoning-/Cachetokens und Kosten
bestätigen. Nur dann heißt die Kostenbasis `billed`. Verglichen wird mit
Dezimalzahlen; fehlende Werte sind keine Null. Bei Abweichung stehen die beiden
unveränderten Rohbelege nebeneinander, ohne Mittelwert oder Schätzung.

Request ohne Secret, Endpoint-Snapshot, unveränderte Antwortbytes,
unveränderte Generation-Antwort und abgeleiteter Ergebnisstatus werden
getrennt geschrieben. Existierende Artefakte verhindern einen zweiten Call.
Timeout/Transportfehler/ungeklärte Abrechnung: sofortiger Abbruch, keine
Wiederholung, kein Ersatzmodell. Fehlender nativer Stop ist invalid, niemals
refusal. Native Verweigerung plus Rohantwort ist refusal; der Lauf publiziert
keinen gültigen Ersatzrekord. Erfolgreich beendete, aber unparsebare Voten
scheitern an der Phasenbarriere. Die Rohbelege bleiben erhalten.

## Darstellung und Nachweise

Neue Provenienz wird je Runde im bestehenden Sitzungs-Explorer sichtbar.
Fables DE/EN-Verfahrenstext erscheint ausschließlich bei entsprechenden
OpenRouter-Daten. Keine globale Umdeutung historischer Kosten oder Voten.
Das Schema verlangt für gekennzeichnete neue Rekorde Stimm-Provenienz und
konsistente Modellzuordnung; Bestandsrekorde behalten ihren Vertrag.

Die Abnahmetests verwenden synthetische Providerdaten. Sie belegen keine
tatsächliche Parameterannahme, Rechnung, Modellverweigerung oder ZDR-Eignung
bei einem realen Anbieter. Der vollständige synthetische Sitzungs-/Commission-
Schreibweg schreibt ausschließlich in Test-Tmp-Verzeichnisse.

## Noch offen, ausdrücklich nicht ausgeführt

- Gate 3: konkrete Endpunkte/Präzision/Preise abnehmen, separates Canarybudget
  und genau fünf reale, schreibfreie Canaries; Identität, native Stops,
  Parameterannahme, Usage und Kosten empirisch abgleichen.
- Gate 4: echte Commission, Medaillons und kompletter Fünfer-Rat-Dry-run mit
  separatem Budget einschließlich direkter Nebenrollen; Wart-Abnahme.
- Gate 5: ausdrückliche Umschaltfreigabe, Secret-Bereitstellung, additive
  Registratur/Rosterumschaltung, überwachter scharfer Lauf und Deploy.
- Gate 6: eigener Search-Provenienz-Canary samt Wart-Entscheid; Research bleibt
  bis dahin direkt.
- Archiv-Commit/Push sowie Produkt-Commit/Push: separat freizugeben.
