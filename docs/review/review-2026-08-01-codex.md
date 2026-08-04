# Go-live-Review 2026-08-01 — Codex

Geprüfter Stand: `review-2026-08-01`, Commit `44f47cff80cbf5223c4db78736afeae3f73a0318`.

## Findings

### 1. Der Produktions-Deploy baut mit der ausdrücklich inkompatiblen Node-Version

- **Ort:** `.github/workflows/deploy.yml:26–37`
- **Beobachtet:** Der Workflow installiert Node 22. Der für diesen Stand festgelegte und lokal erfolgreiche Build läuft mit Node 20.20.2; laut Go-live-Auftrag brechen andere Node-Versionen wegen der nativen Rolldown-Bindings. Damit prüft der lokale Freigabenachweis nicht dieselbe Laufzeit wie der einzige Produktions-Deploy. Ein Push auf `master` kann vor `rsync` am Build scheitern; da noch nichts ausgeliefert ist, bliebe die Website unveröffentlicht.
- **Erwartet:** Der Deploy pinnt dieselbe nachgewiesene Runtime (Node 20.20.2, npm 10.8.2) und führt damit den gelockten Build aus.
- **Schwere:** **blockiert-go-live**

### 2. Modelltext gelangt als unbereinigtes HTML in Besucher-Browser

- **Ort:** `site/src/lib/server/content.js:13–15`; Senken u. a. `site/src/routes/sitzungen/[id]/+page.svelte:130–141,155–159,175–183`, `site/src/routes/journal/[id]/+page.svelte:111–116`, `site/src/lib/components/rooms/ArchiveRoom.svelte:167–175,215`
- **Beobachtet:** `marked.parse` lässt eingebettetes HTML stehen; das Ergebnis wird mit `{@html}` eingesetzt. Die als „trusted build-time content“ kommentierten Sitzungsvoten und Wart-Dossiers stammen jedoch aus Modellantworten bzw. Web-Recherche. Eine Antwort mit z. B. einem HTML-Element samt Event-Handler wird beim nächsten Build origin-eigenes aktives HTML. Das kann Besucher umleiten, die Darstellung des Rekords verändern oder Inhalte unter der Domain vortäuschen. „Build-time“ macht die Quelle unveränderlich, nicht vertrauenswürdig.
- **Erwartet:** Der Wortlaut bleibt vollständig erhalten, wird aber mit einer expliziten, getesteten Markdown-Policy gerendert, die Roh-HTML und gefährliche URL-Schemata nicht ausführbar werden lässt.
- **Schwere:** **blockiert-go-live**

### 3. Eine formal misslungene Modellantwort kann als unvollständige Sitzung veröffentlicht werden

- **Ort:** `gremium/run_session.py:31–60,277–286,330–367,840–851,884–934`; Commitpfad `.github/workflows/session.yml:91–101`
- **Beobachtet:** Ein erfolgreicher API-Call wird unabhängig von der Antwortstruktur akzeptiert. Fehlt der JSON-Block oder fehlen Empfehlungen/Bereiche, wird daraus eine leere Liste. Der Aggregator überspringt einen Bereich ohne Kandidaten (`continue`) und erzeugt keinen Fehler. Auch `unresolved` bleibt in diesem Fall leer; anschließend werden `session.json` und `schedule.json` geschrieben und vom Workflow ohne Schema-/Vollständigkeitsprüfung committet. So kann die nächste Sitzung weniger als vier Bereiche oder weniger als drei verwertbare Schlussvoten enthalten und trotzdem zum neuesten öffentlichen Rekord werden. Der Frontend-Loader erwartet seinerseits `session.recommendations.map(...)` und prüft weder vier eindeutige Bereiche noch die Vollständigkeit der Voten.
- **Erwartet:** Vor Kurzfassung, Persistenz und Commit muss hart validiert werden: je erwartetem Modell genau ein auswertbares Schlussvotum, je Modell genau ein Votum pro A–D, erlaubte Typen/Werte und nach Aggregation genau ein Ergebnisobjekt pro Bereich. Fehler publizieren nur Rohartefakte, keinen Rekord.
- **Schwere:** **blockiert-go-live**

