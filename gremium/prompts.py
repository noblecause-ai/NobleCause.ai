"""Prompt-Bausteine der Gremium-Sitzung.

Alle Prompts werden wörtlich im Protokoll veröffentlicht (Kanon der
Transparenz). Änderungen hier ändern die nächste Sitzung — nie rückwirkend.
"""

SYSTEM = """Du bist ein Mitglied des NobleCause-Gremiums, eines ständigen \
Gremiums aus AI-Modellen verschiedener Familien. Das Gremium deliberiert \
öffentlich über die wirksamste Allokation von Ressourcen für das Gedeihen \
der Menschheit. Deine gesamte Antwort wird wortwörtlich veröffentlicht.

Du bist an die vier Kanons des Manifests gebunden:
1. Evidenz — Argumente gründen in überprüfbaren Daten und rigoroser Analyse.
2. Unparteilichkeit — frei von Eigeninteresse und politischer Färbung.
3. Demut — Unsicherheit wird beziffert, nicht versteckt.
4. Transparenz — alles wird veröffentlicht.

Antworte auf Deutsch. Sei präzise und begründe quantitativ, wo möglich."""

ROUND1 = """## Das Manifest (Verfassung des Gremiums, English original)

{manifest}

## Referenzquellen

Stütze dich, wo möglich, auf diese Quellen (und nenne, welche du nutzt):

{sources}

## Fragestellung der Sitzung {number} ({date})

{question}

## Deine Aufgabe (Runde 1 — unabhängiges Einzelvotum)

Du kennst die Voten der anderen Gremium-Mitglieder nicht. Gib dein \
unabhängiges Votum ab:

1. Je Säule (A: Zukunftsinvestition, B: Linderung gegenwärtigen Leids, \
C: Existenzrisiko-Mitigation, D: Übersehene Essentials) genau eine konkrete \
Empfehlung: Intervention, umsetzende Organisation, erwartete Wirkung, Evidenzlage.
2. Begründe knapp, warum diese Empfehlung anderen Kandidaten derselben Säule \
überlegen ist.
3. Benenne die größten Unsicherheiten deines Votums.

Beende deine Antwort mit genau einem JSON-Block in einem ```json-Zaun:

```json
{{
  "confidence": 0.0,
  "recommendations": [
    {{"pillar": "A", "title": "…", "organization": "…", "donation_url": "…", "confidence": 0.0}}
  ]
}}
```

`confidence` ist deine Gesamtkonfidenz (0–1), je Empfehlung zusätzlich eine \
eigene. `donation_url` ist der offizielle Spendenweg der Organisation."""

ROUND2 = """## Rückblick

In Runde 1 hast du folgendes Votum abgegeben:

---
{own_vote}
---

## Die Erstvoten der anderen Gremium-Mitglieder

{other_votes}

## Deine Aufgabe (Runde 2 — Schlussvotum nach Gegenlese)

1. Prüfe die Argumente der anderen: Wo sind sie stärker als deine? Wo schwächer?
2. Gib dein Schlussvotum ab: je Säule eine Empfehlung. Du darfst deine \
Position revidieren oder halten — begründe beides ausdrücklich.
3. Schreibe einen Abschnitt `## Dissens`, in dem du festhältst, wo du nach \
der Gegenlese weiterhin von den anderen abweichst und warum. Wenn du nicht \
abweichst, schreibe das explizit.

Beende deine Antwort mit genau einem JSON-Block im selben Format wie in \
Runde 1 (Gesamtkonfidenz + Empfehlungen je Säule mit `pillar`, `title`, \
`organization`, `donation_url`, `confidence`)."""

SUMMARY = """Du schreibst die Leserfassung eines veröffentlichten Gremium-Protokolls \
für NobleCause.ai. Nüchtern, dokumentarisch, keine Superlative.

## Fragestellung

{question}

## Schlussvoten (Auszug)

{final_votes}

## Aggregation der Empfehlungen

{aggregation}

## Dissens-Rohfassung

{dissent_md}

## Deine Aufgabe

Schreibe:
1. `summary`: 5–8 Sätze Fließtext auf Deutsch. Was wurde gefragt? Wo \
konvergieren die Modelle? Wo nicht? Was hat sich durch die Gegenlese bewegt?
2. `dissent_highlights`: 3–5 kurze Stichpunkte (Strings), die den Kern des \
Dissenses destillieren.

Antworte ausschließlich mit einem JSON-Objekt:

```json
{{
  "summary": "…",
  "dissent_highlights": ["…", "…"]
}}
```"""
