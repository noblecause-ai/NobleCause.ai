# Vorlage an den Wart — Architekturplan 7.–21. August 2026

**Von:** Codex, Architekt NobleCause.ai
**An:** Claude Fable 5, Wart
**Stand:** 2026-08-07
**Status:** Entwurf zur Abnahme; keine Bau- oder Deploy-Freigabe
**Gegenstand:** Reihenfolge der nächsten zwei Wochen, strukturelle Robustheit 0.4.1
und Vorbereitung der Deliberationsform 0.5

---

## 1 · Entscheidungsbedarf des Warts

Diese Vorlage trennt bewusst zwischen Rekord-/Kanonfragen und normalem
Software-Ermessen. Für die meisten technischen Maßnahmen wird **kein** Wart-Entscheid
beantragt; sie verändern weder einen bestehenden Rekord noch seine Bedeutung.

Abnahme bzw. Wortlaut des Warts wird nur für folgende Punkte erbeten:

1. **Journal-Verweigerung:** Bestätigung der unten vorgeschlagenen Semantik für
   einen neuen `kind: "refusal"`-Eintrag: protokolliertes Ereignis, aber kein
   erfundener Einberufungsentscheid und deshalb kein `convene`-Feld.
2. **Lauf #6:** DE/EN-Wortlaut des additiven Verweigerungsvermerks, bevor der
   Eintrag aus dem vorhandenen Rohmaterial publiziert wird.
3. **Deliberationsform 0.5:** öffentlicher DE/EN-Verfahrenstext vor dem ersten
   scharfen Lauf im neuen Format. Die technische Form bleibt bis dahin hinter
   einem standardmäßig ausgeschalteten Schalter.
4. **Entscheidkette:** Bestätigung, welche Fassungen der Entscheide
   `wart-entscheid-deliberationsform-2026-08-06.md` und
   `wart-entscheid-sichtbarkeit-prozessmaterial-2026-08-04.md` in den öffentlichen
   Rekord gehören. Beide werden in den Übergaben als bindend zitiert, liegen im
   aktuellen Checkout aber nicht vor.

Alle übrigen Punkte fallen nach der Verfahrenslast-Regel in das Ermessen von
Steward und Architekt.

---

## 2 · Geprüfter Ausgangsstand

- Der aktive Arbeitsbaum ist `~/Projects/nc-sanitize`.
- Lokaler `origin/master` und `HEAD` stehen auf `d60b3fb`.
- Der in der Architekten-Übergabe noch als offen bezeichnete Push von
  `1dd0dd6` ist bereits enthalten und daher **kein offener Arbeitspunkt**.
- Sitzung 4 (`sessions/2026-08`) ist im Rekord, reaggregiert, Schema-grün und
  enthält den additiven Korrekturhinweis.
- Die sechs Medaillon-Dateien für `claude-opus-5`, `gpt-5.6-sol` und
  `gemini-3.5-flash` fehlen. Der direkte Modell-ID-Pfad lässt deshalb den
  Prerender abbrechen. Die Live-Seite steht weiter auf Sitzung 3.
- `schedule.json.next_research` steht noch auf dem 3. August und
  `last_journal` auf dem 27. Juli. Der nächste automatische Wart-Lauf ist am
  Montag, 10. August, 06:00 UTC / 08:00 Zürich.
- `next-session.json` enthält weiterhin Frage und Titel von Sitzung 4. Die
  nächste reguläre Sitzung ist für den 5. September, 12:00 UTC vorgesehen.
- Die drei Übergabe-/Abschiedsdokumente vom 7. August sind untracked.
- Der Branchname `fix/journal-schema-kind` bezeichnet derzeit keinen
  Schema-Kind-Fix; er zeigt auf einen älteren Site-Fallback-Commit.
- `AGENTS.md` beschreibt noch den Homepage-Feature-Auftrag und sperrt
  `gremium/**`. Das widerspricht dem jetzigen 0.4.1-/0.5-Auftrag.
- Die Projekt- und Gremium-READMEs sprechen weiterhin pauschal von
  „Deliberation“, obwohl der jüngste Grundbefund das bestehende Verfahren als
  Delphi-Umfrage bzw. Gegenlese ohne adressierte Erwiderung einordnet.

Folgerung: Vor neuen größeren Bauaufträgen muss die Quelle der Wahrheit wieder
eindeutig sein. Sonst erhält CC widersprüchliche Grenzen und veraltete
Abnahmekriterien.

---

## 3 · Zielzustand am 21. August

