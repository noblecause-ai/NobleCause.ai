# Übergabe an die neue Noble-Session — vom Wart

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-07
**Anlass:** Die vorige Noble-Session ist mitten in der Arbeit hängen geblieben; ihre
angekündigte eigene Übergabe existiert nicht. Dieses Dokument ersetzt sie aus
Wart-Sicht. Quellen: die Wart-Entscheide dieser Woche (alle in `docs/`), die letzte
Statusmeldung der hängenden Session, die Projekt-Übergaben vom 28.07.–03.08.
Was allein aus der letzten Statusmeldung stammt und von mir nicht unabhängig
geprüft ist, steht als solches markiert.

---

## 1 · Rollen, in einem Absatz

**Steward** (Afschin): menschliche Letztinstanz, gibt Sitzungsfragen ein, nimmt ab.
**Wart** (Claude Fable 5, dieses Amt): Rekord-Hoheit — Kanon, kanonische IDs,
versiegelte Datennaht, Freigaben; entscheidet auf Vorlage, baut nicht.
**Noble-Session** (du): Architekt/Betrieb — baut, legt vor, entscheidet selbst
alles, was den Rekord weder ergänzt noch umdeutet (Verfahrenslast-Regel, s. §4).
**CC**: führt aus, verifiziert. **Codex/Kimi**: externe Reviews.
Der Rat (Opus · GPT · Gemini) tagt per API; der Wart-Scout recherchiert wöchentlich.

## 2 · Stand des Rekords (geprüft)

- **Sitzung 4 (`sessions/2026-08/`) ist im Rekord und inhaltlich korrekt.** Der
  Namens-Spalt (sechs Voten C/D ohne Klammer-Akronym) wurde nach Wart-Kriterium
  per zwei Alias-Einträgen in `organizations.json` reaggregiert: C = NTI 3/3,
  D = LEEP 3/3, alle sechs `conditional = true` über das strukturierte Feld.
  `unresolved_votes` leer, Korrekturhinweis DE+EN am Eintrag. Entscheid:
  `wart-entscheid-namens-spalt-sitzung-4-2026-08-06.md`.
- **Sitzung 4 ist ein Meinungsbild, keine Evidenzprüfung** — das Dossier fehlte
  (zweite Fable-Verweigerung bei Biosicherheits-Materie). Markierung im Rekord
  vorhanden; neue Kanon-Regel dazu in §4.
- **Live-Seite eingefroren auf `ad75650` (2. August), zeigt Sitzung 3.** Der
  Rekord ist der Auslieferung voraus — das ist der aktuelle Hauptzustand.

## 3 · Das eine Dringende (Frist: Montag, 06:00 UTC / 08:00 Zürich)

**Die drei Medaillon-Assets sind laut letzter Statusmeldung der einzige
verbleibende Build-Blocker** — sechs Dateien, je Normal- und lo-Variante:
`claude-opus-5.avif`, `gpt-5.6-sol.avif`, `gemini-3.5-flash.avif` (+ `-lo`).
Sie brauchen die Hand des Stewards (Bildgenerierung); der Steward hat das
Einholen bereits zugesagt.

Warum Montag: Um 06:00 UTC läuft der Wart-Cron automatisch. Schreibt er einen
Journaleintrag und pusht, läuft der Deploy an — und wäre ohne die Assets rot.
Es ist der dritte Anlauf bei Biosicherheits-Materie nach zwei Verweigerungen;
der Refusal-Guard fängt beide Ausgänge sauber ab, am Montag selbst ist nichts
zu tun. Die Bauvorgaben für die Medaillons sind entschieden und werden nicht neu
verhandelt: Messingrelief-Stil, Opus = Öllampe, GPT = Waage/Zirkel, Gemini =
Florence Nightingale (†1910), **Modellname immer am Medaillon**.

Nach Eingang der Assets: einbauen, Build grün, ausliefern — dann zeigt die
Seite Sitzung 4 mit Korrekturhinweis und Meinungsbild-Markierung.

## 4 · Kanon-Regeln dieser Woche (bindend, nicht neu verhandeln)

1. **Verfahrenslast:** Erzeugt eine Governance-Frage mehr Text als die Änderung
   Code, gilt im Zweifel der einfachere Weg. Was den Rekord weder ergänzt noch
   umdeutet, entscheidet die Noble-Session ohne Wart-Vorlage.
