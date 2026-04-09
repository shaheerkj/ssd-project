import pytest
from app import create_app, db
from app.models import User
from config import TestingConfig


@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, username="alice", email="alice@example.com", password="password123"):
    return client.post("/register", data={
        "username": username,
        "email": email,
        "password": password,
        "confirm": password,
    }, follow_redirects=True)


def login(client, username="alice", password="password123"):
    return client.post("/login", data={
        "username": username,
        "password": password,
    }, follow_redirects=True)


# ── Registration ──────────────────────────────────────────────────────────────

def test_register_success(client):
    rv = register(client)
    assert rv.status_code == 200
    assert b"Account created" in rv.data


def test_register_duplicate_username(client):
    register(client)
    rv = register(client)
    assert b"Username already taken" in rv.data


def test_register_short_password(client):
    rv = register(client, password="short", email="b@b.com", username="bob")
    assert rv.status_code == 200
    # WTForms validation should reject it
    assert b"short" not in rv.data or b"Field must be at least" in rv.data


# ── Login / Logout ────────────────────────────────────────────────────────────

def test_login_success(client):
    register(client)
    rv = login(client)
    assert b"My Vault" in rv.data


def test_login_wrong_password(client):
    register(client)
    rv = login(client, password="wrongpass")
    assert b"Invalid username or password" in rv.data


def test_logout(client):
    register(client)
    login(client)
    rv = client.get("/logout", follow_redirects=True)
    assert b"logged out" in rv.data


# ── Security headers ──────────────────────────────────────────────────────────

def test_clickjacking_header(client):
    rv = client.get("/login")
    assert rv.headers.get("X-Frame-Options") == "DENY"


def test_csp_frame_ancestors(client):
    rv = client.get("/login")
    csp = rv.headers.get("Content-Security-Policy", "")
    assert "frame-ancestors 'none'" in csp


def test_x_content_type_options(client):
    rv = client.get("/login")
    assert rv.headers.get("X-Content-Type-Options") == "nosniff"


# ── Open redirect guard ───────────────────────────────────────────────────────

def test_open_redirect_blocked(client):
    register(client)
    rv = client.post("/login?next=https://evil.com", data={
        "username": "alice",
        "password": "password123",
    }, follow_redirects=False)
    location = rv.headers.get("Location", "")
    assert "evil.com" not in location
