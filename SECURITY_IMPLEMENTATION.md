# Security Implementation Report
**Project:** SecureVault — Password Vault
**Vulnerabilities Fixed:** IDOR, CSRF, Clickjacking
**Date:** 2026-04-08

---

## 1. IDOR (Insecure Direct Object Reference) Fix

### Vulnerability Description
Without an ownership check, any authenticated user can access any vault entry by
guessing or enumerating the integer entry ID in the URL:
```
GET /vault/view/1   ← attacker accesses victim's entry
GET /vault/edit/1   ← attacker modifies victim's entry
POST /vault/delete/1 ← attacker deletes victim's entry
```

### Vulnerable Code (Before)
```python
# VULNERABLE — no ownership check
@vault_bp.route("/view/<int:entry_id>")
@login_required
def view_entry(entry_id):
    entry = VaultEntry.query.get(entry_id)   # any user can access any ID
    return render_template("view_entry.html", entry=entry)
```

### Fixed Code (After) — `app/routes/vault.py`
```python
def get_entry_or_403(entry_id: int) -> VaultEntry:
    """IDOR Fix: verify entry belongs to the current user before returning it."""
    entry = db.session.get(VaultEntry, entry_id)
    if entry is None:
        abort(404)
    if entry.user_id != current_user.id:   # <-- ownership check
        abort(403)
    return entry

@vault_bp.route("/view/<int:entry_id>")
@login_required
def view_entry(entry_id: int):
    entry = get_entry_or_403(entry_id)   # enforced on every operation
    ...
```

### Test Evidence
```
tests/test_vault.py::test_idor_view_blocked   PASSED  (HTTP 403)
tests/test_vault.py::test_idor_edit_blocked   PASSED  (HTTP 403)
tests/test_vault.py::test_idor_delete_blocked PASSED  (HTTP 403)
```

---

## 2. CSRF (Cross-Site Request Forgery) Fix

### Vulnerability Description
Without CSRF tokens, an attacker can host a malicious page that silently submits
a POST form to delete or modify the authenticated victim's vault entries.

### Vulnerable Code (Before)
```html
<!-- VULNERABLE — no CSRF token, state change via GET link -->
<a href="/vault/delete/1">Delete</a>
```

### Fixed Code (After)

**Backend — `app/__init__.py`:**
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
csrf.init_app(app)   # validates csrf_token on every POST/PUT/DELETE
```

**Backend — `config.py`:**
```python
WTF_CSRF_ENABLED = True
SESSION_COOKIE_SAMESITE = "Strict"   # prevents cross-site cookie sending
SESSION_COOKIE_HTTPONLY = True
```

**Frontend — all forms include the token (`app/templates/`):**
```html
<!-- Every form includes the hidden CSRF token field -->
<form method="POST">
  {{ form.hidden_tag() }}   {# generates <input type="hidden" name="csrf_token" ...> #}
  ...
</form>

<!-- Inline delete form uses csrf_token() Jinja global -->
<form method="POST" action="/vault/delete/1">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
  <button type="submit">Delete</button>
</form>
```

**DELETE uses POST only — never GET:**
```python
@vault_bp.route("/delete/<int:entry_id>", methods=["POST"])  # GET not allowed
```

---

## 3. Clickjacking Fix

### Vulnerability Description
Without frame-busting headers, an attacker can embed SecureVault in a transparent
`<iframe>` on a malicious page and trick the user into clicking vault buttons
while thinking they are clicking on the attacker's UI.

### Vulnerable Code (Before)
No headers set — browsers allow any site to iframe the application.

### Fixed Code (After) — `app/__init__.py`

```python
@app.after_request
def set_security_headers(response: Response) -> Response:
    # Primary clickjacking defense — legacy browsers
    response.headers["X-Frame-Options"] = "DENY"

    # Modern clickjacking defense — CSP frame-ancestors
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "frame-ancestors 'none';"   # <-- blocks ALL framing
    )
    # Additional hardening
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

### Test Evidence
```
tests/test_auth.py::test_clickjacking_header    PASSED  (X-Frame-Options: DENY)
tests/test_auth.py::test_csp_frame_ancestors    PASSED  (frame-ancestors 'none')
tests/test_auth.py::test_x_content_type_options PASSED  (nosniff)
```

---

## 4. Additional Security Controls

| Control                  | Implementation                                    |
|--------------------------|---------------------------------------------------|
| Password hashing         | `bcrypt.hashpw()` with `gensalt()` (cost ≥ 12)   |
| Credential encryption    | Fernet (AES-128-CBC + HMAC-SHA256)                |
| Open redirect prevention | `next` param validated — relative paths only      |
| SQL injection prevention | SQLAlchemy ORM (parameterised queries only)       |
| Input validation         | WTForms validators on all user-supplied fields    |
| Secrets management       | `.env` file, never committed (`.gitignore`)       |
