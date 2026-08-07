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

## Serie 1 · The Study — Bühnenspiel-Plates (20.07.2026)

Sechs Master aus der Bestellung `docs/codex-serie-1-study.md` (Aufträge 1–6), Gate
`docs/review/serie-1-gate/`: Kontaktbogen §7 **bestanden** für die vier Plates
(Farbtemperatur, Schwarzpunkt, Messing, Mondblau, Pinselstil, Perspektive, Tür-/Tafel-
und Fensterwirkung konsistent; A↔B nur Türzustand; quer↔hoch eigenständige Komposition).
Kompositions-Grammatik erfüllt: **Tür zentral (±5 %), Tafelzone links frei, Mondfenster
rechts, ruhige dunkle untere Textzone, kein Text.** C2PA-Marker je Datei per
Strings-Scan verifiziert (gpt-image).

| Original unter `docs/asset-originals/media/provenance/serie-1-study/` | Rolle | Maße | Bytes | SHA-256 |
|---|---|---|---:|---|
| `study-plate-a-desktop.png` | **Study Plate A quer** — Tür geschlossen | 1672 × 941 | 1.672.545 | `323579821207983fec83be0fde86f506c8ea72be9b53e12d895fb67963aa0f39` |
| `study-plate-b-desktop.png` | **Study Plate B quer** — Tür offen (Spalt, warmer Durchblick) | 1672 × 941 | 1.589.921 | `8acadfe99c052ecc2d13f73f470752e372f3833455567cea2e2ee2cefe2e6c0a` |
| `study-plate-a-mobile.png` | **Study Plate A hoch** — Tür geschlossen | 1024 × 1536 | 1.994.828 | `acecc5551c9654ed5df87f05c117962f7059d72400372291f6707b8bd8ed5c86` |
| `study-plate-b-mobile.png` | **Study Plate B hoch** — Tür offen | 1024 × 1536 | 1.887.147 | `886b05b93a9bc459ed519b004048d05a1ff18e25cfba2bfffac00ba3fa7b300d` |
| `scout-cutout.png` | **The Scout** — Figur + Stehtisch (⚠ weißer Grund, **kein Alpha** → Nachbestellung, siehe unten) | 1024 × 1536 | 1.403.852 | `f97260af645f5cf45df3efb5c051eb35777637bc01536c165686d21cef3228b4` |
| `warden-cutout.png` | **The Warden** — Figur + Schreibtisch (⚠ weißer Grund, **kein Alpha** → Nachbestellung) | 1024 × 1536 | 1.532.698 | `52f39050786efa3506f3efbb50036ecefdf1cc822d0c723b442cf3c4ae8ecdc7` |

**Cutout-Maße (% der Bildhöhe, Auflage aus dem Horizont-Test, gilt auch für die
Nachbestellung):** Scout Augenhöhe ≈ 13 %, Tischoberkante ≈ 42 %, Fußlinie ≈ 87 % ·
Warden Augenhöhe ≈ 15 %, Tischoberkante ≈ 53 %, Fußlinie ≈ 88 %.

**Alpha-Abweichung (5/6):** stilistisch bestanden, technisch ohne Alpha-Kanal geliefert
— **nicht eingebaut**, Nachbestellung mit unverändertem Motiv + Alpha-Auflage:
`docs/review/serie-1-gate/nachbestellung-cutouts.md` (Fallback-Formulierung chroma-grün).
Die gelieferten PNGs bleiben als Stil-/Posereferenz archiviert.

**Derivate (AVIF gewann 8/8 gegen WebP q80; `avifenc -s 6 -q 55`):** Plate A ersetzt die
bisherigen `antechamber-*`-Slots (gleiche Dateinamen, keine Code-Umstellung); Plate B
und die Tür-Crops liegen als **unverdrahtete Slots** für die künftige Lock-/Peek-
Choreografie bereit. Ersetzte AVIFs der hellen Fassung werden nicht separat archiviert —
Quellfassung und Master liegen bereits in `provenance/scenes-display-v2-hell/` bzw.
`vorraum.png`.

