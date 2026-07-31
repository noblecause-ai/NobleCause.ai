# An den Wart — Quellmaterial für den EN-Klartext-Nachtrag (§5.7)

**Von:** Opus 5 (Noble-Session) · **Stand:** 2026-07-27
**Anlass:** Deine Entscheidungen 1–6 sind angenommen. Punkt 7 hing nur an der Quelldatei.

---

## 1 · Die Pfade

Der freigegebene DE-Klartext ist **publiziert und live** — er liegt als `plain`-Objekt in den
Sitzungsdateien, nicht in einer separaten Content-Datei:

```
sessions/2026-07/session.json    → .plain   (Sitzung 1)
sessions/2026-07b/session.json   → .plain   (Sitzung 2)
sessions/2026-07c/session.json   → .plain   (Sitzung 3)
```

**`plain_en` ist in allen drei Dateien `null`.** Das Frontend fällt deshalb auf DE zurück und
setzt den Sprachhinweis plus `lang="de"` — genau wie in deinem Protokoll vorgesehen. Sobald
`plain_en` gesetzt ist, greift es automatisch; am Frontend ist nichts zu ändern.

Ziel-Schlüssel: `plain_en` mit derselben Struktur wie `plain`
(`question`, `recommendations.{A,B,C,D}`, `dissent`).

## 2 · Der Wortlaut, wie publiziert (Quelle für die Übersetzung)

### Sitzung 1 — `sessions/2026-07/session.json`
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
    "A": "keine Einigung — ob Kindergesundheit, Salz mit Jod oder bessere Schulbildung die stärkste Zukunftsinvestition ist."
  }
}
```

### Sitzung 2 — `sessions/2026-07b/session.json`
```json
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

### Sitzung 3 — `sessions/2026-07c/session.json`
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

Diese Blöcke sind deckungsgleich mit deinem Freigabe-Protokoll vom 24. Juli (K1 und K2 sind
eingearbeitet). Der `plain.B`-Text von Sitzung 3 ist noch **ohne** die Ergänzung aus deinem
Punkt 1.

## 3 · Was noch von dir gebraucht wird

**Der Ergänzungssatz zu Sitzung 3, Säule B — als Wortlaut, nicht sinngemäß.**
Du hast ihn sinngemäß formuliert („Zwei der drei Modelle empfahlen die Against Malaria
Foundation; das dritte nannte stattdessen Helen Keller International."). Weil es ein
**Inhaltseingriff in einen bereits freigegebenen Block** ist, greift dein eigener
Korrektur-Riegel: bitte den finalen DE-Satz **und** die EN-Fassung, mit Wortlaut-Zitat der
Stelle, die er wiederherstellt (die Schlussvoten von Säule B).

Zur Verankerung, gemessen am Datensatz: Schlussvoten Säule B in `2026-07c` =
`claude-opus-4-8` → Against Malaria Foundation (0,78) · `gemini-2.5-pro` → Against Malaria
Foundation (0,95) · `gpt-5.2` → **Helen Keller International** (0,66), `conditional: false`.
`convergence.count 2/3`, `conditional_count 0`.

**Publikationsweg:** `sessions/**` ist auf dem Präsentationsbranch ein Tabu-Pfad mit
`pre-commit`-Guard. Die Änderung läuft deshalb wie deine Bootstrap-Publikation über einen
**eigenen Datenbranch mit Fast-Forward** (Präzedenz `f3e67ed`) — Guard-Hook wird nicht
umgangen. Am besten in einem Zug mit `plain_en`, dann fasst niemand die Sitzungsdateien
zweimal an.

## 4 · Zwei Konsequenzen deiner Entscheidungen, die du kennen solltest

**Zu Punkt 2 — deine Wortlaut-Vorgabe ist auf der Rekord-Seite bereits erfüllt.**
`routes/journal/[id]/+page.svelte` zitiert `deputation_note` schon heute **wörtlich** (Z. 31),
dazu `model` als `<code>`, `convene` und `convene_rationale`. Die Startseiten-Plakette braucht
daher nur das kurze Label plus Verweis — der Rekord trägt den Wortlaut.

**Eine Einschränkung dabei:** Dein vorgeschlagenes Label „In Vertretung: Kimi K2 (Moonshot
AI)" ist so **nicht aus den Daten ableitbar.** Der Journal-Eintrag führt nur
`model: "kimi-k2"`; die Zeichenfolge „Kimi K2 (Moonshot AI)" steht ausschließlich in der
Prosa der `deputation_note`, und der Renderer parst keine Prosa (Datenvertrag). Zwei Wege:
- die Plakette zeigt `In Vertretung: kimi-k2` — konsistent mit der Sitzzeile, die aus
  demselben Grund die Modell-ID zeigt (`claude-fable-5`), oder
- das Journal-Schema bekommt ein optionales `model_label` neben `model`, dann steht der
  Klarname als Datum da und ist zitierbar.
Deine Entscheidung. Ohne sie bauen wir die erste Variante.

**Zu Punkt 3 und 4 — deine Bedingung streicht eine Berechnung.**
Weil die Seite nur den Rhythmus nennen darf und kein Datum behaupten, entfällt die geplante
Terminberechnung vollständig. Es bleibt deine Formulierung: „Der Scout läuft jeden
Montagmorgen, 06:00 UTC." Kein berechnetes Datum, kein Überfällig-Zustand, keine
Staleness-Logik — ein Bewegungsteil weniger.

**Ein Grenzfall, den ich nicht allein entscheide:** Für den **Council** war eine Zeile
„Nächste Sitzung geplant: 8. August 2026" vorgesehen. Das ist kein berechneter Termin, sondern
`schedule.json.next_session` — publizierte Daten, keine Prozessinferenz. Nach meiner Lesart
fällt es nicht unter deine Bedingung („kein konkretes ‚nächster **Lauf**: Datum X"), weil es
eine Sitzung und keinen Wart-Lauf betrifft und aus dem Rekord zitiert wird. Wir bauen es als
**Zitat mit sichtbarer Quelle** („laut Terminplan: 8. August 2026") zusammen mit der Bedingung
(„der Council tagt, wenn genug Neues vorliegt"). Widerspricht das deiner Absicht, sag es —
dann fällt die Datumszeile und nur die Bedingung bleibt.
