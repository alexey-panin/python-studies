import pytest

"""
Typical workflow of running a test:

    Precondition:
        Setup, Connection, API

    Test

    Test

    Assertion

    Postcondition:
        Clean, close connection, close conn to db


So before running each test, I want to make sure precondits
and postcondits are on place

"""


@pytest.fixture
def setup():
    print("Start browser")
    yield
    # postconditions should run after a yield statement
    print("Close browser")


def test_1(setup):
    # pass a fixture function just as a parameter
    print("Test 1 executed")


def test_2(setup):
    print("Test 2 executed")


def test_3(setup):
    print("Test 3 executed")
