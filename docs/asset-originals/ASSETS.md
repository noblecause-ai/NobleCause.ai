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

## Helleres Re-Rendering der Szenen + Tür-Motive (17.07.2026)

Für den Drei-Räume-Umbau (`feat/council-rooms`, siehe `docs/kimi-analysis.md`) hat der
Auftraggeber sechs neue, zusammengehörige Bilder bereitgestellt (ChatGPT-Generierung,
Dateinamen `ChatGPT Image 17. Juli 2026, 11_47_5x (n).png`): die vier Szenen als **hellere
Fassungen** (Mitteltöne angehoben, Motiv und Stil unverändert) sowie **zwei neue Tür-Motive**
im Hochformat — die bewusst weniger prunkvollen Archivtüren, die in den Szenen nicht
existieren. Alle sechs PNGs tragen eingebettete C2PA Content Credentials (`gpt-image`
v2.0, `digitalSourceType: trainedAlgorithmicMedia`; verifiziert per Strings-Scan, kein
`c2patool` verfügbar). Die Originale liegen außerhalb des Deploy-Pfads; die `sips`-Derivate
strippen die Credentials — bewusst in Kauf genommen, die Originale bleiben byte-identisch
archiviert.

| Original unter `docs/asset-originals/media/` | Rolle | ChatGPT-Datei | Maße | Bytes | SHA-256 |
|---|---|---|---:|---:|---|
| `doors/door-study-archive.png` | schlichte Archivtür aus dem Vorzimmer (A1) | `11_47_51 (1)` | 1086 × 1448 | 2.038.648 | `c72da79ffee4ac6b58435f49aa6095c1b7368c16505b2b4330c5b3c376192d82` |
| `doors/door-council-archive.png` | schlichte Archivtür aus dem Ratssaal (A2) | `11_47_51 (2)` | 1086 × 1448 | 1.987.066 | `a2d9752465661a0a48b21eb66116ad3e08c9037f66f5b1abe4f64b6c3c530ecd` |
| `scenes/antechamber.png` | Vorzimmer-Szene, hellere Fassung | `11_47_52 (3)` | 1672 × 941 | 2.608.611 | `b55406417e89d277547038f73b9843122f368297fd1d54d14ccd18d32146687d` |
| `scenes/hall.png` | Ratssaal-Szene, hellere Fassung | `11_47_53 (4)` | 1672 × 941 | 3.068.841 | `11204b4db503e3b28ba0e4d5fa0d52652befb7f10b801a7d1f3987797708b6d0` |
| `scenes/archive.png` | Archiv-Szene, hellere Fassung | `11_47_53 (5)` | 1672 × 941 | 3.112.948 | `259a847a4db0f41940f81c2bdd4d34d3d0574fa0a8557e8cfacdc2e92185e802` |
| `scenes/doorway.png` | Türöffnung-Szene, hellere Fassung | `11_47_54 (6)` | 1672 × 941 | 2.385.787 | `e6ba8d7eff32ade2edd8e83d3f98c2249aab78fea04d178b5f9e5e539bc2f40c` |

**Prompts/Quelle:** Die Tür-Motive folgen der Spezifikation A1/A2 in
`docs/kimi-analysis.md` §5 (schlichte Holztür zwischen Karteischränken mit Wandlämpchen
bzw. unauffällige Seitentür zwischen Steinsäulen mit Bernstein-Lichtfuge; Hochformat 3:4,
ruhige Label-Zonen, keine Schrift im Bild, hellere Mitten als der Bestand). Die vier
Szenen sind hellere Re-Renderings der bestehenden Motive; ihr Promptwortlaut ist nicht
überliefert, die Zuordnung wurde vom Auftraggeber visuell bestätigt (17.07.2026).

**Derivate (einzige ausgelieferte Dateien):** Türen 480 × 640 JPEG q80; Szenen
1600 × 900 JPEG q70 (hellere Bilder komprimieren schlechter — q70 hält das Deploy
leicht); Thumbnails 640 × 360 JPEG q72, aus den neuen Szenen (neu) abgeleitet — neben den
bislang vorhandenen zwei nun alle vier Szenen, weil die Tür-Kacheln der Räume auch auf
Ratssaal und Türöffnung verweisen.

