"""
Threat Model PDF Generator for SecureVault — CYC386
Uses ReportLab to produce a professional multi-page PDF.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor, Color
import os

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_NAVY   = HexColor("#0D1B2A")
NAVY        = HexColor("#1B3A5C")
MID_BLUE    = HexColor("#2E6DA4")
LIGHT_BLUE  = HexColor("#D6E4F0")
ACCENT      = HexColor("#E8A838")       # gold accent
WHITE       = colors.white
BLACK       = colors.black
LIGHT_GRAY  = HexColor("#F5F5F5")
MID_GRAY    = HexColor("#CCCCCC")
DARK_GRAY   = HexColor("#555555")

RED         = HexColor("#C0392B")
ORANGE      = HexColor("#E67E22")
GREEN       = HexColor("#27AE60")
PALE_RED    = HexColor("#FADBD8")
PALE_ORANGE = HexColor("#FDEBD0")
PALE_GREEN  = HexColor("#D5F5E3")

OUTPUT_PATH = r"C:/ssd/THREAT_MODEL_SecureVault.pdf"

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=34,
        spaceAfter=10,
    )
    styles["cover_sub"] = ParagraphStyle(
        "cover_sub",
        fontName="Helvetica",
        fontSize=14,
        textColor=HexColor("#B0C4D8"),
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=6,
    )
    styles["cover_meta"] = ParagraphStyle(
        "cover_meta",
        fontName="Helvetica",
        fontSize=11,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=16,
        spaceAfter=4,
    )
    styles["cover_label"] = ParagraphStyle(
        "cover_label",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=ACCENT,
        alignment=TA_CENTER,
        leading=16,
        spaceBefore=14,
        spaceAfter=2,
    )
    styles["section_h1"] = ParagraphStyle(
        "section_h1",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=WHITE,
        leading=20,
        spaceBefore=18,
        spaceAfter=8,
        leftIndent=0,
    )
    styles["section_h2"] = ParagraphStyle(
        "section_h2",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=NAVY,
        leading=16,
        spaceBefore=12,
        spaceAfter=4,
        leftIndent=0,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=HexColor("#222222"),
        leading=14,
        spaceAfter=4,
        alignment=TA_JUSTIFY,
    )
    styles["mono"] = ParagraphStyle(
        "mono",
        fontName="Courier",
        fontSize=8.5,
        textColor=DARK_NAVY,
        leading=13,
        spaceAfter=3,
        leftIndent=12,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=HexColor("#222222"),
        leading=14,
        spaceAfter=3,
        leftIndent=18,
        bulletIndent=6,
    )
    styles["table_header"] = ParagraphStyle(
        "table_header",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=10,
    )
    styles["table_cell"] = ParagraphStyle(
        "table_cell",
        fontName="Helvetica",
        fontSize=8,
        textColor=BLACK,
        leading=10,
        alignment=TA_LEFT,
    )
    styles["table_cell_center"] = ParagraphStyle(
        "table_cell_center",
        fontName="Helvetica",
        fontSize=8,
        textColor=BLACK,
        leading=10,
        alignment=TA_CENTER,
    )
    styles["caption"] = ParagraphStyle(
        "caption",
        fontName="Helvetica-Oblique",
        fontSize=8,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        leading=11,
        spaceAfter=8,
    )
    styles["attack_node"] = ParagraphStyle(
        "attack_node",
        fontName="Courier",
        fontSize=8.5,
        textColor=DARK_NAVY,
        leading=12,
        leftIndent=0,
    )
    return styles


# ── Helper flowables ──────────────────────────────────────────────────────────
class SectionBanner(Flowable):
    """Full-width coloured banner for section headings."""

    def __init__(self, text, width, bg=NAVY, fg=WHITE, font_size=13):
        super().__init__()
        self.text = text
        self.banner_width = width
        self.bg = bg
        self.fg = fg
        self.font_size = font_size
        self.height = font_size + 12

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.rect(-1, -4, self.banner_width + 2, self.height, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont("Helvetica-Bold", self.font_size)
        c.drawString(8, 4, self.text)

    def wrap(self, availWidth, availHeight):
        return self.banner_width, self.height


class AccentLine(Flowable):
    """Thin horizontal rule in accent colour."""

    def __init__(self, width, color=ACCENT, thickness=2):
        super().__init__()
        self.line_width = width
        self.color = color
        self.thickness = thickness

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.thickness)
        c.line(0, 0, self.line_width, 0)

    def wrap(self, availWidth, availHeight):
        return self.line_width, self.thickness + 4


def P(text, style):
    return Paragraph(text, style)


def header_para(text, styles):
    return Paragraph(text, styles["table_header"])


def cell_para(text, styles, center=False):
    key = "table_cell_center" if center else "table_cell"
    return Paragraph(text, styles[key])


# ── Cover page ────────────────────────────────────────────────────────────────
def build_cover(styles, page_w, page_h):
    story = []

    # Dark background block simulated with a large coloured rectangle table
    cover_data = [[""]]
    cover_table = Table(cover_data, colWidths=[page_w - 4*cm], rowHeights=[page_h * 0.55])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_NAVY),
        ("BOX",        (0, 0), (-1, -1), 1.5, ACCENT),
    ]))

    # We'll build the cover as a series of elements with coloured text
    story.append(Spacer(1, 2*cm))

    # Top banner bar
    banner_data = [["  THREAT MODEL REPORT"]]
    banner_tbl = Table(banner_data, colWidths=[page_w - 4*cm])
    banner_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), DARK_NAVY),
        ("TEXTCOLOR",   (0, 0), (-1, -1), WHITE),
        ("FONTNAME",    (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 11),
        ("TOPPADDING",  (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(banner_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Main title block
    title_data = [
        [P("SecureVault", ParagraphStyle("ct", fontName="Helvetica-Bold",
           fontSize=36, textColor=ACCENT, alignment=TA_CENTER, leading=40))],
        [P("Password Vault", ParagraphStyle("ct2", fontName="Helvetica-Bold",
           fontSize=28, textColor=WHITE, alignment=TA_CENTER, leading=34))],
        [P("Threat Model", ParagraphStyle("ct3", fontName="Helvetica",
           fontSize=20, textColor=HexColor("#B0C4D8"), alignment=TA_CENTER, leading=26))],
    ]
    title_tbl = Table(title_data, colWidths=[page_w - 4*cm])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), DARK_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(title_tbl)
    story.append(Spacer(1, 0.2*cm))

    # Method badge
    method_data = [["  STRIDE + DFD + Attack Tree + CVSS v3.1  "]]
    method_tbl = Table(method_data, colWidths=[page_w - 4*cm])
    method_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), MID_BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(method_tbl)
    story.append(Spacer(1, 0.5*cm))

    # Course + meta info block
    meta_rows = [
        ["Course",     "CYC386 — Secure Software Design and Development"],
        ["Instructor", "Engr. Muhammad Ahmad Nawaz"],
        ["Date",       "April 8, 2026"],
        ["Team",       "SecureVault"],
    ]
    meta_data = [[
        P(r, ParagraphStyle("ml", fontName="Helvetica-Bold", fontSize=9,
                             textColor=ACCENT, leading=13)),
        P(v, ParagraphStyle("mv", fontName="Helvetica", fontSize=9,
                             textColor=WHITE, leading=13)),
    ] for r, v in meta_rows]

    meta_tbl = Table(meta_data, colWidths=[3.5*cm, page_w - 4*cm - 3.5*cm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), DARK_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (0, -1), 20),
        ("LEFTPADDING",   (1, 0), (1, -1), 8),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, HexColor("#2E6DA4")),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 0.4*cm))

    # Team members
    members = [
        ("Daniyal Ahmed",       "SP23-BCT-011"),
        ("Shaheer Khalid",      "SP23-BCT-048"),
        ("Maaz Malik",          "SP23-BCT-025"),
        ("Rana Mutahhar Ahmed", "SP23-BCT-045"),
    ]
    team_header = [[
        P("TEAM MEMBERS", ParagraphStyle("th", fontName="Helvetica-Bold",
           fontSize=9, textColor=ACCENT, leading=12)),
        P("STUDENT ID", ParagraphStyle("ti", fontName="Helvetica-Bold",
           fontSize=9, textColor=ACCENT, leading=12)),
    ]]
    team_rows = [[
        P(n, ParagraphStyle("tn", fontName="Helvetica", fontSize=9.5,
                             textColor=WHITE, leading=14)),
        P(i, ParagraphStyle("tid", fontName="Courier", fontSize=9,
                             textColor=HexColor("#B0C4D8"), leading=14)),
    ] for n, i in members]

    team_data = team_header + team_rows
    col_w = (page_w - 4*cm) / 2
    team_tbl = Table(team_data, colWidths=[col_w, col_w])
    team_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("BACKGROUND",    (0, 1), (-1, -1), DARK_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, HexColor("#2E6DA4")),
        ("BOX",           (0, 0), (-1, -1), 1, ACCENT),
    ]))
    story.append(team_tbl)

    # Bottom accent line
    story.append(Spacer(1, 0.6*cm))
    story.append(AccentLine(page_w - 4*cm, ACCENT, 3))
    story.append(Spacer(1, 0.2*cm))

    # Confidentiality notice
    notice_data = [["CONFIDENTIAL — Academic Use Only — CYC386 Spring 2026"]]
    notice_tbl = Table(notice_data, colWidths=[page_w - 4*cm])
    notice_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#1A1A2E")),
        ("TEXTCOLOR",     (0, 0), (-1, -1), MID_GRAY),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Oblique"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(notice_tbl)
    story.append(PageBreak())
    return story


# ── Table of Contents ─────────────────────────────────────────────────────────
def build_toc(styles, page_w):
    story = []
    story.append(SectionBanner("TABLE OF CONTENTS", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.4*cm))

    toc_items = [
        ("1", "Data Flow Diagrams (DFD Level 0 & Level 1)",    "3"),
        ("2", "STRIDE Threat Table",                            "4"),
        ("3", "Attack Tree — IDOR Attack",                      "6"),
        ("4", "Attack Tree — CSRF Attack",                      "7"),
        ("5", "CVSS v3.1 Risk Assessment",                      "8"),
    ]

    toc_data = [
        [P("#", styles["table_header"]),
         P("Section", styles["table_header"]),
         P("Page", styles["table_header"])]
    ]
    for num, title, page in toc_items:
        toc_data.append([
            cell_para(num, styles, center=True),
            cell_para(title, styles),
            cell_para(page, styles, center=True),
        ])

    toc_tbl = Table(toc_data, colWidths=[1.2*cm, page_w - 4*cm - 2.4*cm, 1.2*cm])
    toc_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("BACKGROUND",    (0, 1), (-1, -1), LIGHT_GRAY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.2, NAVY),
    ]))
    story.append(toc_tbl)
    story.append(Spacer(1, 1*cm))

    # Executive Summary
    story.append(SectionBanner("EXECUTIVE SUMMARY", page_w - 4*cm, NAVY))
    story.append(Spacer(1, 0.3*cm))

    summary_text = (
        "SecureVault is a Flask-based password vault application developed as part of the CYC386 "
        "Secure Software Design and Development course. This threat model applies the STRIDE "
        "methodology, supported by Data Flow Diagrams (DFD), Attack Trees, and CVSS v3.1 scoring, "
        "to systematically identify, analyse, and document security threats across all application layers."
    )
    story.append(P(summary_text, styles["body"]))
    story.append(Spacer(1, 0.2*cm))

    summary2 = (
        "The analysis identified <b>10 distinct threats</b> spanning authentication, session management, "
        "data integrity, information disclosure, and client-side attack vectors. Of these, "
        "<b>9 threats are fully mitigated</b> through implemented controls including bcrypt hashing, "
        "Fernet encryption, ownership-based access control, CSRF token validation, and CI/CD pipeline "
        "security scanning. One threat (audit logging) remains <b>partially mitigated</b> and is "
        "scheduled for future implementation."
    )
    story.append(P(summary2, styles["body"]))
    story.append(Spacer(1, 0.25*cm))

    summary3 = (
        "The highest-severity finding is <b>T2 — IDOR (CVSS 8.1 HIGH)</b>, which allows an "
        "authenticated user to access vault entries belonging to other users by manipulating URL "
        "parameters. This is fully mitigated by the <code>get_entry_or_403()</code> ownership "
        "verification function enforced on every vault operation."
    )
    story.append(P(summary3, styles["body"]))
    story.append(PageBreak())
    return story


# ── Section 1: DFDs ───────────────────────────────────────────────────────────
def build_dfd(styles, page_w):
    story = []
    story.append(SectionBanner("SECTION 1 — DATA FLOW DIAGRAMS", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.5*cm))

    # 1.1 DFD Level 0
    story.append(P("1.1  DFD Level 0 — System Context Diagram", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.3*cm))

    story.append(P(
        "The Level 0 DFD shows the highest-level view of the SecureVault system, depicting "
        "the single process (Flask web application), its external entities, data stores, and "
        "trust boundaries.", styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    # DFD Level 0 diagram as table
    dfd0_rows = [
        ["External Entity", "Data Flow", "Process / Store", "Trust Boundary"],
        ["Browser / User",  "HTTPS (TLS 1.2+)",    "Flask App (Web Server)", "Internet ↔ App Server"],
        ["Flask App",       "SQLAlchemy ORM",       "SQLite Database (vault.db)", "App Server ↔ Database"],
    ]
    dfd0_data = [
        [P(c, styles["table_header"]) for c in dfd0_rows[0]]
    ] + [
        [cell_para(c, styles) for c in row] for row in dfd0_rows[1:]
    ]
    col_w = (page_w - 4*cm) / 4
    dfd0_tbl = Table(dfd0_data, colWidths=[col_w]*4)
    dfd0_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
    ]))
    story.append(dfd0_tbl)
    story.append(P("Figure 1.1 — DFD Level 0: System Context", styles["caption"]))

    # ASCII-art style representation
    story.append(Spacer(1, 0.2*cm))
    flow_lines = [
        "  ┌─────────────────────┐        HTTPS / TLS        ┌──────────────────────────┐",
        "  │   Browser / User    │ ─────────────────────────► │   Flask App (Web Server)  │",
        "  └─────────────────────┘                            └──────────────┬───────────┘",
        "                                                                     │",
        "         ╔═══════ Trust Boundary: Internet / App Server ════════╗   │  SQLAlchemy ORM",
        "         ║                                                       ║   │",
        "         ╔═══════ Trust Boundary: App Server / Database  ════════╗  ▼",
        "                                                            ┌──────────────────────┐",
        "                                                            │  SQLite Database      │",
        "                                                            │  (vault.db)           │",
        "                                                            └──────────────────────┘",
    ]
    dfd_box_data = [["\n".join(flow_lines)]]
    dfd_box = Table(dfd_box_data, colWidths=[page_w - 4*cm])
    dfd_box.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F0F4F8")),
        ("FONTNAME",      (0, 0), (-1, -1), "Courier"),
        ("FONTSIZE",      (0, 0), (-1, -1), 7.5),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("BOX",           (0, 0), (-1, -1), 1, MID_BLUE),
    ]))
    story.append(dfd_box)
    story.append(Spacer(1, 0.5*cm))

    # 1.2 DFD Level 1
    story.append(P("1.2  DFD Level 1 — Key Process Decomposition", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.3*cm))

    story.append(P(
        "The Level 1 DFD decomposes the Flask application into four key processes, each with "
        "its own data flows, security controls, and interactions with external systems.",
        styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    dfd1_rows = [
        ["Process", "Actor / Source", "Data Flow", "Destination / Action", "Security Control"],
        ["Auth Module",    "User",    "Register / Login",         "DB: users table",         "bcrypt cost-12 verify"],
        ["Vault Module",   "User",    "Add / Edit / Delete Entry","DB: vault_entries table",  "Ownership check → 403"],
        ["Vault Module",   "User",    "View Entry",               "Fernet decrypt → plaintext","Fernet symmetric enc."],
        ["CI/CD Pipeline", "CI/CD",   "git push trigger",         "GitHub Actions runner",    "Bandit / CodeQL / ZAP / Safety"],
    ]
    dfd1_data = [
        [P(c, styles["table_header"]) for c in dfd1_rows[0]]
    ] + [
        [cell_para(c, styles) for c in row] for row in dfd1_rows[1:]
    ]
    col_widths_dfd1 = [2.8*cm, 2.2*cm, 3.3*cm, 3.3*cm, 3.7*cm]
    dfd1_tbl = Table(dfd1_data, colWidths=col_widths_dfd1)
    dfd1_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(dfd1_tbl)
    story.append(P("Figure 1.2 — DFD Level 1: Key Process Decomposition", styles["caption"]))
    story.append(PageBreak())
    return story


# ── Section 2: STRIDE Table ───────────────────────────────────────────────────
def build_stride(styles, page_w):
    story = []
    story.append(SectionBanner("SECTION 2 — STRIDE THREAT TABLE", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.3*cm))

    intro = (
        "The STRIDE model categorises threats into six types: <b>S</b>poofing, <b>T</b>ampering, "
        "<b>R</b>epudiation, <b>I</b>nformation Disclosure, <b>D</b>enial of Service, and "
        "<b>E</b>levation of Privilege. The following table documents all 10 identified threats, "
        "their STRIDE category, description, implemented countermeasures, and current status."
    )
    story.append(P(intro, styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    # Threat data
    threats = [
        # ID, Location, Category, Description, Countermeasure, Status
        ("T1",  "Auth — Login",         "Spoofing",               "Brute-force master password",
         "bcrypt cost 12, min 8-char password policy",             "Mitigated"),
        ("T2",  "Vault — View/Edit",    "Tampering",              "IDOR — access another user's entry via URL manipulation",
         "get_entry_or_403() ownership check on every vault op",   "Mitigated"),
        ("T3",  "Session Cookie",       "Repudiation",            "User denies actions; no audit log exists",
         "Timestamps on entries; audit log planned",               "Partial"),
        ("T4",  "DB — vault.db",        "Info. Disclosure",       "DB file read exposes all stored passwords",
         "Fernet symmetric encryption on all vault entries",       "Mitigated"),
        ("T5",  "Any POST Form",        "Elev. of Privilege",     "CSRF — forge state-changing request from attacker site",
         "Flask-WTF CSRF tokens + SameSite=Strict cookie",        "Mitigated"),
        ("T6",  "Browser / IFrame",     "Elev. of Privilege",     "Clickjacking — embed app in hidden iframe",
         "X-Frame-Options: DENY + CSP frame-ancestors 'none'",    "Mitigated"),
        ("T7",  "Encryption Key",       "Info. Disclosure",       "Fernet key committed to Git exposes all passwords",
         ".env file + .gitignore; key never in source control",    "Mitigated"),
        ("T8",  "Login Redirect",       "Spoofing",               "Open redirect — ?next= param redirects to attacker URL",
         "next-param validated: relative paths only",              "Mitigated"),
        ("T9",  "Dependencies",         "Tampering",              "Vulnerable library (supply-chain attack)",
         "safety check integrated in CI/CD pipeline",             "Mitigated"),
        ("T10", "Source Code",          "Info. Disclosure",       "Hardcoded secrets (API keys, passwords in code)",
         "Bandit + CodeQL scanning; no hardcoded secrets found",   "Mitigated"),
    ]

    def status_color(status):
        if status == "Mitigated":
            return PALE_GREEN, GREEN
        elif status == "Partial":
            return PALE_ORANGE, ORANGE
        else:
            return PALE_RED, RED

    headers = ["ID", "Location", "STRIDE\nCategory", "Threat Description",
               "Countermeasure", "Status"]
    col_widths = [1.0*cm, 2.4*cm, 2.0*cm, 4.2*cm, 4.2*cm, 1.8*cm]

    table_data = [[P(h, styles["table_header"]) for h in headers]]
    row_styles = []

    for i, t in enumerate(threats):
        tid, loc, cat, desc, counter, status = t
        bg, fg = status_color(status)
        row = [
            cell_para(f"<b>{tid}</b>", styles, center=True),
            cell_para(loc, styles),
            cell_para(cat, styles),
            cell_para(desc, styles),
            cell_para(counter, styles),
            P(status, ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=7.5,
                                     textColor=fg, leading=10, alignment=TA_CENTER)),
        ]
        table_data.append(row)
        row_num = i + 1
        row_styles.append(("BACKGROUND", (5, row_num), (5, row_num), bg))
        if i % 2 == 0:
            row_styles.append(("BACKGROUND", (0, row_num), (4, row_num), WHITE))
        else:
            row_styles.append(("BACKGROUND", (0, row_num), (4, row_num), LIGHT_GRAY))

    stride_tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
    base_style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, DARK_NAVY),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (0, -1),  "CENTER"),
        ("ALIGN",         (5, 0), (5, -1),  "CENTER"),
    ]
    stride_tbl.setStyle(TableStyle(base_style + row_styles))
    story.append(stride_tbl)
    story.append(P("Table 2.1 — STRIDE Threat Analysis (10 threats)", styles["caption"]))

    story.append(Spacer(1, 0.4*cm))

    # Legend
    legend_data = [[
        P("  Mitigated", ParagraphStyle("lg", fontName="Helvetica-Bold", fontSize=8,
                                         textColor=GREEN, leading=11)),
        P("  Partial", ParagraphStyle("lp", fontName="Helvetica-Bold", fontSize=8,
                                       textColor=ORANGE, leading=11)),
        P("  Unmitigated", ParagraphStyle("lu", fontName="Helvetica-Bold", fontSize=8,
                                           textColor=RED, leading=11)),
        P("  — Status legend", ParagraphStyle("ll", fontName="Helvetica-Oblique",
                                               fontSize=8, textColor=DARK_GRAY, leading=11)),
    ]]
    legend_tbl = Table(legend_data, colWidths=[
        (page_w - 4*cm) / 4] * 4)
    legend_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), PALE_GREEN),
        ("BACKGROUND",    (1, 0), (1, 0), PALE_ORANGE),
        ("BACKGROUND",    (2, 0), (2, 0), PALE_RED),
        ("BACKGROUND",    (3, 0), (3, 0), LIGHT_GRAY),
        ("BOX",           (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(legend_tbl)
    story.append(PageBreak())
    return story


# ── Section 3: Attack Tree — IDOR ─────────────────────────────────────────────
def build_attack_tree_idor(styles, page_w):
    story = []
    story.append(SectionBanner("SECTION 3 — ATTACK TREE: IDOR ATTACK", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.3*cm))

    story.append(P(
        "An Insecure Direct Object Reference (IDOR) attack occurs when an application uses "
        "user-controllable data (such as a URL parameter) to access objects without performing "
        "proper authorisation checks. The following attack tree models the threat against "
        "SecureVault's vault entry endpoints.", styles["body"]))
    story.append(Spacer(1, 0.4*cm))

    # Goal box
    goal_data = [["GOAL: Access another user's vault entry"]]
    goal_tbl = Table(goal_data, colWidths=[page_w - 4*cm])
    goal_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), RED),
        ("TEXTCOLOR",     (0, 0), (-1, -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 11),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX",           (0, 0), (-1, -1), 2, HexColor("#8B0000")),
    ]))
    story.append(goal_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Attack paths
    idor_paths = [
        ("[A]", "Enumerate Entry ID",
         "Guess or enumerate numeric entry ID\nin GET /vault/view/<id>",
         "Ownership check in get_entry_or_403()",
         "HTTP 403 Forbidden",
         "BLOCKED"),
        ("[B]", "Modify via Edit Endpoint",
         "Submit modified data to\nPOST /vault/edit/<id>",
         "Ownership check in get_entry_or_403()",
         "HTTP 403 Forbidden",
         "BLOCKED"),
        ("[C]", "Delete Another User's Entry",
         "Submit deletion request to\nPOST /vault/delete/<id>",
         "Ownership check in get_entry_or_403()",
         "HTTP 403 Forbidden",
         "BLOCKED"),
    ]

    path_header = ["Path", "Attack Vector", "Attacker Action",
                   "Countermeasure", "Result", "Status"]
    path_col_w = [1.0*cm, 2.5*cm, 3.5*cm, 3.8*cm, 2.5*cm, 1.8*cm]

    path_data = [[P(h, styles["table_header"]) for h in path_header]]
    for pid, vec, action, counter, result, status in idor_paths:
        path_data.append([
            cell_para(f"<b>{pid}</b>", styles, center=True),
            cell_para(vec, styles),
            cell_para(action, styles),
            cell_para(counter, styles),
            cell_para(result, styles),
            P(status, ParagraphStyle("bs", fontName="Helvetica-Bold", fontSize=7.5,
                                      textColor=GREEN, leading=10, alignment=TA_CENTER)),
        ])

    path_tbl = Table(path_data, colWidths=path_col_w, repeatRows=1)
    path_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("BACKGROUND",    (5, 1), (5, -1),  PALE_GREEN),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, DARK_NAVY),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (0, -1),  "CENTER"),
        ("ALIGN",         (5, 0), (5, -1),  "CENTER"),
    ]))
    story.append(path_tbl)
    story.append(P("Table 3.1 — IDOR Attack Tree: Attack Paths and Countermeasures", styles["caption"]))

    story.append(Spacer(1, 0.5*cm))

    # ASCII attack tree
    story.append(P("Attack Tree Diagram — IDOR", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.2*cm))

    tree_text = """\
