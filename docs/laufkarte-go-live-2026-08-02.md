# Laufkarte Go-Live noblecause.ai — neun Schritte, drei Akteure

**Von:** Leitstand · **Datum:** 2026-08-02
**Zweck:** Eine Seite, an der entlanggearbeitet wird. Die Begründungen stehen in G1, G2, dem
Nachtrag und den beiden Aufträgen; hier steht nur, wer was tut und was danach passiert.

**Bei der NobleCause-Session liegt nichts mehr.** Alle acht Gate-Zeilen stehen, G1 und G2 sind
erteilt. Was folgt, ist Ausführung.

---

## Die Reihenfolge

| # | Wer | Aktion | Danach |
|---|---|---|---|
| 1 | Mac-CC | Vorher-Beleg sichern | weiter zu 2 |
| 2 | Mac-CC | Merge lokal vorbereiten, Diff vorlegen | **Stopp** |
| 3 | **Afschin** | `git push` nach `master` | weiter zu 4 |
| 4 | VPS-CC | Snapshot + Vorher-Inventar | **Stopp** |
| 5 | **Afschin** | Wort: `deploy.yml` einschalten | weiter zu 6 |
| 6 | Mac-CC | Workflow einschalten, melden | **Stopp**, nicht auslösen |
| 7 | Mac-CC | Deploy über `workflow_dispatch` auslösen | weiter zu 8 |
| 8 | Mac-CC | Verifikation der Auslieferung | **Stopp** |
| 9 | VPS-CC | Caddy Stufe 2b | fertig |

Zwischen 7 und 9 soll wenig Zeit liegen: solange 2b nicht steht, ist die alte Fassung unter
`/sessions/` als Dublette erreichbar.

**Unabhängig davon, nicht Teil dieser Kette:** `wart.yml` einschalten. Ein Satz von Afschin an den
Mac-CC, spätestens Montag vor 06:00 UTC, sonst ist der Testlauf weg.

---

## Prompt A — an den Mac-CC (Schritte 1 und 2)

```
Go-Live noblecause.ai, Schritte 1 und 2 der Laufkarte des Leitstands.
Maßgeblich sind, in ~/Projects/nc-sanitize/docs/:
  cc-auftrag_leitstand_go-live-ablauf-2026-08-01.md  (§1 und §2)
  g2-deploy-freigabe-leitstand-2026-08-02.md
  nachtrag-g2-2026-08-02.md

Schritt 1 — Vorher-Beleg sichern, als docs/go-live-vorher-beleg-2026-08-02.md:
- Status und cache-control fuer: /, /sessions/2026-07c/, /journal/,
  eine Datei unter /_app/immutable/, /favicon.svg, /gibt-es-nicht/
- Die Terminzeile der Startseite im Wortlaut
- /sitzungen/2026-07c/ muss heute 404 liefern
- origin/master vor dem Merge notieren: das ist der Rollback-Punkt

Schritt 2 — Merge vorbereiten, NICHT pushen:
- integration/go-live-0.4 nach master mergen, lokal
- Belegen: es ist ein Fast-Forward, kein Merge-Commit
- Belegen: cf041a7 (P4-Fix, gremium/) ist enthalten
- git log --oneline und Diffstat vorlegen

Dann anhalten. Der Push nach master ist Afschins Hand, nicht deine.
Das gilt auch, wenn deploy.yml aus ist und der Push folgenlos waere.
Kein gh workflow enable, kein Deploy, kein Anfassen von site/ oder gremium/.
```

---

## Prompt B — an den VPS-CC (Schritt 4)

Selbsttragend, nach dem Push und vor dem Einschalten von `deploy.yml`.

```
Snapshot und Vorher-Inventar vor dem ersten Deploy von noblecause.ai.
Read-only bis auf den Snapshot. Kein Caddy, keine Konfiguration, kein Deploy.

1) Snapshot ausserhalb des ausgelieferten Baums:
   sudo cp -a /srv/noblecause /srv/noblecause.vor-0.4.0

2) Pruefen, beide Zahlenpaare muessen uebereinstimmen:
   sudo du -sh /srv/noblecause /srv/noblecause.vor-0.4.0
   sudo find /srv/noblecause -type f | wc -l
   sudo find /srv/noblecause.vor-0.4.0 -type f | wc -l
   Erwartet rund 2,9 MB.

3) Vorher-Inventar, wird spaeter fuer die Waisenliste gebraucht:
   sudo find /srv/noblecause -name index.html -printf '/%P\n' \
     | sed 's|index.html$||' | sort > /root/inventar-vor-0.4.0.txt
   sudo find /srv/noblecause/_app/immutable -type f -printf '/%P\n' \
     | sort > /root/inventar-vor-0.4.0-chunks.txt
   wc -l /root/inventar-vor-0.4.0*.txt

Berichte: die vier Zahlen aus 2, die beiden Zeilenzahlen aus 3, und den
vollstaendigen Inhalt von inventar-vor-0.4.0.txt.

Dann anhalten. Der Snapshot wird nicht vor dem 4. August entfernt — er ist
zugleich die Rueckversicherung fuer die Chunk-Karenz.

Rueckspielung, falls sie je gebraucht wird, hier zur Kenntnis, nicht ausfuehren:
   sudo rm -rf /srv/noblecause
   sudo mv /srv/noblecause.vor-0.4.0 /srv/noblecause
```

