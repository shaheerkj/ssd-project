const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "SecureVault — Password Vault";
pres.author = "SecureVault Team";

// Color palette
const BG      = "1a1d2e";   // dark navy
const WHITE   = "FFFFFF";
const BLUE    = "3182ce";   // main accent
const LBLUE   = "63b3ed";   // light blue
const MBLUE   = "2563eb";   // medium blue for table headers
const DBLUE   = "1e3a5f";   // darker blue for panels
const GREEN   = "38a169";   // green for pass/success
const RED     = "e53e3e";   // red for HIGH severity
const YELLOW  = "d69e2e";   // yellow for MEDIUM severity
const GRAY    = "4a5568";   // subtle gray
const CODEBG  = "0d1117";   // code block bg

// Slide dimensions: 10" x 5.625"
const SW = 10;
const SH = 5.625;

// ─── HELPERS ────────────────────────────────────────────────────────────────

function addBg(slide) {
  slide.background = { color: BG };
}

/** Left accent bar at top-left of title box */
function addTitleBar(slide, title, y = 0.32, accentColor = BLUE) {
  // Blue accent bar left of title
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: y, w: 0.07, h: 0.55,
    fill: { color: accentColor }, line: { color: accentColor }
  });
  slide.addText(title, {
    x: 0.55, y: y, w: 9.1, h: 0.55,
    fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle",
    margin: 0
  });
}

function addFooter(slide, label) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.35, w: SW, h: 0.275,
    fill: { color: DBLUE }, line: { color: DBLUE }
  });
  slide.addText("SecureVault  |  CYC386 — Secure Software Design & Development  |  COMSATS University Islamabad  |  " + label, {
    x: 0.3, y: 5.35, w: 9.4, h: 0.275,
    fontSize: 8, color: LBLUE, fontFace: "Calibri", valign: "middle", align: "center", margin: 0
  });
}

// ─── SLIDE 1 — TITLE ────────────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);

  // Top accent stripe
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: SW, h: 0.08,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  // Large decorative circle behind title area (subtle)
  slide.addShape(pres.shapes.OVAL, {
    x: 6.5, y: -1.5, w: 5.5, h: 5.5,
    fill: { color: MBLUE, transparency: 88 }, line: { color: MBLUE, transparency: 88 }
  });
  slide.addShape(pres.shapes.OVAL, {
    x: -1.5, y: 2.5, w: 4, h: 4,
    fill: { color: BLUE, transparency: 90 }, line: { color: BLUE, transparency: 90 }
  });

  // Shield icon (text-based) — large "🔒" approximated as a bold symbol
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 0.85, w: 1.1, h: 1.1,
    fill: { color: BLUE }, line: { color: LBLUE, width: 1.5 }
  });
  slide.addText("SV", {
    x: 0.5, y: 0.85, w: 1.1, h: 1.1,
    fontSize: 28, bold: true, color: WHITE, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });

  // Main Title
  slide.addText("SecureVault — Password Vault", {
    x: 0.4, y: 1.95, w: 9.2, h: 0.85,
    fontSize: 40, bold: true, color: WHITE, fontFace: "Calibri",
    align: "left", valign: "middle", margin: 0
  });

  // Blue accent line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 2.85, w: 9.2, h: 0.04,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  // Subtitle
  slide.addText("48-Hour DevSecOps Security Sprint", {
    x: 0.4, y: 2.95, w: 9.2, h: 0.5,
    fontSize: 22, color: LBLUE, fontFace: "Calibri", italic: true, margin: 0
  });

  // Course
  slide.addText("CYC386  |  Spring 2026  |  COMSATS University Islamabad", {
    x: 0.4, y: 3.52, w: 9.2, h: 0.32,
    fontSize: 13, color: WHITE, fontFace: "Calibri", margin: 0
  });

  // Team
  slide.addText("Daniyal Ahmed (SP23-BCT-011)  |  Shaheer Khalid (SP23-BCT-048)  |  Maaz Malik (SP23-BCT-025)  |  Rana Mutahhar Ahmed (SP23-BCT-045)", {
    x: 0.4, y: 3.88, w: 9.2, h: 0.32,
    fontSize: 11, color: LBLUE, fontFace: "Calibri", margin: 0
  });

  // Instructor & Date
  slide.addText("Instructor: Engr. Muhammad Ahmad Nawaz  |  April 8, 2026", {
    x: 0.4, y: 4.22, w: 9.2, h: 0.32,
    fontSize: 12, color: WHITE, fontFace: "Calibri", margin: 0
  });

  // Bottom bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.35, w: SW, h: 0.275,
    fill: { color: DBLUE }, line: { color: DBLUE }
  });
  slide.addText("CYC386 — Secure Software Design and Development  |  Spring 2026", {
    x: 0.3, y: 5.35, w: 9.4, h: 0.275,
    fontSize: 8, color: LBLUE, fontFace: "Calibri", valign: "middle", align: "center", margin: 0
  });
}

