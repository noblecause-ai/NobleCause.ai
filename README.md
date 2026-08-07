# NobleCause.ai

Drei AI-Modelle verschiedener Familien prüfen nach vier Kanons (Evidenz,
Unparteilichkeit, Demut, Transparenz), wo zusätzliche Ressourcen voraussichtlich
am meisten bewirken. Jede Sitzung wird vollständig veröffentlicht — Prompts,
Einzelvoten mit Konfidenzen, Gegenlese, Empfehlungen, Korrekturen und Kosten.

**Live:** https://noblecause.ai · **Verfassung:** [manifest.md](manifest.md) ·
**Governance:** [GOVERNANCE.md](GOVERNANCE.md)

## Architektur in einem Satz

Das Produkt ist der veröffentlichte Beratungsrekord, nicht eine Plattform: Eine
Sitzung ist ein Batch-Lauf, git ist die Datenbank, die Website ist statisch.

```
manifest.md          Gründungsdokument (wörtlich, CC BY 4.0)
sessions/            Sitzungsprotokolle, 1 Ordner pro Sitzung (Schema: sessions/README.md)
journal/             wöchentlicher Research- und Betriebsrekord
commissions/         getrennte Modellbestellungen, z. B. für Medaillons
site/                drei statische Räume + Protokoll-Explorer (SvelteKit adapter-static)
gremium/             Python-Maschine, deterministischer Orchestrator, 3 Modellfamilien
.github/workflows/   Push auf master = Build + Deploy auf den VPS
```

## Aktuelles Verfahren

Jedes Modell stimmt zunächst unabhängig ab. In Runde 2 liest es die Erstvoten
der anderen Modelle und darf sein Urteil ändern. Gezählt werden ausschließlich
die strukturierten Schlussvoten; Organisationsidentität kommt aus
`organizations.json`. Das heutige Verfahren ist eine Gegenlese mit
deterministischer Zählung, noch keine verpflichtend adressierte Erwiderung.
Diese erweiterte Deliberationsform ist als Version 0.5 geplant und wird vor
einem echten Lauf zunächst ausgeschaltet und synthetisch getestet.

Die Site inszeniert den Rekord als The Study, The Council und The Archive
(Deutsch: `/`, `/ratssaal/`, `/archiv/`; Englisch unter `/en/`).
Rekordprosa bleibt auch auf der englischen Site in ihrer Originalsprache.

## Bewusst nicht vorhanden

Kein Backend, keine Datenbank, kein Docker, kein Login, keine Kommentare,
kein Newsletter — und vor allem: **keine Spendenannahme**. Empfehlungen
verlinken auf die offiziellen Spendenwege der Organisationen; durch dieses
System fließt kein Geld.

## Einen Lauf durchführen

```bash
cd gremium && make session   # Details: gremium/README.md
```

Das Ergebnis landet als `sessions/YYYY-MM/` im Repo; nach Prüfung, Commit und
Push rendert die Site es automatisch. Ein wöchentlicher Wart-Research läuft
getrennt und schreibt nach `journal/`.

Für Wart-Leitung bei einer Sitzung steht `--led-by-wart` bereit (impliziert
`--with-dossier`): Eröffnung, Runde-0-Dossier, Moderationsnotiz und
Kurzfassung laufen dann über Fable.

Zusätzlich läuft der Wart-Research wöchentlich per GitHub Actions
(`.github/workflows/wart.yml`) und publiziert Einträge unter `journal/`.

## Lizenzen

Code MIT ([LICENSE](LICENSE)), Inhalte/Protokolle CC BY 4.0
([LICENSE-CONTENT.md](LICENSE-CONTENT.md)).

## Historie

Der 2024/25-Stack (FastAPI, Postgres, ChromaDB, Docker, OpenRouter) ist auf dem
Branch [`legacy-2025`](https://github.com/noblecause-ai/NobleCause.ai/tree/legacy-2025)
archiviert. Der Neuaufbau (2026-07) folgt der Architektur-Entscheidung:
radikale Transparenz statt Plattform.
