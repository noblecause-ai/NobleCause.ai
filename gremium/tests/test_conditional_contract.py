"""§5 — conditional ist strukturelles Pflichtfeld; die Titel-Regex ist ersatzlos weg.

Der Titel wird NIE mehr geparst: „unbedingt/vorbehaltlos/nicht konditional/unconditional"
erzeugt keinen Vorbehalt. Fehlt das Feld oder ist es kein echtes JSON-Boolean, ist die
Empfehlung vertragswidrig — ungültig, markiert (votes_invalid), Warnung, kein Titel-Raten
(Codex #6 / Kimi P2 / Wart-Entscheid C).
"""

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GREMIUM = HERE.parent
sys.path.insert(0, str(GREMIUM))

import organizations  # noqa: E402
import run_session  # noqa: E402

FIXTURE = {
    "schema_version": 1,
    "organizations": [
        {"id": "hki", "canonical_name": "Helen Keller International",
         "aliases": ["Helen Keller Intl", "Helen Keller International (HKI)"],
         "donation_url": "https://hki.example/donate"},
    ],
}


@pytest.fixture(autouse=True)
def _registry(tmp_path):
    p = tmp_path / "organizations.json"
    p.write_text(json.dumps(FIXTURE))
    organizations.load_registry(p)
    yield


def r(org, title="x", conditional=False, reservation=None):
    d = {"pillar": "A", "title": title, "organization": org,
         "donation_url": "u", "confidence": 0.7}
    if conditional is not _OMIT:
        d["conditional"] = conditional
    d["reservation"] = reservation
    return d


_OMIT = object()


def vote(label, rec):
    return {"label": label, "parsed": {"recommendations": [rec]}}


def pillar_a(recs):
    return next(x for x in recs if x["pillar"] == "A")


def test_regex_gone_title_never_creates_reservation():
    # Vorbehalts-/Negationswörter im Titel, aber conditional:false → KEIN Vorbehalt.
    for title in ["Unbedingt empfohlen", "Vorbehaltlos empfohlen",
                  "Nicht konditional", "Unconditional recommendation"]:
        recs, _ = run_session.aggregate_recommendations([
            vote("Opus", r("Helen Keller Intl", title=title, conditional=False)),
            vote("GPT", r("Helen Keller International (HKI)", conditional=False)),
        ])
        a = pillar_a(recs)
        assert a["convergence"]["conditional_count"] == 0, title
        assert all(v["conditional"] is False and v["reservation"] is None
                   for v in a["convergence"]["votes"]), title


def test_missing_conditional_is_invalid_not_guessed():
    recs, _ = run_session.aggregate_recommendations([
        vote("Opus", r("Helen Keller Intl", conditional=_OMIT)),  # Feld fehlt ganz
        vote("GPT", r("Helen Keller International (HKI)", conditional=False)),
    ])
    a = pillar_a(recs)
    assert a["votes_valid"] == 1          # nur GPT gültig
    assert a["has_consensus"] is False    # Opus ungültig → kein 2er-Konsens
    assert any("ohne gültiges conditional" in w for w in a.get("warnings", []))


def test_string_false_conditional_is_invalid():
    recs, _ = run_session.aggregate_recommendations([
        vote("Opus", r("Helen Keller Intl", conditional="false")),
    ])
    a = pillar_a(recs)
    assert a["votes_valid"] == 0          # "false"-String ist kein Bool → ungültig
    assert any("conditional" in w for w in a.get("warnings", []))


def test_structured_true_counts_with_reservation():
    recs, _ = run_session.aggregate_recommendations([
        vote("Opus", r("Helen Keller Intl", conditional=True,
                       reservation="Nur vorbehaltlich einer Prüfung.")),
        vote("GPT", r("Helen Keller International (HKI)", conditional=False)),
    ])
    a = pillar_a(recs)
    assert a["has_consensus"] is True
    assert a["convergence"]["conditional_count"] == 1
    opus = next(v for v in a["convergence"]["votes"] if v["model"] == "Opus")
    assert opus["conditional"] is True and "vorbehaltlich" in opus["reservation"]
