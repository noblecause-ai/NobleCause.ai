#!/usr/bin/env python3
"""§5-Probelauf: liefern alle drei Modellfamilien das strukturierte `conditional`-Feld,
wenn der neue gehärtete Sitzungs-Prompt (ROUND1) es anfordert?

Minimaler Validierungslauf gegen die drei ECHTEN APIs mit der neuen Besetzung. Er
**schreibt nichts** in den Rekord: kein Behälter, keine ID, kein Journal, kein Commit,
keine schedule.json, keine Aggregation, kein Schema-Tor. Nur ein Votum-Call je Modell,
Antwort gegen den neuen Vertrag geprüft, Rohantworten in ein Wegwerf-Verzeichnis.

Aufruf:  python3 probe_conditional.py [--out <dir>]
Ausgabe: JSON-Bericht auf stdout + Rohantworten im out-dir.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import prompts  # noqa: E402
import run_session  # noqa: E402
from envtools import load_env, require_keys  # noqa: E402

# Repräsentative Frage nur zum Auslösen eines echten Votums — nichts wird publiziert.
PROBE_QUESTION = (
    "Wo bewirkt eine Spende von 1.000 EUR je Säule (A Zukunftsinvestition, "
    "B Linderung gegenwärtigen Leids, C Existenzrisiko-Mitigation, D übersehene "
    "Essentials) im Jahr 2026 voraussichtlich am meisten?"
)


def build_round1_prompt():
    manifest = (ROOT / "manifest.md").read_text()
    sources = (HERE / "sources.md").read_text()
    return prompts.ROUND1.format(
        manifest=manifest,
        sources=sources,
        question=PROBE_QUESTION,
        number=4,
        date=datetime.date(2026, 8, 6).isoformat(),
        opening_section="",
        dossier_section="",
    )


def check_vote(parsed):
    """Prüft eine Modellantwort gegen den neuen conditional-Vertrag."""
    if not parsed:
        return {"json_block": False, "recommendations": 0, "recs": [], "all_ok": False}
    recs = parsed.get("recommendations") or parsed.get("empfehlungen") or []
    out = []
    for r in recs:
        val = r.get("conditional", "<fehlt>")
        out.append({
            "pillar": r.get("pillar"),
            "has_conditional": "conditional" in r,
            "is_json_bool": isinstance(r.get("conditional"), bool),
            "value": val if isinstance(val, bool) else repr(val),
            "reservation_type": type(r.get("reservation")).__name__,
        })
    all_ok = bool(recs) and all(c["is_json_bool"] for c in out)
    return {"json_block": True, "recommendations": len(recs), "recs": out, "all_ok": all_ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    load_env(HERE, ROOT)
    require_keys("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY")

    out_dir = Path(args.out) if args.out else HERE / ".probe-raw"
    out_dir.mkdir(parents=True, exist_ok=True)

    config = json.loads((HERE / "config.json").read_text())
    system = prompts.SYSTEM_WITH_CONFLICT
    max_tokens = config["max_output_tokens"]
    round1_prompt = build_round1_prompt()
    (out_dir / "prompt-round1.txt").write_text(round1_prompt)

    report = {"question": PROBE_QUESTION, "models": []}
    for spec in config["models"]:
        entry = {"family": spec["family"], "model": spec["model"], "label": spec["label"]}
        try:
            text, usage = run_session.call_model(spec, system, round1_prompt, max_tokens, out_dir, "probe")
            (out_dir / f"probe-{spec['family']}-content.md").write_text(text)
            parsed = run_session.extract_json_block(text)
            entry["reachable"] = True
            entry.update(check_vote(parsed))
        except Exception as e:  # noqa: BLE001
            entry["reachable"] = False
            entry["error"] = str(e)
            entry["all_ok"] = False
        report["models"].append(entry)

    report["verdict"] = "ALLE liefern conditional als JSON-Boolean" if all(
        m.get("all_ok") for m in report["models"]
    ) else "AUSFALL — mindestens ein Modell liefert das Feld nicht korrekt"
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
