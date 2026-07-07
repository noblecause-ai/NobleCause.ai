#!/usr/bin/env python3
"""Orchestrator einer Gremium-Sitzung.

Deterministischer Ablauf (kein LLM steuert den Prozess):
  1. Runde 1 — jedes Modell votiert unabhängig (Manifest + Frage + Quellen).
  2. Runde 2 — jedes Modell liest die Erstvoten der anderen, gibt Schlussvotum
     und Dissens ab.
  3. Protokoll + Rohantworten werden nach sessions/YYYY-MM/ geschrieben.

Aufruf:  python3 run_session.py --question "…" --title "…" [--session-id 2026-07]
Keys:    ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY (oder gremium/.env)
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


# ---------------------------------------------------------------- utilities

def load_env():
    """Minimaler .env-Loader (keine Abhängigkeit).

    Sucht gremium/.env zuerst, dann den Repo-Root als Rückfall."""
    for env_file in (HERE / ".env", ROOT / ".env"):
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"'))


def extract_json_block(text):
    """Letzten ```json-Block aus einer Antwort ziehen."""
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not matches:
        return None
    try:
        return json.loads(matches[-1])
    except json.JSONDecodeError:
        return None


def strip_json_block(text):
    """Antworttext ohne den abschließenden JSON-Zaun (für content_md)."""
    return re.sub(r"```json\s*\{.*?\}\s*```\s*$", "", text, flags=re.DOTALL).strip()


def extract_dissent(text):
    m = re.search(r"##\s*Dissens\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------- API calls

def call_anthropic(model, system, user, max_tokens):
    import anthropic

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    return text, usage, resp.model_dump()


def call_openai(model, system, user, max_tokens):
    from openai import OpenAI

    client = OpenAI()
    resp = client.responses.create(
        model=model,
        max_output_tokens=max_tokens,
        instructions=system,
        input=user,
    )
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    return resp.output_text, usage, resp.model_dump()


def call_google(model, system, user, max_tokens):
    from google import genai
    from google.genai import types

    client = genai.Client()
    resp = client.models.generate_content(
        model=model,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
        ),
    )
    usage = {
        "input_tokens": resp.usage_metadata.prompt_token_count or 0,
        "output_tokens": (resp.usage_metadata.candidates_token_count or 0)
        + (resp.usage_metadata.thoughts_token_count or 0),
    }
    return resp.text, usage, resp.model_dump(mode="json")


CALLERS = {"anthropic": call_anthropic, "openai": call_openai, "google": call_google}


def call_model(spec, system, user, max_tokens, raw_dir, tag):
    """Ein API-Call mit einem Retry; Rohantwort wird immer gespeichert."""
    caller = CALLERS[spec["family"]]
    last_err = None
    for attempt in (1, 2):
        try:
            text, usage, raw = caller(spec["model"], system, user, max_tokens)
            (raw_dir / f"{tag}-{spec['family']}.json").write_text(
                json.dumps(raw, indent=2, ensure_ascii=False, default=str)
            )
            return text, usage
        except Exception as e:  # noqa: BLE001 — Familie egal, wir loggen und retryen einmal
            last_err = e
            print(f"    Versuch {attempt} bei {spec['model']} fehlgeschlagen: {e}", file=sys.stderr)
    raise RuntimeError(f"{spec['model']} nach 2 Versuchen nicht erreichbar") from last_err


# ---------------------------------------------------------------- aggregation

def aggregate_recommendations(final_votes, total_models=None):
    """Deterministische Regel: Nennen ≥2 Modelle im Schlussvotum dieselbe
    Organisation für eine Säule, ist das die Gremium-Empfehlung (Konfidenz =
    Mittelwert). Sonst werden alle Kandidaten der Säule mit Attribution
    gelistet — der Orchestrator urteilt nicht selbst."""
    total = total_models or len(final_votes)
    recs = []
    for pillar in ("A", "B", "C", "D"):
        candidates = []
        for vote in final_votes:
            for r in (vote["parsed"] or {}).get("recommendations", []):
                if r.get("pillar") == pillar:
                    candidates.append({**r, "_model": vote["label"]})
        if not candidates:
            continue
        groups = {}
        for c in candidates:
            key = re.sub(r"[^a-z0-9]", "", (c.get("organization") or "").lower())
            groups.setdefault(key, []).append(c)
        best = max(groups.values(), key=len)
        if len(best) >= 2:
            confs = [c.get("confidence") for c in best if c.get("confidence") is not None]
            recs.append(
                {
                    "pillar": pillar,
                    "has_consensus": True,
                    "title": best[0].get("title"),
                    "organization": best[0].get("organization"),
                    "donation_url": best[0].get("donation_url"),
                    "confidence": round(sum(confs) / len(confs), 2) if confs else None,
                    "convergence": {
                        "count": len(best),
                        "total": total,
                        "models": [c["_model"] for c in best],
                    },
                    "rationale_md": f"Konvergenz im Schlussvotum: {len(best)} von "
                    f"{total} Modellen empfehlen diese Organisation "
                    f"({', '.join(c['_model'] for c in best)}). Begründungen in den Schlussvoten.",
                }
            )
        else:
            recs.append(
                {
                    "pillar": pillar,
                    "has_consensus": False,
                    "title": "Kein Konsens — Einzelvoten",
                    "organization": None,
                    "donation_url": None,
                    "confidence": None,
                    "individual_votes": [
                        {
                            "title": c.get("title"),
                            "organization": c.get("organization"),
                            "donation_url": c.get("donation_url"),
                            "confidence": c.get("confidence"),
                            "model": c["_model"],
                        }
                        for c in candidates
                    ],
                    "rationale_md": "Die Schlussvoten konvergieren für diese Säule nicht "
                    "auf eine Organisation.",
                }
            )
    return recs


def build_dissent(final_votes):
    parts = []
    for vote in final_votes:
        section = extract_dissent(vote["text"])
        if section:
            parts.append(f"**{vote['label']}:** {section}")
    if not parts:
        return "Kein Modell hat im Schlussvotum einen Dissens angemeldet."
    return "\n\n".join(parts)


def format_aggregation_for_summary(recommendations):
    lines = []
    for rec in recommendations:
        if rec.get("has_consensus"):
            conv = rec.get("convergence", {})
            lines.append(
                f"Säule {rec['pillar']}: Konsens — {rec['organization']} "
                f"({conv.get('count', '?')}/{conv.get('total', '?')} Modelle)"
            )
        else:
            votes = rec.get("individual_votes") or []
            parts = [f"{v.get('organization')} ({v.get('model')})" for v in votes]
            lines.append(f"Säule {rec['pillar']}: Kein Konsens — {', '.join(parts)}")
    return "\n".join(lines)


def generate_summary(question, final_votes, recommendations, dissent_md, summarizer, raw_dir):
    """Kurzfassung + Dissens-Kernpunkte per günstigem Claude-Modell."""
    final_excerpt = "\n\n".join(
        f"### {v['label']}\n{strip_json_block(v['text'])[:4000]}" for v in final_votes
    )
    user = prompts.SUMMARY.format(
        question=question,
        final_votes=final_excerpt,
        aggregation=format_aggregation_for_summary(recommendations),
        dissent_md=dissent_md[:6000],
    )
    max_tokens = summarizer.get("max_output_tokens", 1024)
    text, usage, raw = call_anthropic(
        summarizer["model"],
        "Du bist ein nüchterner Protokollredakteur. Antworte nur mit JSON.",
        user,
        max_tokens,
    )
    (raw_dir / "summary-anthropic.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )
    parsed = extract_json_block(text)
    if not parsed or "summary" not in parsed:
        raise RuntimeError("Summarizer lieferte kein gültiges JSON mit summary")
    return parsed.get("summary", ""), parsed.get("dissent_highlights", []), usage


def compute_costs(usage_by_model, model_specs, fx):
    by_model = []
    for spec in model_specs:
        u = usage_by_model.get(spec["model"], {"input_tokens": 0, "output_tokens": 0})
        usd = (
            u["input_tokens"] / 1e6 * spec["usd_per_1m_input"]
            + u["output_tokens"] / 1e6 * spec["usd_per_1m_output"]
        )
        by_model.append(
            {
                "model": spec["model"],
                "label": spec.get("label", spec["model"]),
                "input_tokens": u["input_tokens"],
                "output_tokens": u["output_tokens"],
                "usd": round(usd, 4),
                "eur": round(usd * fx, 4),
            }
        )
    total_eur = round(sum(c["eur"] for c in by_model), 2)
    return {"currency": "EUR", "total": total_eur, "fx_rate_usd_eur": fx, "by_model": by_model}


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--session-id", default=datetime.date.today().strftime("%Y-%m"))
    parser.add_argument("--number", type=int, default=None)
    args = parser.parse_args()

    load_env()
    config = json.loads((HERE / "config.json").read_text())
    manifest = (ROOT / "manifest.md").read_text()
    sources = (HERE / "sources.md").read_text()

    sessions_dir = ROOT / "sessions"
    out_dir = sessions_dir / args.session_id
    if out_dir.exists():
        sys.exit(f"Abbruch: {out_dir} existiert bereits — Protokolle sind unveränderlich.")
    number = args.number or (
        len([d for d in sessions_dir.iterdir() if d.is_dir() and (d / "session.json").exists()]) + 1
    )
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True)

    today = datetime.date.today().isoformat()
    max_tokens = config["max_output_tokens"]
    fx = config["fx_rate_usd_eur"]
    system = prompts.SYSTEM
    round1_prompt = prompts.ROUND1.format(
        manifest=manifest,
        sources=sources,
        number=number,
        date=today,
        question=args.question,
        conflict_rule=prompts.CONFLICT_OF_INTEREST,
    )

    usage_by_model = {m["model"]: {"input_tokens": 0, "output_tokens": 0} for m in config["models"]}

    def record_usage(spec, usage):
        u = usage_by_model[spec["model"]]
        u["input_tokens"] += usage["input_tokens"]
        u["output_tokens"] += usage["output_tokens"]

    # -------- Runde 1
    print("Runde 1 — unabhängige Einzelvoten")
    r1 = []
    for spec in config["models"]:
        print(f"  {spec['label']} ({spec['model']}) …")
        text, usage = call_model(spec, system, round1_prompt, max_tokens, raw_dir, "r1")
        record_usage(spec, usage)
        r1.append({**spec, "text": text, "parsed": extract_json_block(text)})

    # -------- Runde 2
    print("Runde 2 — Gegenlese und Schlussvoten")
    r2 = []
    for spec, own in zip(config["models"], r1):
        others = "\n\n".join(
            f"### Erstvotum {v['label']}\n\n{strip_json_block(v['text'])}"
            for v in r1
            if v["model"] != spec["model"]
        )
        round2_prompt = prompts.ROUND2.format(
            own_vote=strip_json_block(own["text"]),
            other_votes=others,
            conflict_rule=prompts.CONFLICT_OF_INTEREST,
        )
        print(f"  {spec['label']} ({spec['model']}) …")
        text, usage = call_model(spec, system, round2_prompt, max_tokens, raw_dir, "r2")
        record_usage(spec, usage)
        r2.append({**spec, "text": text, "parsed": extract_json_block(text)})

    # -------- Kurzfassung
    print("Kurzfassung — Protokollredaktion")
    dissent_md = build_dissent(r2)
    recommendations = aggregate_recommendations(r2)
    summarizer = config["summarizer"]
    print(f"  {summarizer['label']} ({summarizer['model']}) …")
    summary, dissent_highlights, sum_usage = generate_summary(
        args.question, r2, recommendations, dissent_md, summarizer, raw_dir
    )
    usage_by_model.setdefault(summarizer["model"], {"input_tokens": 0, "output_tokens": 0})
    usage_by_model[summarizer["model"]]["input_tokens"] += sum_usage["input_tokens"]
    usage_by_model[summarizer["model"]]["output_tokens"] += sum_usage["output_tokens"]

    # -------- Kosten
    all_specs = config["models"] + [summarizer]
    costs = compute_costs(usage_by_model, all_specs, fx)

    # -------- Protokoll
    def votes_of(round_votes):
        return [
            {
                "model": v["model"],
                "content_md": strip_json_block(v["text"]),
                "confidence": (v["parsed"] or {}).get("confidence"),
            }
            for v in round_votes
        ]

    session = {
        "schema_version": 2,
        "id": args.session_id,
        "number": number,
        "date": today,
        "title": args.title,
        "question": args.question,
        "summary": summary,
        "dissent_highlights": dissent_highlights,
        "participants": [
            {"family": m["family"], "model": m["model"], "label": m["label"]} for m in config["models"]
        ],
        "prompts": {"system": system, "round1": round1_prompt, "round2": prompts.ROUND2},
        "rounds": [
            {"round": 1, "kind": "initial_vote", "votes": votes_of(r1)},
            {"round": 2, "kind": "final_vote", "votes": votes_of(r2)},
        ],
        "dissent_md": dissent_md,
        "recommendations": recommendations,
        "costs": costs,
    }
    (out_dir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
    print(f"\nProtokoll geschrieben: {out_dir / 'session.json'}")
    print(f"Kosten der Sitzung: {costs['total']} €")


if __name__ == "__main__":
    main()
