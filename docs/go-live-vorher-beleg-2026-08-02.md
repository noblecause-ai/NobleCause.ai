# Go-Live Vorher-Beleg — noblecause.ai, 2026-08-02

**Von:** Mac-CC · **Schritt 1** von `cc-auftrag_leitstand_go-live-ablauf-2026-08-01.md` §1
**Zweck:** Ist-Zustand VOR dem Deploy festhalten, damit nach dem Go-Live nachweisbar ist, was sich
geändert hat — und der Rollback-Punkt notiert ist.
**Messweg:** HTTP gegen die Live-Seite `https://noblecause.ai`. Die Live-Seite ist die **alte
Fassung vom 14. Juli 2026** (`last-modified: Tue, 14 Jul 2026 15:24:19 GMT` durchgängig).

---

## 1 · Gemessene Antworten (Status + cache-control)

| Pfad | Status | `cache-control` | `content-type` | `last-modified` |
|---|---|---|---|---|
| `/` | **200** | `public, max-age=300, must-revalidate` | `text/html; charset=utf-8` | Tue, 14 Jul 2026 15:24:19 GMT |
| `/sessions/2026-07c/` | **200** | `public, max-age=300, must-revalidate` | `text/html; charset=utf-8` | Tue, 14 Jul 2026 15:24:19 GMT |
| `/journal/` | **200** | `public, max-age=300, must-revalidate` | `text/html; charset=utf-8` | Tue, 14 Jul 2026 15:24:19 GMT |
| `/_app/immutable/entry/start.DORCQyTH.js` | **200** | `public, max-age=31536000, immutable` | `text/javascript; charset=utf-8` | Tue, 14 Jul 2026 15:24:19 GMT |
| `/favicon.svg` | **200** | `public, max-age=3600, must-revalidate` | `image/svg+xml` | Tue, 14 Jul 2026 15:24:19 GMT |
| `/gibt-es-nicht/` | **404** | `public, max-age=300, must-revalidate` | — | — |

- Der `/_app/immutable/`-Pfad ist aus der Live-Startseite gezogen (der alte 14.-Juli-Chunk). Er trägt
  korrekt `immutable, max-age=31536000` — das sind die Chunks, die ohne `--delete` erhalten bleiben
  (24-Stunden-Karenz).
- Die cache-control-Werte spiegeln Caddy Stufe 2a (HTML/404 `max-age=300, must-revalidate`,
  ungehashte Medien `max-age=3600`, gehashte Chunks `immutable`).

## 2 · `/gibt-es-nicht/` — kein SPA-Fallback

Status **404**, **Body leer** (keine Startseite untergeschoben). Belegt: ein toter Pfad bleibt tot.

## 3 · `/sitzungen/2026-07c/` — muss heute 404 sein

**404** (`cache-control: public, max-age=300, must-revalidate`). Bestätigt: die neue Protokoll-Route
ist noch nicht ausgeliefert. Nach dem Deploy muss dieser Pfad **200** liefern (Go-Live-Ablauf §5,
Zeile 3).

## 4 · Terminzeile der Startseite (Wortlaut)

> **Nächster Research des Warts in 5 T 14 h (20.7.2026) · Nächste Sitzung in 24 T 20 h (8.8.2026)**

Belegt den Reparaturgrund: das Wart-Datum **20.7.2026 liegt in der Vergangenheit** (heute ist der
2.8.), und der Sitzungstermin **8.8.2026 ist falsch** (die geltende nächste Sitzung ist der 6.8.).
Die relativen Countdowns („in 5 T 14 h", „in 24 T 20 h") sind clientseitig gerechnet und ebenfalls
gegen die alten Daten stehengeblieben. Nach dem Go-Live muss diese Zeile ein nicht in der
Vergangenheit liegendes Wart-Datum und den Sitzungstermin 6.8. tragen (Go-Live-Ablauf §5, Zeile 2).

## 5 · Rollback-Punkt

`origin/master` vor dem Merge:

```
a25d1ee18c8c80019d07e23651a3827d306632e1
```

Das ist der Stand, auf den ein Rollback per erneutem Deploy zurückgeht (Go-Live-Ablauf §7). Ergänzt
durch den Dateisystem-Snapshot des VPS-CC unmittelbar vor dem Deploy (G2-Freigabe §2), der vom Build
unabhängig ist.