// ─── SLIDE 2 — PROJECT OVERVIEW ─────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Project Overview");
  addFooter(slide, "Slide 2 of 12");

  // Accent bar under title
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  const bullets = [
    "Password Vault application built with Flask + SQLite",
    "Secured against OWASP Top 10 critical vulnerabilities",
    "Full DevSecOps pipeline: GitHub Actions CI/CD",
    "Tools: bcrypt, Fernet encryption, Flask-WTF, SQLAlchemy",
    "Theme: Password Vault (Passky-inspired)",
    "Sprint Duration: 48 hours  |  Team Size: 4 members",
  ];

  const icons = ["01", "02", "03", "04", "05", "06"];
  const startY = 1.1;
  const rowH = 0.63;

  bullets.forEach((b, i) => {
    const y = startY + i * rowH;
    // Numbered circle
    slide.addShape(pres.shapes.OVAL, {
      x: 0.4, y: y + 0.05, w: 0.38, h: 0.38,
      fill: { color: BLUE }, line: { color: BLUE }
    });
    slide.addText(String(i + 1), {
      x: 0.4, y: y + 0.05, w: 0.38, h: 0.38,
      fontSize: 12, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    // Text
    slide.addText(b, {
      x: 0.9, y: y, w: 8.7, h: 0.48,
      fontSize: 16, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
  });
}

// ─── SLIDE 3 — PNE ──────────────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Protection Needs Elicitation (PNE)");
  addFooter(slide, "Slide 3 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  // Left panel
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.05, w: 4.35, h: 4.1,
    fill: { color: DBLUE }, line: { color: BLUE, width: 1 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.05, w: 4.35, h: 0.42,
    fill: { color: BLUE }, line: { color: BLUE }
  });
  slide.addText("8 Critical Assets Identified", {
    x: 0.4, y: 1.05, w: 4.35, h: 0.42,
    fontSize: 13, bold: true, color: WHITE, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });

  const assets = [
    { label: "A1", desc: "User master passwords", sev: "Critical", col: RED },
    { label: "A2", desc: "Stored vault passwords", sev: "Critical", col: RED },
    { label: "A3", desc: "Fernet encryption key", sev: "Critical", col: RED },
    { label: "A4", desc: "User PII — email, username", sev: "High", col: YELLOW },
    { label: "A5", desc: "Session tokens", sev: "High", col: YELLOW },
  ];

  assets.forEach((a, i) => {
    const y = 1.57 + i * 0.63;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: y, w: 0.38, h: 0.28,
      fill: { color: a.col }, line: { color: a.col }
    });
    slide.addText(a.label, {
      x: 0.5, y: y, w: 0.38, h: 0.28,
      fontSize: 10, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(a.desc, {
      x: 0.95, y: y, w: 2.5, h: 0.28,
      fontSize: 12, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText(a.sev, {
      x: 3.5, y: y, w: 1.0, h: 0.28,
      fontSize: 10, bold: true, color: a.col, fontFace: "Calibri",
      align: "right", valign: "middle", margin: 0
    });
  });

  // Right panel
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.9, y: 1.05, w: 4.7, h: 4.1,
    fill: { color: DBLUE }, line: { color: BLUE, width: 1 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 4.9, y: 1.05, w: 4.7, h: 0.42,
    fill: { color: MBLUE }, line: { color: MBLUE }
  });
  slide.addText("10 Protection Needs", {
    x: 4.9, y: 1.05, w: 4.7, h: 0.42,
    fontSize: 13, bold: true, color: WHITE, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });

  const pns = [
    "PN-1: Vault passwords never stored in plaintext",
    "PN-2: Master passwords hashed with bcrypt",
    "PN-3: Users access only their own entries (IDOR)",
    "PN-5: All state changes require CSRF tokens",
    "PN-4: Session cookies — HttpOnly, SameSite=Strict",
  ];

  pns.forEach((p, i) => {
    const y = 1.57 + i * 0.63;
    slide.addShape(pres.shapes.OVAL, {
      x: 5.0, y: y + 0.04, w: 0.22, h: 0.22,
      fill: { color: LBLUE }, line: { color: LBLUE }
    });
    slide.addText(p, {
      x: 5.3, y: y, w: 4.15, h: 0.3,
      fontSize: 12, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
  });
}

// ─── SLIDE 4 — STRIDE ───────────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "STRIDE Threat Modeling");
  addFooter(slide, "Slide 4 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  const headers = ["STRIDE Category", "Attack Vector", "Our Mitigation"];
  const colW = [2.8, 3.2, 3.2];
  const colX = [0.4, 3.2, 6.4];

  // Header row
  headers.forEach((h, i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: colX[i], y: 1.05, w: colW[i] - 0.05, h: 0.42,
      fill: { color: BLUE }, line: { color: BLUE }
    });
    slide.addText(h, {
      x: colX[i], y: 1.05, w: colW[i] - 0.05, h: 0.42,
      fontSize: 12, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
  });

  const rows = [
    ["Spoofing", "Brute-force login", "bcrypt (cost 12)"],
    ["Tampering", "IDOR entry access", "Ownership check (403)"],
    ["Repudiation", "No audit trail", "Timestamps recorded"],
    ["Info Disclosure", "DB exposure", "Fernet AES-128-CBC encryption"],
    ["Elev. of Privilege", "CSRF attack", "Flask-WTF CSRF tokens"],
    ["Elev. of Privilege", "Clickjacking", "X-Frame-Options DENY + CSP"],
  ];

  const rowColors = [DBLUE, "1e2742", DBLUE, "1e2742", DBLUE, "1e2742"];

  rows.forEach((row, ri) => {
    const y = 1.52 + ri * 0.62;
    colX.forEach((cx, ci) => {
      slide.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: y, w: colW[ci] - 0.05, h: 0.55,
        fill: { color: rowColors[ri] }, line: { color: GRAY, width: 0.5 }
      });
      slide.addText(row[ci], {
        x: cx + 0.08, y: y, w: colW[ci] - 0.18, h: 0.55,
        fontSize: ci === 0 ? 12 : 11,
        bold: ci === 0,
        color: ci === 0 ? LBLUE : WHITE,
        fontFace: "Calibri", valign: "middle", margin: 0
      });
    });
  });
}

// ─── SLIDE 5 — CVSS ─────────────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "CVSS v3.1 Risk Assessment");
  addFooter(slide, "Slide 5 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  // Risk scale legend
  slide.addText("Risk Scale:", {
    x: 0.4, y: 1.02, w: 1.2, h: 0.3,
    fontSize: 10, color: LBLUE, fontFace: "Calibri", bold: true, margin: 0
  });
  [["HIGH", RED], ["MEDIUM", YELLOW], ["LOW", GREEN]].forEach(([label, col], i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 1.65 + i * 1.4, y: 1.08, w: 0.9, h: 0.22,
      fill: { color: col }, line: { color: col }
    });
    slide.addText(label, {
      x: 1.65 + i * 1.4, y: 1.08, w: 0.9, h: 0.22,
      fontSize: 9, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
  });

  const colX = [0.4, 4.2, 6.7];
  const colW = [3.75, 2.4, 2.7];
  const headers = ["Threat", "CVSS Score", "Severity"];

  // Header
  headers.forEach((h, i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: colX[i], y: 1.42, w: colW[i] - 0.05, h: 0.42,
      fill: { color: BLUE }, line: { color: BLUE }
    });
    slide.addText(h, {
      x: colX[i], y: 1.42, w: colW[i] - 0.05, h: 0.42,
      fontSize: 13, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
  });

  const data = [
    ["IDOR (T2)", "8.1", "HIGH", RED],
    ["Key in Git (T7)", "7.5", "HIGH", RED],
    ["CSRF (T5)", "6.5", "MEDIUM", YELLOW],
    ["Clickjacking (T6)", "6.1", "MEDIUM", YELLOW],
    ["Brute-force (T1)", "5.9", "MEDIUM", YELLOW],
    ["DB Disclosure (T4)", "4.4", "MEDIUM", YELLOW],
  ];
  const rowBg = [DBLUE, "1e2742"];

  data.forEach((row, ri) => {
    const y = 1.89 + ri * 0.57;
    const bg = rowBg[ri % 2];

    // Threat column
    slide.addShape(pres.shapes.RECTANGLE, {
      x: colX[0], y: y, w: colW[0] - 0.05, h: 0.5,
      fill: { color: bg }, line: { color: GRAY, width: 0.5 }
    });
    slide.addText(row[0], {
      x: colX[0] + 0.1, y: y, w: colW[0] - 0.18, h: 0.5,
      fontSize: 13, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });

    // Score column — big number
    slide.addShape(pres.shapes.RECTANGLE, {
      x: colX[1], y: y, w: colW[1] - 0.05, h: 0.5,
      fill: { color: bg }, line: { color: GRAY, width: 0.5 }
    });
    slide.addText(row[1], {
      x: colX[1], y: y, w: colW[1] - 0.05, h: 0.5,
      fontSize: 16, bold: true, color: row[3], fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });

    // Severity badge
    slide.addShape(pres.shapes.RECTANGLE, {
      x: colX[2], y: y, w: colW[2] - 0.05, h: 0.5,
      fill: { color: bg }, line: { color: GRAY, width: 0.5 }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: colX[2] + 0.35, y: y + 0.1, w: 1.8, h: 0.3,
      fill: { color: row[3] }, line: { color: row[3] }
    });
    slide.addText(row[2], {
      x: colX[2] + 0.35, y: y + 0.1, w: 1.8, h: 0.3,
      fontSize: 11, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
  });
}

// ─── SLIDE 6 — IDOR FIX ─────────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Vulnerability Fix #1 — IDOR");
  addFooter(slide, "Slide 6 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: RED }, line: { color: RED }
  });

  // Left column: what + attack
  slide.addText("What is IDOR?", {
    x: 0.4, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.35, w: 4.5, h: 0.8,
    fill: { color: DBLUE }, line: { color: GRAY, width: 0.5 }
  });
  slide.addText("Accessing another user's data by guessing integer IDs", {
    x: 0.5, y: 1.35, w: 4.3, h: 0.8,
    fontSize: 13, color: WHITE, fontFace: "Calibri", valign: "middle",
    wrap: true, margin: 0
  });

  slide.addText("Attack Example", {
    x: 0.4, y: 2.22, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: RED, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 2.55, w: 4.5, h: 0.65,
    fill: { color: CODEBG }, line: { color: RED, width: 1 }
  });
  slide.addText("GET /vault/view/1  →  attacker sees victim's passwords", {
    x: 0.5, y: 2.55, w: 4.3, h: 0.65,
    fontSize: 12, color: RED, fontFace: "Consolas", valign: "middle", margin: 0
  });

  // Result box
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 3.3, w: 4.5, h: 0.7,
    fill: { color: "1a3a2a" }, line: { color: GREEN, width: 1.5 }
  });
  slide.addText("Result: 3 IDOR tests pass\n(view, edit, delete all return HTTP 403)", {
    x: 0.5, y: 3.3, w: 4.3, h: 0.7,
    fontSize: 12, bold: true, color: GREEN, fontFace: "Calibri", valign: "middle", margin: 0
  });

  // Right column: code fix
  slide.addText("Our Fix — get_entry_or_403():", {
    x: 5.1, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.1, y: 1.35, w: 4.5, h: 2.0,
    fill: { color: CODEBG }, line: { color: BLUE, width: 1.5 }
  });
  slide.addText([
    { text: "entry", options: { color: LBLUE } },
    { text: " = db.session.get(", options: { color: WHITE } },
    { text: "VaultEntry", options: { color: "f6c90e" } },
    { text: ", entry_id)", options: { color: WHITE } },
    { text: "\n", options: {} },
    { text: "if", options: { color: BLUE } },
    { text: " entry.user_id ", options: { color: WHITE } },
    { text: "!=", options: { color: RED } },
    { text: " current_user.id:", options: { color: WHITE } },
    { text: "\n", options: {} },
    { text: "    abort(", options: { color: WHITE } },
    { text: "403", options: { color: RED } },
    { text: ")  ", options: { color: WHITE } },
    { text: "# ownership check", options: { color: GRAY } },
  ], {
    x: 5.2, y: 1.4, w: 4.3, h: 1.9,
    fontSize: 13, fontFace: "Consolas", valign: "top", margin: 0
  });

  // IDOR check flow diagram
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.1, y: 3.45, w: 4.5, h: 0.78,
    fill: { color: DBLUE }, line: { color: BLUE, width: 1 }
  });
  slide.addText([
    { text: "Request  →  ", options: { color: WHITE } },
    { text: "Ownership Check", options: { color: LBLUE, bold: true } },
    { text: "\n", options: {} },
    { text: "User owns entry?  ", options: { color: WHITE } },
    { text: "YES", options: { color: GREEN, bold: true } },
    { text: " → Allow  |  ", options: { color: WHITE } },
    { text: "NO", options: { color: RED, bold: true } },
    { text: " → 403 Forbidden", options: { color: RED } },
  ], {
    x: 5.2, y: 3.45, w: 4.3, h: 0.78,
    fontSize: 12, fontFace: "Calibri", valign: "middle", margin: 0
  });
}