| Deploytes Derivat (`site/static/media/`) | Maße | Bytes | SHA-256 |
|---|---|---:|---|
| `scenes/antechamber-display.avif` | 1600 × 900 | 44.191 | `26403587bb2bf3e22bc42c3ab558da8b2f63bc394a92462be61fa652b78ff7ea` |
| `scenes/antechamber-portrait-display.avif` | 1024 × 1536 | 62.962 | `448c03038b890b0f946bffb200fc44d41efc67f135be9cdcf7cab7fb156b7145` |
| `scenes/antechamber-portrait-800.avif` | 800 × 1200 | 36.239 | `351cdb432c298d4a8f87266e63d83564462606ef81022d044a3d343f7b0abbd9` |
| `scenes/antechamber-b-display.avif` (Slot, unverdrahtet) | 1600 × 900 | 43.976 | `890c90f25fea20cb1842818c50913341f32d88d8eeadce7831ed191a0d8ea364` |
| `scenes/antechamber-b-portrait-display.avif` (Slot) | 1024 × 1536 | 56.449 | `33490838feefe0126cc73e98210fa4e7c8500a13634f6a2cd6cf1978abb3527e` |
| `scenes/antechamber-b-portrait-800.avif` (Slot) | 800 × 1200 | 33.388 | `284996aa65255cd33a2545713868fb752d8220107df181ab98922874b0910fdb` |
| `doors/study-door-crop-quer.avif` (Slot, sips-Crop aus Plate A quer) | 385 × 640 | 10.600 | `42f2ddd5823650ce8939c035c971565396f2d003e85bf7459e94a87e6724020c` |
| `doors/study-door-crop-hoch.avif` (Slot, sips-Crop aus Plate A hoch) | 300 × 476 | 7.949 | `170a621aebd3c3e66bcaf98b830fbc7a4e6be44ff9b4539e08d1af219432a8ba` |

## Serie 1b · The Study — Nachbestellung (20.07.2026)

Sieben Master aus der Bestellung `docs/codex-serie-1b-study-nachbestellung.md`
(ersetzt die Serie-1-Cutouts mit weißem Grund sowie die Plates mit gemalten Tischen),
Gate `docs/review/serie-1b-gate/`. C2PA-Marker 7/7 per Strings-Scan verifiziert
(gpt-image), formal kein Alpha-Kanal (0/7 — erwartet, Freistellung aus gemaltem
Schachbrett-Hintergrund).

**Gate-Stand: Kontaktbogen §8 STILISTISCH BESTANDEN (7/7)** — eine Welt mit Serie 1,
A↔B deckungsgleich nur Türzustand, quer↔hoch eigenständige Komposition, Tische
entfernt, Pflanzen gedämpftes Grün, Tafel frei, Scout als Rechercheur am Schreibtisch
(leuchtender Schirm im Messingrahmen). Schirm enthält unleserliche Pseudotext-
Strichzeilen — bei Anzeigegröße ≤ 600 px reine Textur, kein Vertragsbruch (Vermerk in
`checks.txt`). **Freistellung der Cutouts an der Hintergrund-Spezifikation
GESCHEITERT** (weiß/hellgrau-Schachbrett kollidiert mit hellen Motiv-Pixeln,
Farbdistanz 0; Generator malte Lichtschein um Schirm/Lampe und Bodennebel mit —
kein Farb-Key möglich): **Nachbestellung der zwei Cutouts empfohlen**, Details in
`docs/review/serie-1b-gate/` (Bericht + `checks.txt`). Wolke: Kachel-Naht nicht
nahtlos (MAD 9, max 45) — verwendbar mit Ping-Pong-Drift statt Endlos-Loop.
**Keine Derivate, kein Einbau in diesem Gate** — folgt nach Steward-Freigabe.

