# Bildassets der Startseite

> **Deploy-Hygiene (16.07.2026):** Die PNG-**Originale** (Provenienz + Re-Ableitung) liegen
> jetzt hier unter `docs/asset-originals/media/…` — **außerhalb `site/`**, damit sie nicht in
> den Build (`site/build/`) kopiert und nicht via `rsync` ausgeliefert werden. Ausgeliefert
> wird nur, was die Seite referenziert: die `*-display.jpg`-Derivate unter
> `site/static/media/…`. Die „Produktiver Pfad"-Spalten unten sind relativ zu
> `docs/asset-originals/media/` zu lesen. `site/static/media/` schrumpft dadurch von ~34 MB
> auf ~1,5 MB. Zusätzlich wurde `scenes/hall-display.jpg` (initial vorgeladen) von Qualität
> 78 auf 55 neu codiert: **367 kB → 199 kB** (Derivat, kein C2PA-Original — Neucodierung
> unkritisch). Ein echtes WebP/AVIF-Derivat war lokal nicht erzeugbar (`sips` dieser
> macOS-Version kann kein WebP schreiben, kein `cwebp`/`avifenc` vorhanden) → empfohlener
> Folgeschritt: WebP/AVIF-Ableitung im CI (`cwebp`), Original erhalten.

Die beiden produktiven Plates wurden am 15.07.2026 byte-identisch aus dem historischen,
nicht deployten SOL-Build kopiert. Sie wurden weder neu codiert noch komprimiert. Damit
bleiben die eingebetteten C2PA Content Credentials der Originale erhalten.

| Produktiver Pfad | Ursprung | Maße | Bytes | SHA-256 |
|---|---|---:|---:|---|
| `provenance/ratssaal.png` | `sol-build/site/static/ratssaal.png` | 1672 × 941 | 2.005.102 | `b19282508301fe946b1f025e3bc43c6318fb5ed2c3fa546850b64ee13a2fbbbd` |
| `provenance/vorraum.png` | `sol-build/site/static/vorraum.png` | 1915 × 821 | 1.997.325 | `0e02cc4dfa508dc9d29e71325442fc8bbf3ad2b4903a2b0d9a74388cf2d79b56` |

Laut dem Provenienznachweis im Ursprung enthalten beide Dateien C2PA-Angaben von
`gpt-image` v2.0 und deklarieren `trainedAlgorithmicMedia`. Responsive Derivate wurden
bewusst nicht erzeugt, solange kein lokal verifizierter C2PA-erhaltender Prozess besteht.

Diese beiden historischen Plates bleiben als Provenienzoriginale erhalten. Die finale
Bühne verwendet die folgenden neuen Szenenbilder; alle Bildelemente besitzen feste
Breiten- und Höhenattribute.

## Finale Szenenbilder

Am 16.07.2026 wurden vier vom Auftraggeber bereitgestellte, zusammengehörige Szenenbilder
byte-identisch aus `docs/` in den produktiven Pfad übernommen. Sie ersetzen die
provisorischen CSS-Raumobjekte; sämtliche fachlichen Texte und Links bleiben separate
HTML-Ebenen und werden nicht aus den Bildern abgeleitet.

| Produktiver Pfad | Verwendung | Maße | SHA-256 |
|---|---|---:|---|
| `council-machine.png` | Ratssaal, drei Pulte und Zählmaschine | 1672 × 941 | `5f35d5a626cdb89fb3a59eca4db03612be60928c675a01129beb423cf8285b11` |
| `council-door.png` | geöffnete Tür zwischen Ratssaal und Vorzimmer | 1672 × 941 | `32e345db016fcfbbbd3e72c6fb8d82bcf1268ffe3b4e6f008c79b4c8abff9280` |
| `antechamber-final.png` | Vorzimmer mit Späher und Wart | 1672 × 941 | `8cdbd4c77f52b10b76831e3c1a2f12251052f2b196f623637f3b990b1d155246` |
| `archive-final.png` | monumentales Sitzungsarchiv | 1672 × 941 | `f9d7a8b2423f9bd2f5ddb3cee6b33c59d1c65760e917af04974477dcd2c05199` |

## Prozess- und Säulenmotive

Die vier Säulenoriginale wurden am 16.07.2026 nach sichtbarem Inhalt aus den vom
Auftraggeber unter `docs/` bereitgestellten Dateien zugeordnet und byteidentisch archiviert.
Die sechs Prozessoriginale wurden am selben Tag mit Codex Image Generation einzeln nach dem
freigegebenen Motivvertrag erzeugt. Alle Originale sind quadratisch; die Säulen messen
1254 × 1254, die Prozessmotive 1256 × 1256 Pixel.

