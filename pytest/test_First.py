# flake8: noqa: S101
def test_1():
    x = 10
    y = 20
    assert x != y


def test_2():
    name = "Selenium"
    title = "Selenium is for web automation"
    assert name in title


def test_3_jenkins():
    name = "Jenkins"
    title = "Jenkins is CI server"
    # "Title does not match will be printed if assertion fails"
    assert name in title, "Title does not match"
