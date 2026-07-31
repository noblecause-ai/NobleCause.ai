# Titelbereich — Neuordnung (Steward-Vorgabe, für Kimi)

**Grund:** Der Kopf jedes Raums trägt heute sechs verschiedene Typo-Behandlungen
übereinander (Eyebrow, h1, Lead, Pitch, Why-Link, Röhren-Erklärsatz) — zu viel, und der
Titel wirkt nach rechts verschoben. Ziel: **ein stabiler, immer zentrierter Kopf auf
jeder Seite + ein knapper, pro Raum wechselnder Teil darunter.** Bei Konflikt mit
`raum-content-final-fuer-kimi.md` §3.1/§4.1/§5.1 gilt dieses Dokument.

## Der stabile Teil — auf JEDER der drei Raum-Seiten identisch, immer viewport-zentriert

Genau **eine** Typo-Familie: dieselbe Schrift und Farbe wie die Überschrift für den
gesamten Block. Keine zweite Textfarbe, keine dritte Größe außer dem natürlichen
Größenabfall Überschrift → Fließtext.

```
Wo hilft meine Spende am meisten?              ← Überschrift (h1), etwas KLEINER als heute
Je ein KI-Modell verschiedener Familien prüft dieselben Belege und empfiehlt
öffentlich, wo eine Spende voraussichtlich am meisten bewirkt. Warum so umständlich?
                                                 ↑ gleiche Schrift/Farbe wie h1, nur kleiner
```

Regeln:
- **„Wo hilft meine Spende am meisten?"** ist die Überschrift **auf jeder Seite** (Study,
  Council, Archive), etwas kleiner als bisher. Sie ist der stabile Anker — der Besucher
  verliert die Kernfrage nie.
- Darunter der Erklärsatz **in derselben Schrift und Farbe** wie die Überschrift (nur
  kleiner). Kein Wechsel auf ein Grau/Creme, kein zweiter Font.
- **„Warum so umständlich?"** ist die **Fortsetzung desselben Satzes** — gleiche Zeile
  bzw. gleicher Absatz, gleiche Farbe/Schrift, **keine eigene Zeile, kein Gold-Link-Look**.
  Es bleibt ein natives `<details>`-Summary (ohne JS/Tastatur bedienbar), aber optisch
  Teil des Fließtexts (z. B. dezent unterstrichen + ▸, nicht als Akzentfarbe abgesetzt).
- **Immer viewport-zentriert** — nicht im Restraum neben der fixen Tafel zentriert. Die
  Tafel sitzt oben links und ist kürzer; der Kopf zentriert auf die volle Breite und
  läuft nicht mehr nach rechts weg.

## Der dynamische Teil — pro Raum wechselnd, an derselben Stelle darunter

Eingeblendet im selben Duktus wie die Prozess-Schritte (Fade-in):

```
STUDY                          ← EIN Wort, pro Raum wechselnd (nicht „The Study · das Vorzimmer")
Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu.   ← Raumerklärung, pro Raum
```

- **Nur EIN Wort** je Raum, nicht Name + Gloss zusammen. **Entschieden:** der englische
  Eigenname `Study` / `Council` / `Archive` — konsistent mit dem Namenssystem der Site.
  Kein „The", kein deutscher Gloss daneben.
- Darunter die **Raumerklärung**, pro Raum wechselnd — das sind die bereits definierten
  Raum-Leads:
  - Study: „Jede Sitzung beginnt hier — mit einer Frage und den Belegen dazu."
  - Council: „Getrennt abgestimmt, dann öffentlich gezählt. Was mehrfach genannt wird,
    wird Empfehlung."
  - Archive: „Jede Sitzung, vollständig und unverändert — Empfehlungen, Uneinigkeit,
    Kosten."
- Wort + Raumerklärung werden **an derselben Stelle** gerendert und wechseln nur den
  Inhalt je Raum (wie ein Rollenschild, das ausgetauscht wird).

## Was sich damit gegenüber `raum-content-final` ändert

