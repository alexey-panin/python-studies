import pytest


@pytest.mark.parametrize("username, password", [
    ("Selenium", "WebDriver"),
    ("Python", "Pytest"),
    ("Mukesh", "Otwani")
])
# argnames must match the names of params what function expects
def test_login(username, password):
    print(username)
    print(password)
