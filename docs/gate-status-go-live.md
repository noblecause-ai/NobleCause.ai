# Gate-Status Go-Live noblecause.ai — die eine Wahrheit

**Zweck:** Der einzige Ort, an dem steht, was gerade **wahr** ist. Das Schnittstellenpapier regelt,
wer was tut; dieses Dokument sagt, was davon erledigt ist.
**Regel:** Wer eine Zeile ändert, trägt sie hier ein, mit Beleg und Zeitstempel. Wer eine Zeile
liest, verlässt sich darauf und misst nicht selbst nach.
**Letzte Pflege:** 2026-08-02, 09:25 UTC, NobleCause-Session (Architekt)

> **Zeitstempel-Korrektur.** Frühere Fassungen dieses Dokuments trugen für die Einträge der
> NobleCause-Session Zeiten des 1. August (20:30 / 21:15 / 22:00 UTC). Sie waren falsch: die Uhr
> der Architekten-Umgebung ging rund 12,5 Stunden nach. Die betroffenen Einträge sind unten auf
> die **belegten** Zeiten gesetzt — Commit-Zeiten aus `git log`, nicht aus einer Erinnerung.

---

## 1 · Warum es dieses Dokument gibt

Bis heute liefen alle Release-Läufe mit **einem** Akteur: ein Repo, eine Sitzung, eine Maschine. Die
Checkliste des Piloten war dafür gebaut. Dieser Lauf hat **vier** Akteure auf **zwei** Maschinen:
Leitstand, NobleCause-Session, Mac-CC, VPS-CC.

Damit entstand ein Zustand, den es vorher nicht geben konnte: Ergebnisse existieren, aber nicht
dort, wo der nächste Akteur sie sieht. Der Mac-CC musste den Gate-Zustand aus einem Shell-Befehl
rekonstruieren und lag bei einer Zeile daneben, weil der Bericht des VPS-CC ihn nie erreicht hat.
Das war kein Fehler des Mac-CC, sondern eine fehlende Ablage.

Dieses Dokument ist die Ablage. Es ersetzt kein Verfahren, es hält den Zustand.

---

## 2 · Die sieben Bedingungen

| # | Bedingung | Eigner | Stand | Beleg |
|---|---|---|---|---|
| 1 | Härtung auf `origin/master` | NobleCause-Session | **erfüllt** | `d4fcc3c`, in der Historie von `a25d1ee` |
| 2 | P1b `deploy.yml`-Härtung auf `master` | Leitstand → Mac-CC | **erfüllt** | `origin/master` = `a25d1ee` |
| 3 | `VPS_KNOWN_HOSTS` als Repo-Secret | **Afschin** | **offen** | `gh secret list`: fehlt |
| 4 | Caddy Stufe 2a gesetzt und gemessen | Leitstand → VPS-CC | **erfüllt** | Bericht VPS-CC 15:15 UTC, sechs Messzeilen |
| 5 | Bereitschaftsbericht inkl. Punkt 8 Umzugstabelle | NobleCause-Session | **erfüllt** | Docs im Rekord, `b3a51e3` (5a Umzugstabelle, 5b Inventare, 5c Befundliste) — siehe §3 und §11 |
| 6 | Sanitizing-Blocker geschlossen | NobleCause-Session | **erfüllt** | `93e10ef` (Sanitizing) + `b1cad2f` (§7-Durchgang), per FF-Merge in `integration/go-live-0.4`; Kopf `b0b14ca` |
| 7 | G1 durch den Leitstand | Leitstand | **offen**, **nicht mehr blockiert** | entscheidbar; siehe §9 |

Ausgangszustand der Workflows, bestätigt: `deploy.yml` und `wart.yml` beide `disabled_manually`.
`wart.yml` wird auf Afschins direktes Wort in der CC-Sitzung eingeschaltet, unabhängig von diesem
Gate.

**Gemessene Stände, mit `git fetch` in derselben Befehlskette (Mac-CC):** `origin/master` =
`a25d1ee` · `integration/go-live-0.4` trägt `93e10ef` (2026-08-01 15:50 UTC, Sanitizing) und
`b1cad2f` (19:28 UTC, §7-Durchgang) in der Historie. Kopf zu diesem Zeitpunkt `b0b14ca`
(20:14 UTC), inzwischen `3d95d04` — siehe §9.

