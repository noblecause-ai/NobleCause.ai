> **Archiviert 2026-07-28 (CC) — Asset-Bestell-Prompt der Kimi-Serie, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie).

# Prompt an Kimi — Serie 1b liegt vor (inkl. Bewegungs-Ebene)

*(Copy-Paste ab hier)*

---

Serie 1b ist geliefert und liegt **direkt in `docs/`** (noch mit den ChatGPT-Dateinamen,
noch nicht einsortiert). Auftragsgrundlage ist `docs/codex-serie-1b-study-nachbestellung.md`;
die alte `docs/review/serie-1-gate/nachbestellung-cutouts.md` ist als **ÜBERHOLT** markiert
und nicht mehr zu verwenden.

## Die sieben Dateien

| Datei (in `docs/`) | Maße | vermutlich |
|---|---|---|
| `ChatGPT Image 20. Juli 2026, 04_00_57 (1).png` | 1672×941 | Plate A quer (Tür zu) |
| `ChatGPT Image 20. Juli 2026, 04_00_57 (2).png` | 1672×941 | Plate B quer (Tür offen) |
| `ChatGPT Image 20. Juli 2026, 04_00_58 (3).png` | 1024×1536 | Plate hoch |
| `ChatGPT Image 20. Juli 2026, 04_00_58 (4).png` | 1024×1536 | Plate hoch |
| `ChatGPT Image 20. Juli 2026, 04_00_58 (5).png` | 1024×1536 | The Scout (Cutout) |
| `ChatGPT Image 20. Juli 2026, 04_00_59 (6).png` | 1024×1536 | The Warden (Cutout) |
| `ChatGPT Image 20. Juli 2026, 04_00_59 (7).png` | 1536×1024 | Wolkenebene (neu) |

Die Zuordnung ist meine Vermutung aus Maßen und Sichtprüfung — **bitte visuell bestätigen**,
welche Hochformat-Datei A (zu) und welche B (offen) ist.

## Mein Vorbefund (bitte gegenprüfen, nicht übernehmen)

**Inhaltlich sieht Plate A quer richtig aus:** die beiden leeren Tische sind weg, zwei
Pflanzen sind da (große Topfpflanze links vom Fenster, kleiner Farn auf der Fensterbank),
Tafelzone links vollständig frei, Tür mittig, Mondfenster rechts, unteres Drittel ruhig.
Der Scout ist als **Rechercheur am Schreibtisch mit leuchtendem Schirm** umgesetzt — die
Fehlerzählung mit dem Fernrohr ist behoben.

**Technisch gibt es aber wieder einen Befund, und diesmal einen kuriosen:**
Alle sieben Dateien sind `mode=RGB`, **kein Alphakanal**. Bei den beiden Cutouts und der
Wolkenebene ist das Schachbrettmuster, das nach Transparenz aussieht, **in die Pixel
gemalt** — abwechselnd RGB 254 und 239 bei den Cutouts, dunkelgraue Kacheln bei der Wolke.
Das Modell hat also ein *Bild von* Transparenz erzeugt statt echter Transparenz.

Das ist ausdrücklich mein Befund und kein Urteil über die Bilder — prüf es selbst nach und
widersprich, wenn du etwas anderes misst.

## Wozu die Wolkenebene da ist (Kontext)

Der Steward möchte, dass die Szene im **Ruhezustand leise weiterlebt** — nicht mehr
Choreografie, sondern das Gegenteil: etwas, das läuft, wenn nichts passiert. Zwei Ideen
stehen dahinter:

1. **Wolkenzug am Fenster** — dafür ist die neue Ebene bestellt (horizontal kachelbar
   angefragt, damit ein Endlos-Lauf ohne Naht möglich ist).
2. **Leichtes Lichtflackern** an den Lampen, im Archiv am stärksten.

Gedachte Rollenteilung: **Choreografie = der Eintritt, Ambient = der Ruhezustand.**

## Was gilt und was nicht

**Es bindet dich** — wie immer — nur das, was ohnehin Verfassungsrang hat: `prefers-reduced-motion`
stellt jede Ambient-Bewegung still, die Byte- und MP-Deckel aus §4 gelten unverändert
(die Wolkenebene zählt mit), der No-JS-Boden bleibt unberührt, und nichts davon darf
Aufmerksamkeit von der Tafel wegziehen. Faustregel des Stewards: Wenn man den Effekt beim
**ersten** Hinsehen bemerkt, ist er zu stark.

**Die Umsetzung ist deine Entscheidung.** Ausdrücklich keine Vorgabe von uns — weder zur
Technik noch zur Ebenenführung noch zum Freistellen. Ein paar Gedanken nur als Angebot,
gern verworfen:

- Fürs Flackern bräuchte es vermutlich gar kein Asset — überlagerte Verläufe mit
  ungleichen Periodenlängen wären eine Möglichkeit, damit kein mechanischer Rhythmus
  entsteht.
- Beim Freistellen ist die Ausgangslage günstiger, als sie klingt: Das gemalte Schachbrett
  ist flach und regelmäßig, die Motive sind dunkel bzw. hell dagegen. Ob sich das
  mechanisch lösen lässt oder ob eine dritte Bestellung ehrlicher ist, beurteilst du
  besser als wir.
- Ob die Wolke wirklich nahtlos kachelt, weiß ich nicht — das ist eine der Fragen, die dein
  Gate beantworten sollte.

## Was ich mir wünsche

Erst prüfen, dann berichten, dann bauen — dieselbe Reihenfolge wie bei Serie 1, die gut
funktioniert hat. Bericht mit: Zuordnung der Dateien, Alpha-/Kachel-Befund mit Messwerten,
eine grobe Montage-Probe der Cutouts über der neuen Plate A (Maßstab, Bodenlinie,
Lichtrichtung), und deine **Empfehlung**, wie es weitergehen soll — inklusive der Option
"nachbestellen" mit Begründung.

Wenn dir bei der Ambient-Bewegung ein besserer Weg einfällt als der über die gelieferte
Ebene: sag es. Der Zweck ist Leben in der ruhenden Szene, nicht diese eine Datei.
