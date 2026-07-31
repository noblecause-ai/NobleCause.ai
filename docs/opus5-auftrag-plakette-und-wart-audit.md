# Zwei Aufträge: Akteur-Plakette (Bau) und Wart-Mechanismus (Audit)

**Von:** Opus 5 (Architekt/Review) · **Für:** CC · **Datum:** 2026-07-24
Teil A ist ein Bauauftrag. **Teil B ist ausdrücklich KEIN Bauauftrag** — nur Befunde.

---

# Teil A · Die Akteur-Plakette an die Kopflinie

## A1 · Befund

`StudyActors.svelte`, `.actor figcaption`:

```css
position: absolute;
left: 50%;
bottom: -0.4rem;
transform: translate(-50%, 100%);   /* hängt UNTER dem Akteur-Kasten */
```

Der Akteur-Kasten endet an der Schienen-Unterkante. Die Plakette ragt mit ihrer **eigenen
Höhe** darunter — in das schmale Band zwischen Figurfuß und Viewport-Rand, in dem bei
niedriger Höhe auch die Prozess-Röhre sitzt. Verfügbar sind dort je nach Zweig nur
**2–18 svh**; die Plakette braucht drei Zeilen (~4,5 rem). Deshalb ist sie „zu weit unten".

Über den Köpfen ist dagegen viel Platz: Der Akteur-Kasten beginnt je nach Zweig bei
**39–49 svh** von oben. Der Anker gehört also nach oben — mit einer Einschränkung, siehe A3.

## A2 · Die Kopflinie messen, nicht schätzen

Du hast für Paket 1 einen **Canvas-Alpha-Scan am gerenderten AVIF** gebaut und damit die
Fußlinien bestimmt (Scout 0,8202 — deckungsgleich mit dem im Code geführten 0,82, Methode
damit validiert; Warden 0,8099). **Dieselbe Methode, dieselbe Richtung, anderes Ende:** die
oberste nicht-transparente Zeile je Cutout, als Anteil der Bildhöhe. Ergebnis als
`--head`-Variable je Akteur führen, analog zur Fußlinie.

Grund für den Scan statt eines Schätzwerts: Beim Scout wich der Cutout-Master (RGB auf
Magenta-Key, kein Alpha) um ~3 % vom ausgelieferten AVIF ab. Der Master ist keine gültige
Quelle für Geometrie.

## A3 · Die Platzierungsregel — und warum keine `--side`-Formel

**Anker:** Die **Unterkante** der Plakette liegt auf der Kopflinie; die Plakette **überlappt
die obere Figurregion**, statt vollständig über dem Kasten zu schweben (Begründung A4).
`bottom: auto`, Anker über `top` relativ zu `--head`, Vertikalversatz ~40–60 % der eigenen
Höhe nach oben.

**Horizontal: zwei am Plate eingemessene Werte, keine Formel.** Eine symmetrische Regel
„nach innen versetzt" über `--side` sieht elegant aus und ist hier falsch — die ruhigen
Flächen liegen nicht symmetrisch:

| Akteur | nach innen | über dem Kopf | ⇒ Plakette |
|---|---|---|---|
| Scout (links verankert) | Lampenschein + Bildschirm, **unruhig/hell** | dunkle Wandvertäfelung, **ruhig** | über dem Kopf, leicht nach **außen** |
| Warden (rechts verankert) | dunkle Wand über dem Schreibtisch, **ruhig** | helles Fenster, **unruhig** | schräg über dem Kopf nach **innen (links)** |

Also: **ein Mechanismus, zwei getunte Werte** je Akteur. Bitte keine Symmetrie erzwingen.

**Gesichter bleiben frei.** Der Steward wünschte „vor dem Gesicht"; ich rate davon ab und
habe seine Zustimmung, es zunächst so zu bauen: Die Blickrichtungen sind die Erzählung — der
Scout schaut nach rechts auf ihren Schirm, der Warden nach links. Höchstens Haar und Schulter
überlappen, Augen frei. Sollte es ihm zu zurückhaltend sein, ist es ein Wert, kein Umbau.

## A4 · Der Klemmfall, der die Regel bestimmt (bitte nachrechnen)

Nicht die Plakette vollständig über den Kasten setzen. Rechnung für **1440 × 700**
(Ultrawide-Zweig, weil 2,06 > 16/9):

```
rail height = min(29.25vw, 56svh) = min(421, 392) = 392 px = 56 svh
rail bottom = max(2svh, 100svh − 46.13vw) = max(14, 700 − 664) = 36 px = 5,14 svh
Kastenoberkante = 100 − 5,14 − 56 = 38,86 svh = 272 px
Tafel-Oberkante (Masthead-Band, ≥1200 px) = 15,5 rem = 248 px
⇒ Luft zwischen Kasten und Kopfstreifen: 24 px
```

