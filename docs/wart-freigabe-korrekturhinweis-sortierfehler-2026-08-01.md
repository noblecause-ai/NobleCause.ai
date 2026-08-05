# Wart-Freigabe — Korrekturhinweis-Wortlaut für `journal/2026-07-20` und `journal/2026-07-27`

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-01
**Struktur:** `correction_notice` (DE/EN) im Journal-Schema; die Einträge selbst bleiben
unverändert. Der Wortlaut ist für beide Einträge identisch — er spricht vom „diesem Lauf"
und braucht keine Datumsvariante. Sollte das Feld je Eintrag ein Datum des Hinweises
tragen, gilt: 2026-08-01.

---

## DE — für beide Einträge

> **Korrekturhinweis (2026-08-01):** Dieser Lauf prüfte infolge eines Sortierfehlers die
> Evidenzlage der überholten Sitzung 1 statt der geltenden Sitzung 3. Ursache: Alle drei
> Bestandssitzungen tragen dasselbe Datum; die Auswahl der „letzten" Sitzung sortierte
> nur nach dem Datumsstring und hing damit von der Dateisystem-Reihenfolge des Runners
> ab. Geprüft wurden dadurch Malaria Consortium (Bereich B) und Centre for the
> Governance of AI (Bereich C); die geltenden Empfehlungen — Against Malaria Foundation
> und Nuclear Threat Initiative — waren zum Zeitpunkt dieses Laufs ungeprüft. Der
> Einberufungs-Entscheid dieses Laufs (keine Einberufung) beruht auf dieser überholten
> Grundlage. Die Recherche selbst wurde auf der falschen Basis ordnungsgemäß geführt;
> Suchanfragen, Funde und Bewertungen stehen unverändert im Rekord. Der Sortierfehler
> ist behoben (Sortierung nach Sitzungsnummer, dazu ein Abbruch-Gate gegen die Auswahl
> einer überholten Sitzung).

## EN — für beide Einträge

> **Correction notice (2026-08-01):** Due to a sorting error, this run examined the
> evidence base of the superseded Session 1 instead of the current Session 3. Cause:
> all three existing sessions carry the same date; the selection of the "latest"
> session sorted by date string only and therefore depended on the runner's file
> system order. As a result, the run examined Malaria Consortium (area B) and the
> Centre for the Governance of AI (area C); the current recommendations — Against
> Malaria Foundation and Nuclear Threat Initiative — were unexamined at the time of
> this run. This run's convocation decision (no convocation) rests on this superseded
> basis. The research itself was conducted properly on the wrong basis; search
> queries, findings, and assessments remain unchanged in the record. The sorting
> error has been fixed (sorting by session number, plus an abort gate against
> selecting a superseded session).

---

**Zur Abgrenzung, wie erbeten:** Der Text sagt „prüfte infolge eines Sortierfehlers"
und „auf der falschen Basis ordnungsgemäß geführt" — der Fehler liegt bei der Maschine,
die die Eingabe wählte, nicht beim Wart, der sie verarbeitete. Diese Unterscheidung ist
Absicht und bleibt in jeder Übersetzung erhalten.