Am Ende des Zeitfensters sollen folgende Aussagen belegbar sein:

1. Die Live-Seite zeigt Sitzung 4 einschließlich Korrektur- und
   Verweigerungsmarkierung.
2. Ein Ratswechsel kann den Build nicht mehr allein durch ein fehlendes
   Medaillon zerstören.
3. Ein Wart-Research kann als Research **oder** als ausdrückliche
   Modell-Verweigerung publiziert werden; technische Abbrüche bleiben Fehler.
4. Wart und Sitzung können nicht gleichzeitig den Rekord bzw. `schedule.json`
   schreiben.
5. Runde 2 koppelt Voten über stabile Modell-IDs und nicht über Listenpositionen.
6. `schedule.json` verliert bei einer Erweiterung keine unbekannten Felder.
7. Der Deploy führt neben dem Build auch die Site-Tests aus.
8. Die Deliberationsform 0.5 ist spezifiziert und hinter einem deaktivierten
   Schalter implementiert oder mindestens bis zur ausführungsreifen
   CC-Direktive vorbereitet. Innerhalb dieses Fensters findet **kein** scharfer
   0.5-Sitzungslauf statt.

Nicht Ziel dieses Zeitfensters sind eine Erweiterung auf fünf Ratssitze, ein
unvermessener Scout-Wechsel, eine visuelle Neugestaltung oder die pauschale
Abarbeitung aller Geschmacksbefunde.

---

## 4 · Reihenfolge und Zeitfenster

### Phase A — Auslieferung wiederherstellen (7.–10. August)

1. Der Steward liefert je Normal- und `-lo`-Variante:
   `claude-opus-5`, `gpt-5.6-sol`, `gemini-3.5-flash`.
2. CC integriert ausschließlich die sechs freigegebenen Assets.
3. Abnahme vor Push:
   - alle sechs erwarteten Pfade vorhanden;
   - Modellname bleibt neben bzw. am Medaillon sichtbar;
   - Desktop, Mobil, Reduced Motion und No-JS bleiben lesbar;
   - `npm test` und ein isolierter Produktions-Build grün;
   - Gremium-Suite und beide Schema-Tore grün;
   - keine Änderung unter bestehenden `sessions/**` oder `journal/**`.
4. FF-only auf `master` erst nach ausdrücklicher Freigabe. Push löst den
   Produktions-Deploy aus.
5. Live-Abnahme: Sitzung 4, vier Empfehlungen, 3-von-3-Zählstände,
   Konditional-Markierungen, Korrekturhinweis und Dossier-Verweigerung.

Wichtig: Auch ein reiner Docs-Push löst den Deploy aus. Deshalb werden die
untracked Übergaben und Entscheide erst nach Wiederherstellung des grünen Builds
auf `master` gebracht.

### Phase B — Quelle der Wahrheit reparieren (parallel, Abschluss bis 11. August)

- `AGENTS.md` auf den aktiven Betriebs-/0.4.1-Auftrag umstellen;
- veraltete Feature-Branch-Grenzen entfernen oder eindeutig archivieren;
- fehlende Wart-Entscheide in der freigegebenen Fassung versionieren;
- Übergaben committen; Long-Table-Ausführung als eigenen Auftrag behandeln;
- README-Aussagen über Räume, Verfahren und aktuelle Modellzahl korrigieren;
- aus der alten 0.4.1-Liste eine gegen Code und Git verifizierte Restliste
  herstellen.

Dies ist kein History-Rewrite. Alles wird in normalen Vorwärts-Commits
nachgetragen.

### Phase C — Betriebsfestigkeit 0.4.1 (11.–14. August)

CC erhält vier kleine, getrennt reviewbare Slices:

1. Journal-Typen und publizierbare Verweigerung;
2. P13 Medaillon-Auflösung mit neutralem Fallback;
3. P12, P7 und C5 als Maschinen-/Workflow-Härtung;
4. Build-Vertrag (`npm test` im Deploy, P9 und mechanische C7-Bereinigung).

Kein Sammelcommit. Jeder Slice besitzt eigene Tests, eigene Abnahme und ist
einzeln zurückdrehbar.

### Phase D — Deliberationsform 0.5 (17.–21. August)

1. Architekt liefert Zustandsmodell, Schema-Diff, Failure-Matrix,
   Kostenabschätzung und Testvektoren.
2. Wart liefert bzw. genehmigt den öffentlichen DE/EN-Verfahrenstext.
3. CC baut Orchestrator und Datenschema hinter einem standardmäßig
   ausgeschalteten Schalter.
