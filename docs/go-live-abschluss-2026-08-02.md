# Go-Live noblecause.ai 0.4.0 — Abschluss und Beleg

**Von:** Leitstand · **Datum:** 2026-08-02
**Stand:** Auslieferung 12:40 UTC · Caddy Stufe 2b 13:04 UTC · **abgeschlossen**
**Freigabe-Gegenstand:** `site/**` = `21c9851` · `gremium/**` = `cf041a7` · `origin/master` = `8242fa0`

---

## 1 · Vorher und nachher

| Prüfung | vor dem Go-Live | jetzt |
|---|---|---|
| Startseite | Build vom 14. Juli | neue Fassung, `last-modified` 2. August |
| Terminzeile | „Research in 5 T 14 h (20.7.2026)", Datum zwölf Tage in der Vergangenheit; „Sitzung 8.8." | `next_research` 3.8., `next_session` **6.8.**, „Letzte Prüfung: 27. Juli" korrekt vergangen |
| `/sitzungen/2026-07c/` | 404 | 200, Protokoll Sitzung 3 |
| `/sessions/2026-07c/` | 200, alte Fassung | **301** auf `/sitzungen/2026-07c/` |
| Unterseiten-Cache | **kein** `Cache-Control` | `max-age=300, must-revalidate` |
| `favicon.svg` | fälschlich `immutable`, ein Jahr | `max-age=3600, must-revalidate` |
| gehashte Chunks | `immutable` | unverändert `immutable`, zwei Generationen auf der Platte |
| Fehlerantworten | ohne Header, später `max-age=300` | `no-store` |
| CSP | keine | `base-uri`, `form-action`, `frame-ancestors`, `object-src` |
| Modelltext im HTML | ungeprüft per `{@html}` | zentral bereinigt, Wortlaut vollständig erhalten |
| Deploy-Host-Key | `ssh-keyscan`, blind | gepinnt aus `VPS_KNOWN_HOSTS`, mit Preflight |
| Deploy-Fehler | still, alte Seite bleibt stehen | Issue mit Label `ci-failure:deploy` |

---

## 2 · Messzeile 9 geschlossen — Browser-Gegenprobe des Leitstands

Der VPS-CC konnte nur den Header messen, nicht die Ausführung. Vom Leitstand im Browser
nachgeholt:

- **Hydration läuft.** Die scrollgetriebene Bühnenfahrt der Startseite arbeitet, die Szene wechselt
  beim Scrollen. Das ist Client-JavaScript in Ausführung; die CSP unterbindet nichts.
- **Weiterleitung greift.** `https://noblecause.ai/sessions/2026-07c/` landet auf
  `/sitzungen/2026-07c/` mit der neuen Fassung.

### Zwei Feldbefunde, die niemand vorhergesagt hatte

**a) Der erste Versuch sah aus wie ein Fehlschlag — er war der HTML-Cache.** Die Adresse war
Minuten zuvor mit `max-age=300, must-revalidate` geladen worden. Innerhalb dieser fünf Minuten
liefert der Browser aus dem eigenen Cache, ohne den Server zu fragen; die Weiterleitung wird nicht
gesehen. Die URL bleibt auf der alten Adresse stehen, die alte Seite erscheint.

**Das ist kein Mangel, sondern die Cache-Klasse bei der Arbeit.** Es gehört trotzdem
festgehalten: Wer eine alte Adresse kurz zuvor besucht hat, sieht die Weiterleitung bis zu fünf
Minuten lang nicht — und wer das nicht weiss, diagnostiziert einen Fehler, den es nicht gibt. Für
Suchmaschinen ist es folgenlos, sie fragen ohne Cache.

**b) Die Weiterleitung verwirft den Query-String.** `?cachebust=1` war nach dem Redirect fort.
Caddys `redir` überträgt die Abfrage nicht von selbst. Für diese Seite folgenlos, sie verwendet
keine Query-Parameter — jetzt gemessen statt angenommen. Sollte je ein Parameter eingeführt werden,
muss die Regel um `?{query}` ergänzt werden.

---

## 3 · Was der Lauf gekostet und gebracht hat

Acht Gate-Zeilen, zwei Tore, vier Akteure auf zwei Maschinen, neun Ausführungsschritte, ein
Rollback.

