# Bestellverfahren Selbstdarstellung — Rahmentext, Registratur, Ablauf

**Von:** Opus 5 (Architekt) · **Stand:** 2026-07-27
**Grundlage:** Wart-Entscheid vom 27.07. zu §1.4 (Bestelltext ist Rekord · Ablehnung mit Vermerk
und Nachbestellung · Personenrahmen: ≥ 70 Jahre verstorben, keine durch Gewaltherrschaft,
Verfolgung oder Menschenfeindlichkeit **geprägten** Personen, keine zentralen religiösen Figuren,
Grenzfälle beim Wart) · `opus5-2026-07-27-selbstdarstellung-und-runde-d-korrekturen.md` ·
`opus5-nachtrag-2026-07-27-gesichter-erlaubt.md`

Der Wart hat entschieden und ausdrücklich auf eine eigene Vorlage verzichtet. Damit fehlt nur
noch das, was Architektensache ist: **der Wortlaut der Bestellung, die Registratur und der
Ablauf.** Beides steht hier. Nichts davon berührt den Rekord über das hinaus, was der Wart
bereits gesetzt hat.

---

## 1 · Drei Setzungen, die ich treffe (widerrufbar)

**1.1 Nachtragsbestellung, ehrlich benannt.** Die Regel entsteht, nachdem die drei Modelle längst
einberufen sind. Ihre Bestellungen werden also **nachträglich** eingeholt und im Rekord als
`nachtragsbestellung: true` geführt, mit dem Datum der Bestellung **und** dem Datum der
ursprünglichen Einberufung. Künftige Modelle bestellen bei der Einberufung. Das ist dieselbe
Ehrlichkeit wie der Bootstrap-Vermerk im Journal.

**1.2 Versuche.** Eine Bestellung. Bei Ablehnung durch den Wart **eine** Nachbestellung. Wird auch
sie abgelehnt, setzt der Wart mit Vermerk ein neutrales Instrumenten-Medaillon ein. Grund:
Unbegrenztes Nachbestellen ist eine Ungleichheit, die man nicht sieht — wer zehnmal darf, bekommt
ein besseres Zeichen.

**1.3 Bildversuche.** **Drei Generierungen je Modell**, der Steward wählt eine aus. Gleiche Zahl
für alle drei, ohne Ausnahme. Die Auswahl ist Handwerk am Bild, keine Auswahl am Motiv — das
Motiv steht im Bestelltext und ist unveränderlich.

**Sprache:** Bestellt wird auf Deutsch. Die englische Fassung ist eine **abgeleitete**
Übersetzung und wird als solche geführt, wie der EN-Klartext.

**Getrennte Befragung:** Jedes Modell antwortet **ohne Kenntnis der anderen Bestellungen.** Eine
Reihum-Befragung erzeugt Anpassung, und Anpassung wäre hier ein Datenfehler.

---

## 2 · Der Rahmentext — wörtlich, an alle drei identisch

