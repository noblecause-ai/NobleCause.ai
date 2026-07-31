# Übergabe — Architekt-Session NobleCause.ai

**Von:** Opus 5 (Architekt, Session vom 27./28. Juli 2026)
**An:** die nachfolgende Architekt-Session
**Zweck:** vollständiger Kontext ohne Lektüre des Chatverlaufs.

---

## 1 · Rollen

| Rolle | Wer | Tut |
|---|---|---|
| **Steward** | Afschin | entscheidet, prüft im echten Browser, erteilt Freigaben, generiert Bilder extern |
| **Architekt** | diese Session | Konzepte, Direktiven an CC (`.md` unter `docs/`), Bild-Bestellungen als Copy/Paste-Prompts, Entscheide auf CC-Rückfragen |
| **CC** | Claude Code im Repo | baut, misst, berichtet, committet **nur auf ausdrückliche Freigabe** |
| **Wart** | eigene Session (`claude-fable-5`) | Rekord-Hoheit: Kanon, Datennaht, Einberufungen, Rahmen für Personenwahlen |
| **Leitstand** | eigene Session | Gesamtrelease über alle Projekte des Stewards |

**Der Architekt schreibt keinen Code.** Kontext ist zu wertvoll für Code-Details; Ausführung
läuft über Direktiven. Der Chat ist Rekord genug — **nicht jede Antwort als Datei ausgeben.**
Dateien nur für Direktiven, Bestellungen und Konzepte.

---

## 2 · Was das Projekt ist

