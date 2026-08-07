#!/usr/bin/env python3
"""Bestell-Sondersitzung (commission-N) — Selbstdarstellung der Sitzmodelle.

Runde E §1 + Bestellverfahren §2. EIN Lauf über den regulären API-Mechanismus
(``call_model`` aus ``run_session``), einmal je Modell, GETRENNT: kein Umdenken-
Schritt, keine Kenntnis der anderen Bestellungen, KEINE Aggregation, KEIN
schedule-Vorlauf. Der Lauf zählt NICHT als Sitzung — er schreibt nach
``commissions/<date>/`` (nicht ``sessions/``), schreibt die Registratur
``models.json`` ADDITIV fort und legt einen Journaleintrag ``journal/<date>/``
(type=commission) an.

Wiederholbar: ``--commission-id`` und ``--convened`` sind Pflicht. Bestellt
werden ausschließlich die in ``config.json`` konfigurierten Ratsmodelle, deren
``model``-ID noch nicht in ``models.json`` registriert ist; bestehende
Registratur-, Commission- und Journal-Einträge bleiben unangetastet. Bei
Modellwechsel bekommen die neuen Sitzinhaber die nächste Medaillon-Epoche
(``version = max(Bestand) + 1``); ``warden_review`` bleibt ``pending``.

Aufruf:  python3 run_commission.py --date 2026-08-07 \\
             --commission-id commission-2 --convened 2026-08-06 [--dry-run]
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

MOTIV_MAX = 400
BEGR_MAX = 600
MAX_TOKENS = 3000
FAMILY_DISPLAY = {"anthropic": "Anthropic", "openai": "OpenAI", "google": "Google"}

# Hinweistext nur für eine frisch angelegte Registratur (kein Bestand). Bei einer
# bereits vorhandenen models.json wird deren Hinweistext unverändert übernommen —
# historische Aussagen werden nie entfernt (Auflage §3.3).
_FRESH_REGISTRY_NOTE = (
    "Registratur der Modell-Medaillons (Bestellverfahren §3). Alte Einträge "
    "werden nie überschrieben; bei Modellwechsel neuer Eintrag mit höherer "
    "version. warden_review bleibt 'pending', bis der Wart prüft."
)

_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _check_iso(name, value):
    if not (value and _ISO.match(value)):
        sys.exit(f"Abbruch: --{name} muss kanonisches ISO-Datum YYYY-MM-DD sein "
                 f"(war: {value!r}).")
    try:
        datetime.date.fromisoformat(value)  # echte Kalenderprüfung (z. B. 2026-02-30)
    except ValueError:
        sys.exit(f"Abbruch: --{name} ist kein gültiges Kalenderdatum: {value!r}.")


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


def select_new_models(config_models, registry_models):
    """Ratsmodelle aus der Config, deren ``model``-ID noch nicht registriert ist.

    Zwei Quellen der Wahrheit: aktuelle Config + additive Registratur. Laute
    Fehler bei doppelter ``model``-ID (Config oder Registratur) oder unbekannter/
    fehlender Familie — nichts erraten, kein zweites Auswahlverfahren.
    """
    def _nonempty(v):
        return isinstance(v, str) and v.strip()

    for i, m in enumerate(config_models):
        for field in ("model", "family", "label"):
            if not _nonempty(m.get(field)):
                sys.exit(
                    f"Abbruch: config.json Modell #{i}: Feld {field!r} fehlt "
                    "oder ist leer — nichts erraten."
                )
        if m["family"] not in FAMILY_DISPLAY:
            sys.exit(
                f"Abbruch: unbekannte Familie für Modell {m['model']!r} "
                f"(config.json #{i}): {m['family']!r}."
            )
    cfg_ids = [m["model"] for m in config_models]
    cfg_dupes = sorted({i for i in cfg_ids if cfg_ids.count(i) > 1})
    if cfg_dupes:
        sys.exit(f"Abbruch: doppelte model-ID in config.json: {cfg_dupes}.")
    for i, m in enumerate(registry_models):
        if not _nonempty(m.get("model")):
            sys.exit(
                f"Abbruch: models.json Eintrag #{i}: leere/fehlende model-ID."
            )
    reg_ids = [m["model"] for m in registry_models]
    reg_dupes = sorted({i for i in reg_ids if reg_ids.count(i) > 1})
    if reg_dupes:
        sys.exit(f"Abbruch: doppelte model-ID in models.json: {reg_dupes}.")
    registered = set(reg_ids)
    return [m for m in config_models if m["model"] not in registered]


def _registry_entry(order, version, convened, ordered, nachtrag):
    """Neuer Pending-Eintrag nach bestehendem Muster; keine Person aus Freitext
    erraten (``person: null`` bis zur Wart-Prüfung), ``asset: null``."""
    return {
        "model": order["model"],
        "model_label": f"{order['label']} ({FAMILY_DISPLAY[order['family']]})",
        "convened": convened,
        "ordered": ordered,
        "nachtragsbestellung": nachtrag,
        "motiv": order["motiv"],
        "begruendung": order["begruendung"],
        "person": None,
        "warden_review": {"decision": "pending", "date": None, "note": None},
        "attempt": order["attempt"],
        "asset": None,
        "version": version,
    }


def append_registry(existing, new_orders, convened, ordered, nachtrag):
    """Registratur additiv fortschreiben.

    Bestehende Einträge bleiben objektgleich und in derselben Reihenfolge; nur die
    neuen Pending-Einträge werden angehängt. ``version`` = ``max(Bestand) + 1`` —
    alle neuen Sitzinhaber teilen die nächste Medaillon-Epoche. Bei leerem/
    fehlendem Bestand: version 1, generischer Hinweistext.
    """
    if existing and existing.get("models"):
        prior = existing["models"]
        version = max((m.get("version", 1) for m in prior), default=0) + 1
        note = existing.get("note", _FRESH_REGISTRY_NOTE)  # historische Aussagen bleiben
        models = list(prior) + [
            _registry_entry(o, version, convened, ordered, nachtrag) for o in new_orders
        ]
    else:
        version = 1
        note = _FRESH_REGISTRY_NOTE
        models = [
            _registry_entry(o, version, convened, ordered, nachtrag) for o in new_orders
        ]
    return {"schema_version": 1, "note": note, "models": models}


def _existing_commission_ids(root):
    """Bereits vergebene commission-``id``s aus allen vorhandenen
    ``commissions/*/commission.json`` (read-only). Für die repositoryweite
    Eindeutigkeit der Kennung — kein zweites Register, keine Indexdatei."""
    found = {}
    cdir = root / "commissions"
    if cdir.exists():
        for p in sorted(cdir.glob("*/commission.json")):
            try:
                cid = json.loads(p.read_text()).get("id")
            except (ValueError, OSError):
                continue
            if isinstance(cid, str) and cid and cid not in found:
                found[cid] = p
    return found


