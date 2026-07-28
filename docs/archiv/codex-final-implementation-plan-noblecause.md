> **Archiviert 2026-07-28 (CC) — Codex-Bauphase, durch den council-rooms-Bau abgelöst.** Verschoben nach docs/archiv/, nicht gelöscht (erklärt die Historie, warum Dinge so sind).

# Finaler Implementierungsauftrag an Codex  
## NobleCause.ai · „Der Ratssaal als lebende Maschine“

**Stand:** 2026-07-15  
**Arbeitszweig:** `feat/immersive-homepage`  
**Produktiver Zielpfad:** `site/`  
**Ausgabe:** `site/build/`

---

## 0. Auftrag

Setze jetzt die neue Startseite von NobleCause.ai im bestehenden Repository um.

Dies ist **kein weiterer Analyseauftrag** und **kein visueller Prototyp**. Baue die produktive SvelteKit-Seite direkt unter `site/`, so dass sie mit dem bestehenden Deployment tatsächlich ausgeliefert wird.

Lies vor Beginn vollständig:

1. `docs/handoff-notes-for-codex.md`
2. `docs/codex-analysis.md`
3. `AGENTS.md`
4. `.github/workflows/deploy.yml`
5. `schema/session.schema.json`
6. `schema/organizations.schema.json`

Prüfe die Aussagen der Dokumente am Code. Die Analyse ist die Grundlage, aber der Repositoryzustand bleibt die letzte technische Wahrheit.

---

# 1. Zielbild

Die Startseite ist keine normale lange Dokumentseite und kein Stapel dunkler Karten.

Sie ist eine **zusammenhängende, räumliche Bühne**:

- ein gewaltiger Ratssaal,
- drei gleichwertige Pulte,
- eine mechanische Zählmaschine in der leeren Mitte,
- ein Vorzimmer mit Späher und Wart,
- eine monumentale Tür zum Archiv.

Beim Scrollen verändert sich der Zustand derselben Bühne. Der Besucher bewegt sich gedanklich durch das Verfahren, statt bloß weitere Blöcke untereinander zu lesen.

Die visuelle Richtung heißt:

> **Der Ratssaal als lebende Maschine**

Die Seite muss atmosphärisch, ernst und eigenständig wirken:

- gemalte Konzeptkunst,
- warmes Bernstein- und Messinglicht gegen kaltes Mondblau,
- dunkles Holz,
- Stein,
- Messing,
- matte Oberflächen,
- ruhige Mechanik,
- keine Hochglanzästhetik,
- kein Standard-SaaS-Dashboard,
- keine austauschbaren schwarzen Overlaykarten,
- keine Chatblasen,
- keine sprechenden Modellfiguren,
- kein bebildertes Leid.

Die HTML-Oberflächen dürfen über der Bildwelt liegen, müssen aber wie **Bestandteile des Raumes** wirken: Protokollblätter, gravierte Register, Messingbänder, Steininschriften, Tafelflächen und Archivregister.

---

# 2. Inhaltliche Wahrheit

NobleCause ist ein öffentliches Beratungsprotokoll.

Je ein KI-Modell von Anthropic, OpenAI und Google prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.

Die Beratung umfasst vier Bereiche:

1. Investition in die Zukunft
2. Linderung von Leid
3. Schutz vor großen Gefahren
4. Übersehenes

Die Modelle antworten zuerst getrennt. Danach lesen sie die Antworten der anderen und dürfen ihre Meinung ändern.

Ein deterministisches Programm zählt ausschließlich die Nennungen:

- Nennen mindestens zwei Modelle dieselbe Organisation, wird sie empfohlen.
- Sonst bleiben alle genannten Organisationen gleichwertig nebeneinander.

Das Programm urteilt nicht.

Jede Sitzung wird vollständig veröffentlicht:

- Frage,
- Belege,
- erste Antworten,
- spätere Antworten,
- Meinungsänderungen,
- Uneinigkeit,
- Ergebnis,
- Kosten.

Über NobleCause fließt kein Geld. Spendenlinks führen direkt zu den Organisationen.

Uneinigkeit ist ein normales Ergebnis und kein Fehler.

Meinungsänderungen dürfen niemals unsichtbar überschrieben werden.

---

# 3. Der erste Blick: Was, warum und Ergebnis