| Original unter `docs/asset-originals/media/provenance/serie-1b-study/` | Rolle | Maße | Bytes | SHA-256 |
|---|---|---|---:|---|
| `study-plate-a-desktop.png` | **Study Plate A quer** — Tür geschlossen, ohne Tische, Pflanzen | 1672 × 941 | 1.680.137 | `f4f4310589a77a4653e9100eee2c6e5fd11cf82787d5053a006f97b3e20095c9` |
| `study-plate-b-desktop.png` | **Study Plate B quer** — Tür offen | 1672 × 941 | 1.658.383 | `36fded2a0557116d3aa119ad958eff7a283ffc713e9a96b035141b589286975d` |
| `study-plate-a-mobile.png` | **Study Plate A hoch** — Tür geschlossen | 1024 × 1536 | 1.893.693 | `d91de3cfd6d8a53bca03b1b5b580dae8da046496439aab2392c9d07b2be483c8` |
| `study-plate-b-mobile.png` | **Study Plate B hoch** — Tür offen | 1024 × 1536 | 1.798.679 | `1e650d0aac8eb5262d9ac4a4418a1df536d411a7a158693cc41beef6f39423ea` |
| `scout-cutout.png` | **The Scout** — Rechercheur am Schreibtisch, Schirm (⚠ Schachbrett hell, Lichtschein/Boden mitgemalt → Nachbestellung empfohlen) | 1024 × 1536 | 1.704.583 | `88d2d2ce865373b15cbf263b959f07ec0c5f5d4dc7601f2fd8707eb4e4884b0f` |
| `warden-cutout.png` | **The Warden** — am Pult (⚠ Schachbrett hell, Bodennebel mitgemalt → Nachbestellung empfohlen) | 1024 × 1536 | 1.517.210 | `20dfbf61377dafe5a978a91dcb633b3fdf44a766193574715ff65f8905d0dda4` |
| `clouds-layer.png` | **Wolkenzug-Ebene** — für Mondfenster-Ambient (Naht MAD 9/max 45 → Ping-Pong-Drift, kein Endlos-Loop) | 1536 × 1024 | 1.540.598 | `dccfe8d1ef36d5218148cfb5001c5652138e3e3161c73321ceb4b63b9e0c0e93` |

**Cutout-Maße (% der Bildhöhe, aus der Montage-Probe, ±1,5 % — Auflage gilt auch für
die Cutout-Nachbestellung):** Scout Augenhöhe ≈ 21 %, Tischoberkante ≈ 47 %,
Fußlinie ≈ 74 % · Warden Augenhöhe ≈ 21 %, Pult-Oberkante ≈ 43 %, Basislinie
(Pult-Sockel) ≈ 67 %. Köpfe beider Figuren beginnen ≈ 14 % — Ausrichtung im Plate
über diese Anker, nicht über die Bildunterkante.

## Serie 1c · The Study — Cutout-Nachbestellung 2, Magenta-Backdrop (20.07.2026)

Zwei Master aus der Bestellung `docs/review/serie-1b-gate/nachbestellung-cutouts-2.md`
(absichts-basierter Prompt: unbeleuchtete Magenta-Fotowand statt Motiv-Beschreibung),
Gate `docs/review/serie-1c-gate/`: **BESTANDEN (5/5)** — Backdrop flach (Eck-SAD 5,
Hub < 3,5, Band 100 % rein), Motiv-Masse beginnt erst ab SAD ~240 (Histogramm), Key
T=100 kollisionsfrei, Motiv-Konstanz zu 1b deckungsgleich, C2PA 2/2 (gpt-image).
**Lösen die 1b-Cutouts ab** (1b-Master bleiben als Stilreferenz archiviert).
**Kein Einbau in diesem Gate** — Derivate (Alpha-AVIF/WebP aus der dokumentierten
v5-Kette) + Einbau folgen nach Steward-Freigabe.

| Original unter `docs/asset-originals/media/provenance/serie-1c-study/` | Rolle | Maße | Bytes | SHA-256 |
|---|---|---|---:|---|
| `scout-cutout.png` | **The Scout** — Rechercheur am Schreibtisch, leuchtender Schirm, Magenta-Backdrop | 1024 × 1536 | 1.682.203 | `55f84c0a9306154740d238e808a48e99c77eb1538417f709a28f4d9d093c5873` |
| `warden-cutout.png` | **The Warden** — am Pult, Magenta-Backdrop | 1024 × 1536 | 1.608.613 | `00c3f4ed3133cc06421ed041757862872f8cbdf312a69531c9ff55781b24da13` |

