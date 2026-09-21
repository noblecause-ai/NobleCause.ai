"""Context boundary for fresh research and the subsequent archive comparison."""

import datetime
import json

import prompts


def blind_research(scouts):
    return bool(scouts) and all(s.get("research_context") == "blind" for s in scouts)


def historical_comparison(root, as_of, session_id, session):
    """Read only after Scouts finish; retain exact findings and source paths.

    Scope: the preceding session and structured journal findings dated before
    the research day. No raw responses, credentials, or cross-project files.
    Missing structured findings are not reconstructed from published prose.
    """
    cutoff = datetime.date.fromisoformat(as_of)
    journals = []
    for path in sorted((root / "journal").glob("*/entry.json")):
        entry = json.loads(path.read_text())
        if datetime.date.fromisoformat(entry["date"]) >= cutoff:
            continue
        if entry.get("findings"):
            journals.append({
                "path": str(path.relative_to(root)),
                "date": entry["date"],
                "findings": entry["findings"],
            })
    history = {
        "scope": "Vorgängersitzung und strukturierte Journal-Findings vor dem Recherchetag; keine Prosa-Auswertung",
        "before": as_of,
        "session": {
            "path": f"sessions/{session_id}/session.json",
            "date": session.get("date"),
            "recommendations": session.get("recommendations", []),
        } if session else None,
        "journals": journals,
    }
    return prompts.SCOUT_HISTORY_COMPARISON.format(
        history_json=json.dumps(history, indent=2, ensure_ascii=False)
    )
