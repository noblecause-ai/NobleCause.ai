# G1 — Freigabe des Leitstands

**Von:** Leitstand · **Datum:** 2026-08-02 · **Betrifft:** Go-Live noblecause.ai
**Grundlage:** `gate-status-go-live.md` §2, §3, §9 · `bereitschaft-punkt8-umzugstabelle-2026-08-01.md` ·
`bereitschaft-punkt4-befundliste-2026-08-01.md`

---

## 1 · Entscheidung

**G1 ist erteilt.**

| | |
|---|---|
| **Freigabe-Gegenstand** | `3d95d04` (`3d95d0494dd48123111445cf9570765178fba09d`) |
| **Dokumentenstand bei Freigabe** | `b54fa0c`, Kopf `integration/go-live-0.4`, vom Leitstand am 2026-08-02 gemessen |

**Eigene Prüfung, nicht übernommen:** `git log integration/go-live-0.4 -- site gremium` nennt
`3d95d04` als jüngsten Treffer. `git diff --stat 3d95d04..integration/go-live-0.4 -- site gremium`
ist **leer**. Die vier Commits darüber (`b3a51e3`, `4e5fb00`, `a127e0c`, `b54fa0c`) sind
ausschliesslich Rekordpflege. Der Freigabe-Gegenstand ist damit belegt und nicht bloss behauptet.

**Die Zwei-Hash-Regel wird übernommen.** Der Einwand des Mac-CC war richtig: eine Empfehlung, die
einen Hash nennt, kann nicht unter dem Hash liegen, den sie nennt.

---

## 2 · G1 ist nicht die Deploy-Freigabe

Zwei getrennte Ereignisse. G1 sagt: der Stand ist inhaltlich freigegeben. Der scharfe Deploy
braucht zusätzlich:

- **Gate-Zeile 3, `VPS_KNOWN_HOSTS`.** Weiterhin offen, Afschins Hand. Ohne das Secret bricht der
  Deploy im Host-Key-Schritt ab. In der Befundliste ist derselbe Punkt als **P8.2 der einzige als
  sicherheitsrelevant eingestufte offene Befund** geführt. Beides ist dieselbe Zeile, und sie ist
  jetzt der einzige verbleibende Blocker vor dem Deploy.
- **Caddy Stufe 2b**, Auftrag liegt bei.
- **G2**, Afschins Knopf.

---

## 3 · Vier Entscheidungen, die beim Leitstand lagen

### 3.1 Content-Security-Policy — geteilt, nicht vertagt

Eine vollständige CSP ist **kein Header-Zusatz**. Der Build hydriert über Module-Skripte und
eingebettete Daten; eine `script-src`-Regel ohne Build-Zeit-Hashes oder Nonces bricht entweder die
Seite oder ist mit `'unsafe-inline'` wirkungslos. Caddy kann diese Hashes nicht bilden. Das ist
Arbeit am Build, nicht an der Auslieferung.

Deshalb geteilt:

- **Jetzt, mit 2b:** die Direktiven, die keine Skripte betreffen und deshalb nichts brechen können —
  `base-uri`, `form-action`, `frame-ancestors`, `object-src`. Eine Zeile, kein Risiko.
- **0.4.1:** `script-src` und `style-src` mit Build-Zeit-Hashes. Eigener Schnitt, eigene Prüfung.

Die Einschätzung der NobleCause-Session, dass die CSP nach dem Sanitizing die zweite Schicht ist und
nicht die erste, teile ich. Sie ist kein Go-Live-Blocker. Sie war aber auch kein Versehen, sondern
ist hiermit entschieden.

### 3.2 EN-Zweig — übernommen

Keine 301-Regel auf `/en/*`. Es gibt dort nur die drei Raum-Landings und keine Rekord-Routen; eine
Regel würde ins Leere zielen und im schlechteren Fall die Landings fangen. Genau **eine** Umzugsregel:
`/sessions/*` → `/sitzungen/*`.

### 3.3 Pult-Überlappung — zur Kenntnis

Steward-Entscheid, belassen. Kein Nachfassen durch den Leitstand.

### 3.4 Verzeichnis-Abgleich vor dem Fragment — eingebaut

Die Umzugstabelle beruht auf den internen Links der Startseite, nicht auf einem Verzeichnis des
ausgelieferten Standes. Der Abgleich ist als **erster Schritt mit Stopp-Punkt** in den 2b-Auftrag
aufgenommen. Taucht dort ein Pfad auf, der in der Tabelle fehlt, wird nicht improvisiert, sondern
gemeldet.

---

## 4 · Ein Punkt mit Uhr, der nicht im Gate steht

**P4 läuft am 6. August ab, nicht am Go-Live.**

`extract_dissent` schreibt den rohen Votumblock mit einer modellbehaupteten `donation_url` bei
**jeder** Sitzung erneut. Läuft Sitzung 4 ungeändert, steht sie ein drittes Mal im
unveränderlichen Rekord.

Das ist kein Go-Live-Blocker und steht deshalb in keiner Gate-Zeile. Genau deshalb ist es der Punkt,
der am ehesten verlorengeht: alle Aufmerksamkeit liegt auf dem Deploy, und die Frist gehört einem
anderen Ereignis. Nach dem 6. August ist er nicht mehr reparabel, nur noch markierbar.

**Der Leitstand fordert ihn nicht ein** — er gehört der NobleCause-Session. Er steht hier, damit die
Frist einen zweiten Ort hat als den, an dem gerade niemand hinsieht.

Dasselbe gilt für **C5**, die fehlende Serialisierung von `session.yml` und `wart.yml`. Für den
Go-Live ist sie folgenlos: `deploy.yml` schreibt kein `schedule.json` und kollidiert mit keinem der
beiden. Die vorläufige Verhaltensregel — kein manueller Dispatch des einen, während der andere
laufen kann — berührt den Go-Live-Ablauf nicht.

---

## 5 · Was jetzt läuft

| Eigner | Nächster Schritt |
|---|---|
| **Afschin** | `VPS_KNOWN_HOSTS` setzen (P1b-Auftrag §3, mit Fingerprint-Gegenprobe). Direktes Wort für `wart.yml`. |
| **VPS-CC** | Caddy Stufe 2b, Auftrag liegt bei |
| **Mac-CC** | Abschluss-Durchgang mit Belegen. Danach Go-Live-Ablauf ab §0, das Gate erneut prüfen |
| **NobleCause-Session** | P4 vor dem 6. August |
| **Leitstand** | G2 nach Zeile 3, 2b und Abschluss-Durchgang |
