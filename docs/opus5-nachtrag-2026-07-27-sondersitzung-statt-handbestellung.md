# Nachtrag — Sondersitzung statt Handbestellung

**Von:** Opus 5 · **Stand:** 2026-07-27
**Ersetzt** §4 („Ablauf") in `opus5-2026-07-27-bestellverfahren-selbstdarstellung.md`.
**Anlass:** Steward-Vorschlag — die Bestellungen nicht von Hand einholen, sondern als
Sondersitzung über den regulären API-Mechanismus.

---

## Der Vorschlag ist besser als mein Ablauf. Drei Gründe

**1. Die Gleichheit wird erzwungen statt eingehalten.** Ich hatte „derselbe Rahmentext, dieselbe
Zeichenzahl, dieselbe Anzahl Versuche" als Disziplin formuliert. Über den regulären Mechanismus
ist es **Maschinerie**: derselbe Aufruf, dieselben Parameter, dieselbe Fehlerbehandlung für alle
drei. Auf einer Seite, deren Prämisse Gleichbehandlung ist, ist das kein Detail.

**2. Die Herkunft stimmt.** Die Bestelltexte sind Rekord (Wart-Entscheid). Rekord, der über
denselben Pfad entsteht wie jedes andere Modellwort, braucht keine Sonderbegründung, warum man
ihm glauben soll. Eine Handbestellung müsste sie liefern.

**3. Der Backend-Test ist echt fällig.** Die Fehlschläge der Vergangenheit saßen genau dort:
JSON-Parsing, Streaming-Pflicht, Key-Härtung. Der letzte erfolgreiche Lauf war 2026-07-20; seither
ist am Backend gearbeitet worden. Vor Go-Live einen Lauf mit **harmlosem Inhalt** durchs volle
Rohr zu schicken, ist billiger als der erste Fehlschlag auf einer echten Sitzung.

**Mit einer Einschränkung, die im Bericht stehen muss:** Es ist ein **Teiltest**. Geprüft werden
Schlüssel, Streaming, Parsing, Fehlerpfade, Journalschreibung. **Nicht** geprüft werden
Belegrecherche, Aggregation und die Umdenken-Runde — die kommen in einer Bestellsitzung nicht vor.
Ein grüner Lauf heißt „das Rohr trägt", nicht „die Sitzung trägt".

---

## Auflage 1 · Der Mechanismus wird wiederverwendet, **nicht der Behälter**

Das ist die Bedingung, an der alles hängt.

Eine Bestellsitzung hat keine Säulen, keine Organisationen, keine Empfehlung und keinen
Zählstand. Landet sie im normalen `sessions/`-Schema, sieht **jeder Verbraucher** eine Sitzung
ohne Ergebnis: die Aggregation, die Tafel, die Sitzungsliste, der künftige Protokoll-Explorer.
Im besten Fall bricht etwas sichtbar, im schlechteren steht eine leere Sitzung dauerhaft im
Rekord und niemand merkt es.

**Also: eigener Behälter, eigene Kennung, eigenes Schema.** Vorschlag `commissions/2026-07-27/`
mit `kind: "commission"`. Kein Eintrag in `sessions/`, keine Berührung von
`schedule.json`/`next_research` — der Montagsrhythmus bleibt unangetastet.

**Abnahme dazu:** Ein Lauf über die Site-Buildpipeline zeigt die Bestellsitzung **nirgends** als
Sitzung. Wenn ein Renderer sie doch findet, ist der Behälter falsch gewählt und nicht der
Renderer zu flicken.

## Auflage 2 · Eine Runde, keine Umdenken-Runde

Der reguläre Mechanismus zeigt den Modellen in der zweiten Runde die Voten der anderen. **Für
Bestellungen muss dieser Zweig aus sein** — sonst passen sich die Zeichen aneinander an, und
genau das wollten wir mit der getrennten Befragung ausschließen.

Ist das nicht per Konfiguration abschaltbar, sondern nur per Code, dann **ist es ein
Code-Eingriff und wird als solcher berichtet** — nicht heimlich über einen Parameter gelöst, der
später jemanden überrascht. Und dann bleibt der Umdenken-Pfad in diesem Lauf ungetestet; auch das
gehört in den Bericht.

## Auflage 3 · Der Rahmentext wird zur Prompt-Datei

Der Wortlaut aus §2 des Bestellverfahrens geht **unverändert** in die Prompt-Ablage
(`prompts.py` oder eine Schwesterdatei) — unter den Guard-Hook, über den Datenbranch, wie jede
andere Rekord-Datei. Keine Kürzung, keine Anpassung „damit es besser läuft". Wenn der Text
geändert werden muss, ändert ihn der Wart, nicht der Bau.

---

## Wer was tut

- **Der Wart beruft ein.** Eine Sondersitzung ist ein Rekord-Akt; sie beginnt mit seinem
  Entscheid und mit dem Vermerk, warum außer der Reihe getagt wird.
- **CC baut** den Bestell-Lauf: eigener Behälter, eine Runde, Rahmentext aus der Prompt-Ablage,
  Journaleintrag mit eigener Kennzeichnung (**welche** — Wart-Sache, nicht meine).
- **Der Steward startet** den Lauf und trägt das Ergebnis vor.
- **Der Wart prüft** die drei Bestellungen gegen seinen Rahmen, **bevor** generiert wird.
- Danach unverändert: drei Bildversuche je freigegebener Bestellung, Steward wählt, CC keyt und
  trägt die Registratur ein, **dann §7**.

---

## Was das für den Zeitplan heißt

Die Sondersitzung sitzt jetzt **vor** §7 auf dem kritischen Pfad — das UI wartet auf die
Medaillons. Sie ist aber kurz, und sie ersetzt einen Backend-Test, der ohnehin vor Go-Live
fällig gewesen wäre. **Netto kostet sie nichts.**

Parallel laufen unverändert weiter und hängen an nichts davon: die Türmitte, der Medien-Strang,
`docs/`, und der Protokoll-Explorer samt 2b.
