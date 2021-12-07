from flask import Blueprint, render_template, redirect, url_for, flash
from app.auth.forms import RegistrationForm
from app import db
from app.models import User

auth = Blueprint('auth', __name__, template_folder='templates')

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