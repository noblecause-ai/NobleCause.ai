# AGENTS.md — Regeln für Agenten in diesem Repo

Dieses Dokument gilt für **jeden** Agenten (Codex, Claude Code, …), der in diesem
Repository arbeitet. Es wird von Codex automatisch gelesen.

## Aktueller Vorgang: Immersive-Homepage-Neubau
Gearbeitet wird auf **`feat/immersive-homepage`** (Basis: `sol/nachbesserung`, #12 — trägt
Datenvertrag, Plates, Schema, `organizations.json` mit `beschreibung` und beide Sitzungen,
**ohne** das verworfene Kartenstapel-Design aus #14/#15).

Diese Arbeit ist **Präsentation** — nur wie die vorhandenen Daten dargestellt werden.

## Experiment: `feat/council-rooms` (Kimi, Wegwerf)
Isolierter Versuch, die UI-Architektur der Startseite von „ein langer Scroll über acht
Szenen" auf **drei diskrete Räume** (Vorzimmer → Ratssaal → Archiv) umzubauen. **Nur die
Präsentation** wird ersetzt; die **verifizierte Datenschicht** (`site/src/lib/server/
content.js` + `homepage.js` — liest `recommendations`/`convergence`, **aggregiert nie neu**)
und die **Embleme** werden geerbt, nicht angefasst. Der genaue Auftrag steht in
**`docs/council-rooms-brief.md`** (bitte zuerst lesen). Es gelten dieselbe harte Grenze und
dieselben Sauberkeits-Regeln wie unten. Wegwerf: scheitert der Versuch, wird der Branch
gelöscht; `master` und `feat/immersive-homepage` bleiben unberührt.

## HARTE GRENZE — diese Pfade werden NICHT angefasst
Ändere, lösche oder verschiebe **nichts** unter:
- `sessions/**` (publizierte Sitzungstexte)
- `journal/**`
- `schedule.json`
- `gremium/**` (Aggregation, Backend, Läufe)
- `schema/**` (Datenvertrag — nur lesen)
- `prompts.py` / `**/prompts.py`

Wenn eine Aufgabe eine Änderung dort zu verlangen scheint: **sofort stoppen und melden**,
nicht umgehen. Ein `pre-commit`-Hook blockt Commits, die diese Pfade berühren.

Erlaubt ist ausschließlich die **Präsentationsebene**: neue/rendernde Dateien für die
Startseite (z. B. unter `sol-build/`, `site/`, statische Assets), Build-/Render-Skripte der
Darstellung, Styles. Die Datenfundamente werden nur **gelesen**:
`schema/session.schema.json`, `organizations.json`, `sessions/2026-07c` (Konsens),
`sessions/2026-07` (Nicht-Konsens), Plates `sol-build/site/static/{ratssaal,vorraum}.png`.

## Sauberkeits-Regeln
- **NIE Push auf `master`. NIE Merge ohne ausdrückliche Freigabe.** Bis zum Merge auf
  master ist nichts live; Deploy passiert erst beim Merge.
- Im Feature-Branch darf frei committet werden (lokal ruhig unsauber). **Bevor** irgendetwas
  zu GitHub/master geht, werden die Commits zu **sauberen Einheiten gesquasht** — die
  Historie wird nicht beschmutzt.
- **Review läuft lokal** (statischer Server aus einem Render-Verzeichnis), **nicht** über
  einen Merge. Aus echten Daten rendern, nicht aus Sample-HTML.
- Kein Netzzugriff nach außen ohne Nachfrage.

## Datenvertrag
Der Renderer PARST KEINE PROSA. Strukturierte Felder kommen aus `session.json`
(`recommendations`, `rounds[].votes[].recommendations[]`) und `organizations.json`
(`beschreibung`, `donation_url`); Abweichungen sind in `sol-build/data-contract.md`
dokumentiert. Kein erfundenes „Warum", keine LLM-Aggregation in der Darstellung.
