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
import math
from decimal import Decimal
import openrouter
import openrouter_scout
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

import prompts  # noqa: E402
import organizations  # noqa: E402
from ballot_status import check_contract, read_decision  # noqa: E402
from envtools import load_env, require_keys  # noqa: E402
from scout_context import blind_research, historical_comparison  # noqa: E402
from process_config import (  # noqa: E402
    configured_scouts,
    configured_wart,
    feature_enabled,
    validate_scout_transport,
)


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


def parse_addressed_challenge(text, author_model, participant_models):
    """Strikter 0.5-Vertrag; Beratungsprosa wird nie zur Struktur geparst."""
    parsed = extract_json_block(text)
    if not isinstance(parsed, dict):
        raise ValueError("kein strukturierter JSON-Block")
    target = parsed.get("target_model_id")
    allowed = set(participant_models) - {author_model}
    if target not in allowed:
        raise ValueError(f"target_model_id {target!r} ist keine fremde Teilnehmer-ID")
    stance = parsed.get("stance")
    if stance not in {"support", "dispute", "refine"}:
        raise ValueError("stance muss support, dispute oder refine sein")
    for field in ("claim", "challenge", "why_decisive"):
        if not isinstance(parsed.get(field), str) or not parsed[field].strip():
            raise ValueError(f"{field} fehlt oder ist leer")
    evidence_question = parsed.get("evidence_question")
    if evidence_question is not None and not isinstance(evidence_question, str):
        raise ValueError("evidence_question muss String oder null sein")
    return {
        "target_model_id": target,
        "stance": stance,
        "claim": parsed["claim"].strip(),
        "challenge": parsed["challenge"].strip(),
        "why_decisive": parsed["why_decisive"].strip(),
        "evidence_question": evidence_question.strip() if isinstance(evidence_question, str) else None,
    }


def challenges_for_model(exchanges, model):
    addressed = [e for e in exchanges if e.get("status") == "valid" and e.get("target_model_id") == model]
    if not addressed:
        return "Keine gültige Erwiderung wurde an deine Modell-ID gerichtet."
    return "\n\n".join(
        f"### Erwiderung von {e['model']}\n\n"
        f"Haltung: {e['stance']}\n\n"
        f"Behauptung: {e['claim']}\n\n"
        f"Erwiderung: {e['challenge']}\n\n"
        f"Entscheidungsrelevanz: {e['why_decisive']}\n\n"
        f"Belegfrage: {e['evidence_question'] or 'keine'}"
        for e in addressed
    )


