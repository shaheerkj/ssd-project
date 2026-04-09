from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # ── Security headers on every response ────────────────────────────────────
    @app.after_request
    def set_security_headers(response: Response) -> Response:
        # Clickjacking protection
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "frame-ancestors 'none';"          # blocks all framing
        )
        # Additional hardening
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response

    from app.routes.auth import auth_bp
    from app.routes.vault import vault_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)

    with app.app_context():
        db.create_all()

    return app