- Der Pitch („Je ein KI-Modell …") wandert vom „nur im Study" in den **stabilen Kopf auf
  jeder Seite** — er erklärt das Ganze und darf überall stehen.
- Die drei Raum-Leads werden vom „Lead unter dem h1" zum **dynamischen Raumteil** (Wort +
  Erklärung) umgewidmet — Inhalt unverändert, nur Position/Rolle.
- Der Council-h1 „Wie … Modelle entscheiden" und der Archive-h1 „The Archive" **entfallen
  als eigene Überschriften** — die Überschrift ist überall „Wo hilft meine Spende am
  meisten?". Die Raum-Identität trägt das eine Wort. (a11y: weiterhin genau ein `<h1>` je
  Seite — die stabile Frage; das Raumwort ist untergeordnet, z. B. `<p>`/Eyebrow, nicht
  konkurrierende Überschrift.)

## NACHTRAG (2026-07-24) — Kopf muss ganz oben stehen UND beim Raumwechsel stabil bleiben

Steward-Befund nach dem ersten Umbau: Der stabile Kopf sitzt noch mittig im Hero und
**zoomt bei der Türfahrt mit dem Raum weg**. Er soll sich verhalten wie die
Ergebnis-Tafel und die Prozess-Röhre — ein fester Rahmen, der bleibt, während der Raum
darunter wechselt.

Zwei Korrekturen:

1. **Position: ganz oben.** Der stabile Kopf (h1 „Wo hilft meine Spende am meisten?" +
   Pitch + „Warum so umständlich?") sitzt am **oberen Rand des Viewports**, nicht vertikal
   zentriert im Hero. Weiterhin horizontal viewport-zentriert.
2. **Stabil über den Raumwechsel — geteiltes Element wie die Tafel.** Der Kopf bekommt ein
   eigenes `view-transition-name` (z. B. `masthead`) und eine Gruppen-Regel analog zur
   Tafel:
   ```css
   .room-plaque .stable-head { view-transition-name: masthead; }
   @media (prefers-reduced-motion: no-preference) {
     ::view-transition-group(masthead) { animation-duration: 2s; } /* bleibt stabil, zoomt NICHT mit root */
     :root[data-nav-dir='back']::view-transition-group(masthead) { animation-duration: 1.2s; }
   }
   ```
   Der Kopf ist auf allen drei Räumen textgleich (fixe i18n-Copy) — dadurch matchen alt/neu
   und er bleibt bei der Fahrt ruhig stehen, während `::view-transition-old/new(root)` den
   Raum darunter zoomt. Genau das Muster, das die Tafel (`board`) schon nutzt.

**Nur der stabile Kopf ist geteilt/stabil.** Der dynamische Teil darunter (Raumwort
`Study/Council/Archive` + Raum-Lead) bleibt per-Raum und blendet weiter ein (kein
`view-transition-name` — er SOLL wechseln). So entstehen drei ruhende Rahmen (Kopf oben ·
Tafel oben-links · Röhre unten) und dazwischen wechselt sichtbar nur Szene, Raumwort und
Raum-Lead.

Abnahme: Screenshot mitten in der Fahrt Study→Council — der Kopf steht pixelstabil, die
Szene zoomt. No-JS/reduced-motion: Kopf steht ohnehin fest (kein VT), vollständig.

## Doppelte Prozess-Darstellung — ENTSCHIEDEN: FlowRail entfernen
Tube (Röhre) und FlowRail („So läuft es") zeigten beide alle sechs Schritte — Redundanz.
**Die FlowRail „So läuft es" entfällt** (in allen drei Räumen). Die Röhre bleibt als
einzige Prozess-Darstellung; sie trägt laut Ursprungs-Design bereits Emblem, Name und
Erklärsatz je Kugel — bei Hover/Fokus sichtbar, damit die Erklärung, die die FlowRail
trug, nicht verloren geht. Prüfen, dass der Erklärsatz je Kugel per Tastatur erreichbar
ist und ohne JS ein sinnvoller Grundzustand bleibt (§0). Der Röhren-Erklärsatz, der heute
lose unter der Röhre steht (z. B. „Der Späher sammelt Studien …"), wandert damit an die
Kugel bzw. entfällt als separate Zeile — eine Typo-Behandlung weniger im Kopf.
