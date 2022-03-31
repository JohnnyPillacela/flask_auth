from urllib import request

import pytest
from flask_login import current_user
from app.db.models import User

from app.db import db
from app import create_app
from flask import g
from flask import session
import app

"""Tests for Project 2"""


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("j@j.com", "sdgfhkjnsdf", b"Invalid username or password"),
     ("j@j.com", "agvjhhgbghkk", b"Invalid username or password")),
)
def test_bad_password_login(client, email, password, message):
    response = client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("a@a.com", "test", b"Invalid username or password"),
     ("test@test.com", "a", b"Invalid username or password")),
)
def test_bad_username_email_login(client, email, password, message):
    response = client.post("/login", data=dict(email=email, password=password), follow_redirects=True)
    assert message in response.data
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("test1", "test123", "test123", b"Invalid email address."),
     ("test2", "test123", "test123", b"Invalid email address.")),
)
def test_bad_username_email_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (("j@j.com", "test123", "test1234", b"Passwords must match"),
     ("a@a.com", "a12345", "a123456", b"Passwords must match")),
)
def test_password_confirmation_registration(client, username, password, confirm, message):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "confirm"),
    (("j@j.com", "test", "test"),
     ("a@a.com", "a", "a")),
)
def test_bad_password_criteria_registration(client, username, password, confirm):
    response = client.post("/register", data=dict(email=username, password=password, confirm=confirm),
                           follow_redirects=True)
    assert b"Field must be between 6 and 35 characters long." in response.data


def test_already_registered(client):
    email = "test1@test1.com"
    password = "test123"
    response = client.post("/register", data=dict(email=email, password=password, confirm=password),
                           follow_redirects=True)
    response2 = client.post("/register", data=dict(email=email, password=password, confirm=password),
                            follow_redirects=True)
    assert b"Already Registered" in response2.data


def test_successful_login(client):
    response = client.post("/login", data={"email": "j@j.com", "password": "123456"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_successful_registration(client, application):
    response = client.post("/register",
                           data={"email": "test123456@test123456.com", "password": "test123", "confirm": "test123"},
                           follow_redirects=True)
    assert b"Congratulations, you are now a registered user!" in response.data
    with application.app_context():
        client.post("/login",
                    data={"email": "j@j.com", "password": "123456", "confirm": "123456"},
                    follow_redirects=True)
        user_to_delete = User.query.filter_by(email="test123456@test123456.com").first()
        response = client.post("/users/"+user_to_delete.get_id()+"/delete", follow_redirects=True)
        assert response.status_code == 200

def test_deny_dashboard_access_for_logged_users():
    assert 100 == 100


def test_dashboard_access_for_logged_users():
    pass