Der erste sichtbare Zustand muss zunächst erklären, **was NobleCause ist und warum es existiert**.

## Leitfrage

> **Wo hilft meine Spende am meisten?**

## Kernaussage

> Je ein KI-Modell von Anthropic, OpenAI und Google prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am meisten bewirkt.

## Ergänzung

> Für Menschen, die heute Hilfe brauchen. Für unsere gemeinsame Zukunft. Für große Gefahren und für Probleme, die leicht übersehen werden.

## Transparenzsatz

> NobleCause nimmt kein Geld an. Es veröffentlicht die Empfehlungen und führt direkt zu den Organisationen.

## Persönlicher Ursprung

Die kurze Ursprungsgeschichte soll sichtbar sein, aber nicht die Hauptrolle übernehmen:

> NobleCause entstand aus einer einfachen Frage: Nachdem ich eine regelmäßige Spende wegen eines Skandals beendet hatte, wusste ich nicht, wohin sie stattdessen gehen sollte. Für eine gründliche Prüfung fehlte mir die Zeit. Daraus entstand ein öffentliches Verfahren, das diese Recherche regelmäßig übernimmt und vollständig offenlegt.

Du darfst diesen Absatz sprachlich leicht straffen, aber weder dramatisieren noch eine Gründerinszenierung daraus machen.

## Mechanismus, direkt verständlich

Der folgende Satz muss früh und prägnant erscheinen:

> **Drei Modelle antworten getrennt. Sie lesen danach die Antworten der anderen und dürfen umdenken. Ein einfaches Programm zählt nur die Nennungen.**

Direkt danach:

> **Nennen mindestens zwei Modelle dieselbe Organisation, wird sie empfohlen. Sonst bleiben alle Vorschläge gleichwertig nebeneinander.**

Diese Erklärung darf nicht in einer tiefen Unterseite versteckt sein.

## Aktuelle Empfehlungen

Die vier aktuellen Säulen und ihre direkten Spendenlinks müssen im ersten Nutzungsgang leicht erreichbar sein. Keine einzelne Säule darf als globaler Gesamtsieger inszeniert werden.

Die visuelle Hierarchie darf atmosphärisch sein, muss aber alle vier Bereiche fachlich gleichwertig behandeln.

---

# 4. Dramaturgie der Desktop-Bühne

Baue fünf große Akte mit diskreten Unterzuständen.

Die Bühne bleibt auf Desktop über eine längere Strecke sticky. Semantische Cue-Abschnitte steuern lediglich den räumlichen Zustand. Kein Scrolljacking.

## Akt 1 · Eintritt

### Szene `arrival`

- weiter Blick in den Ratssaal,
- Leitfrage,
- Kernaussage,
- Ergänzung,
- Transparenzsatz,
- kurze Ursprungsgeschichte,
- die Bühne bleibt dunkel und ruhig,
- die leere Mitte ist sichtbar,
- die drei Pulte sind gleichwertig angeordnet.

Der Text soll auf einer architektonisch plausiblen Fläche erscheinen, nicht in einer beliebigen Webkarte.

Geeignete Metaphern:

- gravierte Messingtafel,
- dunkles Protokollblatt,
- Steininschrift,
- eingelassene Ratstafel.

## Akt 2 · Heutige Empfehlung

### Szene `recommendations`

Die Kamera beziehungsweise Komposition senkt sich zur Mitte.

Die vier Bereiche erscheinen als **Ergebnisregister** am Rand der Maschine oder des Mittelbodens.

Jeder Bereich zeigt datengetrieben:

- Säulenname,
- Organisation oder mehrere Organisationen,
- Registrybeschreibung,
- Stimmenzahl,
- Vorbehalt, falls vorhanden,
- direkten Spendenlink,
- Link zum vollständigen Schlussvotum beziehungsweise Protokoll.

Keine redaktionell erfundene Kurzbegründung.

### Konsenszustand

Beispielhafte sprachliche Form:

> 3 von 3 nennen dieselbe Organisation.

oder:

> 2 von 3 nennen dieselbe Organisation.

### Konsens mit Vorbehalt

Der Vorbehalt muss direkt sichtbar sein:

> 3 von 3, davon 1 unter Vorbehalt.

Die tatsächliche Reservation kommt aus den Daten.

### Keine Einigkeit

Alle Organisationen erscheinen gleichwertig:

