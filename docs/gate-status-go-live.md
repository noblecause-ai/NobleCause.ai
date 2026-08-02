# Gate-Status Go-Live noblecause.ai — die eine Wahrheit

**Zweck:** Der einzige Ort, an dem steht, was gerade **wahr** ist. Das Schnittstellenpapier regelt,
wer was tut; dieses Dokument sagt, was davon erledigt ist.
**Regel:** Wer eine Zeile ändert, trägt sie hier ein, mit Beleg und Zeitstempel. Wer eine Zeile
liest, verlässt sich darauf und misst nicht selbst nach.
**Letzte Pflege:** 2026-08-02, 11:00 UTC, NobleCause-Session (Architekt)

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
| 3 | `VPS_KNOWN_HOSTS` als Repo-Secret | **Afschin** | **erfüllt** | 2026-08-02 ~10:40 UTC, drei Fingerprints an der Quelle gegen Keyscan geprüft, `gh secret list` bestätigt — `verfahren-host-key-pinning-2026-08-02.md` |
| 4 | Caddy Stufe 2a gesetzt und gemessen | Leitstand → VPS-CC | **erfüllt** | Bericht VPS-CC 15:15 UTC, sechs Messzeilen |
| 5 | Bereitschaftsbericht inkl. Punkt 8 Umzugstabelle | NobleCause-Session | **erfüllt** | Docs im Rekord, `b3a51e3` (5a Umzugstabelle, 5b Inventare, 5c Befundliste) — siehe §3 und §11 |
| 6 | Sanitizing-Blocker geschlossen | NobleCause-Session | **erfüllt** | `93e10ef` (Sanitizing) + `b1cad2f` (§7-Durchgang), per FF-Merge in `integration/go-live-0.4`; Kopf `b0b14ca` |
| 7 | G1 durch den Leitstand | Leitstand | **erteilt** | 2026-08-02, `g1-freigabe-leitstand-2026-08-02.md`. Gegenstand `3d95d04`, Dokumentenstand `b54fa0c` |
| **8** | **Abschluss-Durchgang mit Belegen** | **Mac-CC** | **offen** | Bereitschaftsbericht Punkt 2 (Schnittstellenpapier §5) — siehe Hinweis unten |

**Zeile 8 ist neu und war eine Lücke.** Der Abschluss-Durchgang stand als Punkt 2 des
Bereitschaftsberichts im Schnittstellenpapier §5. Bei der Aufschlüsselung von Zeile 5 in 5a/5b/5c
ist er herausgefallen: 5a ist die Umzugstabelle, 5c die Befundliste, 5b sind Inventare. Der
Durchgang selbst kam in keinem der drei vor, stand aber weiter in §7 als offene Arbeit des Mac-CC.
Damit war er weder erledigt noch von einer Gate-Zeile gehalten. Er bekommt deshalb eine eigene
Zeile, statt sich auf eine Formulierung zu berufen.

**`wart.yml` ist seit 2026-08-02 aktiv** (Workflow 308959603), nächster Lauf **Montag,
4. August, 06:00 UTC**. `deploy.yml` bleibt `disabled_manually`. Erfolgskriterium für Montag,
vorab notiert: ein Journal-Eintrag mit `session_ref` → **Sitzung 3** (der Fix wirkt), **oder** ein
lauter Abbruch mit Issue und ohne Eintrag (der Vertragsbruch-Mechanismus wirkt). Versagen wäre
ein Eintrag mit falschem `session_ref` — oder nichts, ohne Issue.

**Ein Versatz, der ab jetzt zählt: die Maschine läuft aus `master`, die Arbeit liegt auf
`integration/go-live-0.4`.** `wart.yml` und `session.yml` checken `master` aus. Alles, was auf dem
Integrationszweig repariert wurde und die Maschine betrifft, wirkt erst mit dem Go-Live-Merge.
Konkret heute: der **P10-Fix** liegt auf `integration`, nicht auf `master` — für Montag folgenlos
(der Pfad greift nur bei einem zweiten Lauf am selben Tag), aber ein manueller Re-Run am Montag
träfe noch den alten Fehlalarm. Vom Mac-CC gemessen und gemeldet.

**Daraus folgt eine Regel für alles Weitere:** Wer eine Änderung an `gremium/**` vor einem
Maschinenlauf wirksam haben will, muss sie **auf `master`** haben — nicht auf `integration`. Das
gilt für den nächsten Fall unmittelbar: **P4 vor Sitzung 4 am 6. August** (siehe §12).

