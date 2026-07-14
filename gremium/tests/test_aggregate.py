"""Regression tests for the deterministic aggregator + org registry.

Covers exactly the failure modes that produced false non-consensus in the live
sessions: org-name variants (HKI, NTI), silently-dropped nonconforming votes
(German keys), and the correctness guard that distinct orgs are NOT merged.
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
        {
            "id": "hki",
            "canonical_name": "Helen Keller International",
            "aliases": ["Helen Keller Intl", "Helen Keller International (HKI)"],
            "donation_url": "https://hki.example/donate",
        },
        {
            "id": "nti",
            "canonical_name": "Nuclear Threat Initiative (NTI)",
            "aliases": [
                "Nuclear Threat Initiative (NTI), Biosecurity Program",
                "NTI | bio (Nuclear Threat Initiative)",
            ],
            "donation_url": "https://nti.example/donate",
        },
        {
            "id": "amf",
            "canonical_name": "Against Malaria Foundation",
            "aliases": ["Against Malaria Foundation (AMF)"],
            "donation_url": "https://amf.example/donate",
        },
    ],
}


@pytest.fixture(autouse=True)
def _registry(tmp_path):
    p = tmp_path / "organizations.json"
    p.write_text(json.dumps(FIXTURE))
    organizations.load_registry(p)
    yield


def vote(label, *recs, key="recommendations"):
    return {"label": label, "parsed": {key: list(recs)}}


def rec(pillar, org, url="https://model-hallucinated.example/x", conf=0.7):
    return {"pillar": pillar, "title": f"{org} intervention", "organization": org,
            "donation_url": url, "confidence": conf}


def pillar(recs, p):
    return next(r for r in recs if r["pillar"] == p)


def test_name_variants_reach_consensus():
    votes = [
        vote("Opus", rec("A", "Helen Keller Intl")),
        vote("GPT", rec("A", "Helen Keller International (HKI)")),
        vote("Gemini", rec("A", "Against Malaria Foundation")),
    ]
    recs, unresolved = run_session.aggregate_recommendations(votes)
    a = pillar(recs, "A")
    assert a["has_consensus"] is True
    assert a["organization"] == "Helen Keller International"
    assert a["convergence"]["count"] == 2
    assert sorted(a["convergence"]["models"]) == ["GPT", "Opus"]
    assert not unresolved


def test_nti_variants_reach_consensus():
    votes = [
        vote("GPT", rec("C", "Nuclear Threat Initiative (NTI), Biosecurity Program")),
        vote("Gemini", rec("C", "NTI | bio (Nuclear Threat Initiative)")),
    ]
    recs, _ = run_session.aggregate_recommendations(votes)
    c = pillar(recs, "C")
    assert c["has_consensus"] is True
    assert c["organization"] == "Nuclear Threat Initiative (NTI)"


def test_donation_url_comes_from_registry_not_vote():
    votes = [
        vote("Opus", rec("A", "Helen Keller Intl", url="https://evil-hallucination.example")),
        vote("GPT", rec("A", "Helen Keller International (HKI)", url="https://another-fake.example")),
    ]
    recs, _ = run_session.aggregate_recommendations(votes)
    assert pillar(recs, "A")["donation_url"] == "https://hki.example/donate"


def test_distinct_orgs_do_not_false_merge():
    votes = [
        vote("Opus", rec("A", "Helen Keller Intl")),
        vote("GPT", rec("A", "Against Malaria Foundation")),
        vote("Gemini", rec("A", "Nuclear Threat Initiative (NTI)")),
    ]
    recs, unresolved = run_session.aggregate_recommendations(votes)
    a = pillar(recs, "A")
    assert a["has_consensus"] is False
    assert len(a["individual_votes"]) == 3
    assert not unresolved


def test_unknown_org_is_unresolved_not_silent():
    votes = [
        vote("Opus", rec("B", "Some Charity Nobody Curated")),
        vote("GPT", rec("B", "Against Malaria Foundation")),
    ]
    recs, unresolved = run_session.aggregate_recommendations(votes)
    assert len(unresolved) == 1
    assert unresolved[0]["organization"] == "Some Charity Nobody Curated"
    assert unresolved[0]["model"] == "Opus"
    # The resolved AMF vote is a single model -> no false consensus.
    assert pillar(recs, "B")["has_consensus"] is False


def test_german_keys_are_counted():
    votes = [
        vote("Opus", rec("A", "Helen Keller Intl"), key="empfehlungen"),
        vote("GPT", rec("A", "Helen Keller International (HKI)")),
    ]
    recs, _ = run_session.aggregate_recommendations(votes)
    a = pillar(recs, "A")
    assert a["has_consensus"] is True
    assert "Opus" in a["convergence"]["models"]


def test_same_model_twice_is_not_consensus():
    # One model listing the org twice must NOT fake a 2-model consensus.
    votes = [
        vote("Opus", rec("A", "Helen Keller Intl"), rec("A", "Helen Keller International (HKI)")),
    ]
    recs, _ = run_session.aggregate_recommendations(votes)
    assert pillar(recs, "A")["has_consensus"] is False
