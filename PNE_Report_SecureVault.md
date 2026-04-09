# Protection Needs Elicitation (PNE) Report
**Project:** SecureVault — Password Vault
**Team:** SecureVault
**Course:** CYC386 — Secure Software Design and Development
**Instructor:** Engr. Muhammad Ahmad Nawaz
**Date:** 2026-04-08

---

## Team Members

| Name                | Registration No. |
|---------------------|-----------------|
| Daniyal Ahmed       | SP23-BCT-011    |
| Shaheer Khalid      | SP23-BCT-048    |
| Maaz Malik          | SP23-BCT-025    |
| Rana Mutahhar Ahmed | SP23-BCT-045    |

---

## 1. System Overview

SecureVault is a web-based password vault that allows authenticated users to securely store, retrieve, and manage credentials for external services. The application is built on Flask (Python) with SQLite as the persistence layer and Fernet symmetric encryption for credential storage.

---

## 2. Assets Inventory

| ID  | Asset                          | Type              | Value     |
|-----|--------------------------------|-------------------|-----------|
| A1  | User master passwords (hashed) | Credential        | Critical  |
| A2  | Stored vault passwords         | Credential        | Critical  |
| A3  | Fernet encryption key          | Cryptographic key | Critical  |
| A4  | User account data (email, username) | PII          | High      |
| A5  | Session tokens (Flask cookies) | Authentication    | High      |
| A6  | SQLite database file           | Data store        | High      |
| A7  | Application source code        | Intellectual      | Medium    |
| A8  | CI/CD pipeline secrets         | Infrastructure    | High      |

---

## 3. Stakeholders & Roles

| Stakeholder      | Role                             | Security Interest                      |
|------------------|----------------------------------|----------------------------------------|
| End Users        | Vault owners                     | Confidentiality of stored credentials  |
| Application Admin| System operator                  | Integrity, availability                |
| Instructor       | Evaluator                        | Compliance, correctness of fixes       |
| Attacker (threat)| External/Internal adversary      | Credential theft, privilege escalation |

---

## 4. Protection Needs (Elicited Requirements)

### 4.1 Confidentiality

| ID   | Protection Need                                                   | Priority |
|------|-------------------------------------------------------------------|----------|
| PN-1 | Vault passwords must never be stored in plaintext (Fernet AES-128-CBC) | Critical |
| PN-2 | Master passwords must be hashed with bcrypt (cost factor ≥ 12)   | Critical |
| PN-3 | Users must only access their own vault entries (IDOR prevention)  | Critical |
| PN-4 | Session cookies must be HttpOnly, SameSite=Strict, Secure (prod) | High     |

### 4.2 Integrity

| ID   | Protection Need                                                   | Priority |
|------|-------------------------------------------------------------------|----------|
| PN-5 | All state-changing operations must include CSRF tokens            | Critical |
| PN-6 | DELETE and EDIT must use POST/PUT, never GET                      | High     |
| PN-7 | Input must be validated server-side (WTForms validators)          | High     |
| PN-8 | Open redirect must be prevented on login next parameter           | Medium   |

### 4.3 Availability

| ID   | Protection Need                                                   | Priority |
|------|-------------------------------------------------------------------|----------|
| PN-9 | Application must not crash on invalid input or missing entries (404/403 handling) | Medium |

### 4.4 Non-repudiation / Auditability

| ID    | Protection Need                                                   | Priority |
|-------|-------------------------------------------------------------------|----------|
| PN-10 | Vault entry creation/modification timestamps must be recorded     | Low      |

---

## 5. Security Constraints

- **SC-1:** Application must pass OWASP ZAP baseline scan with zero High findings.
- **SC-2:** CI/CD pipeline must fail on any critical SAST finding (Bandit HIGH severity).
- **SC-3:** Encryption key (`VAULT_FERNET_KEY`) must never be committed to Git.
- **SC-4:** `X-Frame-Options: DENY` and `frame-ancestors 'none'` must be present on all responses.

---

## 6. Mapping to OWASP Top 10

| OWASP Category         | Relevant PN IDs        | Mitigation in Code          |
|------------------------|------------------------|-----------------------------|
| A01 Broken Access Control (IDOR) | PN-3       | `get_entry_or_403()` ownership check |
| A03 Injection          | PN-7                   | SQLAlchemy ORM (parameterised), WTForms validation |
| A05 Security Misconfiguration | PN-4, SC-4      | Security headers middleware  |
| A07 Auth Failures      | PN-2, PN-4             | bcrypt, SameSite cookies     |
| A08 CSRF               | PN-5, PN-6             | Flask-WTF CSRF tokens        |
| Clickjacking (OWASP Test) | SC-4               | X-Frame-Options + CSP        |
