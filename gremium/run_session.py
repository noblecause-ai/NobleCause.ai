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
    """Minimaler .env-Loader (keine Abhängigkeit)."""
    env_file = HERE / ".env"
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

def aggregate_recommendations(final_votes):
    """Deterministische Regel: Nennen ≥2 Modelle im Schlussvotum dieselbe
    Organisation für eine Säule, ist das die Gremium-Empfehlung (Konfidenz =
    Mittelwert). Sonst werden alle Kandidaten der Säule mit Attribution
    gelistet — der Orchestrator urteilt nicht selbst."""
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
                    "title": best[0].get("title"),
                    "organization": best[0].get("organization"),
                    "donation_url": best[0].get("donation_url"),
                    "confidence": round(sum(confs) / len(confs), 2) if confs else None,
                    "rationale_md": f"Konvergenz im Schlussvotum: {len(best)} von "
                    f"{len(final_votes)} Modellen empfehlen diese Organisation "
                    f"({', '.join(c['_model'] for c in best)}). Begründungen in den Schlussvoten.",
                }
            )
        else:
            lines = [
                f"- **{c.get('organization')}** — {c.get('title')} "
                f"(Votum {c['_model']}, Konfidenz {c.get('confidence')})"
                for c in candidates
            ]
            recs.append(
                {
                    "pillar": pillar,
                    "title": "Kein Konsens — Einzelvoten",
                    "organization": None,
                    "donation_url": None,
                    "confidence": None,
                    "rationale_md": "Die Schlussvoten konvergieren für diese Säule nicht "
                    "auf eine Organisation:\n" + "\n".join(lines),
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
        manifest=manifest, sources=sources, number=number, date=today, question=args.question
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
        round2_prompt = prompts.ROUND2.format(own_vote=strip_json_block(own["text"]), other_votes=others)
        print(f"  {spec['label']} ({spec['model']}) …")
        text, usage = call_model(spec, system, round2_prompt, max_tokens, raw_dir, "r2")
        record_usage(spec, usage)
        r2.append({**spec, "text": text, "parsed": extract_json_block(text)})

    # -------- Kosten
    by_model = []
    for spec in config["models"]:
        u = usage_by_model[spec["model"]]
        usd = (
            u["input_tokens"] / 1e6 * spec["usd_per_1m_input"]
            + u["output_tokens"] / 1e6 * spec["usd_per_1m_output"]
        )
        by_model.append({"model": spec["model"], **u, "usd": round(usd, 4), "eur": round(usd * fx, 4)})
    total_eur = round(sum(c["eur"] for c in by_model), 2)

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
        "schema_version": 1,
        "id": args.session_id,
        "number": number,
        "date": today,
        "title": args.title,
        "question": args.question,
        "participants": [
            {"family": m["family"], "model": m["model"], "label": m["label"]} for m in config["models"]
        ],
        "prompts": {"system": system, "round1": round1_prompt, "round2": prompts.ROUND2},
        "rounds": [
            {"round": 1, "kind": "initial_vote", "votes": votes_of(r1)},
            {"round": 2, "kind": "final_vote", "votes": votes_of(r2)},
        ],
        "dissent_md": build_dissent(r2),
        "recommendations": aggregate_recommendations(r2),
        "costs": {
            "currency": "EUR",
            "total": total_eur,
            "fx_rate_usd_eur": fx,
            "by_model": by_model,
        },
    }
    (out_dir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
    print(f"\nProtokoll geschrieben: {out_dir / 'session.json'}")
    print(f"Kosten der Sitzung: {total_eur} €")


if __name__ == "__main__":
    main()