**Freistell-Pipeline (dokumentiert in `docs/review/serie-1c-gate/checks.txt`, Skripte
/tmp — flüchtig, bei Einbau neu laufen lassen):** globaler Distanz-Key SAD ≤ 100 →
Loch-Klassifikation (Nicht-Rand-Key-CCs füllen nur bei size < 100 oder meanSad > 15 —
echte Durchsichten hinter Schirm-Gestell/Tischbeinen bleiben offen) → 1-px-Erode →
Despill-Sweep (opake Magenta-Cluster SAD ≤ 220, < 3000 px, entfernen). Ergebnis:
Magenta-Rest 0 px, Montage auf Plate A ohne sichtbare Kante. Gelernte Falle:
**Loch ≠ Loch** — pauschales Füllen aller Nicht-Rand-Komponenten holt Durchsichten
als Magenta-Flächen ins Motiv zurück.

**Cutout-Maße 1c (% der Bildhöhe, v5-Alpha-BBox):** Scout Kopf 13,9 % / Fuß
(Tisch-Strebe) 85 % · Warden Kopf 16,1 % / Pult-Basis 81 %. Augenhöhe beide ≈ 21 %
(Vollbild-Sichtung, ±1,5 %). **Achtung:** kein Bodennebel mehr — Platzierungs-Anker
ist die BBox-Unterkante (85/81 %), nicht die 1b-Fußlinie (74/67 %).

### Serie 1c — Derivate und Einbau (20.07.2026, nach Steward-Freigabe)

| Deploytes Derivat (`site/static/media/`) | Maße | Bytes | Quelle |
|---|---|---:|---|
| `actors/scout.avif` | 540 × 810 (Alpha) | 24.922 | v5-Kette aus `serie-1c-study/scout-cutout.png`, AVIF q55 (gewann vs WebP 36.092) |
| `actors/warden.avif` | 540 × 810 (Alpha) | 19.505 | v5-Kette aus `serie-1c-study/warden-cutout.png`, AVIF q55 (WebP 26.800) |
| `ambient/clouds-study.avif` | 384 × 512 | 10.536 | mittleres Band (768×1024 ab x=384) aus `serie-1b-study/clouds-layer.png`, AVIF q55 (WebP 11.622) |

Dimensionierung nach MP-Nachmessung heruntergesetzt (geplant 600×900/576×768 —
Deckel-Logik in `docs/asset-budget.md` §5 Nachtrag 20.07.): Akteure 540×810
(0,44 MP; Anzeige 42svh ≈ 378 px, DPR2-Deckung 756 ≤ 810), Wolke 384×512
(0,20 MP, Ambient-Blur).

**Nebenbefund — Embleme re-dimensioniert (gleicher Pass, MP-Deckel):** alle zehn
Embleme aus `provenance/emblems-v2/` neu abgeleitet 320² → **160²** (Anzeige ≤ 64 px,
DPR2 = 128). AVIF gewann 9/10; `process-three-answers-display` ist jetzt **.webp**
(1.164 B < 1.495 B — Referenzen in `de.js`/`en.js` und der Testliste angepasst).
Gesamt 83 KB → 30 KB, 1,02 MP → 0,26 MP. Masters unverändert; Re-Derivation jederzeit
möglich. Schärfe am gebauten Artefakt gesichtet (Tafel + Röhre).

## Wolken-Ebene — Freistellung statt Nachbestellung (23.07.2026)

Bug `docs/bug-wolken-raster-und-scroll.md` Befund 1: das bisherige Derivat war RGB
ohne Alpha, das „Transparenz"-Schachbrett des Masters leuchtete als Raster über der
Szene. Steward-Freigabe (Neugenerierung ODER Freistellung, Entscheidung bei Kimi) —
Weg: **Freistellung des 1b-Masters** (Chroma-Key auf Bläulichkeit, weiche
Alpha-Rampe), weil das Motiv hell auf flachem neutralen Schachbrett liegt.