// ─── SLIDE 7 — CSRF FIX ─────────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Vulnerability Fix #2 — CSRF");
  addFooter(slide, "Slide 7 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: YELLOW }, line: { color: YELLOW }
  });

  // Left col
  slide.addText("What is CSRF?", {
    x: 0.4, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.35, w: 4.5, h: 0.72,
    fill: { color: DBLUE }, line: { color: GRAY, width: 0.5 }
  });
  slide.addText("Forged requests submitted by attacker on victim's behalf", {
    x: 0.5, y: 1.35, w: 4.3, h: 0.72,
    fontSize: 13, color: WHITE, fontFace: "Calibri", valign: "middle", wrap: true, margin: 0
  });

  slide.addText("Attack Example", {
    x: 0.4, y: 2.14, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: RED, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 2.47, w: 4.5, h: 0.65,
    fill: { color: CODEBG }, line: { color: RED, width: 1 }
  });
  slide.addText("Hidden form on evil.com\nauto-submits DELETE to vault", {
    x: 0.5, y: 2.47, w: 4.3, h: 0.65,
    fontSize: 12, color: RED, fontFace: "Consolas", valign: "middle", margin: 0
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 3.22, w: 4.5, h: 0.72,
    fill: { color: "1a3a2a" }, line: { color: GREEN, width: 1.5 }
  });
  slide.addText("Result: Any POST without valid token\n→ 400 Bad Request", {
    x: 0.5, y: 3.22, w: 4.3, h: 0.72,
    fontSize: 12, bold: true, color: GREEN, fontFace: "Calibri", valign: "middle", margin: 0
  });

  // Right col: fixes
  slide.addText("Our Fix:", {
    x: 5.1, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });

  const fixes = [
    "Flask-WTF CSRFProtect — validates token on every POST",
    "{{ form.hidden_tag() }} — CSRF token in every form",
    "SameSite=Strict cookies — blocks cross-site requests",
    "DELETE uses POST only — no GET-triggered deletions",
  ];
  fixes.forEach((f, i) => {
    const y = 1.38 + i * 0.62;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 5.1, y: y, w: 4.5, h: 0.55,
      fill: { color: DBLUE }, line: { color: BLUE, width: 0.5 }
    });
    slide.addShape(pres.shapes.OVAL, {
      x: 5.2, y: y + 0.14, w: 0.28, h: 0.28,
      fill: { color: GREEN }, line: { color: GREEN }
    });
    slide.addText(f, {
      x: 5.6, y: y, w: 3.85, h: 0.55,
      fontSize: 12, color: WHITE, fontFace: "Calibri", valign: "middle", wrap: true, margin: 0
    });
  });
}

