# Review 2026-08-01 — kimi

Stand: Tag `review-2026-08-01` (44f47cf), Worktree `nc-review-kimi`. Gelesen, gemessen,
gerechnet — nichts geändert, nichts committet, kein Lauf ausgelöst, der Geld kostet oder
Rekord schreibt. Build und Preview lokal (Node 20.20.2), zusätzlich Gegenprobe der
Build-Umgebung unter Node 22/25 (siehe Befund P8).

**Kurzfassung:** Ein Befund sperrt für mich den Go-Live: Der Wöchentliche Wart recherchiert
nichtdeterministisch gegen die falsche Sitzung — die beiden letzten Research-Läufe (20. und
27. Juli) prüften die Empfehlungen der **überholten Sitzung 1**, während die Seite Sitzung 3
zeigt. Für Säule B und C fand die auf der Startseite behauptete „letzte Prüfung" der aktuellen
Empfehlungen nie statt, und der nächste automatische Lauf (Mo 2026-08-03) wiederholt das.
Die reparierte Registry-Aggregation habe ich unabhängig nachgerechnet: Sie ist gegen die
Rohvoten dicht (Details unten, positiv vermerkt).

---

## blockiert-go-live

### B1 · Der Wart recherchiert gegen die überholte Sitzung 1 — die „letzte Prüfung" auf der Startseite deckt die aktuellen Empfehlungen B und C nicht