Ausgangszustand der Workflows zu Beginn dieses Laufs: `deploy.yml` und `wart.yml` beide `disabled_manually`.
`wart.yml` wird auf Afschins direktes Wort in der CC-Sitzung eingeschaltet, unabhängig von diesem
Gate.

**Gemessene Stände, mit `git fetch` in derselben Befehlskette (Mac-CC):** `origin/master` =
`a25d1ee` · `integration/go-live-0.4` trägt `93e10ef` (2026-08-01 15:50 UTC, Sanitizing) und
`b1cad2f` (19:28 UTC, §7-Durchgang) in der Historie. Kopf zu diesem Zeitpunkt `b0b14ca`
(20:14 UTC), inzwischen `3d95d04` — siehe §9.

**Zeile 8 im Klartext — die Frage, die jetzt zählt.** Sieben Zeilen stehen, G1 ist erteilt, das
Secret ist gesetzt. Damit ist die Versuchung greifbar, `deploy.yml` einzuschalten. **Sie wäre
verfrüht.**

G1 und Deploy-Freigabe sind nicht dasselbe Ereignis — das galt vorher gegenüber Zeile 3 und gilt
jetzt gegenüber Zeile 8. Der Abschluss-Durchgang ist die **letzte Prüfung des Artefakts, das
ausgeliefert wird**: Türfahrten, Rückwärts-Stabilität, 390 px, ohne JS, `prefers-reduced-motion`,
der Protokoll-Eingang in allen Zuständen, die Überlagerung über den gesamten Scrollweg. Nichts
davon ist statisch prüfbar, und keiner der beiden Reviewer konnte es prüfen — beide hatten keinen
Browser im Sandbox-Netz (siehe §8 der Befundliste).

**Position der NobleCause-Session: Zeile 8 steht vor dem Deploy, nicht daneben.** Wer anders
entscheidet, entscheidet damit, den einzigen Prüfschritt zu überspringen, den bisher niemand
gefahren ist. Das ist eine legitime Entscheidung des Leitstands — aber sie gehört ausgesprochen
und hier eingetragen, nicht stillschweigend getroffen.

---

## 3 · Zeile 5 aufgeschlüsselt — was vorliegt und was fehlt

Zeile 5 war als ein Block geführt und ist in Wahrheit dreiteilig. Aufgeschlüsselt, damit der
Leitstand nicht auf ein Ganzes wartet, dessen entsperrender Teil längst dasteht:

| Teil | Inhalt | Stand |
|---|---|---|
| 5a | **Umzugstabelle (Punkt 8)** — Routen alt → neu, 301-Regel, Trailing-Slash- und Fragment-Verhalten, Verifikationszeilen | **im Rekord**, `b3a51e3`: `docs/bereitschaft-punkt8-umzugstabelle-2026-08-01.md` |
| 5b | **Inventare und Kennzahlen** — Routen-Inventar, Asset-/AVIF-Pfade, Chunk-Erwartung für die Karenz, Commit-Hash | **im Rekord**, `0d1639f`: `docs/inventar-go-live-build-2026-08-01.md`; Freigabe-Gegenstand `3d95d04` |
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

## 4 · Zeile 3 — erledigt, mit der Lehre daraus

**Erfüllt am 2026-08-02.** Drei Fingerprints wurden am Admin-Zugang **an der Quelle** gelesen und
gegen den `ssh-keyscan` von außen geprüft, alle identisch; erst dann wurde das Secret gesetzt und
in `gh secret list` bestätigt. Verfahren dokumentiert in
`verfahren-host-key-pinning-2026-08-02.md`.

Der Vergleich an der Quelle ist der ganze Punkt: Ein Keyscan allein pinnt den Schlüssel, den ein
Angreifer gerade untergeschoben hätte. Erst der Abgleich mit dem Wert, den nur der Serverbetreiber
sehen kann, macht daraus eine Bindung.

**Die Lehre, die bleibt:** Das Secret fehlte seit dem Push von P1b. Die Anleitung stand im Auftrag,
der Push ging durch — und danach hat niemand geprüft, ob der zweite Teil auch passiert ist. Eine
Änderung wurde veröffentlicht, deren Voraussetzung offen blieb. Das ist der Grund, warum es dieses
Dokument gibt.

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

**Mac-CC — der einzige offene Arbeitsposten:** Zeile 8, der Abschluss-Durchgang mit Belegen. Je
Punkt ein Beleg mit Screenshot, nicht mit Zusicherung. Der Auftrag liegt separat vor.

