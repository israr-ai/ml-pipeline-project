import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from src.auth.forms import ForgotPasswordForm, LoginForm, ResetPasswordForm, SignupForm
from src.models_db import User, db

auth_bp = Blueprint("auth", __name__)

RESET_TOKEN_TTL = timedelta(hours=1)


def _utcnow_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))

    return render_template("signup.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc:
                next_page = url_for("index")
            return redirect(next_page)
        form.password.errors.append("Invalid email or password.")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = ForgotPasswordForm()
    reset_url = None
    not_found = False

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.reset_token = secrets.token_urlsafe(32)
            user.reset_token_expires_at = _utcnow_naive() + RESET_TOKEN_TTL
            db.session.commit()
            reset_url = url_for("auth.reset_password", token=user.reset_token, _external=True)
        else:
            not_found = True

    return render_template("forgot_password.html", form=form, reset_url=reset_url, not_found=not_found)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expires_at is None or user.reset_token_expires_at < _utcnow_naive():
        return render_template("reset_password.html", form=None, invalid=True)

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        user.reset_token = None
        user.reset_token_expires_at = None
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form, invalid=False)
