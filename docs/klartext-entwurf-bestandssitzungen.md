# Klartext-Entwurf — drei Bestandssitzungen (Bootstrap, DE)

**Rolle:** Entwurf durch Opus. **Keine Entscheidung, keine Zeichnung** — Freigabe getrennt
durch die Wart-Vertretung, publizierter Diff.
**Input-Grenze eingehalten:** gelesen wurden je Sitzung ausschließlich `summary`,
`recommendations` und die `final_vote`-Einzelvoten (+ `question`/`title`). **Nicht gelesen:**
`wart_dossier`, `wart_opening`, `wart_moderation`, Kladde, Journal. Die `wart_*`-Runden
wurden gezielt übersprungen.
**Sprache:** DE. EN folgt als eigener Nachtrag.

---

## ⚠ Zwei Befunde für die Freigabe (Entwerfer darf sie nicht auflösen)

**Befund 1 — Sitzung 2 (2026-07b), Säule A: Zusammenfassung widerspricht den Schlussvoten.**
Die `summary` sagt, A sei ungelöst geblieben — „Opus hält an HKI fest, während GPT und
Gemini Pro sich für Pratham/TaRL aussprechen". Die `final_vote`-Einzelvoten zeigen aber:
**Opus = HKI, GPT = HKI, Gemini = Pratham** — also 2 von 3 für HKI, und `recommendations.A`
= Konsens HKI. **GPTs Schlussvotum ist HKI, nicht Pratham.** Ich habe A nach Voten und
Empfehlung entworfen (Konsens HKI). Die Zusammenfassung ist an dieser Stelle unzutreffend —
die Wart-Vertretung muss entscheiden, ob der `summary`-Text korrigiert wird.

**Befund 2 — Sitzung 1 (2026-07), Säule C: Zusammenfassung nennt C „fragmentiert", Voten sind es nicht.**
Die `summary` beschreibt C als Spaltung (MIRI/GovAI/NTI). Die Schlussvoten zeigen
**GovAI 2, MIRI 1** → Konsens GovAI, wie `recommendations.C`. Ich habe C als Konsens GovAI
entworfen (die Fragmentierung war der Anfangszustand vor der Gegenlese). Kein Widerspruch zur
Empfehlung, nur zur erzählenden Zusammenfassung — zur Kenntnis.

---

## Sitzung 1 · 2026-07 · Nr. 1 (Eröffnungsfrage)

```json
"plain": {
  "question": "Wo bringt je 1.000 Euro Spende 2026 in jedem der vier Bereiche die größte Wirkung?",
  "recommendations": {
    "A": null,
    "B": "Leid lindern → Malaria Consortium, weil Medikamente Kinder in der Malaria-Hochsaison nachweislich günstig vor Erkrankung schützen.",
    "C": "Große Gefahren → Centre for the Governance of AI, weil klare Regeln für fortgeschrittene KI großen künftigen Schaden verhindern sollen.",
    "D": "Was sonst übersehen wird → Lead Exposure Elimination Project, weil strengere Regeln gegen Blei in Farben Kinder vor Vergiftung schützen."
  },
  "dissent": {
    "A": "keine Einigung — die Modelle waren uneins, ob Kindergesundheit, Salz mit Jod oder bessere Schulbildung die stärkste Zukunftsinvestition ist."
  }
}
```

