# Wart-Entscheid — Modell-Verweigerung im Rekord (Lauf #6, 2026-08-03)

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-03
**Anlass:** Research-Lauf #6 abgebrochen — `claude-fable-5` verweigerte nach acht
Websuchen die Ausgabe (`stop_reason: refusal`); Thema Säule C, Pandemievorsorge/H5N1.
**Offenlegung:** Der Wart urteilt hier über eine Verweigerung des Modells, das er selbst
ist. Fragen 1–3 sind Kanon-Fragen und werden entschieden; bei Frage 4 (Sitzbesetzung)
ist der Wart befangen und gibt nur Strukturhinweise. Entscheidung: Steward.

---

## 1 · Ist eine Verweigerung ein markierungspflichtiges Rekord-Ereignis? — Ja.

Eine Verweigerung ist kein Betriebsfehler und kein Vertragsbruch — sie ist ein
**Datum über das Modell**, derselben Klasse wie ein abweichendes oder ungültiges
Votum. Ein Projekt, das publiziert, wie Modelle urteilen, muss auch publizieren,
wo ein Modell nicht urteilen will. Sie wegzulassen wäre die stille Lücke, die die
Grundsatzregel verbietet; sie zu verstecken wäre schlechter als die Verweigerung
selbst.

Abgrenzung zum Vertragsbruch-Entscheid: Dort entsteht kein Journal-Eintrag, weil
eine unlesbare Antwort keine Entscheidung enthält, die man protokollieren könnte —
ein Eintrag würde etwas behaupten, das nie geschah. Eine Verweigerung ist das
Gegenteil: ein klares, strukturiertes Ergebnis (`stop_reason: refusal`). Es geschah
etwas Protokollierbares.

## 2 · Wo und wie erscheint sie?

**Eigener Journal-Eintrag** für Lauf #6, mit:

- den gelaufenen Suchanfragen (sie sind geschehen und liegen als Rohartefakt vor),
- einem Verweigerungsvermerk als Strukturfeld (z. B. `refusal: true` +
  `refusal_note`), **kein** `convene`-Feld — es wurde keine Einberufungsfrage
  entschieden, und die Maschine erfindet keine Entscheidung,
- `model` / `model_label` wie üblich.

**Vermerk in Sitzung 4**, falls das Dossier fehlt (siehe 3): „Für Bereich C liegt
kein Research-Dossier vor" mit Verweis auf den Journal-Eintrag.

**Auf der Seite steht der Grund, nicht nur die Lücke.** „Kein Dossier" ohne Grund
lädt zur Spekulation ein und wäre eine halbe Wahrheit auf einer Seite, deren Zweck
ganze Wahrheiten sind. Wortlaut sachlich, ohne Dramatisierung, sinngemäß: *„Das
Modell hat die Ausgabe zu diesem Thema verweigert; die Suchanfragen und die
Rohantwort stehen im Rekord."* Endfassung DE/EN auf dem üblichen Weg. Die
Verweigerung ist ein Befund über das Modell — die Seite zeigt Befunde.

## 3 · Darf Sitzung 4 ohne Dossier für einen Bereich laufen? — Ja, markiert.

Der Architekt hat recht: Das Dossier ist Zulieferer, nicht Sitzung. Die drei
Ratsvoten hängen weder an Fable noch an der Websuche. Eine Sitzung an einem
fehlenden Beipack scheitern zu lassen würde den Ausfall eines Zulieferers zum
Ausfall des Gremiums machen — genau die Abhängigkeit, die die Grundsatzregel
vermeiden will. Bedingung: Der Sitzungsrekord markiert das fehlende Dossier
(siehe 2), und der Ratsprompt behauptet kein Dossier, wo keines ist.

**Aber: `run_session.py` braucht den Refusal-Guard vor Donnerstag.** Der
Dossier-Schritt ruft dasselbe Modell über dieselbe Materie — ohne Guard wird aus
einer sauberen Verweigerung ein unsauberer Parse-Fehler. Gleiche Behandlung wie in
`run_wart.py`: Abbruch des Dossier-Schritts, Markierung, Sitzung läuft weiter.
Kleiner Diff, gleicher Bauweg (Codex baut, CC verifiziert, Diff an den Wart).

## 4 · Zum Wart-Sitz — Strukturhinweise eines Befangenen

Die Messung vorab ist richtig: dieselben acht Suchanfragen gegen GPT und Gemini,
ohne Rekordschreibung. Vor Daten wird kein Sitz getauscht.

Zur Zulässigkeit: **Ein Modellwechsel als Antwort auf eine Verweigerung ist
zulässig, wenn die Verweigerung publiziert ist und bleibt.** Getauscht würde dann
nicht das Ergebnis, sondern der Zulieferer — das Ergebnis (die Verweigerung) steht
im Rekord. Unzulässig wäre nur der stille Tausch, der so tut, als wäre nichts
gewesen.

Zur Struktur — die Ämter sind bereits getrennt, und die Trennung trägt die Lösung:

- **Scout (Research):** Braucht Websuche und Verlässlichkeit, nicht das stärkste
  Modell. Ein Scout aus einer **vierten Familie, die nicht im Rat sitzt** (Präzedenz:
  Kimi K2 lief bereits in Vertretung, sauber attribuiert), vermeidet die
  Befangenheitsfrage vollständig — kein Ratsmitglied prüft die Belege vor der
  eigenen Sitzung. Die geplante Erweiterung (größerer Rat, **zwei Scouts**) löst
  zusätzlich das Ausfallproblem strukturell: Verweigert einer, liefert der andere,
  und die Verweigerung steht trotzdem im Rekord. Vorziehen ist sinnvoll.
- **Wart (Governance):** Prüft Rahmen, IDs, Datennaht — keine Bio-/Chemie-Recherche.
  Kein bekannter Konfliktfall; bleibt unverändert, bis einer eintritt.
- **Rekord bei Sitzwechsel:** Kein Epochen-Vermerk nötig. Jeder Journal-Eintrag
  trägt `model`/`model_label` — die Attribution ist pro Lauf, nicht pro Ära. Es
  genügt der `config.json`-Commit plus ein Satz im nächsten regulären Vermerk.
  (Der `conditional`-Fall brauchte die Epoche, weil sich eine *Methode* änderte;
  hier wechselt eine *Besetzung*, und Besetzungen sind schon heute pro Eintrag
  attribuiert.)

## Reihenfolge bis Donnerstag

1. Refusal-Guard in `run_session.py` (blockierend für Sitzung 4).
2. Journal-Eintrag Lauf #6 nach Ziffer 2, Wortlaut-Freigabe parallel.
3. Messlauf GPT/Gemini (ohne Rekordschreibung) — Ergebnis an den Steward.
4. Sitzung 4 läuft Donnerstag, notfalls mit markiert fehlendem Dossier für C.
5. Sitzbesetzung Scout: Steward-Entscheid nach der Messung, nicht vorher.
