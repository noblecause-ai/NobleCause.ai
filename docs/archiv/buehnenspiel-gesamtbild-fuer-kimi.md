> **Archiviert 2026-07-28 (CC) — Pre-CC-Bühnenspiel-Entwurf, durch die späteren Runden abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# Das Bühnenspiel — Gesamtbild der Site (Zusammenfassung für Kimi)

**Zweck:** Die ursprünglich vom Steward beschriebene Bühnen-Darstellung der *ganzen*
Site, so originalgetreu wie möglich zusammengefasst — als Orientierung beim Bau, damit
die Einzelteile (Plates, Cutouts, Beats, Röhre, Tafel) wieder auf das eine Bild
zurückführen, aus dem sie stammen.

**Quellenlage, ehrlich:** Die Urfassung wurde im Gespräch formuliert und liegt nicht als
eigenes Dokument vor. Diese Zusammenfassung ist aus den Dokumenten rekonstruiert, die
sie festgehalten haben — `fable-2026-07-19-buehnenspiel-synthese-umlauf--mit-runde3-codex.md`
(§0–§5, kanonisch bei Konflikt) und `opus-buehnenspiel-plan.md` (§2–§6). Wo der
abgeschlossene Umlauf die Urfassung bewusst überstimmt hat, steht es dabei.

---

## Das Bild dahinter

**Die Site ist ein Haus mit drei Räumen, und jeder Aufruf ist ein Bühnenauftritt.**
Man betritt einen Raum, das Licht geht an, die Beteiligten treten auf, die Antwort
erscheint auf der Tafel, und eine Tür führt weiter. Das Verfahren, über das die Site
berichtet, wird nicht erklärt — es wird **gespielt**.

Die drei Räume sind die drei Stationen des Verfahrens:

| Raum | Route | Was hier geschieht |
|---|---|---|
| **The Study** | `/` | Die Frage wird gestellt, Belege werden gesammelt |
| **The Council** | `/ratssaal/` | Die Stimmen beraten getrennt, dann wird gezählt |
| **The Archive** | `/archiv/` | Alles wird veröffentlicht und aufbewahrt |

## Die Bühnenelemente

Jeder Raum ist aus denselben Teilen gebaut — gleiche Grammatik, eigener Inhalt:

- **Das Bühnenbild** (Plate): der gemalte Raum. Tafelzone links, **Tür zentral**,
  Mondfenster rechts als kalter Gegenpol, ruhige dunkle Zone unten für den Text.
- **Die zweite Ebene**: die Beteiligten dieses Raums, als freigestellte Figuren, die
  auf Schienen einfahren.
- **Die Ergebnis-Tafel**: die Schiefertafel links, auf der die Antwort steht.
- **Die Prozess-Röhre**: sechs Kugeln, die zeigen, wo im Verfahren man steht.
- **Die Tür**: der Weg in den nächsten Raum, mitten im Bild.

## Der Auftritt (~2 Sekunden, alle Räume gleich)

| Takt | Was | Warum |
|---|---|---|
| 0 | Bühnenbild blendet auf | Der Raum entsteht |
| 1 | Zweite Ebene fährt auf Schienen ein | Die Beteiligten treten auf |
| 2 | **Ergebnis erscheint auf der Tafel (~1,2 s)** | Die Antwort — früh, nicht am Ende |
| 3 | Titel und Erklärtext setzen sich | Die Einordnung |
| 4 | Röhre füllt sich | Wo wir im Verfahren stehen |

Die Takte überlappen um ~50 ms — es soll wie ein Atemzug wirken, nicht wie eine
Abarbeitung. Danach steht die Szene still: **der Lock.**

> **Wichtig, und im Umlauf gegen die Urfassung entschieden:** Der Lock ist ein
> **visueller Ruhezustand, nie ein gesperrter Eingabekanal.** Kein Scroll-Hijacking.
> Wer während des Aufbaus scrollt, äußert eine Absicht — die Choreografie **springt
> dann in ihren Endzustand**, statt Beats nachzuspielen.

Die Haltung des Stewards zur Dauer ist ausdrücklich: **Wer die Ergebnisse sehen will,
muss so viel Geduld mitbringen.** Der Auftritt wird nicht wegoptimiert.

## Die zweite Ebene je Raum

- **The Study:** The Scout von links, The Warden von rechts — jeder mit seinem Tisch
  und seiner Lampe. *(Das sind die Cutouts aus Serie 1b.)*
- **The Council:** die Lesepulte fahren von unten in den Ring und nehmen ihre Plätze
  ein, die Lichter gehen nacheinander an. Das dramatisiert die Kernaussage des Raums:
  *getrennte, gleichrangige Stimmen.*
  **Auflage:** EIN Pult-Cutout, N-fach gerendert aus `modelTracks.length` — keine
  anbieterspezifisch gemalten Pulte. Das hält die Fünf-Sitze-Zukunft offen und wahrt
  die Vorwegnahme-Sperre.
