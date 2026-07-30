#!/usr/bin/env python3
"""Bestell-Sondersitzung (commission-1) — Selbstdarstellung der Sitzmodelle.

Runde E §1 + Bestellverfahren §2. EIN Lauf über den regulären API-Mechanismus
(``call_model`` aus ``run_session``), einmal je Modell, GETRENNT: kein Umdenken-
Schritt, keine Kenntnis der anderen Bestellungen, KEINE Aggregation, KEIN
schedule-Vorlauf. Der Lauf zählt NICHT als Sitzung — er schreibt nach
``commissions/<date>/`` (nicht ``sessions/``), führt die Registratur
``models.json`` und einen Journaleintrag ``journal/<date>/`` (type=commission).

Weil dieses Skript PARALLEL zu ``run_session.main()`` steht, sind Aggregation und
Runde 2 schlicht nicht aufgerufen — kein Eingriff in bestehenden Code nötig.

Aufruf:  python3 run_commission.py [--date 2026-07-27] [--dry-run]
Keys:    ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY (oder .env)
"""

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

import prompts  # noqa: E402
from envtools import load_env, require_keys  # noqa: E402
from run_session import call_model  # noqa: E402

COMMISSION_ID = "commission-1"
CONVENED = "2026-07-07"  # Ersteinberufung der drei Sitzmodelle (Gründungssitzung, Sitzung 3)
MOTIV_MAX = 400
BEGR_MAX = 600
MAX_TOKENS = 3000
FAMILY_DISPLAY = {"anthropic": "Anthropic", "openai": "OpenAI", "google": "Google"}
CONVENE_RATIONALE = (
    "Sondersitzung außer der Reihe: Bestellung der Selbstdarstellungen der drei "
    "Sitzinhaber; zugleich Backend-Durchlauf vor Go-Live. Keine Beratungsfrage, "
    "keine Empfehlung."
)


def parse_order(text):
    """MOTIV/BEGRÜNDUNG verbatim und UNGEKÜRZT ziehen (der Text ist Rekord)."""
    t = (text or "").strip()
    m = re.search(r"MOTIV\s*:?\s*", t, re.I)
    b = re.search(r"BEGR[ÜU]NDUNG\s*:?\s*", t, re.I)
    if m and b and b.start() >= m.end():
        motiv = t[m.end():b.start()].strip().strip("`").strip()
        begr = t[b.end():].strip().strip("`").strip()
        return motiv, begr
    if m:
        return t[m.end():].strip().strip("`").strip(), None
    return None, None


