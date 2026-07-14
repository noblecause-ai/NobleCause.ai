# Datenvertrags-Vorschlag — Trennung „Was tut die Org" vs. „Warum gewählt"

**Vorschlag, NICHT umgesetzt.** Umsetzung erst nach Freigabe des Stewards.
Betrifft MUSS-FIX **F1**: `recommendations[].rationale_md` ist heute frontend-erfunden
(Säule A: „Die Finanzierungslücke ist aktuell besser belegt als bei der
Bildungsalternative" — eine vergleichende Schlussfolgerung, die kein Modell so
publiziert hat). Verfassungsregel: **Das Frontend erfindet keine Inhalte.**

## Beleg des Bruchs
`data/sitzung.json` → `recommendations[A].rationale_md` mischt zwei Dinge:
- **faktisch** („Vitamin A schützt Kinder vor vermeidbarer Krankheit und Tod.") und
- **wertend/vergleichend** („Finanzierungslücke besser belegt als bei der
  Bildungsalternative.") — nicht aus `summary`/`dissent_md`/Voten ableitbar.
B/C/D sind überwiegend faktische Org-Beschreibungen, tragen die Signatur aber latent.

## Die zwei Datenquellen sauber trennen

### (a) „Was die Organisation TUT" → `organizations.json` (kuratiert, versioniert, publiziert)
Faktische, zeitstabile Beschreibung. Gehört in die Registry, die schon die einzige
Quelle für `donation_url` ist — nicht in die Sitzungsdaten.

Neues Feld je Eintrag:
```json
{
  "id": "lead-exposure-elimination-project",
  "canonical_name": "Lead Exposure Elimination Project (LEEP)",
  "beschreibung": "LEEP hilft Ländern, bleihaltige Farbe zu verbieten. Das schützt Kinder dauerhaft vor Schäden an Gehirn und Gesundheit.",
  "beschreibung_quelle": "kuratiert; faktisch, keine Wahl-Begründung",
  "donation_url": "…"
}
```
→ `schema/organizations.schema.json` um `beschreibung` (string) +
`beschreibung_quelle` (string) erweitern (Vorschlag). Auf der Karte als „Was die
Organisation tut" ok. **Enthält nie**, warum das Gremium sie wählte.

### (b) „WARUM das Gremium wählte" → nur aus publizierten Sitzungsdaten
Nie handgeschrieben. Zwei erlaubte Wege:
1. **Direkt attribuiert** — die Karte zeigt/zitiert `summary` bzw. den einschlägigen
   `dissent_md`/Votentext mit Quelle („aus der Kurzfassung der Sitzung", verlinkt aufs
   Protokoll). Keine neue Prosa.
2. **Oma-taugliche Kurzfassung, falls nötig** — vom **publizierten, attribuierten
   Summarizer** im Lauf erzeugt, nicht im Frontend. Konkret: neues Backend-Feld
   ```json
   "recommendations[].begruendung_kurz": {
     "text": "…",
     "quelle": "summarizer",
     "modell": "claude-haiku-4-5"
   }
   ```
   in `run_session.generate_summary` gefüllt, im Schema definiert, mit ausgewiesener
   Modell-Attribution publiziert. Deterministisch reproduzierbar, im Golden-Netz
   (PR #10) prüfbar.

**`recommendations[].rationale_md` in seiner jetzigen Form entfällt.**

## Karten-Rendering (Skizze)
```
[Säule A · Vitamin-A]              Einigkeit mit Vorbehalt · 2 von 3
Helen Keller International
› Was sie tut:  <organizations.beschreibung>        (Fakt, Registry)
› Warum gewählt: <begruendung_kurz.text>            (Summarizer, attribuiert)
                 „… — aus der Kurzfassung der Sitzung ↗"   → Protokoll
[Direkt zur Organisation ↗]        (donation_url, Registry)
```
Fakt (Registry) und Wahl-Begründung (Sitzungsdaten) sind sichtbar getrennt und je
mit Quelle versehen. Das Frontend fügt **nichts** hinzu.

## Nebenwirkung auf F2 (Integration)
Weg (b)-Variante 2 macht die Wahl-Begründung zu einem **echten Backend-Feld** — damit
verschwindet ein weiterer erfundener Frontend-Inhalt und der Datentausch wird um ein
Feld sauberer. Zusammen mit dem F2-Vertrag (strukturierte Vote-Recs, Labels/Symbole,
Archiv) ergibt das den vollständigen Startseiten-Datenvertrag.

**Entscheidung offen (Steward):** (b)-Variante 1 (nur zitieren, kein neues Feld) oder
Variante 2 (Summarizer-`begruendung_kurz`). Empfehlung: Variante 2, weil oma-tauglich
UND attribuiert/deterministisch.
