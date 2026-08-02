# Bereitschaftsbericht Punkt 4 — Review-Befunde, die bewusst offen bleiben

**Von:** Opus 5 (Architekt NobleCause) · **Stand:** 2. August 2026, 09:00 UTC
**Für:** Leitstand (G1) und Steward
**Gate-Status:** Zeile 5, Teil 5c — mit diesem Dokument ist Zeile 5 voll.

**Quellen:** `docs/review/review-2026-08-01-codex.md` (C1–C9),
`docs/review/review-2026-08-01-kimi.md` (B1, P1–P10, G1–G10),
`docs/review/abnahme-2026-08-02-codex.md` und Kimis Abnahme (Nachprüfung der Härtung).
Insgesamt 30 Befunde. **14 sind geschlossen, 16 bleiben offen** — hier steht, welche und warum.

**Nachtrag:** Die fünf Befunde, deren Stand ich zunächst nicht belegen konnte, sind vom Mac-CC
gemessen (§6): P8.1 war bereits geschlossen, vier waren offen. Auf Steward-Entscheid sind
**P5 (`21c9851`, 2026-08-02 08:43 UTC) und P10 (`3d95d04`, 08:46 UTC) vor dem Freeze
geschlossen** worden. P6 und C7 bleiben offen und gehen nach 0.4.1.
**Freigabe-Gegenstand ist `3d95d04`** — der letzte Commit mit Änderung an `site/**` oder
`gremium/**`. Alles darüber ist Rekordpflege. Wie G1 daran gebunden wird, steht im Gate-Status §9.

---

## 1 · Der Maßstab, nach dem eingestuft wird

Die Grundsatzregel des Warts, auf Befunde angewandt:

> Publiziert wird, was gültig ist; markiert wird, was fehlt. Nicht der Befund, der offen
> bleibt, ist der Bruch — der **unmarkiert** offene ist es.

Ein Befund darf offen bleiben, wenn er alle drei Bedingungen erfüllt:

1. Er **verfälscht den publizierten Rekord nicht** — weder heute noch durch bloßen Zeitablauf.
2. Er **tritt nicht von selbst ein.** Ein Fehler, den ein Cron am Montag früh auslöst, ist
   nicht „offen", sondern terminiert.
3. Er **steht hier namentlich**, mit Frist und Eigner.

Wo eine dieser Bedingungen nicht gilt, steht der Befund unter einer Frist — nicht unter „offen".

**Zwei Fristen, die nicht dieselben sind.** Der Go-Live ist nicht die einzige Schwelle. Am
**6. August läuft Sitzung 4** und schreibt in den unveränderlichen Rekord. Ein Befund, der die
Website nicht berührt, aber in den nächsten Rekord wandert, ist damit **dringender** als
mancher Frontend-Befund — nach dem 6. August ist er nicht mehr reparabel, nur noch markierbar.

---

## 2 · Geschlossen — zur Referenz, nicht Teil der offenen Liste

| Nr | Befund | Geschlossen durch |
|---|---|---|
| C2 | Modelltext als unbereinigtes HTML in Besucher-Browser | Sanitizing, `93e10ef` + `b1cad2f` — Gate-Zeile 6 |
| C3 / P1 | Formal misslungene Antwort wird als Sitzung publiziert; kein Inhalts-Gate vor Commit | Schema-Tore in beiden Workflows **vor** `git add`; markierter Bereichsausfall statt `continue` |
| C4 | Wart publiziert String `"false"` als Einberufung JA | `parse_wart_answer`: nur echtes JSON-Boolean, kein Prosa-Fallback, Parse vor dem Schreiben |
| C6 / P2 | „Konditional" aus Prosa geraten, trifft Negationen | Regex ersatzlos entfernt; strukturiertes Pflichtfeld ab Sitzung 4; Bestand grandfathered (Wart-Nachtrag 3) |
| B1 | Wart recherchiert gegen die überholte Sitzung 1 | Sortierschlüssel `(number, date)` + hartes Aktualitäts-Gate + öffentlicher Korrekturhinweis |
| P3 | Gleichstand still per Einfügereihenfolge entschieden | 2:2 ergibt `has_consensus: false` |
| — | Dubletten bei der höchsten Sitzungsnummer umgehen das Gate (Codex-Abnahme 1) | Dubletten-Gate vor dem Max-Vergleich |
| — | Schema erlaubte bei `conditional` nur Boolean → eine ungültige Stimme hätte die ganze Sitzung am Tor scheitern lassen (Codex-Abnahme 5) | `["boolean","null"]`; Ungültigkeit wird am Zählstand markiert, nicht am Rohvotum |
| — | Kein Test über den tatsächlich persistierten Rekord (Codex-Abnahme 6) | `test_full_record_path.py` — Vollpfad bis durchs Schema-Tor |
| — | Entscheid-Dokumente fehlten im Abnahme-Worktree (Codex-Abnahme 7) | vier Entscheide + `WART-NACHTRAEGE.md` in beide Worktrees |
| C1 | Deploy baut mit „inkompatibler" Node-Version | **Entkräftet, nicht repariert** — siehe P8.3. Die Inkompatibilitäts-Behauptung stammt aus meinem Review-Auftrag und war falsch; Kimi hat den Build unter 22.23.1 und 25.9.0 sauber durchlaufen lassen. |

