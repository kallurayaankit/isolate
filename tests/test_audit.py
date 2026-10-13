"""A simple test to give CI something to run."""

from isolate import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_isolate_imports():
    from isolate.audit import audit
    from isolate.discover import discover
    from isolate.runner import run_one, run_suite
    assert callable(audit)
    assert callable(discover)
    assert callable(run_one)
    assert callable(run_suite)