---

## Prompt C — an den Mac-CC (Schritte 6 bis 8)

Erst nach Afschins Wort zu `deploy.yml`.

```
Go-Live noblecause.ai, Schritte 6 bis 8. Afschin hat deploy.yml freigegeben.
Maßgeblich: ~/Projects/nc-sanitize/docs/cc-auftrag_leitstand_go-live-ablauf-2026-08-01.md, §4 und §5.

Schritt 6: deploy.yml einschalten, Status melden. NICHT ausloesen. Anhalten.

Schritt 7: Deploy ueber workflow_dispatch auf master ausloesen, nicht durch
einen Push. Lauf-URL in den Bericht. Bricht der Lauf ab, greift die
P1b-Haertung und legt ein Issue an — dann kein Rollback noetig, es wurde
nichts ausgeliefert.

Schritt 8: Verifikation. Erwartungen:
 1 /                          200, neue Fassung, max-age=300, must-revalidate
 2 Terminzeile Startseite     Wart-Datum nicht in der Vergangenheit, Sitzung 6.8.
 3 /sitzungen/2026-07c/       200  (vorher 404)
 4 /sessions/2026-07c/        200 mit der ALTEN Seite — erwartet, kein Fehler.
                              Der Deploy laeuft ohne --delete, die alten Dateien
                              bleiben liegen. Beleg gehoert in den Bericht, weil
                              erst er zeigt, dass die 301 in Schritt 9 etwas bewirkt.
 5 zwei Permalinks aus der Umzugstabelle   200
 6 eine AVIF-Datei            content-type festhalten. Nicht image/avif -> an 2b melden
 7 ein Chunk der VORGAENGER-Version (Hash aus dem Vorher-Beleg)   200, Karenz-Beleg
 8 /gibt-es-nicht/            404, keine Startseite

Schlaegt 1, 3 oder 5 fehl: Rollback nach §7 des Ablaufs, kein Nachbessern im
Live-Betrieb. Danach anhalten und melden — Schritt 9 laeuft auf dem VPS.
```

---

## Prompt D — an den VPS-CC (Schritt 9)

Der vollständige Auftrag liegt als
`~/Projects/nc-sanitize/docs/cc-auftrag_leitstand_caddy-stufe2b-VPS.md`. Inhalt in die
VPS-Sitzung einfügen, er ist selbsttragend.

**Zwei Ergänzungen aus dem Nachtrag, die vor §1 des Auftrags gehören:**

```
Vor dem Verzeichnis-Abgleich: Nach-Inventar erheben und die Waisenliste bilden.

   sudo find /srv/noblecause -name index.html -printf '/%P\n' \
     | sed 's|index.html$||' | sort > /root/inventar-nach-0.4.0.txt
   sudo find /srv/noblecause/_app/immutable -type f -printf '/%P\n' \
     | sort > /root/inventar-nach-0.4.0-chunks.txt
   comm -23 /root/inventar-vor-0.4.0.txt /root/inventar-nach-0.4.0.txt
   comm -23 /root/inventar-vor-0.4.0-chunks.txt /root/inventar-nach-0.4.0-chunks.txt

Die Liste wird klassifiziert, NICHT geloescht:
 - Chunks der Vorgaengerversion  -> erwartet, bleiben liegen, das ist die Karenz
 - /sessions/ und alles darunter -> erwartet, ab 2b durch die 301 verdeckt
 - alles andere                  -> MELDEN, nicht entfernen. Eine Route, die
   verschwindet, ohne dass jemand sie umbenannt hat, ist ein Befund ueber den
   Build, nicht ueber die Auslieferung.
```

---

## Was danach noch offen ist, aber nichts blockiert

- Aufräumen von Snapshot und verwaistem `/srv/noblecause/sessions/`, frühestens 4. August
- Host-Key-Sweep über `aion-lumen.com`, `carta`, `Frag-Shifu`, zusammen mit dem
  aion-lumen-Cache-Doppelmangel, im 0.4.0-Strang
- CSP `script-src`/`style-src` mit Build-Zeit-Hashes, 0.4.1
- P6, C7, P7, P9, P8.3, P11 nach 0.4.1
- Abschluss-Fieldnote des Release-Piloten