---

## 3 · Offen unter Frist — vor Sitzung 4 (6. August)

Diese greifen in den unveränderlichen Rekord. Sie sind **kein** Go-Live-Blocker, aber sie haben
ein Datum.

| Nr | Befund | Warum offen bleiben darf | Warum die Frist gilt |
|---|---|---|---|
| **P4** | `dissent_md` enthält den rohen JSON-Votumblock, darin eine **modellbehauptete** `donation_url` (`helenkellerintl.org/donate/`), die nicht die kuratierte ist | Der Block steht in einem Code-Block, ist nicht klickbar, und nach dem Sanitizing bleibt er es. Kein Umgehen der Registry. Der Bestand ist unveränderlich — dort ist ohnehin nichts zu tun. | `extract_dissent` schreibt es bei **jeder** Sitzung erneut. Läuft Sitzung 4 ungeändert, steht es dreimal statt zweimal im Rekord und ist dann dauerhaft. Fix: Votumblock vor der Extraktion abstreifen — für künftige Läufe, nie rückwirkend. |
| **C5** | `session.yml` und `wart.yml` sind gegeneinander nicht serialisiert und schreiben beide `schedule.json` | Verschiedene Cron-Zeiten (Wart Mo 06:00 UTC, Sitzung 12:00 UTC) — sechs Stunden Abstand. Der zweite Push scheitert laut als non-fast-forward, publiziert also nichts Falsches. | Ab dem ersten Montag mit **beiden** Workflows an ist die Naht scharf. **Vorläufige Regel, bis serialisiert:** kein manueller Dispatch des einen, während der andere laufen kann. Das ist eine Verhaltensregel, kein Fix. |
| ~~P10~~ | ~~Zweiter Wart-Lauf am selben Tag löst falschen CI-Alarm aus~~ | **Geschlossen** durch `3d95d04`, vor dem Freeze. Der Restpunkt zum Leerlaufpfad ist geprüft und entkräftet (§6). | — |

---

## 4 · Offen ohne Frist — 0.4.1

Latente Befunde: sie treten erst bei einer Konstellation ein, die heute nicht vorliegt, und
verfälschen nichts, solange sie nicht eintritt.

| Nr | Befund | Warum das trägt |
|---|---|---|
| P7 | `run_wart.write_schedule()` baut `schedule.json` aus drei Schlüsseln neu statt zu mutieren — jedes künftige Feld wird still gelöscht | Die Datei hat heute genau diese drei Felder. Der Schaden entsteht **erst bei der ersten Erweiterung** — und die geht durch meine Hand. Bis dahin: keine Wirkung. `run_session.advance_schedule()` macht es bereits richtig und ist die Vorlage. |
| C7 | Vier Svelte-Compilerwarnungen im Build (`orgEn`, `passage` — nur initial erfasste Prop-Werte) | Der Build ist grün, die Tests bestehen. Die Warnung widerspricht der eigenen Definition „Build warnungsfrei" — das ist eine Doku-/Sauberkeitsfrage. Bei `passage` ist eine spätere Prop-Änderung nicht garantiert reaktiv; da heute nichts die Prop nachträglich ändert, ist es latent. **Offen, gemessen** — siehe §6. |
| P9 | `plain`/`plain_en` — die Klartext-Schicht, die ein Besucher **zuerst** liest — stehen weder im Schema noch im Datenvertrag | `additionalProperties: true`, also keine Vertragsverletzung, sondern Drift. Aber: die versiegelte Datennaht beruft sich auf diesen Vertrag. Ein Vertrag, der die prominenteste Schicht nicht kennt, beschreibt die Realität nicht. **Meine Empfehlung: mitnehmen, wenn der Freeze-Commit ohnehin angefasst wird** — es sind zwei Feldbeschreibungen und ein Absatz. |
| P8.3 | Briefing und `deploy.yml` widersprechen einander bei der Node-Version; `npm test` läuft im Deploy nicht | Der Widerspruch stammt aus **meiner** falschen Behauptung im Review-Auftrag (Rolldown-Bindings brächen unter anderer Version). Kimi hat sie empirisch entkräftet. Zu korrigieren ist die Dokumentation, nicht der Code. Das fehlende `npm test` im Deploy ist ein echter, aber kleiner Mangel: der Build-Schritt fängt das Grobe. |

