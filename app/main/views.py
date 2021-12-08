from flask import Blueprint, render_template, session
from app.models import User

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def home():
    users = User.query.all()
    return render_template('home/home.html', users=users)