2. **Vertragsbruch-Maschine:** Publiziert wird, was gültig ist; markiert, was
   fehlt; Abbruch nur, wenn der Rekord nicht wohlgeformt herstellbar ist.
   Schema-Tore vor jedem Commit. `convene` nur als echtes JSON-Boolean.
3. **Verweigerung ist Rekord:** Eine Modell-Verweigerung ist ein Datum über das
   Modell — eigener Journaleintrag (Typ `refusal`), Grund erscheint auf der
   Seite, nichts wird weggefiltert.
4. **Zählstand:** `Y` ist die Zahl der Sitze (3), nie gesenkt; Ausfälle stehen
   daneben („2 von 3 · 1 ohne auswertbares Votum"), nie eingerechnet.
5. **`conditional`:** strukturiertes Pflichtfeld ab Sitzung 4; Bestand
   grandfathered; nie aus Prosa erschlossen.
6. **Familien-Zuordnung:** immer aus der Config, nie aus der Selbstaussage eines
   Modells; das Prompt nennt die hinterlegte Familie und lädt zum Widerspruch ein.
7. **Ohne Dossier keine Evidenzprüfungs-Frage** — die Sitzungsfrage muss zum
   Belegstand passen (Muster: erzwungene Wahl misst Prioritäten ohne Evidenz).
8. **Aliase sind Daten, Matcher bleibt streng** — kein Fuzzy-Matching, je Alias
   ein begründeter Registratur-Eintrag; zweifelhafte Aliase gibt es nicht.
9. **Sichtbarkeit:** `raw/` unantastbar öffentlich · Dreiteilung
   (Rekord-Grundlagen / Prüfmaterial öffentlich, nur Arbeitsmaterial privat;
   Kriterium: braucht ein Leser die Datei, um Publiziertes zu prüfen?) · **kein
   History-Rewrite, nie** · Personennamen künftig als Rollen.
10. **`schedule.json` gehört dem Mechanismus** — lokal nie editieren, bei
    Zusammenführungen immer von `origin/master` übernehmen.

## 5 · Offen mit ausdrücklicher Zeit (Reihenfolge aus letzter Statusmeldung)

| Was | Stand |
|---|---|
| **Deliberationsform** (Erwiderungsrunde A + Fragedesign B) | Entschieden und zulässig (`wart-entscheid-deliberationsform-2026-08-06.md`); Bau erst nach Steward-Freigabe, **nicht in der Woche eines scharfen Laufs**. Auflage offen: Verfahrensbeschreibung der Seite (DE/EN) vor dem ersten Lauf im neuen Format präzisieren — Wortlaut über den Wart. |
| **Teil 2 / A2** | `kind`-Feld im Journal-Schema (`research`\|`refusal`), dann Verweigerungseintrag Lauf #6 publizieren (Wortlaut-Freigabe über den Wart steht noch aus). |
| **Einstiegskonzept** | `claude/noblecause-einstiegskonzept-2026-08-02.md` — Umstellung, kein Neubau; „Durch dieses System fließt kein Geld" nach vorn. |
| **Scout-Redundanz** | Zwei Scouts, mindestens einer aus einer Familie außerhalb des Rats; vorher Messlauf der acht Suchanfragen gegen GPT/Gemini (ohne Rekordschreibung), Ergebnis an den Steward. Sitzbesetzung ist Steward-Entscheid. |
| **P13 (Medaillon-Befund), Sortier-Listen, Container-Aufräumarbeiten** | Nur aus der letzten Statusmeldung bekannt, vom Wart nicht geprüft — Details bei CC bzw. in `docs/` rekonstruieren; falls ein Rekord-Bezug auftaucht, vorlegen. |

## 6 · Wie du mit dem Wart arbeitest

Vorlagen mit Rohmaterial im Wortlaut und einem klaren Entscheidungsbedarf — wie
die Namens-Spalt-Diagnose, sie ist das Muster. Gebündelt statt tröpfelnd. Keine
Vorlagen für Darstellungsermessen. Wortlaute (Korrekturhinweise, Vermerke,
Klartext) liefere ich DE und EN in einem Zug. Und der Maßstab aus §4.1 gilt auch
für mich: Wenn eine Vorlage mehr Verfahren erzeugt als Substanz, sag es.