GOAL: Access Another User's Vault Entry
    [ATTACKER IS AUTHENTICATED]
    │
    ├── [A] Enumerate entry ID in GET /vault/view/<id>
    │       └── Countermeasure: get_entry_or_403() → compares entry.user_id == current_user.id
    │           └── RESULT: HTTP 403 Forbidden ✗
    │
    ├── [B] Modify entry via POST /vault/edit/<id>
    │       └── Countermeasure: get_entry_or_403() → ownership enforced before any write
    │           └── RESULT: HTTP 403 Forbidden ✗
    │
    └── [C] Delete entry via POST /vault/delete/<id>
            └── Countermeasure: get_entry_or_403() → ownership enforced before deletion
                └── RESULT: HTTP 403 Forbidden ✗

    ALL ATTACK PATHS BLOCKED — THREAT MITIGATED"""

    tree_data = [[tree_text]]
    tree_tbl = Table(tree_data, colWidths=[page_w - 4*cm])
    tree_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F7F9FB")),
        ("FONTNAME",      (0, 0), (-1, -1), "Courier"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("BOX",           (0, 0), (-1, -1), 1.5, MID_BLUE),
        ("LINEAFTER",     (0, 0), (0, -1),  3, GREEN),
    ]))
    story.append(tree_tbl)

    story.append(Spacer(1, 0.4*cm))
    story.append(P(
        "<b>Key Insight:</b> The IDOR vulnerability is eliminated by the consistent application "
        "of the <code>get_entry_or_403()</code> helper function across all three vault endpoints. "
        "This function fetches the entry by ID and immediately verifies that the "
        "<code>entry.user_id</code> matches the <code>current_user.id</code>. If they differ, "
        "the request is aborted with HTTP 403 before any data is returned or modified.",
        styles["body"]))

    story.append(PageBreak())
    return story


# ── Section 4: Attack Tree — CSRF ─────────────────────────────────────────────
def build_attack_tree_csrf(styles, page_w):
    story = []
    story.append(SectionBanner("SECTION 4 — ATTACK TREE: CSRF ATTACK", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.3*cm))

    story.append(P(
        "A Cross-Site Request Forgery (CSRF) attack tricks an authenticated victim into "
        "unknowingly submitting a malicious request to the application. The attacker exploits "
        "the victim's existing session cookies. The following attack tree models CSRF threats "
        "against SecureVault.", styles["body"]))
    story.append(Spacer(1, 0.4*cm))

    # Goal box
    goal_data = [["GOAL: Perform unauthorised action as the authenticated victim"]]
    goal_tbl = Table(goal_data, colWidths=[page_w - 4*cm])
    goal_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), RED),
        ("TEXTCOLOR",     (0, 0), (-1, -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 11),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX",           (0, 0), (-1, -1), 2, HexColor("#8B0000")),
    ]))
    story.append(goal_tbl)
    story.append(Spacer(1, 0.3*cm))

    csrf_paths = [
        ("[A]", "Crafted GET Link",
         "Trick victim into clicking a crafted\nGET /vault/delete/<id> link",
         "Delete endpoint uses POST only;\nGET requests ignored",
         "HTTP 405 Method Not Allowed",
         "BLOCKED"),
        ("[B]", "Hidden Auto-Submit Form",
         "Embed hidden HTML form on attacker\nsite; auto-submit via JavaScript",
         "Flask-WTF CSRF token required;\nmissing/invalid token → rejected",
         "HTTP 400 Bad Request",
         "BLOCKED"),
        ("[C]", "Same-Site Cookie Theft",
         "Exploit same-site subdomain to\nsteal session cookie",
         "SameSite=Strict cookie attribute;\nbrowser refuses cross-site cookie send",
         "Cookie not transmitted",
         "BLOCKED"),
    ]

    path_header = ["Path", "Attack Vector", "Attacker Action",
                   "Countermeasure", "Result", "Status"]
    path_col_w = [1.0*cm, 2.5*cm, 3.5*cm, 3.8*cm, 2.5*cm, 1.8*cm]

    path_data = [[P(h, styles["table_header"]) for h in path_header]]
    for pid, vec, action, counter, result, status in csrf_paths:
        path_data.append([
            cell_para(f"<b>{pid}</b>", styles, center=True),
            cell_para(vec, styles),
            cell_para(action, styles),
            cell_para(counter, styles),
            cell_para(result, styles),
            P(status, ParagraphStyle("bs2", fontName="Helvetica-Bold", fontSize=7.5,
                                      textColor=GREEN, leading=10, alignment=TA_CENTER)),
        ])

    path_tbl = Table(path_data, colWidths=path_col_w, repeatRows=1)
    path_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("BACKGROUND",    (5, 1), (5, -1),  PALE_GREEN),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, DARK_NAVY),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (0, -1),  "CENTER"),
        ("ALIGN",         (5, 0), (5, -1),  "CENTER"),
    ]))
    story.append(path_tbl)
    story.append(P("Table 4.1 — CSRF Attack Tree: Attack Paths and Countermeasures", styles["caption"]))

    story.append(Spacer(1, 0.5*cm))

    story.append(P("Attack Tree Diagram — CSRF", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.2*cm))

    csrf_tree = """\