// ─── SLIDE 8 — CLICKJACKING FIX ─────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Vulnerability Fix #3 — Clickjacking");
  addFooter(slide, "Slide 8 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: YELLOW }, line: { color: YELLOW }
  });

  // Left col
  slide.addText("What is Clickjacking?", {
    x: 0.4, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.35, w: 4.5, h: 0.82,
    fill: { color: DBLUE }, line: { color: GRAY, width: 0.5 }
  });
  slide.addText("App embedded in iframe on attacker site;\nuser clicks invisible buttons", {
    x: 0.5, y: 1.35, w: 4.3, h: 0.82,
    fontSize: 13, color: WHITE, fontFace: "Calibri", valign: "middle", wrap: true, margin: 0
  });

  slide.addText("Attack Technique", {
    x: 0.4, y: 2.24, w: 4.5, h: 0.3,
    fontSize: 14, bold: true, color: RED, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 2.57, w: 4.5, h: 0.58,
    fill: { color: CODEBG }, line: { color: RED, width: 1 }
  });
  slide.addText('iframe { opacity: 0; }  // overlay trick', {
    x: 0.5, y: 2.57, w: 4.3, h: 0.58,
    fontSize: 12, color: RED, fontFace: "Consolas", valign: "middle", margin: 0
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 3.25, w: 4.5, h: 0.72,
    fill: { color: "1a3a2a" }, line: { color: GREEN, width: 1.5 }
  });
  slide.addText("Result: Browser blocks all iframe\nembedding of SecureVault", {
    x: 0.5, y: 3.25, w: 4.3, h: 0.72,
    fontSize: 12, bold: true, color: GREEN, fontFace: "Calibri", valign: "middle", margin: 0
  });

  // Right col: code headers
  slide.addText("Our Fix (applied on EVERY response):", {
    x: 5.1, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 13, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.1, y: 1.35, w: 4.5, h: 2.25,
    fill: { color: CODEBG }, line: { color: BLUE, width: 1.5 }
  });
  slide.addText([
    { text: "X-Frame-Options", options: { color: LBLUE } },
    { text: ": DENY", options: { color: WHITE } },
    { text: "\n", options: {} },
    { text: "Content-Security-Policy", options: { color: LBLUE } },
    { text: ":\n  frame-ancestors 'none'", options: { color: WHITE } },
    { text: "\n", options: {} },
    { text: "X-Content-Type-Options", options: { color: LBLUE } },
    { text: ": nosniff", options: { color: WHITE } },
    { text: "\n", options: {} },
    { text: "Referrer-Policy", options: { color: LBLUE } },
    { text: ":\n  strict-origin-when-cross-origin", options: { color: WHITE } },
  ], {
    x: 5.2, y: 1.42, w: 4.3, h: 2.12,
    fontSize: 12, fontFace: "Consolas", valign: "top", margin: 0
  });
}