def _run(root, config, args, call_model_fn=call_model):
    date = args.date
    commission_id = args.commission_id
    convened = args.convened

    # --- Validierung VOR jeder Verzeichnisanlage, Schreib- oder API-Aktion (§3.5)
    if not commission_id or not commission_id.strip():
        sys.exit("Abbruch: --commission-id fehlt oder ist leer/whitespace.")
    _check_iso("date", date)
    _check_iso("convened", convened)
    ordered = date
    if convened > ordered:
        sys.exit(
            f"Abbruch: --convened ({convened}) liegt nach dem Bestelldatum "
            f"({ordered}) — implausibel."
        )
    nachtrag = ordered > convened

    models_path = root / "models.json"
    out_dir = root / "commissions" / date
    journal_dir = root / "journal" / date

    registry_existing = (
        json.loads(models_path.read_text()) if models_path.exists() else None
    )
    registry_models = (registry_existing or {}).get("models", [])
    new_specs = select_new_models(config["models"], registry_models)

    print(
        "Bestellmenge (neue, noch nicht registrierte Modelle): "
        + (", ".join(s["model"] for s in new_specs) or "—"),
        file=sys.stderr,
    )
    if not new_specs:
        sys.exit(
            "Abbruch: keine neuen Modelle zu bestellen — alle konfigurierten "
            "Ratsmodelle sind bereits registriert. Kein Verzeichnis angelegt, "
            "kein API-Call."
        )
    for p in (out_dir, journal_dir):
        if p.exists():
            sys.exit(f"Abbruch: {p} existiert bereits — Rekord ist unveränderlich.")
    used = _existing_commission_ids(root)
    if commission_id in used:
        sys.exit(
            f"Abbruch: commission-id {commission_id!r} ist bereits vergeben "
            f"({used[commission_id]}) — Kennungen sind repositoryweit eindeutig."
        )

    frame = prompts.COMMISSION_FRAME
    frame_sha = hashlib.sha256(frame.encode("utf-8")).hexdigest()

    # --- ab hier Schreiben/API: Key-Preflight ZUERST, VOR jeder Verzeichnis-
    # anlage (P1). Fehlt ein Key, entsteht kein commissions/<date>/raw/, das den
    # nächsten Lauf am Unveränderlichkeits-Gate scheitern ließe. ----------------
    if not args.dry_run:
        load_env(HERE, ROOT)
        require_keys("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY")
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True)

    print(
        f"Bestell-Sondersitzung {commission_id} · {date}"
        f"{' · DRY-RUN' if args.dry_run else ''}",
        file=sys.stderr,
    )
    print(f"Rahmen-SHA256: {frame_sha}", file=sys.stderr)

    orders = []
    for spec in new_specs:
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if args.dry_run:
            text, usage = stub_response(spec)
            (raw_dir / f"order-{spec['family']}.json").write_text(
                json.dumps({"dry_run": True, "text": text}, ensure_ascii=False, indent=2)
            )
        else:
            # GETRENNT: der Rahmen als user-Prompt, kein System-Zusatz, KEINE
            # anderen Voten. call_model dumpt die Rohantwort nach raw_dir.
            text, usage = call_model_fn(spec, "", frame, MAX_TOKENS, raw_dir, "order")
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

    labels = ", ".join(o["label"] for o in orders)

    # --- commissions/<date>/commission.json ---------------------------------
    commission = {
        "schema_version": 1,
        "kind": "commission",
        "id": commission_id,
        "date": date,
        "convened": convened,
        "ordered": ordered,
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

    # --- models.json (Registratur §3) — ADDITIV -----------------------------
    registry = append_registry(registry_existing, orders, convened, ordered, nachtrag)
    models_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2))

    # --- journal/<date>/entry.json (Runde E §5) -----------------------------
    # KEIN schedule-Eingriff (kein write_schedule/advance_schedule): ein Journal-
    # eintrag berührt schedule.json nicht. model/model_label bleiben absent —
    # kein LLM hat den Eintrag verfasst (mechanischer Rekord), Regel „kein Modell
    # gelaufen → kein Feld".
    tok_in = sum((o["usage"] or {}).get("input_tokens", 0) or 0 for o in orders)
    tok_out = sum((o["usage"] or {}).get("output_tokens", 0) or 0 for o in orders)
    kind_phrase = (
        "Nachbestellung nach Besetzungswechsel" if nachtrag else "Erstbestellung"
    )
    journal_dir.mkdir(parents=True)
    entry = {
        "schema_version": 1,
        "date": date,
        "type": "commission",
        "commission_ref": f"/commissions/{date}/",
        "session_ref": None,
        "convene": True,
        "convene_rationale": (
            f"Sondersitzung außer der Reihe: Selbstdarstellungs-Bestellung "
            f"({kind_phrase}) der neu besetzten Sitzinhaber. Keine Beratungsfrage, "
            "keine Empfehlung."
            if nachtrag else
            "Sondersitzung außer der Reihe: Selbstdarstellungs-Bestellung der "
            "Sitzinhaber. Keine Beratungsfrage, keine Empfehlung."
        ),
        "search_queries": [],
        "findings": [],
        "rejected_findings": [],
        "delta_assessment": (
            f"Bestell-Sondersitzung ({commission_id}): {kind_phrase} der "
            f"Selbstdarstellungen von {len(orders)} Sitzmodellen ({labels}) über "
            "den regulären API-Mechanismus. Keine Beratungsfrage, keine "
            "Aggregation, keine Gremium-Empfehlung."
        ),
        "content_md": (
            f"# Bestell-Sondersitzung — {commission_id}\n\n"
            "*Sondersitzung außer der Reihe, kein Beratungslauf. Zählt nicht als "
            "Sitzung; die Sitzungsnummerierung bleibt den Beratungen vorbehalten.*\n\n"
            "## Gegenstand\n"
            "Die Sitzmodelle bestellen ihr rundes Messingmedaillon selbst — "
            "getrennt befragt, ohne Kenntnis der anderen Bestellungen, mit dem "
            "identischen Rahmentext (§2 des Bestellverfahrens). "
            + (
                f"{kind_phrase}: neue Sitzbesetzung, erstmals einberufen am "
                f"{convened}. Bestellt werden ausschließlich die Modelle, deren "
                "Modell-ID noch nicht in der Medaillon-Registratur steht.\n\n"
                if nachtrag else
                f"Ersteinberufung {convened}.\n\n"
            )
            + "## Bestellte Modelle\n"
            + "".join(f"- `{o['model']}` ({o['label']})\n" for o in orders)
            + "\n## Ablauf\n"
            "Ein Lauf über den regulären API-Mechanismus (`gremium/run_commission.py`, "
            "`call_model`). Keine Aggregationsregel angewandt (keine Säulenfrage), "
            "kein Umdenken-Schritt. Rahmentext-Hash, Versuchszahl und Zeitstempel je "
            f"Modell liegen in `/commissions/{date}/commission.json`.\n\n"
            "## Nächster Schritt\n"
            "Der Wart prüft die Wortlaute gegen den Rahmen, **bevor** generiert "
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
    print(json.dumps({"ok": True, "commission_id": commission_id, "orders": [
        {"label": o["label"], "parse_ok": o["parse_ok"],
         "motiv_len": o["motiv_len"], "begruendung_len": o["begruendung_len"],
         "within_limits": o["within_limits"]} for o in orders]}, ensure_ascii=False))
    return {"commission": commission, "registry": registry, "entry": entry}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--commission-id", required=True,
                    help="z. B. commission-2 (Pflicht, keine Vorbelegung)")
    ap.add_argument("--convened", required=True,
                    help="Datum der Ersteinberufung dieser Modellbesetzung, "
                         "ISO YYYY-MM-DD (Pflicht)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    config = json.loads((HERE / "config.json").read_text())
    _run(ROOT, config, args)


if __name__ == "__main__":
    main()
