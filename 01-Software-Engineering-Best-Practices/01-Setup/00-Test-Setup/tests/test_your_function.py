import pytest
from app.main import your_function


def test_something():
    """mandatory test"""
    assert your_function(1, 1) == 2


@pytest.mark.optional
def test_something_else_optional():
    """optional test, not checked by `make test`"""
    assert your_function(-1, 1) == 0
