#!/usr/bin/env python3
"""Wöchentlicher Research-Lauf des Warts (Fable + Web-Suche).

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


def fallback_from_markdown(text):
    """Strukturierte Felder aus dem Dossier-Text, falls der JSON-Zaun unvollständig ist."""
    convene = bool(re.search(r"einberufen\.?\s*\*\*ja", text, re.I)) or bool(
        re.search(r"\*\*Einberufen\*\*", text, re.I)
    )
    if re.search(r"\*\*Nicht einberufen\*\*|Nicht einberufen\.", text, re.I):
        convene = False
    delta_m = re.search(r"## 4\. Delta-Bewertung\s*\n\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    convene_m = re.search(r"## 5\. Einberufungs-Entscheid\s*\n\n(.*?)(?=\n```|\Z)", text, re.DOTALL)
    queries = re.findall(r"^\s*·\s+(.+)$", text, re.MULTILINE)
    if not queries:
        queries = re.findall(r'^\s*"([^"]+)"\s*,?\s*$', text, re.MULTILINE)
    return {
        "search_queries": queries[:20],
        "findings": [],
        "rejected_findings": [],
        "delta_assessment": delta_m.group(1).strip() if delta_m else "",
        "convene": convene,
        "convene_rationale": convene_m.group(1).strip() if convene_m else "",
    }


def strip_json_block(text):
    return re.sub(r"```json\s*\{.*?\}\s*```\s*$", "", text, flags=re.DOTALL).strip()


def latest_session():
    sessions_dir = ROOT / "sessions"
    entries = []
    for d in sessions_dir.iterdir():
        if not d.is_dir():
            continue
        f = d / "session.json"
        if f.exists():
            s = json.loads(f.read_text())
            entries.append((s.get("date", ""), d.name, s))
    if not entries:
        sys.exit("Abbruch: keine session.json gefunden.")
    entries.sort(key=lambda x: x[0], reverse=True)
    return entries[0][1], entries[0][2]


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


def call_wart(wart_cfg, system, user, raw_dir):
    import anthropic

    client = anthropic.Anthropic()
    max_uses = wart_cfg.get("max_web_search_uses", 15)
    print(f"  Modell: {wart_cfg['model']}")
    print(f"  Web-Suche: max. {max_uses} Anfragen")
    print("  Starte API-Call …")

    resp = client.messages.create(
        model=wart_cfg["model"],
        max_tokens=wart_cfg.get("max_output_tokens", 8192),
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
    )
    raw = resp.model_dump()
    (raw_dir / "wart-response.json").write_text(
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


def compute_wart_costs(usage, wart_cfg, fx):
    token_usd = (
        usage["input_tokens"] / 1e6 * wart_cfg["usd_per_1m_input"]
        + usage["output_tokens"] / 1e6 * wart_cfg["usd_per_1m_output"]
    )
    search_usd = (
        usage.get("web_search_requests", 0) / 1000 * wart_cfg.get("usd_per_1k_web_searches", 10.0)
    )
    total_usd = token_usd + search_usd
    return {
        "currency": "EUR",
        "total": round(total_usd * fx, 4),
        "fx_rate_usd_eur": fx,
        "model": wart_cfg["model"],
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "web_search_requests": usage.get("web_search_requests", 0),
        "usd_tokens": round(token_usd, 4),
        "usd_web_search": round(search_usd, 4),
        "usd_total": round(total_usd, 4),
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
    wart_cfg = config.get("wart")
    if not wart_cfg:
        sys.exit("Abbruch: kein wart-Eintrag in config.json.")

    session_id, session = latest_session()
    entry_date = args.date
    out_dir = ROOT / "journal" / entry_date
    if out_dir.exists():
        sys.exit(f"Abbruch: {out_dir} existiert bereits — Journal-Einträge sind unveränderlich.")
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True)

    print("=== NobleCause Wart-Lauf ===")
    print(f"Datum: {entry_date}")
    print(f"Jüngste Sitzung: {session_id} ({session.get('date')})")

    user = prompts.WART_USER.format(
        session_id=session_id,
        session_date=session.get("date"),
        question=session.get("question"),
        recommendations_summary=summarize_recommendations(session),
    )
    (raw_dir / "prompt-user.txt").write_text(user)

    print("\nSchritt 1 — Web-Recherche (Fable)")
    text, usage, raw, api_queries = call_wart(
        wart_cfg, prompts.WART_SYSTEM, user, raw_dir
    )
    (raw_dir / "wart-content.md").write_text(text)

    print("\nSchritt 2 — JSON extrahieren")
    parsed = extract_json_block(text)
    if not parsed:
        print("  Warnung: JSON unvollständig — Fallback aus Dossier-Text")
        parsed = fallback_from_markdown(text)
    if not parsed.get("delta_assessment"):
        sys.exit("Abbruch: kein auswertbares Dossier in der Wart-Antwort.")

    search_queries = parsed.get("search_queries") or api_queries
    print("  Suchanfragen (Dossier):")
    for q in search_queries:
        print(f"    · {q}")

    convene = bool(parsed.get("convene"))
    print(f"\nSchritt 3 — Einberufung: {'JA' if convene else 'NEIN'}")
    print(f"  Begründung: {parsed.get('convene_rationale', '—')}")

    run_url = actions_run_url()
    costs = compute_wart_costs(usage, wart_cfg, config["fx_rate_usd_eur"])

    entry = {
        "schema_version": 1,
        "date": entry_date,
        "session_ref": session_id,
        "model": wart_cfg["model"],
        "search_queries": search_queries,
        "findings": parsed.get("findings", []),
        "rejected_findings": parsed.get("rejected_findings", []),
        "delta_assessment": parsed.get("delta_assessment", ""),
        "convene": convene,
        "convene_rationale": parsed.get("convene_rationale", ""),
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
