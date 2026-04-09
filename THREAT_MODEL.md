# Threat Model — SecureVault Password Vault
**Project:** SecureVault
**Method:** STRIDE + DFD + Attack Tree + CVSS v3.1
**Date:** 2026-04-08

---

## 1. Data Flow Diagram (DFD) — Level 0

```
 [Browser / User]
       |
       | HTTPS (TLS)
       v
 +------------------+
 |   Flask App      |  <-- Trust Boundary: Internet / App Server
 |  (Web Server)    |
 +------------------+
       |
       | SQLAlchemy ORM (parameterised)
       v
 +------------------+
 |  SQLite Database |  <-- Trust Boundary: App Server / DB
 |  (vault.db)      |
 +------------------+
```

## 2. DFD Level 1 — Key Processes

```
[User] ---(Register / Login)---> [Auth Module] ---(bcrypt verify)---> [DB: users]
[User] ---(Add/Edit/Delete Entry)---> [Vault Module] ---(ownership check)---> [DB: vault_entries]
[User] ---(View Entry)---> [Vault Module] ---(Fernet decrypt)---> [plaintext password]
[CI/CD] ---(push)---> [GitHub Actions] ---(Bandit/CodeQL/ZAP/Safety)--->  [Reports]
```

---

## 3. STRIDE Threat Table

| ID  | Component         | Threat Category      | Threat Description                                        | Mitigation                                           | Status   |
|-----|-------------------|----------------------|-----------------------------------------------------------|------------------------------------------------------|----------|
| T1  | Auth — Login      | **S**poofing         | Attacker brute-forces weak master password                | bcrypt (cost 12), strong password requirement (≥8 chars) | Mitigated |
| T2  | Vault — View/Edit | **T**ampering        | Attacker modifies another user's vault entry via IDOR     | `get_entry_or_403()` — user_id ownership check       | Mitigated |
| T3  | Session Cookie    | **R**epudiation      | User denies actions; no audit log                         | Timestamps on vault entries; future: audit log       | Partial  |
| T4  | DB — vault.db     | **I**nformation Disclosure | DB file read exposes encrypted passwords          | Fernet encryption; DB should be outside web root     | Mitigated |
| T5  | Any POST Form     | **E**levation of Privilege | CSRF attack triggers state change on behalf of victim | Flask-WTF CSRF tokens + SameSite=Strict cookies     | Mitigated |
| T6  | Browser / IFrame  | **E**levation of Privilege | Clickjacking — malicious site embeds vault in iframe | X-Frame-Options: DENY + CSP frame-ancestors 'none'  | Mitigated |
| T7  | Encryption Key    | **I**nformation Disclosure | Fernet key committed to Git exposes all passwords   | Key in `.env`, `.gitignore` enforced                 | Mitigated |
| T8  | Login Redirect    | **S**poofing         | Open redirect sends user to attacker-controlled URL       | next-param validation: only relative paths allowed   | Mitigated |
| T9  | Dependencies      | **T**ampering        | Vulnerable library (supply chain)                         | `safety check` in CI/CD pipeline                    | Mitigated |
| T10 | Source Code       | **I**nformation Disclosure | SAST finds hardcoded secrets                        | Bandit + CodeQL in pipeline; no hardcoded secrets    | Mitigated |

---

## 4. Attack Tree — IDOR Attack

```
Goal: Access another user's vault entry
├── [A] Guess/enumerate entry ID in GET /vault/view/<id>
│   └── Countermeasure: ownership check → HTTP 403
├── [B] Modify entry via POST /vault/edit/<id>
│   └── Countermeasure: ownership check → HTTP 403
└── [C] Delete entry via POST /vault/delete/<id>
    └── Countermeasure: ownership check → HTTP 403
```

## 5. Attack Tree — CSRF Attack

```
Goal: Perform unauthorized action as victim
├── [A] Trick victim into clicking crafted GET delete link
│   └── Countermeasure: delete uses POST only
├── [B] Embed hidden form on attacker site, auto-submit POST
│   └── Countermeasure: CSRF token required (Flask-WTF) → 400 Bad Request
└── [C] Same-site subdomain cookie theft
    └── Countermeasure: SameSite=Strict cookie attribute
```

---

## 6. CVSS v3.1 Risk Assessment Table

| ID  | Threat | AV | AC | PR | UI | S | C | I | A | Base Score | Severity |
|-----|--------|----|----|----|----|---|---|---|---|------------|----------|
| T2  | IDOR   | N  | L  | L  | N  | U | H | H | N | **8.1**    | High     |
| T5  | CSRF   | N  | L  | N  | R  | U | N | H | N | **6.5**    | Medium   |
| T6  | Clickjacking | N | L | N | R | U | L | H | N | **6.1** | Medium |
| T1  | Brute-force | N | H | N | N | U | H | N | N | **5.9**  | Medium   |
| T4  | DB Disclosure | L | L | H | N | U | H | N | N | **4.4** | Medium   |
| T7  | Key in Git | N | L | N | N | U | H | N | N | **7.5** | High     |

**CVSS Vector key:** AV=Attack Vector, AC=Attack Complexity, PR=Privileges Required,
UI=User Interaction, S=Scope, C=Confidentiality, I=Integrity, A=Availability
(N=Network/None, L=Low, H=High, R=Required, U=Unchanged)