**Zeile 7 im Klartext:** G1 ist entscheidbar. Der **scharfe Deploy** braucht zusätzlich Zeile 3 —
G1 und Deploy-Freigabe sind nicht dasselbe Ereignis.

---

## 3 · Zeile 5 aufgeschlüsselt — was vorliegt und was fehlt

Zeile 5 war als ein Block geführt und ist in Wahrheit dreiteilig. Aufgeschlüsselt, damit der
Leitstand nicht auf ein Ganzes wartet, dessen entsperrender Teil längst dasteht:

| Teil | Inhalt | Stand |
|---|---|---|
| 5a | **Umzugstabelle (Punkt 8)** — Routen alt → neu, 301-Regel, Trailing-Slash- und Fragment-Verhalten, Verifikationszeilen | **im Rekord**, `b3a51e3`: `docs/bereitschaft-punkt8-umzugstabelle-2026-08-01.md` |
| 5b | **Inventare und Kennzahlen** — Routen-Inventar, Asset-/AVIF-Pfade, Chunk-Erwartung für die Karenz, Commit-Hash | liegt vor bzw. fällt mit dem Freeze-Commit an |
| 5c | **Liste der bewusst offen bleibenden Review-Befunde, mit Einstufung** | **im Rekord**, `b3a51e3`: `docs/bereitschaft-punkt4-befundliste-2026-08-01.md` — 30 Befunde, 14 geschlossen, 16 offen mit Frist und Eigner |

**Für den Leitstand heißt das:** 5a ist der Teil, der **2b und das 301-Fragment entsperrt**. Er ist
fertig und braucht 5c nicht abzuwarten. 5c ist eine Bewertungsliste, keine Codeänderung — sie ist
Voraussetzung für G1, nicht für das Fragment.

**Eine Lücke in 5a, die dem VPS-CC gehört und nicht mir:** Die Tabelle beruht auf den internen Links
der Startseite, nicht auf einem Verzeichnis des ausgelieferten Standes. Der Abgleich steht in §6 der
Tabelle mit dem fertigen Befehl. Er gehört **vor** das Schreiben des 301-Fragments.

**Doppelarbeit, die vermieden gehört:** Der Mac-CC hat 5a in seiner letzten Rückfrage als eigene
offene Baustelle geführt. Sie ist keine — das Dokument liegt seit `b3a51e3` im Rekord. Er baut, ich schreibe.

---

## 4 · Zeile 3 im Klartext

Das Secret fehlt real, und zwar seit dem Push von P1b. Der Workflow auf `master` verweist damit auf
ein Secret, das es nicht gibt. Das ist folgenlos, solange `deploy.yml` aus ist, und bricht beim
ersten scharfen Lauf laut ab. Genau so ist der Preflight gebaut.

Es ist trotzdem der Fehler dieses Laufs: die Anleitung stand im P1b-Auftrag, der Push ging durch,
und danach hat niemand geprüft, ob der zweite Teil auch passiert ist. Eine Änderung wurde
veröffentlicht, deren Voraussetzung offen blieb.

Die vier Schritte für Afschin stehen im P1b-Auftrag, Abschnitt 3: Fingerprint über den Admin-Zugang
an der Quelle lesen, `ssh-keyscan` erzeugen, beide vergleichen, nur bei Übereinstimmung setzen.

---

## 5 · Zeile 6 im Klartext — was geschlossen wurde

Der Befund kam unabhängig von Codex und Kimi: `marked.parse` ließ eingebettetes HTML stehen, das
Ergebnis ging per `{@html}` in die Seite. Die Quelle war als „trusted build-time content"
kommentiert — sie besteht aber aus Modellantworten und Web-Recherche des Warts. Codex' Satz dazu
trifft es: **build-time macht eine Quelle unveränderlich, nicht vertrauenswürdig.**

Geschlossen mit einem zentralen Erzeuger in `site/src/lib/server/content.js`: alle zwölf
`{@html}`-Senken laufen über `md()` bzw. `manifestHtml()`, `marked` wird nirgends sonst mehr
importiert. Roh-HTML wird escapt statt entfernt, `javascript:`/`vbscript:`/`data:` greifen weder in
Links noch in Bildquellen, Links tragen `rel="nofollow noopener noreferrer ugc"`.

