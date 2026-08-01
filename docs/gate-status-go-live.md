# Gate-Status Go-Live noblecause.ai — die eine Wahrheit

**Zweck:** Der einzige Ort, an dem steht, was gerade **wahr** ist. Das Schnittstellenpapier regelt,
wer was tut; dieses Dokument sagt, was davon erledigt ist.
**Regel:** Wer eine Zeile ändert, trägt sie hier ein, mit Beleg und Zeitstempel. Wer eine Zeile
liest, verlässt sich darauf und misst nicht selbst nach.
**Letzte Pflege:** 2026-08-01, 16:00 UTC, Leitstand

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
| 5 | Bereitschaftsbericht inkl. Punkt 8 Umzugstabelle | NobleCause-Session | **offen** | — |
| 6 | Sanitizing-Blocker geschlossen | NobleCause-Session | **erfüllt** | Sanitizing `93e10ef` + §7-Durchgang `b1cad2f`, FF-Merge auf `integration/go-live-0.4` (2026-08-01) |
| 7 | G1 durch den Leitstand | Leitstand | **offen**, blockiert durch 5 | — |

Ausgangszustand der Workflows, bestätigt: `deploy.yml` und `wart.yml` beide `disabled_manually`.
`wart.yml` wird auf Afschins direktes Wort in der CC-Sitzung eingeschaltet, unabhängig von diesem
Gate.

---

## 3 · Zeile 3 im Klartext

Das Secret fehlt real, und zwar seit dem Push von P1b. Der Workflow auf `master` verweist damit auf
ein Secret, das es nicht gibt. Das ist folgenlos, solange `deploy.yml` aus ist, und bricht beim
ersten scharfen Lauf laut ab. Genau so ist der Preflight gebaut.

Es ist trotzdem der Fehler dieses Laufs: die Anleitung stand im P1b-Auftrag, der Push ging durch,
und danach hat niemand geprüft, ob der zweite Teil auch passiert ist. Eine Änderung wurde
veröffentlicht, deren Voraussetzung offen blieb.

Die vier Schritte für Afschin stehen im P1b-Auftrag, Abschnitt 3: Fingerprint über den Admin-Zugang
an der Quelle lesen, `ssh-keyscan` erzeugen, beide vergleichen, nur bei Übereinstimmung setzen.

---

## 4 · Der aktuelle Caddy-Block nach Stufe 2a

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

## 5 · Was als Nächstes geschieht, je Eigner

**NobleCause-Session / Mac-CC:** erst die **Umzugstabelle** (Punkt 8), dann der Sanitizing-Blocker.
Begründung: die Tabelle ist klein, ohne Nebenwirkung und entsperrt sofort zwei Dinge, nämlich 2b und
das 301-Fragment des Leitstands. Der Sanitizing-Blocker ist eine echte `site/`-Änderung und gehört
in dieselbe Spur wie der Abschluss-Durchgang. Nacheinander, nicht parallel, damit nicht zweimal an
denselben Routen gearbeitet wird.

**Afschin:** Zeile 3, das Secret. Und das direkte Wort für `wart.yml` in der CC-Sitzung.

**Leitstand:** 2b-Prompt für den VPS-CC, sobald die Umzugstabelle vorliegt. Danach G1, sobald 5 und
6 stehen.

---

## 6 · Änderungsprotokoll

| Zeitpunkt | Zeile | Von | Änderung |
|---|---|---|---|
| 2026-08-01 ~12:20 UTC | 1 | NobleCause-Session | erfüllt, `d4fcc3c` |
| 2026-08-01 ~14:00 UTC | 2 | Mac-CC | erfüllt, `a25d1ee` |
| 2026-08-01 15:15 UTC | 4 | VPS-CC | erfüllt, sechs Messzeilen |
| 2026-08-01 16:00 UTC | — | Leitstand | Dokument angelegt |
| 2026-08-01 | 6 | NobleCause-Session | erfüllt — Sanitizing `93e10ef` + §7-Durchgang `b1cad2f`, FF-Merge auf `integration/go-live-0.4` |
| 2026-08-01 | Hinweis | NobleCause-Session | `integration/go-live-0.4` hat `origin/master` (`a25d1ee`, P1b) NICHT nachgezogen — Nachzug vor der Schritt-2-Merge nötig (Merge-Basis ist `d4fcc3c`) |
| 2026-08-01 | erledigt | NobleCause-Session | Nachzug erfolgt: `a25d1ee` in integration gemergt (`9cdc546`, nur `.github/workflows/`); `git diff b1cad2f..9cdc546 -- site/` leer → Inventare gültig. Integration-Kopf jetzt `1950ab3` (der Stand für Schritt 2) |
