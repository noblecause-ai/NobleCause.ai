---
folio_import: v1
type: note
target: 02-durchbruch
id: fable-2026-07-24-klartext-freigabe
source: fable-session-claude-ai
created: 2026-07-24
title: "Klartext-Schicht: Freigabe-Protokoll (Bootstrap, drei Bestandssitzungen)"
tags: [noblecause, klartext, freigabe, wart, journal-nachtrag]
ref: klartext-entwurf-bestandssitzungen
---

# Klartext-Schicht — Freigabe-Protokoll (Bootstrap)

**Entwurf:** Opus (Claude, separate Rolle, Input-Grenze eingehalten: nur Rats-Wortlaut, keine wart_*-Artefakte, keine Kladde). **Freigabe:** interaktive Fable-Instanz **in deklarierter Vertretung des Wart-Amtes** (Bootstrap; ab Pipeline übernimmt der Amts-Wart). **Korrektur-Riegel angewandt:** Jede inhaltliche Korrektur zitiert die Wortlaut-Stelle, die sie wiederherstellt.

## Verifikationsbasis (ehrlich, dreistufig)
- **Sitzung 2 (2026-07b): vollverifiziert am Live-Rekord** (noblecause.ai/sessions/2026-07b/ — Schlussvoten-JSON, recommendations, Korrektur-Notiz vom 14.07. gelesen).
- **Sitzung 1 (2026-07): kreuzverifiziert über den S2-Rekord** (Befangenheits-Narrativ bestätigt C-Voten MIRI 1 / GovAI 2; Wart-Dossier bestätigt die A-Dreiteilung HKI/IGN/Evidence Action).
- **Sitzung 3 (2026-07c): auf Basis der Opus-Fundstellen.** ⚠ **Auflage vor Publikation:** Die Noble-Session prüft den S3-plain-Block einmal gegen `sessions/2026-07c/session.json` (Soll: A = HKI konditional 3/3 mit Vertagungsantrag · B = AMF 2/3, GPT-Vorbehalt innerhalb des Konsenses · C = NTI 3/3 · D = LEEP 3/3). 60 Sekunden; weicht etwas ab → zurück an mich, nicht stillschweigend fixen.

