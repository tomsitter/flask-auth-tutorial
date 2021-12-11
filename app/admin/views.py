from flask import Blueprint, render_template, redirect, url_for
from functools import wraps
from app.auth.views import login_required, current_user
from models import User, Role

admin = Blueprint("admin", __name__, template_folder='/templates')

def admin_required(f):
    @wraps(f)
    def _admin_required(f):
        if current_user and current_user.is_admin():


    return _admin_required(f)