# CC-Auftrag (Leitstand) — auf dem VPS auszuführen: Caddy Stufe 2b für noblecause.ai

**Für:** Claude Code **auf dem VPS** `185.143.100.222` · **Von:** Leitstand · **Datum:** 2026-08-02
**Dieser Auftrag ist selbsttragend.** Er verweist auf keine Datei, die dort nicht liegt.

**Reihenfolge, die nicht verhandelbar ist:** Dieser Auftrag wird **nach** dem Deploy der neuen
Fassung ausgeführt, nicht davor. Vorher zeigt eine Weiterleitung auf `/sitzungen/…`, das es auf der
Platte noch nicht gibt, und bricht die laufende Seite selbst.

**Ausgangslage:** Caddy `v2.11.2`, systemd, **eine** `/etc/caddy/Caddyfile`. Der noblecause-Block
ist eigenständig. Stufe 2a ist gesetzt (drei Cache-Klassen). **Einrückung im Block: Tabs, nicht
Leerzeichen.** Die Datei ist `caddy fmt`-konform und muss es bleiben.

---

## 1 · Schritt 1: Verzeichnis-Abgleich — mit Stopp-Punkt

Die Umzugstabelle beruht auf den internen Links der Startseite, nicht auf einem Verzeichnis des
ausgelieferten Standes. Vor jeder Änderung die autoritative Liste erheben:

```bash
find /srv/noblecause -name index.html -printf '/%P\n' | sed 's|index.html$||' | sort
```

Erwartet werden genau diese Gruppen:

- **umzugspflichtig:** `/sessions/`, `/sessions/2026-07/`, `/sessions/2026-07b/`,
  `/sessions/2026-07c/`
- **unverändert:** `/`, `/manifest/`, `/idee/`, `/impressum/`, `/journal/` und alle `/journal/<id>/`
- **neu:** `/sitzungen/…`, `/ratssaal/`, `/archiv/`, `/en/`, `/en/council/`, `/en/archive/`

**Taucht ein Pfad auf, der in keine dieser Gruppen fällt: anhalten und melden.** Nicht raten, keine
zusätzliche Regel erfinden. Besonders zu prüfen: ob die alte Fassung bereits einen `/en/`-Zweig
hatte. Falls ja, ist er nicht neu, und die Pfade müssen verglichen werden.

Ergebnis der Liste vollständig in den Bericht.

---

## 2 · Schritt 2: Die Änderungen

Alle drei bleiben im noblecause-Block. Sicherung zuerst, Abschnitt 3.

### 2.1 Umzug `/sessions/` → `/sitzungen/`

**Genau eine Umzugsregel**, in zwei Zeilen aufgeteilt, damit keine Weiterleitungskette entsteht.
Direkt nach `encode` einfügen, vor den Cache-Klassen:

```caddy
	# --- 301: Protokoll-Pfad umbenannt (/sessions -> /sitzungen), dauerhaft ---
	@sess_root path /sessions /sessions/
	redir @sess_root /sitzungen/ permanent

	@sess_sub path_regexp sess ^/sessions/(.+)$
	redir @sess_sub /sitzungen/{re.sess.1} permanent
```

Begründung der Aufteilung: `(.+)` behält den Pfadrest samt abschliessendem Slash, `/sessions` und
`/sessions/` landen ohne Zwischenschritt auf `/sitzungen/`. Eine einzige Regel über
`^/sessions(/.*)?$` erzeugte für die Wurzelform ein `/sitzungen` ohne Slash und damit eine zweite
Weiterleitung durch den `file_server`.

**Keine Regel auf `/en/*`.** Der englische Zweig hat nur die drei Raum-Landings und keine
Rekord-Routen; eine Regel dort zielte ins Leere und finge im schlechteren Fall die Landings.

**Fragmente** (`#saeule-a` und ähnliche) überträgt der Browser selbst und werden nicht angefasst.
Die Seite verwendet keine Query-Parameter; sollte der Abgleich aus Schritt 1 welche zeigen, melden
statt ergänzen.

### 2.2 Fehlerantworten nicht zwischenspeichern

Seit Stufe 2a tragen 404-Antworten `max-age=300`, weil der `@html`-Matcher `*/` auch bei Fehlern
greift. Das ist strenger als der Zustand davor, aber ausgerechnet beim 404 will man nicht, dass er
fünf Minuten überlebt, nachdem er aufgehört hat wahr zu sein — und der Moment, in dem das auffällt,
ist die Permalink-Prüfung unmittelbar nach diesem Auftrag.

Am Ende des Blocks, vor `log`:

```caddy
	handle_errors {
		header Cache-Control "no-store"
		respond "" {err.status_code}
	}
```

Der leere Rumpf hält das heutige Verhalten (404 mit 0 Bytes) bei. **Falls Caddy diese Form nicht
annimmt: melden, nicht improvisieren.** Eine Fehlerseite mit Inhalt ist eine Gestaltungsfrage und
gehört nicht in diesen Auftrag.

### 2.3 Eingeschränkte Content-Security-Policy

In den vorhandenen `header`-Sammelblock, als zusätzliche Zeile:

```caddy
		Content-Security-Policy "base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'"
```

**Bewusst ohne `script-src` und `style-src`.** Die Seite hydriert über Module-Skripte und
eingebettete Daten; eine Skript-Direktive ohne Build-Zeit-Hashes bricht entweder die Seite oder ist
mit `'unsafe-inline'` wirkungslos. Diese vier Direktiven können nichts brechen. Der Rest ist Arbeit
am Build und geht nach 0.4.1.

