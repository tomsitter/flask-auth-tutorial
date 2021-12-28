from flask import Blueprint, render_template, session
from app.models import User, Role, Gig
from app.auth.views import current_user

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def home():
    gigs = None
    musicians = None
    if current_user.is_role(Role.MUSICIAN):
        gigs = Gig.query.all()
    if current_user.is_role(Role.EMPLOYER):
        musicians = User.query.filter_by(role_id=Role.MUSICIAN).all()
    return render_template('home.html', gigs=gigs, musicians=musicians)