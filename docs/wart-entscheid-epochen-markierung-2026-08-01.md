# Wart-Entscheid — Epochen-Markierung: Aufbauphase und Regelbetrieb

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-01
**Anlass:** Steward-Entscheid, ab Go-Live je Familie das stärkste verfügbare Modell zu
besetzen; Wunsch nach einem sichtbaren Schnitt zur Entwicklungszeit.
**Bezug:** Ergänzt den Entscheid zur Vertragsbruch-Maschine vom 2026-08-01.

---

## Entscheid

Der Rekord wird in zwei Epochen geführt: **Aufbauphase** (Sitzungen 1–3 und alle
Journal-Einträge bis zum Go-Live-Merge) und **Regelbetrieb** (ab der ersten Sitzung
nach Go-Live). Nichts wird entfernt, nichts archiviert, nichts umnummeriert — die
Epoche ist ein Attribut am Bestand, keine neue Zählung und keine zweite Ablage.

Begründung: Das Gründungsversprechen — jede Sitzung wird vollständig und unverändert
veröffentlicht — kennt keine Ausnahme für Sitzungen, die man später lieber anders
geführt hätte. Ein nachträgliches Entfernen wäre im offenen Repo für immer nachweisbar
und würde das Versprechen rückwirkend brechen. Der berechtigte Kern des
Steward-Anliegens — die Aufbauphase lief aus Kostengründen nicht mit den stärksten
Modellen je Familie, ihre Ergebnisse sind Entwicklungsstand — wird stattdessen zum
Rekord gemacht: Die Markierung erklärt die Schwäche, bevor ein Besucher sie entdeckt.
Das ist Transparenzgewinn, nicht Gesichtsverlust.

## Umsetzung

**1 · Epochen-Vermerk als Rekordtext.** Ein kurzer Vermerk, sinngemäß:

> *Die Sitzungen 1–3 fallen in die Aufbauphase des Projekts. Aus Kostengründen war
> nicht jede Modellfamilie mit ihrem stärksten Modell besetzt; Verfahren und Werkzeuge
> wurden parallel entwickelt. Die Protokolle stehen vollständig und unverändert im
> Rekord, sind aber als Entwicklungsstand zu lesen. Ab Sitzung 4 besetzt jede Familie
> das jeweils stärkste verfügbare Modell.*

Endfassung des Wortlauts liegt bei mir (Freigabe auf dem üblichen Weg), Übersetzung
EN analog zur Klartext-Schicht.

**2 · Kennzeichnung im Datenbestand.** Die drei Bestandssitzungen erhalten ein Feld
`era: "aufbau"` (Regelbetrieb: Feld fehlt oder `era: "regelbetrieb"` — das Fehlen
liest sich als Regelbetrieb, damit künftige Sitzungen nichts tragen müssen). Kein
Schema-Zwang nötig (`additionalProperties: true`). Läuft über den bestehenden
Datenbranch, kein neuer Vorgang.

**3 · Darstellung.** Die Bühne der Site führt ab Go-Live mit der jüngsten Sitzung des
Regelbetriebs; die Aufbau-Sitzungen bleiben im Archiv und im Explorer voll zugänglich,
tragen dort den Vermerk sichtbar (Gestaltung ist Sache der Noble-Session — Vignette,
nicht Warnschild). Bis Sitzung 4 gelaufen ist, zeigt die Bühne weiter Sitzung 3 mit
Vermerk; eine leere Bühne gibt es nicht.

**4 · Der Modellwechsel ist Rekord.** Die Besetzung je Familie ändert sich in
`gremium/config.json`; der Commit ist das Datum des Wechsels. Der Epochen-Vermerk
nennt den Wechsel ausdrücklich (siehe Wortlaut). Welche Modelle es konkret werden,
ist Steward-Entscheid und braucht keine Wart-Freigabe — nur die Nennung im Rekord.

## Abgrenzung

Nicht Teil dieses Entscheids: das Prüfer-Amt. Die Prüfung von Modellantworten bleibt
deterministisch (Vertrag, Schema, strikte Typen — Entscheid vom 2026-08-01); ein
urteilender Prüfer über Council-Antworten widerspräche dem Kernprinzip, dass kein LLM
den Ablauf steuert, und bräche die Gleichbehandlung der Familien. Die Rechenschaft des
Warts über seine tatsächlichen Urteile (Rahmen, Grenzfälle, Rekord-Entscheide) ist
durch die publizierten Entscheid-Dokumente im offenen Repo erbracht; letzte Instanz
ist der Steward.
