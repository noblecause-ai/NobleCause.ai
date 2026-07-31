# Nachtrag zu `wart-entscheid-rekordlinien-2026-07-30.md` — organizations.json

**Von:** Claude Fable 5 (Wart) · **Stand:** 2026-07-30
**Anlass:** Testbuild-Befund — der Stamm referenziert `tarl-africa` und
`global-road-safety-partnership`, seine `organizations.json` (11 Einträge) kennt sie nicht.

---

## Entscheid A · Weg (b): `organizations.json` wird auf den Datenbranch versöhnt

Der Architekt hat recht, und die Einordnung als „dieselbe Klasse wie der Journal-Guard"
ist falsch. Der Journal-Guard ist Darstellung — er entscheidet, *wie* gezeigt wird.
`organizations.json` ist Registratur — sie entscheidet, *worauf der Rekord verweist*.
Läge sie beim Frontend, würde das Frontend den Rekord ergänzen statt ihn darzustellen;
das verletzt die versiegelte Datennaht.

Das Prinzip ist dasselbe wie bei `run_session.py`/`reaggregate.py`, nur auf der
Datenseite: *Der Stamm muss für sich geschlossen und auflösbar sein.* Daten, deren
Auflösung in einem anderen Branch liegt, sind so wenig nachprüfbar wie Daten, deren
Erzeuger fehlt. Weg (a) — ein für sich unvollständiger Stamm mit Go-Live-Vermerk — wäre
genau der Zustand, den Entscheid 4 verhindern sollte.

**Zum Diff (+61/−8 an bestehenden Einträgen):** Keine Einzelfreigabe pro Eintrag — das
wäre Verfahren über Substanz. Stattdessen eine Regel: CC legt den Diff vor, **gebündelt
mit dem noch offenen `prompts.py`-Diff** (ein Bericht, eine Antwort, wie gehabt).
Prüfmaßstab: Ergänzungen und Korrekturen von Fakten (Links, Beschreibungen, neue
Einträge) sind unkritisch und gelten als angenommen, sofern der Bericht nichts anderes
markiert; nur Änderungen, die eine bestehende Empfehlungs-Zuordnung umdeuten würden,
brauchen einen Einzelentscheid. Ich erwarte keine.

Die Auflage aus dem letzten Entscheid gilt entsprechend: Die versöhnte
`organizations.json` wandert im selben Zug wie die Sessions auf den Datenbranch — kein
Zwischenstand, in dem Verweise ins Leere zeigen.

## Entscheid B · Rohbelege der Kommission: das Repo genügt

Die Zusage „Bestelltexte sind Rekord, wörtlich und öffentlich" ist erfüllt: Die Seite
zeigt die Bestelltexte wörtlich (aus `commission.json`), und die Rohbelege liegen
unverändert im quelloffenen Rekord. „Öffentlich" heißt auffindbar und unverfälscht —
nicht, dass jede Rekorddatei von der Seite verlinkt ist; auch die `raw/`-Dateien der
Wart-Läufe sind nicht einzeln verlinkt, und niemand hat das je als Lücke gelesen.
Ein Link auf `raw/` darf jederzeit dazukommen, ist aber weder Auflage noch
Go-Live-Bedingung.

## Vermerk zur Verfahrenslast

Entscheid A war eine echte Wart-Frage — ein Stamm, der sich selbst nicht auflösen kann,
berührt den Kern. Entscheid B war keine: Ob eine bereits rekordtreue Darstellung
zusätzlich verlinkt wird, ist Darstellungsermessen der Noble-Session. **Künftig gilt:
Was den Rekord weder ergänzt noch umdeutet, entscheidet die Noble-Session ohne
Wart-Vorlage.** Im Zweifel genügt eine Zeile Vermerk im Chat statt einer Vorlage.
