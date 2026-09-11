# NobleCause.ai — Architektur-Umsetzung zur Abnahme

Stand: 7. September 2026
Arbeitszweig: `codex/nc-next-phase-20260907`
Aktuelle Basis: `origin/master` bei `de50cfd`
Status: Slice A veröffentlicht; Slice B nach Wart-Review nachgebessert und lokal
geprüft, nicht gestaged, nicht committet, nicht gepusht

## Abnahmevorschlag: zwei getrennte Slices

### Slice A — verständlicher Einstieg

Der interne Hinweis „Klartext folgt …“ beziehungsweise „Plain-language version
pending …“ ist aus Study und Archive entfernt. Fehlt die optionale
Klartext-Schicht, bleibt der bereits veröffentlichte Rekordtext sichtbar, ohne
den Besucher mit dem Freigabeprozess zu belasten.

Nur The Study erhält zusätzlich einen unmittelbaren Einstieg:

> NobleCause.ai lässt mehrere KI-Modelle dieselbe Spendenfrage prüfen und
> veröffentlicht ihre Antworten vollständig. Ein festes Programm zählt nur
> ihre Schlussvoten. NobleCause nimmt kein Geld an; Spendenlinks führen direkt
> zu den Organisationen.

Die englische Fassung ist inhaltlich gleich. Council und Archive behalten ihren
bisherigen, raumspezifischen Kopf. Es gibt keine neue Route und keine parallele
Darstellung.

Betroffene Pfade:

- `site/src/lib/components/rooms/StudyRoom.svelte`
- `site/src/lib/components/rooms/ArchiveRoom.svelte`
- `site/src/lib/i18n/de.js`
- `site/src/lib/i18n/en.js`
- `site/src/lib/server/homepage.js`
- `site/tests/homepage-build.test.js`

Dieser Slice wurde als Commit `de50cfd` unabhängig von Slice B veröffentlicht.
Der GitHub-Deploy `34216159718` war grün; die deutsche und englische Live-Seite
wurden danach direkt geprüft.

### Slice B — Prozess 0.5 und zwei Scouts, beide AUS

Die bereits entschiedenen Verfahrensformen sind implementiert, aber in
`gremium/config.json` ausdrücklich deaktiviert:

```json
"features": {
  "two_scouts": { "enabled": false },
  "deliberation_0_5": { "enabled": false }
}
```

Zwei Scouts:

- genau zwei Modelle aus verschiedenen Familien;
- mindestens eine Familie ausserhalb des Rates;
- identischer Auftrag, getrennte Rohpfade und Berichte;
- exakter, als solcher beschrifteter Divergenzausweis im Wochenlauf;
- ein Ausfall bleibt sichtbar und kann durch den zweiten Bericht aufgefangen
  werden; verweigern beide Scouts explizit, entsteht ein Refusal-Journal ohne
  Einberufungsentscheid; technische Doppelausfälle bleiben laute Fehler;
- kein neuer Provider wurde gewählt oder angebunden. Eine versehentliche
  Aktivierung mit einer nicht unterstützten Familie bricht vor Verzeichnis und
  API-Call laut ab.

Deliberation 0.5:

- unabhängige Erstvoten bleiben unverändert;
- jedes Ratsmodell muss genau eine überprüfbare Position eines anderen Modells
  adressieren; `support | dispute | refine` hält fest, ob es die Position
  stützt, bestreitet oder präzisiert; eine Enthaltung gibt es nicht;
- nur gültige, exakt adressierte Erwiderungen werden dem Zielmodell zugestellt;
- ungültige Antworten und technische Ausfälle bleiben im Rekord sichtbar;
- jedes Ziel beantwortet seine Erwiderungen vor dem Schlussvotum;
- nur strukturierte Schlussvoten gelangen in die bestehende deterministische
  Aggregation.

Die Sitzungsansicht kann gültige Erwiderungen samt Haltung und Ausfälle
darstellen. Bestehende Sitzungen und Journale wurden nicht verändert. Vor der
ersten echten Aktivierung fehlen weiterhin Providerentscheid, Adapter,
Kostenfreigabe, synthetische Endabnahme und die bereits entschiedene öffentliche
DE/EN-Verfahrenserklärung.

