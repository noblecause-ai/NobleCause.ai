# NobleCause Corrective Build Report

Stand: 16. Juli 2026  
Produktiver Pfad: `site/`  
Statische Ausgabe: `site/build/`

## Ergebnis

Die abgelehnte, abschnittsweise Präsentationsschicht wurde durch eine einzige feste
Desktopbühne ersetzt. Das Ziel-Mockup ist nun der kompositorische Vertrag: Empfehlungen
links, Ratssaal und Zählmaschine im Zentrum, Archiv rechts, Vorzimmer als räumlicher
Übergang und der Ablauf als integrierte mechanische Schiene am unteren Rand.

Die vorhandene Datenlogik blieb erhalten. Organisationen und Spendenziele werden weiterhin
ausschließlich über `organization_id` aus der Registry aufgelöst. Konsens, Nicht-Konsens,
Erst- und Schlussvoten, sichtbare Änderungen, Vorbehalte, Korrekturhinweise und Kosten
stammen aus den publizierten Sitzungsdaten.

## Umgesetzte Zustände

Die Bühne besitzt acht adressierbare Zustände:

1. `arrival` – Ratssaal, Kernfrage und Mechanismus
2. `recommendations` – beleuchtetes kompaktes Empfehlungsregister
3. `door-opening` – zweiflügelige CSS-Tür öffnet den Übergang
4. `antechamber` – Vorzimmer übernimmt die Hauptfläche; Späher und Wart werden verortet
5. `initial` – alle drei Modellpulte sind gleichzeitig sichtbar
6. `revision` – Erst- und Schlussvotum werden nebeneinander gezeigt; alte Voten bleiben sichtbar
7. `count` – die deterministische Zählmaschine rückt ins Zentrum
8. `archive` – monumentale Archivtür und Sitzungsregister erhalten den Fokus

Scrollposition, Hash-Navigation, Tastaturfokus und Browser-Zurück steuern dasselbe
Zustandsmodell. Die Bühne transformiert Kamera, Licht und räumlichen Fokus; der Nutzer
scrollt nicht durch autonome Inhaltssektionen.

## Desktop, Mobil und Fallback

Desktop nutzt eine viewportfüllende 3×3-Instrumentenkomposition. Die Ratssaal-Plate bleibt
die dominante Fläche; Informationsoberflächen sind kompakte Register, Schilder und Pulte.

Unter 800 px wird nicht die Desktopbühne skaliert. Es entsteht eine lineare mobile
Komposition mit frühem Ratssaal, Mechanismuserklärung, Empfehlungen und Direktlinks,
Vorzimmer, Prozess, Pulten, Revisionen, Zählung und Archiv. Horizontaler Überlauf wurde bei
390 px und 320 px ausgeschlossen.

Der ohne JavaScript vorgerenderte Grundzustand ist ein eigenständiges semantisches
Dokument. Er bleibt sichtbar, bis die Svelte-Bühne erfolgreich hydriert ist. Ohne JavaScript
sind Empfehlungen, Gründe, Stimmen, sichtbare Änderungen, Dissens, Kosten sowie Spenden-
und Protokolllinks erreichbar. Auf Mobil ist das Ergebnisregister einspaltig.

## Gemeinsame Bildwelt

Das globale Layout verwendet nun eine dunkle, matte Archivhülle mit Messinglinien,
Mondblau-Akzenten und einer ruhigen Dokumentfläche. Damit gehören Manifest, Sitzungen,
Journal, Idee und Impressum zur selben materiellen Welt wie die Bühne, ohne ihre
dokumentarische Lesbarkeit oder Routenstruktur zu verlieren. Die Sitzung `2026-07c` wurde
zusätzlich bei 1440 × 900 visuell geprüft.

## Daten- und Inhaltsintegrität

- `site/src/lib/server/homepage.js` bleibt das explizite Homepage-View-Model.
- Unbekannte Registry-IDs und nicht auflösbare Stimmen brechen den Build ab.
- `2026-07c` bildet vier 2-von-3-Konsense einschließlich Vorbehalt und Revisionen ab.
- `2026-07` bildet den Säule-A-Nicht-Konsens mit drei gleichwertigen Registry-Zielen ab.
- Rohes `dissent_md` und eingebettetes JSON werden nicht als Organisationsidentität benutzt.
- Boilerplate in `rationale_md` wird nicht zur Erfindung einer Begründung ergänzt.
- `sessions/`, `journal/`, `schedule/`, `gremium/` und `schema/` wurden nicht verändert.

## Abnahmescreenshots

