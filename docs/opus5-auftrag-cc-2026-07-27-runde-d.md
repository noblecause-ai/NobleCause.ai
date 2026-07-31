# Auftrag an CC — Runde D: Die Zählmaschine erwacht (§8) und wird umkreist (§7)

**Von:** Opus 5 (Architekt) · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Vorlauf:** Runde C abgeschlossen — der Zyklus Archiv → Study → Council → Archiv trägt in allen
drei Türen den echten Durchgang samt Ruhe-Stapel. **Steward-Urteil: der Wow-Effekt ist da.**

**§2-Council-Commit: Freigabe erteilt.** Setzen, Guard mit, kein Push; die drei neuen Medien
(`hall-wall-hole.avif`, `hall-leaf-left/right.avif`, `archive-display-lo.avif`) bleiben im
untracked Strang.

Der Freischnitt hat in beiden Räumen getragen und war damit die richtige Wahl gegen die
Bestellung — RGB byteidentisch, Alpha nur in der Tür-Bbox, kein Nachmessen. Zwei Bestellungen
und zwei Runden Nachmessen gespart.

---

## §8 · Die Zählmaschine bekommt ein Mouseover

**Steward-Auftrag.** Die Tür hat jetzt eine Hover-Antwort — sie zeigt den Nachbarraum. Die
Zählmaschine steht daneben und antwortet auf nichts. Das liest wie ein Fehler, sobald die Tür
funktioniert.

### Was der Hover zeigen soll

Die Tür beantwortet beim Hover die Frage **„wohin?"**. Die Zählmaschine muss die Frage
**„was passiert hier?"** beantworten — nicht mit einem Ergebnis, sondern mit ihrer **Regel**:

> **Zwei gleiche Nennungen ergeben eine Empfehlung.**

Das ist die Aggregationsregel des Gremiums, und sie steht heute **nirgends auf der Seite**. Die
Tafel zeigt „· 2 von 3", ohne je zu sagen, warum 2 von 3 genügen. Der Besucher, der genau
hinsieht, stolpert genau hier — und die Maschine ist der Ort, an dem die Antwort hingehört.

**Formulierung ist Steward-Sache** (Wortlaut oben ist ein Vorschlag), aber die Gattung steht
fest: eine **Prozessaussage**, kein Ergebnis, keine Zahl aus einer Sitzung. Damit bleibt die
versiegelte Datennaht unberührt — dieselbe Kategorie wie „vier Bereiche" oder „jeden
Montagmorgen".

### Wie er aussieht

- **Die Maschine erwacht:** warmes Licht steigt in ihr auf, die Zählglieder rücken **eine**
  Stufe weiter und bleiben dort. Kein Rattern, kein Dauerlauf, keine Endlosschleife — ein
  einzelner Ruck und Licht. Die Räume arbeiten mit Gleiten und Licht.
- **Eine Plakette** in der bestehenden Grammatik: Vignette statt Kasten, Kopflinie, `text-shadow`
  — exakt wie Scout, Warden und die Pultplaketten (`c87cb97`, `00b0d1c`). **Keine neue
  Gestaltungsfamilie für ein einzelnes Element.**
- Der Text steht als echter Inhalt im DOM (i18n de/en), nicht als `title`-Attribut. Ohne JS und
  bei `prefers-reduced-motion` ist er lesbar da; nur Licht und Ruck entfallen.

### Was der Hover NICHT tut

- **Kein Klickziel.** Die Maschine wäre der natürliche Weg zu den Protokollen — aber die
  Protokollseiten tragen noch das alte Dokumentlayout. Ein Klick, der aus einem gebauten Raum in
  eine ungestaltete Seite führt, beschädigt beide. **Das Klickziel kommt, wenn der
  Protokoll-Explorer steht** — bitte so bauen, dass es dann nachgerüstet werden kann, ohne die
  Plakette umzubauen.
- Keine Zahl aus einer Sitzung, kein Live-Zählstand, keine Animation, die weiterläuft.

### Abnahme

