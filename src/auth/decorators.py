from functools import wraps

from flask import abort
from flask_login import current_user, login_required

from src.models_db import UserRole


def admin_required(view):
    @login_required
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user.role != UserRole.ADMIN:
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view
