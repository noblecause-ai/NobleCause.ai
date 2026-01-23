"""Pytest configuration and hooks for better test output."""

import pytest


def pytest_collection_modifyitems(config, items):
    """Modify test items to add better skip reason display."""
    pass


def pytest_runtest_setup(item):
    """Hook to show skip reasons more clearly."""
    # Check if test has live marker
    if item.get_closest_marker("live"):
        # Verify API key is available
        import os
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            # Try loading from .env
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.getenv('OPENROUTER_API_KEY')
            except:
                pass
        
        if not api_key:
            pytest.skip(
                "SKIP REASON: OPENROUTER_API_KEY not set. "
                "Set it with: export OPENROUTER_API_KEY='your-key' "
                "or add it to backend/.env file"
            )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Make skip reasons more visible in output."""
    if call.when == "setup" and call.excinfo is not None:
        if isinstance(call.excinfo.value, pytest.skip.Exception):
            # Print skip reason prominently
            print(f"\n{'='*70}")
            print(f"SKIPPED: {item.name}")
            print(f"REASON: {call.excinfo.value.msg}")
            print(f"{'='*70}\n")
