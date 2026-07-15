"""Test-Isolation für den Registry-Global.

`organizations._REGISTRY` ist ein prozessweiter, mutabler Modul-Global. Ohne Reset
leckt ein Test, der eine Fixture-Registry lädt (z. B. gremium/tests/test_aggregate.py),
seinen Zustand in nachfolgende Tests — die Golden-Aggregation löst dann gegen die
falsche Registry auf und ist reihenfolgeabhängig rot. Ein Golden-Test, der nur isoliert
grün ist, ist als Garantie wertlos.

Diese autouse-Fixture schnappt den Global vor jedem Test und stellt ihn danach wieder
her. Damit trägt kein Test Registry-Zustand an einen anderen weiter — repo-weit,
reihenfolge-unabhängig, für alle jetzigen und künftigen Tests.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent / "gremium"))

import organizations  # noqa: E402


@pytest.fixture(autouse=True)
def _isolate_registry():
    saved = organizations._REGISTRY
    try:
        yield
    finally:
        organizations._REGISTRY = saved