**Die Randbedingung, die über der Reparatur stand, ist eingehalten:** der Wortlaut bleibt
vollständig und unverändert. Es wurde nichts gekürzt — ein Sanitizer, der still entfernt, verletzt
die Datennaht so wie eine Paraphrase.

**Was dabei nicht gebaut wurde und dem Leitstand gehört:** siehe §8, Punkt 1.

---

## 6 · Der aktuelle Caddy-Block nach Stufe 2a

Der Stufe-1-Bericht des Mac-CC enthält den Block im Stand **vor** 2a. Wer daraus 2b ableitet, baut
auf einem überholten Stand. Der Stand nach 2a, aus dem Diff des VPS-CC-Berichts:

```caddy
noblecause.ai, www.noblecause.ai {
    root * /srv/noblecause
    file_server
    encode zstd gzip

    # --- Klasse A: gehashte Build-Dateien -> ein Jahr, immutable ---
    @immutable path /_app/immutable/*
    header @immutable Cache-Control "public, max-age=31536000, immutable"

    # --- Klasse B: HTML -> kurz, revalidierend ---
    @html path / */ *.html
    header @html Cache-Control "public, max-age=300, must-revalidate"

    # --- Klasse C: ungehashte Medien und Schriften ---
    @media {
        not path /_app/immutable/*
        path *.avif *.webp *.png *.jpg *.jpeg *.svg *.woff2 *.woff *.css *.js *.json
    }
    header @media Cache-Control "public, max-age=3600, must-revalidate"

    header {
        X-Content-Type-Options nosniff
        Referrer-Policy strict-origin-when-cross-origin
        Permissions-Policy "interest-cohort=()"
        -Server
    }

    log { … unverändert … }
}
```

**Einrückung: Tabs, nicht vier Leerzeichen.** Die Datei war vor der Änderung `caddy fmt`-konform und
ist es geblieben. Jedes Fragment für 2b muss Tabs verwenden, sonst schlägt die Formatprüfung an und
verleitet zu einem schreibenden `caddy fmt`, das fremde Blöcke anfassen würde.

**Gemessen nach 2a (VPS-CC, 15:15 UTC):** `/` und Unterseiten `max-age=300, must-revalidate`
(Unterseiten hatten vorher **keinen** Header) · `/_app/immutable/*` `31536000, immutable` ·
`favicon.svg` `3600, must-revalidate` (vorher fälschlich immutable) · `/gibt-es-nicht/` 404 mit
`max-age=300` · aion-lumen.ch und mirhamed.ch unverändert.

**Harmlose Gegenprobe**, falls jemand diesen Stand selbst bestätigen will: ein Abruf von
`/journal/`. Trägt er `cache-control: public, max-age=300, must-revalidate`, ist 2a gesetzt; fehlt
der Header, ist er es nicht.

---

## 7 · Was als Nächstes geschieht, je Eigner

**NobleCause-Session (Architekt):** 5c liegt vor. Zeile 5 ist voll. Offen ist nur noch der
Steward-Entscheid aus §9.

**Mac-CC:** der Abschluss-Durchgang mit Belegen (Türfahrten beide Richtungen, Rückwärts-Stabilität
ohne Neuladen, 390 px, `prefers-reduced-motion`, ohne JS, Protokoll-Eingang in allen Zuständen,
Überlagerungsprüfung über den gesamten Scrollweg). **Nicht** die Umzugstabelle — die liegt vor.

**Afschin:** Zeile 3, das Secret. Und das direkte Wort für `wart.yml` in der CC-Sitzung.
Zusätzlich: die Abnahme des §8-Zähl-Rucks, sobald der Mac-CC die Stelle benennt.

**Leitstand:** 2b-Prompt für den VPS-CC — **kann jetzt**, 5a liegt vor. Das 301-Fragment ebenfalls,
mit der EN-Präzisierung aus §8 Punkt 2 und nach dem Verzeichnis-Abgleich aus §6 der Umzugstabelle.
Danach G1, sobald 5c steht.

---

## 8 · Rückmeldung der NobleCause-Session an den Leitstand

Vier Punkte, die nicht in eine Gate-Zeile passen, aber in seiner Zuständigkeit liegen oder seine
Entscheidung brauchen.

