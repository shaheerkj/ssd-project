from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL
from app import db
from app.models import VaultEntry

vault_bp = Blueprint("vault", __name__, url_prefix="/vault")


# ── Forms ─────────────────────────────────────────────────────────────────────

class VaultEntryForm(FlaskForm):
    site_name = StringField("Site Name", validators=[DataRequired(), Length(1, 200)])
    site_url = StringField("Site URL", validators=[Optional(), URL(), Length(max=500)])
    username = StringField("Username / Email", validators=[DataRequired(), Length(1, 200)])
    password = PasswordField("Password", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Save")


# ── Helper: IDOR-safe lookup ──────────────────────────────────────────────────

def get_entry_or_403(entry_id: int) -> VaultEntry:
    """
    IDOR Fix: Fetch vault entry by ID and verify it belongs to the
    currently authenticated user.  Returns 403 if ownership check fails,
    preventing any user from accessing another user's entries by guessing IDs.
    """
    entry = db.session.get(VaultEntry, entry_id)
    if entry is None:
        abort(404)
    if entry.user_id != current_user.id:   # <-- ownership check
        abort(403)
    return entry


# ── Routes ────────────────────────────────────────────────────────────────────

@vault_bp.route("/")
@login_required
def dashboard():
    entries = VaultEntry.query.filter_by(user_id=current_user.id).order_by(
        VaultEntry.site_name
    ).all()
    return render_template("dashboard.html", entries=entries)


@vault_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_entry():
    form = VaultEntryForm()
    if form.validate_on_submit():
        entry = VaultEntry(
            user_id=current_user.id,
            site_name=form.site_name.data,
            site_url=form.site_url.data or None,
            username=form.username.data,
            notes=form.notes.data or None,
        )
        entry.set_password(form.password.data)
        db.session.add(entry)
        db.session.commit()
        flash(f'Entry for "{entry.site_name}" added.', "success")
        return redirect(url_for("vault.dashboard"))
    return render_template("entry_form.html", form=form, title="Add Entry")


@vault_bp.route("/view/<int:entry_id>")
@login_required
def view_entry(entry_id: int):
    entry = get_entry_or_403(entry_id)           # IDOR fix applied
    plaintext = entry.get_password()
    return render_template("view_entry.html", entry=entry, plaintext=plaintext)


@vault_bp.route("/edit/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id: int):
    entry = get_entry_or_403(entry_id)           # IDOR fix applied
    form = VaultEntryForm(obj=entry)
    if form.validate_on_submit():
        entry.site_name = form.site_name.data
        entry.site_url = form.site_url.data or None
        entry.username = form.username.data
        entry.notes = form.notes.data or None
        entry.set_password(form.password.data)
        db.session.commit()
        flash(f'Entry for "{entry.site_name}" updated.', "success")
        return redirect(url_for("vault.dashboard"))
    # Pre-fill password field with decrypted value for editing
    form.password.data = entry.get_password()
    return render_template("entry_form.html", form=form, title="Edit Entry", entry=entry)


@vault_bp.route("/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id: int):
    """
    Delete uses POST (not GET) so it cannot be triggered by a simple link/image
    load (CSRF vector).  Flask-WTF CSRF token is validated automatically on POST.
    IDOR fix is also applied.
    """
    entry = get_entry_or_403(entry_id)           # IDOR fix applied
    db.session.delete(entry)
    db.session.commit()
    flash(f'Entry for "{entry.site_name}" deleted.', "success")
    return redirect(url_for("vault.dashboard"))