GOAL: Perform Unauthorised Action as Victim (CSRF)
    [VICTIM IS AUTHENTICATED IN ANOTHER BROWSER TAB]
    │
    ├── [A] Trick victim into clicking crafted GET delete link
    │       └── Countermeasure: DELETE endpoint requires HTTP POST method
    │           └── RESULT: HTTP 405 Method Not Allowed ✗
    │
    ├── [B] Embed hidden form on attacker site, auto-submit POST
    │       └── Countermeasure: Flask-WTF generates per-session CSRF token
    │           └── Token missing → rejected before processing
    │               └── RESULT: HTTP 400 Bad Request ✗
    │
    └── [C] Same-site subdomain cookie theft (subdomain takeover)
            └── Countermeasure: SameSite=Strict on session cookie
                └── Browser refuses to send cookie on cross-site request
                    └── RESULT: Request unauthenticated → rejected ✗

    ALL ATTACK PATHS BLOCKED — THREAT MITIGATED"""

    csrf_tree_data = [[csrf_tree]]
    csrf_tree_tbl = Table(csrf_tree_data, colWidths=[page_w - 4*cm])
    csrf_tree_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F7F9FB")),
        ("FONTNAME",      (0, 0), (-1, -1), "Courier"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("BOX",           (0, 0), (-1, -1), 1.5, MID_BLUE),
        ("LINEAFTER",     (0, 0), (0, -1),  3, GREEN),
    ]))
    story.append(csrf_tree_tbl)

    story.append(Spacer(1, 0.4*cm))
    story.append(P(
        "<b>Defence-in-Depth:</b> SecureVault employs three independent CSRF countermeasures "
        "that together provide defence-in-depth. Even if one control is bypassed (e.g., an "
        "attacker finds a GET-based state change), the CSRF token and SameSite cookie attribute "
        "serve as additional independent layers of protection.",
        styles["body"]))

    story.append(PageBreak())
    return story


# ── Section 5: CVSS ───────────────────────────────────────────────────────────
def build_cvss(styles, page_w):
    story = []
    story.append(SectionBanner("SECTION 5 — CVSS v3.1 RISK ASSESSMENT", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.3*cm))

    intro = (
        "CVSS (Common Vulnerability Scoring System) v3.1 provides a standardised numerical "
        "score (0.0–10.0) representing the severity of a vulnerability. Scores are derived from "
        "Base Metrics covering Attack Vector (AV), Attack Complexity (AC), Privileges Required "
        "(PR), User Interaction (UI), Scope (S), Confidentiality (C), Integrity (I), and "
        "Availability (A) impacts."
    )
    story.append(P(intro, styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    # CVSS scoring ranges legend
    ranges = [
        ("None",     "0.0",       HexColor("#AAAAAA"), WHITE),
        ("Low",      "0.1–3.9",   HexColor("#4A9E4A"), WHITE),
        ("Medium",   "4.0–6.9",   ORANGE,              WHITE),
        ("High",     "7.0–8.9",   RED,                 WHITE),
        ("Critical", "9.0–10.0",  HexColor("#8B0000"), WHITE),
    ]
    range_data = [[
        P(f"{sev}\n{rng}", ParagraphStyle(f"rng_{sev}", fontName="Helvetica-Bold",
                                          fontSize=8, textColor=fg,
                                          alignment=TA_CENTER, leading=11))
        for sev, rng, bg, fg in ranges
    ]]
    range_colors = [("BACKGROUND", (i, 0), (i, 0), ranges[i][2]) for i in range(5)]
    range_tbl = Table(range_data, colWidths=[(page_w - 4*cm) / 5] * 5)
    range_tbl.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BOX",           (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, WHITE),
    ] + range_colors))
    story.append(range_tbl)
    story.append(P("CVSS v3.1 Severity Rating Scale", styles["caption"]))
    story.append(Spacer(1, 0.3*cm))

    # Main CVSS table
    cvss_threats = [
        # TID, Name, Vector String, Score, Severity
        ("T2",  "IDOR",
         "AV:N / AC:L / PR:L / UI:N / S:U / C:H / I:H / A:N",
         "8.1", "HIGH"),
        ("T5",  "CSRF",
         "AV:N / AC:L / PR:N / UI:R / S:U / C:N / I:H / A:N",
         "6.5", "MEDIUM"),
        ("T6",  "Clickjacking",
         "AV:N / AC:L / PR:N / UI:R / S:U / C:L / I:H / A:N",
         "6.1", "MEDIUM"),
        ("T1",  "Brute-force",
         "AV:N / AC:H / PR:N / UI:N / S:U / C:H / I:N / A:N",
         "5.9", "MEDIUM"),
        ("T4",  "DB Disclosure",
         "AV:L / AC:L / PR:H / UI:N / S:U / C:H / I:N / A:N",
         "4.4", "MEDIUM"),
        ("T7",  "Key in Git",
         "AV:N / AC:L / PR:N / UI:N / S:U / C:H / I:N / A:N",
         "7.5", "HIGH"),
    ]

    # Sort by score descending
    cvss_threats.sort(key=lambda x: float(x[3]), reverse=True)

    cvss_headers = ["ID", "Threat Name", "CVSS v3.1 Vector String", "Score", "Severity", "Risk Bar"]
    cvss_col_w = [1.0*cm, 2.5*cm, 6.5*cm, 1.2*cm, 1.8*cm, 2.6*cm]

    cvss_data = [[P(h, styles["table_header"]) for h in cvss_headers]]
    row_extra_styles = []

    def sev_colors(sev, score):
        s = float(score)
        if s >= 7.0:
            return PALE_RED, RED
        elif s >= 4.0:
            return PALE_ORANGE, ORANGE
        else:
            return PALE_GREEN, GREEN

    def score_bar(score):
        s = float(score)
        filled = int(s)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        return bar

    for i, (tid, name, vector, score, sev) in enumerate(cvss_threats):
        bg, fg = sev_colors(sev, score)
        bar = score_bar(score)
        row = [
            cell_para(f"<b>{tid}</b>", styles, center=True),
            cell_para(f"<b>{name}</b>", styles),
            cell_para(vector, styles),
            P(score, ParagraphStyle("sc", fontName="Helvetica-Bold", fontSize=9,
                                    textColor=fg, leading=11, alignment=TA_CENTER)),
            P(sev, ParagraphStyle("sv", fontName="Helvetica-Bold", fontSize=8,
                                   textColor=fg, leading=10, alignment=TA_CENTER)),
            P(f'<font color="#{"%02x%02x%02x" % (fg.red*255, fg.green*255, fg.blue*255)}">{bar}</font>',
              ParagraphStyle("bar", fontName="Courier", fontSize=7.5,
                             leading=10, alignment=TA_CENTER)),
        ]
        cvss_data.append(row)
        row_num = i + 1
        row_extra_styles.append(("BACKGROUND", (3, row_num), (4, row_num), bg))
        if i % 2 == 0:
            row_extra_styles.append(("BACKGROUND", (0, row_num), (2, row_num), WHITE))
            row_extra_styles.append(("BACKGROUND", (5, row_num), (5, row_num), WHITE))
        else:
            row_extra_styles.append(("BACKGROUND", (0, row_num), (2, row_num), LIGHT_GRAY))
            row_extra_styles.append(("BACKGROUND", (5, row_num), (5, row_num), LIGHT_GRAY))

    cvss_tbl = Table(cvss_data, colWidths=cvss_col_w, repeatRows=1)
    cvss_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, DARK_NAVY),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (0, -1),  "CENTER"),
        ("ALIGN",         (3, 0), (5, -1),  "CENTER"),
    ] + row_extra_styles))

    story.append(cvss_tbl)
    story.append(P("Table 5.1 — CVSS v3.1 Risk Assessment (sorted by score, highest first)", styles["caption"]))

    story.append(Spacer(1, 0.5*cm))

    # CVSS Breakdown details
    story.append(P("5.1  Metric Breakdown — Top Threats", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.2*cm))

    breakdown_rows = [
        ["Metric", "T2 IDOR", "T7 Key in Git", "T5 CSRF", "T6 Clickjacking"],
        ["Attack Vector (AV)",         "Network", "Network",  "Network",  "Network"],
        ["Attack Complexity (AC)",      "Low",     "Low",      "Low",      "Low"],
        ["Privileges Required (PR)",    "Low",     "None",     "None",     "None"],
        ["User Interaction (UI)",       "None",    "None",     "Required", "Required"],
        ["Scope (S)",                   "Unchanged","Unchanged","Unchanged","Unchanged"],
        ["Confidentiality Impact (C)",  "High",    "High",     "None",     "Low"],
        ["Integrity Impact (I)",        "High",    "None",     "High",     "High"],
        ["Availability Impact (A)",     "None",    "None",     "None",     "None"],
        ["CVSS Score",                  "8.1",     "7.5",      "6.5",      "6.1"],
    ]

    breakdown_col_w = [4.0*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm]
    breakdown_data = [
        [P(c, styles["table_header"]) for c in breakdown_rows[0]]
    ] + [
        [cell_para(c, styles, center=(j > 0)) for j, c in enumerate(row)]
        for row in breakdown_rows[1:]
    ]

    breakdown_tbl = Table(breakdown_data, colWidths=breakdown_col_w, repeatRows=1)
    score_row = len(breakdown_rows) - 1
    breakdown_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -2), [WHITE, LIGHT_GRAY]),
        ("BACKGROUND",    (0, score_row), (-1, score_row), DARK_NAVY),
        ("TEXTCOLOR",     (0, score_row), (-1, score_row), WHITE),
        ("FONTNAME",      (0, score_row), (-1, score_row), "Helvetica-Bold"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
    ]))
    story.append(breakdown_tbl)
    story.append(P("Table 5.2 — CVSS Metric Breakdown for Top 4 Threats", styles["caption"]))

    story.append(PageBreak())
    return story


# ── Section 6: Summary & Recommendations ─────────────────────────────────────
def build_summary(styles, page_w):
    story = []
    story.append(SectionBanner("SECTION 6 — SUMMARY & RECOMMENDATIONS", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.3*cm))

    story.append(P("6.1  Overall Risk Posture", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.2*cm))

    summary_stats = [
        ["Metric", "Value"],
        ["Total Threats Identified", "10"],
        ["Fully Mitigated",          "9 (90%)"],
        ["Partially Mitigated",      "1 (10%) — T3 Repudiation"],
        ["Unmitigated",              "0"],
        ["Highest CVSS Score",       "8.1 HIGH — T2 IDOR"],
        ["Average CVSS Score",       "6.4 MEDIUM"],
        ["CI/CD Security Tools",     "Bandit, CodeQL, OWASP ZAP, Safety"],
    ]

    stats_col_w = [(page_w - 4*cm) * 0.5, (page_w - 4*cm) * 0.5]
    stats_data = [
        [P(c, styles["table_header"]) for c in summary_stats[0]]
    ] + [
        [cell_para(r[0], styles), cell_para(r[1], styles)]
        for r in summary_stats[1:]
    ]
    stats_tbl = Table(stats_data, colWidths=stats_col_w)
    stats_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        ("FONTNAME",      (0, 2), (0, 2),   "Helvetica-Bold"),
        ("TEXTCOLOR",     (0, 2), (1, 2),   ORANGE),  # partial row
    ]))
    story.append(stats_tbl)
    story.append(Spacer(1, 0.4*cm))

    story.append(P("6.2  Recommendations", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.2*cm))

    recs = [
        ("HIGH",   "Implement Audit Log (T3)",
         "Add an audit_log table to record create/update/delete events with user ID, timestamp, "
         "and entry ID. This fully mitigates the Repudiation threat and supports forensic investigation."),
        ("MEDIUM", "Enforce Account Lockout (T1)",
         "Implement rate limiting (Flask-Limiter) on the login endpoint to complement bcrypt's "
         "inherent slowness. Suggested: 5 attempts → 15-minute lockout with exponential back-off."),
        ("MEDIUM", "Add Security Headers Middleware (T6)",
         "Centralise all security headers (X-Frame-Options, CSP, HSTS, X-Content-Type-Options) "
         "in a Flask after_request hook to ensure consistent application across all responses."),
        ("LOW",    "Rotate Fernet Key (T4/T7)",
         "Implement a key rotation procedure using Fernet.MultiFernet to support periodic key "
         "rotation without service interruption, reducing the impact of key compromise."),
        ("LOW",    "Dependency Pinning (T9)",
         "Pin all dependencies to exact versions in requirements.txt and use Dependabot or "
         "Renovate Bot to automate PR creation for dependency updates after CI/CD validation."),
    ]

    rec_col_w = [1.5*cm, 3.5*cm, page_w - 4*cm - 5.0*cm]
    rec_data = [[P(h, styles["table_header"]) for h in ["Priority", "Recommendation", "Description"]]]
    prio_colors = {"HIGH": (PALE_RED, RED), "MEDIUM": (PALE_ORANGE, ORANGE), "LOW": (LIGHT_BLUE, MID_BLUE)}

    for i, (prio, title, desc) in enumerate(recs):
        bg, fg = prio_colors[prio]
        rec_data.append([
            P(prio, ParagraphStyle(f"pr{i}", fontName="Helvetica-Bold", fontSize=7.5,
                                   textColor=fg, leading=10, alignment=TA_CENTER)),
            cell_para(f"<b>{title}</b>", styles),
            cell_para(desc, styles),
        ])
    rec_tbl = Table(rec_data, colWidths=rec_col_w, repeatRows=1)
    extra = [("BACKGROUND", (0, i+1), (0, i+1), prio_colors[recs[i][0]][0]) for i in range(len(recs))]
    rec_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0),  (-1, 0),  DARK_NAVY),
        ("ROWBACKGROUNDS",(0, 1),  (-1, -1), [WHITE, LIGHT_GRAY]),
        ("TOPPADDING",    (0, 0),  (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0),  (-1, -1), 7),
        ("LEFTPADDING",   (0, 0),  (-1, -1), 6),
        ("GRID",          (0, 0),  (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0),  (-1, -1), 1.5, DARK_NAVY),
        ("VALIGN",        (0, 0),  (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0),  (0, -1),  "CENTER"),
    ] + extra))
    story.append(rec_tbl)
    story.append(P("Table 6.1 — Security Recommendations", styles["caption"]))

    story.append(Spacer(1, 0.5*cm))

    story.append(P("6.3  CI/CD Security Pipeline", styles["section_h2"]))
    story.append(AccentLine(page_w - 4*cm, MID_BLUE, 1))
    story.append(Spacer(1, 0.2*cm))

    cicd_text = """\
