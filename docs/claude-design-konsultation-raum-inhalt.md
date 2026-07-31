# Claude-Design-Konsultation — der Raum-Inhalt jenseits von Tafel und Prozessleiste

**Von:** Steward (via Opus) · **An:** Claude Design · **Zweck:** Den *inhaltlichen*
Aufbau der drei Räume finalisieren — nicht die Bühnenchoreografie (die steht), sondern
die Textblöcke und Panels, die in jedem Raum unter der Bühne liegen. Wir wollen
Redundanz raus, Komplexität runter, und jedem Raum eine eigene Aufgabe geben, bevor Kimi
es einsetzt.

---

## 1 · Worum es geht (Kurzkontext)

NobleCause.ai ist ein öffentliches KI-Deliberationsprotokoll. Drei KI-Modelle
verschiedener Familien (Anthropic, OpenAI, Google) prüfen dieselben Belege und empfehlen
öffentlich, wo eine Spende voraussichtlich am meisten bewirkt — in vier Bereichen. Alles
wird veröffentlicht: Empfehlungen, Meinungsänderungen, Uneinigkeit, Kosten. **Es fließt
kein Geld über die Seite** — Spendenlinks führen direkt zu den Organisationen.

Die Site ist als **Bühnenspiel** gebaut: ein Haus mit drei Räumen, jeder Aufruf ist ein
Auftritt. Man betritt einen Raum, die Beteiligten treten auf, die Antwort erscheint auf
einer Tafel, eine Tür führt weiter.

| Raum | Route | Rolle im Verfahren |
|---|---|---|
| **The Study** | `/` | Die Frage wird gestellt, Belege gesammelt |
| **The Council** | `/ratssaal/` | Getrennt beraten, dann öffentlich gezählt |
| **The Archive** | `/archiv/` | Alles veröffentlicht und aufbewahrt |

Register: gemalte Konzeptkunst, dunkles Holz, Messing, Bernstein-/Lampenlicht gegen
kaltes Mondblau — ernst, ruhig, „Frostpunk"-nah.

## 2 · Was FIX ist und NICHT zur Debatte steht

Zwei Elemente sind gesetzt und in **jedem** Raum sichtbar — bitte als gegeben behandeln:

