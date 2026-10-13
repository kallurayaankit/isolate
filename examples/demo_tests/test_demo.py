
"""Demo tests. One of these is deliberately order-dependent."""

_DB = {"users": []}


def test_00_isolated_pass():
    assert 1 + 1 == 2


def test_01_isolated_pass_too():
    assert 2 * 2 == 4


def test_02_creates_user():
    _DB["users"].append({"email": "alice@example.com"})
    assert len(_DB["users"]) == 1


def test_03_needs_user():
    assert len(_DB["users"]) > 0, "no users - test_02 must run first"


def test_04_another_pass():
    assert "hello".upper() == "HELLO"