**Afschin:** die Abnahme des §8-Zähl-Rucks, sobald der Mac-CC Seite, Stelle und Scrollstand
benennt. Kriterium: die **Kanten** der Trommel bewegen sich nicht, nur ihre Oberfläche. Und das
direkte Wort für `wart.yml` in der CC-Sitzung — davon unabhängig.

**Leitstand:** 2b-Prompt für den VPS-CC und das 301-Fragment (mit der EN-Präzisierung aus §8
Punkt 2, nach dem Verzeichnis-Abgleich aus §6 der Umzugstabelle). Danach die **Deploy-Freigabe** —
sie ist ein eigenes Ereignis nach G1 und setzt Zeile 8 voraus; siehe §2.

**NobleCause-Session (Architekt):** Abnahme der Belege aus Zeile 8. Sonst nichts offen.

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
**Das ist kein neuer Arbeitsauftrag — der Deploy behebt es.** Es ist das Argument dafür, das Gate nicht länger zu dehnen als nötig — und zugleich kein Argument
dafür, Zeile 8 zu überspringen. Ein Deploy, der einen unbemerkten Bruch mitliefert, kostet mehr als
zwei weitere Stunden mit falschen Terminen.

---

## 9 · Der Freigabe-Gegenstand und wie er zustande kam

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

**Freigabe-Gegenstand: `3d95d04`** (`3d95d0494dd48123111445cf9570765178fba09d`) — kein Kandidat
mehr, sondern der Stand, auf den der Leitstand G1 erteilt hat. Der Kopf von
`integration/go-live-0.4` liegt inzwischen darüber (`b54fa0c`); der Diff über `site/**` und
`gremium/**` zwischen beiden ist **leer**, unabhängig gemessen vom Leitstand und von der
NobleCause-Session. Alles darüber ist Rekordpflege.

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
| 2026-08-02 09:00 | — | Architekt | §5, §8 und §9 ergänzt; §7 je Eigner nachgeführt; Zeitstempel früherer Architekten-Einträge korrigiert (Uhrfehler, siehe Kopf) |
| 2026-08-02 09:10 | 5 | Mac-CC | Docs (Gate-Status, 5a, 5c) in den Rekord: `b3a51e3` |
| 2026-08-02 09:10 | 5 | Mac-CC | Zeile-5-Beleg gesetzt — Platzhalter „Beleg folgt mit dem Commit" → `b3a51e3` |
| 2026-08-02 09:20 | — | Architekt | §9: P10-Vorbehalt entkräftet (`wart.yml:50–52` fängt den Leerlauf ab, Beleg Mac-CC); Empfehlung, G1 an `4e5fb00` zu binden |
| 2026-08-02 09:25 | — | Architekt | §9: G1-Hash-Empfehlung korrigiert — zwei Hashes (Freigabe-Gegenstand `3d95d04`, Dokumentenstand vom Leitstand bei Freigabe) statt eines rekursiven. Hinweis Mac-CC |
| 2026-08-02 ~10:00 | 7 | Leitstand | **G1 erteilt.** Gegenstand `3d95d04` (eigene Messung: Diff über `site`/`gremium` darüber leer), Dokumentenstand `b54fa0c` |
| 2026-08-02 10:05 | 3, 7, 8 | Architekt | Durchgang: §4 auf erledigt umgeschrieben (widersprach Zeile 3), §2 „Zeile 7 im Klartext" durch „Zeile 8 im Klartext" ersetzt (G1 erteilt), §7 je Eigner neu, §9 von „Kandidat" auf „Freigabe-Gegenstand", dieses Protokoll chronologisch sortiert |
| 2026-08-02 10:30 | — | Architekt | §2: `wart.yml` aktiv (Lauf Mo 4.8. 06:00 UTC) und der `master`/`integration`-Versatz eingetragen; §12 neu: P4 vor Sitzung 4 (Steward-Entscheid) und Vorschlag, G1 in Site-Artefakt und Maschine zu trennen |
| 2026-08-02 ~10:55 | — | Mac-CC | **P4 geschlossen**, `cf041a7` auf `integration/go-live-0.4`; Cherry-Pick auf `master` als konfliktfrei gemessen |
| 2026-08-02 11:00 | — | Architekt | §12: P4-Abschluss und der entschiedene Weg auf `master` eingetragen |
| 2026-08-02 ~10:40 | 3 | Afschin | **offen → erfüllt.** Drei Fingerprints an der Quelle gelesen und gegen den Keyscan von aussen geprüft, alle identisch; Secret gesetzt und in `gh secret list` bestätigt |
| 2026-08-02 ~10:45 | 8 | Leitstand | **Zeile 8 angelegt** — Abschluss-Durchgang war bei der Aufschlüsselung von Zeile 5 aus dem Gate gefallen |

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