**Der Rollback war ein Erfolg, kein Rückschlag.** Messzeile 2 verlangte „eine Weiterleitung", der
slashlose Pfad lieferte zwei. Der VPS-CC hat zurückgerollt statt nachzubessern und die Ursache
sauber isoliert. Die Fehlspezifikation lag beim Leitstand: `(.+)` behält den abschliessenden Slash
nur, wenn die Anfrage einen trägt. Aufgelöst durch eine korrigierte Erwartung, nicht durch eine
dritte Regel — Verzeichnis von Datei am Pfadstring zu unterscheiden wäre eine Namensheuristik
gewesen, und die Kette existierte vor dem Go-Live in derselben Form.

**Drei Befunde kamen aus dem Messen, nicht aus dem Planen:** die Unterseiten ohne Cache-Header, der
Permalink-Bruch durch die Umbenennung, und die Waisenlisten-Rechnung (`comm -23` misst, was
verschwunden ist, und ohne `--delete` kann nichts verschwinden — die Waisen stehen in der
Schnittmenge, nicht in der Differenz).

---

## 4 · Offen, mit Terminen

| Was | Wann | Wer |
|---|---|---|
| `wart.yml` einschalten | vor Mo 3.8., 06:00 UTC | Afschin, Wort an den Mac-CC |
| Sitzung 4, erster Produktivlauf der gehärteten Maschine | Do 6.8., 12:00 UTC | läuft von selbst |
| Aufräumen: Snapshot `/srv/noblecause.vor-0.4.0`, verwaistes `/srv/noblecause/sessions/`, Altkopie `~/inventar-vor-0.4.0.txt` | frühestens 4.8. | VPS-CC |
| Hauptbaum `~/Projects/NobleCause.ai` nachziehen, vier untracked Pfade beiseite | nach dem Go-Live | Mac-CC |
| Host-Key-Sweep `aion-lumen.com`, `carta`, `Frag-Shifu` + aion-lumen-Cache-Doppelmangel | 0.4.0-Strang | Leitstand |
| CSP `script-src`/`style-src` mit Build-Zeit-Hashes | 0.4.1 | — |
| P6, C7, P7, P9, P8.3, P11 | 0.4.1 | Befundliste |
| 0.4.0 als Release-Lauf über den Piloten schliessen | nächster Schritt | Leitstand |

---

## 5 · Für die Abschluss-Fieldnote

1. **Bei mehreren Akteuren braucht der Pilot eine Zustandsablage, nicht nur eine
   Rollenverteilung.** Das Schnittstellenpapier sagte, wer was tut; es fehlte ein Ort, der sagt, was
   gerade wahr ist. Der Gate-Status wurde mitten im Lauf nachgezogen, nachdem der Mac-CC den Zustand
   aus einem Shell-Befehl rekonstruieren musste und bei einer Zeile danebenlag.
2. **„Liegt vor" ist kein Beleg.** Zweimal in diesem Lauf, einmal beim Architekten und einmal beim
   Leitstand: Dokumente lagen im Arbeitsverzeichnis und galten als erledigt, waren aber in keinem
   Commit. Ein Gate-Beleg ist ein Hash oder eine Messung.
3. **Eine Zeile, die neu geschnitten wird, verliert Teile.** Der Abschluss-Durchgang fiel aus dem
   Gate, als Zeile 5 in 5a/5b/5c aufgeteilt wurde, und war danach von keiner Zeile gehalten.
4. **„Freigabe" gegen „Afschins Hand" war dreimal ad hoc zu klären.** Gehört zwischen den Läufen
   entschieden und in `00-START-HIER` eindeutig formuliert.
5. **Erwartungen müssen stimmen, sonst kostet die Rollback-Disziplin funktionierende Arbeit.** Der
   Rollback nahm CSP und `no-store` mit, obwohl beide bestanden hatten. Die Lehre ist nicht, die
   Regel zu lockern.
6. **Konzept Freigabekonsole.** Das Freigabesystem hat klar getrennte Tore, aber seine Menschenhälfte
   ist ein Satz in einem Terminal. Eine Konsole, die den Gate-Status live liest, den freizugebenden
   Befehl samt Folgen zeigt und die Freigabe zu einer bewussten Handlung macht — Schieber statt
   Knopf — wäre die fehlende Hälfte. Zusammen mit dem Automationsmuster dieses Laufs: serielle
   Prompt-Erzeugung, Rückmeldung, nächste Anweisung, Zwischenergebnisse im geteilten Ordner.
