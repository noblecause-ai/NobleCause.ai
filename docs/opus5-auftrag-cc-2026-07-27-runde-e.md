# Auftrag an CC — Runde E: Bestell-Sondersitzung, Council-Türmitte, Aufräumen

**Von:** Opus 5 · **Branch:** `feat/council-rooms` · **Stand:** 2026-07-27
**Commit nur auf ausdrückliche Freigabe. Kein Push.**

---

## §1 · Bestell-Sondersitzung (Backend)

Ein Lauf über den **regulären API-Mechanismus**, der die drei amtierenden Modelle nach ihrer
Selbstdarstellung fragt. Zweck doppelt: die Bestellungen entstehen auf demselben Pfad wie jedes
andere Modellwort, und das Backend läuft vor Go-Live einmal vollständig durch.

**Drei bindende Auflagen:**

1. **Eigener Behälter, nicht `sessions/`.** Vorschlag `commissions/2026-07-27/`, `kind:
   "commission"`. Eine Bestellsitzung hat keine Säulen, keine Empfehlung, keinen Zählstand —
   im normalen Schema sähe jeder Verbraucher (Aggregation, Tafel, Sitzungsliste, künftiger
   Explorer) eine leere Sitzung. `schedule.json` / `next_research` bleiben unberührt.
   *Abnahme:* ein Buildlauf zeigt die Bestellsitzung **nirgends** als Sitzung. Findet ein
   Renderer sie doch, ist der Behälter falsch — nicht der Renderer zu flicken.
2. **Eine Runde, kein Umdenken-Schritt.** Die Modelle dürfen die Bestellungen der anderen nicht
   sehen, sonst gleichen sich die Zeichen an. Ist das nur per Code abschaltbar: als Code-Eingriff
   berichten, nicht still über einen Parameter lösen. Dann bleibt der Umdenken-Pfad in diesem
   Lauf ungetestet — auch das in den Bericht.
3. **Rahmentext unverändert** aus `docs/opus5-2026-07-27-bestellverfahren-selbstdarstellung.md`
   §2 in die Prompt-Ablage, über den **Datenbranch**, unter den Guard-Hook. Keine Kürzung, keine
   Anpassung „damit es besser läuft" — ändern darf ihn nur der Wart.

Antwortformat: zwei Felder `MOTIV` (≤ 400 Zeichen) und `BEGRÜNDUNG` (≤ 600 Zeichen), Deutsch.
Registratur-Schema steht in §3 desselben Dokuments.

**Einberufung durch den Wart abwarten** — Entscheid und Journal-Kennzeichnung kommen von dort.
Bau darf vorher stehen, der Lauf nicht.

**Bericht:** Ergebnis je Modell, plus was der Lauf über das Backend gezeigt hat — Schlüssel,
Streaming, Parsing, Fehlerpfade, Journalschreibung. Ausdrücklich als **Teiltest** benennen.

---

## §2 · Council-Türmitte

**Nur der Ratssaal.** Study und Archiv sitzen und werden nicht angefasst.

Die Tür öffnet nach rechts versetzt statt mittig. Verdacht: `perspective-origin` steht als feste
Viewport-Prozentzahl, die Aperturmitte wandert aber mit dem Cover-Crop — im Council klaffen schon
im Messfall sechs Punkte in y (gemessen 50,7 / 42,1 %, gesetzt 50,5 / 48 %).

**Auftrag:** Origin zur Laufzeit aus derselben Cover-Rechnung ableiten wie der Türhotspot. Eine
Quelle, keine zweite Konstante.

**Abnahme:** bei 16:9, 21:9 und einem hohen schmalen Fenster liegt die Fahrtachse auf der
Türmitte; Abweichung in Prozentpunkten je Fall nennen.

---

## §3 · Aufräumen

**§3.1 Journal-Backfill (Wart-Vorgabe).** Der Lauf vom **2026-07-27** hat mutmaßlich einen
Journaleintrag geschrieben, bevor der `model_label`-Branch gemerged war. Er fällt unter den
Backfill: `model` gesetzt → Label nachziehen, über den **Datenbranch** + `--ff-only`, nie
`--no-verify`. **Zuerst nachsehen und berichten**, was der Eintrag enthält. Weicht etwas ab —
fehlender Eintrag, Abbruch, Teilschreibung — **berichten statt reparieren**, das geht an den Wart
zurück.

