# SecureVault

**SecureVault** is a self-hosted, Flask-based web password vault that lets users securely store and manage credentials for multiple sites. Every stored password is encrypted at rest with Fernet (AES-128-CBC + HMAC-SHA256), master passwords are hashed with bcrypt, and the application ships with layered security controls — CSRF protection, IDOR prevention, clickjacking headers, and a full CI/CD security pipeline (Bandit · CodeQL · OWASP ZAP · Safety).

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Development Workflow](#development-workflow)
7. [Security Considerations](#security-considerations)
8. [Docker](#docker)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [License](#license)
11. [Contributing](#contributing)

---

## Features

| Feature | Details |
|---|---|
| **Encrypted credential storage** | Vault entries are encrypted with Fernet (AES-128-CBC + HMAC-SHA256) before being written to the database |
| **bcrypt master passwords** | User master passwords are hashed with bcrypt (adaptive cost factor) — never stored in plaintext |
| **CSRF protection** | Every state-changing form includes a Flask-WTF CSRF token; session cookies use `SameSite=Strict` |
| **IDOR prevention** | All vault entry endpoints verify the requesting user owns the entry (`get_entry_or_403`) |
| **Clickjacking defence** | `X-Frame-Options: DENY` + `Content-Security-Policy: frame-ancestors 'none'` on every response |
| **Additional hardening** | `X-Content-Type-Options: nosniff`, `Referrer-Policy`, open-redirect guard on login `next` param |
| **Multi-user support** | Each user has an isolated set of vault entries; cross-user access is blocked at the application layer |
| **Docker-ready** | Multi-stage image, non-root user (`appuser`), read-only root filesystem |

---

## Prerequisites

- **Python 3.11+**
- **pip**
- *(Optional)* Docker & Docker Compose for containerised deployment

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/shaheerkj/secure-vault.git
cd secure-vault
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows PowerShell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in **all three** required values (see [Configuration](#configuration) below).

### 5. Run the application

```bash
python run.py
```

The app listens on `http://localhost:5000` by default.

> **First run:** SQLAlchemy automatically creates `data/vault.db` (SQLite) and the required tables on startup.

---

## Configuration

All sensitive settings are read from environment variables (loaded via `python-dotenv`). Copy `.env.example` to `.env` and set the values — **never commit `.env` to version control**.

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | **Yes** | Flask session signing key. Use a long, random string (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `VAULT_FERNET_KEY` | **Yes (production)** | Fernet symmetric key used to encrypt vault entries. Generate with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`. If omitted, a temporary key is generated per-process (development only — all stored entries become unreadable on restart) |
| `FLASK_ENV` | Recommended | Set to `production` to enable `Secure` flag on session cookies and other production hardening |
| `DATABASE_URL` | Optional | SQLAlchemy connection string. Defaults to `sqlite:///data/vault.db` relative to the project root |

### Generating keys

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# VAULT_FERNET_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Usage

### Register an account

Navigate to `http://localhost:5000/register`, choose a username, email, and a strong master password (minimum 8 characters).

### Add a vault entry

After logging in, click **Add Entry** on the dashboard and fill in the site name, URL, username, and password. The password is encrypted with Fernet before being saved.

### View / edit / delete entries

All entries are listed on the **Dashboard** (`/vault/`). Click **View** to reveal the decrypted password, **Edit** to update an entry, or **Delete** to permanently remove it. Delete operations require a form POST with a CSRF token — they cannot be triggered by a simple link or image load.

### Logout

Click **Logout** in the navigation to end your session.

---

## Development Workflow

### Run the test suite

```bash
pytest tests/ -v
```

### Run Bandit (SAST — static analysis)

```bash
bandit -r app/ -ll -ii
```

### Run Safety (dependency vulnerability scan)

```bash
safety check --full-report
```

### Project layout

```
secure-vault/
├── app/
│   ├── __init__.py          # App factory, security headers, extensions
│   ├── models.py            # User and VaultEntry SQLAlchemy models + encryption helpers
│   ├── routes/
│   │   ├── auth.py          # Register / login / logout blueprints + forms
│   │   └── vault.py         # CRUD vault entry blueprints + IDOR guard
│   ├── static/              # CSS / JS assets
│   └── templates/           # Jinja2 HTML templates
├── tests/
│   ├── test_auth.py         # Auth, session, security-header tests
│   └── test_vault.py        # Vault CRUD and IDOR tests
├── config.py                # Config and TestingConfig classes
├── run.py                   # Application entry point
├── Dockerfile               # Multi-stage Docker image
├── docker-compose.yml       # Compose stack with hardened container settings
├── requirements.txt
└── .env.example             # Environment variable template
```

---

## Security Considerations

> **This is a security-sensitive application. Please read these notes before deploying.**

1. **Set `SECRET_KEY` and `VAULT_FERNET_KEY` from a secrets manager or secure environment injection — never hard-code them or commit `.env` to git.** Loss of `VAULT_FERNET_KEY` means all stored vault entries become permanently unreadable.

2. **Run behind TLS in production.** Flask's built-in server is not suitable for production. Use a reverse proxy (e.g. Nginx or Caddy) with a valid TLS certificate so that session cookies are transmitted over HTTPS only. The `SESSION_COOKIE_SECURE` flag is automatically enabled when `FLASK_ENV=production`.

3. **Keep dependencies up to date.** The CI pipeline runs `safety check` on every push. If a vulnerability is reported, update the affected package in `requirements.txt` promptly.

4. **Database file access.** The SQLite database contains Fernet-encrypted passwords, but the encryption keys are separate. Ensure the database file and its parent directory are not accessible from the web root and are not world-readable on the host.

5. **Backup `VAULT_FERNET_KEY` securely.** Without the original key, there is no way to recover encrypted vault data.

6. **Audit log.** Currently, vault operations are not written to an audit log. For higher-security deployments, consider adding application-level logging of create/read/update/delete events (without logging plaintext passwords).

---

## Docker

### Build and run with Docker Compose (recommended)

```bash
# Copy and edit .env first
cp .env.example .env

docker compose up -d
```

The container runs as a non-root user (`appuser`, UID 1001), with a read-only root filesystem (only `/data` and `/tmp` are writable) and `no-new-privileges` security option.

### Build and run manually

```bash
docker build -t securevault .

docker run -d \
  --name securevault \
  -p 5000:5000 \
  -e SECRET_KEY=<your-secret-key> \
  -e VAULT_FERNET_KEY=<your-fernet-key> \
  -e FLASK_ENV=production \
  -v vault_data:/data \
  securevault
```

---

## CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/ci-cd.yml`) runs on every push and pull request:

| Job | Tool | Purpose |
|---|---|---|
| **Unit Tests** | pytest | Functional and security-header tests |
| **SAST — Bandit** | Bandit | Python static analysis, detects common security issues |
| **SAST — CodeQL** | CodeQL | Deep semantic code analysis by GitHub |
| **Dependency Scan** | Safety | Checks `requirements.txt` against known CVE database |
| **DAST — ZAP** | OWASP ZAP Baseline | Dynamic scan of the running app for web vulnerabilities |
| **Docker Build** | Docker | Validates the image builds and the container starts |

---

## License

This project does not currently include a `LICENSE` file. Please add one before public distribution. For open-source projects, [MIT](https://choosealicense.com/licenses/mit/) or [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) are common choices.

---

## Contributing

Contributions are welcome via the standard GitHub flow:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes with clear messages.
4. Open a pull request against `main` — the CI pipeline will run automatically.
5. Address any review feedback.

For security vulnerability reports, please open a private security advisory rather than a public issue.
