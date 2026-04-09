from datetime import datetime, timezone
from flask_login import UserMixin
from cryptography.fernet import Fernet
from flask import current_app
import bcrypt
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    vault_entries = db.relationship("VaultEntry", backref="owner", lazy=True,
                                    cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Hash and store the master password using bcrypt."""
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class VaultEntry(db.Model):
    __tablename__ = "vault_entries"

    id = db.Column(db.Integer, primary_key=True)
    # IDOR fix: every entry is explicitly tied to its owner
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    site_name = db.Column(db.String(200), nullable=False)
    site_url = db.Column(db.String(500), nullable=True)
    username = db.Column(db.String(200), nullable=False)
    # Stored encrypted with Fernet; never stored in plaintext
    encrypted_password = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # ── Encryption helpers ────────────────────────────────────────────────────

    @staticmethod
    def _get_fernet() -> Fernet:
        """Return a Fernet instance.  Key is read from app config or auto-generated
        (auto-generation is only safe for development/testing)."""
        key = current_app.config.get("VAULT_FERNET_KEY")
        if not key:
            # Dev fallback — generate a stable per-process key stored in app config
            key = Fernet.generate_key().decode()
            current_app.config["VAULT_FERNET_KEY"] = key
        if isinstance(key, str):
            key = key.encode()
        return Fernet(key)

    def set_password(self, plaintext: str) -> None:
        f = self._get_fernet()
        self.encrypted_password = f.encrypt(plaintext.encode()).decode()

    def get_password(self) -> str:
        f = self._get_fernet()
        return f.decrypt(self.encrypted_password.encode()).decode()

    def __repr__(self) -> str:
        return f"<VaultEntry {self.site_name} (user={self.user_id})>"


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))