- **The Archive:** die Registerfächer füllen sich, Sitzungen laufen von unten in die
  Regale. Das Archiv wächst, während man es betritt.

## Die Tür

Die Tür liegt zentriert im Plate — deshalb die harte Kompositionsauflage „Türmitte
±5 %". Darüber liegt als eigene Ebene das **Türblatt** (Crop aus dem eigenen Plate,
nicht separat generiert — pixelgenaue Passung statt Generierungs-Glücksspiel).
Dahinter, maskiert auf die Öffnung, der nächste Raum.

- **Ruhe:** geschlossen, ein schmaler warmer Lichtspalt.
- **Hover/Fokus:** das Türblatt schwenkt ~8° auf, der Spalt wächst, mehr vom nächsten
  Raum wird sichtbar.
- **Mobil:** kein Hover — der Spalt zeigt dauerhaft einen Schimmer, Antippen navigiert.

Die Tür ist ein **echter `<a href>`**. Ohne JS navigierbar, tastaturbedienbar, mit
Fokusring. Das Schwenken ist die Zugabe, nie die Funktion.

## Der Übergang — durch die Tür hinein

Gelesen als *Hineingehen*, nicht als Herauszoomen. ~2,0 s vorwärts, ~1,2 s zurück
(Zurück ist Orientierung, nicht Erlebnis):

1. **Die Bühne räumt** — die Schienen-Elemente ziehen sich zurück, die Röhre weicht.
2. **Das Türblatt schwingt auf.**
3. **Durchgang** — die Szene skaliert auf den Türrahmen zu (`transform-origin` =
   Türmitte), dunkelt sanft ab, die Öffnung reißt als Blende auf.
4. **Ankunft** — im neuen Raum läuft der Auftritt ab Takt 0.

**Die Ergebnisse verschwinden dabei nie.** Bei der Fahrt komprimiert die Tafel zu einer
schmalen messinggerahmten Leiste oben links, **reist mit** und expandiert im Zielraum
auf dessen Tafelfläche. Die Aussage dahinter: *dieselbe Sitzung wandert durchs Haus.*

## Die Prozess-Röhre

**Der Röhrenstand ist eine Eigenschaft des Raums, keine Erinnerung an den Weg.**

| Raum | gefüllt | blass |
|---|---|---|
| The Study | Frage, Belege | die übrigen vier |
| The Council | + Drei Antworten, Umdenken, Zählen | Veröffentlichen |
| The Archive | alle sechs | — |

Die Animation ist die **Differenz** zum Vorzustand: Was neu gefüllt ist, rollt herein;
was wegfällt, rollt hinaus. Daraus folgt gratis, dass Rückwärtsgang und Direkteinstieg
korrekt sind, ohne Sonderfälle. Ohne JS steht der richtige Stand statisch da.

Jede Kugel trägt Emblem, Namen und Erklärsatz — die Röhre ist Fortschrittsanzeige
**und** Erklärung des Verfahrens zugleich.

## Mobil — dieselbe Erzählung, andere Physik

Im Hochformat gibt es kein Links und Rechts, aus dem Akteure einfahren könnten. Also
wird die Dramaturgie **vertikal**, nicht geschrumpft: die zweite Ebene steigt von
unten, die Tafel schiebt sich von oben ein und rastet. Kürzere Wege, gleiche
Reihenfolge. Die Plates sind **eigene Hochformat-Kompositionen**, keine Desktop-Crops.

## Topologie — Rundgang als Erzählung, Karten als Freiheit

Die **In-Szene-Tür** führt immer eine Station weiter: Study → Council → Archive →
Study. Ein Raum, eine Vorwärtstür — das macht die Tür bedeutungsvoll. Die
**Tür-Karten** bleiben daneben bestehen und erlauben jeden Sprung; sie sind zugleich
der barrierefreie und der No-JS-Weg.

Die Inszenierung ist linear, die Navigation frei.

---

## Der Satz, an dem sich alles messen lässt (§0, Verfassungsrang)

> **Die Seite ist bereits vollständig, bevor das Spiel beginnt.
> Die Inszenierung verzögert und bewegt nur — sie erzeugt nichts und versteckt nichts.**

Ohne JS: das unchoreografierte, vollständige Dokument. `prefers-reduced-motion`:
derselbe Zustand. Bricht JS mitten in der Sequenz: es bleibt ein vollständiges
Dokument stehen.

Und der zweite Maßstab, der gleichrangig danebensteht: **Ein Achtzigjähriger muss in
30 Sekunden finden, wohin er spenden kann.** Die Lesbarkeit ist der Boden, nicht das
Ziel — das Bühnenspiel darf beeindrucken, aber der Weg zur Antwort darf nie länger
werden.