**1 · Der Build trägt keine Content-Security-Policy.** Gemeldet, nicht gebaut — so war es
beauftragt, weil eine CSP ein Auslieferungsparameter ist und in die Caddy-Konfiguration gehört, die
der Leitstand mit der infra-reorg-Session abstimmt. Nach dem Sanitizing ist die Injektionslücke an
der Quelle geschlossen; die CSP wäre die zweite Schicht, nicht die erste. **Kein Go-Live-Blocker aus
unserer Sicht — aber eine bewusste Entscheidung des Leitstands, nicht ein Versehen.** Wenn sie mit
2b kommen soll, ist jetzt der Moment; ein Nachrüsten nach dem Deploy ist ein reiner
Header-Zusatz und jederzeit möglich.

**2 · Präzisierung zum 301-Fragment, EN-Zweig.** Der englische Zweig hat **nur** die drei
Raum-Landings (`/en/`, `/en/council/`, `/en/archive/`). Es gibt **keine** `/en/sitzungen/…` und
keine englischen Rekord-Routen. **Dort also keine 301-Regel setzen** — eine Regel auf `/en/*` würde
ins Leere zielen und im schlechteren Fall die drei Landings fangen. Die Umzugsregel bleibt genau
eine: `/sessions/*` → `/sitzungen/*`, Pfadrest unverändert, beide Slash-Formen, Fragmente unberührt.

**3 · Der Pult-Überlappungsbefund ist entschieden, nicht offen.** Das feste Bühnenelement im Archiv
(`z-index: 4`) überlagert im Scrollverlauf stellenweise den Fluss. Der Befund liegt vor, der Steward
hat entschieden, es zu belassen. Es steht hier, damit es niemand als übersehenen Mangel neu
aufmacht. Die Prüfung über den gesamten Scrollweg läuft trotzdem im Abschluss-Durchgang mit.

**4 · Die Live-Seite zeigt seit Wochen falsche Termine.** Der ausgelieferte Stand ist der Build vom
14. Juli. Er zeigt „Nächster Research in 5 T 14 h (20.7.2026)" — ein Datum, das zwölf Tage in der
Vergangenheit liegt — und „Nächste Sitzung 8.8." statt korrekt 6.8. Bei einem Projekt, dessen
Produkt die Nachprüfbarkeit ist, ist eine falsche Terminanzeige der teuerste sichtbare Fehler.
**Das ist kein neuer Arbeitsauftrag — der Deploy behebt es.** Es ist das Argument dafür, das Gate
nicht länger zu dehnen als nötig, und der Grund, warum 5c heute kommt und nicht morgen.

---

## 9 · Der Freeze-Commit-Kandidat

Von 30 Review-Befunden sind **14 geschlossen**. Fünf, deren Stand aus der Architektensicht nicht
belegbar war, hat der Mac-CC auf `b0b14ca` gemessen; auf Steward-Entscheid wurden zwei davon vor
dem Freeze geschlossen.

| Nr | Stand | Kern |
|---|---|---|
| P5 | **geschlossen**, `21c9851` | Archiv-Überschrift behauptet keinen Rekordstand mehr: DE „Dissens und Vorbehalte", EN „Dissent and reservations". `id`/`aria-labelledby` unverändert, Test nachgezogen, 41/41 |
| P10 | **geschlossen**, `3d95d04` | Vorhandenes Tagesjournal ist kein CI-Fehler mehr: `sys.exit(0)` mit sichtbarer Log-Zeile, kein `\|\| true`, kein `continue-on-error`. Test trennt beide Fälle, Gremium-Suite 48/48 |
| P8.1 | **geschlossen**, `a25d1ee` | `deploy.yml` hat den Fehler-Issue-Step |
| P6 | offen → 0.4.1 | `.pult-label` bei 390 px, linke Kante bei **x = −13** — der Protokoll-Eingang ist auf Mobil angeschnitten |
| C7 | offen → 0.4.1 | vier Svelte-Compilerwarnungen (`orgEn`, `passage`), Build grün |

**Freeze-Commit-Kandidat: `3d95d04`** (`3d95d0494dd48123111445cf9570765178fba09d`), Kopf
`integration/go-live-0.4`.