### 4. Der Wart kann den String `"false"` als Einberufung **JA** publizieren

- **Ort:** `gremium/run_wart.py:301–315,321–341`
- **Beobachtet:** Nach dem JSON-Parse wird nur `delta_assessment` verlangt. `convene` wird mit `bool(parsed.get("convene"))` umgewandelt. In Python sind nichtleere Strings wahr; eine geringfügig formatabweichende Modellantwort mit `"convene": "false"` wird daher als `true` ins Journal geschrieben und zieht den Sitzungstermin vor. Für `findings`, `search_queries` und die übrigen Felder gibt es ebenfalls keine Typprüfung. Der robuste `stop_reason`-Guard schützt nicht vor einer vollständigen, aber typfalschen Antwort.
- **Erwartet:** Die strukturierte Wart-Antwort wird vor jeder Entscheidung gegen einen strikten Vertrag geprüft; `convene` muss ein echtes JSON-Boolean sein, sonst bricht der Lauf ohne Journal-/Schedule-Schreibvorgang ab.
- **Schwere:** **blockiert-go-live**

### 5. Sitzung und Wart sind gegeneinander nicht serialisiert und schreiben dieselbe Schedule-Datei

- **Ort:** `.github/workflows/session.yml:37–39,91–101`; `.github/workflows/wart.yml:8–10,40–50`; `gremium/run_session.py:136–147,947–951`; `gremium/run_wart.py:232–244,336–341`
- **Beobachtet:** Die Workflows verwenden verschiedene Concurrency-Gruppen (`gremium-session` und `wart-research`), dürfen also parallel laufen. Beide checken denselben alten Commit aus, ersetzen `schedule.json` und pushen. Der zweite Push scheitert typischerweise als non-fast-forward, nachdem API-Kosten und lokale Rekorddateien bereits entstanden sind; ungünstiger ist, dass die inhaltlich zuletzt erzeugte Schedule-Version nicht zwingend die zuletzt publizierte ist. Die Concurrency-Grenze schützt nur gleichartige Läufe, nicht die gemeinsame Schreibnaht.
- **Erwartet:** Alle Schreiber derselben Rekord-/Schedule-Naht werden repo-weit serialisiert oder integrieren nach einem frischen Fetch mit expliziter Konfliktprüfung; ein Lauf darf erst auf einer nachweislich aktuellen Basis entscheiden.
- **Schwere:** **punktversion**

### 6. „Konditional“ wird aus Prosa geraten und kann nachweislich falsch positiv sein

- **Ort:** `gremium/run_session.py:315–327,376–406`
- **Beobachtet:** Die veröffentlichte Zahl `conditional_count` entsteht per Regex über den freien Titel. Der Marker `conditional` trifft auch `unconditional`; deutsche Negationen wie „nicht konditional“ treffen ebenfalls. Damit kann ein festes Votum öffentlich als Vorbehalt erscheinen. Diese abgeleitete Ergebnisaussage wird anschließend in Konvergenz, Begründung und Website angezeigt, obwohl kein strukturiertes Boolean des Modells vorliegt.
- **Erwartet:** Konditionalität ist ein strikt strukturiertes Feld des Votums oder wird nicht als gezählte Tatsache publiziert; freie Prosa bleibt Wortlaut und wird nicht klassifiziert.
- **Schwere:** **punktversion**

### 7. Der Freigabe-Build ist grün, aber nicht warnungsfrei

- **Ort:** `site/src/lib/components/rooms/CouncilRoom.svelte:28–29`; `site/src/lib/components/rooms/StageHero.svelte:38–40`
- **Beobachtet:** `npm test` baut erfolgreich und alle 31 JS-Tests bestehen, Svelte meldet im SSR- und Client-Build jedoch jeweils zwei Warnungen über nur initial erfasste Prop-Werte (`orgEn`, `passage`). Das widerspricht der dokumentierten Definition „Build warnungsfrei“. Bei `passage` ist außerdem eine spätere Prop-Änderung nicht garantiert reaktiv.
- **Erwartet:** Entweder die Werte sind bewusst unveränderlich und werden ohne irreführende reaktive Form deklariert, oder die Ableitung wird tatsächlich reaktiv; der Produktions-Build endet ohne Compilerwarnungen.
- **Schwere:** **punktversion**