| Original unter `docs/asset-originals/media/` | Zuordnung | Bytes | SHA-256 |
|---|---|---:|---|
| `pillars/pillar-future.png` | Zukunft — Rakete | 2.619.231 | `f1cf408ad75773f87564b3ebed2a83a0087557747e98bb6fcfa98503c14b57b4` |
| `pillars/pillar-relieve-suffering.png` | Leid lindern — gebende und empfangende Hand | 2.358.139 | `7839270a12c066d370be927d43104d16cd294be6e31f67cc38d39ad0e8ee53da` |
| `pillars/pillar-major-risks.png` | Große Gefahren — Atompilz | 2.562.631 | `6c17d338fec4fab8bb8fd911bf4ff8e2da7cbb053fab43c1eadd836b28d2fd6f` |
| `pillars/pillar-overlooked.png` | Was sonst übersehen wird — gefährdete Brücke | 2.676.957 | `e77f3f8f22dd38812af9f6e703e7995fe5c3a57152fd61e7c5bd2ff1b6a0890f` |
| `process/process-question.png` | Frage — Feder, Blatt und Fragezeichen | 2.584.674 | `094b326ff4a622b794d266ba6bcea852c254390a458621181bb7640374b7c9b0` |
| `process/process-evidence.png` | Belege — Lupe und drei geordnete Dokumente | 2.754.423 | `21a88ba92ea27483f672cd5f81cb84c7bda4e9eedf0e9baad53c7c2d9fb6a575` |
| `process/process-three-answers.png` | Drei Antworten — drei gleichwertige Pulte | 2.624.008 | `e941c332ca95a79798ce4d6ec4bd6035501768cb9b27beaa791d0cd03c96d9e3` |
| `process/process-reconsider.png` | Umdenken — Kopfprofil und Wendepfeil | 2.542.076 | `1be9a80d18335faaa08920d3b439c5d1db4506e248c50bfa2d9c58ca70d5d6d1` |
| `process/process-count.png` | Zählen — mechanisches Zählwerk mit drei Zuflüssen | 2.475.247 | `50491e4b0735fb3414b6de834dc6281edb70e67c645d20b03c22ea8a4cd06b7a` |
| `process/process-publish.png` | Veröffentlichen — offenes Protokoll und Siegel | 2.812.225 | `c4ddd295cbf4eb3df54913512dfc538fc1ec924a9b34fec427bda09e0023cd80` |

Für die UI wurden mit macOS `sips` 320 × 320 große JPEG-Anzeigederivate (Qualität 72)
erzeugt. Sie liegen semantisch gleich benannt als `*-display.jpg` unter
`site/static/media/pillars/` beziehungsweise `site/static/media/process/`, sind jeweils
25–31 kB groß und werden allein ausgeliefert. Die hochauflösenden Originale bleiben
außerhalb des Deploypfads.

| Deploytes Derivat | Bytes | SHA-256 |
|---|---:|---|
| `pillars/pillar-future-display.jpg` | 28.047 | `5e559bd783f05c327b6b8b5d402bfa7b9336092fbd0197a3b1288a15e16eb014` |
| `pillars/pillar-relieve-suffering-display.jpg` | 25.272 | `5fbd3ce0e690e5900b5817e651571d2956cf93bad738610e9de5c8136ed7baca` |
| `pillars/pillar-major-risks-display.jpg` | 25.165 | `40b3d5cd7eb2ed1e49c6ee50b28059fc61c4debfdada3eeb6e980d31323a1873` |
| `pillars/pillar-overlooked-display.jpg` | 29.502 | `7e427dabdba0dbd042bb42d004050ab75c36ce0d1921a72a95f42a8506481eec` |
| `process/process-question-display.jpg` | 27.124 | `b3ffd52e00a32e69106f2d7d0859129f148d0418ba833c3eb298dbf9ab8bafe4` |
| `process/process-evidence-display.jpg` | 27.418 | `23211fc8295e1b06ffab6059138aa4cf6ba6ed5dcd31266e14005bbf69688710` |
| `process/process-three-answers-display.jpg` | 26.261 | `78b3c3d13aa56473cb993af1eb0fe9d70b8088cd0ef19256307f1e9bccb18b0e` |
| `process/process-reconsider-display.jpg` | 28.419 | `42f16ba4e1302506fe7fc61fabc28e2b8250858a1078bc4b1781215b4492e0aa` |
| `process/process-count-display.jpg` | 28.440 | `7d69f2ac2b8e5973638013462998ca94bc0f9eb6caa845082a14f02d2c0d1146` |
| `process/process-publish-display.jpg` | 31.044 | `57e0c280470c61703328553e8785e365fa8ba8305f7cae0d86459b13fc020916` |

Die vier großen Szenenoriginale werden ebenfalls nicht direkt ausgeliefert. Unter
`media/scenes/` liegen 1600 × 900 große JPEG-Derivate (Qualität 78, 271–367 kB); unter
`media/scene-thumbnails/` zwei 640 × 360 große Vorschaubilder (41 bzw. 62 kB). Nur der
Ratssaal wird initial als große Szene geladen. Tür, Vorzimmer und Archiv werden erst beim
zugehörigen Zustand in den DOM eingesetzt. Die unveränderten PNG-Originale bleiben im Repo
(`docs/asset-originals/media/`) für Provenienz und spätere Neuableitungen erhalten, außerhalb
des Deploy-Pfads.