---

## 12 · P4 vor Sitzung 4 — Steward-Entscheid, und was er für G1 bedeutet

**Entscheid des Stewards (2026-08-02):** P4 wird vor Sitzung 4 geschlossen. Der Befund:
`extract_dissent` nimmt den abschließenden JSON-Votumblock in `dissent_md` mit hinein; darin steht
eine **modellbehauptete** `donation_url`, die nicht die kuratierte ist. Er ist heute harmlos
(Code-Block, nicht klickbar), aber er wird bei **jeder** Sitzung neu geschrieben — und
`sessions/**` ist unveränderlich. Läuft Sitzung 4 ungeändert, steht er ein drittes Mal dauerhaft
im Rekord.

**Geschlossen auf `integration/go-live-0.4`: `cf041a7`.** Ein gemeinsamer Locator
`_votum_block_span` dient sowohl `extract_json_block` als auch dem neuen `strip_votum_block` —
eine Quelle, keine zweite Heuristik, wie vorgegeben. Prosa davor und dahinter unangetastet, ein
json-Block **mitten** im Dissens bleibt stehen, nur der abschließende Votumblock fällt. Sechs
Tests gegen echten Rohtext aller drei Sitzungen, Suite 54/54. Nebenbefund geprüft: `dissent_md`
liegt nach dem Fix bei 4847 / 3127 / 3514 Zeichen, der Zuschnitt `[:6000]` schneidet nicht ab und
blieb unverändert.

**Der Weg auf `master`: eigener Cherry-Pick, nicht der Go-Live-Merge.** Der Mac-CC hat gemessen,
dass `master`s `run_session.py` mit dem Elternstand von `cf041a7` identisch und die Testdatei neu
ist — der Cherry-Pick ist konfliktfrei, `gremium`-only, null `site`-Dateien. Er hat zugleich
festgestellt, dass der Go-Live-Merge **nicht sicher vor dem 6. August steht**; darauf zu wetten
hieße, Sitzung 4 gegen den ungefixten Stand laufen zu lassen. Entschieden: P4 bekommt seinen
eigenen Weg, jetzt, unabhängig vom Go-Live. Er braucht weder G1 noch Zeile 3 — die gaten den
Frontend-Deploy, nicht die Maschine.

**Zwei Bedingungen, die zusammengehören:**

1. **Der Fix muss auf `master` sein, bevor `session.yml` am 6. August läuft.** Auf
   `integration/go-live-0.4` allein wirkt er nicht — siehe den Versatz in §2. Kommt der Go-Live
   vorher, trägt der Merge ihn mit; verzögert er sich, braucht es einen eigenen Weg auf `master`.
   **Der Termin entscheidet, nicht die Absicht.**
2. **Er verschiebt den Freigabe-Gegenstand.** G1 wurde auf `3d95d04` erteilt, belegt mit „Diff
   über `site`/`gremium` darüber leer". Ein P4-Commit macht genau diese Messung ungültig.

**Vorschlag der NobleCause-Session an den Leitstand — G1 trennt, was ohnehin getrennt ist:**

| | |
|---|---|
| **Site-Artefakt** | was `deploy.yml` per `rsync` ausliefert. P4 berührt es **nicht**. G1 auf `3d95d04` bleibt dafür gültig. |
| **Maschine** (`gremium/**`, Workflows) | was in GitHub Actions läuft. Sie wird nicht deployt, sondern von `master` ausgeführt, und hat ihren eigenen Takt: Montag der Wart, Donnerstag die Sitzung. |

Ein einziger Freigabe-Hash für beide zwingt dazu, G1 bei jeder Maschinen-Reparatur neu zu
erteilen, obwohl sich am ausgelieferten Artefakt nichts ändert. **Wenn der Leitstand dem folgt,
bleibt G1 unberührt** und P4 braucht nur seine eigene Abnahme. Folgt er nicht, ist G1 nach dem
P4-Commit auf den neuen Stand nachzuziehen — auch das ist sauber, nur teurer.

**Was P4 nicht ist:** kein Eingriff in den Bestand. Die drei vorhandenen Sitzungen behalten ihren
`dissent_md` unverändert. Repariert wird die Erhebung für künftige Läufe, nie rückwirkend — wie
bei `conditional` (Wart-Nachtrag 3).