- identische Fläche,
- identischer Kontrast,
- identische Linkbehandlung,
- Modellattribution,
- keine visuelle Siegerwahl,
- kein Warnrot,
- kein Fehlericon.

Text:

> Keine zwei Modelle nennen dieselbe Organisation.

## Akt 3 · Frage und Vorzimmer

### Szene `question`

- Fokus auf Mittelboden oder Tafel,
- aktuelle Sitzungsfrage aus den Daten,
- kurze Zählregel,
- Link zum vollständigen Sitzungsprotokoll.

### Szene `evidence`

Der Raum wechselt durch die monumentale Tür in das Vorzimmer.

Das Vorzimmer zeigt:

- Späher als Ort der Belegsammlung,
- Wart als Ort der Dokumentation,
- Schiefertafel als HTML-Fläche,
- Frage,
- vorhandene Dossier-/Quellenzugänge,
- keine erfundene Quellenzahl,
- keine erfundene Belegqualität.

Verwende keine Figurenrede und keine Sprechblasen.

Passende kurze Labels:

> Der Späher sammelt Belege.

> Der Wart ordnet das öffentliche Protokoll.

Diese Labels sind Funktionsbeschreibungen, keine Personifizierung der Modelle.

## Akt 4 · Getrennte Stimmen, Gegenlesen und Umdenken

### Szene `initial`

Zurück im Ratssaal.

Die drei Pulte erscheinen gleichzeitig und gleichrangig:

- Anthropic,
- OpenAI,
- Google.

Jedes Pult zeigt strukturierte Erstvoten aus `rounds[kind="initial_vote"]`.

Keine Chatdarstellung.

Die Voten wirken wie gleichzeitig abgelegte schriftliche Protokolle.

### Szene `review`

Die Schlussvoten erscheinen.

Für jede Kombination aus Modell und Säule:

- vergleiche Erst- und Schlussvotum über `organization_id`,
- bei Änderung bleibt das alte Votum sichtbar,
- altes Votum in `<del>`,
- neue Organisation klar darunter oder daneben,
- zusätzlich Textlabel wie „Erstvotum“ und „geändert zu“.

Beispiel:

```text
Erstvotum
TaRL Africa

geändert zu
Helen Keller International
```

Das alte Votum muss typografisch durchgestrichen bleiben.

Erfinde keinen kurzen Änderungsgrund. Falls die Begründung nur im vollständigen Schlussvotum liegt, verlinke dorthin oder zeige den vollständigen Text in einem zugänglichen `<details>`.

## Akt 5 · Zählen, Veröffentlichung und Archiv

### Szene `count`

Die mechanische Mitte wird fokussiert.

Die Maschine zeigt ausschließlich die vorhandenen Nennungen.

Visuelle Regeln:

- drei Marken beziehungsweise Wege, eine je Modell,
- gleiche Nennungen landen im selben Ergebnisfach,
- verschiedene Nennungen bleiben getrennt,
- keine Darstellung von „Intelligenz“,
- kein Gesicht,
- kein Modell bedient die Maschine,
- die Maschine darf leicht mechanisch animiert sein,
- keine Information darf nur durch Bewegung vermittelt werden.

Die Regel erscheint noch einmal in Klartext:

> Das Programm zählt nur, wie oft dieselbe Organisation genannt wurde.

### Szene `publish`

- Ergebnisprotokoll,
- Kosten aus den Daten,
- Korrekturhinweis, falls vorhanden,
- Zugang zum vollständigen Dissens,
- Link zur vollständigen Sitzung,
- Tür zum Archiv,
- frühere Sitzungen als Register.

Bei früheren Sitzungen muss ein säulenweiser Nicht-Konsens korrekt erkennbar sein. Eine Sitzung darf nicht pauschal als vollständig uneinig bezeichnet werden, wenn nur eine Säule keinen Konsens hat.

---

# 5. Interaktionsmodell

## Desktop

Verwende:

- semantische Inhaltsreihenfolge im DOM,
- sticky Bühnenfläche,
- kurze Cue-Abschnitte,
- `IntersectionObserver`,
- CSS Custom Properties,
- `transform`,
- `opacity`,
- `filter`,
- Masken und Vignetten,
- diskrete Szenenzustände.

Optional darf `ScrollTimeline` als progressive Kür verwendet werden. Die Seite darf davon nicht abhängen.