**§3.2 Medien-Strang bündeln und committen.** Vorher eine Zeile je Datei: wird sie referenziert,
von wo? Was keinen Verweis hat, kommt nicht mit — insbesondere `register.avif` und Reste der
`jpg → avif`-Migration. *Abnahme:* ein sauberer Checkout von HEAD rendert alle drei Räume
vollständig.

**§3.3 `docs/`.** Nur eine **Liste vorlegen**, nichts verschieben: Bild-Originale nach
`docs/asset-originals/` in die Provenienz-Struktur (benannt nach Serie/Position statt
Generatorzeit), überholte und `--SKIP`-Dokumente nach `docs/archiv/` mit einer Zeile Begründung
im Kopf. Nicht löschen — sie erklären, warum Dinge so sind. Löschen macht der Steward selbst.

---

## §4 · Reihenfolge

1. §2 Council-Türmitte (klein, unabhängig).
2. §3.1 Journal-Backfill.
3. §1 Sondersitzung bauen; Lauf erst nach Wart-Einberufung.
4. §3.2 Medien-Strang.
5. §3.3 `docs/`-Liste.

**Liegt bewusst:** §7 Medaillons (wartet auf die Bestellungen), Vordergrund-Cutout der
Zählmaschine (Freischnitt zuerst versuchen, wie bei den Türen), Protokoll-Explorer inkl. 2b.

**Guardrails unverändert:** Guard-Hook, Daten nur über Datenbranch + `--ff-only`, nie
`--no-verify`, kein Push, §0-Verfassung, versiegelte Datennaht, Geometrie am gerenderten AVIF.

---

## §5 · Nachtrag aus der Einberufung des Warts (27.07., verbindlich)

Die Einberufung ist erteilt. Damit gilt zusätzlich zu §1:

**Kennung und Ablage:** Kennung `commission-1`, Ablage `commissions/2026-07-27/`. **Der Lauf
zählt nicht als Sitzung** — die Sitzungsnummerierung bleibt den Beratungen vorbehalten,
Sitzung 4 ist weiterhin die vom 8. August.

**Journaleintrag, Felder wörtlich:**

- `type: "commission"` — Bestandseinträge brauchen **kein** Backfill; ein fehlendes `type` liest
  sich als regulärer Scout- oder Einberufungseintrag, das Schema hat `additionalProperties`.
- `commission_ref: "/commissions/2026-07-27/"`
- `convene: true`
- `convene_rationale:` „Sondersitzung außer der Reihe: Bestellung der Selbstdarstellungen der
  drei Sitzinhaber; zugleich Backend-Durchlauf vor Go-Live. Keine Beratungsfrage, keine
  Empfehlung."
- `model` / `model_label` nach dem tatsächlich laufenden Orchestrator-Kontext, bestehende Regel
  (kein Modell gelaufen → kein Feld).

**Gleichbehandlung wird belegt, nicht behauptet.** Die Kommissionsdatei führt **je Modell**:
Rahmentext-Hash (oder Wortlaut), Versuchszahl, Zeitstempel. Das ist eine Rekord-Anforderung, kein
Logging — sie gehört in die Kommissionsdatei, nicht in eine Logdatei.

**Keine Aggregation.** Es wird keine Säulenfrage verhandelt, also entsteht keine
Gremium-Empfehlung und die Aggregationsregel findet keine Anwendung. Wenn der Mechanismus an
dieser Stelle etwas berechnen will, ist der Zweig abzuschalten — und das im Bericht zu nennen.

**Rahmengrenzen im Prompt:** Der Wart weist darauf hin, dass die Modelle die drei Rahmengrenzen
kennen müssen, wenn ihnen die Personenwahl eröffnet wird. **Das ist bereits erfüllt** — §2 des
Bestellverfahrens nennt die 70-Jahre-Regel, den Prägungs-Ausschluss und den Ausschluss zentraler
religiöser Figuren im Wortlaut. Keine Ergänzung nötig; bitte beim Einpflegen gegenprüfen, dass
diese drei Sätze vollständig mitgehen.

**Nach dem Lauf:** die drei Wortlaute **gesammelt und nebeneinander** vorlegen — der Wart prüft
sie gegen seinen Rahmen, **bevor** generiert wird. Ablehnungen mit Vermerk in den Rekord,
Nachbestellung mit gleicher Versuchszahl.