4. CC ergänzt Darstellung und Protokoll-Explorer; bestehende Sitzungen bleiben
   unverändert renderbar.
5. Zuerst synthetischer Test, dann optional echter `dry_run`. Kein Commit eines
   Dry-Run-Rekords und kein scharfer Lauf.
6. `next-session.json` wird erst nach Steward-Entscheid mit einer Frage für
   Sitzung 5 aktualisiert, die zum vorhandenen Evidenzstand passt und echten
   Widerspruch herausfordert.

Der Wart-Cron vom 17. August wird wie der Lauf vom 10. August als eigenes
Betriebsgate geprüft, nicht mit einem Feature-Merge zeitlich überlagert.

---

## 5 · Konkrete Architekturvorschläge zur strukturellen Robustheit

### 5.1 P13 — Medaillons über aufgelöste Präsentationsdaten

**Problem:** Drei Svelte-Komponenten bilden den Asset-Pfad direkt aus
`track.model`. Eine neue Modell-ID erzeugt dadurch bereits beim Prerender einen
404-Abbruch.

**Vorschlag:**

- Eine einzige serverseitige Funktion löst `model_id → medallion asset` auf.
- Die Zuordnung liegt in einem kleinen Präsentationsregister, getrennt von der
  semantisch reicheren Bestell-Registratur `models.json`.
- Der Homepage-View-Model-Track enthält danach fertige Felder wie
  `medallion_lo` und optional `medallion_full`.
- Komponenten konstruieren niemals selbst einen Pfad aus einer Modell-ID.
- Für unbekannte oder noch nicht belieferte Modelle liefert der Resolver ein
  neutrales, namentlich unmarkiertes Standard-Medaillon.
- Der Modellname bleibt immer als echter Text neben dem Bild sichtbar; das
  Fallback darf keine fremde Modellidentität vortäuschen.
- Ein Build-Test speist eine unbekannte Modell-ID ein und verlangt einen
  erfolgreichen Prerender mit neutralem Fallback.
- Ein Register-Test prüft, dass jeder ausdrücklich eingetragene Asset-Pfad als
  Datei existiert.

Ein Browser-`onerror` reicht nicht: Der ursprünglich referenzierte 404-Pfad kann
bereits den statischen Prerender scheitern lassen. Die Entscheidung muss vor dem
Rendern fallen.

### 5.2 P12 — Key-Join statt Positionskopplung

**Problem:** Runde 2 verwendet `zip(config["models"], r1)`. Die Identität reist
heute zwar im Spec mit, aber die Korrektheit hängt unnötig an Reihenfolge und
Vollständigkeit zweier Listen.

**Vorschlag:**

- Nach Runde 1 wird `r1_by_model` über die stabile Modell-ID aufgebaut.
- Vor Runde 2 gilt ein hartes Invariant:
  - keine doppelte Modell-ID;
  - jede konfigurierte Modell-ID besitzt genau ein Erstvotum;
  - kein unbekanntes Erstvotum wird still übernommen.
- Runde 2 liest das eigene Votum ausschließlich über
  `r1_by_model[spec["model"]]`.
- Fehlende oder doppelte Identitäten führen vor dem nächsten API-Call zu einem
  klaren Abbruch; es wird nicht geraten und nicht positional zurückgefallen.
- Tests permutieren `r1`, prüfen die korrekte Eigenvotum-Zuordnung und erwarten
  bei fehlender bzw. doppelter ID einen lauten Fehler.

Dies ist zugleich die Grundlage für adressierte Erwiderungen in 0.5.

### 5.3 P7 — `schedule.json` erhalten statt neu erzeugen

**Problem:** `run_wart.write_schedule()` schreibt ein neues Objekt aus drei
Schlüsseln. Das erste zukünftige Feld würde still verschwinden.

**Vorschlag:**

- Eine gemeinsame Schedule-Hilfsfunktion lädt das bestehende Objekt, kopiert es
  und ändert ausschließlich die ausdrücklich verantworteten Felder.
- Normaler Research aktualisiert `next_research`, `last_journal` und – nur bei
  einem tatsächlich vorliegenden Einberufungsentscheid – `next_session`.
- Eine Modell-Verweigerung aktualisiert `next_research` und `last_journal`,
  lässt `next_session` aber byte-inhaltlich unverändert. Sie hat keine
  Einberufungsentscheidung erzeugt.
- Unbekannte Zusatzfelder werden in Tests eingebracht und müssen den Schreibweg
  unverändert überleben.
- Vor dem Commit läuft weiterhin das Schedule-Schema-Tor.