Nicht verwenden:

- Scrolljacking,
- `preventDefault` für normales Scrollen,
- künstliche Scrollgeschwindigkeit,
- WebGL,
- Three.js,
- Canvas als Informationsquelle,
- große Animationsbibliothek,
- neue Runtime-Abhängigkeit.

## Szenennavigation

Eine kompakte Navigation soll die fünf Akte erreichbar machen:

1. Was und warum
2. Empfehlungen
3. Belege
4. Stimmen und Änderungen
5. Zählen und Archiv

Anker und Hash-Navigation müssen funktionieren.

## Tastatur

- normale Tab-Reihenfolge folgt der Dokumentreihenfolge,
- Skiplinks zu Empfehlungen, Verfahren und Protokoll,
- fokussierbare Pulte nur dann, wenn sie echte alternative Inhalte steuern,
- sichtbare `:focus-visible`-Zustände,
- Hash-Direktaufruf und Browser-Zurück funktionieren,
- bei Fokus auf einen aktuell ausgeblendeten Szeneninhalt wird die passende Szene ohne Verzögerung sichtbar.

---

# 6. Eigenständiges mobiles Konzept

Mobil ist kein verkleinerter Desktop-Ratssaal.

Baue ein **Sitzungsbuch mit Raumfenstern**.

Reihenfolge:

1. Leitfrage und Was/Warum.
2. Vier aktuelle Empfehlungen mit sofort sichtbaren Spendenlinks.
3. Kurze Mechanismuserklärung.
4. Breites Ratssaal-Fenster als atmosphärischer Trenner.
5. Frage und Vorzimmer.
6. Drei Modellkapitel.
7. Sichtbare Änderungen.
8. Zählregel.
9. Veröffentlichung und Archiv.

Regeln:

- keine fragile `100vh`-Sticky-Kamera,
- keine horizontal abgeschnittenen Desktoppanels,
- bei Nicht-Konsens alle Links gleichwertig sichtbar,
- direkte Spendenlinks ohne Aufklappen erreichbar,
- Bildfenster mit bewusstem `object-position`,
- Protokolltexte normal lesbar,
- 320 CSS px und 200 Prozent Zoom müssen funktionieren.

---

# 7. Progressive Enhancement und No-JS

Die vollständige Wahrheit muss bereits im prerendered HTML stehen.

Ohne JavaScript müssen erreichbar sein:

- Leitfrage,
- Was und warum,
- alle vier aktuellen Ergebnisse,
- alle abweichenden Organisationen,
- Stimmenzahlen,
- Modellattribution,
- Vorbehalte,
- Erst- und Schlussvoten,
- sichtbare Änderungen,
- Kosten,
- Korrekturhinweise,
- Dissenszugang,
- direkte Spendenlinks,
- vollständiges Sitzungsprotokoll,
- Archiv.

Die lineare HTML-Fassung ist der Grundzustand.

Erst nach erfolgreicher Clientinitialisierung darf eine Enhancement-Klasse die Desktopinhalte in die sticky Bühne überführen.

Kein Element mit fachlicher Information darf ausschließlich in einem dekorativen Layer existieren.

Native `<details>` dürfen für lange Protokolltexte verwendet werden.

---

# 8. Datenregeln

## Kanonische Organisationsidentität

Organisationen werden ausschließlich über `organization_id` aufgelöst.

Verwende `organizations.json` als Wahrheit für:

- `canonical_name`,
- `beschreibung`,
- `donation_url`.

Niemals Namen per Stringvergleich zusammenführen.

Modell-URLs aus Prosa niemals als Spendenlink verwenden.

## Fehlende Registry-ID

Bei unbekannter oder widersprüchlicher `organization_id`:

- keine Ersatzorganisation erfinden,
- klare Datenwarnung rendern,
- keinen Spendenlink erzeugen,
- Test fehlschlagen lassen.

## Fehlende Spenden-URL

Bei `donation_url: null`:

> Kein kuratierter direkter Spendenweg veröffentlicht.

Keine tote Schaltfläche.

## Begründungen

Nicht als Begründung verwenden:

- `rationale_md`.

Es enthält Aggregations-Boilerplate.

Zulässige Darstellung:

- Registrybeschreibung als Beschreibung der Organisation,
- vollständiges `content_md` als publiziertes Votum,
- vorhandene `summary` oder `dissent_highlights` nur mit Korrekturhinweisen,
- keine selbst erzeugten Kurzbegründungen.