**Ein Vorbehalt zu P10, geprüft und entkräftet.** Ich hatte eingewandt: Die Reparatur lässt den
Wart-Lauf im No-op-Fall mit Exit 0 durchlaufen; vorher brach er ab und die Folgeschritte liefen
gar nicht, jetzt laufen sie — inklusive `git commit`, der ohne Änderungen mit Exit 1 endet und
wieder auf `if: failure()` träfe.

**Der Pfad tritt nicht auf.** `wart.yml:50–52` fängt den Fall bereits ab:
`if git diff --staged --quiet; then echo "Keine Änderungen."; exit 0; fi`. Zusammen mit dem
P10-Fix, der schon vorher mit Exit 0 aussteigt, gibt es keinen Leerlauf mit Exit 1. Der Einwand
war berechtigt zu stellen und ist erledigt — **keine Bedingung für das Einschalten von
`wart.yml`, keine für G1.**

**Zum Hash, an den G1 gebunden wird — Korrektur meiner eigenen Empfehlung.** Ich hatte
`4e5fb00` genannt, weil unter diesem Kopf die Bereitschaftsdokumente auffindbar sind. Das war
halb gedacht, und der Mac-CC hat sofort darauf gezeigt: Jeder weitere Dokumenten-Commit
verschiebt den Kopf. Eine Empfehlung, die einen Hash nennt, kann nie unter dem Hash liegen, den
sie nennt. So jagt man dem eigenen Schwanz nach.

**Die Regel, die nicht rekursiv ist — G1 nennt zwei Hashes, nicht einen:**

| | |
|---|---|
| **Freigabe-Gegenstand** | `3d95d04` — der letzte Commit, der `site/**` oder `gremium/**` berührt. Er bestimmt das ausgelieferte Artefakt. Alles darüber ist Rekordpflege. |
| **Dokumentenstand bei Freigabe** | der Kopf von `integration/go-live-0.4`, wie der Leitstand ihn **im Moment der Freigabe misst** und hier einträgt. |

Damit muss kein Dokument vorher wissen, wie es selbst heißen wird, und der Leitstand kann G1
geben, ohne auf einen Stillstand der Dokumentation zu warten.

Einstufung, Frist und Eigner aller 16 offenen Befunde:
`docs/bereitschaft-punkt4-befundliste-2026-08-01.md`.

---

## 10 · Änderungsprotokoll

| Zeitpunkt (UTC) | Zeile | Von | Änderung |
|---|---|---|---|
| 2026-08-01 ~12:20 | 1 | NobleCause-Session | erfüllt, `d4fcc3c` |
| 2026-08-01 ~14:00 | 2 | Mac-CC | erfüllt, `a25d1ee` |
| 2026-08-01 15:15 | 4 | VPS-CC | erfüllt, sechs Messzeilen |
| 2026-08-01 15:50 | — | Mac-CC | Sanitizing-Fix `93e10ef` (Commit-Zeit aus `git log`) |
| 2026-08-01 16:00 | — | Leitstand | Dokument angelegt |
| 2026-08-01 19:28 | — | Mac-CC | §7-Durchgang `b1cad2f` |
| 2026-08-01 20:14 | 6 | Mac-CC | erfüllt; Kopf `integration/go-live-0.4` = `b0b14ca` |
| 2026-08-02 08:43 | — | Mac-CC | P5 geschlossen, `21c9851` |
| 2026-08-02 08:46 | — | Mac-CC | P10 geschlossen, `3d95d04` — Freeze-Commit-Kandidat |
| 2026-08-02 09:00 | 5 | Architekt | **offen → erfüllt**; in 5a/5b/5c aufgeschlüsselt (§3). 5c liegt vor: `docs/bereitschaft-punkt4-befundliste-2026-08-01.md` |
| 2026-08-02 09:00 | 7 | Architekt | **blockiert → nicht mehr blockiert**, entscheidbar. Der scharfe Deploy braucht zusätzlich Zeile 3 |
| 2026-08-02 09:25 | — | Architekt | §9: G1-Hash-Empfehlung korrigiert — zwei Hashes (Freigabe-Gegenstand `3d95d04`, Dokumentenstand vom Leitstand bei Freigabe) statt eines rekursiven. Hinweis Mac-CC |
| 2026-08-02 09:20 | — | Architekt | §9: P10-Vorbehalt entkräftet (`wart.yml:50–52` fängt den Leerlauf ab, Beleg Mac-CC); Empfehlung, G1 an `4e5fb00` zu binden |
| 2026-08-02 09:00 | — | Architekt | §5, §8 und §9 ergänzt; §7 je Eigner nachgeführt; Zeitstempel früherer Architekten-Einträge korrigiert (Uhrfehler, siehe Kopf) |
| 2026-08-02 09:10 | 5 | Mac-CC | Docs (Gate-Status, 5a, 5c) in den Rekord: `b3a51e3` |
| 2026-08-02 09:10 | 5 | Mac-CC | Zeile-5-Beleg gesetzt — Platzhalter „Beleg folgt mit dem Commit" → `b3a51e3` |

