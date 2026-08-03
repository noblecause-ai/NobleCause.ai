#!/usr/bin/env python3
"""Orchestrator einer Gremium-Sitzung.

Deterministischer Ablauf (kein LLM steuert den Prozess):
  0. Runde 0 (optional) — Wart liefert Evidenz-Dossier per Web-Suche.
  1. Runde 1 — jedes Modell votiert unabhängig (Manifest + Frage + Quellen + Dossier).
  2. Runde 2 — jedes Modell liest die Erstvoten der anderen, gibt Schlussvotum ab.
  3. Kurzfassung + Protokoll nach sessions/<id>/.

Aufruf:  python3 run_session.py --question "…" --title "…" [--with-dossier]
Keys:    ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY (oder gremium/.env)
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

import prompts  # noqa: E402
import organizations  # noqa: E402
from envtools import load_env, require_keys  # noqa: E402


# ---------------------------------------------------------------- utilities

def _votum_block_span(text):
    """(start, end) des abschließenden Votum-Codeblocks — die eine Stelle, die sowohl der
    Votum-Parser (extract_json_block) liest als auch aus dissent_md abgestreift wird
    (strip_votum_block). Fundort: rfind der letzten ```json-Fence bis zur schließenden
    ```-Fence; (-1, -1), wenn keiner da ist. Eine Quelle, damit Parser und Abstreifen
    dieselbe Grenze sehen und nicht auseinanderdriften (P4)."""
    start = text.rfind("```json")
    if start == -1:
        return -1, -1
    end_fence = text.find("```", start + 7)
    end = len(text) if end_fence == -1 else end_fence + 3
    return start, end


def extract_json_block(text):
    start, end = _votum_block_span(text)
    if start != -1:
        body = text[start + 7 : end]
        if body.endswith("```"):
            body = body[:-3]
        body = body.strip()
        if not body.startswith("{"):
            brace = body.find("{")
            if brace != -1:
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
                        pass
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not matches:
        return None
    try:
        return json.loads(matches[-1])
    except json.JSONDecodeError:
        return None


def strip_votum_block(text):
    """Entfernt genau den abschließenden Votum-JSON-Block — den, den extract_json_block
    parst (gemeinsamer Fundort _votum_block_span). Prosa davor UND dahinter bleibt
    unverändert; ein json-Block MITTEN im Dissens (nicht der abschließende) bleibt stehen,
    weil der Fundort rfind ist. So kann in dissent_md nichts anderes stehen als der Parser
    gesehen hat (P4)."""
    start, end = _votum_block_span(text)
    if start == -1:
        return text
    return text[:start] + text[end:]


def strip_json_block(text):
    return re.sub(r"```json\s*\{.*?\}\s*```\s*$", "", text, flags=re.DOTALL).strip()


def extract_dissent(text):
    m = re.search(r"##\s*Dissens\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL)
    return m.group(1).strip() if m else None


def extract_search_queries(text):
    section = re.search(r"##\s*Suchanfragen\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not section:
        return []
    queries = []
    for line in section.group(1).splitlines():
        line = line.strip().lstrip("-·*").strip()
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        if line:
            queries.append(line)
    return queries


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


def prior_session():
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
        return None, None
    entries.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return entries[0][2], entries[0][3]


def resolve_session_id(sessions_dir, base):
    """Ersten freien Kandidaten base, base+'b', base+'c', … zurückgeben.

    Konsistent mit dem bestehenden Schema (2026-07, 2026-07b, 2026-07c). Wird nur
    genutzt, wenn keine --session-id explizit übergeben wurde.
    """
    if not (sessions_dir / base).exists():
        return base
    for suffix in "bcdefghijklmnopqrstuvwxyz":
        candidate = base + suffix
        if not (sessions_dir / candidate).exists():
            return candidate
    sys.exit(f"Abbruch: keine freie session-id für Basis {base} gefunden.")


def advance_schedule(session_date):
    """schedule.json.next_session auf session_date + 30 Tage fortschreiben.

    Nur run_session.py-relevantes Feld ändern; next_research/last_journal bleiben
    unangetastet (die pflegt run_wart.py). Format wie run_wart.next_regular_session:
    ISO-Datum + 'T12:00:00Z'.
    """
    schedule_path = ROOT / "schedule.json"
    schedule = json.loads(schedule_path.read_text()) if schedule_path.exists() else {}
    base = datetime.date.fromisoformat(session_date)
    schedule["next_session"] = (base + datetime.timedelta(days=30)).isoformat() + "T12:00:00Z"
    schedule_path.write_text(json.dumps(schedule, indent=2, ensure_ascii=False) + "\n")
    print(f"schedule.json aktualisiert (nächste Sitzung: {schedule['next_session']})")


# ---------------------------------------------------------------- API calls

def call_anthropic(model, system, user, max_tokens):
    import anthropic

    client = anthropic.Anthropic()
    # Streaming: bei hohem max_output_tokens (die reasoning-lastige Besetzung ab Sitzung 4
    # braucht es, sonst schneidet die Antwort vor dem JSON-Block ab) verweigert das SDK
    # den nicht-gestreamten Call (>10 min veranschlagt). Der Wart-Caller streamt aus
    # demselben Grund. Ergebnis identisch — nur der Transportweg ist gestreamt.
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        resp = stream.get_final_message()
    text = "".join(b.text for b in resp.content if b.type == "text")
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    return text, usage, resp.model_dump()


def call_wart_dossier(wart_cfg, system, user, raw_dir):
    import anthropic

    client = anthropic.Anthropic()
    max_uses = wart_cfg.get("max_web_search_uses", 15)
    print(f"  Modell: {wart_cfg['model']}")
    print(f"  Web-Suche: max. {max_uses} Anfragen")

    # Streaming Pflicht bei hohem max_output_tokens (langes Dossier + Web-Suche);
    # das SDK verweigert sonst den nicht-gestreamten Call (>10 min veranschlagt).
    with client.messages.stream(
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
    ) as stream:
        resp = stream.get_final_message()
    raw = resp.model_dump()
    (raw_dir / "r0-wart.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    server = (raw.get("usage") or {}).get("server_tool_use") or {}
    usage = {
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "web_search_requests": server.get("web_search_requests", 0),
    }
    api_queries = []
    for block in raw.get("content") or []:
        if block.get("type") == "server_tool_use" and block.get("name") == "web_search":
            q = (block.get("input") or {}).get("query")
            if q:
                api_queries.append(q)
    if api_queries:
        print("  Suchanfragen (API):")
        for q in api_queries:
            print(f"    · {q}")
    print(
        f"  Tokens: {usage['input_tokens']} in / {usage['output_tokens']} out · "
        f"Suchen: {usage['web_search_requests']}"
    )
    return text, usage, raw, api_queries


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
    caller = CALLERS[spec["family"]]
    last_err = None
    for attempt in (1, 2):
        try:
            text, usage, raw = caller(spec["model"], system, user, max_tokens)
            (raw_dir / f"{tag}-{spec['family']}.json").write_text(
                json.dumps(raw, indent=2, ensure_ascii=False, default=str)
            )
            return text, usage
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"    Versuch {attempt} bei {spec['model']} fehlgeschlagen: {e}", file=sys.stderr)
    raise RuntimeError(f"{spec['model']} nach 2 Versuchen nicht erreichbar") from last_err


# ---------------------------------------------------------------- aggregation

def _vote_recommendations(parsed):
    """Empfehlungsliste aus einem geparsten Votum — key-tolerant.

    Ein Modell kann von der Prompt-Vorgabe abweichen (Opus 2026-07c nutzte die
    deutschen Keys 'empfehlungen'/'gesamtkonfidenz'). Solche Voten werden gelesen,
    NICHT verschluckt. Rein deterministische Key-Alternativen, kein Fuzzy.
    """
    if not parsed:
        return []
    return parsed.get("recommendations") or parsed.get("empfehlungen") or []


def structured_vote_recs(parsed):
    """Registry-aufgelöste Voten je Säule für die Persistenz in session.json.

    Erlaubt dem Frontend, Protokollspalten + Revision (wer nannte r1 vs r2 welche
    Org) zu rendern, OHNE Prosa zu parsen. Unbekannte Org → weggelassen (der
    Aggregator meldet sie separat als unresolved); nie stiller Textfall.
    """
    out = []
    for r in _vote_recommendations(parsed):
        pillar = r.get("pillar")
        org_id = organizations.resolve(r.get("organization"))
        if pillar not in ("A", "B", "C", "D") or org_id is None:
            continue
        # Rohvotum je Modell (Anzeige): conditional strukturell; None, wenn das Modell
        # kein gültiges Bool lieferte (der Aggregator schließt es separat als ungültig aus).
        _valid, cond, reservation = read_conditional(r)
        out.append({
            "pillar": pillar,
            "organization_id": org_id,
            "organization": organizations.get(org_id)["canonical_name"],
            "title": r.get("title"),
            "confidence": r.get("confidence"),
            "conditional": cond,
            "reservation": reservation,
        })
    return out


# §5: `conditional` ist Pflichtfeld im Votum-Vertrag und wird AUSSCHLIESSLICH aus dem
# strukturierten Feld gelesen — nie aus dem Titel geraten. Die Regex entfällt ersatzlos:
# die versiegelte Datennaht verbietet der rekord-erzeugenden Maschine, Prosa zu parsen.
def read_conditional(rec):
    """Gibt (valid, conditional, reservation).

    valid=False, wenn `conditional` fehlt oder kein echtes JSON-Boolean ist — dann ist die
    Empfehlung vertragswidrig. Kein Titel-Raten als Fallback (Vertragsbruch-Entscheid):
    der Aufrufer behandelt sie als ungültig. `reservation` nur bei conditional=True.
    """
    cond = rec.get("conditional")
    if not isinstance(cond, bool):
        return False, None, None
    reservation = rec.get("reservation") if cond else None
    return True, cond, reservation


def aggregate_recommendations(final_votes, total_models=None):
    """Deterministische Aggregation gegen die Organisations-Registry.

    Konsens = >=2 VERSCHIEDENE Modelle lösen auf dieselbe org_id auf. Auflösung
    ausschließlich via organizations.resolve() (Alias-Match, kein Modell, kein
    Fuzzy). donation_url + canonical_name kommen aus der Registry, nie aus dem
    Votum (Halluzinationsschutz).

    Gibt (recommendations, unresolved) zurück. `unresolved` sammelt Voten mit
    unbekannter Organisation — sie werden NIE stillschweigend als Dissens
    verbucht, sondern explizit ausgewiesen.
    """
    total = total_models or len(final_votes)
    recs = []
    unresolved = []
    for pillar in ("A", "B", "C", "D"):
        candidates = []
        contract_warnings = []
        for vote in final_votes:
            for r in _vote_recommendations(vote["parsed"]):
                if r.get("pillar") != pillar:
                    continue
                org_id = organizations.resolve(r.get("organization"))
                if org_id is None:
                    unresolved.append(
                        {
                            "pillar": pillar,
                            "organization": r.get("organization"),
                            "model": vote["label"],
                        }
                    )
                    continue
                # §5 Vertragsdurchsetzung: conditional muss ein echtes JSON-Boolean sein.
                # Fehlt es / falscher Typ → Empfehlung ungültig (kein Kandidat, zählt
                # votes_invalid), Warnung in den Rekord, KEIN Titel-Raten.
                valid, cond, reservation = read_conditional(r)
                if not valid:
                    contract_warnings.append(
                        f"{vote['label']}: Säule {pillar} — Votum ohne gültiges "
                        f"conditional-Feld (Wert {r.get('conditional')!r}); als ungültig "
                        f"behandelt, kein Titel-Raten."
                    )
                    continue
                candidates.append({
                    **r, "_model": vote["label"], "_org_id": org_id,
                    "_conditional": cond, "_reservation": reservation,
                })
        # Zähler statt Sonderflag (Steward-Entscheid): votes_valid = verschiedene
        # Modelle mit auswertbarem, aufgelöstem Votum in dieser Säule; votes_invalid =
        # der Rest der teilnehmenden Modelle (unlesbar/ohne verwertbares Säulen-Votum).
        # Damit sind alle vier Fälle unterscheidbar — Konsens · Dissens aus
        # vollständigen Voten · unvollständig · gar nichts (votes_valid=0) — und die
        # Tafel entscheidet selbst, ab wann sie welchen Zustand zeigt.
        valid_models = sorted({c["_model"] for c in candidates})
        votes_valid = len(valid_models)
        votes_invalid = max(0, total - votes_valid)
        # Doppelvotum-Warnung (Kimi P3): ein Modell mit mehreren Empfehlungen in
        # derselben Säule ist vom Vertrag untersagt — als Warnung in den Rekord.
        per_model = {}
        for c in candidates:
            per_model[c["_model"]] = per_model.get(c["_model"], 0) + 1
        warnings = contract_warnings + [
            f"{m} hat in Säule {pillar} {n} Empfehlungen abgegeben (Vertrag: genau eine)."
            for m, n in sorted(per_model.items()) if n > 1
        ]

        # Dritter Zustand: kein gültiges Votum. Der Bereich bleibt sichtbar, markiert —
        # nie fehlt der Bereich, nie stille Leere. Wortlaut vom Steward.
        if not candidates:
            rec = {
                "pillar": pillar,
                "has_consensus": False,
                "votes_valid": 0,
                "votes_invalid": votes_invalid,
                "title": None,
                "organization": None,
                "donation_url": None,
                "confidence": None,
                "rationale_md": "Die Antworten zu diesem Bereich waren nicht auswertbar. "
                "Die Rohdaten liegen im Protokoll.",
            }
            if warnings:
                rec["warnings"] = warnings
            recs.append(rec)
            continue

        groups = {}
        for c in candidates:
            groups.setdefault(c["_org_id"], []).append(c)
        # Trägerzahl je Gruppe = VERSCHIEDENE Modelle. Gleichstand explizit erkennen,
        # nicht still die zuerst eingefügte Gruppe wählen (Kimi P3).
        support = {k: len({c["_model"] for c in v}) for k, v in groups.items()}
        max_support = max(support.values())
        leaders = [k for k, n in support.items() if n == max_support]
        tie = max_support >= 2 and len(leaders) > 1

        if max_support >= 2 and not tie:
            best_id = leaders[0]
            best = groups[best_id]
            best_models = sorted({c["_model"] for c in best})
            org = organizations.get(best_id)
            confs = [c.get("confidence") for c in best if c.get("confidence") is not None]
            # Konditionalität je Modell (ein Modell kann mehrfach votieren).
            by_model = {}
            for c in best:
                d = by_model.setdefault(c["_model"], {"model": c["_model"], "conditional": False, "reservation": None})
                if c.get("_conditional"):
                    d["conditional"] = True
                    d["reservation"] = c.get("_reservation")
            vote_details = [by_model[m] for m in best_models]
            conditional_count = sum(1 for v in vote_details if v["conditional"])
            cond_clause = f", davon {conditional_count} konditional," if conditional_count else ""
            # Bei unvollständigen Voten NICHT den Zählstand „X von Y" umdeuten — die
            # Y-Frage (zählt ein unlesbares Modell mit?) gehört dem Wart. Nur ein
            # nachprüfbarer Faktenzusatz, der auf die Rohdaten verweist.
            invalid_clause = (
                f" {votes_invalid} Modell(e) ohne auswertbares Votum (Rohdaten im Protokoll)."
                if votes_invalid else ""
            )
            rec = {
                "pillar": pillar,
                "has_consensus": True,
                "votes_valid": votes_valid,
                "votes_invalid": votes_invalid,
                "title": best[0].get("title"),
                "organization": org["canonical_name"],
                "organization_id": best_id,
                "donation_url": org.get("donation_url"),
                "confidence": round(sum(confs) / len(confs), 2) if confs else None,
                "convergence": {
                    "count": len(best_models),
                    "total": total,
                    "conditional_count": conditional_count,
                    "models": best_models,
                    "votes": vote_details,
                },
                "rationale_md": f"Konvergenz im Schlussvotum: {len(best_models)} von "
                f"{total} Modellen{cond_clause} empfehlen diese Organisation "
                f"({', '.join(best_models)}).{invalid_clause} Begründungen in den Schlussvoten.",
            }
            if warnings:
                rec["warnings"] = warnings
            recs.append(rec)
        else:
            # Kein Konsens: Dissens aus gültigen Voten ODER Gleichstand (tie).
            note = (
                "Gleichstand: mehrere Organisationen mit gleicher Modellzahl — kein Konsens."
                if tie
                else "Die Schlussvoten konvergieren für diese Säule nicht auf eine Organisation."
            )
            rec = {
                "pillar": pillar,
                "has_consensus": False,
                "votes_valid": votes_valid,
                "votes_invalid": votes_invalid,
                "tie": tie,
                "title": "Kein Konsens — Einzelvoten",
                "organization": None,
                "donation_url": None,
                "confidence": None,
                "individual_votes": [
                    {
                        "title": c.get("title"),
                        "organization": organizations.get(c["_org_id"])["canonical_name"],
                        "organization_id": c["_org_id"],
                        "donation_url": organizations.get(c["_org_id"]).get("donation_url"),
                        "confidence": c.get("confidence"),
                        "model": c["_model"],
                        "conditional": c["_conditional"],
                        "reservation": c["_reservation"],
                    }
                    for c in candidates
                ],
                "rationale_md": note,
            }
            if warnings:
                rec["warnings"] = warnings
            recs.append(rec)
    return recs, unresolved


def build_dissent(final_votes):
    parts = []
    for vote in final_votes:
        # P4: den abschließenden Votum-Block am Fundort des Parsers entfernen, DANN den
        # Dissens-Abschnitt lesen — so landet der Maschinenblock (mit modellbehaupteter
        # donation_url) nicht in dissent_md, während der Dissens-Wortlaut vollständig bleibt.
        section = extract_dissent(strip_votum_block(vote["text"]))
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


def generate_summary(
    question, final_votes, recommendations, dissent_md, summarizer, raw_dir, summary_prompt=None
):
    final_excerpt = "\n\n".join(
        f"### {v['label']}\n{strip_json_block(v['text'])[:4000]}" for v in final_votes
    )
    template = summary_prompt or prompts.SUMMARY
    user = template.format(
        question=question,
        final_votes=final_excerpt,
        aggregation=format_aggregation_for_summary(recommendations),
        dissent_md=dissent_md[:6000],
    )
    max_tokens = summarizer.get("max_output_tokens", 1024)
    system = (
        prompts.WART_LEAD_SYSTEM
        if summary_prompt
        else "Du bist ein nüchterner Protokollredakteur. Antworte nur mit JSON."
    )
    text, usage, raw = call_anthropic(
        summarizer["model"],
        system,
        user,
        max_tokens,
    )
    tag = "summary-wart" if summary_prompt else "summary-anthropic"
    (raw_dir / f"{tag}.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )
    parsed = extract_json_block(text)
    if not parsed or "summary" not in parsed:
        raise RuntimeError("Summarizer lieferte kein gültiges JSON mit summary")
    return parsed.get("summary", ""), parsed.get("dissent_highlights", []), usage


def pillar_a_context(prior):
    for rec in prior.get("recommendations", []):
        if rec.get("pillar") == "A":
            if rec.get("has_consensus"):
                return (
                    f"Konsens: {rec.get('title')} — {rec.get('organization')} "
                    f"(Konfidenz {rec.get('confidence')})"
                )
            lines = ["Kein Konsens — Einzelvoten:"]
            for v in rec.get("individual_votes") or []:
                lines.append(
                    f"  · {v.get('model')}: {v.get('organization')} — {v.get('title')} "
                    f"(Konfidenz {v.get('confidence')})"
                )
            return "\n".join(lines)
    return "Keine Säule-A-Empfehlungen in der Vorgänger-Sitzung."


def call_wart_simple(wart_cfg, system, user, raw_dir, tag, max_tokens=None):
    import anthropic

    raw_dir.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()
    tokens = max_tokens or wart_cfg.get("max_output_tokens", 4096)
    resp = client.messages.create(
        model=wart_cfg["model"],
        max_tokens=tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    raw = resp.model_dump()
    (raw_dir / f"{tag}.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    return text, usage, raw


def wart_step_result(text, raw, artifact):
    """Ergebnis eines Fable-Zulieferer-Calls, gegen den stop_reason geprüft (B-Härtung, wie
    run_wart.py). Nur end_turn ist eine vollständige, übernehmbare Antwort; jeder andere
    stop_reason (refusal, max_tokens, pause_turn, …) heißt: Teiltext NICHT übernehmen — bei
    einer Verweigerung stand sonst der 81-Byte-Anlauf ("Ich beginne mit der Recherche …") als
    echtes Dossier im Rekord. KEIN Abbruch: die Sitzung läuft weiter (das Dossier ist
    Zulieferer, nicht Sitzung; die drei Ratsvoten hängen weder an Fable noch an der Websuche).

    Rückgabe: (text, None) bei end_turn, sonst (None, marker). Der Marker macht die ABWESENHEIT
    begründet — sonst wäre "das Modell hat verweigert" nicht von "es wurde keins angefordert"
    unterscheidbar (kein stilles None). Feld raw_artifact zeigt auf die gesicherte Rohantwort."""
    stop = (raw or {}).get("stop_reason")
    if stop == "end_turn":
        return text, None
    marker = {
        "stop_reason": stop,
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "raw_artifact": f"raw/{artifact}",
    }
    return None, marker


def check_fable_available(wart_cfg, raw_dir=None):
    print("Fable-Verfügbarkeits-Check …")
    check_dir = raw_dir or Path("/tmp")
    try:
        text, usage, _ = call_wart_simple(
            wart_cfg,
            "Antworte mit genau einem Wort: bereit.",
            "Ping.",
            check_dir,
            "fable-check",
            max_tokens=16,
        )
        print(f"  OK — Antwort: {text.strip()[:40]}")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"  FEHLGESCHLAGEN: {e}", file=sys.stderr)
        return False


def empty_wart_usage():
    return {"input_tokens": 0, "output_tokens": 0, "web_search_requests": 0}


def accumulate_wart_usage(total, usage):
    total["input_tokens"] += usage.get("input_tokens", 0)
    total["output_tokens"] += usage.get("output_tokens", 0)
    total["web_search_requests"] += usage.get("web_search_requests", 0)


def compute_wart_cost(usage, wart_cfg, fx):
    token_usd = (
        usage["input_tokens"] / 1e6 * wart_cfg["usd_per_1m_input"]
        + usage["output_tokens"] / 1e6 * wart_cfg["usd_per_1m_output"]
    )
    search_usd = (
        usage.get("web_search_requests", 0) / 1000 * wart_cfg.get("usd_per_1k_web_searches", 10.0)
    )
    total_usd = token_usd + search_usd
    return {
        "model": wart_cfg["model"],
        "label": wart_cfg.get("label", wart_cfg["model"]),
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "web_search_requests": usage.get("web_search_requests", 0),
        "usd": round(total_usd, 4),
        "eur": round(total_usd * fx, 4),
    }


def compute_costs(usage_by_model, model_specs, fx, wart_cost=None):
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
    if wart_cost:
        by_model.append(wart_cost)
    total_eur = round(sum(c["eur"] for c in by_model), 2)
    return {"currency": "EUR", "total": total_eur, "fx_rate_usd_eur": fx, "by_model": by_model}


def check_budget(costs, cap_eur, label):
    total = costs["total"]
    print(f"  Zwischenkosten ({label}): {total:.2f} €")
    if total > cap_eur:
        print(f"  WARNUNG: Budgetdeckel {cap_eur} € überschritten ({total:.2f} €)", file=sys.stderr)


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument(
        "--session-id",
        default=None,
        help="Ohne Angabe: YYYY-MM des heutigen Tages, bei Kollision Suffix b/c/…",
    )
    parser.add_argument("--number", type=int, default=None)
    parser.add_argument("--with-dossier", action="store_true")
    parser.add_argument(
        "--led-by-wart",
        action="store_true",
        help="Gründungssitzung: Wart eröffnet, moderiert, schreibt Kurzfassung (impliziert --with-dossier)",
    )
    parser.add_argument("--budget-cap", type=float, default=15.0)
    args = parser.parse_args()

    if args.led_by_wart:
        args.with_dossier = True

    load_env(HERE, ROOT)
    require_keys("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY")
    config = json.loads((HERE / "config.json").read_text())
    manifest = (ROOT / "manifest.md").read_text()
    sources = (HERE / "sources.md").read_text()

    sessions_dir = ROOT / "sessions"
    if args.session_id is None:
        args.session_id = resolve_session_id(sessions_dir, datetime.date.today().strftime("%Y-%m"))
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
    system = prompts.SYSTEM_WITH_CONFLICT
    wart_dossier = None
    wart_dossier_prompt = None
    dossier_section = ""
    opening_section = ""
    wart_opening_md = None
    wart_moderation_md = None
    wart_opening_prompt = None
    wart_moderation_prompt = None
    moderation_section = ""
    wart_opening_refusal = None
    wart_dossier_refusal = None
    wart_moderation_refusal = None
    wart_cfg = config.get("wart")

    usage_by_model = {m["model"]: {"input_tokens": 0, "output_tokens": 0} for m in config["models"]}
    wart_usage = empty_wart_usage()
    wart_cost_entry = None

    def refresh_wart_cost():
        nonlocal wart_cost_entry
        if wart_usage["input_tokens"] or wart_usage["output_tokens"] or wart_usage["web_search_requests"]:
            wart_cost_entry = compute_wart_cost(wart_usage, wart_cfg, fx)

    def interim_costs(summarizer=None):
        refresh_wart_cost()
        specs = config["models"] + ([summarizer] if summarizer else [config["summarizer"]])
        return compute_costs(usage_by_model, specs, fx, wart_cost_entry)

    def record_usage(spec, usage):
        u = usage_by_model[spec["model"]]
        u["input_tokens"] += usage["input_tokens"]
        u["output_tokens"] += usage["output_tokens"]

    prior_id, prior = prior_session()

    # -------- Eröffnung (Wart-Leitung)
    if args.led_by_wart:
        if not prior:
            sys.exit("Abbruch: keine Vorgänger-Sitzung für Gründungssitzung gefunden.")
        pa_ctx = pillar_a_context(prior)
        wart_opening_prompt = prompts.WART_OPENING_USER.format(
            question=args.question,
            pillar_a_context=pa_ctx,
        )
        (raw_dir / "prompt-r0-opening.txt").write_text(wart_opening_prompt)
        print("Eröffnung — Wart (Fable)")
        text, usage, raw = call_wart_simple(
            wart_cfg,
            prompts.WART_LEAD_SYSTEM,
            wart_opening_prompt,
            raw_dir,
            "r0-opening",
            max_tokens=2048,
        )
        accumulate_wart_usage(wart_usage, usage)
        opening_text, wart_opening_refusal = wart_step_result(text, raw, "r0-opening.json")
        if opening_text is not None:
            wart_opening_md = opening_text.strip()
            (raw_dir / "r0-opening-content.md").write_text(wart_opening_md)
            opening_section = (
                "## Eröffnung durch den Wart\n\n"
                f"{wart_opening_md}\n\n---"
            )
        else:
            print(
                f"  Verweigerung (stop_reason={wart_opening_refusal['stop_reason']}) — kein "
                "Eröffnungswort übernommen; Sitzung läuft weiter."
            )
        check_budget(interim_costs(), args.budget_cap, "nach Eröffnung")

    # -------- Runde 0 (Wart-Dossier)
    if args.with_dossier:
        if not prior:
            sys.exit("Abbruch: keine Vorgänger-Sitzung für Dossier gefunden.")
        if args.led_by_wart:
            wart_dossier_prompt = prompts.WART_FOUNDING_DOSSIER_USER.format(
                question=args.question,
                prior_session_id=prior_id,
                prior_session_date=prior.get("date"),
                pillar_a_context=pillar_a_context(prior),
            )
        else:
            wart_dossier_prompt = prompts.WART_DOSSIER_USER.format(
                question=args.question,
                prior_session_id=prior_id,
                prior_session_date=prior.get("date"),
                prior_recommendations=summarize_recommendations(prior),
            )
        (raw_dir / "prompt-r0-wart.txt").write_text(wart_dossier_prompt)
        print("Runde 0 — Wart-Dossier (Fable + Web-Suche)")
        text, usage, raw, api_queries = call_wart_dossier(
            wart_cfg, prompts.WART_DOSSIER_SYSTEM, wart_dossier_prompt, raw_dir
        )
        (raw_dir / "r0-wart-content.md").write_text(text)
        accumulate_wart_usage(wart_usage, usage)
        refresh_wart_cost()
        dossier_text, wart_dossier_refusal = wart_step_result(text, raw, "r0-wart.json")
        if dossier_text is not None:
            search_queries = extract_search_queries(dossier_text) or api_queries
            content_md = strip_json_block(dossier_text)
            wart_dossier = {
                "model": wart_cfg["model"],
                "label": wart_cfg.get("label", wart_cfg["model"]),
                "content_md": content_md,
                "search_queries": search_queries,
                "costs": wart_cost_entry,
            }
            dossier_section = (
                "## Wart-Dossier (Runde 0)\n\n"
                "Der Wart (Fable, claude-fable-5) hat vor den Einzelvoten folgendes "
                "Evidenz-Dossier geliefert. Es enthält keine Empfehlung — nur Fakten "
                "und Quellen.\n\n---\n\n"
                f"{content_md}\n\n---"
            )
        else:
            # dossier_section bleibt "" — kein fiktives Dossier im Ratsprompt (Punkt 4).
            print(
                f"  Verweigerung (stop_reason={wart_dossier_refusal['stop_reason']}) — kein "
                "Dossier übernommen; die drei Ratsvoten laufen ohne Dossier weiter."
            )
        check_budget(interim_costs(), args.budget_cap, "nach Runde 0")

    round1_prompt = prompts.ROUND1.format(
        manifest=manifest,
        sources=sources,
        number=number,
        date=today,
        question=args.question,
        opening_section=opening_section,
        dossier_section=dossier_section,
    )

    # -------- Runde 1
    print("Runde 1 — unabhängige Einzelvoten")
    r1 = []
    for spec in config["models"]:
        print(f"  {spec['label']} ({spec['model']}) …")
        text, usage = call_model(spec, system, round1_prompt, max_tokens, raw_dir, "r1")
        record_usage(spec, usage)
        r1.append({**spec, "text": text, "parsed": extract_json_block(text)})
    check_budget(interim_costs(), args.budget_cap, "nach Runde 1")

    # -------- Moderation (Wart-Leitung)
    if args.led_by_wart:
        initial_votes_text = "\n\n".join(
            f"### Erstvotum {v['label']}\n\n{strip_json_block(v['text'])}"
            for v in r1
        )
        wart_moderation_prompt = prompts.WART_MODERATION_USER.format(
            question=args.question,
            initial_votes=initial_votes_text,
        )
        (raw_dir / "prompt-moderation-wart.txt").write_text(wart_moderation_prompt)
        print("Moderation — Wart (Fable)")
        text, usage, raw = call_wart_simple(
            wart_cfg,
            prompts.WART_LEAD_SYSTEM,
            wart_moderation_prompt,
            raw_dir,
            "moderation-wart",
            max_tokens=4096,
        )
        accumulate_wart_usage(wart_usage, usage)
        moderation_text, wart_moderation_refusal = wart_step_result(text, raw, "moderation-wart.json")
        if moderation_text is not None:
            wart_moderation_md = moderation_text.strip()
            (raw_dir / "moderation-wart-content.md").write_text(wart_moderation_md)
            moderation_section = (
                "## Moderationsnotiz des Warts\n\n"
                f"{wart_moderation_md}\n\n---"
            )
        else:
            # moderation_section bleibt "" — keine fiktive Moderationsnotiz in Runde 2.
            print(
                f"  Verweigerung (stop_reason={wart_moderation_refusal['stop_reason']}) — keine "
                "Moderationsnotiz übernommen; Runde 2 läuft ohne sie."
            )
        check_budget(interim_costs(), args.budget_cap, "nach Moderation")

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
            moderation_section=moderation_section,
        )
        print(f"  {spec['label']} ({spec['model']}) …")
        text, usage = call_model(spec, system, round2_prompt, max_tokens, raw_dir, "r2")
        record_usage(spec, usage)
        r2.append({**spec, "text": text, "parsed": extract_json_block(text)})
    check_budget(interim_costs(), args.budget_cap, "nach Runde 2")

    # -------- Kurzfassung
    print("Kurzfassung — Protokollredaktion")
    dissent_md = build_dissent(r2)
    recommendations, unresolved = aggregate_recommendations(r2)
    if unresolved:
        print(f"  WARNUNG: {len(unresolved)} Votum/Voten mit nicht zuordenbarer Organisation:", file=sys.stderr)
        for u in unresolved:
            print(f"    Säule {u['pillar']}: {u['organization']!r} ({u['model']})", file=sys.stderr)
        note = "\n".join(
            f"- [ ] Säule {u['pillar']}: {u['organization']!r} ({u['model']}) — Session {args.session_id}"
            for u in unresolved
        )
        with (ROOT / "organizations_unresolved.md").open("a") as f:
            f.write(note + "\n")
    if args.led_by_wart:
        summarizer = {
            **wart_cfg,
            "label": wart_cfg.get("label", "Der Wart"),
            "max_output_tokens": 2048,
        }
        summary_prompt = prompts.WART_SUMMARY
    else:
        summarizer = config["summarizer"]
        summary_prompt = None
    print(f"  {summarizer['label']} ({summarizer['model']}) …")
    summary, dissent_highlights, sum_usage = generate_summary(
        args.question,
        r2,
        recommendations,
        dissent_md,
        summarizer,
        raw_dir,
        summary_prompt=summary_prompt,
    )
    if args.led_by_wart:
        accumulate_wart_usage(wart_usage, sum_usage)
        refresh_wart_cost()
    else:
        usage_by_model.setdefault(summarizer["model"], {"input_tokens": 0, "output_tokens": 0})
        usage_by_model[summarizer["model"]]["input_tokens"] += sum_usage["input_tokens"]
        usage_by_model[summarizer["model"]]["output_tokens"] += sum_usage["output_tokens"]

    all_specs = config["models"] + ([] if args.led_by_wart else [summarizer])
    costs = compute_costs(usage_by_model, all_specs, fx, wart_cost_entry)
    check_budget(costs, args.budget_cap, "gesamt")

    def votes_of(round_votes):
        return [
            {
                "model": v["model"],
                "content_md": strip_json_block(v["text"]),
                "confidence": (v["parsed"] or {}).get("confidence"),
                "recommendations": structured_vote_recs(v["parsed"]),
            }
            for v in round_votes
        ]

    rounds = []
    if wart_opening_md:
        rounds.append({"round": -1, "kind": "wart_opening", "content_md": wart_opening_md})
    if wart_dossier:
        rounds.append({"round": 0, "kind": "wart_dossier", "wart": wart_dossier})
    if wart_moderation_md:
        rounds.append({"round": 1.5, "kind": "wart_moderation", "content_md": wart_moderation_md})
    rounds.extend(
        [
            {"round": 1, "kind": "initial_vote", "votes": votes_of(r1)},
            {"round": 2, "kind": "final_vote", "votes": votes_of(r2)},
        ]
    )

    prompts_dict = {"system": system, "round1": round1_prompt, "round2": prompts.ROUND2}
    if wart_dossier_prompt:
        prompts_dict["wart_dossier"] = wart_dossier_prompt
    if wart_opening_prompt:
        prompts_dict["wart_opening"] = wart_opening_prompt
    if wart_moderation_prompt:
        prompts_dict["wart_moderation"] = wart_moderation_prompt

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
        "prompts": prompts_dict,
        "rounds": rounds,
        "dissent_md": dissent_md,
        "recommendations": recommendations,
        "unresolved_votes": unresolved,
        "costs": costs,
    }
    if args.led_by_wart:
        session["designation"] = "Gründungssitzung"
        session["led_by"] = {
            "model": wart_cfg["model"],
            "label": wart_cfg.get("label", wart_cfg["model"]),
        }
        if wart_opening_md:
            session["wart_opening_md"] = wart_opening_md
        elif wart_opening_refusal:
            session["wart_opening_refusal"] = wart_opening_refusal
        if wart_moderation_md:
            session["wart_moderation_md"] = wart_moderation_md
        elif wart_moderation_refusal:
            session["wart_moderation_refusal"] = wart_moderation_refusal
    if wart_dossier:
        session["wart_dossier"] = wart_dossier
    elif wart_dossier_refusal:
        session["wart_dossier_refusal"] = wart_dossier_refusal

    (out_dir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
    print(f"\nProtokoll geschrieben: {out_dir / 'session.json'}")
    print(f"Kosten der Sitzung: {costs['total']} €")

    advance_schedule(today)


if __name__ == "__main__":
    main()
