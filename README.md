# NobleCause.ai

Ein ständiges Gremium von AI-Modellen deliberiert nach vier Kanons (Evidenz,
Unparteilichkeit, Demut, Transparenz) über die wirksamste Ressourcen-Allokation
für das Gedeihen der Menschheit. Jede Sitzung wird vollständig veröffentlicht —
Prompts, Einzelvoten mit Konfidenzen, Dissens, Empfehlungen und Kosten.

**Live:** https://noblecause.ai · **Verfassung:** [manifest.md](manifest.md) ·
**Governance:** [GOVERNANCE.md](GOVERNANCE.md)

## Architektur in einem Satz

Das Produkt ist die veröffentlichte Deliberation, nicht eine Plattform: Eine
Sitzung ist ein Batch-Lauf, git ist die Datenbank, die Website ist statisch.

```
manifest.md          Gründungsdokument (wörtlich, CC BY 4.0)
sessions/            Deliberations-Protokolle, 1 Ordner pro Sitzung (Schema: sessions/README.md)
site/                statische Website (SvelteKit adapter-static), rendert manifest + sessions zur Build-Zeit
gremium/             Deliberations-Pipeline (Python, deterministischer Orchestrator, 3 Modellfamilien)
.github/workflows/   Push auf master = Build + Deploy auf den VPS
```

## Bewusst nicht vorhanden

Kein Backend, keine Datenbank, kein Docker, kein Login, keine Kommentare,
kein Newsletter — und vor allem: **keine Spendenannahme**. Empfehlungen
verlinken auf die offiziellen Spendenwege der Organisationen; durch dieses
System fließt kein Geld.

## Eine Sitzung durchführen

```bash
cd gremium && make session   # Details: gremium/README.md
```

Das Ergebnis landet als `sessions/YYYY-MM/` im Repo; nach Commit + Push
rendert die Site es automatisch.

## Lizenzen

Code MIT ([LICENSE](LICENSE)), Inhalte/Protokolle CC BY 4.0
([LICENSE-CONTENT.md](LICENSE-CONTENT.md)).

## Historie

Der 2024/25-Stack (FastAPI, Postgres, ChromaDB, Docker, OpenRouter) ist auf dem
Branch [`legacy-2025`](https://github.com/noblecause-ai/NobleCause.ai/tree/legacy-2025)
archiviert. Der Neuaufbau (2026-07) folgt der Architektur-Entscheidung:
radikale Transparenz statt Plattform.
