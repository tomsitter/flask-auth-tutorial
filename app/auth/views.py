from flask import Blueprint, session, render_template, redirect, url_for, flash
from app.auth.forms import RegistrationForm, LoginForm
from app import db
from app.models import User

auth = Blueprint('auth', __name__, template_folder='templates')


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
        flash("You are reigstered", "success")
        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)

@auth.route("/logout")
def logout():
    if not session.get("user_id"):
        flash("You are not logged in", "danger")
    else:
        logout_user()
        flash("You are logged out", "success")
        return redirect(url_for("main.home"))

def logout_user():
    session.pop("user_id")

def login_user(user):
    session["user_id"] = user.id