## Dissens und Korrektur

- `dissent_md` als echtes Markdown behandeln,
- eingebettete JSON-Codeblöcke robust darstellen,
- horizontales Scrollen in Codeblöcken,
- keine Inhalte per Regex extrahieren,
- `correction_notice.text` als Markdown behandeln,
- Korrekturhinweis vor potenziell widersprüchlichen älteren Zusammenfassungen zeigen.

## Runden

Runden anhand `kind` identifizieren, nicht nur anhand der Nummer.

Relevante Arten:

- `initial_vote`,
- `final_vote`.

Jede Iteration muss fehlende `votes` tolerieren.

## Konfidenz

- `null` bedeutet „nicht publiziert“,
- nicht als 0 Prozent darstellen,
- nicht zur visuellen Siegerwahl nutzen,
- nur als ergänzende publizierte Information anzeigen.

## Unaufgelöste Stimmen

`unresolved_votes` dürfen nicht verschwinden.

Sie müssen als Datenproblem sichtbar oder im Build explizit behandelt werden.

---

# 9. Technische Architektur

## Produktive Dateien

Die Implementierung erfolgt innerhalb von `site/`.

Erwarte mindestens Änderungen an:

- `site/src/routes/+page.server.js`
- `site/src/routes/+page.svelte`
- `site/src/routes/+layout.svelte`
- `site/src/lib/server/content.js`

Lege bei Bedarf an:

- `site/src/lib/server/homepage.js`
- `site/src/lib/server/homepage.test.js`
- `site/src/lib/server/markdown.js`
- `site/src/lib/components/home/HomeIntro.svelte`
- `site/src/lib/components/home/CouncilStage.svelte`
- `site/src/lib/components/home/StageNavigation.svelte`
- `site/src/lib/components/home/RecommendationLedger.svelte`
- `site/src/lib/components/home/RecommendationEntry.svelte`
- `site/src/lib/components/home/ModelLectern.svelte`
- `site/src/lib/components/home/RevisionMark.svelte`
- `site/src/lib/components/home/CountingMachine.svelte`
- `site/src/lib/components/home/Antechamber.svelte`
- `site/src/lib/components/home/ProtocolDisclosure.svelte`
- `site/src/lib/components/home/ArchiveDoor.svelte`
- `site/src/lib/components/home/CouncilStageController.svelte`
- `site/src/lib/components/home/home.css`

Die konkrete Dateigrenze darf abweichen, wenn eine klarere Architektur entsteht.

## Serverseitiges View-Model

Erzeuge ein explizites Homepage-View-Model mit mindestens:

```text
currentSession
recommendations[]
modelTracks[]
revisions[]
correction
dissent
costs
archive[]
```

Datenlogik bleibt serverseitig beziehungsweise buildzeitlich.

Der Clientcontroller kennt nur Szenen-IDs und visuelle Zustände. Er berechnet keine Empfehlungen.

## Gemeinsame Ergebnisprimitive

Konsens, Vorbehalt und Nicht-Konsens sollen über dieselbe Datenprimitive gerendert werden.

Vermeide eine zweite, divergierende Ergebnislogik nur für die Bühne.

## Sitzungsdetailroute

Die Homepage ist Priorität.

Ändere die Sitzungsdetailroute nur dort, wo gemeinsame Registry- oder Revisionsprimitive notwendig sind, damit Homepage und Vollprotokoll nicht widersprechen.

Kein vollständiges Redesign aller Dokumentrouten in diesem Auftrag.

---

# 10. Assets

Suche zunächst die vorhandenen Originale im Repository, insbesondere unter:

- `sol-build/site/static/`
- `sol-build/`
- `serve/`

Erwarte Ratssaal und Vorzimmer.

Kopiere die Originalbytes unverändert in einen produktiven Pfad, zum Beispiel:

- `site/static/media/provenance/ratssaal.png`
- `site/static/media/provenance/vorraum.png`

Dokumentiere:

- Ursprungspfad,
- SHA-256,
- Dateigröße,
- Abmessungen.

Lege an:

- `site/static/media/ASSETS.md`

Erzeuge keine neu komprimierten Derivate, wenn die C2PA-Provenienz dabei ungeprüft verloren geht.