Kette (`clouds-layer.png`, unverändert in Provenienz): RGB σ8-Blur (das Schachbrett
schlug durch die halbtransparent gemalten Wolken und sass als Luminanz-Raster IM
Wolken-RGB) → Bläulichkeit `B−(R+G)/2`, σ10-geblurrt (Kachel ist Hochfrequenz und
mittelt sich weg; Wolken sind grossflächig) → smoothstep-Key t0=8/t1=22 → Feder σ1,2
→ 3:4-Center-Crop (768×1024 ab x=384) → Lanczos 384×512 RGBA. Encoder-Duell:
AVIF q60/qalpha60 (16.472 B) schlug WebP q85 (43.532 B).

| Deploytes Derivat (`site/static/media/`) | Maße | Bytes | Quelle |
|---|---|---|---|
| `ambient/clouds-study.avif` (ersetzt die 10.536-B-RGB-Fassung) | 384 × 512 **RGBA** | 16.472 | Retusche aus `serie-1b-study/clouds-layer.png`, AVIF q60 |

Abnahme `docs/review/wolken-fix/`: kein Raster über Dunkelblau/Grau und in situ
(1440/390, oben + 600 px Scroll, reduced-motion); Ebene bleibt aktiviert.
Befund 2 (scrollte mit): Ebene auf `position:fixed; z-index:0` wie `.room-bg`.

## Nachtrag: The Scout sitzend (24.07.2026, Steward-Lieferung)

Neuer Scout-Cutout ausserhalb der Codex-Serien (direkte Steward-Lieferung, ChatGPT,
C2PA im Master). Ersetzt den stehenden Scout aus Serie 1c **im selben Slot**
(`/media/actors/scout.avif`) — Einbau nach dem Szene-Kantenprinzip
(`docs/szene-kantenprinzip-fuer-kimi.md`, links verankert).

| Datei (`provenance/nachtrag-study-scout-sitzend/`) | Motiv / Rolle | Maße | Bytes | SHA-256 |
|---|---|---|---|---|
| `scout-sitzend-cutout.png` | **The Scout** — sitzend am Schreibtisch (Lampe, Monitor, Bücher, Stuhl), weisser Grund, C2PA | 1122 × 1402 | 1.328.434 | `81f5e819bda0a5343ed975766c5e8c806a94e2106ea283db203118118cf0b3ca` |

**Cutout-Maße (% der Bildhöhe, vermessen am Alpha-Master):** Augenhöhe ≈ 26 % ·
Tischoberkante ≈ 49,5 % · Fußlinie ≈ 82 % (Alpha-Bbox x 5,6–99,6 %, y 17,8–82 %).

**Freistell-Pipeline (Browser-Canvas per CDP, Skript /tmp — flüchtig):** Rand-Flood-Fill
auf Entsättigung+Helligkeit (mn > 150, mx−mn < 30 — erfasst den grauen Bodenschatten-
Verlauf) → Loch-Füllung nur für grosse randferne CCs (> 4000 px, meanSat < 12,
meanMn > 190 — schützt Papier/Buch/Halstuch/Monitor) plus Bodenschatten-Reste
(cy > 66 %, sat < 14, mn > 150, ≥ 20 px) → **Schatten-Unmultiply** (untere Zone,
entsättigte Mitteltöne → fast schwarz, Alpha ∝ Abdunklung × 0,6 — weicher
Kontaktschatten statt grauem Fleck) → 1-px-Erode (halbe Kante). Messung: 0 opake
Weiss-Reste; Montage auf dunklem Grund ohne sichtbaren Saum.

| Deploytes Derivat (`site/static/media/`) | Maße | Bytes | Quelle |
|---|---|---|---|
| `actors/scout.avif` | 935 × 1168 **RGBA** | 41.382 | `nachtrag-study-scout-sitzend/scout-sitzend-cutout.png`, AVIF q55 (schlug WebP q80: 60.992 B) |