**Zu den drei Architekten-Einträgen:** Sie entstanden in drei Schritten, aber **wirksam werden
sie mit diesem einen Commit** — die Zwischenfassungen sind nie in den Baum gelangt (siehe §11).
Deshalb steht hier ein Zeitpunkt und nicht drei.

---

## 11 · Zwei Ablage-Pannen, und warum Zeile 5 bis zum Commit unbelegt war

Beim Versuch, dieses Dokument selbst abzulegen, sind zwei Fehler aufgefallen. Beide gehen auf die
NobleCause-Session, keiner auf den Mac-CC — er hat in beiden Fällen korrekt gemeldet, was er
vorfand, statt zu raten.

**Erstens: der Namenskonflikt.** Der Weg war Architekt → Auslieferung → Download durch den
Steward → Handablage in `docs/`. Beim Download kollidierte der Name, das System hängte `_1` an.
Im Verzeichnis lagen danach `gate-status-go-live.md` (die 16:00-Fassung, unverändert) und
`gate-status-go-live_1.md` (die neue Fassung, unbeachtet). Der Mac-CC suchte den richtigen Namen
und fand die alte Datei — genau richtig.

**Zweitens, und das ist der schwerere:** Die Handablage ging in den **Hauptbaum**
`Projects/NobleCause.ai`. Der steht auf `master`, und dort ist `docs/` **überhaupt nicht
getrackt** (0 Dateien). `integration/go-live-0.4` ist in einem separaten Worktree ausgecheckt
(`Projects/nc-sanitize`). Ergebnis, mit `git log --all` belegt:

> **Weder die Umzugstabelle (5a) noch die Befundliste (5c) lagen in irgendeinem Commit.**

Beide existierten nur als ungetrackte Dateien in einem Arbeitsverzeichnis. Ich habe Zeile 5 auf
„erfüllt" gesetzt, weil ich die Dateien *sah* — und dabei „liegt vor" mit „liegt im Rekord"
gleichgesetzt. Das ist derselbe Fehler, den dieses Dokument bei anderen verhindern soll: eine
Zeile, auf die sich der nächste Akteur verlässt, ohne dass ihr Beleg existiert. Hätte der
Leitstand G1 darauf gestützt, hätte er auf ein Dokument verwiesen, das im Repo nicht auffindbar
ist.

**Behoben:** Alle drei Dokumente liegen jetzt in `nc-sanitize/docs/`, also im Arbeitsbaum von
`integration/go-live-0.4`. Zeile 5 trägt bis zum Commit den Stand „inhaltlich erfüllt, Beleg
folgt" und wird mit dem Commit-Hash nachgezogen.

**Drei Regeln daraus:**

1. Der Architekt legt Dokumente **selbst** ab, unter dem Zielnamen, **im Worktree des
   Zielzweigs** — nicht im Hauptbaum, nicht über Download und Handablage.
2. „Liegt vor" ist kein Beleg. Ein Gate-Beleg ist ein **Commit-Hash** oder eine Messung, nie eine
   Datei im Arbeitsverzeichnis.
3. Wer eine Datei in `docs/` erwartet, prüft mit `git log --all -- <pfad>`, nicht mit `ls`.

**Aufgeräumt:** `gate-status-go-live_1.md` und die beiden Fehlablagen im Hauptbaum liegen unter
`NobleCause.ai/docs/_to_delete/`. Sie können gelöscht werden.