Für diese Implementierung ist es akzeptabel:

- den Ratssaal als priorisiertes Desktopbild zu laden,
- das Vorzimmer lazy zu laden,
- die Originale mit festen Dimensionen einzubinden,
- Performance durch einmalige Nutzung, korrektes Preloading und Lazy Loading zu begrenzen.

Keine externen CDNs.

Keine externen Schriften.

---

# 11. Gestaltungssystem

Entwickle ein kleines, projektspezifisches Token-System:

## Farben

- kaltes tiefes Mondblau,
- Graphit,
- warmes Messing,
- Honigbernstein,
- alter Stein,
- gebrochenes Papierweiß,
- gedämpftes Grün nur für die Pflanze beziehungsweise sehr sparsame Statusdetails.

Keine leuchtenden SaaS-Akzentfarben.

## Typografie

Verwende selbst gehostete vorhandene Schriften oder Systemschriften.

Die Typografie darf institutionell, literarisch und technisch wirken, ohne historisierende Freizeitparkästhetik.

Trenne:

- große Leitfrage,
- klare Organisationsnamen,
- kleine Protokollmetadaten,
- mechanische Labels,
- längere Lesetexte.

## Oberflächen

Erlaubt:

- Papier,
- Schiefer,
- graviertes Messing,
- Stein,
- dunkles Holz,
- dünne Lichtkanten,
- matte Vignetten.

Verboten:

- Glasflächen,
- starke Blur-Karten,
- Standard-Dashboard-Kacheln,
- massive opake Boxenwand,
- Neon,
- Hochglanz,
- futuristische Hologramme.

## Licht als Information

Jedes funktionale Licht muss einen Daten- oder Szenenzustand ausdrücken.

Kein zufälliges dekoratives Aufleuchten.

---

# 12. Bewegung

Bewegung ist ruhig, mechanisch und sparsam.

Geeignet:

- sanfte Kameraannäherung,
- Lichtfokus,
- Papierregister, die sich einschieben,
- Messingmarken, die ihre Bahn wechseln,
- Türüberblendung zum Vorzimmer,
- ruhige Vignette,
- sehr langsame Maschinenbewegung.

Nicht geeignet:

- federnde Animation,
- Partikeleffekte,
- hektische Parallaxe,
- permanente Zahnradrotation,
- Cursor-Gimmicks,
- Mausverfolgung,
- lange unüberspringbare Introanimation.

Übergangsdauer:

- ungefähr 350 bis 700 ms,
- keine Information von zeitlicher Reihenfolge abhängig machen.

---

# 13. Reduced Motion

Bei `prefers-reduced-motion: reduce`:

- keine scrollgebundene Kamera,
- keine Parallaxe,
- keine Lichtwanderung,
- keine Zahnradrotation,
- keine erzwungene Smooth-Scroll-Bewegung,
- Szenen sofort oder mit sehr kurzer Opazitätsänderung wechseln,
- lineare Dokumentstruktur bevorzugen, falls sticky irritiert.

Alle Zustände bleiben durch Text, Position und Typografie verständlich.

---

# 14. Barrierefreiheit

Erfülle mindestens:

- genau ein sinnvolles `<h1>`,
- logische Überschriftenhierarchie,
- Landmarken,
- Skiplinks,
- Tastaturnavigation,
- sichtbare Fokuszustände,
- 44 × 44 CSS px Touchziele,
- WCAG-AA-Kontrast für funktionalen Text,
- 200 Prozent Zoom,
- Reflow bei 320 CSS px,
- keine abgeschnittenen sticky Texte,
- keine Farbe als einzige Zustandsinformation,
- „2 von 3“ als Text,
- „unter Vorbehalt“ als Text,
- „keine Einigung“ als Text,
- Durchstreichung zusätzlich sprachlich erklären,
- externe Links kennzeichnen,
- keine ungefragten neuen Tabs,
- sinnvolle Alt-Texte,
- dekorative Wiederholungen mit `alt=""`,
- lange Codeblöcke scrollbar.

Die drei Modelle müssen gleichrangig sein in:

- DOM-Reihenfolge,
- Fläche,
- Kontrast,
- Fokusbehandlung.

---

# 15. Tests ohne neue Runtime-Abhängigkeiten

Führe den produktiven Build aus und ergänze nach Möglichkeit Tests mit Node-Bordmitteln.