Hover einmal, Ruck einmal — auch bei schnellem Hin und Her kein Aufschaukeln; Plakette liest auf
dem dunklen Maschinengrund; kein Layout-Shift; Fokusreihenfolge unverändert (die Maschine ist
Kulisse, kein Bedienelement); reduced-motion und No-JS geprüft.

---

## §7 · Die Sitze um die Zählmaschine

**Steward-Entscheid gefallen: die drei Modell-Medaillons**, nicht Sitzmöbel. Runde Objekte sind
richtungslos und als Billboard ehrlich; ein Stuhl müsste auf der Rückseite der Ellipse seine
Rückseite zeigen. Kein neues Asset, und inhaltlich richtig: **drei Stimmen kreisen um die
Zählung.**

Das Konzept steht in `docs/opus5-konzept-2026-07-27-durchgang-und-sitze.md` §7 und gilt
unverändert. Kurzfassung der bindenden Punkte:

- **Billboard-Ellipse** um die Maschine, b deutlich kleiner als a (Aufsicht von leicht oben).
- Aus dem Winkel folgt die **Tiefe**, und aus der Tiefe **Skalierung (≈ 0,62 → 1,0), Helligkeit,
  ein Hauch Blur und `z-index`** — die hintere Hälfte liegt **wirklich hinter** der Maschine.
  Das ist die Tiefenlogik aus dem Durchgang: **einmal geschrieben, zweimal benutzt.**
- **Einflug** nach dem Eintrittstakt der Pulte: von außerhalb des Bildrands, Ankunft mit leichtem
  Überschwingen, dann ins ruhige Kreisen. Kein Blinken, kein Aufleuchten bei der Ankunft.
- **Kreisen nur im Ruhezustand**; auf `--retreat` weitet sich die Ellipse und die Medaillons
  weichen an die Ränder — dieselbe Scrub wie alle Bühnenelemente, kein zweiter Mechanismus.
- **Eine Umdrehung 40–60 s.** Schneller zieht Aufmerksamkeit von der Tafel ab, und die Tafel ist
  der Zweck der Seite.
- **Eine** rAF-Schleife, pausiert bei `hidden` und außerhalb des Viewports.
- §0: Ruhepositionen im prärenderten HTML; reduced-motion und No-JS zeigen die Medaillons still
  an ihren Bahnpunkten.

### Zusammenspiel mit §8

Beide Elemente gehören derselben Maschine. **§8 zuerst bauen**, damit der Ruhezustand der
Maschine feststeht, bevor etwas darum kreist. Der Hover darf die Bahn nicht anhalten; das
Medaillon, das im Moment des Hovers vor der Maschine steht, darf die Plakette nicht verdecken —
falls doch, weicht die Plakette aus, nicht das Medaillon.

### Abnahme

Medaillons hinter der Maschine liegen sichtbar dahinter; kein Flackern der Stapelreihenfolge an
den Scheiteln; kein Overflow, keine Scrollbar; die Tafel bleibt frei; CPU im Ruhezustand niedrig;
reduced-motion und No-JS geprüft.

---

## §9 · Reihenfolge

1. §2-Council-Commit setzen.
2. **§8** Mouseover der Zählmaschine → Bericht, eigener Commit.
3. **§7** Medaillons → Bericht, eigener Commit.
4. Danach: **Protokoll-Explorer** — die letzte große Designlücke vor Go-Live. Ich schreibe das
   Konzept, während du §8 und §7 baust.
5. Vor Go-Live weiterhin offen: der gebündelte **Medien-Strang**.

---

## §10 · Guardrails (unverändert)

Guard-Hook; Daten nur über Datenbranch + `--ff-only`; **nie `--no-verify`**; kein Push.
§0-Verfassung: voller Inhalt ohne JS und bei `prefers-reduced-motion`; die Bühne verzögert und
bewegt, sie erzeugt und versteckt nie. Versiegelte Datennaht — das Frontend paraphrasiert nie.
Geometrie immer am gerenderten AVIF messen.