---

## 5 · Offen bei anderen Eignern

| Nr | Befund | Eigner | Stand |
|---|---|---|---|
| P8.2 | `ssh-keyscan -H <ip> >> known_hosts` nimmt den Host-Key blind aus dem Netz — MITM auf dem Deploy-Pfad bei einem Projekt, dessen Produkt die Unverfälschbarkeit ist | **Afschin** | Das ist **Gate-Zeile 3**, `VPS_KNOWN_HOSTS`. Der einzige offene Befund, den ich als sicherheitsrelevant einstufe. Er ist bereits Gate-Bedingung — deshalb steht er nicht in §3 oder §4. |
| P8.1 | `deploy.yml` ist der einzige Workflow ohne Fehler-Issue-Step — ein Build-Bruch nach einem Bot-Push lässt die alte Site stehen und ruft niemanden | Leitstand → Mac-CC | **Geschlossen** durch `a25d1ee` (P1b-Nachzug), `deploy.yml:92–106`. Gemessen, siehe §6. |
| — | Keine Content-Security-Policy im Build | Leitstand | Gemeldet, nicht gebaut — so beauftragt. Steht als Punkt 1 in §8 des Gate-Status. |

---

## 6 · Fünf Befunde, gemessen — drei geschlossen, zwei nach 0.4.1

Diese fünf konnte ich vom Architektenplatz aus nicht belegen. Der Mac-CC hat sie auf
`integration/go-live-0.4` (`b0b14ca`) gemessen. Auf Steward-Entscheid wurden P5 und P10 danach
vor dem Freeze geschlossen — je ein Commit, einzeln zurückdrehbar.

| Nr | Stand | Beleg |
|---|---|---|
| **P5** | **geschlossen**, `21c9851` | `dissentTitle`: DE „Dissens und Vorbehalte", EN „Dissent and reservations" (`de.js:300`, `en.js:298`). Nur in `ArchiveRoom` verwendet, `id`/`aria-labelledby` unverändert, Test nachgezogen (`homepage-build.test.js:188/311`), 41/41. Auf beiden Archiv-Seiten gemessen: neue Überschrift 1×, alter String 0× |
| **P10** | **geschlossen**, `3d95d04` | `sys.exit(0)` mit sichtbarer Log-Zeile statt `sys.exit(<msg>)`; kein `\|\| true`, kein `continue-on-error`. `test_wart_idempotent_journal.py` trennt beide Fälle (vorhandenes Journal → Exit 0, kein `raw/`; leeres `sessions/` → Exit ≠ 0, Alarm bleibt). Gremium-Suite 48/48 |
| **P8.1** | **geschlossen**, `a25d1ee` | `deploy.yml:92–106` trägt den Fehler-Issue-Step (`if: failure()`, Label `ci-failure:deploy`) wie session/wart/preflight/canary; über den P1b-Nachzug jetzt in `integration` |
| **P6** | **offen → 0.4.1** | `.pult-label` linke Kante bei **x = −13** bei 390 px; `right:100%` + `width:max-content/15rem` (`ArchiveActors.svelte:224–231`). Der Mobil-Override (`max-width:1199px`, Z. 272) ändert nur `top`/`opacity`/`pointer-events`, **nicht** den horizontalen Anker |
| **C7** | **offen → 0.4.1** | vier Warnungen: `CouncilRoom.svelte:29` (`orgEn`) und `StageHero.svelte:38` (`passage`), je einmal im Client- und Server-Pass. Wortlaut: „This reference only captures the initial value of orgEn/passage." |