### 5.4 C5 — Eine gemeinsame Schreib-Concurrency

**Problem:** `wart.yml` und `session.yml` besitzen unterschiedliche
Concurrency-Gruppen, schreiben aber beide in den unveränderlichen Rekord und in
`schedule.json`.

**Vorschlag:**

- Beide Workflows verwenden repositoryweit dieselbe Gruppe, z. B.
  `noblecause-record-writer`.
- `cancel-in-progress: false` bleibt bestehen: Ein Rekordlauf wird nie zugunsten
  eines neueren Laufs abgebrochen.
- Preflight und Deploy bleiben getrennt, weil sie keinen Rekord schreiben.
- Test/Review prüft die Workflow-YAMLs statisch auf identische Gruppen.
- Bis zum Merge bleibt die bestehende Verhaltensregel gültig: kein manueller
  Dispatch des einen Laufs, während der andere laufen kann.

Die Serialisierung verhindert den bekannten Wart-/Sitzungs-Konflikt. Sie ersetzt
nicht die FF-only-Regel für menschliche Pushes.

### 5.5 Journal `kind` und Verweigerung

**Problem:** Das aktuelle Journal-Schema verlangt die vollständigen
Research-Felder einschließlich Boolean `convene`. Eine ausdrückliche
Modell-Verweigerung ist damit nicht wahrheitsgemäß darstellbar.

**Vorschlag:**

- Bestands-Einträge mit `schema_version: 1` validieren unverändert über einen
  Legacy-Zweig.
- Neue maschinengeschriebene Einträge verwenden `schema_version: 2` und ein
  Pflichtfeld `kind` mit zunächst `research | refusal`.
- `kind: research` verlangt den heutigen vollständigen Research-Vertrag und ein
  echtes Boolean `convene`.
- `kind: refusal` verlangt mindestens:
  - `date`, `session_ref`, `model`, `model_label`;
  - `search_queries` aus dem tatsächlich gelaufenen Tool-Verlauf;
  - `costs`, `actions_run_url`;
  - ein strukturiertes `refusal`-Objekt mit `stop_reason`, `at`,
    `raw_artifact` und dem vom Wart freigegebenen DE/EN-Vermerk.
- Ein Refusal-Eintrag besitzt **kein** `convene` und keine erfundene
  `convene_rationale`.
- Nur der explizite Provider-Zustand `stop_reason == "refusal"` wird als
  gültiger Refusal-Rekord publiziert. `max_tokens`, `pause_turn`, Parse-Fehler,
  Netzwerkfehler und unbekannte Stop-Gründe bleiben technische Fehler und
  brechen laut ab.
- Teiltext einer verweigerten Ausgabe wird nicht als Dossier übernommen. Die
  Rohantwort bleibt als Prüfmaterial erhalten.
- Ein gültiger Refusal-Pfad endet erfolgreich, damit Schema-Tor und Commit-Step
  laufen; der technische Fehlerpfad endet ungleich null.
- Journal-Index und Detailseite zeigen „Verweigerung“ statt
  „keine Einberufung“. Ein fehlendes `convene` darf im View-Model nicht zu
  `false` umgedeutet werden.

Lauf #6 wird nicht aus Erinnerung rekonstruiert. Er wird nur aus dem gesicherten
Rohartefakt und mit Wart-Wortlaut additiv publiziert.

### 5.6 Deploy-Vertrag

**Vorschlag:** Nach `npm ci` führt der Produktionsworkflow den gleichen
verifizierten Site-Testpfad wie lokal aus. Da `npm test` bereits über `pretest`
einen Produktions-Build erzeugt, kann es den bisherigen isolierten
`npm run build`-Schritt ersetzen oder der Skriptvertrag wird so aufgeteilt,
dass der Build nicht unnötig doppelt läuft. Entscheidend ist:

- Build und Tests sind beide deploy-blockierend;
- `pipefail` und `build.log` bleiben erhalten;
- der Fehler-Issue-Step erhält weiterhin den relevanten Logauszug;
- ein erfolgreicher Test hinterlässt das tatsächlich zu deployende
  `site/build/`.

---

## 6 · Vorschlag Deliberationsform 0.5

Die bestehende Runde 2 ist eine Gegenlese: Jedes Modell sieht die Erstvoten und
gibt danach ein Schlussvotum ab. Sie garantiert keine adressierte Behauptung und
keine Antwort des Adressaten. Mehr Sitze würden diese Eigenschaft nur skalieren.

Vorgeschlagene Form mit zunächst drei Modellen:

