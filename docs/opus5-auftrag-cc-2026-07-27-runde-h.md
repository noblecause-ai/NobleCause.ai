# Auftrag an CC — Runde H: Die Zählmaschine erwacht, die Medaillons kreisen

**Von:** Opus 5 · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Vorlauf:** P10 (Maschine mit Podest) und P11 (Trommel) liegen freigestellt in
`docs/asset-originals/media/provenance/`. Damit sind §8 und §7 freigeschaltet.
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

---

## §1 · P10 einbauen — die Maschine wird eine Ebene

Keying wie gehabt, Ablage im Medien-Strang, Kleinauflösung mit.

P10 wird **deckungsgleich über die gemalte Maschine** im `hall`-Plate gelegt und ersetzt sie
optisch. Die gemalte bleibt im Plate stehen und liegt darunter — sie ist die Rückfallebene, falls
die Silhouette an einer Kante nicht ganz deckt.

**Registrierung am gerenderten AVIF messen**, nicht am Master: Podestbreite, Podest-Unterkante,
Trommelmitte. Sitzt die Silhouette nicht satt — sichtbarer Doppelrand, verschobene Podestkante —
**berichten, nicht nachbearbeiten.** Dann geht eine engere Bestellung raus.

Ab jetzt trägt diese Ebene die Verdeckung für §7 und die Bewegung für §8. Sie ist damit **nicht**
mehr Kulisse im Sinne des Kantenprinzips, sondern zweite Ebene — sie darf sich bewegen.

---

## §2 · §8 — der Zähl-Ruck

Der Hover-Kern (Hotspot, Aufwach-Licht, Plakette mit der Aggregationsregel, i18n, §0) ist gebaut.
Jetzt kommt der Ruck dazu, für den P11 bestellt wurde.

**Das Problem, das du gleich haben wirst:** Ein flaches Bild einer liegenden Trommel kann sich
nicht um seine Achse drehen. Wer P11 rotiert, bekommt ein kippendes Rad, kein rollendes.

**Der Weg, der trägt:** P11 liegt **über** P10, auf die Trommel-Silhouette **geclippt**, und wird
beim Hover **vertikal um etwa eine Ringhöhe verschoben** — die Oberfläche rollt, die Silhouette
steht. Was am Rand freigelegt wird, zeigt die identische Trommel aus P10 darunter; deshalb bleibt
der Übergang unsichtbar. Ein Schlag, kurz (≈ 220 ms), leicht überschwingend, dann Ruhe.

**Abnahme:** Die **Kanten** der Trommel bewegen sich nicht — nur ihre Oberfläche. Kein Spalt, kein
Aufblitzen an Ober- oder Unterkante. Ein Hover, ein Ruck; schnelles Hin und Her schaukelt nicht
auf. reduced-motion und No-JS: kein Ruck, Plakette steht.

Findest du einen besseren Weg: nimm ihn, aber die Abnahme bleibt.

---

## §3 · §7 — die Medaillons

Konzept unverändert (`opus5-konzept-...-durchgang-und-sitze.md` §7, Runde D §7). Jetzt baubar,
weil P10 als Vordergrund existiert.

- Billboard-Ellipse um die Maschine, b deutlich kleiner als a. Aus dem Winkel folgt die Tiefe,
  aus der Tiefe Skalierung (≈ 0,62 → 1,0), Helligkeit, ein Hauch Blur und `z-index`.
- **Die hintere Hälfte liegt unter P10**, die vordere darüber. Das ist der Punkt der ganzen
  Bestellung — ohne sichtbare Verdeckung wird nicht gebaut.
- Einflug nach dem Eintrittstakt der Pulte, von außerhalb des Bildrands, leichtes Überschwingen
  bei der Ankunft, dann ins Kreisen. Kein Blinken, kein Aufleuchten.
- Kreisen nur im Ruhezustand; auf `--retreat` weitet sich die Ellipse. Eine rAF-Schleife,
  pausiert bei `hidden` und außerhalb des Viewports. Umdrehung 40–60 s.
- **Der Modellname steht immer am Medaillon** — Plakettengrammatik wie Scout/Warden/Pulte. Das
  ist keine Gestaltungsfrage, sondern der Schutz gegen „Nightingale empfiehlt" statt „Gemini
  empfiehlt". Motiv- und Begründungstext bleiben draußen; sie kommen mit dem Explorer.
- §0: Ruhepositionen im prärenderten HTML; reduced-motion und No-JS zeigen die Medaillons still
  an ihren Bahnpunkten.

**Zusammenspiel mit §8:** Der Hover hält die Bahn nicht an. Steht ein Medaillon im Weg der
Plakette, weicht **die Plakette** aus, nicht das Medaillon.

---

## §4 · Reihenfolge und Abnahme

1. §1 P10 einbauen → Registrierungsmaße im Bericht.
2. §2 Ruck.
3. §3 Medaillons.

Je Schritt ein Commit. **Vor jeder visuellen Aussage die Vorstufe fahren:** frischer Build,
Konsole ohne Chunk-Fehler, Handler feuert — dann erst messen. Das gilt ab sofort für jede Runde.

Zusätzlich vor dem letzten Commit: alle drei Räume einmal durchgehen (Fahrt in jeder Tür, mobil
390, reduced-motion, No-JS). Wir sind nah am Ausliefern; ab jetzt kostet ein übersehener
Nebeneffekt mehr als die Prüfung.

Guardrails unverändert.