### 8. Die Startansicht beantwortet „wo“, aber „warum diese Organisation?“ nicht in 30 Sekunden

- **Ort:** Route `/`, Referenz-Viewports 1440×900 und 390×844 (`docs/review/referenz-review-2026-08-01/study-1440.png`, `study-390.png`)
- **Beobachtet:** Desktop zeigt sofort vier Organisationen, Zählstand und Spendenlinks; Mobil zeigt im ersten langen Bühnenbild noch keine Empfehlung. In beiden Fällen erklärt die sichtbare Ergebnistafel nur, wie viele Modelle dieselbe Organisation nannten, nicht warum gerade sie empfohlen wird. Die in der Registry vorhandene Beschreibung bzw. die Begründungen liegen erst tiefer im Raum/Protokoll. Ein neuer Besucher findet auf Desktop schnell den Spendenort, aber nicht den organisationsbezogenen Grund; auf Mobil nicht einmal den Spendenort im ersten Viewport.
- **Erwartet:** Ohne den versiegelten Wortlaut zu paraphrasieren, führt die erste Ergebnisfläche sichtbar zu der vorhandenen wörtlichen/registrierten Begründung; mobil ist der Ergebniszugang vor oder unmittelbar nach der Leitfrage klar auffindbar.
- **Schwere:** **punktversion**

### 9. Frage an die Gestaltung: zentrale Handlungslinks sind absichtlich sehr dunkel

- **Ort:** Routen `/`, `/ratssaal/`, `/archiv/` bei 1440×900; Referenzaufnahmen `*-1440.png`
- **Beobachtet:** Die Ergebnisplatte und der Archiv-Pult-Link liegen im ersten Frame teilweise sehr dunkel über detailreichen Plates. Beim Archiv ist „Vollständiges Protokoll öffnen“ in der Ruheaufnahme deutlich schwächer als dekorative Goldakzente. Das kann die gewünschte Vignette tragen, konkurriert aber mit der wichtigsten Handlung der jeweiligen Szene.
- **Erwartet:** Frage: Soll die zentrale Handlung in Ruhe absichtlich erst beim Erkunden lesbar werden? Falls nein, sollte nur ihre Ruhe-Luminanz gegen die echten Pixel angehoben werden, ohne Bildsprache oder Dunkelheit neu zu verhandeln.
- **Schwere:** **geschmack**

## Prüfabschluss

**Geprüft:** Stand/Tag/Worktree; Backend und alle fünf Workflows statisch; Aggregation, Registry-Auflösung, Wart-Entscheid, Kosten-/Fehler- und Schreibpfade; Website-Datennaht, sechs Raumrouten, Explorer/Journal/Protokoll-Renderer, No-JS-/Sprachlogik; Build unter Node 20.20.2/npm 10.8.2; 31/31 Website-Tests; 18 Referenzaufnahmen visuell stichprobenartig gegen Struktur und Viewports.

**Nicht geprüft:** Keine kostenpflichtige API, kein Workflow und kein rekordschreibender Lauf; kein externer Netz-/Spendenlinktest; kein echter Screenreader-Durchgang; keine automatisierte Pixel-Kontrastmessung; kein belastbarer 50-Sitzungen-Lasttest; kein Produktionsbuild unter Node 22; Python-Aggregationstests nicht ausgeführt, weil im Review-Environment `pytest` nicht installiert war (keine Abhängigkeiten nachinstalliert); Preview-Routen wegen Prozess-/Netz-Namespace der Sandbox nicht per HTTP/Browser neu aufgenommen, daher kein eigener Pixel-Diff gegen die Referenzen.

**Beim nächsten Mal zuerst:** Mit korrigierter Deploy-Runtime einen isolierten Produktions-Deploy-Dry-run fahren und danach adversarielle, vollständig lokale Fixtures für typfalsche/fehlende Voten, `convene: "false"`, Roh-HTML im Modelltext sowie einen zeitgleichen Wart-/Sitzungsschreibvorgang durch die gesamte Buildkette schicken.
