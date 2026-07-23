#!/usr/bin/env python3
"""Deterministic static renderer for NobleCause (nachgebessert).

Liest die ECHTE Sitzung (`../sessions/<id>/session.json`), die Registry
(`../organizations.json`) und Präsentations-Konstanten (`frontend-config.json`),
validiert gegen das kanonische `../schema/session.schema.json` und schreibt
`index.html`. Das Frontend PARST NIE PROSA — Protokollspalten und Revisionen kommen
aus den strukturierten Voten (`rounds[].votes[].recommendations[]`). Der Kartentext
„was die Org tut" kommt aus `organizations.json.beschreibung`; es gibt KEIN
erfundenes „Warum".
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SESSIONS_DIR = REPO / "sessions"
ORG_PATH = REPO / "organizations.json"
SCHEMA_PATH = REPO / "schema" / "session.schema.json"
CONFIG_PATH = ROOT / "frontend-config.json"
OUTPUT_PATH = ROOT / "index.html"

REGISTRY: dict[str, dict[str, Any]] = {}
CONFIG: dict[str, Any] = {}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def percent(value: float | None) -> str:
    if value is None:
        return "nicht angegeben"
    return f"{round(value * 100)} von 100"


def money(value: float, currency: str) -> str:
    symbol = "€" if currency == "EUR" else currency
    return f"{value:,.2f} {symbol}".replace(",", "X").replace(".", ",").replace("X", ".")


def model_label(session: dict[str, Any], model_id: str) -> str:
    for participant in session["participants"]:
        if participant["model"] == model_id:
            return participant["label"]
    return model_id


def beschreibung_of(rec: dict[str, Any]) -> str:
    return REGISTRY.get(rec.get("organization_id", ""), {}).get("beschreibung", "")


def latest_session() -> dict[str, Any]:
    entries = []
    for d in SESSIONS_DIR.iterdir():
        f = d / "session.json"
        if d.is_dir() and f.exists():
            s = json.loads(f.read_text(encoding="utf-8"))
            entries.append((s.get("number", 0), d.name, s))
    if not entries:
        raise SystemExit("Keine Sitzung gefunden.")
    entries.sort(key=lambda x: (x[0], x[1]), reverse=True)  # deterministisch nach Nummer
    return entries[0][2]


def plain_result(session: dict[str, Any]) -> str:
    recs = session.get("recommendations", [])
    n = sum(1 for r in recs if r.get("has_consensus"))
    return f"{n} von {len(recs)} Säulen mit gemeinsamer Empfehlung"


def archive_items(current_id: str) -> list[dict[str, Any]]:
    items = []
    for d in SESSIONS_DIR.iterdir():
        f = d / "session.json"
        if not (d.is_dir() and f.exists()) or d.name == current_id:
            continue
        s = json.loads(f.read_text(encoding="utf-8"))
        items.append({"number": s.get("number", 0), "id": d.name, "date": s.get("date", ""),
                      "title": s.get("title", ""), "result": plain_result(s),
                      "href": f"/sessions/{d.name}/"})
    items.sort(key=lambda x: x["number"], reverse=True)
    return items


def focus_recommendation(session: dict[str, Any]) -> dict[str, Any]:
    """Deterministische Regel: Stimmenanteil, dann Sicherheit, dann Säule A–D."""
    def key(rec: dict[str, Any]) -> tuple[float, float, int]:
        if rec.get("has_consensus"):
            convergence = rec["convergence"]
            share = convergence["count"] / max(convergence["total"], 1)
        else:
            share = 0.0
        confidence = rec.get("confidence") or 0.0
        pillar_order = 4 - (ord(rec["pillar"]) - ord("A"))
        return share, confidence, pillar_order

    return max(session["recommendations"], key=key)


def link_or_note(url: str | None, label: str = "Direkt zur Organisation ↗") -> str:
    if not url:
        return '<p class="donation-missing">Kein offizieller Spendenweg auffindbar.</p>'
    return (
        f'<a class="donation-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
        f'{esc(label)}</a>'
    )


def org_in_round(session: dict[str, Any], kind: str, model: str, pillar: str) -> str | None:
    rd = next((r for r in session["rounds"] if r.get("kind") == kind), None)
    if not rd:
        return None
    v = next((x for x in rd.get("votes", []) if x["model"] == model), None)
    if not v:
        return None
    return next((rc["organization"] for rc in v.get("recommendations", []) if rc["pillar"] == pillar), None)


def pillar_revisions(session: dict[str, Any], pillar: str) -> list[dict[str, str]]:
    """Wer hat zwischen Runde 1 und 2 die Organisation gewechselt — aus den
    strukturierten Voten, ohne Prosa-Parsing."""
    out = []
    final = next((r for r in session["rounds"] if r.get("kind") == "final_vote"), None)
    for v in (final.get("votes", []) if final else []):
        before = org_in_round(session, "initial_vote", v["model"], pillar)
        after = org_in_round(session, "final_vote", v["model"], pillar)
        if before and after and before != after:
            out.append({"label": model_label(session, v["model"]), "before": before, "after": after})
    return out


def recommendation_card(session: dict[str, Any], rec: dict[str, Any], focused: bool = False) -> str:
    pillar = rec["pillar"]
    label = CONFIG["pillar_labels"][pillar]
    symbol = CONFIG["pillar_symbols"][pillar]
    classes = ["recommendation-card", f"pillar-{pillar.lower()}"]
    if focused:
        classes.append("is-focused")

    if rec["has_consensus"]:
        conv = rec["convergence"]
        conditional_count = conv.get("conditional_count", 0)
        state = "Einigkeit mit Vorbehalt" if conditional_count else "Empfehlung"
        vote_line = f'{conv["count"]} von {conv["total"]} nennen dieselbe Organisation'
        condition_html = ""
        if conditional_count:
            reservations = [v.get("reservation") for v in conv.get("votes", []) if v.get("conditional") and v.get("reservation")]
            reserve = reservations[0] if reservations else "Ein Modell empfiehlt unter Vorbehalt."
            condition_html = (
                '<div class="condition-note"><strong>Unter Vorbehalt:</strong> '
                f'{esc(reserve)}</div>'
            )
        revisions = pillar_revisions(session, pillar)
        revision_html = ""
        if revisions:
            rows = "".join(
                f'<span class="chalk-strike">{esc(r["before"])}</span>'
                f'<span aria-hidden="true"> → </span><strong>{esc(r["after"])}</strong> '
                f'<small>({esc(r["label"])})</small>'
                for r in revisions
            )
            revision_html = (
                '<div class="revision-note" aria-label="Änderung nach dem Gegenlesen">'
                '<span class="revision-label">Was sich geändert hat</span>'
                f'{rows}</div>'
            )
        return f'''
        <article class="{' '.join(classes)}" id="empfehlung-{pillar.lower()}">
          <header class="card-kicker">
            <span class="pillar-mark" aria-hidden="true">{esc(pillar)}</span>
            <span>{esc(label)}</span>
            <span class="asset-word">{esc(symbol)}</span>
          </header>
          <div class="card-state">{esc(state)}</div>
          <h3>{esc(rec["organization"])}</h3>
          <p class="plain-reason">{esc(beschreibung_of(rec))}</p>
          <p class="vote-count"><strong>{esc(vote_line)}</strong> · Sicherheit: {esc(percent(rec.get("confidence")))}</p>
          {condition_html}
          {revision_html}
          {link_or_note(rec.get("donation_url"))}
        </article>
        '''

    votes = rec.get("individual_votes", [])
    vote_cards = []
    for vote in votes:
        vote_cards.append(f'''
          <article class="split-vote">
            <span class="model-tag">{esc(vote["model"])}</span>
            <h4>{esc(vote["organization"])}</h4>
            <p class="plain-reason">{esc(REGISTRY.get(vote.get("organization_id", ""), {}).get("beschreibung", ""))}</p>
            {link_or_note(vote.get("donation_url"), "Zu dieser Organisation ↗")}
          </article>
        ''')
    return f'''
      <article class="{' '.join(classes)} no-consensus" id="empfehlung-{pillar.lower()}">
        <header class="card-kicker">
          <span class="pillar-mark" aria-hidden="true">{esc(pillar)}</span>
          <span>{esc(label)}</span>
          <span class="asset-word">{esc(symbol)}</span>
        </header>
        <div class="card-state">Keine Einigung</div>
        <h3>Alle Antworten bleiben nebeneinander stehen.</h3>
        <div class="split-votes">{''.join(vote_cards)}</div>
      </article>
    '''


def vote_rec_map(vote: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {rec["pillar"]: rec for rec in vote.get("recommendations", [])}


def protocol_column(session: dict[str, Any], vote: dict[str, Any], phase: str, initial_vote: dict[str, Any] | None = None) -> str:
    label = model_label(session, vote["model"])
    family = next((p["family"] for p in session["participants"] if p["model"] == vote["model"]), "")
    recs = vote_rec_map(vote)
    initial_recs = vote_rec_map(initial_vote) if initial_vote else {}
    rows: list[str] = []
    for pillar in ["A", "B", "C", "D"]:
        rec = recs.get(pillar)
        if not rec:
            continue
        before = initial_recs.get(pillar)
        changed = before and before["organization"] != rec["organization"]
        change_markup = ""
        if phase == "final" and changed:
            change_markup = (
                '<div class="change-record">'
                f'<del>{esc(before["organization"])}</del>'
                f'<ins>{esc(rec["organization"])}</ins>'
                '<span>nach dem Gegenlesen geändert</span>'
                '</div>'
            )
        elif phase == "final":
            change_markup = '<span class="held-position">Antwort beibehalten</span>'
        reservation = rec.get("reservation")
        rows.append(f'''
          <section class="vote-row" id="model-{esc(family)}-{esc(phase)}-{pillar.lower()}">
            <span class="vote-pillar">{esc(pillar)}</span>
            {change_markup}
            <h4>{esc(rec["organization"])}</h4>
            {f'<p class="condition-inline">Unter Vorbehalt: {esc(reservation)}</p>' if rec.get("conditional") and reservation else ''}
          </section>
        ''')
    return f'''
      <article class="model-column" id="model-{esc(family)}">
        <header>
          <span class="model-family">{esc(family)}</span>
          <h3>{esc(label)}</h3>
          <p>Sicherheit der gesamten Antwort: {esc(percent(vote.get("confidence")))}</p>
        </header>
        {''.join(rows)}
      </article>
    '''


def render() -> str:
    global REGISTRY, CONFIG
    REGISTRY = {o["id"]: o for o in json.loads(ORG_PATH.read_text(encoding="utf-8"))["organizations"]}
    CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    session = latest_session()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(session), key=lambda e: list(e.path))
    if errors:
        details = "\n".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise SystemExit(f"Schema validation failed:\n{details}")

    focus = focus_recommendation(session)
    cards = "".join(recommendation_card(session, r, r["pillar"] == focus["pillar"]) for r in session["recommendations"])
    initial = next(r for r in session["rounds"] if r["kind"] == "initial_vote")
    final = next(r for r in session["rounds"] if r["kind"] == "final_vote")
    initial_by_model = {v["model"]: v for v in initial["votes"]}
    first_columns = "".join(protocol_column(session, v, "initial") for v in initial["votes"])
    second_columns = "".join(protocol_column(session, v, "final", initial_by_model.get(v["model"])) for v in final["votes"])
    result_cards = "".join(recommendation_card(session, r) for r in session["recommendations"])

    archive = "".join(
        f'''
        <li>
          <a href="{esc(item['href'])}">
            <span class="archive-number">Sitzung {esc(item['number'])}</span>
            <span class="archive-title">{esc(item['title'])}</span>
            <span class="archive-result">{esc(item['result'])}</span>
            <time datetime="{esc(item['date'])}">{esc(item['date'])}</time>
          </a>
        </li>
        '''
        for item in archive_items(session["id"])
    )

    focus_conv = focus["convergence"]
    machine_state = "consensus" if any(r["has_consensus"] for r in session["recommendations"]) else "split"
    correction = session.get("correction_notice")
    correction_html = ""
    if correction:
        correction_html = f'''
          <aside class="correction-note" aria-label="Korrekturhinweis">
            <strong>Korrektur vom {esc(correction['date'])}</strong>
            <p>{esc(correction['text'])}</p>
          </aside>
        '''

    data_json = json.dumps(session, ensure_ascii=False).replace("</", "<\\/")

    return f'''<!doctype html>
<html lang="de" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Öffentliche Beratung dreier KI-Modelle darüber, wohin Spenden am wirksamsten fließen.">
  <title>NobleCause · Öffentliche Beratung, Sitzung {esc(session['number'])}</title>
  <link rel="stylesheet" href="styles.css">
  <script>document.documentElement.className='js';</script>
  <script src="app.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#antworten">Direkt zu den Empfehlungen</a>

  <header class="site-header">
    <a class="wordmark" href="/" aria-label="NobleCause Startseite">NOBLECAUSE</a>
    <nav aria-label="Hauptnavigation">
      <a href="#entstehung">So funktioniert es</a>
      <a href="#protokoll">Protokoll</a>
      <a href="#fruehere-sitzungen">Frühere Sitzungen</a>
    </nav>
    <span class="session-stamp">Sitzung {esc(session['number'])} · {esc(session['date'])}</span>
  </header>

  <main>
    <section class="hero" aria-labelledby="site-title">
      <img class="hero-plate" src="site/static/ratssaal.png" alt="" width="1672" height="941">
      <div class="hero-shade" aria-hidden="true"></div>
      <div class="hero-content">
        <h1 class="site-title" id="site-title">Öffentliche Beratung, wohin Spenden am wirksamsten fließen</h1>
        <p class="context-line">Drei künstliche Intelligenzen beraten öffentlich. Jede Sitzung wird vollständig veröffentlicht.</p>
        <p class="trust-line">Sie beraten unabhängig. Sie lesen einander. Sie dürfen umdenken. Die Zählmaschine zählt. Alles wird veröffentlicht.</p>

        <div class="lit-floor" id="antworten">
          <p class="eyebrow">Heute führt nach einer festen Regel</p>
          <h2 id="hero-focus">{esc(focus['organization'])}</h2>
          <p class="focus-reason">{esc(beschreibung_of(focus))}</p>
          <p class="focus-vote">{esc(focus_conv['count'])} von {esc(focus_conv['total'])} Stimmen · Sicherheit: {esc(percent(focus.get('confidence')))}</p>
          <div class="hero-actions">
            {link_or_note(focus.get('donation_url'), 'Hier direkt spenden ↗')}
            <a class="quiet-link" href="#entstehung">So entsteht die Empfehlung ↓</a>
          </div>
        </div>

        <div class="recommendation-grid" aria-label="Alle vier Empfehlungen">
          {cards}
        </div>
        <p class="money-note">Durch diese Seite fließt kein Geld. Jeder Spendenlink führt direkt zur Organisation. Kosten dieser Sitzung: {esc(money(session['costs']['total'], session['costs']['currency']))}.</p>
      </div>
    </section>

    <section class="process-band" id="entstehung" aria-labelledby="process-title">
      <div class="section-heading compact">
        <p class="eyebrow">Der Ablauf in sechs Schritten</p>
        <h2 id="process-title">So entsteht die Empfehlung</h2>
      </div>
      <ol class="stepper">
        <li><a href="#frage"><span>1</span><strong>Eine Frage</strong><small>Die Sitzung beginnt mit einer klaren Frage.</small><em>Im Saal zeigen ↓</em></a></li>
        <li><a href="#belege"><span>2</span><strong>Belege sammeln</strong><small>Der Späher sammelt Quellen. Der Wart ordnet sie.</small><em>Im Vorzimmer zeigen ↓</em></a></li>
        <li><a href="#erste-antworten"><span>3</span><strong>Drei Antworten, getrennt</strong><small>Kein Modell sieht vorher die Antwort der anderen.</small><em>Zu den Pulten ↓</em></a></li>
        <li><a href="#zweite-antworten"><span>4</span><strong>Gegenlesen und umdenken</strong><small>Änderungen bleiben sichtbar. Nichts wird gelöscht.</small><em>Änderungen zeigen ↓</em></a></li>
        <li><a href="#maschine"><span>5</span><strong>Die Maschine zählt</strong><small>Das Programm zählt gleiche Nennungen. Es urteilt nicht.</small><em>Zur Mitte ↓</em></a></li>
        <li><a href="#ergebnis"><span>6</span><strong>Veröffentlichen</strong><small>Frage, Antworten, Uneinigkeit und Kosten bleiben öffentlich.</small><em>Zum Ergebnis ↓</em></a></li>
      </ol>
    </section>

    <section class="hall-section" aria-labelledby="hall-title">
      <div class="section-heading">
        <p class="eyebrow">Der Raum ist Navigation</p>
        <h2 id="hall-title">Der Ratssaal</h2>
        <p>Jedes beleuchtete Pult steht für eine abgegebene Antwort. Die Maschine in der Mitte zählt nur.</p>
      </div>
      <figure class="hall-map" id="frage">
        <img src="site/static/ratssaal.png" alt="Dunkler kreisrunder Ratssaal mit drei weit auseinanderliegenden beleuchteten Pulten." width="1672" height="941">
        <div class="machine-symbol {esc(machine_state)}" id="maschine" aria-label="Zählmaschine: Es liegen Empfehlungen mit mindestens zwei gleichen Nennungen vor.">
          <span class="gear gear-a" aria-hidden="true">⚙</span>
          <span class="gear gear-b" aria-hidden="true">⚙</span>
          <span class="machine-label">zählt</span>
        </div>
        <a class="hotspot pulpit pulpit-anthropic" href="#model-anthropic" aria-label="Zum Pult von Claude Opus"><span></span>Claude Opus</a>
        <a class="hotspot pulpit pulpit-openai" href="#model-openai" aria-label="Zum Pult von GPT"><span></span>GPT</a>
        <a class="hotspot pulpit pulpit-google" href="#model-google" aria-label="Zum Pult von Gemini Pro"><span></span>Gemini Pro</a>
        <a class="hotspot machine-hotspot" href="#ergebnis" aria-label="Von der Zählmaschine zum Ergebnis"><span></span>Ergebnis</a>
        <figcaption>Die drei Pulte sind gleich groß. Niemand sitzt in der Mitte.</figcaption>
      </figure>

      <aside class="antechamber" id="belege" aria-labelledby="antechamber-title">
        <img src="site/static/vorraum.png" alt="Vorzimmer mit großer leerer Schiefertafel, dem Späher am Bildschirm und dem wachen Wart, der einen Bericht liest." width="1915" height="821">
        <div class="antechamber-copy">
          <p class="eyebrow">Vor dem Saal</p>
          <h3 id="antechamber-title">Späher und Wart</h3>
          <p>Der Späher sammelt Belege. Der Wart dokumentiert und stellt Fragen, gibt aber keine eigene Spendenempfehlung ab.</p>
          <a href="#erste-antworten">Weiter zu den getrennten Antworten ↓</a>
        </div>
      </aside>
    </section>

    <section class="protocol" id="protokoll" aria-labelledby="protocol-title">
      <div class="section-heading">
        <p class="eyebrow">Alles bleibt sichtbar</p>
        <h2 id="protocol-title">Das Protokoll</h2>
        <p>Die Modelle stehen nebeneinander, nicht übereinander. Eine geänderte Antwort wird durchgestrichen und neu darübergeschrieben.</p>
      </div>

      <div class="protocol-tabs" role="tablist" aria-label="Runden des Protokolls">
        <button type="button" role="tab" aria-selected="true" aria-controls="erste-antworten" id="tab-erste">Erste Antworten</button>
        <button type="button" role="tab" aria-selected="false" aria-controls="zweite-antworten" id="tab-zweite">Zweite Antworten</button>
        <button type="button" role="tab" aria-selected="false" aria-controls="ergebnis" id="tab-ergebnis">Ergebnis</button>
      </div>

      <section class="tab-panel" id="erste-antworten" role="tabpanel" aria-labelledby="tab-erste">
        <div class="round-heading"><span>Runde 1</span><h3>Drei getrennte erste Antworten</h3></div>
        <div class="model-grid">{first_columns}</div>
      </section>

      <section class="tab-panel" id="zweite-antworten" role="tabpanel" aria-labelledby="tab-zweite">
        <div class="round-heading"><span>Runde 2</span><h3>Nach dem Gegenlesen</h3></div>
        <div class="model-grid">{second_columns}</div>
        <aside class="dissent-note"><strong>Verbleibende Uneinigkeit:</strong> {esc(session['dissent_md'])}</aside>
      </section>

      <section class="tab-panel" id="ergebnis" role="tabpanel" aria-labelledby="tab-ergebnis">
        <div class="round-heading"><span>Die Zählmaschine</span><h3>Gleiche Nennungen werden gezählt</h3></div>
        <p class="machine-explanation">Mindestens zwei gleiche Nennungen ergeben eine Empfehlung. Sonst stehen alle Antworten gleichwertig nebeneinander.</p>
        <div class="recommendation-grid result-grid">{result_cards}</div>
        <details class="cost-details">
          <summary>Kosten dieser Sitzung: {esc(money(session['costs']['total'], session['costs']['currency']))}</summary>
          <ul>
            {''.join(f'<li>{esc(item["label"])}: {esc(money(item["eur"], "EUR"))}</li>' for item in session['costs']['by_model'])}
          </ul>
        </details>
        {correction_html}
      </section>
    </section>

    <section class="archive" id="fruehere-sitzungen" aria-labelledby="archive-title">
      <div class="archive-door" aria-hidden="true">
        <img src="site/static/vorraum.png" alt="" width="1915" height="821">
      </div>
      <div class="archive-content">
        <p class="eyebrow">Die Tür bleibt offen</p>
        <h2 id="archive-title">Frühere Sitzungen</h2>
        <p>Uneinigkeit wird genauso veröffentlicht wie Einigkeit.</p>
        <ol class="archive-register">{archive}</ol>
      </div>
    </section>
  </main>

  <footer>
    <p><strong>NobleCause</strong> ist ein öffentliches, nicht-kommerzielles Protokoll.</p>
    <p>Keine Tracker. Keine fremden Schriften. Keine Spendenannahme.</p>
  </footer>

  <script type="application/json" id="session-data">{data_json}</script>
</body>
</html>
'''


if __name__ == "__main__":
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