// ─── SLIDE 9 — CI/CD PIPELINE ───────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "GitHub Actions CI/CD Pipeline");
  addFooter(slide, "Slide 9 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  slide.addText("6-Job Pipeline", {
    x: 0.4, y: 1.0, w: 4.0, h: 0.35,
    fontSize: 16, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });

  const jobs = [
    { num: "1", title: "Unit Tests", detail: "pytest — 18 tests", col: GREEN },
    { num: "2", title: "SAST — Bandit", detail: "Python security linting", col: BLUE },
    { num: "3", title: "SAST — CodeQL", detail: "GitHub security analysis", col: BLUE },
    { num: "4", title: "Dependency Scan", detail: "Safety — CVE database check", col: YELLOW },
    { num: "5", title: "DAST", detail: "OWASP ZAP Baseline Scan", col: RED },
    { num: "6", title: "Docker Build", detail: "Build + Smoke Test", col: "9f7aea" },
  ];

  // Two columns of 3 jobs each
  jobs.forEach((job, i) => {
    const col = i < 3 ? 0 : 1;
    const row = i % 3;
    const x = col === 0 ? 0.4 : 5.15;
    const y = 1.38 + row * 1.17;
    const w = 4.55;

    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: w, h: 1.0,
      fill: { color: DBLUE }, line: { color: job.col, width: 1.5 }
    });
    // Job number circle
    slide.addShape(pres.shapes.OVAL, {
      x: x + 0.12, y: y + 0.25, w: 0.48, h: 0.48,
      fill: { color: job.col }, line: { color: job.col }
    });
    slide.addText(job.num, {
      x: x + 0.12, y: y + 0.25, w: 0.48, h: 0.48,
      fontSize: 14, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(job.title, {
      x: x + 0.72, y: y + 0.08, w: w - 0.85, h: 0.38,
      fontSize: 14, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText(job.detail, {
      x: x + 0.72, y: y + 0.48, w: w - 0.85, h: 0.38,
      fontSize: 12, color: LBLUE, fontFace: "Calibri", valign: "middle", margin: 0
    });
  });

  // Footer warning
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 4.9, w: 9.2, h: 0.35,
    fill: { color: "3a1a1a" }, line: { color: RED, width: 1.5 }
  });
  slide.addText("Pipeline fails on any HIGH severity finding", {
    x: 0.5, y: 4.9, w: 9.0, h: 0.35,
    fontSize: 13, bold: true, color: RED, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });
}

