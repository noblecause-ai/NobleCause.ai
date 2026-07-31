# Nachbestellung 2 · Scout + Warden Cutouts — Absichts-basiert (20.07.2026)

**Kontext:** Nachbestellung zu Serie 1b (`docs/codex-serie-1b-study-nachbestellung.md`),
Gate-Befund `docs/review/serie-1b-gate/checks.txt`. Die 1b-Lieferung ist inhaltlich und
stilistisch bestanden (§8, 7/7) und bleibt als Stil-/Posereferenz maßgebend — gescheitert
ist sie allein an der maschinellen Entfernbarkeit des Hintergrunds:

- Weiß/Hellgrau-Schachbrett kollidiert mit hellen Motiv-Pixeln (Schirm, Lampe, Papier) —
  Farbdistanz 0, kein globaler Key möglich.
- Der Generator hat den Hintergrund mitgemalt: Lichtschein um Schirm/Lampe (Scout,
  2,66 % Rest nach Rand-Flood-Fill; Steward-Nachmessung), Bodennebel um
  Tischbeine/Pult-Sockel (beide).
- Folge: Weder Flood-Fill noch Chroma-Key trennen Motiv von Backdrop, und ein reiner
  Farbwechsel (Magenta) würde im ausgebrannten Schein ebenfalls gegen Weiß kollabieren.

**Deshalb Absichts- statt Motiv-Beschreibung** (Hinweis des Auftraggebers: der
ChatGPT-Kontext kennt die bisherigen Runden — die Absicht erklären statt nur das Bild):

---

## Paste-fertiger Bestelltext (DE, in denselben ChatGPT-Kontext)

> Die beiden Figuren aus der letzten Runde — der Scout am Schreibtisch mit leuchtendem
> Schirm, der Warden am Pult — sind inhaltlich und stilistisch genau richtig. Bitte
> Motiv, Pose, Kleidung, Tische, Lichtstimmung und Malstil **exakt beibehalten**.
>
> Was wir mit den Bildern vorhaben: Wir stellen die Figuren **per Programm frei** —
> ein Flood-Fill vom Bildrand entfernt alles in einer einheitlichen Hintergrundfarbe —
> und montieren sie anschließend in einen gemalten dunklen Raum. Die letzte Lieferung
> scheiterte daran, dass der Hintergrund mitgemalt war: Licht aus Schirm und Lampe fraß
> als Schein in den Hintergrund, Nebel verwischte ihn am Boden, und das Schachbrett
> hatte dieselbe Helligkeit wie Schirm und Papier. Ein programmierbarer Hintergrund
> muss deshalb **vom Motiv vollkommen unbeleuchtet und unbemalt** bleiben.
>
> Bitte beide Figuren neu, mit diesen Hintergrund-Regeln:
>
> 1. **Hintergrund = eine einzige flache Volltonfarbe: gesättigtes Magenta (#FF00FF).**
>    Wie eine nahtlose Fotowand: kein Muster, kein Schachbrett, kein Verlauf, keine
>    Vignette, keine Textur, kein einziger Pinselstrich. Magenta kommt im Motiv
>    nirgends vor — Schirm, Papier, Hemd und Lampenlicht dürfen gern hell bleiben,
>    sie kollidieren mit Magenta nicht.
> 2. **Kein Licht auf den Hintergrund:** Schirm und Lampe leuchten nur das Motiv an
>    (Gesicht, Hände, Tischplatte). Kein Glow, Halo, Schein oder Lichtkegel, der über
>    die Silhouette hinaus in den Hintergrund austritt. **Kein Schattenwurf** auf den
>    Hintergrund. **Kein Boden und kein Bodennebel** — Tischbeine und Schuhe enden
>    sauber, ohne Kontaktschatten, als stünde das Möbel direkt vor der Fotowand.
> 3. **Komposition wie geliefert:** Ganzfigur hinter dem Tisch, vollständig sichtbar
>    inklusive Schuhe und Tischbeine, ≥ 3 % Abstand zu allen Bildrändern, Hochformat
>    1024 × 1536, eine Figur pro Bild.
>
> Kurz: identische Figuren wie in der letzten Lieferung, aber vor einer toten,
> unbeleuchteten Magenta-Fotowand — der Hintergrund ist keine Bühne, sondern
> Verpackung, die entfernt wird.

---

## Abnahme-Kriterien bei Lieferung (Gate 1c, Messung statt Sichtung allein)

1. **Backdrop-Flachheit:** Eckproben uniform (SAD < 10); kein Luminanz-Gradient > 8
   über je 100 px reiner Hintergrund-Zeile/-Spalte; untere 15 % des Bildes außerhalb
   der Silhouette = reine Schlüsselfarbe (kein Nebel, kein Schatten).
2. **Kollisionsfreiheit:** Mindest-Farbabstand (SAD RGB) irgendeines Motiv-Pixels zur
   Schlüsselfarbe > 60 — insbesondere Schirm, Papier, Lampenschirm, Hemd.
3. **Key-Test:** einfacher globaler Distanz-Key (kein Flood nötig) lässt < 0,3 %
   Rest-Opazität, keine zusammenhängende Rest-Komponente > 500 px außerhalb der
   Silhouette; Kante ohne Halo (1-px-Feather ausreichend).
4. **Motiv-Konstanz:** Pose, Tische, Schirm, Stil deckungsgleich mit den 1b-Mastern
   (Kontaktbogen 1b-Master ↔ 1c-Lieferung, §8-Checkliste).
5. C2PA vorhanden; Maße 1024 × 1536; Ablage dann `provenance/serie-1c-study/`.

Bei Teilerfolg (nur eine Figur sauber): saubere annehmen, andere einzeln nachrollen —
Neugenerierung ist ausdrücklich billig und mehrfach erlaubt (Steward, 20.07.2026).

## Verworfene Alternativen (Begründung)

- **Retusche der 1b-Alphas:** Scout-Defekt sitzt um Schirm/Lampe (empfindlichstes
  Motivteil); gemalter Nebel zwischen Tischbeinen ist per Pipeline nicht vom Motiv
  trennbar; manuelle Maske wäre Grafiktool-Arbeit außerhalb der Mess-Pipeline.
- **Magenta-Neugenerierung ohne Absichts-Klausel:** löst die Distanz-0-Kollision,
  nicht die Ursache (Generator beleuchtet/bemalt den Backdrop; ausgebrannter Schein
  kollabiert jeden Chroma-Ton gegen Weiß — Steward-Messung, 20.07.2026).