## Entscheide zu den zwei gemeldeten Befunden
**Befund 1 (S2, Säule A) — Entwurf folgt zu Recht den Voten; KEINE summary-Korrektur.** Live-Rekord: Opus HKI (0,6), GPT HKI (0,65), Gemini Pratham (0,85) ⇒ 2/3 HKI; `recommendations.A` = HKI, Konsens. Die widersprechende Kurzfassung ist durch die **publizierte Korrektur-Notiz vom 14.07.** bereits ausgewiesen („Kurzfassung und Dissens-Text stammen unverändert aus dem Originallauf und können der korrigierten Aggregation widersprechen"). Ein nachträgliches Umschreiben der summary wäre ein Eingriff in den Originallauf — genau das, was die Rekord-Politik verbietet. Der Klartext übersetzt das korrigierte Ergebnis; die Narbe bleibt sichtbar, wo sie ist.
**Befund 2 (S1, Säule C) — zur Kenntnis, keine Änderung.** Schlussvoten GovAI 2 / MIRI 1 = Konsens; die „fragmentiert"-Erzählung der summary beschreibt den Vor-Gegenlese-Zustand. Entwurf folgt Empfehlung — korrekt.

## Verdikte je Sitzung
**Sitzung 1:** `question` ✓ · `A: null` ✓ · `B` ✓ · `C` ✓ (das „sollen" hält die Epistemik ehrlich) · `D` ✓ · `dissent.A` → **K2 (Form)**.
**Sitzung 2:** `question` ✓ · `A` → **K1 (Inhalt)** · `B` ✓ · `C` ✓ (Weglassen des Enthaltungs-Prozessdetails ist zulässige Vereinfachung; Wortlaut ist einen Klick entfernt) · `D` ✓ (Weglassen der 2027-Kopplung als „Detail, kein Alltagsgrund" — getragen) · `dissent {}` ✓.
**Sitzung 3:** alle ✓ vorbehaltlich der S3-Auflage oben. Die Behandlung der Konditionalität in `A` („…der Rat will Letztere später erneut prüfen") ist vorbildlich — exakt die Zeile, die verhindert, dass HKI belastbarer klingt, als der Rat beschloss.

## Korrekturen (publizierter Diff, Entwurf → freigegeben)
**K1 — Sitzung 2, `recommendations.A` (Inhalt):**
- Entwurf: „…weil **Vitamin-A-Tropfen** für Kinder pro Euro eine besonders gut belegte Wirkung haben."
- Freigegeben: „…weil **Vitamin-A-Gaben** für Kinder pro Euro eine besonders gut belegte Wirkung haben."
- Wortlaut-Zitat: `recommendations.A.title` = „Vitamin-A-Supplementierung (VAS)". „Tropfen" ist eine nicht belegte Konkretisierung der Darreichungsform — klein, aber genau die Kategorie, die der Riegel fangen soll.
**K2 — Sitzung 1, `dissent.A` (Form, kein Inhalt):**
- Entwurf: „keine Einigung — **die Modelle waren uneins, ob** Kindergesundheit, Salz mit Jod oder bessere Schulbildung die stärkste Zukunftsinvestition ist."
- Freigegeben: „keine Einigung — **ob** Kindergesundheit, Salz mit Jod oder bessere Schulbildung die stärkste Zukunftsinvestition ist."
- Grund: Dopplung („keine Einigung" + „uneins") gegen die Spec-Form; kein Inhaltseingriff, daher ohne Wortlaut-Zitat zulässig, als Form-Korrektur deklariert.

## Freigegebene Blöcke (final, für Kimi/Frontend)
```jsonc
// sessions/2026-07/session.json
"plain": {
  "question": "Wo bringt je 1.000 Euro Spende 2026 in jedem der vier Bereiche die größte Wirkung?",
  "recommendations": {
    "A": null,
    "B": "Leid lindern → Malaria Consortium, weil Medikamente Kinder in der Malaria-Hochsaison nachweislich günstig vor Erkrankung schützen.",
    "C": "Große Gefahren → Centre for the Governance of AI, weil klare Regeln für fortgeschrittene KI großen künftigen Schaden verhindern sollen.",
    "D": "Was sonst übersehen wird → Lead Exposure Elimination Project, weil strengere Regeln gegen Blei in Farben Kinder vor Vergiftung schützen."
  },
  "dissent": {
    "A": "keine Einigung — ob Kindergesundheit, Salz mit Jod oder bessere Schulbildung die stärkste Zukunftsinvestition ist."
  }
}
```
```jsonc
// sessions/2026-07b/session.json
"plain": {
  "question": "Halten die vier Empfehlungen aus der ersten Sitzung der aktuellen Beleglage stand?",
  "recommendations": {
    "A": "Zukunft → Helen Keller International, weil Vitamin-A-Gaben für Kinder pro Euro eine besonders gut belegte Wirkung haben.",
    "B": "Leid lindern → Malaria Consortium, weil Medikamente Kinder in der Malaria-Hochsaison nachweislich günstig vor Erkrankung schützen.",
    "C": "Große Gefahren → Nuclear Threat Initiative, weil Vorsorge gegen Pandemien und Biogefahren großen künftigen Schaden abwenden kann.",
    "D": "Was sonst übersehen wird → Lead Exposure Elimination Project, weil strengere Regeln gegen Blei in Farben Kinder vor Vergiftung schützen."
  },
  "dissent": {}
}
```
```jsonc
// sessions/2026-07c/session.json — vorbehaltlich 60-Sekunden-Check (Auflage oben)
"plain": {
  "question": "Bereich Zukunft: Ist Kindergesundheit (Helen Keller) oder Bildung (Pratham/TaRL) besser belegt?",
  "recommendations": {
    "A": "Zukunft → Helen Keller International, weil ihre Wirkung besser belegt ist als die der geprüften Bildungs-Alternative; der Rat will Letztere später erneut prüfen.",
    "B": "Leid lindern → Against Malaria Foundation, weil imprägnierte Moskitonetze Malaria besonders günstig verhindern.",
    "C": "Große Gefahren → Nuclear Threat Initiative, weil Vorsorge gegen Pandemien und Biogefahren großen künftigen Schaden abwenden kann.",
    "D": "Was sonst übersehen wird → Lead Exposure Elimination Project, weil Regeln gegen Blei in Farben Kinder vor bleibenden Schäden schützen."
  },
  "dissent": {}
}
```

## Journal-Nachtrag (Publikationsauftrag an die Noble-Session)
Eintrag „Klartext-Schicht, rückwirkend (Bootstrap)": Verweis aufs Regelwerk · beide Deklarationen (Entwurf Opus wortlaut-only / Freigabe Fable-Instanz in Vertretung des Wart-Amtes) · dieses Protokoll verlinkt · die zwei Diffs K1/K2 sichtbar (der fast leere Diff ist selbst der Beleg, dass die Freigabe geprüft und nicht durchgewinkt hat) · Befund-Entscheide inkl. Begründung, warum die summary NICHT angefasst wird · Integrations-Hinweise aus dem Entwurf (Label-Dopplung, „keine Einigung"-Präfix) an Kimi weiterreichen. EN-Klartext folgt als eigener Nachtrag; bis dahin DE-Fallback mit Sprachhinweis.
