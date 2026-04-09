# Security Test Report
**Project:** SecureVault — Password Vault
**Tools:** pytest, Bandit (SAST), CodeQL (SAST), OWASP ZAP (DAST), Safety
**Date:** 2026-04-08

---

## 1. Unit & Security Tests (pytest)

### Run Command
```bash
pytest tests/ -v
```

### Results

| Test                                    | Result | Description                              |
|-----------------------------------------|--------|------------------------------------------|
| test_register_success                   | PASS   | User registration works                  |
| test_register_duplicate_username        | PASS   | Duplicate usernames rejected             |
| test_login_success                      | PASS   | Valid credentials accepted               |
| test_login_wrong_password               | PASS   | Invalid credentials rejected             |
| test_logout                             | PASS   | Session cleared on logout                |
| test_clickjacking_header                | PASS   | X-Frame-Options: DENY present            |
| test_csp_frame_ancestors                | PASS   | frame-ancestors 'none' in CSP            |
| test_x_content_type_options             | PASS   | nosniff header present                   |
| test_open_redirect_blocked              | PASS   | Absolute URLs stripped from next param   |
| test_add_entry                          | PASS   | Vault entry creation works               |
| test_view_own_entry                     | PASS   | Owner can view their own entry           |
| test_delete_own_entry                   | PASS   | Owner can delete their own entry         |
| **test_idor_view_blocked**              | **PASS** | **HTTP 403 for cross-user view**       |
| **test_idor_edit_blocked**              | **PASS** | **HTTP 403 for cross-user edit**       |
| **test_idor_delete_blocked**            | **PASS** | **HTTP 403 for cross-user delete**     |
| test_password_stored_encrypted          | PASS   | DB value != plaintext; decrypt works     |
| test_dashboard_requires_login           | PASS   | Unauthenticated redirect to /login       |

**Total: 17 passed, 0 failed**

---

## 2. SAST — Bandit

### Run Command
```bash
bandit -r app/ -ll -ii -f json -o bandit-report.json
```

### Summary

| Severity | Count (Before Fix) | Count (After Fix) |
|----------|--------------------|-------------------|
| HIGH     | 0                  | 0                 |
| MEDIUM   | 0                  | 0                 |
| LOW      | 0                  | 0                 |

**No security issues detected by Bandit.**

Key checks passed:
- No hardcoded passwords (`B105`, `B106`, `B107`)
- No use of `eval()` or `exec()` (`B307`)
- No use of `subprocess` with shell=True (`B602`)
- No use of `pickle` (`B301`)
- SQL queries use ORM only, not string formatting (`B608`)

---

## 3. SAST — CodeQL

CodeQL GitHub Action runs on every push/PR via `.github/workflows/ci-cd.yml`.

Queries applied: `security-and-quality`

### Key Rules Checked

| Rule                          | Finding |
|-------------------------------|---------|
| SQL injection                 | None — SQLAlchemy ORM used |
| Path traversal                | None    |
| Stored XSS                    | None — Jinja2 auto-escapes |
| Open redirect                 | None — next param sanitised |
| Hardcoded credentials         | None    |

---

## 4. Dependency Scan — Safety

### Run Command
```bash
safety check -r requirements.txt --full-report
```

### Results
All dependencies checked against CVE database.
No known vulnerabilities found in pinned versions:
- Flask 3.0.3 — clean
- Flask-WTF 1.2.1 — clean
- bcrypt 4.1.3 — clean
- cryptography 42.0.8 — clean

---

## 5. DAST — OWASP ZAP Baseline Scan

### Target
`http://localhost:5000` (Flask dev server started in CI/CD pipeline)

### Run Method
GitHub Actions: `zaproxy/action-baseline@v0.12.0`

### Alert Summary (After Fixes)

| Risk     | Alert                          | Status   | Evidence                          |
|----------|--------------------------------|----------|-----------------------------------|
| High     | Clickjacking (missing X-Frame-Options) | **Fixed** | X-Frame-Options: DENY header set |
| High     | Content-Security-Policy missing | **Fixed** | CSP with frame-ancestors 'none'  |
| Medium   | CSRF token missing             | **Fixed** | Flask-WTF CSRF on all POST forms |
| Medium   | X-Content-Type-Options missing | **Fixed** | nosniff header set                |
| Low      | Referrer-Policy missing        | **Fixed** | strict-origin-when-cross-origin   |

**0 High-risk alerts remaining after fixes.**

---

## 6. Before / After Comparison

| Vulnerability | Before                     | After                              |
|---------------|----------------------------|------------------------------------|
| IDOR          | Any user can access any entry by ID | HTTP 403 for unauthorized access |
| CSRF          | No tokens — any site can forge requests | All POSTs require valid CSRF token |
| Clickjacking  | No headers — app can be iframed | DENY + frame-ancestors 'none' on every response |
| Password storage | (assumed plaintext) | Fernet AES-128-CBC encryption |
| Master password | (assumed plaintext) | bcrypt with gensalt() |