### 2.4 AVIF — nur falls die Messung es verlangt

Liefert die Auslieferung nach dem Deploy AVIF-Dateien **nicht** als `image/avif`, dann und nur dann:

```caddy
	@avif path *.avif
	header @avif Content-Type image/avif
```

Ist der Content-Type korrekt, wird **nichts** ergänzt. Eine überflüssige MIME-Regel ist eine, die
später jemand erklären muss.

---

## 3 · Ablauf

1. **Sicherung:** `sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-301-csp-$(date -u +%Y%m%dT%H%M%SZ)`
   Pfad notieren.
2. **Ändern.** Nur der noblecause-Block, Tabs als Einrückung. Vor dem Speichern per `diff` gegen die
   Sicherung prüfen, dass ausschliesslich Zeilen dieses Blocks betroffen sind.
3. `sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile` — schlägt es fehl:
   zurückrollen, nicht reparieren.
4. `sudo caddy fmt /etc/caddy/Caddyfile --diff` — nur lesend. Zeigt es Abweichungen: **nicht**
   schreibend formatieren, sondern die eigene Einrückung korrigieren.
5. `sudo systemctl reload caddy`, danach `systemctl is-active caddy` und
   `journalctl -u caddy -n 20 --no-pager`.
6. Messen, Abschnitt 4.

---

## 4 · Abnahme durch Messung

Alle Abrufe gegen `https://noblecause.ai`, **ohne** dem Redirect automatisch zu folgen, damit der
Statuscode sichtbar bleibt.

| # | Pfad | Erwartung |
|---|---|---|
| 1 | `/sessions/2026-07c/` | **301** auf `/sitzungen/2026-07c/` |
| 2 | `/sessions/2026-07c` (ohne Slash) | **301** auf `/sitzungen/2026-07c/`, **eine** Weiterleitung, kein 404 dazwischen |
| 3 | `/sitzungen/2026-07c/` | 200, Protokoll der Sitzung 3, `max-age=300, must-revalidate` |
| 4 | `/sessions/` und `/sessions` | **301** auf `/sitzungen/`, je eine Weiterleitung |
| 5 | `/journal/2026-07-20/` | **200**, kein Redirect. Belegt, dass die Regel nicht zu breit greift |
| 6 | `/en/` | **200**, kein Redirect |
| 7 | `/gibt-es-nicht/` | 404, `cache-control: no-store`, Rumpf 0 Bytes |
| 8 | eine Datei unter `/_app/immutable/` | `31536000, immutable` — unverändert durch 2b |
| 9 | eine AVIF-Datei | `content-type` festhalten. Nicht `image/avif` → Abschnitt 2.4 |
| 10 | `/` | Antwort trägt den `Content-Security-Policy`-Header, Seite lädt und hydriert |

**Zeile 5 ist die wichtigste.** Sie belegt, dass die Umzugsregel nur den umbenannten Pfad fängt und
nicht die unveränderten. Zeile 10 belegt, dass die CSP nichts gebrochen hat: nicht nur der Header
zählt, sondern dass die Seite im Browser normal arbeitet.

**Zusätzlich, weil derselbe Caddy vier Sites bedient:** je ein Abruf auf `https://aion-lumen.ch/`
und `https://mirhamed.ch/` mit Status und `cache-control`, als Beleg, dass nichts Fremdes berührt
wurde.

---

## 5 · Rollback

Bei fehlgeschlagener Validierung, fehlgeschlagenem Reload oder einer nicht erfüllten Erwartung:

```
sudo cp <Sicherungspfad> /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl reload caddy
```

Danach die Messungen wiederholen und den Ausgangszustand belegen. **Kein Reparieren im laufenden
Betrieb.**

**Ein Sonderfall, der koordiniert werden muss:** Wird die *Auslieferung* zurückgerollt, also der
Deploy, dann müssen auch diese 301-Regeln zurück. Sonst zeigen Weiterleitungen auf Pfade, die es
nach dem Rollback nicht mehr gibt. In dem Fall meldet der Mac-CC, und dieser Auftrag wird über
Abschnitt 5 rückgängig gemacht.

---

## 6 · Bericht

Sicherungspfad · vollständige Ausgabe des `find` aus Schritt 1 · vollständiger Diff des Blocks ·
Ausgabe von `validate` und `fmt --diff` · Reload-Status und Journal-Auszug · die zehn Messzeilen ·
die zwei Fremd-Site-Abrufe · falls zurückgerollt: an welchem Schritt und mit welcher Ausgabe.

Gemessene Werte, keine Zusicherungen. Ein „konnte ich nicht prüfen" ist ein zulässiges Ergebnis.

---

## 7 · Verbote

- **Nicht vor dem Deploy ausführen.**
- Nichts unter `/srv/` ändern oder löschen. Keine Aufräum-Routine einführen, jetzt und künftig.
- Keine Änderung an den Blöcken für aion-lumen.ch, mirhamed.ch, frag-shifu.ch oder ntfy.
- Kein schreibendes `caddy fmt` auf die ganze Datei.
- Keine 301-Regel ausser der einen aus 2.1. Keine `/en/`-Regel. Kein Catch-All auf `/sitzungen/`
  ohne Pfadrest.
- Keine `script-src`- oder `style-src`-Direktive in der CSP.
- Keine AVIF-Regel ohne vorherige Messung.
- Kein `git`, kein Deploy, keine Paketinstallation, kein Dienst-Neustart ausser `reload caddy`.
