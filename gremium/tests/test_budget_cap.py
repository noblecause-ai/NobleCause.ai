import sys
from pathlib import Path

import pytest


GREMIUM = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GREMIUM))

from run_session import check_budget  # noqa: E402


def test_budget_at_cap_is_allowed(capsys):
    check_budget({"total": 1.25}, 1.25, "nach Runde 1")
    assert "1.25 €" in capsys.readouterr().out


def test_budget_over_cap_aborts_before_further_calls():
    with pytest.raises(SystemExit, match="Kein weiterer Modellaufruf"):
        check_budget({"total": 1.26}, 1.25, "nach Runde 1")


def test_budget_uses_unrounded_model_costs():
    with pytest.raises(SystemExit, match="Budgetdeckel"):
        check_budget({"total": 1.25, "by_model": [{"eur": 1.254}]}, 1.25, "nach Erstvotum")


@pytest.mark.parametrize("cap", [-1, float("nan"), float("inf")])
def test_invalid_budget_cap_cannot_bypass_guard(cap):
    with pytest.raises(ValueError, match="endlich und nicht negativ"):
        check_budget({"total": 0}, cap, "vor Lauf")
