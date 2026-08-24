# CC-Review — Scout/Wart-Trennung und Ratsbesetzung

**Stand:** 24.08.2026
**Rolle:** CC prüft ausschließlich read-only. Keine Änderungen, keine echten API-Calls,
kein Staging, kein Commit, kein Push.

## Ziel des Slices

- `claude-opus-5` arbeitet ausschließlich als Scout, nicht als Ratsmitglied.
- Der Rat enthält je Familie genau das stärkste produktionsreife Modell:
  `claude-fable-5`, `gpt-5.6-sol`, `gemini-3.7-flash`.
- Der Wochenlauf ist zweistufig: Scout recherchiert; Wart entscheidet anschließend
  ausschließlich über die Einberufung.
- Das Sitzungsdossier kommt vom Scout; Eröffnung, Moderation und Kurzfassung bleiben
  beim Wart.
- Fehlende Medaillons erzeugen einen neutralen CSS-Platzhalter statt eines aus der
  Modell-ID konstruierten 404-Pfads.
- Bestehende Rekorde bleiben unverändert.

## Bitte gezielt prüfen

1. **Konfiguration:** `gremium/config.json`
   - Scout und Wart sind getrennte Modelle.
   - Opus steht nicht in `models`.
   - genau eine Ratsstimme je Familie; keine Preview-Kennung.

2. **Wochenlauf:** `gremium/run_wart.py`, `gremium/prompts.py`
   - Scout produziert Evidenzfelder, aber kein `convene`.
   - Wart erhält das Scout-Dossier und produziert nur `convene` plus Begründung.
   - Journal attribuiert Recherchemodell und Entscheidmodell getrennt.
   - Kosten beider Calls werden vollständig und ohne Doppelzählung erfasst.
   - Kein stiller Default oder Prosa-Raten bei Vertragsbruch/Refusal.

3. **Sitzungslauf:** `gremium/run_session.py`
   - Nur das Runde-0-Dossier nutzt `scout`.
   - Leitung, Moderation und Wart-Kurzfassung nutzen weiterhin `wart`.
   - Ratsvoten nutzen ausschließlich `config.models`.
   - Scout- und Wart-Kosten werden getrennt erfasst; Council-Fable wird nicht mit
     Wart-Fable verwechselt oder doppelt/gar nicht berechnet.
   - Historische Feldnamen wie `wart_dossier` dürfen aus Kompatibilitätsgründen bleiben,
     müssen in neuem Inhalt aber korrekt als Scout-Dossier attribuiert sein.

4. **Medaillon-Robustheit:** `site/src/lib/server/homepage.js`,
   `(rooms)/+layout.server.js` und die drei Council-Komponenten
   - Assetpfad kommt ausschließlich aus `models.json`/Registratur.
   - Fehlender Eintrag rendert eine neutrale Münze und niemals
     `/media/medallions/{model-id}-lo.avif`.
   - Vorhandene Medaillons und Modellnamen bleiben unverändert sichtbar.

5. **Grenzen:**
   - `sessions/**`, `journal/**`, `commissions/**`, `models.json`, `schedule.json` und
     `schema/**` müssen im Diff vollständig fehlen.
   - Die bereits vorher ungetrackten August-Übergabedokumente sind fremder Bestand und
     nicht Teil des Slices.

## Verifikation

Bitte selbst erneut ausführen:

```bash
gremium/.venv/bin/python -m pytest -p no:cacheprovider gremium/tests
gremium/.venv/bin/python gremium/schema_gate.py all
npm --prefix site test
git diff --check
```

Erwartung des Architekten: **93 Python-Tests**, **45 Site-Tests**, Schema-Tor grün,
Build grün; nur die zwei bekannten Svelte-Warnungen.

## Rückgabe

Kurzbericht mit:

- Urteil: grün / blockierend;
- nur konkrete Befunde mit Datei und Zeile;
- Testzahlen;
- Bestätigung, dass keine Datei verändert wurde;
- falls grün: ausdrückliche Aussage, ob Commit/Push und danach ein einmaliger manueller
  Wochenlauf verantwortbar sind.