// ─── SLIDE 10 — SECURITY TESTING RESULTS ────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Security Testing Results");
  addFooter(slide, "Slide 10 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: GREEN }, line: { color: GREEN }
  });

  // Top results row
  const results = [
    { tool: "pytest", result: "18/18", detail: "PASSED", col: GREEN },
    { tool: "Bandit", result: "0/0/0", detail: "HIGH/MED/LOW", col: GREEN },
    { tool: "CodeQL", result: "CLEAN", detail: "No vulns found", col: GREEN },
    { tool: "Safety", result: "CLEAN", detail: "No CVEs found", col: GREEN },
    { tool: "ZAP DAST", result: "0 HIGH", detail: "All alerts fixed", col: GREEN },
  ];

  const boxW = 1.75;
  results.forEach((r, i) => {
    const x = 0.4 + i * (boxW + 0.12);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.05, w: boxW, h: 1.05,
      fill: { color: "1a3a2a" }, line: { color: GREEN, width: 1.5 }
    });
    slide.addText(r.tool, {
      x: x, y: 1.05, w: boxW, h: 0.28,
      fontSize: 10, bold: true, color: LBLUE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(r.result, {
      x: x, y: 1.33, w: boxW, h: 0.42,
      fontSize: 15, bold: true, color: GREEN, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(r.detail, {
      x: x, y: 1.78, w: boxW, h: 0.25,
      fontSize: 9, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
  });

  // Before vs After table
  slide.addText("Before vs After Security Improvements", {
    x: 0.4, y: 2.25, w: 9.2, h: 0.32,
    fontSize: 14, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });

  const tableHeaders = ["Vulnerability", "Before", "After"];
  const tableColX = [0.4, 3.8, 6.6];
  const tableColW = [3.35, 2.75, 3.0];

  tableHeaders.forEach((h, i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: tableColX[i], y: 2.6, w: tableColW[i] - 0.05, h: 0.38,
      fill: { color: BLUE }, line: { color: BLUE }
    });
    slide.addText(h, {
      x: tableColX[i], y: 2.6, w: tableColW[i] - 0.05, h: 0.38,
      fontSize: 12, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
  });

  const tableRows = [
    ["IDOR", "Any user could access", "HTTP 403 blocked"],
    ["CSRF", "No token protection", "CSRF token required"],
    ["Clickjacking", "No security headers", "DENY + frame-ancestors none"],
  ];
  const rowBg2 = [DBLUE, "1e2742"];

  tableRows.forEach((row, ri) => {
    const y = 3.02 + ri * 0.62;
    tableColX.forEach((cx, ci) => {
      slide.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: y, w: tableColW[ci] - 0.05, h: 0.55,
        fill: { color: rowBg2[ri % 2] }, line: { color: GRAY, width: 0.5 }
      });
      // "After" column gets a green indicator
      const textColor = ci === 2 ? GREEN : ci === 1 ? RED : WHITE;
      slide.addText(row[ci], {
        x: cx + 0.1, y: y, w: tableColW[ci] - 0.2, h: 0.55,
        fontSize: 12, color: textColor, fontFace: "Calibri",
        bold: ci !== 0 ? true : false,
        valign: "middle", margin: 0
      });
    });
  });
}

// ─── SLIDE 11 — SECURITY ARCHITECTURE ───────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);
  addTitleBar(slide, "Security Architecture");
  addFooter(slide, "Slide 11 of 12");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  slide.addText("Layered Defense-in-Depth", {
    x: 0.4, y: 1.0, w: 9.2, h: 0.3,
    fontSize: 14, color: LBLUE, fontFace: "Calibri", italic: true, margin: 0
  });

  const layers = [
    { n: "1", label: "Transport", detail: "HTTPS / TLS", col: "9f7aea" },
    { n: "2", label: "Authentication", detail: "bcrypt + Flask-Login", col: BLUE },
    { n: "3", label: "Authorization", detail: "IDOR check (ownership)", col: MBLUE },
    { n: "4", label: "Session", detail: "HttpOnly + SameSite=Strict + Secure", col: "0891b2" },
    { n: "5", label: "CSRF", detail: "Flask-WTF token validation", col: YELLOW },
    { n: "6", label: "Framing", detail: "X-Frame-Options + CSP", col: YELLOW },
    { n: "7", label: "Storage", detail: "Fernet AES-128-CBC encryption", col: GREEN },
    { n: "8", label: "CI/CD", detail: "Automated SAST+DAST on every push", col: GREEN },
  ];

  layers.forEach((l, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i % 4;
    const x = col === 0 ? 0.4 : 5.15;
    const y = 1.35 + row * 0.97;
    const w = 4.55;

    // Gradient effect via two rect overlay
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: w, h: 0.82,
      fill: { color: DBLUE }, line: { color: l.col, width: 1 }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: 0.06, h: 0.82,
      fill: { color: l.col }, line: { color: l.col }
    });
    // Layer number
    slide.addText(l.n, {
      x: x + 0.12, y: y, w: 0.38, h: 0.82,
      fontSize: 18, bold: true, color: l.col, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(l.label, {
      x: x + 0.55, y: y + 0.05, w: w - 0.65, h: 0.32,
      fontSize: 13, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
    slide.addText(l.detail, {
      x: x + 0.55, y: y + 0.42, w: w - 0.65, h: 0.3,
      fontSize: 11, color: LBLUE, fontFace: "Calibri", valign: "middle", margin: 0
    });
  });
}

// ─── SLIDE 12 — CONCLUSION ───────────────────────────────────────────────────
{
  const slide = pres.addSlide();
  addBg(slide);

  // Top accent stripe
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: SW, h: 0.08,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  // Decorative circles
  slide.addShape(pres.shapes.OVAL, {
    x: 7.5, y: -0.8, w: 4, h: 4,
    fill: { color: MBLUE, transparency: 88 }, line: { color: MBLUE, transparency: 88 }
  });

  addTitleBar(slide, "Conclusion & Demo");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.92, w: 9.2, h: 0.03,
    fill: { color: GREEN }, line: { color: GREEN }
  });

  // Achievements
  slide.addText("Achievements", {
    x: 0.4, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 15, bold: true, color: GREEN, fontFace: "Calibri", margin: 0
  });

  const achievements = [
    "3 OWASP vulnerabilities fully mitigated (IDOR, CSRF, Clickjacking)",
    "18/18 security tests pass",
    "Production-ready 6-job CI/CD pipeline",
    "Fernet-encrypted vault storage",
    "Dockerized with non-root user, read-only filesystem",
    "Complete security documentation (PNE, STRIDE, CVSS)",
  ];

  achievements.forEach((a, i) => {
    const y = 1.35 + i * 0.48;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: y + 0.08, w: 0.26, h: 0.26,
      fill: { color: GREEN }, line: { color: GREEN }
    });
    slide.addText("✓", {
      x: 0.4, y: y + 0.08, w: 0.26, h: 0.26,
      fontSize: 11, bold: true, color: WHITE, fontFace: "Calibri",
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(a, {
      x: 0.75, y: y, w: 4.1, h: 0.42,
      fontSize: 12, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
  });

  // Future Work
  slide.addText("Future Work", {
    x: 5.1, y: 1.02, w: 4.5, h: 0.3,
    fontSize: 15, bold: true, color: LBLUE, fontFace: "Calibri", margin: 0
  });

  const future = [
    "Rate limiting on login (brute-force protection)",
    "Two-factor authentication (2FA)",
    "Full audit logging",
    "Password strength meter",
  ];

  future.forEach((f, i) => {
    const y = 1.35 + i * 0.6;
    slide.addShape(pres.shapes.OVAL, {
      x: 5.1, y: y + 0.1, w: 0.26, h: 0.26,
      fill: { color: LBLUE }, line: { color: LBLUE }
    });
    slide.addText(f, {
      x: 5.45, y: y, w: 4.15, h: 0.48,
      fontSize: 13, color: WHITE, fontFace: "Calibri", valign: "middle", margin: 0
    });
  });

  // Separator line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.0, y: 1.05, w: 0.04, h: 3.55,
    fill: { color: BLUE }, line: { color: BLUE }
  });

  // Thank you
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 4.62, w: 9.2, h: 0.68,
    fill: { color: BLUE }, line: { color: BLUE }
  });
  slide.addText("Thank you!   Questions?", {
    x: 0.4, y: 4.62, w: 9.2, h: 0.68,
    fontSize: 24, bold: true, color: WHITE, fontFace: "Calibri",
    align: "center", valign: "middle", margin: 0
  });
}

// ─── SAVE ────────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "C:/ssd/Presentation_SecureVault.pptx" })
  .then(() => { console.log("Saved: C:/ssd/Presentation_SecureVault.pptx"); })
  .catch(err => { console.error("Error:", err); process.exit(1); });
