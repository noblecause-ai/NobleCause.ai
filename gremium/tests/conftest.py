"""Explicit historical configuration for regression tests of the old weekly role."""
import json
from pathlib import Path

import pytest


@pytest.fixture
def legacy_weekly_configuration(tmp_path, monkeypatch):
    import run_wart
    cfg = json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
    cfg['features']['live_council']['enabled'] = False
    cfg['features']['three_scouts']['enabled'] = False
    here = tmp_path/'legacy-gremium'
    here.mkdir()
    (here/'config.json').write_text(json.dumps(cfg))
    monkeypatch.setattr(run_wart,'HERE',here)
