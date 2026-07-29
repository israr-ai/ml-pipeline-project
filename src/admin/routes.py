from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user
from flask_wtf.csrf import generate_csrf, validate_csrf
from wtforms import ValidationError

from src.analytics.aggregations import build_dashboard_data
from src.auth.decorators import admin_required
from src.models_db import Prediction, User, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("")
@admin_required
def dashboard():
    predictions = Prediction.query.all()
    dashboard_data = build_dashboard_data(predictions)
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template(
        "admin.html",
        dashboard_data=dashboard_data,
        users=users,
        csrf_token=generate_csrf(),
    )


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    try:
        validate_csrf(request.form.get("csrf_token"))
    except ValidationError:
        abort(400)

    if user_id == current_user.id:
        abort(400)

    user = db.session.get(User, user_id)
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))
