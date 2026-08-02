"""P4 — Der Votum-JSON-Block gehört nicht in dissent_md.

`extract_dissent` erfasste den Dissens-Abschnitt bis Textende und zog damit den
abschließenden Votum-Codeblock mit hinein — inklusive einer modellbehaupteten
`donation_url`, die die kuratierte Registry gerade NICHT ist. `build_dissent` streift
den Block jetzt am SELBEN Fundort ab, den der Votum-Parser nutzt (`_votum_block_span`),
bevor der Abschnitt gelesen wird. Der Dissens-Wortlaut bleibt vollständig; nur der
abschließende Maschinenblock fällt weg — ein json-Zitat MITTEN im Dissens bleibt.

Nicht rückwirkend: `sessions/**` bleibt unverändert; repariert ist die Erhebung
künftiger Läufe. Geprüft gegen den echten Rohtext (Schlussvotum Anthropic) aller drei
Bestandssitzungen.
"""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
ROOT = GREMIUM.parent
sys.path.insert(0, str(GREMIUM))

import run_session  # noqa: E402

SESSIONS = ["2026-07", "2026-07b", "2026-07c"]


def _anthropic_final_vote_text(session_id):
    """Roher Modelltext des Schlussvotums (Anthropic) aus dem Rekord."""
    d = json.loads((ROOT / "sessions" / session_id / "raw" / "r2-anthropic.json").read_text())
    return "".join(b.get("text", "") for b in d["content"] if isinstance(b, dict))


@pytest.mark.parametrize("session_id", SESSIONS)
def test_real_dissent_no_votum_no_prose_loss(session_id):
    text = _anthropic_final_vote_text(session_id)
    old = run_session.extract_dissent(text)
    if old is None:
        pytest.skip(f"{session_id}: Anthropic-Schlussvotum hat keinen Dissens-Abschnitt")

    fixed = run_session.extract_dissent(run_session.strip_votum_block(text))

    # Kein Votum-Block mehr, keine modellbehauptete Maschinen-URL.
    assert "```json" not in fixed
    assert "donation_url" not in fixed
    # Prosa bytegleich mit vorher, bis zum Blockbeginn (kein Wort Dissens verloren).
    cut = old.find("```json")
    prose_before = (old[:cut] if cut != -1 else old).rstrip()
    assert fixed == prose_before


def test_fix_is_not_vacuous_removes_real_votum():
    # Mindestens eine Bestandssitzung zeigt den Bug tatsächlich — sonst prüft der Test nichts.
    removed = []
    for sid in SESSIONS:
        old = run_session.extract_dissent(_anthropic_final_vote_text(sid)) or ""
        if "```json" in old:
            fixed = run_session.extract_dissent(
                run_session.strip_votum_block(_anthropic_final_vote_text(sid))
            )
            assert "```json" not in fixed
            removed.append(sid)
    assert removed, "kein Bestandstext zeigt den Votum-im-Dissens-Bug — Test wäre vacuous"


def test_json_quote_mid_dissent_is_kept():
    # Ein json-Block MITTEN im Dissens (Zitat) bleibt; nur der ABSCHLIESSENDE Votumblock fällt.
    text = (
        "## Dissens\n"
        "Ich zitiere die strittige Behauptung des Modells:\n"
        '```json\n{"claim": "strittig"}\n```\n'
        "und widerspreche ihr im folgenden Absatz ausführlich.\n"
        '```json\n{"pillar": "A", "organization": "X", "conditional": false}\n```\n'
    )
    fixed = run_session.extract_dissent(run_session.strip_votum_block(text))
    assert "strittig" in fixed                 # Zitat bleibt
    assert "widerspreche ihr" in fixed         # Prosa hinter dem Zitat bleibt
    assert '"pillar"' not in fixed             # abschließender Votumblock weg
    assert fixed.count("```json") == 1         # genau der eine Zitat-Block bleibt


def test_build_dissent_joined_has_no_votum():
    # Der zusammengesetzte dissent_md (mehrere Modelle) trägt keinen Votumblock mehr.
    votes = [{"label": sid, "text": _anthropic_final_vote_text(sid)} for sid in SESSIONS]
    joined = run_session.build_dissent(votes)
    assert "```json" not in joined
    assert "donation_url" not in joined