NobleCause.ai: Drei KI-Modelle verschiedener Familien (Claude Opus, GPT, Gemini Pro) prüfen
dieselben Belege und empfehlen öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.
Jede Sitzung wird vollständig und unverändert veröffentlicht. Vier Bereiche („Säulen"): Zukunft,
Leid lindern, Große Gefahren, Was sonst übersehen wird. Aggregationsregel: **zwei gleiche
Nennungen ergeben eine Empfehlung.**

Die Site ist ein SvelteKit-Static-Build (`adapter-static`), inszeniert als **drei nächtliche
Räume**: The Study (Frage und Belege) → The Council / Ratssaal (Beratung) → The Archive (das
Protokoll). Dahinter der **Protokoll-Explorer** (Sitzungen, Journal, Kommissionen).

---

## 3 · Die Verfassung — nicht verhandelbar

**§0:** Voller Inhalt ohne JS und bei `prefers-reduced-motion`. Die Bühne **verzögert und bewegt,
sie erzeugt und versteckt nie.** Kein `buildTime`, kein Überfällig-Zustand.

**Versiegelte Datennaht:** Das Frontend paraphrasiert nie. Sitzungs- und Journaltext wörtlich.
Der Renderer parst keine Prosa, nur strukturelle Signale (Zählstand, `conditional`, geändertes
Votum, Dissens, Kosten, `search_queries`). **Prozessaussagen sind erlaubt** („zwei gleiche
Nennungen ergeben eine Empfehlung", „vier Bereiche") — Ergebnisaussagen nie.

**Kantenprinzip:** Bewegte Bühnenelemente `position: fixed`, von der Kante herein, Rückzug nur
über `--retreat`. Die Kulisse steht, bewegt wird die zweite Ebene. (Ausnahme seit Runde H: die
Zählmaschine ist als P10-Ebene zweite Ebene und darf sich bewegen.)

**Gestaltung:** Vignette statt Kasten. Gleiten und Licht statt Effekten. Schichtung statt
Auswahl. Kein Weiß. Serifen für den Rekord, Versalien für die Ordnung.

**Guardrails:** Guard-Hook blockt `sessions/**`, `journal/**`, `schedule.json`, `gremium/**`,
`schema/**`, `prompts.py` auf `feat/*`. Daten nur über eigenen Datenbranch + `--ff-only`.
**Nie `--no-verify`. Kein Push** — der gesamte Stand ist lokal.

**Verifikations-Vorstufe (seit dieser Session Pflicht vor jeder visuellen Aussage):** frischer
Build (`rm -rf site/build site/.svelte-kit && npm run build`), Konsole ohne Chunk-Ladefehler,
Klick-Handler feuert nachweislich. Erst dann messen. Geometrie **immer am gerenderten AVIF**,
nie am Master.

---

## 4 · Stand des Baus

**Branch `feat/council-rooms`**, kein Push. Wichtige Commits dieser Session in Reihenfolge:

`c03a120` Archiv-Möbel · `a9ec155` Archiv §1–§3 · `00b0d1c` Council-Sitzzeilen · `3fd11e2`
Rooms-Aufräumen · `72c78d5` schedule.json untracken · `af8eca7` **Türdurchgang** · `d1b20ed`
Council-Türmitte · `22f2575` Medien-Strang · `61ca071` try/catch-Härtung · `04ac905` Medaillons ·
`82aa498` Rückwärts-Stabilität + Orbit-Math · `2d3524e` Pulte weg (Desktop) + Medaillon-Hover ·
`bdad6d4` docs-Reorg · `7bf4ab8` `docs/go-live.md` · `3fd979d` Zählstrang v1 · `010a83c`/`c44253f`
Explorer-Sprungleiste · `d336df8`/`ec5c9b2`/`71d6a28` Trichter 2b · `b32df19` Lesetisch-Übergang.

**Branch `master` = `5071194`** — inhaltsdefinierter Rekord-Commit (Sitzungen, Journal, Schemas,
Kommission), per `--ff-only` von `c7b7ba6`. `data/commission-selbstdarstellung` = `master`.

**Gebaut und vom Steward im Browser bestätigt:**
- **Echter Türdurchgang** in allen drei Türen (Study ↔ Council ↔ Archiv). CSS-3D-Kamerafahrt,
  kein WebGL: drei Ebenen im Tiefenraum (Wand-mit-Loch z=0, Türflügel z≈−200, Zielraum-Plate
  z≈−1400), animiert wird **nur** `translateZ` des Kamerawagens. `perspective` ≈ 0,6 × Fahrtstrecke
  (850 bei 1400) — **das ist der kritische Wert:** ist er größer, passiert die Wand die Kamera nie
  und die Fahrt liest als Blende. `perspective-origin` zur Laufzeit aus der Cover-Rechnung.
- **Ruhe-Stapel:** Der Ruhezustand jedes Raums ist derselbe Ebenenstapel bei Kamera 0 — dadurch
  ist Frame 1 der Fahrt konstruktiv gleich dem Ruhebild, auf jedem Seitenverhältnis. Beim Hover
  spreizen die Flügel, dahinter steht der Zielraum bereits.
- **Medaillon-Orbit** um die Zählmaschine im Ratssaal, mit echter Verdeckung (Doppel-Render:
  „hinten"-Kopie vor P10 im DOM, „vorn"-Kopie danach; Wechsel an den Ellipsenscheiteln).
- **Zählstrang 2b** als senkrechter Trichter im Ratssaal.
- **Protokoll-Explorer:** Übersicht, Sitzungsseite, Journal, Kommissionen, Sprungleiste mit
  Säulen-Emblemen, `:target`-Hervorhebung ohne Ausblenden.

**Gebaut, visuell noch nicht vom Steward abgenommen:** §8 Zähl-Ruck der Trommel, der
Lesetisch-Übergang (siehe §6 — Fehlentwicklung).

---

## 5 · Entschiedenes, das nicht neu verhandelt wird

- **Selbstdarstellung der Modelle:** Jedes Modell **bestellt** seine Darstellung in Worten; ein
  einziger Generator erzeugt alle drei im Hausstil. Grund: ließe man jedes Modell selbst
  generieren, könnte Claude nicht teilnehmen (keine Bildgenerierung) — die Gleichbehandlung, die
  Prämisse der Seite, wäre an der sichtbarsten Stelle gebrochen.
- **Bestelltexte sind Rekord**, wörtlich und öffentlich (`models.json`,
  `commissions/2026-07-27/`). Gelaufen als **Kommission `commission-1`** über den regulären
  API-Mechanismus, eigener Behälter, **nicht als Sitzung gezählt**.
- **Ergebnis:** Opus = antike Öllampe · GPT = Waage/Zirkel · Gemini = **Florence Nightingale**
  (†1910). Gesichter sind erlaubt, aber als **Messingrelief**, nur lange Verstorbene, und **der
  Modellname steht immer beim Medaillon** — der Schutz gegen „Nightingale empfiehlt" statt
  „Gemini empfiehlt". Das ist Bauvorgabe, keine Gestaltungsfrage.
- **Wart-Rahmen für Personenwahlen:** ≥ 70 Jahre verstorben; nicht wesentlich durch
  Gewaltherrschaft, Verfolgung oder Menschenfeindlichkeit **geprägt**; keine zentralen religiösen
  Figuren; Grenzfälle beim Wart. Klare Fälle sind angenommen, ohne Wart-Vorlage.
- **Keine unnötigen Schranken.** Der Steward hat Zeichengrenzen und ein Zitatverbot ausdrücklich
  gestrichen: „wir wollen sehen, messen und nachbessern". Halluzinierte Zitate wären ein
  sichtbarer, protokollierter Befund über das Modell — kein Anlass für eine Klausel.
- **Explorer ist kein vierter Raum** und **bewegungslos**. Kein Maschinenbild dort.
- **Der Lesetisch hat keinen Rückweg** — die Tür verbindet zwei Orte, der Lesetisch einen Ort mit
  einem Text.
- **Keine erneute Design-Konsultation.** Die Bildsprache steht; offene Fragen sind
  informationsarchitektonisch, nicht gestalterisch.

---

## 6 · Drei Fehlentwicklungen — und die Lehre. **Wichtigster Abschnitt.**

Drei Mal hat CC nach meiner Direktive etwas Plausibles gebaut, das nicht das Gemeinte war. In
allen drei Fällen lag es an der Direktive, nicht an CC.

1. **2b im Explorer statt im Ratssaal.** Ich hatte „Zählstrang als Bühne" in mein
   Explorer-Konzept einsortiert, weil beides vom Zählen handelt. 2b ist aber der Abschnitt
   „Wie gezählt wurde" **im Council-Raum**.
2. **Kein zweites Maschinenbild.** Ich untersagte das Cutout im Fluss („die Maschine steht ja
   schon in der Szene") — falsch: die Szenen-Maschine liegt in anderem Maßstab, hinter den
   Karten, desktop-only. Ein Abschnitt im Fluss braucht seine eigene Abbildung.
3. **Der Trichter als waagerechte Reihe.** Ich schrieb „Cutout im Fluss, Voten daneben". 2b ist
   ein **senkrechter Trichter**: drei Pulte oben, Linien laufen nach unten zusammen, Maschine
   unten mittig.
4. **Der Lesetisch ohne Eingang.** Ich beschrieb die Bewegung („der Tisch fährt heran, das Licht
   weitet sich") und nannte nie das **anklickbare Element**. CC hängte den Übergang an die
   vorhandenen Textlinks; sichtbar ist jetzt ein kurz aufblitzender riesiger Schreibtisch am
   Anfang der Protokollseite. Ein einfacher Link auf dem Pult hätte genügt.

**Die Lehre, an die sich die Nachfolge halten sollte:**

- **Nenne immer drei Dinge: das Element, den Ort im DOM, die Anordnung.** Bewegung und Absicht
  allein reichen nicht — CC baut daraus etwas Plausibles, und Plausibel ist oft falsch.
- **Wo ist es anklickbar?** Bei jeder Interaktion ausdrücklich beantworten.
- **Wo steht es im Baum?** „Im Fluss" oder „in der fixen Szene" entscheidet über Maßstab,
  Koordinatensystem und Sichtbarkeit.
- **Wie ist es angeordnet?** Senkrecht oder waagerecht, was oben, was unten.
- **Wenn eine Skizze existiert, ist sie die Vorlage** — sie in Prosa zu übersetzen verliert genau
  das, was sie festhält.

---

## 7 · Offene Punkte

**Sofort:**

1. **Lesetisch-Übergang zurückbauen** (`b32df19`). Der aktuelle Zustand — ein sekundenlang
   riesiger Schreibtisch am Anfang der Protokollseite — ist zu verwerfen. Der Steward hat gesagt,
   ein einfacher Link hätte genügt. Empfehlung: den Übergang entfernen und das **sichtbare Pult
   im Archiv** (`ArchiveActors.svelte`, `.pult-desk`, `pult-lamp`-Asset) zu einem schlichten,
   fokussierbaren Link auf das aktuelle Protokoll machen. Bewegung erst wieder, wenn der Eingang
   sitzt und der Steward sie will.
2. **Abschluss-Durchgang alle drei Räume:** jede Türfahrt, jeweils Zurück und erneute Fahrt ohne
   Neuladen, mobil 390, reduced-motion, ohne JS. Vorstufe jedes Mal.
3. **§8 Zähl-Ruck** vom Steward visuell abnehmen lassen. Abnahme: die **Kanten** der Trommel
   bewegen sich nicht, nur ihre Oberfläche.

**Vor Go-Live:**

4. **Auslieferungsparameter** (`docs/noblecause-auslieferungsparameter-fuer-leitstand.md`) beim
   Leitstand umsetzen: Cache in drei Klassen (immutable-Chunks / HTML no-cache / **ungehashte
   Medien mit Revalidierung**), **24 h Karenz für die Chunks der Vorgängerversion**, avif-MIME,
   Routing ohne SPA-Fallback. Der Karenz-Punkt ist kritisch: ohne ihn trifft bei jedem Release
   der Ausfall „altes HTML, Chunks weg → keine Hydration → alles tot" echte Besucher.
5. **Medien-Strang** der seit `22f2575` neu entstandenen Assets committen (P10/P11,
   `council-machine`, Trichter-Assets).
6. **`master` und `feat/council-rooms` zusammenführen** und pushen — bisher ist **nichts
   gepusht**.

**Danach:**

7. 57 Zeitstempel-Bilder in `docs/` einsortieren (bewusst nach Go-Live verschoben).
8. Rückweg-Bestellungen P7/P8 sind **nicht** nötig — der Freischnitt aus den vorhandenen Plates
   hat in Study und Council getragen.

---

## 8 · Empfohlener Go-Live-Schnitt

Der Gesamtrelease des Stewards (aion-lumen 0.4.0) wartet seit zwei Wochen auf NobleCause.
**Ausliefern lässt sich nach Punkt 1–2 und 4–6.** Alles Weitere ist Ausbau und kann in einer
Punktversion nachkommen, ohne dass jemand eine unfertige Seite sieht.

---

## 9 · Dokumente, die zählen

Unter `docs/`, in der Reihenfolge ihrer Nützlichkeit:

- `opus5-konzept-2026-07-27-durchgang-und-sitze.md` — Türdurchgang und Orbit, die Tiefenlogik
- `opus5-nachtrag-2026-07-27-durchgang-liest-als-blende.md` — warum `perspective` ≈ 0,6 × Strecke
- `opus5-konzept-2026-07-28-protokoll-explorer.md` — Explorer, „jede Ansicht hat eine Adresse"
- `opus5-2026-07-27-bestellverfahren-selbstdarstellung.md` — Rahmentext, Registratur, Ablauf
- `opus5-nachtrag-2026-07-27-gesichter-erlaubt.md` — Relief, Personenrahmen, Modellname am Zeichen
- `noblecause-auslieferungsparameter-fuer-leitstand.md` — Deploy und Cache
- `go-live.md` — CCs laufende Liste
- `bestellung-serie-5-archiv-2026-07-27.md`, `bestellung-medaillons-2026-07-27.md`,
  `bestellung-zaehlmaschine-2026-07-27.md` — Bestellmuster, falls neue Assets nötig werden
- `docs/archiv/` — überholt, aber erklärend; nicht löschen

**Der Entwurf 2b** liegt beim Steward als Bild, nicht im Repo. Wer 2b anfasst, lässt ihn sich
zeigen.