| Deploytes Derivat | Bytes | SHA-256 |
|---|---:|---|
| `doors/door-study-archive-display.jpg` | 64.975 | `7ec2d60e753b3848c0e3ff7a118dfca7927f5cc8722ca586fe911a7883077ba4` |
| `doors/door-council-archive-display.jpg` | 53.598 | `d37f2e5e12bc1827be397489a88a7a84416766e219bba23027b662a5d598cd9e` |
| `scenes/antechamber-display.jpg` | 400.117 | `39a3bdc8aa76268342092e12f8ee0e595dc24cf3b6082add7cf01f184c974be6` |
| `scenes/hall-display.jpg` | 492.733 | `9952dc999c287ec2711d7125d80ca89a413ce5e427a4bdb64718b5e5c27c613c` |
| `scenes/archive-display.jpg` | 592.787 | `66c7fb94a32b9f30292829da07500262b7e7827cd1c475564b34f96ce6cfd210` |
| `scenes/doorway-display.jpg` | 356.294 | `9c64c79a1515ed889074746109e2fabcf7b624e215a921fa91c4622c07aaf693` |
| `scene-thumbnails/antechamber-display.jpg` | 66.907 | `71561d22901d2293c435569a63e9e32392498fea4bcd1275e720f77627916139` |
| `scene-thumbnails/archive-display.jpg` | 107.562 | `1dba443c65c1c266f5d0f8e27c07f81124d6eec4a12946e47e84a600084adf29` |
| `scene-thumbnails/hall-display.jpg` | 84.814 | `7d11254ea61683d0dbb091b06c470b0ad1f4357ed73b08a8ed201d26c85fb34c` |
| `scene-thumbnails/doorway-display.jpg` | 65.241 | `bf6fb696b8bca319bda1f7beda0166a683ea40d8721daca05c97eee2a9c11af1` |

**Ruhestand der dunklen Fassungen:** Die vier bisherigen Szenen-Derivate (Qualität 78
bzw. 55) und die beiden alten Thumbnails wurden am 17.07.2026 durch die helleren Fassungen
ersetzt und liegen als Provenienz unter
`docs/asset-originals/media/provenance/scenes-display-v1/` (die beiden Thumbnails dort als
`*-thumbnail.jpg`, da die Dateinamen mit den Szenen kollidieren). Ihre PNG-Originale
(`council-machine.png`, `council-door.png`, `antechamber-final.png`, `archive-final.png`)
bleiben unverändert an ihrem dokumentierten Ort. Ausgeliefert wird nichts davon.

**Bekannte Einordnung:** `door-council-archive` ist das dunkelste der sechs Bilder
(obere Bildhälfte fast Schwarz); die Anklickbarkeit der Tür wird in der UI daher über
Rahmen/Beschriftung der Tür-Kachel getragen, nicht über das Bild allein.

## Farbige Embleme (v2) + Rückkehr zu dunklen Szenen (17.07.2026, zweiter Pass)

Nach Sichtung des helleren Re-Renderings entschied der Auftraggeber: Die Aufhellung der
Szenen war zu viel — die Farbe soll aus den **Emblemen** kommen, nicht aus den Plates.
Deshalb liefert derselbe Tagesdurchgang zehn **farbige Emblem-Motive** (ChatGPT-
Generierung, Dateinamen `ChatGPT Image 17. Juli 2026, 16_*_*.png`, je 1254 × 1254,
eingebettete C2PA Content Credentials — `jumb`/`c2pa`-Marker per Strings-Scan verifiziert).
Sie ersetzen die unbunten Erstfassungen **unter denselben Slot-Dateinamen**; am Code
ändert sich nichts.