- **Ort:** `gremium/run_wart.py:81-94` (`latest_session()`), sichtbar in
  `journal/2026-07-20/entry.json` und `journal/2026-07-27/entry.json` (je `session_ref:
  "2026-07"`), Route `/journal/`, Route `/` (Zeile „Letzte Prüfung: 27. Juli 2026").
- **Beobachtet:** `latest_session()` sortiert Sitzungen nur nach dem Datumsstring
  (`entries.sort(key=lambda x: x[0], reverse=True)`, Zeile 93). Alle drei Sitzungen tragen
  dasselbe Datum (`2026-07-07`) — die Reihenfolge der Gleichen hängt damit von
  `iterdir()`-, also von der Dateisystem-Reihenfolge des Runners ab. Belegt ist der
  Ausfall bereits im Rekord: Die Läufe vom 20.07. und 27.07. haben `session_ref:
  "2026-07"` — Sitzung **1** (die mit dem damaligen Aggregationsfehler und ohne
  Säule-A-Konsens). Der Wart selbst hat sauber gearbeitet, aber auf falscher Basis: Sein
  Dossier vom 27.07. trägt die Zeile „**Bezug:** Sitzung 2026-07 (2026-07-07)" und
  recherchiert „Säule A — Einzelvoten (kein Konsens)", Malaria Consortium (Säule B alt;
  aktuell: Against Malaria Foundation) und GovAI (Säule C alt; aktuell: NTI). AMF und NTI
  wurden seit ihrer Empfehlung **nie** vom Wart geprüft. Der Journal-Einführungstext
  („…prüft wöchentlich per Web-Recherche die Evidenzlage zu den **jüngsten**
  Empfehlungen") ist für die zwei jüngsten Läufe falsch, und die Startseiten-Zeile
  „Letzte Prüfung: 27. Juli 2026" verspricht eine Aktualitätsprüfung, die für zwei von
  vier Empfehlungen nicht stattfand. Die Einberufungs-Entscheide dieser Läufe
  (`convene: false`) beruhen ebenfalls auf den überholten Empfehlungen — der
  Sicherheitsloop „neue Evidenz widerspricht einer Empfehlung" ist für die aktuellen
  Empfehlungen B und C blind. Die Wahl schwankte real: 08.07. traf der Lauf `2026-07b`,
  dann `2026-07c`, ab 20.07. zweimal `2026-07` — exakt das Bild einer
  runner-abhängigen Reihenfolge.
- **Erwartet:** „Jüngste Sitzung" muss deterministisch dieselbe sein, die die Site
  anzeigt. `run_session.prior_session()` sortiert bereits korrekt nach `(number, date)`
  (`run_session.py:105-118`), die Site ebenso (`content.js:40`, mit erklärendem
  Kommentar). Derselbe Schlüssel gehört in `run_wart.latest_session()`; zusätzlich
  wäre ein hartes Gate sinnvoll (Abbruch, wenn `session_ref.number` nicht das Maximum
  ist — der Defekt wäre dann am 20.07. laut aufgefallen statt still publiziert).
- **Schwere:** blockiert-go-live — der publizierte Rekord (zwei Journal-Einträge samt
  Einberufungs-Entscheiden) bezieht sich auf eine ersetzte Sitzung, die Site behauptet
  das Gegenteil, und der nächste Cron-Lauf schreibt den Fehler fort. Die Maschine läuft
  ab Montag automatisch weiter; ohne Fix ist jede Woche ein Münzwurf.

---

## punktversion

### P1 · Kein Inhalts-Gate vor Commit: eine Sitzung mit null auswertbaren Voten würde publiziert

- **Ort:** `gremium/run_session.py:786, 835, 841` + `.github/workflows/session.yml:91-101`.
- **Beobachtet:** Scheitert das JSON-Parsing aller drei Schlussvoten (`parsed = None`),
  liefert `aggregate_recommendations` leere `recommendations` **und** leere
  `unresolved_votes` — unauffällig. Die Sitzung läuft „erfolgreich" zu Ende,
  `session.json` wird committed und gepusht; das Frontend wirft nicht
  (`buildHomepageViewModel` wirft nur bei `unresolved_votes` bzw. unbekannten
  organization_ids, `homepage.js:145-147`), sondern rendert eine leere Ergebnis-Tafel
  („Die Antwort der letzten Sitzung" — ohne Antworten). Kein Workflow validiert
  `session.json` gegen `schema/session.schema.json` — das Schema existiert nur als
  Dokumentation.
- **Erwartet:** Mindest-Invarianten im Orchestrator vor dem Schreiben (≥1 Säule mit
  Kandidaten oder ≥1 explizitem unresolved-Eintrag; sonst Abbruch ohne Commit) und/oder
  Schema- + Plausibilitätsprüfung als Workflow-Schritt vor `git commit`.
- **Schwere:** punktversion — heute kein falscher Rekord, aber der Fehlerpfad
  „Formatabweichung aller Modelle" (im Auftrag als ungeprüft genannt) publiziert sich
  selbst.

### P2 · Der Konditional-Marker trifft Negationen — ein künftiges Votum kann im Rekord ins Gegenteil gedreht werden

- **Ort:** `gremium/run_session.py:320` (`_CONDITIONAL_MARKERS =
  konditional|conditional|bedingt|vorbehalt|vertag`).
- **Beobachtet:** Probe gegen die Funktion: Titel „Unbedingt empfohlen",
  „Vorbehaltlos empfohlen" und „Nicht konditional" liefern alle `conditional: True` —
  der Rekord würde einen Vorbehalt behaupten, den das Modell explizit verneint hat.
  Der aktuelle Rekord ist nicht betroffen (alle Titel der drei Sitzungen geprüft; der
  eine echte Treffer „… — konditional, mit Vertagungsantrag …" ist korrekt). Kein Gate
  würde einen Fehlgriff bemerken; `convergence.conditional_count` erscheint auf der
  Ergebnis-Tafel und in den Antwortzeilen.
- **Erwartet:** Wortgrenzen und Negations-Ausschluss (z. B. `unbedingt`,
  `vorbehaltlos`, `nicht/kein … konditional` ausschließen) — oder das im Code-Kommentar
  selbst empfohlene strukturierte Feld im Prompt.
- **Schwere:** punktversion — latent, aber ein Rekord-Fälschungsmechanismus, sobald ein
  Modell die naheliegenden Formulierungen wählt.

### P3 · Gleichstand in der Aggregation wird per Einfügereihenfolge entschieden — still

- **Ort:** `gremium/run_session.py:372` (`best_id = max(groups, key=…)`).
- **Beobachtet:** Votieren zwei Modelle für Org X und zwei für Org Y, gewinnt die
  zuerst eingefügte Gruppe (Config-Reihenfolge der Modelle) — ein „Konsens 2/3", der
  genauso gut Y sein könnte, ohne jeden Hinweis im Rekord. Mit drei Modellen nur
  erreichbar, wenn ein Modell **zwei Empfehlungen in derselben Säule** abgibt — vom
  Prompt untersagt, vom Parser aber still akzeptiert. Dass Modelle von der Vorgabe
  abweichen, ist kein Gedankenexperiment: GPT votierte 2026-07c HKI in Säule A **und**
  B. Probe bestätigt den Ausgang (X = erste Gruppe, `has_consensus: True`).
- **Erwartet:** Gleichstand → `has_consensus: False` (oder Abbruch mit Warnung);
  Mehrfach-Empfehlungen eines Modells je Säule mindestens als Warnung in den Rekord.
- **Schwere:** punktversion — seltene Konstellation, aber ein arbiträrer „Konsens" ist
  genau die Klasse Fehler, die das Projekt einmal öffentlich korrigieren musste.

### P4 · `dissent_md` enthält in allen drei Sitzungen den rohen JSON-Votum-Block — inklusive modellbehaupteter Spenden-URLs

- **Ort:** `gremium/run_session.py:67-69` (`extract_dissent`); sichtbar auf
  `/sitzungen/2026-07c/` und `/archiv/` („Dissens im Wortlaut" / „Wortlaut des Rates").
- **Beobachtet:** Der Regex erfasst von `## Dissens` alles bis zur nächsten
  `##`-Überschrift oder zum Textende. Der abgeschlossene ```json-Block steht danach —
  er landet komplett in `dissent_md` (in allen drei Sitzungen verifiziert). Die Seite
  rendert das Feld als Markdown: Im Ausklapp steht rohes JSON mit
  `"donation_url": "https://helenkellerintl.org/donate/"` — eine modellbehauptete URL,
  die ausdrücklich **nicht** die kuratierte Registry-URL ist
  (`giving.helenkellerintl.org/page/FUNUYQRJGHG`; die Registry-Notiz sagt, das alte
  `/donate/` leite auf die Startseite um). Genau die Halluzinations-Klasse, für die die
  Registry gebaut wurde, erscheint so doch auf der Seite — als Klartext in einem
  Code-Block, nicht klickbar, darum nicht blockierend. Nebenbefund: `generate_summary`
  erhielt `dissent_md[:6000]` mit diesem JSON-Rauschen. Fix-Falle: `sessions/**` ist
  unveränderlich — die Korrektur gehört in `extract_dissent` für künftige Läufe
  (Votum-Block vor der Extraktion abstreifen), nicht in den bestehenden Rekord.
- **Erwartet:** `dissent_md` = nur der Dissens-Abschnitt, ohne Maschinen-JSON.
- **Schwere:** punktversion.

### P5 · Archiv-Überschrift „Noch keine Einigkeit" widerspricht dem gezeigten Rekordstand

- **Ort:** `site/src/lib/i18n/de.js:300` / `en.js:298`, gerendert in
  `ArchiveRoom.svelte:180-215`, Routen `/archiv/` und `/en/archive/`.
- **Beobachtet:** Über den Dissens-Highlights der aktuellen Sitzung steht die statische
  Überschrift „Noch keine Einigkeit" (EN: „No agreement yet"). Sitzung 3 hat in allen
  vier Bereichen Konsens; die erste Highlight-Zeile darunter beginnt wörtlich „Säule A
  faktisch konvergiert …". Überschrift und Inhalt widersprechen sich auf derselben
  Seite, einen Scroll unter einer Ergebnis-Tafel mit vier Empfehlungen. Copy-Erbe aus
  der Zeit von Sitzung 1 (Säule A offen).
- **Erwartet:** Überschrift, die den Zustand nicht behauptet (z. B. „Dissens und
  Vorbehalte"), oder bedingte Copy nach `dissentOpen.length`.
- **Schwere:** punktversion — eine Formulierung, die etwas Falsches behauptet, direkt
  über dem Rekord.

### P6 · Der Protokoll-Eingang am Archiv-Pult läuft bei 390 px links aus dem Viewport

- **Ort:** `site/src/lib/components/rooms/ArchiveActors.svelte:216-254` (`.pult-label`),
  Route `/archiv/`, Viewport 390 — im eigenen Referenz-Shot
  `docs/review/referenz-review-2026-08-01/archive-390.png` sichtbar.
- **Beobachtet:** Die Beschriftung („SITZUNG 3 · 7. JULI 2026 / Vollständiges Protokoll
  öffnen →") ist per `right: 100%; width: max-content; white-space: nowrap` links an
  das Pult gehängt; der lange deutsche Titel ragt ~20–25 px über die linke
  Viewport-Kante — „Vollständiges Protokoll öffnen →" ist angeschnitten. Der Zustand
  steht so in der Referenz, ist also kein Regress — aber der Haupt-Einstieg in den
  Rekord ist auf der häufigsten Geräteklasse teilweise unleserlich.
- **Erwartet:** Label so begrenzen/umbrechen, dass es im Viewport bleibt (der Fluss-Link
  „Vollständiges Protokoll öffnen" existiert zusätzlich im Inhalt — er trägt, aber das
  Pult ist der inszenierte Eingang).
- **Schwere:** punktversion.

### P7 · `run_wart.write_schedule()` verwirft still jede Zeile, die es nicht kennt

- **Ort:** `gremium/run_wart.py:232-243`.
- **Beobachtet:** Die Funktion schreibt `schedule.json` aus genau drei Schlüsseln neu
  (`next_research`, `next_session`, `last_journal`). Jedes künftig manuell gepflegte
  Feld — etwa eine redaktionell vorbereitete Frage für die nächste Sitzung — wird beim
  nächsten Wart-Lauf kommentarlos gelöscht. `run_session.advance_schedule()`
  (`run_session.py:136-148`) macht es richtig: lesen, ein Feld mutieren, zurückschreiben.
- **Erwartet:** Ebenso mutierend schreiben statt neu bauen.
- **Schwere:** punktversion — heute keine Wirkung (die Datei hat nur die drei Felder),
  ein stiller Datenverlust bei der ersten Erweiterung.

### P8 · Deploy-Pfad: kein Fehler-Alarm, kein Test-Gate, Host-Key ohne Pinning — und die Node-Warnung ist überholt

- **Ort:** `.github/workflows/deploy.yml:29, 45, 47-51`.
- **Beobachtet (drei Punkte, ein Fundort):**
  1. `deploy.yml` ist der einzige Workflow ohne Fehler-Issue-Step. Ein Build-Bruch nach
     einem Bot-Push (z. B. das absichtlich laute `unresolved_votes`-Gate im View-Model)
     hinterlässt die alte Site und ruft niemanden — die anderen Workflows (session,
     wart, preflight, canary) zeigen, dass der Mechanismus existiert.
  2. `ssh-keyscan -H <ip> >> known_hosts` nimmt den Host-Key des VPS blind aus dem
     Netz. Ein MITM auf dem Deploy-Pfad ersetzt die ausgelieferte Site — bei einem
     Projekt, dessen Produkt die Unverfälschbarkeit des Rekords ist. Fingerprint als
     Secret pinnen.
  3. **Entkräftet, aber berichtenswert:** Der Auftrag warnt, der Build breche unter
     einer anderen Node-Version (deploy nutzt 22, verifiziert war 20.20.2). Ich habe
     den vollen Build unter Node 22.23.1 **und** 25.9.0 laufen lassen: beide bauen
     sauber (rolldown-Bindings sind vorkompiliert, ABI-stabil). Der Deploy mit Node 22
     ist damit kein Blocker — aber die Dokumentation (Briefing) und `deploy.yml`
     widersprechen einander, und `npm test` läuft im Deploy nicht.
- **Schwere:** punktversion (1+2), geschmack/Beobachtung (3).

### P9 · Die Klartext-Schicht (`plain`/`plain_en`) fehlt im Datenvertrag

- **Ort:** `schema/session.schema.json`, `sol-build/data-contract.md`,
  `site/src/lib/server/homepage.js:151-171`.
- **Beobachtet:** Die prominenteste neue Darstellungsschicht („Vereinfachte Fassung,
  verantwortet vom Wart" auf der Startseite, inkl. kuratierter EN-Fassung) wird aus den
  Session-Feldern `plain`/`plain_en` gelesen. Beide Felder stehen weder im Schema noch
  im Datenvertrags-Dokument (`additionalProperties: true` — keine Verletzung, aber
  Drift). Wer den Vertrag liest, lernt die Schicht nicht, die ein Besucher zuerst
  sieht; und das Freigabe-Verfahren für diese Felder ist nur in Code-Kommentaren
  beschrieben.
- **Schwere:** punktversion — der Vertrag, auf den sich die „versiegelte Datennaht"
  beruft, beschreibt die Realität nicht mehr vollständig.

### P10 · Wart-Doppel-Lauf am selben Tag erzeugt einen falschen CI-Fehler

- **Ort:** `gremium/run_wart.py:263-264` + `.github/workflows/wart.yml:63-77`.
- **Beobachtet:** Existiert `journal/<heute>/` bereits, bricht der Lauf hart ab —
  beabsichtigt (Unveränderlichkeit). Der Workflow wertet das als `failure()` und
  öffnet/kommentiert ein „CI-Fehler: Wart-Lauf"-Issue. Auslöser liegt nahe: manueller
  Dispatch plus Cron am selben Montag. Alarm-Müdigkeit bei den echten Kanälen.
- **Erwartet:** „Bereits vorhanden" als Exit 0 (oder eigenen Code, den der Workflow
  als Erfolg behandelt).
- **Schwere:** punktversion.

---

## geschmack

- **G1 — Akteurs-Namen drift:** Dieselbe Figur heißt auf einer Seite „The Scout"
  (Caption, `de.js:133`), „Der Späher" (Prozess-Röhre, `de.js:152`) und „Der Scout"
  (Rhythmuszeile, `de.js:119`); analog „The Warden" vs. „der Wart"/„Journal des Warts".
  Absicht (Eigenname vs. Rolle)? Ohne Glossar wirkt es wie zwei Akteure zu viel.
- **G2 — „Der Council tagt nicht nach Kalender" (`/idee/`) vs. „Laut Terminplan: 6.
  August 2026" (`/ratssaal/`) und `schedule.json` (Sitzungsdatum + 30 Tage):** Der
  Maschinen-Rhythmus *ist* kalenderisch, mit anlassbezogener Vorverlegung. Die
  Idee-Seite verspricht mehr Anlassbezug, als das System hat.
- **G3 — „die Kosten des Laufs in Euro, auf den Cent" (`/idee/`):** Gerechnet mit
  festem fx 0,85 und Listenpreisen aus `config.json`, nicht gegen die Abrechnung. Die
  Tokenzählung ist korrekt (Reasoning/Thoughts eingerechnet, Summen nachgerechnet) —
  aber „auf den Cent" verspricht Abrechnungsgenauigkeit, die niemand prüfen kann.
- **G4 — EN-Zeile „Last: not convened · July 27, 2026":** liest sich, als sei der
  Scout selbst „nicht einberufen" worden; gemeint ist „keine Einberufung empfohlen".
- **G5 — Deutsche Räume mit englischen Seitentiteln** („NobleCause — The Council",
  „— The Archive", `de.js:260, 305`), während die deutsche Study einen deutschen Titel
  trägt. Passt zur englischen Raumnamen-Ästhetik der deutschen UI, wirkt in
  Tab-Leiste/Teilen-Dialog uneinheitlich. Absicht?
- **G6 — Keine og:/twitter:-Meta-Tags, keine robots.txt/sitemap:** Der erste Eindruck
  in Messengern und Suche ist ungestaltet. Keine Rekordfrage — aber das Projekt lebt
  vom Geteilt-Werden.
- **G7 — Spendenlinks „(extern) ↗" öffnen im selben Tab:** Der Pfeil verspricht neuen
  Kontext; bei mehrstufigen Spendenformularen (AMF) ist der Rückweg holprig.
- **G8 — Referenz-Set-Dubletten:** `tafel-ruhe-1440.png` ≡ `study-1440.png` und
  `archive-1440.png` ≡ `pult-ruhe-1440.png` (md5-identisch). Zwei benannte Zustände
  der 18er-Liste sind gar keine eigenen Aufnahmen.
- **G9 — „kein Modell steuert den Prozess" (`/idee/`):** Für Zählung und Orchestrierung
  wahr; die Einberufungs-Entscheid (`convene`) ist Modell-Output und steuert den
  Terminplan. Ein Halbsatz („… die Zählung") machte den Satz exakt.
- **G10 — Das Zählwerk im Ratssaal zeigt „3 von 3" ohne Konditional-Hinweis an der
  Plakette** (`CouncilRoom.svelte:219-224`); die Reservation liegt eine Ebene tiefer
  („Reservation ▸", Zeile 256). An der sichtbarsten Stelle des Demut-Kanons wird die
  Unsicherheit weggeglättet.

---

## Positiv vermerkt — was ich geprüft habe und was trägt

- **Die Registry-Aggregation ist dicht.** Unabhängige Nachrechnung: alle
  Schlussvoten-Organisationsstrings der drei Sitzungen aus den committeten Rohantworten
  (`raw/r2-*.json`) extrahiert, gegen die Registry aufgelöst, Konsense selbst gezählt —
  deckt sich exakt mit den publizierten `recommendations` (inkl. der kniffligen Fälle
  „NTI | bio (…)", „Helen Keller Intl", GPTs HKI-in-B-Ausreißer 2026-07c → korrekter
  2/3-Konsens AMF). `reaggregate.py` im Dry-Run: **keine Differenzen** in allen drei
  Sitzungen. `correction_notice` vollständig, Commit-Platzhalter ersetzt.
- **Halluzinations-Schutz wirkt:** `donation_url` kommt ausschließlich aus der Registry
  (Code + Test `test_donation_url_comes_from_registry_not_vote`); die Seite zeigt für
  nicht verifizierte Registry-URLs (MIRI u. a.) keinen Link. Tests: 9/9
  `test_aggregate.py`, 31/31 JS-Tests — grün.
- **Permalinks sauber:** alle 63 internen hrefs/srcs des Builds auflösbar; kein
  `/sessions//`-Rest; Routen-Umzug vollständig; 404-Seite antwortet 404.
- **§0 hält strukturell:** Alle Versteck-Regeln sind an `html.stage-armed` (nur via JS,
  synchron im `<head>`) und `prefers-reduced-motion: no-preference` gekettet — ohne JS
  und mit Reduced-Motion ist der Inhalt vollständig (gemessen am ausgelieferten HTML:
  Tafel, Empfehlungen, Spendenlinks, Protokoll stehen im pragerenderten Markup).
- **Kostenrechnung konsistent:** alle drei Sitzungen nachgerechnet (Token × Preise ×
  fx), Wart-Web-Suche eingerechnet, Reasoning-/Thoughts-Tokens korrekt einbezogen;
  Summen stimmen mit dem Rekord überein. (Gegen die echte Abrechnung ungeprüft —
  kein Zugang.)
- **Kontrast, soweit ohne Browser messbar:** Tafel- und Masthead-Texte liegen auf
  nahezu schwarzem Scrim (an den Referenz-Pixeln gemessen: Hintergrund-Luminanz ≈
  0,00–0,01 → Kontrast weit über WCAG AA).
- **30-Sekunden-Test:** Desktop 1440 — bestanden: Tafel fix im ersten Viewport, vier
  Organisationen, Zählstand, Spendenlinks; das „Warum" trägt die Klartext-Zeile darunter
  (wörtlich aus `plain`, als „Vereinfachte Fassung" deklariert). Mobil 390 —
  eingeschränkt: der erste Screen trägt Frage, Szene und Prozess-Röhre, die Tafel folgt
  unmittelbar nach dem Hero im Fluss; findbar, aber nicht im ersten Blick.

---

## Drei Zeilen zum Schluss

- **Geprüft:** Maschine komplett gelesen (run_session, run_wart, reaggregate, prompts,
  organizations, preflight, donation_canary, envtools, run_commission, alle fünf
  Workflows); Aggregation unabhängig nachgerechnet; Kosten nachgerechnet;
  Marker-/Gleichstands-Proben; Build unter Node 20/22/25; Preview; alle Routen
  (DE+EN, Räume, Explorer, Journal, idee/manifest/impressum); interne Links;
  Schema-Pflichtfelder; Referenz-Screenshots gesichtet und an ausgewählten Stellen
  pixelgemessen; Test-Suiten ausgeführt (9/9, 31/31).
- **Nicht geprüft:** pixelgenauer Render-Abgleich gegen die Referenzen (kein
  Headless-Browser ohne Netzzugriff — struktureller Abgleich + Sichtung stattdessen);
  Screenreader- und Tastatur-Durchgang interaktiv (nur statisch: aria-Muster,
  `lang`-Attribute, DOM-Reihenfolge — das Pult als zweiter Tab-Stopp ist m. E. als
  Protokoll-Kurzweg vertretbar); Kontrast flächendeckend (nur Stichproben); Token-Kosten
  gegen die echte Provider-Abrechnung; die Workflows in echter Ausführung (nur statisch);
  das Archiv mit 50 Sitzungen als gerenderte Seite (statisch: lange Liste, kein Umbruch-
  Risiko, keine Paginierung); die Wirkung der Prompttexte auf die Modelle empirisch
  (nur gelesen — die Befangenheitsregel nennt Sitzung 1 wörtlich, das ist Transparenz,
  die zugleich primt).
- **Beim nächsten Mal zuerst:** den `session_ref` des nächsten Journal-Eintrags
  (beweist, ob B1 repariert ist), danach den Dissens-Beschnitt (P4) und das
  Inhalts-Gate (P1) — und einmal den Deploy-Pfad real: erster Push auf `master`,
  Build-Log, Cache-Header, fertig.