- **Die Ergebnis-Tafel** (ResultBoard): trägt die Antwort der Sitzung und „reist" per
  View-Transition durch die Räume. Zeigt je Bereich: Emblem · Bereichsname · Organisation
  · Zählstand (z. B. „3 von 3") · Spendenlink. Ab 1200 px fix oben links, sonst im Fluss.
- **Die Prozess-Leiste** (FlowRail „So läuft es"): die sechs Verfahrensschritte, in jedem
  Raum sichtbar (auch im Council). Daneben zeigt eine schmale Prozess-Röhre im Bühnenbild
  denselben Ablauf als Füllstand (Position im Verfahren).

Alles Übrige unten ist Gegenstand der Konsultation.

## 3 · Die harten Randbedingungen (der Boden, nicht verhandelbar)

1. **§0, Verfassungsrang:** *Die Seite ist vollständig, bevor das Spiel beginnt. Die
   Inszenierung verzögert und bewegt nur — sie erzeugt nichts und versteckt nichts.* Ohne
   JS und bei `prefers-reduced-motion`: dasselbe vollständige Dokument.
2. **Der zweite Maßstab, gleichrangig:** *Ein Achtzigjähriger muss in 30 Sekunden finden,
   wohin er spenden kann.* Lesbarkeit ist der **Boden**, nicht das Ziel — Atmosphäre darf
   beeindrucken, aber den Weg zur Antwort nie verlängern.
3. **Versiegelte Datennaht:** Das Frontend paraphrasiert nie. Jeder sitzungsabhängige
   Text kommt aus den Daten (siehe §4). Feste Site-Copy (Erklärungen des Verfahrens,
   Bereichsnamen) steht in i18n und ändert sich nie.
4. Barrierefrei: ein `<h1>` je Raum, Tippziele ≥ 44 px, Reflow bei 320/390 px,
   AA-Kontraste, Tastaturbedienung, Ausklapp-Details ohne JS bedienbar.

## 4 · NEU und entscheidend: die Klartext-Schicht (gerade beschlossen)

Das schwerste Textproblem der Site — und der wichtigste Design-Input hier.

**Das Problem:** Der sitzungsabhängige Zusammenfassungstext ist heute Fachsprache und
ändert sich jede Sitzung. Beispiel-Original (1594 Zeichen):

> „…die Unterscheidung zwischen Interventions-Evidenz und Marginal-Evidenz …
> Absorptionskapazität … die Fungibilität einer Spende senkt …"

Für das eigentliche Publikum unlesbar. Die Site darf es nicht selbst vereinfachen
(versiegelte Naht). Beschlossen ist deshalb eine **Zwei-Schichten-Struktur, beide als
Daten**:

- **Klartext-Schicht** (neu): ein laienverständlicher Satz je Bereich, nach fester Regel
  — *„[Alltagsbereich] → [Organisation], weil [Alltagsgrund ohne Fachwort]"*, aktiv,
  ≤ 25 Wörter, kein Fachbegriff ohne Klammer-Erklärung. Erzeugt als Pipeline-Entwurf,
  **vom Wart freigegeben** (Korrekturen als Diff publiziert).
- **Rekord-Schicht** (Bestand): der Wortlaut (Zusammenfassung, Uneinigkeit) — unverändert,
  hinter Ausklapp.

**Pflicht-Kennzeichnung (nicht verhandelbar, Governance-Auflage):** Unter jeder
Klartext-Zeile steht ein fester Halbsatz — *„Vereinfachte Fassung, verantwortet vom Wart ·
Wortlaut des Rates darunter"* — mit dem Ausklapp zum Original direkt daneben. Die
Übersetzung deklariert sich als Übersetzung; wer den Rat zitieren will, findet ihn in
einem Klick.

**Beispiel, wie es beim Achtzigjährigen ankommen soll:**
> **Kindergesundheit → Malaria Consortium**, weil Moskitonetze und Vorsorge dort pro
> Franken die meisten Kinderleben schützen.
> *Vereinfachte Fassung, verantwortet vom Wart · Wortlaut des Rates ▸*

**Die Design-Frage dazu (Kern der Konsultation):** Die Ergebnis-Tafel zeigt heute nur das
*Was* (Bereich → Organisation → Zählstand). Der Klartext liefert das *Warum* in einem
Satz plus seine Pflicht-Kennzeichnung. **Wo lebt das Warum, und wie verbindet es sich mit
dem Was, ohne die Tafel zu überladen oder die 30-Sekunden-Regel zu brechen?** Sitzt der
Klartext-Satz auf der Tafel? Direkt darunter? Als eigener Block im Study-Eingang? Und wie
trägt die Pflicht-Kennzeichnung ehrlich, ohne wie ein Rechtstext zu wirken oder den
Sog zur Antwort zu bremsen?

---

## 5 · Der übrige Inhalt je Raum — Ist-Zustand, Problem, Frage

Reihenfolge = aktuelle Reihenfolge auf der Seite (nach Bühnenbild + Tafel + FlowRail).

### 5.1 · The Study — Aufgabe: „Die Frage"

**Ist-Zustand (in Reihenfolge):**
1. **Lead-Satz** unter dem Titel „Wo hilft meine Spende am meisten?" — heute:
   *„Je ein KI-Modell der Familien … prüft dieselben Belege und empfiehlt öffentlich,
   wo eine Spende voraussichtlich am meisten bewirkt."*
2. **Dossiers-Abschnitt:** sichtbarer Klartext-Kontext „Worum es ging" (heute der lange
   Fach-Text), darunter zwei Ausklapp-Details — die wörtliche Frage aus dem Protokoll,
   und die Suchanfragen des Spähers (als Code-Zeilen).
3. **Türen-Galerie** (zwei Türkarten zu Council und Archive).

**Probleme:** (a) Der Lead-Satz ist **wortgleich mit dem des Council** (siehe 5.2). (b)
Der „Worum es ging"-Text ist genau das Fach-Monster aus §4 — er wird durch die
Klartext-Schicht ersetzt.

**Design-Frage:** Study ist der Einstieg. Der Lead sollte hier *diese Sitzung* greifbar
machen (die Frage, in Klartext), nicht das Verfahren erklären (das tut die FlowRail). Wie
sieht der Eingangs-Textfluss aus, wenn oben die Frage in Klartext steht, die Tafel die
Antwort trägt, und der Fach-Wortlaut nur noch einen Klick tief liegt?

### 5.2 · The Council — Aufgabe: „Die Entscheidung"

**Ist-Zustand (in Reihenfolge):**
1. **Lead-Satz** — heute **identisch mit The Study** (derselbe Aufruf im Code).
2. **„Vier Empfehlungen":** je eine Zeile — Emblem · Bereich · Organisation · Zählstand ·
   Spendenlink, Vorbehalte hinter Ausklapp in der Zeile. (Inhaltlich nah an der Tafel,
   aber detaillierter: Vorbehalte, bei Uneinigkeit die Einzelvoten.)
3. **„Änderungen nach dem Gegenlesen":** wer sein Votum revidiert hat (Erst → Schluss),
   als kleine Kärtchen. Nur wenn es Revisionen gab.
4. **„Zählwerk":** kurze Zeile „Das Programm zählt nur gleiche Nennungen" + je Bereich ein
   Feld „N gleich" / „getrennt".
5. **„Alle Voten zeigen":** die volle Voten-Matrix je Modell, hinter Ausklapp.
6. **Türen-Galerie.**

**Probleme:** (a) Lead-Redundanz mit Study. (b) Die „Vier Empfehlungen"-Zeilen und die
Ergebnis-Tafel zeigen weitgehend dasselbe — hier braucht es eine klare Rollentrennung
(Tafel = die Antwort; dieser Abschnitt = das, was die Tafel *nicht* zeigt: Vorbehalte,
Einzelvoten, das Zählen). (c) Zählwerk, Revisionen, Empfehlungszeilen und Voten-Matrix
behandeln alle denselben Stoff (das Abstimmen) in vier getrennten Blöcken — womöglich zu
viel Mechanik für den Laien.

**Design-Frage:** Der Council ist der dramatische Höhepunkt (getrennte, gleichrangige
Stimmen, dann das Zählen). Wie ordnet man diese vier Mechanik-Blöcke so, dass die
*Kernaussage* — „getrennt geurteilt, öffentlich gezählt, Änderungen offengelegt" — sofort
lesbar ist und die Tiefe (volle Matrix, Vorbehalte) für den Interessierten daruntersteht,
ohne zu wiederholen, was die Tafel schon sagt? Und welcher fixe Lead-Satz gehört hierher?

### 5.3 · The Archive — Aufgabe: „Der Nachweis"

**Ist-Zustand (in Reihenfolge):**
1. **Kein Lead-Satz** (Titel „The Archive" steht allein).
2. **Sitzungsarchiv:** Liste aller Sitzungen, je „Sitzung N" + „Empfehlungen in allen
   Bereichen" bzw. „Noch keine Einigkeit: [Bereiche]".
3. **Kosten:** ein Satz + Tabelle (Kosten je Modell).
4. **Korrekturhinweis:** falls vorhanden (Wortlaut).
5. **„Noch keine Einigkeit":** Auszug aus dem Protokoll (Highlights) + voller Wortlaut
   hinter Ausklapp. Die Highlights sind heute **ebenfalls Fachsprache** (dieselbe
   Textsorte wie in §4).
6. **Link „Vollständiges Protokoll öffnen".**
7. **Türen-Galerie.**

**Probleme:** (a) Kein Lead — der Raum sagt nicht, wofür er da ist. (b) Die
Uneinigkeits-Highlights sind wieder Fach-Text; hier stellt sich dieselbe
Klartext/Rekord-Frage wie in §4 (braucht die Uneinigkeit ebenfalls eine Klartext-Zeile,
oder bleibt sie bewusst Rekord?). (c) Der Raum ist der einzige *ohne* zweite Bühnenebene —
er wirkt inhaltlich am trockensten.

**Design-Frage:** Wie gibt man dem Archiv einen ehrlichen Eingang (fixer Lead:
„Jede Sitzung vollständig und unverändert") und eine Ordnung, die den Nachweis-Charakter
würdig trägt — Vollständigkeit als Tugend, nicht als Datenfriedhof? Und: bekommt die
Uneinigkeit eine Klartext-Ebene, oder ist Uneinigkeit genau der Ort, an dem der Wortlaut
unübersetzt stehenbleiben muss?

---

## 6 · Die konkreten Fragen an Claude Design (zusammengefasst)

1. **Warum-Platzierung (wichtigste):** Wo lebt der Klartext-Satz (das *Warum*) im
   Verhältnis zur fixen Ergebnis-Tafel (dem *Was*), und wie trägt die Pflicht-Kennzeichnung
   ehrlich, ohne Sog und Register zu brechen? (§4)
2. **Drei fixe Lead-Sätze:** je Raum ein eigener, sich nie ändernder Eröffnungssatz, der
   die Raum-Aufgabe trägt (Study = die Frage in Klartext / Council = das Entscheiden /
   Archive = der Nachweis) — Vorschläge für Wortlaut und Platzierung.
3. **Council entrümpeln:** Rollentrennung Tafel ↔ „Vier Empfehlungen" und eine Ordnung
   der vier Mechanik-Blöcke (Empfehlungen, Revisionen, Zählwerk, Voten-Matrix), die die
   Kernaussage sofort lesbar macht und die Tiefe sauber staffelt.
4. **Archiv aufwerten:** Eingang + Ordnung, die Vollständigkeit würdig trägt; Entscheidung,
   ob Uneinigkeit eine Klartext-Ebene bekommt oder bewusst Wortlaut bleibt.
5. **Ausklapp-Disziplin:** Über alle Räume verteilt liegt viel hinter `<details>` (Frage
   wörtlich, Suchanfragen, Vorbehalte, volle Voten-Matrix, voller Dissens). Ist die
   Staffelung „Klartext sichtbar / Wortlaut einen Klick tief" konsequent und für den Laien
   navigierbar — oder gibt es zu viele Ausklapp-Ebenen?

**Nicht Gegenstand:** die Bühnenchoreografie, die Ergebnis-Tafel als Prinzip, die
FlowRail, die Bild-Assets, der Farbregister. Nur der textliche/strukturelle Raum-Inhalt.
