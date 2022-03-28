from urllib import request

import pytest
from app.db.models import User
from app.db import db
from flask import g
from flask import session
import app

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
    response = client.post("/login", data=dict(email=username, password=password))
    assert message in response.data
    return client.post('/login', data=dict(email=username, password=password), follow_redirects=True)


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("test1", "test123", "test123", b"Invalid email address."),
     ("test2", "test123", "test123", b"Invalid email address.")),
)
def test_bad_username_email_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm))
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("j@j.com", "test123", "test1234", b"Passwords must match"),
     ("a@a.com", "a12345", "a123456", b"Passwords must match")),
)
def test_password_confirmation_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm))
    assert message in response.data
    # return client.post('/register', data=dict(email=username, password=password, confirm=confirm), follow_redirects=True)


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("j@j.com", "test", "test", b"Field must be between 6 and 35 characters long."),
     ("a@a.com", "a", "a", b"Field must be between 6 and 35 characters long.")),
)
def test_bad_password_criteria_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm))
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("test1@test1.com", "test123", "test123", b"User with that email already exists"),
     ("test2@test1.com", "test123", "test123", b"User with that email already exists")),
)
def test_already_registered(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm))
    response2 = client.post("/register", data=dict(email=username, password=password, confirm=confirm))
    assert message in response2.data

@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("j@j.com", "testvgfhgbh", b"Welcome"),
     ("j@j.com", "agvjhhgbghkk", b"Welcome")),
)
def test_successful_login(client, username, password, message):
    response = client.post("/login", data={"email": username, "password": password})
    assert response.status_code == 200
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("test1@test.com", "test123", "test123", b"Congratulations, you are now a registered user!"),
     ("test2@test.com", "a123456", "a123456", b"Congratulations, you are now a registered user!")),
)
def test_successful_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=password))
    # User.query.filter(User.email == username).delete()
    # db.session.commit()
    # assert message in response.data
    pass

def test_deny_dashboard_access_for_logged_users():
    pass


def test_dashboard_access_for_logged_users():
    pass
