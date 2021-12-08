from flask import Blueprint, render_template, session
from app.models import User

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def home():
    users = User.query.all()
    logged_in_user = None

    if session.get("user_id"):
        logged_in_user = User.query.get(session.get("user_id"))

    return render_template('home/home.html', users=users, logged_in_user=logged_in_user)