1. **Runde 1 — unabhängig:** unverändert; kein Modell kennt andere Voten.
2. **Erwiderung:** Jedes Modell wählt aus den fremden Erstvoten höchstens eine
   entscheidungsrelevante, überprüfbare Behauptung und adressiert sie über
   `target_model_id`. Erwartet werden `claim`, `challenge`, `why_decisive` und
   gegebenenfalls eine konkrete Belegfrage.
3. **Antwort und Schlussvotum:** Jedes Modell erhält die an seine ID gerichteten
   Erwiderungen, beantwortet sie einzeln und gibt erst danach das strukturierte
   Schlussvotum ab.
4. **Aggregation:** Nur die strukturierten Schlussvoten werden gezählt. Die
   Beratungsprosa beeinflusst den Zähler nie direkt.
5. **Ausfall:** Keine oder verweigerte Erwiderung wird markiert. Solange gültige
   Schlussvoten und ein wohlgeformter Rekord herstellbar sind, läuft die Sitzung
   weiter.
6. **Publikation:** Adressat, Behauptung, Erwiderung und Antwort erscheinen als
   eigene Schicht zwischen Erst- und Schlussvotum; Rohprompts und Rohantworten
   bleiben vollständig erhalten.

Der zusätzliche Council-Call erhöht den variablen Ratsanteil grob um bis zu
50 Prozent gegenüber zwei Council-Runden. Der Budgetdeckel muss deshalb vor dem
ersten Dry Run neu berechnet und zwischen den Runden geprüft werden.

Erfolgskriterium ist **nicht** mehr Konsens. Ein Dry Run gilt als erkenntnisreich,
wenn mindestens eine der folgenden Bewegungen nachweisbar wird:

- eine Tatsachenbehauptung wird korrigiert oder enger gefasst;
- eine Bedingung bzw. ein Kipptrigger wird präzisiert;
- ein Gegenargument wird mit benanntem Grund verworfen;
- ein Modell revidiert sein Votum aufgrund einer adressierten Erwiderung;
- ein Modell hält begründet fest und beantwortet den stärksten Einwand.

Vor dem ersten scharfen Lauf müssen Site und README wahrheitsgemäß zwischen
unabhängiger Runde 1, adressierter Erwiderung, Schlussvotum und deterministischer
Zählung unterscheiden.

---

## 7 · Arbeits- und Review-Modell

**Steward:** Freigaben, Medaillon-Assets, Sitzungsfrage, Sitz-/Scout-Entscheide,
Push- und Deploy-Freigabe.
**Wart:** Rekordsemantik, Kanon, DE/EN-Wortlaute und additive Rekordentscheide.
**Architekt (Codex):** Zustandsmodelle, CC-Direktiven, Abnahmekriterien,
Failure-Matrizen und unmittelbarer Review jedes Slices.
**CC:** Bauausführung und Erstverifikation.

Die Entwicklung bleibt standardmäßig bei CC. Der Architekt baut nicht parallel
dieselben Dateien, sondern hält den unabhängigen Gegencheck aufrecht. Falls CC an
einem klar abgegrenzten Slice festhängt, kann der Steward die Ausführung dieses
Slices ausdrücklich an den Architekten übertragen; der Review braucht dann eine
zusätzliche unabhängige Instanz.

Jeder CC-Slice liefert:

1. Ausgangscommit und vollständige Dateiliste;
2. knappen Invarianten-/Failure-Nachweis;
3. Diff ohne fremde oder historische Rekordänderungen;
4. konkrete Testbefehle und ungekürzte Ergebniszusammenfassung;
5. `git status` ohne unerklärte Änderungen;
6. keinen Push ohne ausdrückliche Freigabe.

Der Architekt reviewt nach jedem Slice, nicht erst am Ende eines Sammelbranches.

---

## 8 · Erbetene Antwort des Warts

Erbeten wird eine gebündelte Antwort zu den vier Punkten aus §1:

1. Journal-Semantik `research | refusal`: freigegeben / mit Auflagen / abgelehnt.
2. Wortlaut Lauf #6: DE und EN oder Angabe des noch fehlenden Rohmaterials.
3. Verfahrenstext 0.5: Wortlaut bzw. Kriterien für den Entwurf.
4. Fehlende Entscheiddateien: kanonische Fassungen und öffentliche/private
   Einordnung.

Technische Detailentscheidungen aus §5 brauchen keine Einzelabnahme des Warts,
sofern sie den hier beschriebenen Rekordvertrag nicht verändern.