def extract_dissent(text):
    m = re.search(r"##\s*Dissens\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL)
    return m.group(1).strip() if m else None


def extract_search_queries(text):
    section = re.search(r"##\s*Suchanfragen\s*\n(.*?)(?=\n#{2,}\s|\Z)", text, re.DOTALL)
    if not section:
        return []
    queries = []
    for line in section.group(1).splitlines():
        item = re.match(r"\s*(?:[-·*]|\d+[.)])\s+(.+?)\s*$", line)
        if not item:
            continue
        query = item.group(1).strip()
        if len(query) >= 2 and query[0] == query[-1] and query[0] in {'"', '`'}:
            query = query[1:-1].strip()
        if query:
            queries.append(query)
    return queries


def recorded_search_queries(text, api_queries):
    """Beobachtete API-Anfragen sind kanonisch; Modellprosa ist nur Fallback."""
    return list(api_queries) if api_queries else extract_search_queries(text)


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


def scout_dossier_prompt(scouts, question, as_of, prior_id, prior, led_by_wart, scout_question=None):
    """The independent research question never defaults to a historical brief."""
    if blind_research(scouts):
        return prompts.SCOUT_BLIND_USER.format(
            question=scout_question or prompts.SCOUT_BLIND_QUESTION, as_of=as_of
        )
    if not prior:
        sys.exit("Abbruch: keine Vorgänger-Sitzung für Dossier gefunden.")
    if led_by_wart:
        return prompts.SCOUT_FOUNDING_DOSSIER_USER.format(
            question=question,
            prior_session_id=prior_id,
            prior_session_date=prior.get("date"),
            pillar_a_context=pillar_a_context(prior),
        )
    return prompts.SCOUT_DOSSIER_USER.format(
        question=question,
        prior_session_id=prior_id,
        prior_session_date=prior.get("date"),
        prior_recommendations=summarize_recommendations(prior),
    )


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


def call_scout_dossier(scout_cfg, system, user, raw_dir):
    validate_scout_transport(scout_cfg)
    if scout_cfg.get("transport") == "openrouter_api":
        return openrouter_scout.call_scout(scout_cfg, system, user, raw_dir)
    if scout_cfg.get("family") == "google":
        from google_scout import call_google_scout

        return call_google_scout(
            scout_cfg, system, user, raw_dir, "r0-wart.json"
        )
    if scout_cfg.get("family") != "anthropic":
        raise RuntimeError(
            f"Kein freigegebener Web-Suche-Adapter für Scout-Familie "
            f"{scout_cfg.get('family')!r}. Provider erst nach Messung und Steward-Entscheid anbinden."
        )
    import anthropic

    client = anthropic.Anthropic()
    max_uses = scout_cfg.get("max_web_search_uses", 15)
    print(f"  Modell: {scout_cfg['model']}")
    print(f"  Web-Suche: max. {max_uses} Anfragen")

    # Streaming Pflicht bei hohem max_output_tokens (langes Dossier + Web-Suche);
    # das SDK verweigert sonst den nicht-gestreamten Call (>10 min veranschlagt).
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


def call_model(spec, system, user, max_tokens, raw_dir, tag, *, budget=None):
    transport = spec.get("transport", "api")
    if transport == "openrouter_api":
        if budget is None:
            raise openrouter.OpenRouterError("OpenRouter requires an explicit budget")
        return openrouter.call(spec, system, user, max_tokens, raw_dir, tag, **budget)
    if transport != "api":
        raise ValueError("Unsupported transport")
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


def structured_vote_recs(parsed, *, ballot_contract=None):
    """Registry-aufgelöste Voten je Säule für die Persistenz in session.json.

    Erlaubt dem Frontend, Protokollspalten + Revision (wer nannte r1 vs r2 welche
    Org) zu rendern, OHNE Prosa zu parsen. Unbekannte Org → weggelassen (der
    Aggregator meldet sie separat als unresolved); nie stiller Textfall.
    """
    check_contract(ballot_contract)
    out = []
    for r in _vote_recommendations(parsed):
        pillar = r.get("pillar")
        if ballot_contract:
            decision = read_decision(r)
            if not decision or pillar not in ('A', 'B', 'C', 'D'):
                continue
            if decision == 'abstain':
                out.append({'pillar':pillar, 'decision':decision, 'organization_id':None,
                    'organization':None, 'title':r.get('title'), 'confidence':r.get('confidence'),
                    'conditional':None, 'reservation':None, 'abstention_reason':r['abstention_reason']})
                continue
        org_id = organizations.resolve(r.get("organization"))
        if pillar not in ("A", "B", "C", "D") or org_id is None:
            continue
        # Rohvotum je Modell (Anzeige): conditional strukturell; None, wenn das Modell
        # kein gültiges Bool lieferte (der Aggregator schließt es separat als ungültig aus).
        _valid, cond, reservation = read_conditional(r)
        out.append({
            **({'decision':'recommend', 'abstention_reason':None} if ballot_contract else {}),
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


def aggregate_recommendations(final_votes, total_models=None, procedure_version=None, *, ballot_contract=None):
    """Deterministische Aggregation gegen die Organisations-Registry.

    Bis 0.5: >=2 verschiedene Modelle; ab 0.6: Mehrheit >=3 bei Nenner 5.
    Die Stimmen lösen auf dieselbe org_id auf. Auflösung
    ausschließlich via organizations.resolve() (Alias-Match, kein Modell, kein
    Fuzzy). donation_url + canonical_name kommen aus der Registry, nie aus dem
    Votum (Halluzinationsschutz).

    Gibt (recommendations, unresolved) zurück. `unresolved` sammelt Voten mit
    unbekannter Organisation — sie werden NIE stillschweigend als Dissens
    verbucht, sondern explizit ausgewiesen.
    """
    if procedure_version not in (None, '0.5', '0.6'):
        raise ValueError('Unbekannte Verfahrensversion')
    check_contract(ballot_contract)
    if ballot_contract and procedure_version != '0.6':
        raise ValueError('Explizite Enthaltung benötigt Verfahren 0.6')
    if ballot_contract and (len(final_votes) > 5 or len({v['label'] for v in final_votes}) != len(final_votes)):
        raise ValueError('Doppelte oder zusätzliche Sitzstimme')
    total = 5 if procedure_version == '0.6' else (total_models or len(final_votes))
    threshold = 3 if procedure_version == '0.6' else 2
    recs = []
    unresolved = []
    for pillar in ("A", "B", "C", "D"):
        candidates = []
        abstentions = []
        contract_warnings = []
        for vote in final_votes:
            entries = _vote_recommendations(vote["parsed"])
            if ballot_contract:
                entries = entries if isinstance(entries, list) else []
                entries = [r for r in entries if isinstance(r, dict) and r.get('pillar') == pillar]
                if len(entries) != 1 or read_decision(entries[0]) is None:
                    contract_warnings.append(f"{vote['label']}: Säule {pillar} — fehlende, doppelte oder widersprüchliche strukturierte Entscheidung; ungültig.")
                    continue
                if entries[0]['decision'] == 'abstain':
                    abstentions.append({'model':vote['label'], 'reason':entries[0]['abstention_reason']})
                    continue
            for r in entries:
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
        # der Rest der teilnehmenden Modelle abzüglich expliziter Enthaltungen.
        # Enthaltungen werden separat gezählt, niemals als Zustimmung/ungültig.
        # Damit sind alle vier Fälle unterscheidbar — Konsens · Dissens aus
        # vollständigen Voten · unvollständig · gar nichts (votes_valid=0) — und die
        # Tafel entscheidet selbst, ab wann sie welchen Zustand zeigt.
        valid_models = sorted({c["_model"] for c in candidates})
        votes_valid = len(valid_models)
        votes_invalid = max(0, total - votes_valid - len(abstentions))
        abstention_fields = ({'votes_abstained':len(abstentions),
                              'abstentions':sorted(abstentions, key=lambda a:a['model'])} if ballot_contract else {})
        abstention_clause = f" {len(abstentions)} Enthaltung(en); der Nenner bleibt fünf." if abstentions else ''
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
                **abstention_fields,
                "pillar": pillar,
                "has_consensus": False,
                "votes_valid": 0,
                "votes_invalid": votes_invalid,
                "title": None,
                "organization": None,
                "donation_url": None,
                "confidence": None,
                "rationale_md": ("Für diese Säule liegt keine auswertbare Empfehlung vor." + abstention_clause
                    if abstentions else "Die Antworten zu diesem Bereich waren nicht auswertbar. Die Rohdaten liegen im Protokoll."),
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

        if max_support >= threshold and not tie:
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
                **abstention_fields,
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
                "rationale_md": f"{'Mehrheit' if procedure_version == '0.6' else 'Konvergenz'} im Schlussvotum: {len(best_models)} von "
                f"{total} Modellen{cond_clause} empfehlen diese Organisation "
                f"({', '.join(best_models)}).{abstention_clause}{invalid_clause} Begründungen in den Schlussvoten.",
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
            if procedure_version == '0.6':
                note = 'Keine Organisation erreicht die erforderliche Mehrheit von drei der fünf Sitzstimmen.'
            rec = {
                **abstention_fields,
                "pillar": pillar,
                "has_consensus": False,
                "votes_valid": votes_valid,
                "votes_invalid": votes_invalid,
                "tie": tie,
                "title": "Keine Mehrheit — Einzelvoten" if procedure_version == '0.6' else "Kein Konsens — Einzelvoten",
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
                "rationale_md": note + abstention_clause,
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
    tag = "summary-wart" if summary_prompt else "summary-anthropic"
    if summarizer.get("transport") == "openrouter_api":
        text, usage, raw = openrouter_scout.call_wart(summarizer, system, user, raw_dir, tag, max_tokens)
    else:
        text, usage, raw = call_anthropic(summarizer["model"], system, user, max_tokens)
    (raw_dir / f"{tag}.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str)
    )
    summary_text, refusal = wart_step_result(text, raw, f"{tag}.json")
    if refusal is not None:
        # Verweigerung: DEGRADIEREN, nicht abbrechen (Steward-Entscheid). Die Kurzfassung
        # ist Darstellungsschicht — sie paraphrasiert, was ungekürzt darunter steht. Eine
        # Sitzung ohne Kurzfassung ist unvollständig, aber wahr; eine abgestürzte Sitzung
        # ist gar nichts. summary="" besteht das Tor (required, string).
        return "", [], usage, refusal
    parsed = extract_json_block(summary_text)
    if not parsed or "summary" not in parsed:
        raise RuntimeError("Summarizer lieferte kein gültiges JSON mit summary")
    return parsed.get("summary", ""), parsed.get("dissent_highlights", []), usage, None


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
    if wart_cfg.get("transport") == "openrouter_api":
        result = openrouter_scout.call_wart(wart_cfg, system, user, raw_dir, tag, max_tokens)
        (raw_dir / f"{tag}.json").write_text(json.dumps(result[2], indent=2))
        return result
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
    if "billed_usd" in usage:
        total["billed_usd"] = str(openrouter.amount(total.get("billed_usd", "0")) + openrouter.amount(usage["billed_usd"]))
        total["research_provenance"] = usage.get("research_provenance")


def compute_wart_cost(usage, wart_cfg, fx):
    if "billed_usd" in usage:
        usd = openrouter.amount(usage["billed_usd"])
        provenance = usage.get("research_provenance") or {}
        return {"model": wart_cfg["model"], "label": wart_cfg.get("label", wart_cfg["model"]),
                "input_tokens": usage["input_tokens"], "output_tokens": usage["output_tokens"],
                "web_search_requests": provenance.get("web_search_requests"),
                "cost_basis": "billed", "usd": float(usd), "eur": float(usd * openrouter.amount(fx))}
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


def compute_costs(usage_by_model, model_specs, fx, role_costs=None):
    by_model = []
    for spec in model_specs:
        u = usage_by_model.get(spec["model"], {"input_tokens": 0, "output_tokens": 0})
        routed = spec.get("transport") == "openrouter_api"
        usd = float(openrouter.amount(u.get("billed_usd", "0"))) if routed else (
            u["input_tokens"] / 1e6 * spec["usd_per_1m_input"]
            + u["output_tokens"] / 1e6 * spec["usd_per_1m_output"]
        )
        by_model.append(
            {
                "model": spec["model"],
                "label": spec.get("label", spec["model"]),
                "input_tokens": u["input_tokens"],
                "output_tokens": u["output_tokens"],
                "usd": usd if routed else round(usd, 4),
                "eur": usd * fx if routed else round(usd * fx, 4),
                **({"cost_basis": "billed", "transport": "openrouter_api"} if routed else {}),
            }
        )
    if role_costs:
        by_model.extend(role_costs if isinstance(role_costs, list) else [role_costs])
    total_eur = round(sum(c["eur"] for c in by_model), 2)
    return {"currency": "EUR", "total": total_eur, "fx_rate_usd_eur": fx, "by_model": by_model}


def check_budget(costs, cap_eur, label):
    if not math.isfinite(cap_eur) or cap_eur < 0:
        raise ValueError("Budgetdeckel muss endlich und nicht negativ sein")
    by_model = costs.get("by_model")
    total = sum(entry["eur"] for entry in by_model) if by_model else costs["total"]
    if not math.isfinite(total) or total < 0:
        raise SystemExit("Abbruch: Kostenstand ist nicht auswertbar.")
    print(f"  Zwischenkosten ({label}): {total:.2f} €")
    if total > cap_eur:
        raise SystemExit(
            f"Abbruch: Budgetdeckel {cap_eur:.2f} € überschritten "
            f"({total:.4f} €, Stand {label}). Kein weiterer Modellaufruf."
        )


# ---------------------------------------------------------------- main

def openrouter_phase_barrier(models, entries, kind, raw_dir):
    """Strict OpenRouter phase contract; API-only historical procedure unchanged."""
    if not any(m.get("transport") == "openrouter_api" for m in models):
        return
    valid = len(entries) == len(models) and {e["model"] for e in entries} == {m["model"] for m in models}
    for entry in entries:
        if kind == "challenge":
            valid = valid and entry.get("status") == "valid"
        else:
            try:
                raw_recs = _vote_recommendations(entry.get("parsed"))
                recommendations = structured_vote_recs(entry.get("parsed"))
                valid = valid and len(raw_recs) == 4 and len(recommendations) == 4 and {
                    r["pillar"] for r in recommendations
                } == {"A", "B", "C", "D"} and all(read_conditional(r)[0] for r in raw_recs)
            except (AttributeError, TypeError, ValueError):
                valid = False

    if not valid:
        (raw_dir / f"phase-{kind}-invalid.json").write_text(
            json.dumps(entries, indent=2, ensure_ascii=False) + "\n"
        )
        raise SystemExit(f"Abbruch: OpenRouter-Phasenbarriere {kind} nicht erfüllt; Rohdaten erhalten, keine Folgephase")


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
        "--scout-question",
        help="Eigenständige Suchfrage für die drei blinden Scouts; Standard: offene Frage über vier Säulen",
    )
    parser.add_argument(
        "--led-by-wart",
        action="store_true",
        help="Gründungssitzung: Wart eröffnet, moderiert, schreibt Kurzfassung (impliziert --with-dossier)",
    )
    parser.add_argument("--budget-cap", type=float, default=15.0)
    parser.add_argument('--live-council', action='store_true', help='Isolierter Backend-Pilot 0.6, ohne Publikation')
    parser.add_argument('--observe-costs', action='store_true', help='Pilot: belegte Ist-Kosten beobachten, ohne Input-Bound/Abschlussreserve; Key-Limit bleibt')
    parser.add_argument('--stop-after-first', action='store_true', help='Pilot nach erstem gültigen Erstvotum pausieren; mit --resume weiterverwenden')
    parser.add_argument('--dossier-json', help='Vorhandener blinder Drei-Scout-Journalrekord')
    parser.add_argument('--output-dir', help='Lokaler Pilotordner außerhalb der veröffentlichten Rekorde')
    parser.add_argument('--resume', action='store_true', help='Bestätigte Aufrufe wiederverwenden; keine Inferenzwiederholung')
    parser.add_argument('--live-feed-dir', help='Optionales Dateiziel für den ausdrücklich sichtbaren Live-Pilot; kein Upload')
    parser.add_argument('--public-session', action='store_true', help='Freigegebene öffentliche Sitzung: Originalrekord in sessions/, Rotation nach gültigem Abschluss')
    parser.add_argument('--live-feed-ssh', help='Vorhandener SSH-Deploy-Host für synchrone Live-Publikation')
    parser.add_argument('--live-feed-identity', help='Optionaler Pfad zum vorhandenen SSH-Deploy-Key')
    args = parser.parse_args()
    if not math.isfinite(args.budget_cap) or args.budget_cap < 0:
        parser.error("--budget-cap muss endlich und nicht negativ sein")
    if args.observe_costs and not args.live_council:
        parser.error('--observe-costs ist ausschließlich für den isolierten Live-Pilot zulässig')
    if args.stop_after_first and not args.live_council:
        parser.error('--stop-after-first ist ausschließlich für den isolierten Live-Pilot zulässig')
    if args.live_feed_dir and not args.live_council:
        parser.error('--live-feed-dir benötigt --live-council')
    if (args.public_session or args.live_feed_ssh or args.live_feed_identity) and not args.live_council:
        parser.error('Öffentliche Sitzung/SSH-Publisher benötigen --live-council')
    if args.live_feed_ssh and not args.live_feed_dir:
        parser.error('--live-feed-ssh benötigt ein lokales --live-feed-dir als Veröffentlichungsbeleg')

    if args.led_by_wart:
        args.with_dossier = True

    config = json.loads((HERE / "config.json").read_text())
    if args.live_council:
        from live_session import run
        result = run(ROOT, config, args)
        if args.public_session and result['status'] == 'completed':
            from council_state import accept_session
            accept_session(ROOT, ROOT/'sessions'/result['id'], config)
            print(f"Öffentlicher Live-Rat {result['id']}: abgeschlossen und übernommen")
        else:
            print(f"Live-Rat-Pilot {result['id']}: {result['status']}; keine Rekordübernahme oder Rotation")
        return
    if feature_enabled(config, 'live_council'):
        parser.error('0.6-Backend derzeit über --live-council und --dossier-json starten; Frontend/Rollout noch offen')
    routed = openrouter.validate_roster(config["models"])
    if routed:
        openrouter.amount(config["fx_rate_usd_eur"])
        if config["fx_rate_usd_eur"] <= 0:
            sys.exit("Abbruch: positiver Wechselkurs erforderlich")
    try:
        scouts = configured_scouts(config)
        wart_cfg = configured_wart(config)
    except ValueError as exc:
        sys.exit(f"Abbruch: {exc}")
    if args.with_dossier:
        try:
            for scout in scouts:
                validate_scout_transport(scout)
        except ValueError as exc:
            sys.exit(f"Abbruch: {exc} Kein Verzeichnis angelegt.")
    role_specs = ([wart_cfg] if args.led_by_wart else [config["summarizer"]])
    if any(s.get("transport", "api") != "api" and s.get("role") != "wart" for s in role_specs):
        sys.exit("Abbruch: Redaktion bleibt direkt")
    if args.with_dossier:
        role_specs += scouts
    load_env(HERE, ROOT)
    gateway_roles = [s for s in role_specs if s.get("transport") == "openrouter_api"]
    direct_roles = [s for s in role_specs if s not in gateway_roles]
    require_keys(*openrouter.required_keys(config["models"] + direct_roles), *(["OPENROUTER_API_KEY"] if gateway_roles else []))
    openrouter.preflight(config["models"])
    if routed:
        # This preflight happens before directories, even for insufficient budget.
        for spec in config["models"]:
            openrouter.reserve(spec, config["max_output_tokens"], 0, args.budget_cap, config["fx_rate_usd_eur"])
    deliberation_05 = feature_enabled(config, "deliberation_0_5")
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
    scout_cfg = scouts[0]

    usage_by_model = {m["model"]: {"input_tokens": 0, "output_tokens": 0} for m in config["models"]}
    scout_usages = {s["model"]: empty_wart_usage() for s in scouts}
    wart_usage = empty_wart_usage()
    scout_cost_entries = []
    wart_cost_entry = None

    def refresh_role_costs():
        nonlocal scout_cost_entries, wart_cost_entry
        scout_cost_entries = [
            compute_wart_cost(scout_usages[s["model"]], s, fx)
            for s in scouts
            if any(scout_usages[s["model"]].values())
        ]
        if wart_usage["input_tokens"] or wart_usage["output_tokens"] or wart_usage["web_search_requests"]:
            wart_cost_entry = compute_wart_cost(wart_usage, wart_cfg, fx)

    def interim_costs(summarizer=None):
        refresh_role_costs()
        specs = config["models"] + ([summarizer] if summarizer else [config["summarizer"]])
        role_costs = scout_cost_entries + ([wart_cost_entry] if wart_cost_entry else [])
        return compute_costs(usage_by_model, specs, fx, role_costs)

    def record_usage(spec, usage):
        u = usage_by_model[spec["model"]]
        u["input_tokens"] += usage["input_tokens"]
        u["output_tokens"] += usage["output_tokens"]
        if spec.get("transport") == "openrouter_api":
            u["billed_usd"] = str(openrouter.amount(u.get("billed_usd", "0")) + openrouter.amount(usage["billed_usd"]))
        check_budget(interim_costs(), args.budget_cap, f"nach {spec['model']}")

    def council_call(spec, system, user, max_tokens, raw_dir, tag):
        if spec.get("transport") == "openrouter_api":
            spent = sum(Decimal(str(c["eur"])) for c in interim_costs()["by_model"])
            return call_model(spec, system, user, max_tokens, raw_dir, tag,
                              budget={"spent_eur": spent, "cap_eur": args.budget_cap, "fx": fx})
        return call_model(spec, system, user, max_tokens, raw_dir, tag)

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
        print(f"Eröffnung — Wart ({wart_cfg['model']})")
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

    # -------- Runde 0 (Scout-Dossier; historische Rekordfelder heißen wart_dossier)
    if args.with_dossier:
        wart_dossier_prompt = scout_dossier_prompt(
            scouts, args.question, today, prior_id, prior, args.led_by_wart, args.scout_question
        )
        (raw_dir / "prompt-r0-wart.txt").write_text(wart_dossier_prompt)
        print(f"Runde 0 — {len(scouts)} Scout-Dossier{'s' if len(scouts) != 1 else ''} (+ Web-Suche)")
        valid_dossiers = []
        dossier_failures = []
        for index, active_scout in enumerate(scouts, start=1):
            scout_dir = raw_dir if len(scouts) == 1 else raw_dir / f"scout-{index}"
            scout_dir.mkdir(parents=True, exist_ok=True)
            print(f"  Scout {index}: {active_scout['model']}")
            try:
                scout_system = prompts.scout_system_for(active_scout, prompts.SCOUT_DOSSIER_SYSTEM)
                if active_scout.get("research_role"):
                    (scout_dir / "prompt-scout-system.txt").write_text(scout_system)
                text, usage, raw, api_queries = call_scout_dossier(
                    active_scout,
                    scout_system,
                    wart_dossier_prompt,
                    scout_dir,
                )
                (scout_dir / "r0-wart-content.md").write_text(text)
                accumulate_wart_usage(scout_usages[active_scout["model"]], usage)
                check_budget(interim_costs(), args.budget_cap, f"nach Scout {index}")
                artifact = (
                    "r0-wart.json" if len(scouts) == 1 else f"scout-{index}/r0-wart.json"
                )
                dossier_text, refusal = wart_step_result(text, raw, artifact)
                if dossier_text is None:
                    dossier_failures.append({**refusal, "model": active_scout["model"]})
                    print(
                        f"    Verweigerung (stop_reason={refusal['stop_reason']}) — "
                        "kein Inhalt übernommen."
                    )
                    continue
                content_md = strip_json_block(dossier_text) + openrouter_scout.disclosure(usage.get("research_provenance"))
                structured = {}
                if "max_findings" in active_scout:
                    parsed_dossier = extract_json_block(dossier_text)
                    if not isinstance(parsed_dossier, dict) or not isinstance(parsed_dossier.get("findings"), list):
                        raise RuntimeError("Scout-Dossier ohne strukturierte findings")
                    if len(parsed_dossier["findings"]) > active_scout["max_findings"]:
                        raise RuntimeError("Scout überschreitet max_findings — Dossier nicht übernommen")
                    structured = {k: parsed_dossier.get(k) for k in ("findings", "rejected_findings", "delta_assessment")}
                valid_dossiers.append(
                    {
                        "model": active_scout["model"],
                        "label": active_scout.get("label", active_scout["model"]),
                        **({"research_role": active_scout["research_role"]} if active_scout.get("research_role") else {}),
                        "content_md": content_md,
                        "search_queries": recorded_search_queries(dossier_text, api_queries),
                        **structured,
                        **({"research_provenance": usage["research_provenance"]} if "research_provenance" in usage else {}),
                    }
                )
            except openrouter_scout.ScoutAccountingError:
                raise
            except Exception as exc:  # noqa: BLE001
                if len(scouts) == 1:
                    raise
                dossier_failures.append(
                    {
                        "stop_reason": "caller_error",
                        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                        "raw_artifact": f"raw/scout-{index}/",
                        "model": active_scout["model"],
                        "reason": str(exc),
                    }
                )
        refresh_role_costs()
        costs_by_model = {c["model"]: c for c in scout_cost_entries}
        for dossier in valid_dossiers:
            dossier["costs"] = costs_by_model.get(dossier["model"])

        if valid_dossiers:
            if len(scouts) == 1:
                wart_dossier = valid_dossiers[0]
            else:
                all_queries = []
                for dossier in valid_dossiers:
                    for query in dossier["search_queries"]:
                        if query not in all_queries:
                            all_queries.append(query)
                combined = "\n\n---\n\n".join(
                    f"## {d['label']} ({d['model']})\n\n{d['content_md']}"
                    + ("\n\n```json\n" + json.dumps({"findings": d["findings"]}, ensure_ascii=False) + "\n```" if "findings" in d else "")
                    for d in valid_dossiers
                )
                wart_dossier = {
                    "model": valid_dossiers[0]["model"],
                    "label": f"Scout-Dossiers ({len(valid_dossiers)} von {len(scouts)})",
                    "content_md": combined,
                    "search_queries": all_queries,
                    "scouts": valid_dossiers,
                    "failures": dossier_failures,
                }
            if len(scouts) == 1:
                # Default-off-Vertrag: Der bestehende Ein-Scout-Prompt bleibt
                # wortgleich, solange two_scouts nicht aktiviert ist.
                dossier_section = (
                    "## Scout-Dossier (Runde 0)\n\n"
                    f"Der Scout ({scout_cfg['model']}) hat vor den Einzelvoten folgendes "
                    "Evidenz-Dossier geliefert. Es enthält keine Empfehlung — nur Fakten "
                    "und Quellen.\n\n---\n\n"
                    f"{wart_dossier['content_md']}\n\n---"
                )
            else:
                dossier_count_text = (
                    "Ein unabhängiges Scout-Dossier wurde"
                    if len(valid_dossiers) == 1
                    else f"{len(valid_dossiers)} unabhängige Scout-Dossiers wurden"
                )
                dossier_section = (
                    "## Scout-Dossier (Runde 0)\n\n"
                    f"{dossier_count_text} vor den Einzelvoten geliefert. Die Dossiers enthalten "
                    "keine Empfehlung — nur Fakten und Quellen.\n\n---\n\n"
                    f"{wart_dossier['content_md']}\n\n---"
                )
            if blind_research(scouts):
                wart_dossier["research_mode"] = "blind_then_compare"
                # The Council may compare only after all independent searches.
                comparison = historical_comparison(ROOT, today, prior_id, prior)
                (raw_dir / "prompt-history-comparison.txt").write_text(comparison)
                dossier_section += "\n\n" + comparison
        else:
            # dossier_section bleibt "" — kein fiktives Dossier im Ratsprompt.
            wart_dossier_refusal = dossier_failures[0] if dossier_failures else None
            print("  Kein Scout-Dossier übernommen; die Ratsvoten laufen ohne Dossier weiter.")
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
        text, usage = council_call(spec, system, round1_prompt, max_tokens, raw_dir, "r1")
        record_usage(spec, usage)
        r1.append({**spec, "text": text, "parsed": extract_json_block(text), **({"provenance": usage["provenance"]} if "provenance" in usage else {})})
    check_budget(interim_costs(), args.budget_cap, "nach Runde 1")
    openrouter_phase_barrier(config["models"], r1, "r1", raw_dir)

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
        print(f"Moderation — Wart ({wart_cfg['model']})")
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

    # -------- Adressierte Erwiderung (0.5, standardmäßig AUS)
    exchanges = []
    if deliberation_05:
        print("Erwiderung — adressierte, überprüfbare Position")
        participant_models = [m["model"] for m in config["models"]]
        for spec, own in zip(config["models"], r1):
            others = "\n\n".join(
                f"### Erstvotum {v['label']} · Modell-ID `{v['model']}`\n\n"
                f"{strip_json_block(v['text'])}"
                for v in r1
                if v["model"] != spec["model"]
            )
            target_ids = [m for m in participant_models if m != spec["model"]]
            challenge_prompt = prompts.ADDRESSED_CHALLENGE.format(
                own_vote=strip_json_block(own["text"]),
                other_votes=others,
                target_model_ids=", ".join(f"`{m}`" for m in target_ids),
            )
            (raw_dir / f"prompt-challenge-{spec['family']}.txt").write_text(challenge_prompt)
            print(f"  {spec['label']} ({spec['model']}) …")
            try:
                text, usage = council_call(
                    spec, system, challenge_prompt, max_tokens, raw_dir, "challenge"
                )
                record_usage(spec, usage)
                content_md = strip_json_block(text)
                try:
                    structured = parse_addressed_challenge(
                        text, spec["model"], participant_models
                    )
                    exchanges.append(
                        {
                            "model": spec["model"],
                            "status": "valid",
                            "content_md": content_md,
                            **({"provenance": usage["provenance"]} if "provenance" in usage else {}),
                            **structured,
                        }
                    )
                except ValueError as exc:
                    exchanges.append(
                        {
                            "model": spec["model"],
                            "status": "invalid",
                            "content_md": content_md,
                            **({"provenance": usage["provenance"]} if "provenance" in usage else {}),
                            "target_model_id": None,
                            "failure": str(exc),
                            "raw_artifact": usage.get("provenance", {}).get("raw_artifact", f"raw/challenge-{spec['family']}.json"),
                        }
                    )
            except Exception as exc:  # noqa: BLE001
                if spec.get("transport") == "openrouter_api":
                    raise SystemExit("OpenRouter-Erwiderung fehlgeschlagen; keine weiteren Calls") from exc
                exchanges.append(
                    {
                        "model": spec["model"],
                        "status": "unavailable",
                        "content_md": "",
                        "target_model_id": None,
                        "failure": str(exc),
                    }
                )
        check_budget(interim_costs(), args.budget_cap, "nach adressierter Erwiderung")
        openrouter_phase_barrier(config["models"], exchanges, "challenge", raw_dir)

    # -------- Runde 2
    print("Runde 2 — Antwort und Schlussvoten" if deliberation_05 else "Runde 2 — Gegenlese und Schlussvoten")
    r2 = []
    for spec, own in zip(config["models"], r1):
        others = "\n\n".join(
            f"### Erstvotum {v['label']}\n\n{strip_json_block(v['text'])}"
            for v in r1
            if v["model"] != spec["model"]
        )
        if deliberation_05:
            round2_prompt = prompts.ROUND2_05.format(
                own_vote=strip_json_block(own["text"]),
                other_votes=others,
                addressed_challenges=challenges_for_model(exchanges, spec["model"]),
                moderation_section=moderation_section,
            )
            (raw_dir / f"prompt-r2-{spec['family']}.txt").write_text(round2_prompt)
        else:
            round2_prompt = prompts.ROUND2.format(
                own_vote=strip_json_block(own["text"]),
                other_votes=others,
                moderation_section=moderation_section,
            )
        print(f"  {spec['label']} ({spec['model']}) …")
        text, usage = council_call(spec, system, round2_prompt, max_tokens, raw_dir, "r2")
        record_usage(spec, usage)
        r2.append({**spec, "text": text, "parsed": extract_json_block(text), **({"provenance": usage["provenance"]} if "provenance" in usage else {})})
    check_budget(interim_costs(), args.budget_cap, "nach Runde 2")
    openrouter_phase_barrier(config["models"], r2, "r2", raw_dir)

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
    summary, dissent_highlights, sum_usage, summary_refusal = generate_summary(
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
        refresh_role_costs()
    else:
        usage_by_model.setdefault(summarizer["model"], {"input_tokens": 0, "output_tokens": 0})
        usage_by_model[summarizer["model"]]["input_tokens"] += sum_usage["input_tokens"]
        usage_by_model[summarizer["model"]]["output_tokens"] += sum_usage["output_tokens"]

    all_specs = config["models"] + ([] if args.led_by_wart else [summarizer])
    role_costs = scout_cost_entries + ([wart_cost_entry] if wart_cost_entry else [])
    costs = compute_costs(usage_by_model, all_specs, fx, role_costs)
    check_budget(costs, args.budget_cap, "gesamt")

    def votes_of(round_votes):
        return [
            {
                "model": v["model"],
                "content_md": strip_json_block(v["text"]),
                "confidence": (v["parsed"] or {}).get("confidence"),
                "recommendations": structured_vote_recs(v["parsed"]),
                **({"provenance": v["provenance"]} if "provenance" in v else {}),
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
    rounds.append({"round": 1, "kind": "initial_vote", "votes": votes_of(r1)})
    if deliberation_05:
        rounds.append({"round": 1.75, "kind": "addressed_challenge", "exchanges": exchanges})
    rounds.append({"round": 2, "kind": "final_vote", "votes": votes_of(r2)})

    prompts_dict = {
        "system": system,
        "round1": round1_prompt,
        "round2": prompts.ROUND2_05 if deliberation_05 else prompts.ROUND2,
    }
    if deliberation_05:
        prompts_dict["addressed_challenge"] = prompts.ADDRESSED_CHALLENGE
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
    if routed:
        session["council_transport"] = "openrouter_api"
    if deliberation_05:
        session["deliberation_version"] = "0.5"
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
    if summary_refusal:
        session["summary_refusal"] = summary_refusal

    (out_dir / "session.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
    print(f"\nProtokoll geschrieben: {out_dir / 'session.json'}")
    print(f"Kosten der Sitzung: {costs['total']} €")

    advance_schedule(today)


if __name__ == "__main__":
    main()
