#!/usr/bin/env python3
"""Wöchentlicher Research-Lauf: Scout recherchiert, Wart entscheidet.

Liest die jüngste session.json, recherchiert die Evidenzlage, schreibt
journal/YYYY-MM-DD/entry.json und aktualisiert schedule.json am Repo-Root.

Aufruf:  python3 run_wart.py [--date YYYY-MM-DD]
Keys:    ANTHROPIC_API_KEY (oder gremium/.env / Repo-Root .env)
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

import prompts  # noqa: E402
from envtools import load_env, require_keys  # noqa: E402


def extract_json_block(text):
    """Letzten ```json-Block ziehen; balancierte Klammern für verschachteltes JSON."""
    start = text.rfind("```json")
    if start == -1:
        return None
    body = text[start + 7 :]
    end_fence = body.find("```")
    if end_fence != -1:
        body = body[:end_fence]
    body = body.strip()
    if not body.startswith("{"):
        brace = body.find("{")
        if brace == -1:
            return None
        body = body[brace:]
    depth = 0
    for i, ch in enumerate(body):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(body[: i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def strip_json_block(text):
    return re.sub(r"```json\s*\{.*?\}\s*```\s*$", "", text, flags=re.DOTALL).strip()


def parse_scout_answer(text):
    """Strikter Datenvertrag des Recherche-Zulieferers, ohne Governance-Entscheid."""
    parsed = extract_json_block(text)
    if not parsed:
        sys.exit(
            "Abbruch: kein strukturierter JSON-Block in der Scout-Antwort — "
            "Rohartefakte gesichert, kein Journal-Eintrag."
        )
    if not parsed.get("delta_assessment"):
        sys.exit("Abbruch: Scout-Dossier ohne delta_assessment — kein Journal-Eintrag.")
    for field in ("search_queries", "findings", "rejected_findings"):
        if not isinstance(parsed.get(field), list):
            sys.exit(f"Abbruch: Scout-Feld {field} ist keine Liste — kein Journal-Eintrag.")
    if "convene" in parsed or "convene_rationale" in parsed:
        sys.exit("Abbruch: Scout hat eine Governance-Entscheidung abgegeben — Rollenbruch.")
    return parsed


def parse_wart_decision(text):
    """Der Wart entscheidet nur über die Einberufung; Prosa wird nie geraten."""
    parsed = extract_json_block(text)
    if not parsed:
        sys.exit("Abbruch: kein strukturierter JSON-Block im Wart-Entscheid.")
    if not isinstance(parsed.get("convene"), bool):
        raw = parsed.get("convene")
        sys.exit(
            f"Abbruch: Wart-Feld convene ist kein JSON-Boolean (Wert {raw!r}, "
            f"Typ {type(raw).__name__})."
        )
    if not isinstance(parsed.get("convene_rationale"), str) or not parsed["convene_rationale"].strip():
        sys.exit("Abbruch: Wart-Entscheid ohne convene_rationale.")
    return parsed


def latest_session():
    sessions_dir = ROOT / "sessions"
    entries = []
    for d in sessions_dir.iterdir():
        if not d.is_dir():
            continue
        f = d / "session.json"
        if f.exists():
            s = json.loads(f.read_text())
            entries.append((s.get("number", 0), s.get("date", ""), d.name, s))
    if not entries:
        sys.exit("Abbruch: keine session.json gefunden.")
    # Sortierschlüssel (number, date) — identisch zu run_session.prior_session()
    # und content.js. NICHT nach Datumsstring allein: alle Bestandssitzungen tragen
    # dasselbe Datum (2026-07-07), die Reihenfolge der Gleichen hinge sonst von
    # iterdir() (der Dateisystemreihenfolge des Runners) ab — genau so recherchierte
    # der Wart am 20./27.07. gegen die überholte Sitzung 1.
    entries.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return entries[0][2], entries[0][3]


def assert_current_session(session_id):
    """Hartes Aktualitäts-Gate: die Sitzung, auf die der Journal-Eintrag zeigen wird
    (session_ref), MUSS die höchste Sitzungsnummer tragen. Unabhängig von
    latest_session() neu hergeleitet — fängt auch künftige Ursachen derselben Wirkung
    laut ab, statt eine überholte Sitzung still als „geprüft" zu publizieren. Der Wart
    nennt dieses Gate ausdrücklich wichtiger als die Sortierung selbst."""
    sessions_dir = ROOT / "sessions"
    numbers = {}
    for d in sessions_dir.iterdir():
        if not d.is_dir():
            continue
        f = d / "session.json"
        if f.exists():
            numbers[d.name] = json.loads(f.read_text()).get("number", 0)
    if not numbers:
        sys.exit("Abbruch: keine session.json für das Aktualitäts-Gate gefunden.")
    # Fix 3 (Codex): Sitzungsnummern MÜSSEN eindeutig sein. Eine doppelt vergebene
    # Nummer ist immer ein Fehler — nicht nur, wenn sie die höchste betrifft: bei
    # doppelter höchster Nummer bestünden beide den max-Check, und die Auswahl hinge
    # wieder an iterdir(). Genau diese Kollision (gleiche Kennung) ist beim Journal
    # real vorgekommen. Darum vor dem Max-Vergleich hart abbrechen.
    by_number = {}
    for sid, num in numbers.items():
        by_number.setdefault(num, []).append(sid)
    dupes = {num: sorted(sids) for num, sids in by_number.items() if len(sids) > 1}
    if dupes:
        sys.exit(
            f"Abbruch (Aktualitäts-Gate): mehrfach vergebene Sitzungsnummer(n) {dupes} — "
            f"Sitzungsnummern müssen eindeutig sein."
        )
    max_number = max(numbers.values())
    chosen = numbers.get(session_id)
    if chosen is None:
        sys.exit(f"Abbruch (Aktualitäts-Gate): session_ref {session_id!r} hat keine session.json.")
    if chosen != max_number:
        current = sorted(n for n, num in numbers.items() if num == max_number)
        sys.exit(
            f"Abbruch (Aktualitäts-Gate): session_ref {session_id!r} (Nummer {chosen}) ist "
            f"nicht die höchste Sitzung (Nummer {max_number}: {current}). Kein Journal-"
            f"Eintrag — er würde eine überholte Sitzung als geprüft ausweisen."
        )


def summarize_recommendations(session):
    lines = []
    for rec in session.get("recommendations", []):
        pillar = rec.get("pillar", "?")
        if rec.get("has_consensus"):
            lines.append(
                f"- Säule {pillar} (Konsens): {rec.get('title')} — "
                f"{rec.get('organization')} (Konfidenz {rec.get('confidence')})"
            )
        else:
            lines.append(f"- Säule {pillar} (kein Konsens):")
            for v in rec.get("individual_votes") or []:
                lines.append(
                    f"  · {v.get('organization')} — {v.get('title')} "
                    f"({v.get('model')}, Konfidenz {v.get('confidence')})"
                )
    return "\n".join(lines)


def count_web_searches(raw):
    usage = raw.get("usage") or {}
    server = usage.get("server_tool_use") or {}
    return server.get("web_search_requests", 0)


def extract_search_queries_from_raw(raw):
    queries = []
    for block in raw.get("content") or []:
        if block.get("type") == "server_tool_use" and block.get("name") == "web_search":
            inp = block.get("input") or {}
            q = inp.get("query")
            if q:
                queries.append(q)
    return queries


def next_monday_0600_utc(after: datetime.datetime) -> datetime.datetime:
    """Nächster Montag 06:00 UTC strikt nach `after`."""
    candidate = after.replace(hour=6, minute=0, second=0, microsecond=0)
    days_ahead = (0 - candidate.weekday()) % 7
    if days_ahead == 0 and candidate <= after:
        days_ahead = 7
    return candidate + datetime.timedelta(days=days_ahead)


def next_regular_session(session_date: str, convene: bool) -> str:
    base = datetime.date.fromisoformat(session_date)
    regular = base + datetime.timedelta(days=30)
    if convene:
        sooner = datetime.date.today() + datetime.timedelta(days=7)
        return min(regular, sooner).isoformat() + "T12:00:00Z"
    return regular.isoformat() + "T12:00:00Z"


def actions_run_url():
    repo = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    if repo and run_id:
        return f"https://github.com/{repo}/actions/runs/{run_id}"
    return None


def call_scout(scout_cfg, system, user, raw_dir):
    import anthropic

    client = anthropic.Anthropic()
    max_uses = scout_cfg.get("max_web_search_uses", 15)
    print(f"  Modell: {scout_cfg['model']}")
    print(f"  Web-Suche: max. {max_uses} Anfragen")
    print("  Starte API-Call …")

    # Streaming ist Pflicht: bei hohem max_output_tokens (langes Dossier +
    # Web-Suche) veranschlagt das SDK >10 min und verweigert den nicht-
    # gestreamten Call. get_final_message() akkumuliert die volle Antwort.
    with client.messages.stream(
        model=scout_cfg["model"],
        max_tokens=scout_cfg.get("max_output_tokens", 8192),
        system=system,
        messages=[{"role": "user", "content": user}],
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": max_uses,
                "allowed_callers": ["direct"],
            }
        ],
    ) as stream:
        resp = stream.get_final_message()
    raw = resp.model_dump()
    (raw_dir / "scout-response.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )

    text = "".join(b.text for b in resp.content if b.type == "text")
    usage = {
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "web_search_requests": count_web_searches(raw),
    }
    api_queries = extract_search_queries_from_raw(raw)
    if api_queries:
        print("  Suchanfragen (API):")
        for q in api_queries:
            print(f"    · {q}")
    print(
        f"  Tokens: {usage['input_tokens']} in / {usage['output_tokens']} out · "
        f"Suchen: {usage['web_search_requests']}"
    )
    return text, usage, raw, api_queries


def call_wart_decision(wart_cfg, system, user, raw_dir):
    import anthropic

    client = anthropic.Anthropic()
    print(f"  Modell: {wart_cfg['model']}")
    with client.messages.stream(
        model=wart_cfg["model"],
        max_tokens=min(wart_cfg.get("max_output_tokens", 2048), 2048),
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        resp = stream.get_final_message()
    raw = resp.model_dump()
    (raw_dir / "wart-decision-response.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )
    if raw.get("stop_reason") != "end_turn":
        sys.exit(
            f"Abbruch: Wart-Entscheid stop_reason={raw.get('stop_reason')} — "
            "keine Einberufung wird geraten."
        )
    text = "".join(b.text for b in resp.content if b.type == "text")
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    return text, usage, raw


def compute_role_costs(usage, cfg, fx):
    token_usd = (
        usage["input_tokens"] / 1e6 * cfg["usd_per_1m_input"]
        + usage["output_tokens"] / 1e6 * cfg["usd_per_1m_output"]
    )
    search_usd = (
        usage.get("web_search_requests", 0) / 1000 * cfg.get("usd_per_1k_web_searches", 10.0)
    )
    total_usd = token_usd + search_usd
    return {
        "currency": "EUR",
        "total": round(total_usd * fx, 4),
        "fx_rate_usd_eur": fx,
        "model": cfg["model"],
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "web_search_requests": usage.get("web_search_requests", 0),
        "usd_tokens": round(token_usd, 4),
        "usd_web_search": round(search_usd, 4),
        "usd_total": round(total_usd, 4),
    }


def compute_run_costs(scout_usage, scout_cfg, wart_usage, wart_cfg, fx):
    scout = compute_role_costs(scout_usage, scout_cfg, fx)
    wart = compute_role_costs(wart_usage, wart_cfg, fx)
    return {
        "currency": "EUR",
        "total": round(scout["total"] + wart["total"], 4),
        "fx_rate_usd_eur": fx,
        "components": {"scout": scout, "wart": wart},
    }


def write_schedule(entry_date, session_date, convene, journal_path):
    now = datetime.datetime.now(datetime.timezone.utc)
    next_research = next_monday_0600_utc(now)
    next_session = next_regular_session(session_date, convene)
    schedule = {
        "next_research": next_research.replace(tzinfo=datetime.timezone.utc).isoformat().replace(
            "+00:00", "Z"
        ),
        "next_session": next_session,
        "last_journal": f"/journal/{entry_date}/",
    }
    (ROOT / "schedule.json").write_text(json.dumps(schedule, indent=2, ensure_ascii=False) + "\n")
    print(f"schedule.json aktualisiert (nächster Research: {schedule['next_research']})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    args = parser.parse_args()

    load_env(HERE, ROOT)
    require_keys("ANTHROPIC_API_KEY")

    config = json.loads((HERE / "config.json").read_text())
    scout_cfg = config.get("scout")
    wart_cfg = config.get("wart")
    if not scout_cfg or not wart_cfg:
        sys.exit("Abbruch: scout und wart müssen getrennt in config.json konfiguriert sein.")
    if scout_cfg["model"] == wart_cfg["model"]:
        sys.exit("Abbruch: Scout und Wart dürfen nicht dasselbe Modell sein.")

    session_id, session = latest_session()
    # Aktualitäts-Gate VOR Verzeichnis-Anlage und API-Call: eine falsche session_ref
    # bricht laut ab, bevor Kosten entstehen oder ein Eintrag geschrieben wird.
    assert_current_session(session_id)
    entry_date = args.date
    out_dir = ROOT / "journal" / entry_date
    if out_dir.exists():
        # Idempotenz (P10): ein zweiter Lauf am selben Tag darf den unveränderlichen
        # Eintrag nicht überschreiben — der Abbruch bleibt. Aber ein vorhandenes
        # Tagesjournal ist KEIN Defekt, sondern ein No-op: sauberer Exit 0 mit klarer
        # Meldung im Log, damit der Workflow keinen CI-Alarm (`if: failure()`) auslöst.
        # Bewusst KEIN pauschales `|| true`/`continue-on-error`: Exit 0 ist das eng
        # umrissene Erfolgssignal genau dieses Sonderfalls; jeder andere Abbruch in
        # dieser Datei bleibt `sys.exit(!=0)` und schlägt weiterhin als Fehler durch.
        print(f"Nichts zu tun: {out_dir} existiert bereits — Journal-Eintrag ist unveränderlich, kein neuer Lauf.")
        sys.exit(0)
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True)

    print("=== NobleCause Wart-Lauf ===")
    print(f"Datum: {entry_date}")
    print(f"Jüngste Sitzung: {session_id} ({session.get('date')})")

    user = prompts.SCOUT_USER.format(
        session_id=session_id,
        session_date=session.get("date"),
        question=session.get("question"),
        recommendations_summary=summarize_recommendations(session),
    )
    (raw_dir / "prompt-user.txt").write_text(user)

    print("\nSchritt 1 — Web-Recherche (Scout)")
    text, scout_usage, raw, api_queries = call_scout(
        scout_cfg, prompts.SCOUT_SYSTEM, user, raw_dir
    )
    (raw_dir / "scout-content.md").write_text(text)

    # Nur end_turn ist eine vollständige Antwort. Jeder andere stop_reason
    # (refusal, max_tokens, pause_turn, …) heißt: unvollständig/abnormal → laut
    # abbrechen mit dem echten Grund, NICHT in den ratenden Parser laufen (der
    # sonst leere/geratene Inhalte publiziert). Rohantwort ist bereits gesichert.
    stop_reason = raw.get("stop_reason")
    print(f"  stop_reason: {stop_reason}")
    if stop_reason != "end_turn":
        hint = {
            "refusal": "Modell hat die Ausgabe verweigert (Content/Safety) — "
            "Thema/Prompt redaktionell prüfen.",
            "max_tokens": "Antwort abgeschnitten — max_output_tokens (config.json scout) erhöhen.",
            "pause_turn": "Turn pausiert (Server-Tool) — unerwartet nach Streaming.",
        }.get(stop_reason, "unerwarteter Abbruch.")
        sys.exit(f"Abbruch: stop_reason={stop_reason} — {hint} Kein Parse-Versuch.")

    print("\nSchritt 2 — Scout-Dossier prüfen")
    parsed = parse_scout_answer(text)

    search_queries = parsed.get("search_queries") or api_queries
    print("  Suchanfragen (Dossier):")
    for q in search_queries:
        print(f"    · {q}")

    decision_user = prompts.WART_DECISION_USER.format(
        session_id=session_id,
        session_date=session.get("date"),
        scout_dossier=text,
    )
    (raw_dir / "prompt-wart-decision.txt").write_text(decision_user)
    print("\nSchritt 3 — Einberufungs-Entscheid (Wart)")
    decision_text, wart_usage, _ = call_wart_decision(
        wart_cfg, prompts.WART_DECISION_SYSTEM, decision_user, raw_dir
    )
    (raw_dir / "wart-decision-content.md").write_text(decision_text)
    decision = parse_wart_decision(decision_text)
    convene = decision["convene"]
    print(f"  Einberufung: {'JA' if convene else 'NEIN'}")
    print(f"  Begründung: {decision['convene_rationale']}")

    run_url = actions_run_url()
    costs = compute_run_costs(
        scout_usage, scout_cfg, wart_usage, wart_cfg, config["fx_rate_usd_eur"]
    )

    entry = {
        "schema_version": 1,
        "date": entry_date,
        "session_ref": session_id,
        "model": scout_cfg["model"],
        "model_label": scout_cfg.get("model_label", scout_cfg.get("label", scout_cfg["model"])),
        "decision_model": wart_cfg["model"],
        "search_queries": search_queries,
        "findings": parsed.get("findings", []),
        "rejected_findings": parsed.get("rejected_findings", []),
        "delta_assessment": parsed.get("delta_assessment", ""),
        "convene": convene,
        "convene_rationale": decision["convene_rationale"],
        "content_md": strip_json_block(text),
        "costs": costs,
        "actions_run_url": run_url,
    }
    (out_dir / "entry.json").write_text(json.dumps(entry, indent=2, ensure_ascii=False))
    print(f"\nJournal geschrieben: {out_dir / 'entry.json'}")
    print(f"Kosten des Laufs: {costs['total']} €")

    print("\nSchritt 4 — schedule.json")
    write_schedule(entry_date, session.get("date"), convene, out_dir)
    print("\n=== Wart-Lauf abgeschlossen ===")


if __name__ == "__main__":
    main()
