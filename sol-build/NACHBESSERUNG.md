# Nachbesserung SOL-Frontend + Datenvertrag — Vorher/Nachher

Umsetzung der Muss-Fixes aus dem Review (PR #11) in der vorgegebenen Reihenfolge.
**Kein Merge, kein Deploy.** `prompts.py` und publizierte Sitzungs-**Texte**
(summary/dissent_md/Votentext/Titel) unangetastet.

## Schritt 1 — Schema-Naht + strukturierte Voten
| | Vorher | Nachher |
|---|---|---|
| Schema | Dublette `session.schema.json` == `sitzung.schema.json` | **eine** kanonische `schema/session.schema.json`; Alias entfällt |
| Voten in `session.json` | nur `{model, content_md (Prosa), confidence}` | **+ `recommendations[]`** (registry-aufgelöst: pillar/organization_id/organization/title/confidence/conditional/reservation) |
| Generator | `votes_of()` verwarf die geparsten Recs | persistiert sie (`structured_vote_recs`) |
| Bestandsdaten | — | **Backfill** der 3 Sitzungen aus `raw/` (`reaggregate.py --backfill-votes`), **kein Text geändert** |
| Registry | deckte nur r2-Strings | deckt **alle** r1+r2-Voten (0 unresolved); neu: `tarl-africa`, `global-road-safety-partnership` + NTI/GovAI-Aliasse |

**Ergebnis:** Das Frontend rendert Protokollspalten **und** die Revision
(„TaRL Africa → Helen Keller International", GPT & Gemini) **ohne Prosa zu parsen**.

## Schritt 2 — Datenvertrag (`data-contract.md`)
Jede Abweichung disponiert (Backend / Frontend-Konstante / entfällt / build-abgeleitet).
Ziel dokumentiert: realer Generator-Output == Frontend-Input, **reiner Swap**.

## Schritt 3 — F1 verankert
| | Vorher | Nachher |
|---|---|---|
| „Warum" auf der Karte | `rationale_md` (frontend-erfunden, Säule A: „Finanzierungslücke besser belegt als bei der Bildungsalternative") | **entfernt** |
| Faktische Beschreibung | — | `organizations.json.beschreibung` (kuratiert, neutral, ohne Wertung) je Org; im Schema Pflicht |
| Karte zeigt | Org + erfundenes Warum + Stimmen + Sicherheit + Link | Org + **beschreibung** + „X von 3 nennen dieselbe Organisation" + „Sicherheit: N von 100" + Link |

## Schritt 4 — Handwerk
- **F5 Tap-Ziele:** `donation-link` 48px & Protokoll-Reiter 50px waren bereits ≥44px
  (Review-Schätzung ~37px war falsch); **Nav-Links + `quiet-link` auf 44px** gehärtet.
- **F6:** echtes `<h1>` = Seitentitel („Öffentliche Beratung, wohin Spenden am
  wirksamsten fließen"); führende Organisation ist jetzt `<h2>`.
- **F4:** publizierter Sitzungstitel **nicht** geändert; er erscheint nicht auf der
  Antwortebene (dort Klartext). Notiz für die Content-Kaskade in `data-contract.md`.
- **Assets:** `ratssaal.png`/`vorraum.png` mit **intakten C2PA-Credentials** nach
  `site/static/` versioniert; Herkunft (KI, `gpt-image` v2.0, `trainedAlgorithmicMedia`)
  in `site/static/ASSETS.md`. Verlustarme Verkleinerung **aufgeschoben** (das einzige
  lokale Werkzeug `sips` würde C2PA strippen — Transparenz vor Bytes; C2PA-erhaltender
  Optimierer als Folge empfohlen).

## Unveränderte Stärken (Review bestätigt, weiter gültig)
no-JS vollständig, Datenschutz sauber (0 Tracker/Fonts/Cookies; alle Links
`rel="noopener noreferrer"`), Kontrast WCAG-AA+, Skip-Link + sichtbarer Fokus.

## Ehrliche Grenze — Sprache im Protokoll
Mit **echten** Daten trägt der **verbatim** gerenderte `dissent_md` (Modell-Prosa) und
der `correction_notice` Fachvokabular (Konfidenz/Dissens/konditional/Diff). Das ist
**publizierter Text (tabu)**, kein Frontend-Label — es steht in der Protokoll-/
Transparenzebene, nicht auf der Antwortebene (die ist jargonfrei). **Empfehlung:**
künftige Dissens-/Titeltexte redaktionell klarer (Content-Kaskade), nicht im Frontend.

## Verifikation
`python build.py` grün (rendert aus echter `sessions/2026-07c/session.json`);
`pytest` 22 grün (10 golden + 9 aggregate + 3 build); Schemas validieren alle realen
Dateien; Browser-Render bestätigt H1/H2, `beschreibung` statt erfundenem Warum,
abgeleitete Revision. Backfill nur additiv (kein Text entfernt/geändert).
