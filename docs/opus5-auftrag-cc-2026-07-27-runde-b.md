# Auftrag an CC — Runde B: Archiv-Korrekturen + Council abräumen

**Von:** Opus 5 (Architekt) · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Vorlauf:** Runde A erledigt (`c03a120`), Serie-5-Kulisse eingebaut.
**Arbeitsweise unverändert:** Plan → Freigabe → Bau → Browser-Verifikation → Bericht.
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

---

## Vorbemerkung — Runde A ist angenommen

Der Strang-Bericht ist überzeugend und die Empfehlung wird übernommen:

- **`app.html` + `FlowRail`/`RoomHero`-Löschung + `EmblemLegend`/`RecommendationCard`/
  Journal-Seiten = ein eigener Commit** („Rooms-Aufräumen / Titelbereich"). **Freigabe erteilt**,
  am Ende dieser Runde zu setzen.
- **`site/static/schedule.json` zurücksetzen** und zusätzlich gitignoren — ein Build-Artefakt
  gehört nicht in den Baum. Bitte `prebuild` im Bericht kurz bestätigen.
- **Medien-Strang** bleibt gebündelt und ungetestet liegen bis zur eigenen Runde vor Go-Live.
  Der Befund „blockiert: JA" ist korrekt und bleibt auf der Go-Live-Liste.

Auch der vorgezogene Serie-5-Einbau war richtig — mit allen drei Bildern in der Hand wäre eine
eigene Runde Leerlauf gewesen.

---

## §1 · Das Pult fährt von rechts ein, nicht von unten

Aktuell nimmt das Pult seinen Platz von der **unteren** Kante ein. Es soll die Bühne von der
**rechten Kante** betreten — dieselbe Grammatik wie der **Warden im Study**: Schiene an der
Seitenkante, horizontale Einfahrt, Rückzug horizontal über `--retreat`, Staffelung über `--i`.

**Begründung:** Der Warden gibt den Takt für schweres Mobiliar vor, das *ankommt*. Von unten
aufzutauchen liest wie Einblenden; von der Seite hereinzugleiten liest wie Hereinstellen. Im
Archiv, dem Raum des Verwahrens, ist das die richtige Geste — und die drei Räume sprechen dann
dieselbe Bewegungssprache.

Der Lampen-Glow bleibt unverändert und fährt mit.

**Abnahme:** Bewegungsprofil deckungsgleich mit dem Warden (Dauer, Kurve, Rückzugsrichtung);
kein horizontaler Overflow, keine Scrollbar; Ruheposition steht im prärenderten HTML;
reduced-motion und No-JS zeigen den statischen Endzustand (§0).

---

## §2 · Das Regal-Asset links entfällt ersatzlos

Der Karteikasten an der linken Flanke (`actors/register.avif`) wird **vollständig entfernt** —
Schiene, Figur, `registerAlt` in `i18n/de.js` und `en.js`, die zugehörige Tafel-Klemme und die
Testzeile, die ihn prüft. Die linke Flanke bleibt leer.

**Begründung:** Zwei Möbel an beiden Flanken schließen die Mitte zu und drücken auf die
Ergebnis-Tafel. Ein einzelnes ankommendes Möbel ist die stärkere Geste, und die Klemmung
gegen die Tafel (395/403 px) entfällt damit ersatzlos statt knapp gelöst zu werden. Das Archiv
ist der ruhigste der drei Räume — es verträgt Leere.

Die Datei `actors/register.avif` **bleibt liegen** (untracked, Medien-Strang) — sie kann für die
Council-Sitze oder eine spätere Runde noch gebraucht werden. Nur der Einbau geht raus.

**Abnahme:** kein Verweis mehr auf `register` in Komponenten, i18n, Tests; Tafel steht frei;
Mobil unverändert ohne Overflow.

---

## §3 · Die Spaltansicht gleicht nicht den anderen Räumen

Im Archiv ist der geöffnete Zustand derzeit **der geschlossene Komposit plus ein warmer Glow an
der Mittelfuge** — außerhalb byte-identisch, technisch sauber, aber es *öffnet* sich nichts.
Study und Council zeigen an dieser Stelle eine sichtbar geöffnete Tür mit Tiefe dahinter. Der
Rundgang bricht damit im dritten Raum.

**Auftrag:** Den Archiv-Spalt auf das Niveau der anderen beiden Räume bringen — **ohne neue
Bestellung.** Der Weg dahin steht dir frei; die naheliegende Fassung: die gekeyten **P8-Flügel
sind eine eigene Ebene** und lassen sich auseinanderfahren (Fuge öffnet sich, Flügel wandern
je zur Laibung, leichte Perspektivneigung), dahinter die bereits vorhandene warme Tiefe. Das ist
genau die Ebenentrennung, für die P7/P8 bestellt wurden — sie ist ohnehin da.

**Wichtig:** Das ist der **Zwischenstand**, nicht der echte Durchgang. §6 (Kamerafahrt durch die
Öffnung) kommt als eigener Auftrag und wird diese Ebene weiterverwenden — bitte so bauen, dass
die Flügel-Ebene später übernommen werden kann, statt sie als Einwegeffekt zu verdrahten.

**Abnahme:** außerhalb der Türkontur weiterhin keine Bewegung; der Übergang liest in allen drei
Räumen als dieselbe Geste; reduced-motion springt ohne Zwischenbild.

---

## §4 · Council-Korrekturen (aus Runde A übernommen)

**§4.1 Crossfade** — `hall-door-open` weicht außerhalb der Tür um 5,86 / 17,96 % ab. Auf das
gefederte Tür-Composite umstellen, Ziel: Archiv-Niveau. **Study nicht anfassen** (0,78 / 0,65 %).

**§4.2 Sitzzeilen** — `figcaption` an die Oberkante des Pults, `z-index` über dem Bild
(`.pult img { z-index: 1 }`-Falle), Vignette statt Kasten, exakt wie Scout/Warden (`c87cb97`).
Kein neuer Text, keine neue i18n-Zeile.

---

## §5 · Reihenfolge und Commits dieser Runde

1. §1 + §2 + §3 (Archiv) → ein Commit.
2. §4.1 + §4.2 (Council) → ein Commit.
3. Rooms-Aufräumen (`app.html`, Löschungen, Kleinänderungen) → ein Commit.
4. `schedule.json` zurücksetzen + gitignoren.

**Kein Push. Kein Medien-Commit. Kein Türdurchgang, keine Sitze um die Zählmaschine** — beide
hängen an derselben Übergangsebene und kommen als eigener Auftrag, sobald das Konzept steht.
Die Protokollseiten bleiben unberührt.

---

## §6 · Guardrails (unverändert)

Guard-Hook auf `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`, `schema/**`,
`prompts.py`; Daten nur über Datenbranch + `--ff-only`; **nie `--no-verify`**. §0-Verfassung:
voller Inhalt ohne JS und bei `prefers-reduced-motion`; die Bühne verzögert und bewegt, sie
erzeugt und versteckt nie. Versiegelte Datennaht. Geometrie am gerenderten AVIF messen.