| Slot | Motiv | ChatGPT-Datei | Status |
|---|---|---|---|
| `pillar-future` | rote Rakete | `16_42_03` | eingebaut |
| `pillar-major-risks` | blauer Atompilz | `16_42_24` | eingebaut |
| `pillar-relieve-suffering` | orange Hände | `16_44_27` | eingebaut |
| `pillar-overlooked` | Auto auf Brücke | `16_49_04` | eingebaut (17.07.2026, zweiter Pass — vom Auftraggeber bestätigt: das Motiv steht für übersehene Gefahren, z. B. Verkehrssicherheit) |
| `process-question` | blaues Fragezeichen | `16_48_49` | eingebaut |
| `process-evidence` | Lupe über Dokumenten | `16_42_44` | eingebaut |
| `process-three-answers` | drei Pulte | `16_43_02` | eingebaut |
| `process-reconsider` | Umdenken-Kopf | `16_43_18` | eingebaut |
| `process-count` | Abakus | `16_43_36` | eingebaut |
| `process-publish` | Buch mit Siegel | `16_44_43` | eingebaut |

**Originale (Provenienz, nicht Deploy):** `provenance/emblems-v2/<slot>.png`, slot-benannt.

| Original unter `provenance/emblems-v2/` | SHA-256 |
|---|---|
| `pillar-future.png` | `d7f614c4830c13cf5e31ed69311d975c52b797a9b4a458e034cb38d36321a5d3` |
| `pillar-major-risks.png` | `030616e5db51517152a20d68ee54d420933064c2dbcd4017264e786108face07` |
| `pillar-relieve-suffering.png` | `d9eb2b79796a000f9ab6f1667d7f68a0eb0d3d768d90462b0def318f5e40fb6f` |
| `pillar-overlooked.png` | `bee51c008acba4b057e8f235cae539ecdd3e5639f1bfe99d805895de291ffb9f` |
| `process-question.png` | `7e9b14b4c8bd21cb2eaeee1e8182266ac7f005f6b64c35407d0fcef752cd0c7a` |
| `process-evidence.png` | `3532dec803fb7e59d7917e035e31ad03fc59cd265533156a6603401a6d1523d9` |
| `process-three-answers.png` | `06a4141b95aa14d321732254166e01b85cf0b9b7e0b3d8b485c0b744acc8f6f1` |
| `process-reconsider.png` | `b0fb16aa7d43a106843725b8ddc8fd7d58f3310893ba59d344553f1a5533b298` |
| `process-count.png` | `1050ab95d812ce6276e71045934eb4d2a2bffcb6e824ebb2da17ce245a668657` |
| `process-publish.png` | `5ac014d756db43450cb04fb2d26b4bebeed76473257bd1897cbf07447b7f03ba` |

**Derivate (einzige ausgelieferte Dateien):** wie bisher 320 × 320 JPEG q72 via `sips`,
gleiche Slot-Namen. Lesbarkeit auf einem Kontaktbogen bei 120 px **und 32 px** gesichtet:
alle zehn Motive (inkl. des zurückgestellten) sind bei 32 px eindeutig erkennbar.

| Deploytes Derivat | Bytes | SHA-256 |
|---|---:|---|
| `pillars/pillar-future-display.jpg` | 27.845 | `ff52a62f52d52f0bfcbeebc8a6268ebd56026bdb4705f652f26881b005679a27` |
| `pillars/pillar-major-risks-display.jpg` | 25.647 | `97fd3340437373dc23881ceff2c340557356abd35df355854afe24474198ddfe` |
| `pillars/pillar-relieve-suffering-display.jpg` | 28.708 | `14e8b79eed6942ed639a03c96e744dc0b3aaeb0a94580737cb682437329473e9` |
| `pillars/pillar-overlooked-display.jpg` (Nachtrag 17.07.2026, bestätigt) | 29.930 | `791fe51136719d99c6c79424c9e9ff70e4ad06055b1748ce210f20f9135937d7` |
| `process/process-question-display.jpg` | 34.638 | `7d7fd4dca39191db421d8726d3b73d12e5d6335d8e72f85c3124029e0633ddb6` |
| `process/process-evidence-display.jpg` | 42.217 | `06a3246d38e5983bffbaf0164c9e801d3c022e84c41d1de7440f7b7e03761de0` |
| `process/process-three-answers-display.jpg` | 17.632 | `40a62a7bcf12865f15932e4a4f53d77b8755cfe32e8bd75b4d557a7d2a4b5a33` |
| `process/process-reconsider-display.jpg` | 38.740 | `bb7b5f09e5bc79f031c20666a0bae42adde782d9dcbacff9ad15d412602c1eb1` |
| `process/process-count-display.jpg` | 19.575 | `c1c8591928f17aae861896daf8d9bde003f8895120afb4c26c151741a207f2e2` |
| `process/process-publish-display.jpg` | 33.794 | `f8b036d880c9cae36a740e30727d8d68b4ec560428d50a14f5f75b7736085802` |

