from src.models_db import User


def test_signup_creates_user_and_logs_in(client, app):
    response = client.post(
        "/signup",
        data={"name": "Alice", "email": "alice@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(email="alice@example.com").first() is not None


def test_signup_rejects_duplicate_email(client, make_user):
    make_user(email="bob@example.com")
    response = client.post(
        "/signup",
        data={"name": "Bob 2", "email": "bob@example.com", "password": "password123"},
    )
    assert b"already registered" in response.data


def test_login_with_correct_credentials_succeeds(client, make_user):
    make_user(email="carol@example.com", password="password123")
    response = client.post(
        "/login",
        data={"email": "carol@example.com", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid email or password" not in response.data


def test_login_with_wrong_password_shows_error(client, make_user):
    make_user(email="dave@example.com", password="password123")
    response = client.post(
        "/login",
        data={"email": "dave@example.com", "password": "wrong-password"},
    )
    assert b"Invalid email or password" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout_clears_session(client, make_user):
    make_user(email="erin@example.com", password="password123")
    client.post("/login", data={"email": "erin@example.com", "password": "password123"})
    client.get("/logout")
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