Keine neue Runtime-Abhängigkeit.

Neue Dev-Abhängigkeiten nur, wenn absolut erforderlich. Bevorzuge `node:test` und `node:assert`.

Mindestens testen:

1. Neueste Sitzung wird nach `number` gewählt.
2. Registryauflösung erfolgt über `organization_id`.
3. Unbekannte ID schlägt fehl.
4. Spendenlink kommt ausschließlich aus der Registry.
5. `donation_url: null` wird korrekt behandelt.
6. `dissent_highlights` funktioniert als Array und String.
7. Runden ohne `votes` verursachen keinen Fehler.
8. Revisionen werden aus Erst- und Schlussvotum abgeleitet.
9. Konditionale Stimmen bleiben sichtbar.
10. `2026-07c` zeigt:
    - vier Konsensresultate,
    - Säule A mit Vorbehalt,
    - Säule B mit 2 von 3,
    - sichtbare Revisionen.
11. `2026-07` zeigt:
    - Säule A mit drei gleichwertigen Organisationen,
    - drei direkte Links,
    - keinen künstlichen Sieger.
12. Das gebaute `site/build/index.html` enthält ohne JavaScript:
    - aktuelle Organisationen,
    - Stimmenzahlen,
    - Spendenlinks,
    - Mechanismuserklärung,
    - Kosten,
    - Link zum vollständigen Protokoll.

Füge ein npm-Skript für die neuen Node-Tests hinzu, sofern es ohne zusätzliche Pakete möglich ist.

---

# 16. Build- und Qualitätsprüfung

Führe mindestens aus:

```bash
cd site
npm ci
npm run build
```

Falls du ein Testskript ergänzt:

```bash
npm test
```

Starte anschließend:

```bash
npm run preview -- --host 127.0.0.1
```

Prüfe die produktive Ausgabe aus `site/build/`, nicht nur den Dev-Server.

Teste mindestens:

- Desktop ungefähr 1440 × 900,
- Desktop ungefähr 1024 × 768,
- Mobil ungefähr 390 × 844,
- Mobil ungefähr 320 × 700,
- JavaScript deaktiviert,
- Reduced Motion,
- Tastatur,
- 200 Prozent Zoom.

Falls lokale Browser- oder Screenshotwerkzeuge verfügbar sind, erzeuge:

- `docs/review/home-desktop.png`
- `docs/review/home-mobile.png`
- `docs/review/home-nojs.png`

Falls nicht verfügbar, dokumentiere das ehrlich.

---

# 17. Performanceziele

Ziele:

- kein WebGL,
- keine große neue Bibliothek,
- zusätzliches Szenen-JavaScript möglichst unter 15 KB gzip,
- Ratssaal nur einmal initial laden,
- Vorzimmer lazy laden,
- Bildmaße setzen,
- praktisch kein CLS,
- keine Tracker,
- keine externen Requests,
- keine fremden Fonts,
- keine doppelten Plate-Downloads.

Erzeuge keine falschen Performancebehauptungen. Berichte gemessene oder beobachtete Werte.

---

# 18. Nicht verändern

Ändere nicht:

- `sessions/**`
- `journal/**`
- `schedule.json`
- `gremium/**`
- `schema/**`

Ändere `sol-build/` nicht, außer es ist für einen ausdrücklich dokumentierten Assetkopiervorgang notwendig. Der alte Build bleibt Referenz.

Baue keinen neuen Prototypordner.

Erzeuge kein separates `index.html` außerhalb von SvelteKit.

---

# 19. Arbeitsweise

Arbeite in dieser Reihenfolge:

1. Repositoryzustand und aktuelle Assets prüfen.
2. View-Model und Datenregeln implementieren.
3. Node-Goldentests für Konsens und Nicht-Konsens ergänzen.
4. Semantischen No-JS-Grundzustand bauen.
5. Mobile Fassung fertigstellen.
6. Desktopbühne progressiv darüberlegen.
7. Fokus, Hash, Tastatur und Reduced Motion ergänzen.
8. Assets und Provenienzdokumentation integrieren.
9. Produktionsbuild und Tests ausführen.
10. Produktive Ausgabe visuell prüfen.
11. Nur reale Probleme korrigieren.
12. Abschlussbericht schreiben.

Treffe begründete Entscheidungen selbstständig.