Eine dreizeilige Plakette über dem Kasten würde dort mit Kopf und Tafel kollidieren. Liegt
sie dagegen **auf der Kopflinie und überlappt die Figur**, bleibt sie immer im Band der Figur
selbst und kann per Konstruktion nicht mit dem Masthead kollidieren. Kein `clamp()` nötig,
keine Zusatzlogik — die richtige Verankerung erledigt es.

## A5 · Optional: die Kadenz in die Plakette

Der Steward möchte den nächsten Scout-Lauf dort haben. Thematisch richtig — der Akteur trägt
seine eigene Kadenz (§4.2 in `docs/opus5-zeitschicht-konzept.md`). **Aber:** Die Plakette
erscheint nur bei Hover; auf Touch existiert sie nicht. **Hover-Information ist Zugabe, nie
der Träger einer Tatsache.**

Also beides, ohne Widerspruch:
- **Plakette (Detailkarte, Hover):** vierte Zeile mit der Kadenz des Akteurs, z. B.
  „prüft jeden Montagmorgen · letzte Prüfung 8. Juli 2026". Datum aus
  `listJournalEntries()[0].date`, Termin aus dem Rhythmus berechnet (§3 des Konzepts) —
  **nicht** aus `schedule.json`.
- **Persistente Zeile unter der Röhre:** bleibt als Minimum, immer sichtbar, auch auf Touch.

Die kleine Redundanz ist korrekt: die Plakette ist die Detailansicht.

**Sequenz-Hinweis:** A5 hängt an der Zeitschicht. Wenn du die Plakette jetzt umhängst, baue
A1–A4 zuerst und lasse A5 für den Zeitschicht-Durchgang liegen — die Zeile lässt sich später
ohne Layoutänderung ergänzen.

## A6 · Zwei Nebenpunkte

- **Touch hat keine Plakette.** Das ist heute schon so, unabhängig von diesem Umbau. Der
  `alt`-Text trägt Name, Gloss und Rolle, assistive Technik ist also versorgt — ein sehender
  Touch-Nutzer bekommt nichts. Separat zu entscheiden, nicht in diesem Paket lösen.
  **Kein Tab-Stopp auf dem nicht-interaktiven Element** (StageTube-Regel gilt weiter).
- **Bodenreflexion prüfen.** Auf einem Screenshot des Stewards wirkt die Reflexion unter
  Tisch und Stuhl bei niedriger Auflösung eher wie ein harter Schattenfleck als wie eine
  Spiegelung, die Stuhlbeine wirken leicht freigestellt. Kein Befund, ein Eindruck — bitte
  bei der Gelegenheit mit ansehen (`.reflection`, `opacity: 0.16`, `scaleY(-1)`).

## A7 · Abnahme

1. **1440 × 700** und **1280 × 720**: Plakette vollständig sichtbar, keine Kollision mit
   Masthead, Tafel oder Röhre. Das ist der Fall, der heute bricht.
2. Beide Akteure, Hover und `:focus-visible`-Äquivalent falls vorhanden: Augen frei, Plakette
   auf ruhiger Fläche.
3. Reduced-Motion und No-JS: unverändert (die Plakette ist reine Hover-Zugabe, ohne Hover
   nicht sichtbar — das ist der Bestandszustand, kein §0-Thema).
4. Reflow 320/390: unverändert, kein Overflow.
5. Build warnungsfrei (außer StageTube-Altposten, falls noch offen), Testsuite grün, Preview
   neu gestartet.

---

# Teil B · Wart-Mechanismus: AUDIT, kein Fix

## B0 · Warum ein Audit und kein Fix

Der Steward hat das Secret-Thema **schon zweimal angegangen**, das zweite Mal mit langem
Debugging, Korrekturläufen und Tests. Ich habe ihm auf Basis von
`noblecause-SESSION-KONTEXT-2026-07-10.md` trotzdem empfohlen, Secret zu setzen und einen
Preflight zu bauen — **das war falsch, und er hat mich gestoppt.** Beim Nachsehen im Code:

- Der Kontext behauptet, `run_wart.py` habe eine `load_env()`-Funktion. **Hat es nicht.** Sie
  liegt längst in `gremium/envtools.py`, zusammen mit `require_keys()`; `run_wart.py:252–253`
  ruft beides auf.
- `envtools.py` ist **besser gehärtet** als mein Vorschlag: `.env` ist in CI abgeschaltet
  (`CI == "true"`), mit dem Docstring-Vermerk „a stale/absent .env must never paper over a
  missing secret (that hid the 401 once)". `require_keys()` fängt fehlend, leer **und**
  umschließenden Whitespace, bricht vor jedem API-Call ab, loggt nur Längen.
