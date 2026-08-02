# Bereitschaftsbericht Punkt 8 — Umzugstabelle der Routen

**Von:** Opus 5 (Architekt NobleCause) · **Stand:** 1. August 2026
**Für:** Leitstand → 2b-Fragment (301) und VPS-CC
**Gate-Status:** Zeile 5, Teilerfüllung — dieser Teil entsperrt 2b und das 301-Fragment.

---

## 1 · Warum es Umzüge gibt

noblecause.ai ist bereits live. Die neue Fassung benennt **eine** Route um: `/sessions/`
wurde zu `/sitzungen/`, weil sie das einzige englische Wort auf der deutschen Ebene war —
und weil sie die Permalinks auf den Rekord trägt. Der Umzug war vor der ersten
Veröffentlichung gedacht; dass die Seite schon live ist, war mir bis gestern nicht bekannt.

**Damit sind es echte 301-Fälle:** Die alten Adressen sind öffentlich erreichbar und
möglicherweise geteilt. Bei einem Projekt, dessen Produkt ein nachprüfbarer Rekord ist, darf
kein Permalink ins Leere laufen.

---

## 2 · Umzüge — 301 erforderlich

| alt (live) | neu | Belegt live |
|---|---|---|
| `/sessions/` | `/sitzungen/` | ja |
| `/sessions/2026-07/` | `/sitzungen/2026-07/` | ja |
| `/sessions/2026-07b/` | `/sitzungen/2026-07b/` | ja |
| `/sessions/2026-07c/` | `/sitzungen/2026-07c/` | ja |

**Als eine Regel:** `/sessions/*` → `/sitzungen/*`, Pfadrest unverändert, **301 permanent**.

Drei Punkte, die die Regel treffen muss:

- **Trailing Slash.** Die Site läuft mit `trailingSlash: 'always'`; ohne Slash antwortet
  SvelteKit mit 307 auf die Slash-Form. Die Redirect-Regel muss **beide** Formen fangen —
  `/sessions/2026-07c` und `/sessions/2026-07c/` —, sonst entsteht eine Kette
  301 → 307 oder, schlimmer, ein 404 vor dem Redirect.
- **Fragmente.** Die Sitzungsseiten nutzen `:target`-Anker (`#saeule-a` und ähnliche) für
  die Sprungleiste. Fragmente überträgt der Browser selbst, sie dürfen in der Regel nicht
  angefasst werden.
- **Kein Catch-All-Fallback.** Ein `/sessions/*` → `/sitzungen/` **ohne** Pfadrest würde
  jeden alten Permalink auf die Übersicht werfen statt auf sein Protokoll. Der Rest muss
  mitwandern.

---

## 3 · Unverändert — kein Redirect

| Route | Bemerkung |
|---|---|
| `/` | Startseite, jetzt „The Study" |
| `/manifest/` | |
| `/idee/` | |
| `/impressum/` | |
| `/journal/` | bleibt bewusst englisch-neutral — `schedule.json` trägt `last_journal: "/journal/…"`, geschrieben vom Cron. Eine Umbenennung wäre ein Eingriff in ein Feld, das dem Mechanismus gehört. |
| `/journal/2026-07-08c/` | und alle weiteren Journal-IDs |

---

## 4 · Neu — noch nie öffentlich, kein Redirect nötig

| Route | Inhalt |
|---|---|
| `/ratssaal/` | The Council |
| `/archiv/` | The Archive |
| `/en/` | Study, englisch |
| `/en/council/` | |
| `/en/archive/` | |
| `/journal/2026-07-24/` | Journaleintrag, neu im Rekord |
| `/journal/2026-07-27b/` | Kommission, neu im Rekord |

---

## 5 · Was entfällt

**Nichts.** Jede live erreichbare Route existiert in der neuen Fassung weiter — entweder
unverändert oder unter der neuen Adresse. Es gibt keinen Pfad, der ersatzlos verschwindet
und einen 410 oder eine Erklärseite bräuchte.

---

## 6 · Eine Lücke, und wie sie zu schließen ist

**Diese Tabelle beruht auf den internen Links der Startseite**, nicht auf einem
vollständigen Verzeichnis. Eine Route, die live existiert, aber von der Startseite nicht
verlinkt ist, würde ich hier nicht sehen.

**Die autoritative Liste liegt auf dem VPS.** Der VPS-CC kann sie in einem Befehl erheben:

```
find /srv/noblecause -name index.html -printf '/%P\n' | sed 's|index.html$||' | sort
```

**Bitte gegen Abschnitt 2 bis 4 abgleichen, bevor das 301-Fragment geschrieben wird.**
Taucht dort ein Pfad auf, der hier fehlt, gehört er in die Tabelle — und möglicherweise in
die Redirect-Regel. Das ist der Unterschied zwischen einer belegten und einer plausiblen
Umzugstabelle, und ich kann ihn von hier aus nicht schließen.

Ein Kandidat, den ich ausdrücklich nicht ausschließen kann: ob die alte Fassung bereits
einen englischen Zweig unter `/en/` hatte. Falls ja, wäre er nicht „neu", und es müsste
geprüft werden, ob die Pfade identisch sind.

---

## 7 · Nach dem Deploy zu verifizieren

Zwei Zeilen genügen, sie gehören in die Verifikationsliste des Leitstands:

- `/sessions/2026-07c/` → **301** auf `/sitzungen/2026-07c/`, und diese Adresse liefert
  **200** mit dem Protokoll der Sitzung 3
- `/sessions/2026-07c` (ohne Slash) → landet ebenfalls auf `/sitzungen/2026-07c/`,
  **ohne Zwischen-404**

---

## 8 · Was von Punkt 5 des Schnittstellenpapiers noch aussteht

Diese Tabelle deckt den Umzugsteil. Der vollständige Bereitschaftsbericht folgt nach dem
Sanitizing-Blocker und dem Abschluss-Durchgang und bringt mit: Routen-Inventar der
ausgelieferten Verzeichnisse, Asset-Inventar mit allen AVIF-Pfaden, Chunk-Erwartung für die
Karenz, den Commit-Hash und die Liste der bewusst offen bleibenden Review-Befunde.