Frage nur nach, wenn:

- der Datenvertrag die fachliche Wahrheit nicht eindeutig hergibt,
- ein geschützter Pfad verändert werden müsste,
- eine neue Abhängigkeit zwingend erforderlich wäre,
- ein Asset fehlt und keine belastbare Alternative vorhanden ist.

---

# 20. Deliverables

Am Ende müssen vorhanden sein:

## Produktiver Code

Direkt in `site/`, vollständig buildbar und deploybar.

## Neue Startseite

Mit:

- Was und warum,
- Ursprungsgeschichte,
- vier aktuellen Ergebnissen,
- direkten Spendenlinks,
- Mechanismuserklärung,
- Vorzimmer,
- drei gleichwertigen Modellpulten,
- sichtbaren Änderungen,
- mechanischer Zählmaschine,
- Veröffentlichung,
- Archiv.

## Datenunterstützung

Für:

- Konsens,
- Konsens mit Vorbehalt,
- Nicht-Konsens,
- fehlende Spenden-URL,
- sichtbare Revisionen,
- Korrekturhinweise,
- Kosten.

## Progressive Enhancement

Vollständige semantische Ausgabe ohne JavaScript.

## Mobile

Eigenständige, fertige mobile Komposition.

## Tests

Daten- und No-JS-Goldens mit realen Sitzungen.

## Dokumentation

Aktualisiere:

- `site/README.md`

Lege an:

- `site/static/media/ASSETS.md`
- `docs/codex-build-report.md`

Der Abschlussbericht enthält:

1. Kurzbeschreibung der umgesetzten Designidee.
2. Geänderte und neue Dateien.
3. Tatsächlicher Datenfluss.
4. Konsens- und Nicht-Konsensdarstellung.
5. Revisionsdarstellung.
6. No-JS-Verhalten.
7. Mobile Verhalten.
8. Accessibility-Entscheidungen.
9. Asset- und Provenienzbehandlung.
10. Ausgeführte Befehle mit Exit-Code.
11. Buildwarnungen und verbleibende Probleme.
12. Testresultate.
13. Nicht umgesetzte Punkte und ehrliche Gründe.
14. Pfad der produktiven Ausgabe.

---

# 21. Abnahmekriterien

Der Auftrag ist erst abgeschlossen, wenn alle folgenden Punkte erfüllt sind:

- Die neue Startseite liegt im produktiven SvelteKit-Pfad.
- `npm run build` erzeugt erfolgreich `site/build/`.
- Die Seite wirkt wie eine zusammenhängende räumliche Bühne, nicht wie ein Kartenstapel.
- Das Was und Warum ist im ersten Nutzungsgang verständlich.
- Die vier aktuellen Bereiche sind früh auffindbar.
- Spendenlinks führen direkt zur Registry-URL der Organisation.
- Über NobleCause fließt laut UI kein Geld.
- Der Mechanismus wird in zwei kurzen Sätzen ohne Fachbegriffe erklärt.
- Drei Modelle erscheinen gleichrangig.
- Erst- und Schlussvoten werden aus echten Daten gelesen.
- Änderungen bleiben sichtbar.
- Uneinigkeit wird gleichwertig und ohne Fehlerästhetik gezeigt.
- Die Zählmaschine wird als nicht-intelligentes Zählwerk dargestellt.
- Die aufwendige Ebene erfindet keine Wahrheit.
- Ohne JavaScript bleibt der vollständige Kerninhalt vorhanden.
- Mobil ist eine eigenständige Gestaltung vorhanden.
- Reduced Motion funktioniert.
- Tastaturnavigation funktioniert.
- Ratssaal und Vorzimmer sind atmosphärisch integriert.
- Kein zweiter, nicht deployter Prototyp wurde gebaut.
- Der Abschlussbericht enthält nur verifizierte Ergebnisse.

---

# 22. Letzte Leitfrage

Prüfe jede Designentscheidung an dieser Frage:

> **Trägt die Szene den Zweck oder frisst sie ihn?**

Die Antwort soll weder eine nüchterne Dokumentseite noch ein unlesbares Kunstprojekt sein.

Das Ziel ist beides zugleich:

> **Ein beeindruckender öffentlicher Ratssaal und ein glaubwürdiges, vollständig überprüfbares Spendenprotokoll.**

Beginne jetzt mit der Implementierung.