## Nachtrag: The Council — Saal-Serie + Lesepult (24.07.2026, Steward-Lieferung)

Council-Serie ausserhalb der Codex-Serien (direkte Steward-Lieferung, ChatGPT,
C2PA in allen Mastern): Saal-Plates quer/hoch je geschlossen/offen (Zählmaschine
bereits gemalt, Tür zentriert), Lesepult auf weissem Grund, Zählmaschinen-Einzelbild.
Einbau nach dem Szene-Kantenprinzip (`docs/szene-kantenprinzip-fuer-kimi.md`,
Pulte von unten). `15_36_54.png` ist bytidentisch mit `15_37_38.png` (nur ein Master
archiviert); `15_36_34.png` ist ein Kontaktbogen der STUDY-Serie (Dokumentation,
kein Asset — nicht archiviert).

| Datei (`provenance/nachtrag-council-serie/`) | Motiv / Rolle | Maße | Bytes | SHA-256 |
|---|---|---|---|---|
| `council-plate-quer-geschlossen.png` | Saal 16:9, Tür geschlossen, Zählmaschine mittig, C2PA | 1672 × 941 | 2.115.607 | `15126961360a3e62939a9528869bb627ab2c8767f0c3933c324c5bbe6382ea9f` |
| `council-plate-quer-offen.png` | Saal 16:9, Tür OFFEN (warmer Spalt), C2PA | 1672 × 941 | 1.976.708 | `d37ccd9d19655dca0c33f7baf32bd9c23263d6a4681c65c2b9e718f8abb6b357` |
| `council-plate-hoch-geschlossen.png` | Saal 2:3, Tür geschlossen (Mobil-Slot, bislang null), C2PA | 1024 × 1536 | 1.956.371 | `234cd4830d635c748e582f11ebee249f8a141ff0b7773ff992793c08d5ce1d7d` |
| `council-plate-hoch-offen.png` | Saal 2:3, Tür offen — nur Provenienz (Tür-offen-Ebene ist Desktop-only), C2PA | 1024 × 1536 | 1.815.211 | `f6dacc733f6953926468df07498fc4274ef574ad045f5dc89cd23ef8f2e63854` |
| `lesepult-cutout.png` | **Lesepult** mit Lämpchen und Buchfläche, weisser Grund, C2PA | 1024 × 1536 | 1.642.695 | `46611eff4ff8be6bcff334f1387c80f58371e46eec2409a12c89b80c3aeb0a06` |
| `zaehlmaschine.png` | Zählmaschine auf Rundtisch, dunkler gemalter Grund — nur Provenienz (in den Plates gemalt; Freistellung gegen Dunkel unsauber), C2PA | 1448 × 1086 | 2.082.507 | `22ae8795b94b70e3dbc5624c7bfa30d95c936452d8db9599c73f85b2968d86c5` |

**Lesepult-Maße (% der Bildhöhe, vermessen am Alpha-Master):** Lampenmitte ≈ 16 % ·
Buchfläche ≈ 26 % · Basislinie ≈ 88,7 % (Alpha-Bbox x 17,9–79,3 %, y 13,9–88,7 %).

**Freistell-Pipeline (Browser-Canvas per CDP, Skript /tmp — flüchtig):** wie Scout-
Nachtrag (Rand-Flood-Fill mn > 150/mx−mn < 30 → Loch-Füllung grosser randferner CCs
→ 1-px-Erode), zwei Anpassungen: **Warmhalo-Rettung** in der oberen Bildhälfte
(bg-markierte warme Pixel r > b+15, mn > 140 → transluzent statt hart abgeschnittener
Lampenschein, 53 px) und Sockelschatten-Unmultiply enger auf y > 84 % H (das Pult
reicht fast bis zum Bildgrund). Messung: 352 px behaltene Reste (Lampen-Blendenfleck
auf der Buchfläche + Staub ≤ 8 px), Montage auf dem Saal-Plate ohne sichtbaren Saum.