GitHub Actions Pipeline — Security Gates:

  git push ──► GitHub Actions Triggered
                │
                ├── [1] Bandit (SAST)    ── Python static analysis for security bugs
                ├── [2] CodeQL           ── Deep semantic vulnerability detection
                ├── [3] Safety           ── Dependency CVE check (PyPI advisories)
                └── [4] OWASP ZAP (DAST) ── Dynamic web app scanning (active scan)

  All gates must PASS before merge to main branch is permitted."""

    cicd_data = [[cicd_text]]
    cicd_tbl = Table(cicd_data, colWidths=[page_w - 4*cm])
    cicd_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#0D1B2A")),
        ("TEXTCOLOR",     (0, 0), (-1, -1), HexColor("#B0C4D8")),
        ("FONTNAME",      (0, 0), (-1, -1), "Courier"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("BOX",           (0, 0), (-1, -1), 1.5, ACCENT),
    ]))
    story.append(cicd_tbl)

    story.append(PageBreak())
    return story


# ── Final page: Conclusion ────────────────────────────────────────────────────
def build_conclusion(styles, page_w):
    story = []
    story.append(SectionBanner("CONCLUSION", page_w - 4*cm, DARK_NAVY))
    story.append(Spacer(1, 0.4*cm))

    conclusion_paras = [
        ("Threat Modelling Outcome",
         "This threat model demonstrates that SecureVault has been designed with security as a "
         "first-class concern throughout the development lifecycle. Applying the STRIDE methodology "
         "identified 10 distinct threats across authentication, session management, data storage, "
         "client-side attacks, and the software supply chain."),
        ("Mitigation Coverage",
         "Nine of the ten identified threats are fully mitigated through implemented security "
         "controls. The remaining threat (T3 — Repudiation/Audit Log) is partially addressed "
         "through record timestamps and has a clear remediation path via audit log implementation."),
        ("Risk-Based Prioritisation",
         "CVSS v3.1 scoring enabled risk-based prioritisation. The highest-severity finding "
         "(T2 — IDOR, score 8.1 HIGH) is fully mitigated by consistent ownership verification. "
         "The CI/CD pipeline integrates four security scanning tools ensuring continuous security "
         "validation on every code push."),
        ("Compliance with DevSecOps Principles",
         "SecureVault's development approach aligns with DevSecOps principles by integrating "
         "security testing (Bandit, CodeQL, ZAP, Safety) directly into the GitHub Actions pipeline, "
         "ensuring security is not an afterthought but an integral part of the build process."),
    ]

    for title, text in conclusion_paras:
        story.append(P(f"<b>{title}</b>", styles["section_h2"]))
        story.append(P(text, styles["body"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(AccentLine(page_w - 4*cm, ACCENT, 2))
    story.append(Spacer(1, 0.4*cm))

    # Signature block
    sig_rows = [["Team Member", "Student ID", "Signature"]]
    members = [
        ("Daniyal Ahmed",       "SP23-BCT-011"),
        ("Shaheer Khalid",      "SP23-BCT-048"),
        ("Maaz Malik",          "SP23-BCT-025"),
        ("Rana Mutahhar Ahmed", "SP23-BCT-045"),
    ]
    for name, sid in members:
        sig_rows.append([name, sid, "_" * 30])

    sig_col_w = [(page_w - 4*cm) / 3] * 3
    sig_data = [
        [P(h, styles["table_header"]) for h in sig_rows[0]]
    ] + [
        [cell_para(c, styles, center=(i > 0)) for i, c in enumerate(row)]
        for row in sig_rows[1:]
    ]
    sig_tbl = Table(sig_data, colWidths=sig_col_w)
    sig_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
    ]))
    story.append(P("Declaration: We certify that this threat model represents our own original analysis.", styles["body"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(sig_tbl)
    story.append(Spacer(1, 0.4*cm))

    footer_data = [["SecureVault Threat Model  |  CYC386  |  Engr. Muhammad Ahmad Nawaz  |  April 8, 2026"]]
    footer_tbl = Table(footer_data, colWidths=[page_w - 4*cm])
    footer_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), DARK_NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, -1), HexColor("#7F8C8D")),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 7.5),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(footer_tbl)
    return story


# ── Page template callbacks ───────────────────────────────────────────────────
def on_first_page(canvas, doc):
    pass  # cover page handles its own layout


def on_later_pages(canvas, doc):
    canvas.saveState()
    page_w, page_h = A4

    # Header bar
    canvas.setFillColor(DARK_NAVY)
    canvas.rect(1.5*cm, page_h - 1.3*cm, page_w - 3*cm, 0.7*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawString(1.7*cm, page_h - 0.95*cm, "THREAT MODEL — SecureVault Password Vault")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(page_w - 1.7*cm, page_h - 0.95*cm, "CYC386  |  Secure Software Design and Development")

    # Accent line under header
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(1.5*cm, page_h - 1.3*cm, page_w - 1.5*cm, page_h - 1.3*cm)

    # Footer
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(1.5*cm, 1.4*cm, page_w - 1.5*cm, 1.4*cm)
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(1.5*cm, 0.9*cm, "SecureVault  |  Team: Daniyal Ahmed · Shaheer Khalid · Maaz Malik · Rana Mutahhar Ahmed")
    canvas.setFont("Helvetica-Bold", 7)
    canvas.drawRightString(page_w - 1.5*cm, 0.9*cm, f"Page {doc.page}")
    canvas.restoreState()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    page_w, page_h = A4
    styles = make_styles()

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=1.6*cm,
        bottomMargin=1.8*cm,
        title="Threat Model — SecureVault Password Vault",
        author="SecureVault Team — CYC386",
        subject="STRIDE + DFD + Attack Tree + CVSS v3.1",
    )

    story = []
    story += build_cover(styles, page_w, page_h)
    story += build_toc(styles, page_w)
    story += build_dfd(styles, page_w)
    story += build_stride(styles, page_w)
    story += build_attack_tree_idor(styles, page_w)
    story += build_attack_tree_csrf(styles, page_w)
    story += build_cvss(styles, page_w)
    story += build_summary(styles, page_w)
    story += build_conclusion(styles, page_w)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF generated successfully: {OUTPUT_PATH}")
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