**Szenen zurück auf dunkel:** `scenes/antechamber-display.jpg` und
`scenes/hall-display.jpg` wurden auf die dunklen Erst-Derivate aus
`provenance/scenes-display-v1/` zurückgesetzt (byte-identisch kopiert); dasselbe gilt für
`scene-thumbnails/antechamber-display.jpg` (v1 `antechamber-thumbnail.jpg`). Das
Hall-Thumbnail existierte in v1 nicht und wurde neu aus dem v1 `hall-display.jpg`
abgeleitet (640 × 360 JPEG q72). `doorway` und `archive` bleiben **bewusst** in der
helleren v2-Fassung (In-Szene-Tür und Übergänge sind ein separater Pass). Die abgelösten
hellen Fassungen von Vorzimmer und Ratssaal liegen als Provenienz unter
`provenance/scenes-display-v2-hell/` und werden nicht ausgeliefert. Die Tafel-Zone des
dunklen Vorzimmer-Plates wurde nach dem Tausch per Screenshot gegengeprüft: Das
Ergebnis-Overlay (Position unverändert, `StudyRoom.svelte`) sitzt weiter auf der
Schiefer-Zone — keine Justage nötig.

| Wieder aktives Derivat | Bytes | SHA-256 |
|---|---:|---|
| `scenes/antechamber-display.jpg` | 270.866 | `e87c0513d0e1136d43ac73c838a8893622029d40c0ad59aef9984a8da76ff8f1` |
| `scenes/hall-display.jpg` | 199.308 | `92032b5441b080375ce1feaec6e2cf3262b349ac04a5694813084d5b0b5f2274` |
| `scene-thumbnails/antechamber-display.jpg` | 41.460 | `9fadeeb4e4c1cff7eda8ae466bc6248a861ac5f3eca4979f5929bccaefd4519e` |
| `scene-thumbnails/hall-display.jpg` (neu abgeleitet) | 50.608 | `02dd1dee9b94fd95b387b7396889b65b8564aec0a727c50b4e9b291b29c7eeaf` |

## Vorzimmer v3 — volles Original-Frame, zwei Wart-Zustände (18.07.2026)

