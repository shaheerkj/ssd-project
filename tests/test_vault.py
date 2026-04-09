import pytest
from app import create_app, db
from app.models import User, VaultEntry
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


def _register_and_login(client, username, email, password="password123"):
    client.post("/register", data={
        "username": username, "email": email,
        "password": password, "confirm": password,
    }, follow_redirects=True)
    client.post("/login", data={"username": username, "password": password},
                follow_redirects=True)


def _add_entry(client, site="GitHub", username="alice", password="secret"):
    return client.post("/vault/add", data={
        "site_name": site, "username": username,
        "password": password,
    }, follow_redirects=True)


# ── CRUD ──────────────────────────────────────────────────────────────────────

def test_add_entry(client, app):
    _register_and_login(client, "alice", "alice@example.com")
    rv = _add_entry(client)
    assert rv.status_code == 200
    with app.app_context():
        assert VaultEntry.query.count() == 1


def test_view_own_entry(client, app):
    _register_and_login(client, "alice", "alice@example.com")
    _add_entry(client)
    with app.app_context():
        entry = VaultEntry.query.first()
        entry_id = entry.id
    rv = client.get(f"/vault/view/{entry_id}")
    assert rv.status_code == 200
    assert b"GitHub" in rv.data


def test_delete_own_entry(client, app):
    _register_and_login(client, "alice", "alice@example.com")
    _add_entry(client)
    with app.app_context():
        entry_id = VaultEntry.query.first().id
    rv = client.post(f"/vault/delete/{entry_id}", follow_redirects=True)
    assert rv.status_code == 200
    with app.app_context():
        assert VaultEntry.query.count() == 0


# ── IDOR Tests ────────────────────────────────────────────────────────────────

def test_idor_view_blocked(client, app):
    """Bob must NOT be able to view Alice's vault entry."""
    _register_and_login(client, "alice", "alice@example.com")
    _add_entry(client)
    with app.app_context():
        entry_id = VaultEntry.query.first().id

    # Log out Alice, log in Bob
    client.get("/logout")
    _register_and_login(client, "bob", "bob@example.com")

    rv = client.get(f"/vault/view/{entry_id}")
    assert rv.status_code == 403   # ownership check enforced


def test_idor_edit_blocked(client, app):
    """Bob must NOT be able to edit Alice's vault entry."""
    _register_and_login(client, "alice", "alice@example.com")
    _add_entry(client)
    with app.app_context():
        entry_id = VaultEntry.query.first().id

    client.get("/logout")
    _register_and_login(client, "bob", "bob@example.com")

    rv = client.post(f"/vault/edit/{entry_id}", data={
        "site_name": "hacked", "username": "bob",
        "password": "pwned", "confirm": "pwned",
    }, follow_redirects=False)
    assert rv.status_code == 403


def test_idor_delete_blocked(client, app):
    """Bob must NOT be able to delete Alice's vault entry."""
    _register_and_login(client, "alice", "alice@example.com")
    _add_entry(client)
    with app.app_context():
        entry_id = VaultEntry.query.first().id

    client.get("/logout")
    _register_and_login(client, "bob", "bob@example.com")

    rv = client.post(f"/vault/delete/{entry_id}", follow_redirects=False)
    assert rv.status_code == 403
    # Alice's entry must still exist
    with app.app_context():
        assert VaultEntry.query.count() == 1


# ── Encryption ────────────────────────────────────────────────────────────────

def test_password_stored_encrypted(app):
    """Raw DB value must never equal the plaintext password."""
    with app.app_context():
        user = User(username="carol", email="carol@example.com")
        user.set_password("masterpass")
        db.session.add(user)
        db.session.commit()

        entry = VaultEntry(user_id=user.id, site_name="Test",
                           username="carol", notes=None)
        entry.set_password("mysecretpassword")
        db.session.add(entry)
        db.session.commit()

        stored = VaultEntry.query.first().encrypted_password
        assert stored != "mysecretpassword"
        assert entry.get_password() == "mysecretpassword"


# ── Unauthenticated access ────────────────────────────────────────────────────

def test_dashboard_requires_login(client):
    rv = client.get("/vault/", follow_redirects=False)
    assert rv.status_code == 302
    assert "/login" in rv.headers["Location"]