Betroffene Pfade:

- `gremium/config.json`
- `gremium/process_config.py`
- `gremium/prompts.py`
- `gremium/run_session.py`
- `gremium/run_wart.py`
- `gremium/README.md`
- `gremium/tests/test_process_config.py`
- `gremium/tests/test_deliberation_05.py`
- `gremium/tests/test_wart_role_pipeline.py`
- `schema/journal.schema.json`
- `schema/session.schema.json`
- `site/src/lib/components/rooms/StudyActors.svelte`
- `site/src/lib/i18n/de.js`
- `site/src/lib/i18n/en.js`
- `site/src/lib/server/content.js`
- `site/src/routes/(rooms)/+layout.server.js`
- `site/src/routes/journal/+page.svelte`
- `site/src/routes/journal/[id]/+page.svelte`
- `site/src/routes/sitzungen/[id]/+page.server.js`
- `site/src/routes/sitzungen/[id]/+page.svelte`

## Modell- und Scout-Recherche

Der aktuelle, nur aus offiziellen Anbieterquellen hergeleitete Vergleich liegt
in `docs/modell-und-scout-recherche-2026-09-07.md`. Er trennt Ratsstärke von
Scout-Eignung und trifft noch keine Sitzentscheidung.

Die acht bestehenden Vergleichsanfragen wurden aus
`journal/2026-07-08c/entry.json` übernommen. Es gab keine bezahlten
Generations- oder Suchläufe. Grok 4.6 ist ein sinnvoller externer
Scout-Kandidat für den später gesondert zu genehmigenden Vergleich; das ist
keine Vorentscheidung für den Sitz.

## Entscheidquellen

Die drei vom Wart für den gemeinsamen Slice-B-Commit verlangten kanonischen
Dateien liegen nun mit dem Bau vor:

- `docs/wart-entscheid-deliberationsform-2026-08-06.md`
- `docs/wart-entscheid-sichtbarkeit-prozessmaterial-2026-08-04.md`
- `docs/claude/noblecause-einstiegskonzept-2026-08-02.md`

Deliberationsentscheid und Einstiegskonzept wurden wörtlich aus dem
claude.ai-Projekt `noblecause.ai` übernommen; der Sichtbarkeitsentscheid aus
dem lokalen Meta-Bestand wurde bytegleich übernommen. Der öffentliche
DE/EN-Verfahrenstext liegt zusätzlich in
`docs/wart-antwort-architekturplan-2026-08-07.md` vor.

## Prüfung

- Python: **103/103** Tests grün.
- Schema-Tor: **4/4** Sitzungen und **14/14** Journale gültig.
- Site: **45/45** Tests grün, statischer Build erfolgreich.
- `git diff --check`: sauber.
- Lokale Sichtprüfung von `/`: neuer Einstieg sichtbar; „Klartext folgt“ nicht
  vorhanden.
- Bekannte, unveränderte Build-Warnungen: `CouncilRoom.svelte` (`orgEn`) und
  `StageHero.svelte` (`passage`).

## Noch beim Owner

1. Den nachgebesserten Slice B vom Wart voll abnehmen lassen; ausgeschaltet lassen.
2. Den bezahlten Acht-Fragen-Vergleich mit exaktem Kostenrahmen separat
   freigeben.
3. Danach die zwei Scout-Sitze wählen und erst dann den zweiten Provideradapter
   bauen.
4. Deliberation 0.5 erst nach öffentlicher Verfahrenserklärung und einer
   ausdrücklich freigegebenen Probesitzung aktivieren.
5. Eine Erweiterung des Rates bleibt eine eigene Owner-Entscheidung.

Der Aion-Lumen-Blogentwurf wurde nicht verändert: Er liegt ausserhalb der für
diese Sitzung gesetzten NobleCause-Grenze und braucht eine eigene ausdrückliche
Schreibfreigabe.
