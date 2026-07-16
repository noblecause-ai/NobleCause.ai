# Bildassets der Startseite

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

Die folgenden zehn Originale wurden am 16.07.2026 byte-identisch aus `docs/` übernommen.
Die Arbeitskopien bleiben bis nach dem Review erhalten. Alle Originale messen 1254 × 1254
Pixel. Die Zuordnung folgt dem sichtbaren Motiv, nicht der ursprünglichen generischen
Exportnummer.

| Produktiver Pfad | Quelldatei unter `docs/` | Zuordnung | Bytes | SHA-256 |
|---|---|---|---:|---|
| `process/question.png` | `ChatGPT Image 16. Juli 2026, 08_57_14 (1).png` | Frage | 2.191.992 | `501d240c863f86cc5a3fd7bc41ef10b799aba682cabd5b32bda985f71d445bb4` |
| `process/evidence.png` | `ChatGPT Image 16. Juli 2026, 08_57_15 (2).png` | Belege sammeln | 1.946.744 | `1aa3a30548291539ff3b209d1521d2781b2e72ec46841d1c8eab1ddcf13f9416` |
| `process/three-answers.png` | `ChatGPT Image 16. Juli 2026, 08_57_15 (3).png` | Drei Antworten | 2.312.377 | `d7cf4ca61fa378f009350c4af31877c6b85a8241de83d1b974d0051b09b2146f` |
| `process/review-and-revise.png` | `ChatGPT Image 16. Juli 2026, 08_57_16 (4).png` | Gegenlesen und Umdenken | 1.964.180 | `199f6d9e5df3b8f83037faf7ffc1a04f77f1d402702e94cdf6d7735d965a763c` |
| `process/count.png` | `ChatGPT Image 16. Juli 2026, 08_57_16 (5).png` | Zählen | 1.889.574 | `581991c48f5975ea306e6fa84d27f430d670f883262e19c19df176dfceef2556` |
| `process/publish.png` | `ChatGPT Image 16. Juli 2026, 08_57_16 (6).png` | Veröffentlichen | 1.951.028 | `1c658573cdcb2068d8ca74bc63440845d903c5251d32b2e19f4af589e29eb373` |
| `pillars/future.png` | `ChatGPT Image 16. Juli 2026, 08_57_17 (7).png` | Investition in die Zukunft | 1.837.691 | `2c7190b8e17ba057fe68837f918c3768b2fc04745975a1a3cb73f09f20011830` |
| `pillars/suffering.png` | `ChatGPT Image 16. Juli 2026, 08_57_17 (8).png` | Linderung von Leid | 2.295.159 | `9fec5a51c2882f1dc3978861a8032bf2cc2e9c93be27192886e5d0fc3f3b1401` |
| `pillars/global-risks.png` | `ChatGPT Image 16. Juli 2026, 08_57_17 (9).png` | Schutz vor großen Gefahren | 2.175.640 | `9de7cca7e63e0a8abd8dc38dbea6c9c7b9ee38a8e402129902fa48a07e5f7d46` |
| `pillars/overlooked.png` | `ChatGPT Image 16. Juli 2026, 08_57_17 (10).png` | Übersehenes | 1.997.834 | `51449a110b65f4b51fab3b75eb741057e0e2d6682dda43d8251bf5372e59d705` |

Für die nur 34–43 CSS-Pixel großen UI-Motive wurden mit macOS `sips` 320 × 320 große
JPEG-Anzeigederivate (`*-display.jpg`, Qualität 72) erzeugt. Sie sind je 17,6–20,2 kB groß;
die Seite lädt ausschließlich diese Derivate und nicht zusätzlich die rund 20,6 MB großen
Originale. Die Originale bleiben als unveränderte Provenienz- und Reviewartefakte im
produktiven Assetpfad erhalten.

Die vier großen Szenenoriginale werden ebenfalls nicht direkt ausgeliefert. Unter
`media/scenes/` liegen 1600 × 900 große JPEG-Derivate (Qualität 78, 271–367 kB); unter
`media/scene-thumbnails/` zwei 640 × 360 große Vorschaubilder (41 bzw. 62 kB). Nur der
Ratssaal wird initial als große Szene geladen. Tür, Vorzimmer und Archiv werden erst beim
zugehörigen Zustand in den DOM eingesetzt. Die unveränderten PNG-Originale bleiben daneben
für Provenienz und spätere Neuableitungen erhalten.
