from flask import Blueprint, render_template, redirect, url_for, flash
from functools import wraps
from app.auth.views import current_user
from app.models import User, Role

admin = Blueprint("admin", __name__, template_folder='/templates')

def admin_required(f):
    @wraps(f)
    def _admin_required(*args, **kwargs):
        if not current_user.is_admin():
            flash("You need to be admin to access this page", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return _admin_required(f)