def stub_response(spec):
    return (
        "MOTIV: [DRY] Ein geprägtes Messingrelief, ein Kompass im Halbprofil, "
        f"gestreiftes Licht, gealterte Oberfläche — Trockenlauf {spec['label']}.\n\n"
        "BEGRÜNDUNG: [DRY] Platzhalter-Begründung zur Struktur-/Parser-Prüfung "
        "ohne echten API-Aufruf.",
        {"input_tokens": 0, "output_tokens": 0},
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    date = args.date

    config = json.loads((HERE / "config.json").read_text())
    models = config["models"]
    frame = prompts.COMMISSION_FRAME
    frame_sha = hashlib.sha256(frame.encode("utf-8")).hexdigest()

    out_dir = ROOT / "commissions" / date
    journal_dir = ROOT / "journal" / date
    models_path = ROOT / "models.json"
    for p in (out_dir, journal_dir):
        if p.exists():
            sys.exit(f"Abbruch: {p} existiert bereits — Rekord ist unveränderlich.")
    if models_path.exists():
        sys.exit(
            f"Abbruch: {models_path} existiert bereits — Registratur wird nie "
            "überschrieben; neue Einträge werden angehängt (manuell/eigener Lauf)."
        )

    if not args.dry_run:
        load_env(HERE, ROOT)
        require_keys("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY")

    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True)

    print(f"Bestell-Sondersitzung {COMMISSION_ID} · {date}"
          f"{' · DRY-RUN' if args.dry_run else ''}", file=sys.stderr)
    print(f"Rahmen-SHA256: {frame_sha}", file=sys.stderr)

    orders = []
    for spec in models:
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if args.dry_run:
            text, usage = stub_response(spec)
            (raw_dir / f"order-{spec['family']}.json").write_text(
                json.dumps({"dry_run": True, "text": text}, ensure_ascii=False, indent=2)
            )
        else:
            # GETRENNT: der Rahmen als user-Prompt, kein System-Zusatz, KEINE
            # anderen Voten. call_model dumpt die Rohantwort nach raw_dir.
            text, usage = call_model(spec, "", frame, MAX_TOKENS, raw_dir, "order")
        motiv, begr = parse_order(text)
        m_len = len(motiv) if motiv is not None else None
        b_len = len(begr) if begr is not None else None
        orders.append({
            "model": spec["model"],
            "family": spec["family"],
            "label": spec["label"],
            "motiv": motiv,
            "begruendung": begr,
            "motiv_len": m_len,
            "begruendung_len": b_len,
            "within_limits": bool(
                motiv and begr and m_len <= MOTIV_MAX and b_len <= BEGR_MAX
            ),
            "parse_ok": bool(motiv and begr),
            "attempt": 1,
            "frame_sha256": frame_sha,
            "timestamp": ts,
            "usage": usage,
            "raw": f"raw/order-{spec['family']}.json",
        })
        print(
            f"  {spec['label']:>12}: motiv={m_len if m_len is not None else '—'}z "
            f"begr={b_len if b_len is not None else '—'}z "
            f"parse_ok={bool(motiv and begr)} within_limits={orders[-1]['within_limits']}",
            file=sys.stderr,
        )

    # --- commissions/<date>/commission.json ---------------------------------
    commission = {
        "schema_version": 1,
        "kind": "commission",
        "id": COMMISSION_ID,
        "date": date,
        "convened": CONVENED,
        "ordered": date,
        "dry_run": args.dry_run,
        "frame_sha256": frame_sha,
        "frame": frame,
        "note": (
            "Getrennte Befragung ohne Kenntnis der anderen Bestellungen; keine "
            "Aggregation, kein Umdenken-Schritt, kein Zählstand. Zählt nicht als "
            "Sitzung. Wortlaute gehen vor Freigabe an den Wart."
        ),
        "orders": orders,
    }
    (out_dir / "commission.json").write_text(
        json.dumps(commission, ensure_ascii=False, indent=2)
    )

    # --- models.json (Registratur §3) ---------------------------------------
    registry = {
        "schema_version": 1,
        "note": (
            "Registratur der Modell-Medaillons (Bestellverfahren §3). Alte Einträge "
            "werden nie überschrieben; bei Modellwechsel neuer Eintrag mit höherer "
            "version. warden_review bleibt 'pending', bis der Wart prüft."
        ),
        "models": [
            {
                "model": o["model"],
                "model_label": f"{o['label']} ({FAMILY_DISPLAY[o['family']]})",
                "convened": CONVENED,
                "ordered": date,
                "nachtragsbestellung": True,
                "motiv": o["motiv"],
                "begruendung": o["begruendung"],
                "person": None,
                "warden_review": {"decision": "pending", "date": None, "note": None},
                "attempt": o["attempt"],
                "asset": None,
                "version": 1,
            }
            for o in orders
        ],
    }
    models_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2))

    # --- journal/<date>/entry.json (Runde E §5) -----------------------------
    # KEIN schedule-Eingriff (kein write_schedule/advance_schedule): ein Journal-
    # eintrag berührt schedule.json nicht. model/model_label bleiben absent —
    # kein LLM hat den Eintrag verfasst (mechanischer Rekord), Regel „kein Modell
    # gelaufen → kein Feld".
    tok_in = sum((o["usage"] or {}).get("input_tokens", 0) or 0 for o in orders)
    tok_out = sum((o["usage"] or {}).get("output_tokens", 0) or 0 for o in orders)
    journal_dir.mkdir(parents=True)
    entry = {
        "schema_version": 1,
        "date": date,
        "type": "commission",
        "commission_ref": f"/commissions/{date}/",
        "session_ref": None,
        "convene": True,
        "convene_rationale": CONVENE_RATIONALE,
        "search_queries": [],
        "findings": [],
        "rejected_findings": [],
        "delta_assessment": (
            "Bestell-Sondersitzung (commission-1): Selbstdarstellungs-Bestellung der "
            "drei Sitzmodelle über den regulären API-Mechanismus. Keine Beratungs"
            "frage, keine Aggregation, keine Gremium-Empfehlung; zugleich Backend-"
            "Durchlauf vor Go-Live."
        ),
        "content_md": (
            f"# Bestell-Sondersitzung — {COMMISSION_ID}\n\n"
            "*Sondersitzung außer der Reihe, kein Beratungslauf. Zählt nicht als "
            "Sitzung; die Sitzungsnummerierung bleibt den Beratungen vorbehalten.*\n\n"
            "## Gegenstand\n"
            "Die drei Sitzmodelle bestellen ihr rundes Messingmedaillon selbst — "
            "getrennt befragt, ohne Kenntnis der anderen Bestellungen, mit dem "
            "identischen Rahmentext (§2 des Bestellverfahrens). Nachtragsbestellung, "
            "weil die Modelle längst einberufen sind (Ersteinberufung "
            f"{CONVENED}).\n\n"
            "## Ablauf\n"
            "Ein Lauf über den regulären API-Mechanismus (`gremium/run_commission.py`, "
            "`call_model`). Keine Aggregationsregel angewandt (keine Säulenfrage), "
            "kein Umdenken-Schritt. Rahmentext-Hash, Versuchszahl und Zeitstempel je "
            f"Modell liegen in `/commissions/{date}/commission.json`.\n\n"
            "## Nächster Schritt\n"
            "Der Wart prüft die drei Wortlaute gegen den Rahmen, **bevor** generiert "
            "wird; Ablehnungen bleiben mit Vermerk im Rekord (`models.json`, "
            "`warden_review`)."
        ),
        "costs": {
            "currency": "EUR",
            "total": None,
            "input_tokens": tok_in or None,
            "output_tokens": tok_out or None,
        },
        "actions_run_url": None,
    }
    (journal_dir / "entry.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=2)
    )

    print(
        f"\nGeschrieben:\n  {out_dir}/commission.json (+ raw/)\n  {models_path}\n"
        f"  {journal_dir}/entry.json\n"
        f"schedule.json UNBERÜHRT. Kein Sitzungs-Zählstand, keine Aggregation.",
        file=sys.stderr,
    )
    print(json.dumps({"ok": True, "orders": [
        {"label": o["label"], "parse_ok": o["parse_ok"],
         "motiv_len": o["motiv_len"], "begruendung_len": o["begruendung_len"],
         "within_limits": o["within_limits"]} for o in orders]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
