import pytest
from flask import g
from flask import session

"""Tests for Project 2"""


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("j@j.com", "testvgfhgbh", b"Invalid username or password"),
     ("j@j.com", "agvjhhgbghkk", b"Invalid username or password")),
)
def test_bad_password_login(client, username, password, message):
    response = client.post("/login", data={"email": username, "password": password})
    assert response.status_code == 200
    assert message in response.data

@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a@a.com", "test", b"Invalid username or password"),
     ("test@test.com", "a", b"Invalid username or password")),
)
def test_bad_username_email_login(client, username, password, message):
    response = client.post("/login", data=dict(email=username,password=password))
    assert message in response.data
    return client.post('/login', data=dict(email=username, password=password), follow_redirects=True)

@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("test@test.com", "test", b"Already Registered"),
     ("a@a.com", "a", b"Already Registered")),
)
def test_bad_username_email_registration(client, username, password, message):
    response = client.post("/register", data=dict(email=username,password=password))
    assert message in response.data
    return client.post('/register', data=dict(email=username, password=password), follow_redirects=True)

@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("test@test.com", "test", b"Already Registered"),
     ("a@a.com", "a", b"Already Registered")),
)
def test_password_confirmation_registration(client, username, password, message):
    response = client.post("/register", data=dict(email=username,password=password))
    assert message in response.data
    return client.post('/register', data=dict(email=username, password=password), follow_redirects=True)


def test_bad_password_criteria_registration():
    pass


def test_already_registered():
    pass


def test_successful_login():
    pass


def test_successful_registration():
    pass


def test_deny_dashboard_access_for_logged_users():
    pass


def test_dashboard_access_for_logged_users():
    pass
