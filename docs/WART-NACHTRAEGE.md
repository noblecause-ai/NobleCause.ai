# Wart-Nachträge zum Vertragsbruch-Entscheid (2026-08-01)

Diese drei Entscheide ergingen als Antworten auf Rückfragen aus der Umsetzung und liegen
nicht als eigene Dokumente vor. Sie sind Teil des Maßstabs für die Abnahme.

---

## Nachtrag 1 · Sortierung — der B1-Befund (Kimi)

**Freigegeben, Position 1 der Reihenfolge.** Sortierschlüssel `(number, date)` in
`latest_session()`, dazu ein **hartes Gate** (Abbruch, wenn `session_ref.number` nicht das
Maximum ist).

Wörtlich: *„Das Gate ist wichtiger als die Sortierung, denn es fängt auch künftige Ursachen
derselben Wirkung."*

Die Priorisierung des Haupt-Entscheids wurde damit korrigiert: Dieser Befund schlägt B
(`convene`), weil B eine Formatabweichung braucht, dieser Fehler aber mit Sicherheit
eintritt.

## Nachtrag 2 · Die Y-Frage — Zählweise bei Ausfall

**`Y` bleibt 3.** Wörtlich: *„`Y` ist die Zahl der Sitze, nicht der auswertbaren
Antworten — sie zu senken hieße, die Prämisse der Seite (drei Familien prüfen dieselben
Belege) am Zählstand still umzuschreiben. Und `Y = 3` mit stillschweigender Einrechnung des
Ausfalls würde ein Votum behaupten, das nie abgegeben wurde. Also: `Y` bleibt 3, der Ausfall
steht daneben, nie eingerechnet — „2 von 3 · 1 ohne auswertbares Votum". Das ist die
Grundsatzregel auf den Zählstand angewandt: publizieren, was gültig ist; markieren, was
fehlt."*

**Zwei Randfälle, mitentschieden:**

- **Bleibt nur ein gültiges Votum:** Die Regel kann keinen Konsens erzeugen. Der Bereich
  zeigt das Einzelvotum **mit Attribution** plus Ausfallsvermerk — wie jeder andere Bereich
  ohne Konsens.
- **Null gültige Voten:** markierter Ausfall des Bereichs (Regel 2 des Haupt-Entscheids).

**Ratssaal:** dieselbe Zählweise, zwingend. *„Zwei Darstellungen desselben Rekords dürfen
nicht verschieden zählen."* Wie der Ausfall dort gestalterisch erscheint, ist Sache der
Noble-Session; **dass** er erscheint und nicht weggerechnet wird, ist Rekord.

## Nachtrag 3 · `conditional` — grandfathered, Vertrag nur vorwärts

Der Beleg des Warts für ein bereits strukturiert geliefertes Feld war **zirkulär** — er
stützte sich auf ein Feld im aggregierten `session.json`, das die zu ersetzende Regex dort
hineingeschrieben hatte. **Kein rohes Modell-Votum trägt das Feld.**

Entscheid:

- **Der Bestand behält seine eine `conditional_count`-Zählung** (2026-07c, Säule A, Claude
  Opus; unabhängig als inhaltlich korrekt bestätigt). Dass die Nachrechnung nach dem Umbau
  0 ergibt, ist **keine Abweichung, sondern ein Methodenwechsel**.
- **Die Nachrechnungsauflage aus dem Haupt-Entscheid ist gestrichen** — es gibt nichts
  nachzurechnen, wenn sich die Erhebungsmethode ändert.
- Vermerk „vor-strukturell erhoben" gehört in den Epochen-Vermerk, **kein Feld-Backfill**.
- **Der Pflichtfeld-Vertrag gilt nur vorwärts:** ab Sitzung 4 fragt der Prompt `conditional`
  strukturiert ab, die Zählung läuft ausschließlich darüber, die Regex entfällt ersatzlos.
  Liefert ein Modell das Feld nicht, greift der Vertragsbruch-Mechanismus — Votum ungültig,
  markiert, **kein Titel-Raten als Fallback**.