- Es gibt zusätzlich `preflight.py`, `reaggregate.py`, ein `.fable-check`-Verzeichnis vom
  8. Juli. Der Projekt-Kontext ist Tage hinter dem Code.

**Ein YAML-Preflight in `wart.yml` wäre die dritte, schwächere Fassung derselben Sache. Nicht
bauen.** Erst herausfinden, was tatsächlich noch fehlt.

## B1 · Die Leithypothese

**Cron-Workflows laufen ausschließlich vom Default-Branch.** Die gehärteten Dateien liegen im
Arbeitsbaum von `feat/council-rooms`; `gremium/**` ist dort ein **Tabu-Pfad mit Guard-Hook**,
kann also von diesem Branch nie committet worden sein. Ob `envtools.py` und `require_keys`
überhaupt auf `master` angekommen sind, ist offen. Wenn nicht, läuft der Montags-Cron seit
Wochen die alte, ungehärtete Fassung — **und das würde erklären, warum zwei Reparaturrunden
nichts geändert haben.**

## B2 · Prüfliste (nur lesen und berichten)

1. **Was liegt auf `master`?** `master:.github/workflows/wart.yml`,
   `master:gremium/envtools.py`, `master:gremium/run_wart.py`, `master:gremium/config.json`
   gegen den Arbeitsbaum vergleichen. Frage: Ist die Härtung live oder nur lokal?
2. **Lauf-Historie:** `gh run list --workflow=wart.yml` seit 2026-07-08 — Anzahl, Status,
   Conclusion, Trigger (schedule vs. workflow_dispatch).
3. **Die Selbstmeldung des Workflows:** `wart.yml` legt bei Fehlschlag automatisch ein Issue
   mit Label `ci-failure:wart` an und hängt die letzten 3000 Zeichen Log an.
   `gh issue list --label ci-failure:wart --state all` → **das ist der schnellste Weg zur
   echten Fehlermeldung.** Dort steht, ob es überhaupt noch 401 ist.
4. **Secret-Namen** (nicht Werte): `gh secret list`. Existieren `ANTHROPIC_API_KEY`,
   `OPENAI_API_KEY`, `GEMINI_API_KEY`? Unter **Repository secrets**, nicht nur Environment?
   → **Wichtig:** `run_session.py:644` fordert `require_keys("ANTHROPIC_API_KEY",
   "OPENAI_API_KEY", "GEMINI_API_KEY")` — **alle drei.** Fehlt einer, scheitert die Sitzung
   am 8. August genauso, nur mit anderer Meldung. Das ist der Folge-Check, der im alten
   Kontext als „wichtigster" markiert war.
5. **Kam je ein Eintrag aus Actions?** Das Journal-Schema hat ein Feld `actions_run_url`.
   Über alle `journal/*/entry.json` prüfen, welche gesetzt sind. Antwortet, ob ein
   Actions-Lauf **jemals** erfolgreich war.
6. **Die Deputation aufklären:** `journal/2026-07-08c/entry.json` hat `model: kimi-k2` und
   eine `deputation_note`, obwohl `config.json` den Wart auf `claude-fable-5` setzt. War das
   eine Umgehung des 401? Wenn ja, ist das ein Indiz, dass der Anthropic-Key in CI **nie**
   funktioniert hat.
7. **Nachrangig:** Modell-IDs in `config.json` gegen die für den Key verfügbaren Modelle. Ein
   unbekanntes Modell liefert 404/403, nicht 401 — also nur relevant, falls die Meldung aus
   Punkt 3 nicht mehr 401 ist.

## B3 · Was du NICHT tust

- **Kein** `workflow_dispatch` auslösen. Der Steward startet den ausgelassenen Lauf selbst,
  nach Abschluss der UI-Arbeit.
- **Kein** Secret anfassen, nicht anlegen, nicht rotieren, keine Werte ausgeben oder
  loggen — auch keine Teilwerte.
- **Kein** Commit unter `gremium/**` oder `.github/**` ohne ausdrückliche Freigabe. Guard-Hook
  nicht umgehen.
- **Kein** Fix vorschlagen, bevor Punkt 3 beantwortet ist. Die echte Fehlermeldung schlägt
  jede Hypothese, meine eingeschlossen.

## B4 · Ergebnis

Ein Befundbericht: Was liegt auf `master`, was sagt das Issue, welche Secrets existieren
namentlich, kam je ein Eintrag aus Actions, was war die Deputation. Daraus leiten wir
gemeinsam ab, was fehlt — **einmal, nicht ein drittes Mal.**

Danach ist `noblecause-SESSION-KONTEXT-2026-07-10.md` im Projekt zu korrigieren, sonst
schickt es die nächste Instanz denselben Weg noch einmal. Das mache ich, sobald dein Bericht
da ist.
