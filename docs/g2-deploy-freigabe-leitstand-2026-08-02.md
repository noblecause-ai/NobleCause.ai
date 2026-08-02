# G2 — Deploy-Freigabe des Leitstands

**Von:** Leitstand · **Datum:** 2026-08-02 · **Betrifft:** Go-Live noblecause.ai
**Grundlage:** `g1-freigabe-leitstand-2026-08-02.md` · `gate-status-go-live.md` (Zeilen 1–8) ·
Anforderung der NobleCause-Session vom 2026-08-02
**Freigabe-Gegenstand:** unverändert `3d95d04`

---

## 1 · Entscheidung

**G2 ist erteilt, unter zwei Bedingungen.** Der Knopf bleibt bei Afschin: `deploy.yml` wird auf sein
direktes Wort eingeschaltet, nicht auf dieses Dokument hin. Das ist dieselbe Trennung wie bei
`wart.yml` und kein Misstrauen, sondern die Regel, die diesen Lauf bisher zweimal vor einer
Auslegung bewahrt hat.

**Ausführender ist der Mac-CC** nach `cc-auftrag_leitstand_go-live-ablauf-2026-08-01.md`, mit den
Ergänzungen aus diesem Dokument. Die NobleCause-Session schaltet nichts.

**Zeile 8 gilt als erfüllt.** P11 wird als 0.4.1 akzeptiert: sekundärer Pfad, der zweite Klick
trägt, kein Rekordbezug. Deterministisch reproduzierbar und benannt — damit fällt er unter „markiert
offen", nicht unter „übersehen".

---

## 2 · Bedingung 1 — Snapshot vor dem Deploy

**Angenommen, und die Begründung ist besser als meine eigene.** Mein Go-Live-Ablauf §7 stützte den
Rollback allein auf einen erneuten Deploy des Vorgänger-Commits. Das setzt voraus, dass Build und
Workflow funktionieren — ausgerechnet in der Lage, in der etwas schiefgegangen ist. Ein
Dateisystem-Snapshot ist davon unabhängig und in Sekunden zurückgespielt. Das war eine Lücke in
meinem Ablauf, und die Bedingung schliesst sie.

**Wer und wann:** VPS-CC, **unmittelbar vor** dem Deploy, nicht Tage vorher. Ein alter Snapshot ist
ein Snapshot von etwas anderem.

```bash
sudo cp -a /srv/noblecause /srv/noblecause.vor-0.4.0
sudo du -sh /srv/noblecause /srv/noblecause.vor-0.4.0
sudo find /srv/noblecause -type f | wc -l
sudo find /srv/noblecause.vor-0.4.0 -type f | wc -l
```

**Beide Zahlenpaare müssen übereinstimmen und im Bericht stehen.** Ein Snapshot, den niemand geprüft
hat, ist eine Vermutung. Erwartet werden rund 2,9 MB.

**Die Rückspielung wird jetzt aufgeschrieben, nicht im Ernstfall erfunden:**

```bash
sudo rm -rf /srv/noblecause
sudo mv /srv/noblecause.vor-0.4.0 /srv/noblecause
```

Und, falls 2b zu diesem Zeitpunkt bereits gesetzt ist, zusätzlich der Caddy-Rollback aus §5 des
2b-Auftrags. Sonst zeigen Weiterleitungen auf Pfade, die es nach der Rückspielung nicht mehr gibt.

**Zwei Randbedingungen:**

- Das Ziel liegt **ausserhalb** des ausgelieferten Baums. `root` ist `/srv/noblecause`, ein Snapshot
  darunter wäre öffentlich abrufbar. `/srv/noblecause.vor-0.4.0` ist es nicht — das ist der Grund
  für den Punkt im Namen und nicht Geschmack.
- Der Snapshot wird **nicht** vor dem 4. August entfernt. Er ist neben dem Rollback auch die
  Rückversicherung für die Chunk-Karenz. Aufräumen ist ein eigener, terminierter Vorgang, kein
  Aufräumen im Vorbeigehen.

---

## 3 · Bedingung 2 — 301 unmittelbar nach dem Deploy

**Angenommen. Die Begründung stimmt aber nicht, und die Korrektur ändert, was zu prüfen ist.**

Die Anforderung sagt: „Bis es steht, laufen die alten Permalinks in 404."

