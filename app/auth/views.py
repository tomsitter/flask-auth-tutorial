from flask import Blueprint, session, g, render_template, redirect, url_for, flash
from app.auth.forms import RegistrationForm, LoginForm
from app import db
from app.models import User
from werkzeug.local import Local, LocalProxy

auth = Blueprint('auth', __name__, template_folder='templates')

current_user = LocalProxy(lambda: get_current_user())

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

        user = User(username, email, password, location, description) # add the rest
        db.session.add(user)
        db.session.commit()
        flash("You are registered", "success")
        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)

@auth.route("/logout")
def logout():
    if current_user.is_anonymous():
        flash("You are not logged in", "danger")
    else:
        logout_user()
        flash("You are logged out", "success")
        return redirect(url_for("main.home"))

def logout_user():
    session.pop("user_id")

def login_user(user):
    session["user_id"] = user.id

@auth.app_context_processor
def inject_current_user():
    return dict(current_user=get_current_user())

def get_current_user():
    _current_user = getattr(g, "_current_user", None)
    if _current_user is None:
        if session.get("user_id"):
            user = User.query.get(session.get("user_id"))
            if user:
                _current_user = g._current_user = user
        
    if _current_user is None:
        _current_user = User()

    return _current_user