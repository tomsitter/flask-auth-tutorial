from flask import Blueprint, current_app, session, g, render_template, redirect, url_for, flash, make_response, request
from app.auth.forms import RegistrationForm, LoginForm
from app import db
from app.models import User, Role
from werkzeug.local import LocalProxy
from itsdangerous.url_safe import URLSafeSerializer
from functools import wraps

auth = Blueprint('auth', __name__, template_folder='templates')

current_user = LocalProxy(lambda: get_current_user())

def login_required(f):
    @wraps(f)
    def _login_required(*args, **kwargs):
        if current_user.is_anonymous():
            flash("You need to be logged in to access this page", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return _login_required


def role_required(role):
    def _role_required(f):
        @wraps(f)
        def __role_required(*args, **kwargs):
            if not current_user.is_role(role):
                flash("You are not authorized to access this page", "danger")
                return redirect(url_for("main.home"))
            return f(*args, **kwargs)
        return __role_required
    return _role_required

def admin_required(f):
    @wraps(f)
    def _admin_required(*args, **kwargs):
        if not current_user.is_admin():
            flash("You need to be a logged in admin to access this page", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return _admin_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user.check_password(password):
            flash("You are successfully logged in.", "success")
            login_user(user)
            if form.remember_me.data:
                resp = make_response(redirect(url_for("main.home")))
                remember_token = user.create_remember_token()
                db.session.commit()
                resp.set_cookie('remember_token', encrypt_cookie(remember_token), max_age=60*60*24*100)
                resp.set_cookie('user_id', encrypt_cookie(user.id), max_age=60*60*24*100)
                return resp
            return redirect(url_for("main.home"))
        else:
            form.password.errors.append("Incorrect password")
    
    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        location = form.location.data
        description = form.description.data
        role = form.role.data

        user = User(username, email, password, location, description, role)
        db.session.add(user)
        db.session.commit()
        flash("You are registered", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    current_user.forget()
    db.session.commit()
    logout_user()

    # delete the remember cookies
    resp = make_response(redirect(url_for("main.home")))
    resp.set_cookie("remember_token", "", max_age=0)
    resp.set_cookie("user_id", "", max_age=0)

    flash("You are logged out", "success")
    return redirect(url_for("main.home"))

def logout_user():
    session.pop("user_id")

def login_user(user):
    session["user_id"] = user.id

def encrypt_cookie(content):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="saltedcookie")
    encrypted_content = s.dumps(content)
    return encrypted_content

def decrypt_cookie(encrypted_content):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="saltedcookie")
    try:
        content = s.loads(encrypted_content)
    except:
        content = "-1"
    return content

@auth.app_context_processor
def inject_current_user():
    return dict(current_user=get_current_user())

@auth.app_context_processor
def inject_roles():
    return dict(Role=Role)

def get_current_user():
    _current_user = getattr(g, "_current_user", None)
    if _current_user is None:
        if session.get("user_id"):
            user = User.query.get(session.get("user_id"))
            if user:
                _current_user = g._current_user = user
        elif request.cookies.get("user_id"):
            user = User.query.get(int(decrypt_cookie(request.cookies.get("user_id"))))
            if user and user.check_remember_token(decrypt_cookie(request.cookies.get("user_id"))):
                login_user(user)
                _current_user = g._current_user = user
        
    if _current_user is None:
        _current_user = User()

    return _current_user