**Warum P6 und C7 liegen bleiben:** P6 ist messbar und unstrittig, aber eine Anker-Änderung am
Pult kurz vor dem Freeze ist eine Layout-Änderung, keine Textkorrektur — und der Fluss-Link zum
Protokoll existiert zusätzlich und trägt. C7 betrifft die eigene Definition „warnungsfrei", nicht
die Auslieferung.

### Zwei Punkte, die aus der Umsetzung entstanden sind

**1 · `noConsensus` trägt weiter die alte Wortwahl — richtig so.** Der Mac-CC hat den Schlüssel
gemeldet statt ihn mitzuändern, und das war die richtige Entscheidung. Er wird **bedingt pro
Bereich** gezeigt (`rec.hasConsensus ? name : noConsensus`) und ist damit eine **zutreffende
Zustandsaussage**, keine statische Behauptung über den Rekord. Auf `/archiv/` rendert er bei
Sitzung 3 gar nicht (Vollkonsens, 0×). P5 war der Fehler, weil eine **unbedingte** Überschrift
einen Zustand behauptete. Hier ist die Bedingung genau der Unterschied. **Kein Befund, kein
Nachfassen** — es steht hier, damit es niemand später als übersehen aufmacht.

**2 · Ein Restpunkt zu P10 — geprüft, entkräftet.** Mein Einwand: Der No-op-Lauf endet jetzt mit
Exit 0, die Folgeschritte laufen also weiter bis zum `git commit`, und der endet ohne Änderungen
mit Exit 1 — wieder `if: failure()`.

**Gemessen: der Pfad tritt nicht auf.** `wart.yml:50–52` fängt ihn ab
(`if git diff --staged --quiet; then echo "Keine Änderungen."; exit 0; fi`). Zusammen mit dem
P10-Fix, der schon vorher mit Exit 0 aussteigt, gibt es keinen Leerlauf mit Exit 1.
**Kein offener Punkt** — weder für G1 noch für das Einschalten von `wart.yml`.

---

## 7 · Geschmack — Entscheidungen des Stewards, keine Mängel

Zehn Beobachtungen Kimis und eine Frage von Codex. Keine davon ist ein Defekt; jede ist eine
Entscheidung, die getroffen oder bewusst nicht getroffen werden kann. Meine Empfehlung dahinter,
knapp.

| Nr | Beobachtung | Mein Rat |
|---|---|---|
| G1 | Dieselbe Figur heißt „The Scout", „Der Späher", „Der Scout"; ebenso „The Warden" / „der Wart" | Eine Zeile Glossar oder eine Schreibweise. Wirkt sonst wie zwei Akteure zu viel. **0.4.1** |
| G2 | „Der Council tagt nicht nach Kalender" (`/idee/`) vs. „Laut Terminplan: 6. August" | Der Rhythmus **ist** kalenderisch mit anlassbezogener Vorverlegung. Der Satz verspricht mehr Anlassbezug, als das System hat. Ein Halbsatz korrigiert ihn. **Mitnehmen** |
| G3 | „die Kosten des Laufs in Euro, auf den Cent" — gerechnet mit festem fx und Listenpreisen | „auf den Cent" verspricht Abrechnungsgenauigkeit, die niemand prüfen kann. „nach Listenpreis" wäre exakt. **Mitnehmen** |
| G4 | EN „Last: not convened · July 27" liest sich, als sei der Scout nicht einberufen worden | „no session convened". **Mitnehmen**, ein String |
| G5 | Deutsche Räume mit englischen Seitentiteln | Absicht? Steward. **0.4.1** |
| **G6** | **Keine og:/twitter:-Meta-Tags, keine robots.txt, keine sitemap** | **Hebe ich aus dem Geschmack heraus.** Das Projekt lebt vom Geteilt-Werden; der erste Eindruck in Messengern und Suche ist derzeit ungestaltet. Kein Rekordbezug, billig zu bauen. **Steward-Entscheid: mitnehmen oder 0.4.1** |
| G7 | Spendenlinks „(extern) ↗" öffnen im selben Tab | Der Pfeil verspricht neuen Kontext. Bei mehrstufigen Formularen (AMF) ist der Rückweg holprig. **Mitnehmen**, ein Attribut |
| G8 | Referenz-Set: zwei Dubletten (`tafel-ruhe-1440` ≡ `study-1440`, `archive-1440` ≡ `pult-ruhe-1440`, md5-identisch) | Zwei benannte Zustände der 18er-Liste sind keine eigenen Aufnahmen. Betrifft die Beweislage künftiger Reviews. **Mit dem Abschluss-Durchgang neu aufnehmen** |
| G9 | „kein Modell steuert den Prozess" — `convene` ist Modell-Output und steuert den Terminplan | „… die Zählung" macht den Satz exakt. **Mitnehmen** |
| G10 | Das Zählwerk zeigt „3 von 3" ohne Konditional-Hinweis an der Plakette; die Reservation liegt eine Ebene tiefer | An der sichtbarsten Stelle des Demut-Kanons wird die Unsicherheit weggeglättet. Inhaltlich der stärkste der zehn. **Steward-Entscheid** |
| C9 | Zentrale Handlungslinks in Ruhe sehr dunkel; „Vollständiges Protokoll öffnen" schwächer als dekorative Goldakzente | Codex' Frage ist die richtige: **soll** die zentrale Handlung erst beim Erkunden lesbar werden? Falls ja, ist es kein Befund. Falls nein, nur die Ruhe-Luminanz anheben — **nicht** Bildsprache oder Dunkelheit neu verhandeln. **Steward-Entscheid** |
| C8 | Mobil (390) trägt der erste Screen Frage, Szene und Prozess-Röhre; die Ergebnis-Tafel folgt unmittelbar danach | Kimi hat es unabhängig geprüft: Desktop bestanden, mobil „findbar, aber nicht im ersten Blick". Das ist eine Inszenierungsentscheidung — die Bühne **soll** vor dem Ergebnis stehen. **Steward-Entscheid**, kein Mangel |