Der Auftraggeber lieferte zwei neue Vorzimmer-Plates (`ChatGPT Image 18. Juli 2026,
19_49_56.png` / `19_50_47.png`, je 1915 × 821, C2PA-Marker per Strings-Scan
verifiziert). Befund: `19_50_47` („Wart wach", beide Figuren wach) ist
**byte-identisch mit dem historischen Original `provenance/vorraum.png`** — das
bisherige 16:9-Display war ein Ausschnitt dieses Frames; v3 stellt die Darstellung
auf das volle Original-Frame um. `19_49_56` zeigt dieselbe Szene mit einer
**schlafenden** Gestalt („Wart schlafend") und ist ohne Design-Vorgabe für einen
Zustandswechsel **nicht eingebunden** — archiviert, Entscheidung offen gemeldet.

| Original unter `docs/asset-originals/media/` | Rolle | ChatGPT-Datei | Maße | SHA-256 |
|---|---|---|---:|---|
| `scenes/antechamber-v3-wart-wach.png` | **Standard-Plate** (byte-identisch mit `provenance/vorraum.png`) | `19_50_47` | 1915 × 821 | `0e02cc4dfa508dc9d29e71325442fc8bbf3ad2b4903a2b0d9a74388cf2d79b56` |
| `scenes/antechamber-v3-wart-schlafend.png` | Variante „schlafend" — nicht eingebunden | `19_49_56` | 1915 × 821 | `f5f9d4a8a181e2457ef144e131fad82273cea8a9e2157c78169aa6e88381b6bb` |

**Derivate (einzige ausgelieferte Dateien):** wegen des breiteren Frames
(1915:821 ≈ 2,33:1) ändert sich das Anzeige-Ratio: Display 1600 × 686 (JPEG q70),
Thumbnail 640 × 274 (q72) — gleiche Slot-Namen; die Thumbnail-Maße wurden in den
Tür-Karten der Locales (`council.doors`/`archive.doors`, de+en) angepasst. Das
bisherige 16:9-Display ruht unverändert in `provenance/scenes-display-v1/`.
Die Doppeltür rechts im Bild (Zone ≈ x 86–100 %, y 5–82 %) trägt den
In-Szene-Hotspot nach The Council.

| Deploytes Derivat | Bytes | SHA-256 |
|---|---:|---|
| `scenes/antechamber-display.jpg` | 203.211 | `4a4f8ee80d6e62d9995ef23aa042a1110a5e58dc43aa75d4976f94f95114bae8` |
| `scene-thumbnails/antechamber-display.jpg` | 38.622 | `881e725b6e1ddde6515d3ac6fdb8cddb844701d04f6fd22c42b3895ed2f66163` |

**Wieder referenziert (18.07.2026, Korrektur 2):** Die Ablauf-Leiste der Study stellt
wieder **alle sechs kanonischen Schritte** dar (Frage → Belege → Drei Antworten →
Umdenken → Zählen → Veröffentlichen). `process/process-question-display.jpg` und
`process/process-reconsider-display.jpg` wurden per `sips -z 320 320 -s format jpeg
-s formatOptions 72` aus `provenance/emblems-v2/` neu abgeleitet und liegen wieder in
`site/static/` — **byte-identisch** mit den historischen Derivaten (Hashes s. Tabellen oben:
question `7d7fd4dc…`, 34.638 B; reconsider `bb7b5f09…`, 38.740 B).

## Hochformat-Plates für Mobil (18.07.2026, Korrektur 2)

Zwei finale Hochformat-Szenen (je 1024 × 1536, 2:3, C2PA-Marker per Strings-Scan
verifiziert) für die quellenabhängige Bildebene: Querformat ≥ 1200 px Viewport,
Hochformat darunter. Die Bildebene steht auf `object-fit: cover` — das Hochformat
begrenzt den Cover-Verlust auf schmalen Viewports.

| Original unter `docs/asset-originals/media/` | Rolle | ChatGPT-Datei | SHA-256 |
|---|---|---|---|
| `scenes/antechamber-portrait.png` | **The Study, Mobil-Plate** — leere Tafel oben (Board-Fläche, Zone ≈ x 7–56 %, y 20–49 %), Protagonist mit grüner Lampe unten | `18. Juli 2026, 20_35_45 (1)` | `07527a3cf655326ad20f9d14467486f98a77ea5973346a0ca00f0c90fda98b2e` |
| `scenes/archive-portrait.png` | **The Archive, Mobil-Plate** — Prunkschrank rechts (x ≈ 35–97 %), dunkle Textspalte links | `18. Juli 2026, 20_35_46 (3)` | `076c9a6aa16c8c582c548b55732ef879b0dc60282a119be68aac8917b1246848` |

Nicht eingebunden: `20_35_45 (2)` (Ratssaal-Hochformat) ist laut Auftraggeber ein
**Draft** — unberührt, kein Archiv-Eintrag; der Ratssaal nutzt vorerst überall die
Querformat-Plate (`sceneMobile`-Slot im RoomHero ist gebaut, später nur Datei + Prop).

**Derivate (einzige ausgelieferte Dateien):** native 1024 × 1536, JPEG q72 — die
Quelle liefert nicht mehr Auflösung; Hochskalieren verworfen.

| Deploytes Derivat | Bytes | SHA-256 |
|---|---:|---|
| `scenes/antechamber-portrait-display.jpg` | 235.984 | `058130470964bf9eb5d443736c0884f7f407090b3f08b9b6fd08308b0fd893a8` |
| `scenes/archive-portrait-display.jpg` | 354.127 | `fe0672e50a3ef18ebad434db5066509a4a2e77921330175fe1d5df3349bbc39d` |