Alle verlangten Aufnahmen liegen unter `docs/review/corrective-home/`:

- `01-arrival.png`
- `02-recommendations.png`
- `03-door-opening.png`
- `04-antechamber.png`
- `05-three-lecterns.png`
- `06-revision.png`
- `07-counting-machine.png`
- `08-archive.png`
- `09-mobile.png`
- `10-nojs.png`

Die ersten acht Aufnahmen entstanden bei 1440 × 900, die mobile und No-JS-Abnahme bei
390 × 844. Die Zielreferenz ist `docs/steampunk_beratungsraum_mit_ui_elementen.png`; der
frühere Build wurde ausschließlich als negative Referenz behandelt.

## Ausgeführte Prüfungen

| Befehl / Prüfung | Exit | Ergebnis |
|---|---:|---|
| `npm test` in `site/` | 0 | `pretest` erzeugte den Produktionsbuild; 7/7 Tests bestanden |
| `npm run build` (über `pretest`) | 0 | SvelteKit/Vite-Build ohne Warnungen; Adapter Static schrieb nach `site/build/` |
| `git diff --check` | 0 | keine Whitespace-Fehler |
| Diff-Prüfung der geschützten Datenpfade | 0 | keine Änderungen |
| Playwright Desktop 1440 | 0 | 1440/1440 px, Bühne sichtbar, H1 korrekt |
| Playwright Desktop 1024 | 0 | 1024/1024 px, kein horizontaler Überlauf |
| Playwright Mobil 390 | 0 | 390/390 px, Bühne sichtbar |
| Playwright Mobil 320 | 0 | 320/320 px, kein horizontaler Überlauf |
| Playwright 200%-Äquivalent | 0 | 720/720 CSS-px, reflowt ohne horizontalen Überlauf |
| Playwright ohne JavaScript | 0 | Fallback sichtbar, Bühne nicht aktiviert; 390/390 px |
| Playwright `prefers-reduced-motion` | 0 | Medienabfrage aktiv, alle acht Szenen vorhanden |
| Playwright Tastatur | 0 | erster Tab erreicht den NobleCause-Home-Link |
| Playwright Hash/Zurück | 0 | `count` wird adressiert, Zurück kehrt zu `arrival` zurück |
| Visuelle Sitzungsroute | 0 | `2026-07c`, korrekte H1, 1440/1440 px |

Das Projekt definiert keine separaten `lint`- oder `check`-Skripte; deshalb wurden dafür
keine erfundenen Ergebnisse berichtet. Playwright wurde aus der bereits lokal vorhandenen
Installation und dem vorhandenen Chromium-Cache ausgeführt; es wurde nichts installiert.

## Performance und Bewegung

Die finalen Ratssaal-, Tür-, Vorzimmer- und Archivbilder werden lokal ausgeliefert. Nur der
Ratssaal wird vorab geladen; die nachfolgenden Räume laden verzögert. Kamerabewegungen und
Bildwechsel verwenden CSS-Transforms und Opacity. Bei `prefers-reduced-motion: reduce`
werden Übergänge praktisch deaktiviert; Inhalt und Zustandsnavigation bleiben erhalten.

Der finale Homepage-CSS-Chunk ist 19,95 kB (3,85 kB gzip), der Homepage-JS-Chunk 14,60 kB
(4,29 kB gzip). Die hochauflösenden Szenenbilder bleiben der größte Übertragungsanteil und
sind das wichtigste spätere Optimierungsfeld (responsive Derivate/AVIF), ohne die
Provenienzoriginale zu ersetzen.

## Bekannte Grenzen

- Ratssaal, Zählmaschine, Tür, Vorzimmer und Archiv sind nun eigene gemalte Szenenbilder.
  Die Modell- und Ergebnisdaten bleiben bewusst zugängliche HTML-Ebenen darüber.
- Die 200%-Prüfung simuliert den resultierenden CSS-Viewport; sie ersetzt keine manuelle
  Prüfung mit Betriebssystem-Lupe oder assistiver Technologie.
- Tastatur, reduzierte Bewegung und semantischer No-JS-Inhalt wurden automatisiert geprüft;
  ein manueller Screenreader-Durchlauf bleibt vor Veröffentlichung empfehlenswert.

## Abschluss

Die Korrektur wurde direkt in der deployten SvelteKit-App umgesetzt. Es gibt keinen
separaten Prototyp und keine zweite Datenwahrheit. `npm run build` in `site/` erzeugt die
auslieferbare Site in `site/build/`; damit kann die Bühne nicht erneut als Waisen-Prototyp
außerhalb des Deploymentpfads enden.
