#!/usr/bin/env python3
"""Re-Aggregation der bestehenden Sitzungen aus den Roh-Schlussvoten.

Rechnet `recommendations` je Sitzung mit der neuen Registry-Aggregation NEU —
aus den committeten `sessions/<id>/raw/r2-*.json` (dort liegt das volle Roh-JSON
aller drei Anbieter). **Kein Umschreiben von Voten**: nur `recommendations` (+
`unresolved_votes`) werden ersetzt; `rounds`, `summary`, `dissent_md` bleiben.

Default: Dry-Run, zeigt nur den Diff. `--write` schreibt (erst nach Freigabe).

Aufruf:  python3 gremium/reaggregate.py [--write] [session-id ...]
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

from run_session import extract_json_block, aggregate_recommendations  # noqa: E402

# Deterministischer Korrektur-Vermerk (AUFLAGE 2). Wird NUR gesetzt, keine
# redaktionelle Prosa (summary/dissent_md) wird je angefasst. {commit} wird nach
# dem Commit durch den SHA der Re-Aggregation ersetzt (Platzhalter unten).
CORRECTION_DATE = "2026-07-14"
CORRECTION_COMMIT_PLACEHOLDER = "⟪COMMIT⟫"
CORRECTION_TEXT = (
    "Korrektur vom 14.07.2026: Die Aggregation dieser Sitzung war fehlerhaft. "
    "Organisationsnamen wurden per Zeichenkette verglichen, wodurch identische "
    "Organisationen als Dissens gewertet wurden; zusätzlich wurden die Voten eines "
    "Modells wegen abweichender Feldnamen nicht erfasst. Die Empfehlungen unten sind "
    "korrigiert. Kurzfassung und Dissens-Text stammen unverändert aus dem Originallauf "
    "und können der korrigierten Aggregation widersprechen. Diff: "
    + CORRECTION_COMMIT_PLACEHOLDER + "."
)


def text_of(raw, family):
    """Anbieter-spezifische Text-Extraktion aus einem model_dump()."""
    if family == "anthropic":
        return "".join(b.get("text", "") for b in raw.get("content", []) if b.get("type") == "text")
    if family == "openai":
        out = []
        for o in raw.get("output", []) or []:
            if o.get("type") == "message":
                for c in o.get("content", []) or []:
                    if c.get("type") == "output_text":
                        out.append(c.get("text", ""))
        return "".join(out)
    if family == "google":
        cands = raw.get("candidates") or []
        if not cands:
            return ""
        parts = cands[0].get("content", {}).get("parts", []) or []
        return "".join(p.get("text", "") for p in parts if p.get("text") and not p.get("thought"))
    return ""


def final_votes_from_raw(session_dir, session):
    """Baut die final_votes-Struktur (label/parsed) aus raw/r2-*.json."""
    label_by_family = {p["family"]: p["label"] for p in session.get("participants", [])}
    votes = []
    for rawf in sorted(glob.glob(str(session_dir / "raw" / "r2-*.json"))):
        family = os.path.basename(rawf).replace("r2-", "").replace(".json", "")
        raw = json.load(open(rawf))
        text = text_of(raw, family)
        votes.append({
            "label": label_by_family.get(family, family),
            "parsed": extract_json_block(text),
        })
    return votes


def summarize(rec):
    if rec.get("has_consensus"):
        conv = rec.get("convergence", {})
        return f"KONSENS  {rec['organization']}  [{conv.get('count')}/{conv.get('total')}: {', '.join(conv.get('models', []))}]  -> {rec.get('donation_url')}"
    votes = rec.get("individual_votes") or []
    return "kein Konsens  (" + "; ".join(f"{v['organization']}/{v['model']}" for v in votes) + ")"


def diff_session(sid, write):
    session_dir = ROOT / "sessions" / sid
    session = json.loads((session_dir / "session.json").read_text())
    votes = final_votes_from_raw(session_dir, session)
    new_recs, unresolved = aggregate_recommendations(votes)
    old_by_pillar = {r["pillar"]: r for r in session.get("recommendations", [])}
    new_by_pillar = {r["pillar"]: r for r in new_recs}

    print(f"\n=== {sid} ===")
    changed = False
    for pillar in ("A", "B", "C", "D"):
        old = old_by_pillar.get(pillar)
        new = new_by_pillar.get(pillar)
        if not old and not new:
            continue
        os_, ns = (summarize(old) if old else "—"), (summarize(new) if new else "—")
        flip = (bool(old and old.get("has_consensus")) != bool(new and new.get("has_consensus"))) \
            or ((old or {}).get("organization") != (new or {}).get("organization"))
        mark = "  <<< ÄNDERUNG" if flip else ""
        if flip:
            changed = True
        print(f"  Säule {pillar}:{mark}")
        print(f"    ALT: {os_}")
        print(f"    NEU: {ns}")
    if unresolved:
        print(f"  ! nicht zuordenbar: {unresolved}")
    if write:
        session["recommendations"] = new_recs
        session["unresolved_votes"] = unresolved
        if changed:
            # Vermerk nur bei tatsächlich geänderten Empfehlungen; die publizierte
            # Prosa bleibt unangetastet.
            session["correction_notice"] = {"date": CORRECTION_DATE, "text": CORRECTION_TEXT}
        (session_dir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
        print(f"  → session.json geschrieben ({sid}{', mit Korrektur-Vermerk' if changed else ''})")
    return changed


def backfill_votes(sid, write):
    """Ergänzt rounds[].votes[].recommendations[] deterministisch aus den
    committeten Rohvoten (raw/r1-*, raw/r2-*). Fügt nur ein maschinell abgeleitetes
    Struktur-Feld hinzu — ändert KEINEN Text (content_md/summary/dissent bleiben)."""
    from run_session import structured_vote_recs
    session_dir = ROOT / "sessions" / sid
    session = json.loads((session_dir / "session.json").read_text())
    family_by_model = {p["model"]: p["family"] for p in session.get("participants", [])}
    phase = {"initial_vote": "r1", "final_vote": "r2"}
    changed = False
    for rd in session.get("rounds", []):
        prefix = phase.get(rd.get("kind"))
        if not prefix:
            continue
        for v in rd.get("votes", []):
            fam = family_by_model.get(v["model"])
            rawf = session_dir / "raw" / f"{prefix}-{fam}.json"
            if not fam or not rawf.exists():
                print(f"  WARN {sid} {rd['kind']} {v['model']}: kein Rohvotum ({rawf.name})")
                continue
            recs = structured_vote_recs(extract_json_block(text_of(json.load(open(rawf)), fam)))
            if v.get("recommendations") != recs:
                v["recommendations"] = recs
                changed = True
    print(f"  {sid}: {'Voten strukturiert ergänzt' if changed else 'unverändert'}")
    if write and changed:
        (session_dir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
        print(f"  → geschrieben ({sid})")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="session.json tatsächlich schreiben (sonst Dry-Run)")
    ap.add_argument("--backfill-votes", action="store_true",
                    help="rounds[].votes[].recommendations[] aus Rohvoten ergänzen (Struktur, kein Text)")
    ap.add_argument("sessions", nargs="*", help="Session-IDs (Default: alle)")
    args = ap.parse_args()
    organizations_check()
    ids = args.sessions or sorted(
        d.name for d in (ROOT / "sessions").iterdir()
        if d.is_dir() and (d / "session.json").exists()
    )
    any_changed = False
    for sid in ids:
        if args.backfill_votes:
            any_changed |= backfill_votes(sid, args.write)
        else:
            any_changed |= diff_session(sid, args.write)
    print("\n" + ("Änderungen vorhanden." if any_changed else "Keine Änderungen."))
    if not args.write:
        print("Dry-Run — nichts geschrieben. Mit --write anwenden (erst nach Freigabe).")


def organizations_check():
    import organizations
    organizations.load_registry(ROOT / "organizations.json")  # Alias-Kollisionen früh melden


if __name__ == "__main__":
    main()