---

## 8 · Was nicht geprüft wurde — und deshalb auch nicht als geprüft gilt

Beide Prüfer haben ihre Grenzen benannt. Zusammengezogen, weil ein Bereitschaftsbericht auch
sagen muss, wo er blind ist:

- **Kein realer Lauf.** Weder Sitzung noch Wart wurden ausgeführt (kostenpflichtig, rekordschreibend).
  Ob Opus/GPT/Gemini am 6. August den neuen Prompt vertragskonform beantworten, ist **statisch
  nicht beweisbar**. Der Vertragsbruch-Mechanismus ist genau dafür gebaut — er ist die Antwort auf
  diese Lücke, nicht ihre Schließung.
- **Kein Produktions-Deploy-Durchlauf.** Der erste Push auf `master` ist der erste echte Test des
  Deploy-Pfads. Deshalb Gate-Zeile 3 und deshalb der Preflight.
- **Kein Screenreader-Durchgang, keine flächendeckende Kontrastmessung.** Nur statisch geprüft:
  aria-Muster, `lang`-Attribute, DOM-Reihenfolge; Kontrast an Stichproben (Ergebnis: weit über
  WCAG AA auf dem nahezu schwarzen Scrim).
- **Kein Pixel-Diff gegen die Referenzen** — beide Prüfer ohne Headless-Browser im Sandbox-Netz.
  Struktureller Abgleich und Sichtung stattdessen.
- **Token-Kosten nicht gegen die Provider-Abrechnung geprüft** — nachgerechnet ist nur die
  interne Konsistenz (Token × Listenpreis × fx). Siehe G3.
- **Das Archiv mit 50 Sitzungen** nur statisch beurteilt, nicht gerendert.

---

## 9 · Der Satz, auf den es hinausläuft

**Kein offener Befund verfälscht die Rekord-Daten, und keiner tritt durch bloßen Zeitablauf vor
dem 6. August ein.** Der sicherheitsrelevanteste ist bereits Gate-Bedingung (Zeile 3, das
Host-Key-Pinning). Die drei mit Datum stehen in §3, ihre Frist liegt **nach** dem Go-Live.

**Die eine Stelle, an der die Fassung sich selbst widersprach, ist geschlossen.** P5 verfälschte
keine Daten, behauptete aber auf der Seite etwas Falsches über den Rekord — „Noch keine
Einigkeit" über vier Konsens-Empfehlungen. Zwei Strings, `21c9851`.

Aus Sicht der NobleCause-Session ist Zeile 5 vollständig und im Rekord belegt (`b3a51e3`); G1 ist
aus unserem Teil nicht mehr blockiert.