**Fundstellen**
- `question` → `question`/`summary` („drei Interventionen pro 1'000 EUR mit höchster erwartbarer Wirkung je Säule").
- `A` = `null` → `recommendations.A` (`has_consensus:false`); Voten HKI / Iodine / Evidence Action (3-fach gespalten).
- `dissent.A` → `summary` („spaltet sich zwischen Vitamin-A-Supplementierung, Salzjodierung und Teaching at the Right Level") + Voten (Kindergesundheit / Salz-Jod / Schulbildung).
- `B` → `recommendations.B` („Saisonale Malaria-Chemoprophylaxe (SMC)", Malaria Consortium); `summary` („weitgehenden Konsens … robuste Evidenz").
- `C` → `recommendations.C` („Förderung von Standards und Governance für fortgeschrittene KI-Systeme", GovAI); Schlussvoten GovAI 2/3.
- `D` → `recommendations.D` („Bekämpfung der Bleivergiftung durch politische und regulatorische Maßnahmen", LEEP).

---

## Sitzung 2 · 2026-07b · Nr. 2 (Evidenzprüfung)

```json
"plain": {
  "question": "Halten die vier Empfehlungen aus der ersten Sitzung der aktuellen Beleglage stand?",
  "recommendations": {
    "A": "Zukunft → Helen Keller International, weil Vitamin-A-Tropfen für Kinder pro Euro eine besonders gut belegte Wirkung haben.",
    "B": "Leid lindern → Malaria Consortium, weil Medikamente Kinder in der Malaria-Hochsaison nachweislich günstig vor Erkrankung schützen.",
    "C": "Große Gefahren → Nuclear Threat Initiative, weil Vorsorge gegen Pandemien und Biogefahren großen künftigen Schaden abwenden kann.",
    "D": "Was sonst übersehen wird → Lead Exposure Elimination Project, weil strengere Regeln gegen Blei in Farben Kinder vor Vergiftung schützen."
  },
  "dissent": {}
}
```

**Fundstellen**
- `question` → `question` („Halten die vier Empfehlungen aus Sitzung 1 einer aktuellen Evidenzprüfung stand?").
- `A` → `recommendations.A` („Vitamin-A-Supplementierung (VAS)", HKI, `has_consensus:true`); Schlussvoten HKI 2/3. **Siehe Befund 1.**
- `B` → `recommendations.B` (Malaria Consortium, Konsens 3/3).
- `C` → `recommendations.C` („Biosecurity & Pandemie-Vorsorge", NTI, Konsens 3/3).
- `D` → `recommendations.D` (LEEP, Konsens 3/3). *(Die Auszahlungs-Kopplung „2027+" aus dem Empfehlungstitel bewusst weggelassen — Detail, kein Alltagsgrund.)*
- `dissent` = `{}` → alle vier `has_consensus:true`.

---

## Sitzung 3 · 2026-07c · Nr. 3 (Auflösung Säule-A-Dissens)

```json
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

**Fundstellen**
- `question` → `question` („HKI oder Pratham/TaRL Africa — was sagt die aktuelle Evidenz?").
- `A` → `recommendations.A` („… konditional, mit Vertagungsantrag zugunsten erneuter TaRL-Prüfung", HKI, Konsens 3/3); `summary` („Alle drei Modelle empfehlen HKI … erneute Prüfung von TaRL Africa … wird gremiumsweit unterstützt"). Die Konditionalität/Vertagung ist im Satz gehalten.
- `B` → `recommendations.B` („Insektizidbehandelte Moskitonetze (LLINs)", Against Malaria Foundation, `has_consensus:true`, 2/3). *(GPTs abweichendes Votum ist ein Vorbehalt innerhalb des Konsenses, kein offener Bereich — daher keine `dissent.B`-Zeile.)*
- `C` → `recommendations.C` (NTI, Konsens 3/3).
- `D` → `recommendations.D` („Eliminierung von Bleivergiftung via Farbregulierung", LEEP, Konsens 3/3).
- `dissent` = `{}` → alle vier `has_consensus:true`.

---

## Selbstcheck (die drei Fragen, dort wo sie beißen)

- **„Steht das sinngemäß im Wortlaut?"** — Ja, Fundstellen je Satz oben. Ausnahme sind die
  zwei gemeldeten Befunde, wo `summary` und Voten auseinanderlaufen; dort folgt der Entwurf
  den Voten/Empfehlungen.
- **„Schickt der Satz jemanden mit falscher Begründung zum Spenden?"** — Kritisch war
  Sitzung 3 A: die Empfehlung ist konditional mit Vertagungsantrag. Deshalb nennt der Satz
  ausdrücklich, dass der Rat die Bildungs-Alternative später erneut prüfen will — sonst
  klänge HKI belastbarer, als der Rat es beschloss.
- **„Ist ein offener Bereich versehentlich als Empfehlung formuliert?"** — Nein. Der einzige
  offene Bereich (Sitzung 1 A) steht als `recommendations.A = null` + `dissent.A`, nie als
  Empfehlung. Sitzung 3 B ist Konsens mit Vorbehalt, kein offener Bereich.

## Zwei Integrations-Hinweise (an Frontend/Freigabe, keine Entwurfsfrage)

1. **Bereichs-Labels** („Zukunft", „Leid lindern", „Große Gefahren", „Was sonst übersehen
   wird") stammen aus den festen Site-Labels und stehen im Satz mit drin. Falls das
   Frontend das Label ohnehin je Zeile voranstellt, entsteht eine Dopplung — dann das Label
   aus dem `plain`-Satz nehmen oder im Renderer nicht doppeln. Abstimmen mit Kimi.
2. **`dissent`-Wert** enthält bereits „keine Einigung — …". Kimis Archiv-Template (§5.3)
   darf „keine Einigung" nicht ein zweites Mal voranstellen.