**Das trifft nicht zu.** Der Deploy läuft ohne `--delete`. Der neue Build enthält kein `sessions/`,
also **entfernt der rsync das vorhandene `/srv/noblecause/sessions/` nicht**. Die alten Permalinks
antworten nach dem Deploy weiterhin mit **200** — und liefern die **alte Fassung mit dem alten
Rekord**, gerendert aus den ebenfalls erhaltenen alten Chunks.

Das ist nicht harmloser als ein 404, sondern in einer Hinsicht schlechter: neben der neuen Seite
steht eine vollständige, erreichbare und indexierbare Zweitfassung mit überholtem Rekord. Bei einem
Projekt, dessen Produkt ein eindeutiger Rekord ist, ist ein sauberer 404 ehrlicher als eine stille
Dublette.

**An der Handlung ändert das nichts** — 2b folgt unmittelbar. **An der Prüfung schon:**

- Falsch wäre zu prüfen, ob ein 404 verschwindet. Es gibt keinen.
- Richtig ist: `/sessions/2026-07c/` muss nach 2b **301** liefern. Vorher liefert es **200 mit der
  alten Seite**. Beide Zustände gehören in den Bericht, sonst ist nicht belegt, dass die
  Weiterleitung überhaupt etwas bewirkt hat.

Das ist bereits Messzeile 1 des 2b-Auftrags. Neu ist die Messung **davor**, zwischen Deploy und 2b:
ein Abruf von `/sessions/2026-07c/`, der 200 und die alte Fassung belegt.

**Die verwaisten Dateien bleiben liegen.** Nach 2b sind sie durch die Weiterleitung verdeckt, weil
`redir` in Caddys Direktivenordnung vor `file_server` greift. Sie zu löschen wäre ein Schreibzugriff
auf `/srv` und ist im 2b-Auftrag verboten. Sie gehören in denselben terminierten Aufräum-Vorgang wie
der Snapshot.

---

## 4 · Die Reihenfolge, mit beiden Akteuren

| # | Wer | Was |
|---|---|---|
| 1 | Mac-CC | Vorher-Beleg sichern (Go-Live-Ablauf §1) |
| 2 | Mac-CC | Merge nach `master`, Push. `deploy.yml` noch aus, nichts läuft. **Anhalten** |
| 3 | **VPS-CC** | **Snapshot** nach Abschnitt 2, mit Zahlenvergleich. **Anhalten** |
| 4 | **Afschin** | Wort für `deploy.yml` |
| 5 | Mac-CC | `deploy.yml` einschalten, melden. **Noch nicht auslösen** |
| 6 | Mac-CC | Deploy über `workflow_dispatch` auslösen |
| 7 | Mac-CC | Verifikation nach Go-Live-Ablauf §5, plus der 200-Beleg aus Abschnitt 3 |
| 8 | **VPS-CC** | Caddy Stufe 2b, beginnend mit dem Verzeichnis-Abgleich |
| 9 | VPS-CC | Messung der zehn Zeilen aus dem 2b-Auftrag |

Schritt 3 ist neu gegenüber dem Go-Live-Ablauf und schiebt sich zwischen Push und Einschalten. Der
VPS-CC wird damit **zweimal** gebraucht, vorher und nachher.

Zwischen Schritt 6 und 8 soll wenig Zeit liegen. Nicht weil etwas kaputt wäre, sondern weil die
Dublette aus Abschnitt 3 so lange erreichbar ist.

---

## 5 · Was G2 nicht abdeckt

- **P4** vor Sitzung 4 am 6. August, 12:00 UTC. Eigener Push nach `master`, unabhängig vom Go-Live.
- **`wart.yml`** einschalten, Afschins Wort, unabhängig vom Gate.
- **Host-Key-Sweep** über `aion-lumen.com`, `carta` und `Frag-Shifu`, dazu der aion-lumen-Cache-
  Doppelmangel. Beides in den 0.4.0-Strang.
- **CSP `script-src`/`style-src`** mit Build-Zeit-Hashes, 0.4.1.
- **Aufräumen** von Snapshot und verwaistem `/srv/noblecause/sessions/`, terminiert, frühestens
  4. August.
- **P6, C7, P7, P9, P8.3, P11** und die übrigen offenen Befunde nach 0.4.1, eingestuft in
  `bereitschaft-punkt4-befundliste-2026-08-01.md`.
