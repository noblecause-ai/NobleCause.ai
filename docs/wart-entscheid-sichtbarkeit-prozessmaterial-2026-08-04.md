# Wart-Entscheid — Sichtbarkeit von Prozessmaterial

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-08-04
**Anlass:** Vorlage der Reorg-Session (privates meta-Repo als Default), eingebracht und
eingeordnet vom Architekten. Rahmen: Bis zu diesem Entscheid wurde nichts verändert.

---

## 1 · `raw/` bleibt öffentlich — Bestätigung, und die Begründung ist korrekt

Die Rohantworten sind nicht Beleg *für* das Produkt, sie **sind** Teil des Produkts.
Die Seite verspricht wörtlich: Wer der Zusammenfassung misstraut, liest die
Rohantworten. Ohne `raw/` ist die versiegelte Datennaht ein Versprechen ohne
Einlösung. Das ist keine Sichtbarkeitsabwägung, sondern Existenzgrundlage — hier
wird nichts entfernt, nie. Die schwächere Begründung der Reorg-Session
(„funktional Produkt, weil `reaggregate.py` sie verarbeitet") ist nicht falsch,
aber nachrangig: Sie würde entfallen, wenn das Skript entfiele. Die richtige
Begründung entfällt nie.

## 2 · Die Dreiteilung trägt — mit dem Kriterium des Architekten, leicht geschärft

Die Zweiteilung Produkt/Prozess der Reorg-Vorlage ist zu grob; die Dreiteilung
(a) Rekord-Grundlagen · (b) Prüfmaterial · (c) Arbeitsmaterial ist richtig.
**Nur (c) darf ins private Repo.**

Kriterium, als Kanon-Regel:

> **Eine Datei bleibt öffentlich, wenn ein Leser des Rekords sie braucht, um eine
> publizierte Aussage zu prüfen oder eine gebaute Entscheidung nachzuvollziehen.**
> Trifft keines von beidem zu, kann sie ins private Repo.

Das deckt (a) — „ein Entscheid, der eine Bauweise bestimmt, wird mit dem Bau
committet" bleibt in Kraft; diese Woche hat gezeigt, was das Nachtragen kostet —
und (b): Ein Bericht ohne die Frage, auf die er antwortet, ist kein Beleg; ein
Review-Auftrag ist ein Prompt. Zweifelsfälle bei der Sortierung entscheidet die
Noble-Session nach diesem Kriterium selbst; nur wo sie schwankt, fragt sie — mit
Datei und einem Satz, nicht mit einer Vorlage.

Zur „Selbstkritik" ausdrücklich: Korrekturhinweise, Einordnungsvermerke,
Fehlerlisten sind Kategorie (a) und (b), nicht (c). Bei diesem Projekt sind
benannte Fehler der Beleg, dass das Verfahren arbeitet — sie zu privatisieren
würde ausgerechnet den stärksten Vertrauensbeweis entfernen.

## 3 · History-Rewrite — Nein, und es ist kein Abwägungsfall

Zwei voneinander unabhängige K.O.-Gründe, jeder allein ausreichend:

- **Technisch:** Ein Rewrite ändert alle SHAs. Der publizierte Rekord verweist auf
  SHAs (`correction_notice.commit`, Gate-Status, Befundliste, Wart-Entscheide).
  Nach einem Rewrite zeigt der gesamte Belegapparat ins Leere — der Rekord würde
  sich selbst die Beweise entziehen.
- **Grundsätzlich:** Ein Force-Push auf das öffentliche Repo eines Projekts, dessen
  Produkt die Unverfälschbarkeit des Rekords ist, widerlegt das Produkt. Dieselbe
  Logik wie beim Epochen-Entscheid: Nichts wird rückwirkend entfernt.

Konsequenz für die Umsetzung der Dreiteilung: Verschiebungen von (c) laufen als
**reguläre Commits vorwärts**. Das heißt auch: Verschobenes bleibt in der Historie
sichtbar. Das ist kein Mangel des Verfahrens, sondern seine Ehrlichkeit — das
private Repo ordnet die Gegenwart, es säubert nicht die Vergangenheit.

## 4 · Verfahrensdokumentation — keine Wart-Frage, bestätigt

Wo eine Verfahrensregel dokumentiert wird, ist Sache des Architekten
(`AGENTS.md`). Nach der Verfahrenslast-Regel vom 30.07. hätte diese Teilfrage
nicht vorgelegt werden müssen — sie ist hiermit ohne Entscheid zurückgegeben.

## Personennamen

Trennscharfer Umgang, drei Sätze:

1. **Vorwärts gilt:** Rekord- und Prozessdokumente nennen Rollen, nicht
   Privatnamen („der Steward", „der Architekt"). Namen, die bewusst öffentlich
   sind (Impressum, Commit-Konfiguration, Lizenz), sind davon unberührt.
2. **Der Bestand im HEAD** darf per regulärem Commit auf Rollen umgestellt werden,
   wo der Name nicht tragend ist — mit einem Sammel-Vermerk im Commit, nicht
   still.
3. **Die Historie bleibt**, aus den Gründen unter 3. Wer einen Namen aus der Welt
   schaffen will, kann das mit Git nicht rekordtreu — das ist ehrlich zu sagen,
   bevor jemand es erwartet.

---

**Zusammengefasst:** `raw/` unantastbar · Dreiteilung mit Prüfbarkeits-Kriterium,
nur (c) privat · kein Rewrite, Verschiebung nur vorwärts · Verfahrensdoku beim
Architekten · Namen künftig als Rollen, Historie bleibt. Die Reorg-Session kann
umsetzen.