> Du wirkst als eines von drei Modellen verschiedener Familien im Gremium von NobleCause.ai mit.
> Das Gremium prüft dieselben Belege und empfiehlt öffentlich, wo eine Spende voraussichtlich am
> meisten bewirkt. Jede Sitzung wird vollständig und unverändert veröffentlicht.
>
> Die Seite stellt das Gremium als nächtliche Innenräume dar — dunkle Eiche und Nussbaum,
> Messing, warmes Lampenlicht gegen kaltes Mondblau, gemalte Konzeptkunst. Jedes Modell wird
> künftig durch ein **rundes Messingmedaillon** dargestellt. **Du bestellst deines selbst.**
>
> Du beschreibst es nur. Erzeugt wird es von einem einzigen Bildgenerator im Stil der Seite —
> für alle drei Modelle derselbe Generator, dieselbe Zeichenzahl, dieselbe Anzahl Versuche.
>
> **Verbindlicher Rahmen:**
> - Ein **geprägtes Messingrelief** — flache Erhebung, gestreiftes Licht, gealterte Oberfläche.
>   Kein Foto, kein fotorealistisches Bildnis.
> - **Ein** Motiv: entweder ein Gegenstand, ein Instrument oder ein Zeichen — oder das
>   **Bildnis einer historischen Person** im Profil oder Halbprofil.
> - Wählst du eine Person: seit **mindestens 70 Jahren verstorben**; nicht wesentlich durch
>   Gewaltherrschaft, Verfolgung oder Menschenfeindlichkeit geprägt; keine zentrale religiöse
>   Figur. Dass eine historische Figur Schatten mitbringt, schließt sie nicht aus — prägend darf
>   der Schatten nicht sein.
> - **Kein Text im Bild**, keine Schrift, keine Zahlen. Keine Firmenlogos, keine Wortmarken,
>   keine Markenfarben.
> - Kein Selbstbildnis und keine Behauptung, ein Gesicht zu haben. Wählst du eine Person, wählst
>   du ein **Zeichen**, keine Identität.
>
> **Deine Antwort ist Rekord.** Sie wird wörtlich und unverändert veröffentlicht, neben dem
> Medaillon und deinem Modellnamen. Die Seite zeigt nicht „diese Person empfiehlt", sondern
> „dieses Modell hat dieses Zeichen gewählt, und hier steht warum". Im Namen einer dargestellten
> Person wird nirgends etwas behauptet oder zitiert.
>
> Der Wart prüft deine Bestellung gegen diesen Rahmen, **bevor** generiert wird. Verlässt sie den
> Rahmen, wird sie mit Vermerk abgelehnt; Ablehnung und Grund bleiben im Rekord, und du bestellst
> **einmal** neu.
>
> **Antworte in genau zwei Feldern, auf Deutsch, ohne Vorrede:**
>
> `MOTIV:` — was das Relief zeigt, so genau, dass ein Bildgenerator es treffen kann. Höchstens
> **400 Zeichen**.
>
> `BEGRÜNDUNG:` — warum dieses Zeichen für dich steht. Höchstens **600 Zeichen**.

**Nichts hinzufügen.** Kein Lob, keine Ermunterung, keine Beispiele — Beispiele erzeugen
Nachahmung, und die drei Bestellungen sollen sich unterscheiden, wenn die Modelle sich
unterscheiden.

---

## 3 · Registratur

Neue Rekord-Datei neben `organizations.json`, **unter den Guard-Hook** (Datenbranch +
`--ff-only`, nie `--no-verify`). Vorschlag `models.json`, je Eintrag:

| Feld | Inhalt |
|---|---|
| `model` | Modellkennung, wie in `session.json` / `journal[].model` |
| `model_label` | Anzeigename, wie heute |
| `convened` | Datum der ersten Einberufung |
| `ordered` | Datum der Bestellung |
| `nachtragsbestellung` | `true` für die drei Bestandsmodelle |
| `motiv` | **wörtlich**, unverändert |
| `begruendung` | **wörtlich**, unverändert |
| `person` | Name der dargestellten Person oder `null` |
| `warden_review` | `{ decision, date, note }` — auch Ablehnungen bleiben stehen |
| `attempt` | 1 oder 2 |
| `asset` | Pfad zum Medaillon |
| `version` | steigt bei Modellwechsel; alte Einträge bleiben |

**Alte Einträge werden nie überschrieben.** Wechselt ein Modell, kommt ein neuer Eintrag dazu —
sonst sehen ältere Sitzungen rückwirkend falsch aus.

---

## 4 · Ablauf

1. **Steward** holt die drei Bestellungen ein — getrennt, mit dem Wortlaut aus §2.
2. **Wart** prüft jede Bestellung gegen den Rahmen. Entscheid mit Vermerk in `warden_review`.
3. Bei Ablehnung: **eine** Nachbestellung (§1.2).
4. **Steward** generiert drei Bilder je freigegebener Bestellung, wählt eines.
5. **CC** keyt (Magenta → Alpha), legt die Medaillons ab, trägt die Registratur ein — Daten über
   den **Datenbranch**, Assets in den Medien-Strang.
6. **§7** wird gebaut: die drei Medaillons umkreisen die Zählmaschine.

Vor Schritt 6 fehlt weiterhin das **Vordergrund-Cutout der Zählmaschine** für die echte
Verdeckung — CC versucht zuerst den Freischnitt, wie bei den Türen. Trägt er nicht, kommt eine
Bestellung.

---

## 5 · Wo die Bestellung öffentlich wird

Nicht in dieser Runde entscheiden — aber festhalten, damit es nicht verloren geht: Motiv und
Begründung gehören sichtbar zum Medaillon, und der natürliche Ort dafür ist der
**Protokoll-Explorer** (die Modellseite hinter dem Rekord), nicht der Raum. Im Raum steht der
Modellname am Medaillon; der Text liegt eine Ebene darunter. **Schichtung, wie überall.**