| Deploytes Derivat (`site/static/media/`) | Maße | Bytes | Quelle |
|---|---|---|---|
| `actors/lectern.avif` | 1024 × 1536 **RGBA** | 55.514 | `lesepult-cutout.png`, AVIF q55 (schlug WebP q80: 80.148 B) |
| `scenes/hall-display.avif` (ersetzt die 1600×900-Fassung vom 17.07.) | 1672 × 941 | 91.160 | `council-plate-quer-geschlossen.png`, AVIF q55 (WebP: 118.534 B) |
| `scenes/hall-door-open-display.avif` | 1672 × 941 | 76.964 | `council-plate-quer-offen.png`, AVIF q55 (WebP: 94.976 B) |
| `scenes/hall-portrait-display.avif` | 1024 × 1536 | 61.777 | `council-plate-hoch-geschlossen.png`, AVIF q55 (WebP: 79.734 B) |
| `scenes/hall-portrait-800.avif` | 800 × 1200 | 34.894 | `council-plate-hoch-geschlossen.png` via sips, AVIF q55 (WebP: 43.118 B) |

## Commission-2-Medaillons (07.08.2026)

Nachbestellung für die neue Besetzung aus
`commissions/2026-08-07/commission.json`; Einbau gemäß
`docs/cc-auftrag-phase-a-medaillons-und-deploy-2026-08-07.md`. Erzeugt in der
ImageGen-Task `019fdda5-e4f2-7a63-b139-2e9a40a3023f` mit drei gleichartigen
Läufen je Modell; archiviert werden nur die drei ausgewählten, unveränderten
C2PA-Originale.

| Original (`provenance/medallions-commission-2/`) | Auswahl | Maße | Bytes | SHA-256 |
|---|---|---:|---:|---|
| `claude-opus-5.png` | Claude v2 | 1254 × 1254 | 2.748.264 | `0bd361ce287ae68b09b678dca028bbd9cc0d108ed760231ecbd2fb708a49f2cf` |
| `gpt-5.6-sol.png` | Sol v1 | 1254 × 1254 | 2.841.974 | `217407f3bd0a646faf75c1acabb6c17f9348b15612574893ea456020e0eb0718` |
| `gemini-3.5-flash.png` | Gemini v3 | 1254 × 1254 | 2.539.042 | `1f8015050c48769c73fdc9668362fd07a115d9e3759f240a1dbdf96864effb96` |

Ableitung: C2PA-Original → motivneutrale Normalisierung der Außenfläche auf
exakt `#FF00FF` → Freistellung und AVIF-Encoding. Die normalisierten
Arbeitsmaster bleiben außerhalb des Repos; das erneute PNG-Speichern entfernte
ihre Credentials. Bezugswerte der reproduzierten Kette:

| Modell | Arbeitsmaster SHA-256 | Deploy-AVIF SHA-256 | `-lo` SHA-256 |
|---|---|---|---|
| Claude | `562927b8869a2527435b5872757bbd61126638895dc48f6b03210bf137d6200d` | `ae9c2b30db9d4923a4a6dfd04aef015bd9fa6905c80e47f58dcc6d854aa40079` | `0a2883c5fedd4f2b5f32889367a3d4a8be965cfdbff6b621ae56fa2ffaa4f34e` |
| Sol | `12fd84c4f16683fa65e8846e9a4caf10c3a6d46c31c035072e41d9989c64becd` | `95546ee07cbce136774de2c530a562331ea8017276e785d3c7c861fc2794c37d` | `d58d044ee3e24503186f3bbd36b3b49676cda1f4e0ecaee15032729dade67137` |
| Gemini | `6ad5b490cb91258d866a6380da1138b222355dc28cd75cb12a2ef88fce69ea44` | `2d370932fa8e75b2614c58771a2cd75b88c25c728f52b3752b200f2a0e16a916` | `8f55df19605091e64104cc65e987d1f5d664cc513b467311dedf253fa4098168` |
