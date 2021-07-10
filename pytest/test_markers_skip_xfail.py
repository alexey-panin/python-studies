import pytest
import sys


@pytest.mark.skip
def test_login():
    print("Login done")


@pytest.mark.skipif(sys.version_info < (3,9), reason="Python version is not supported")
def test_addProducts():
    print("Product added")

# flake8: noqa: S101
@pytest.mark.xfail
def test_logout():
    assert False
    print("Logout done")
