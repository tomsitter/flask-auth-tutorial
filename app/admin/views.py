from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from functools import wraps
from app.auth.views import current_user, admin_required, login_required
from app.models import User, Gig
from app import db

admin = Blueprint("admin", __name__, template_folder='templates')

@admin.before_request
@login_required
@admin_required
def check_admin_in_each_view():
    print(f"Admin {current_user.username} access {request.url}")

@admin.route('/gigs')
def gigs():
    gigs = Gig.query.all()
    return render_template('all_gigs.html', gigs=gigs)

@admin.route('/users')
def users():
    users = User.query.all()
    return render_template('all_users.html', users=users)

@admin.route('/delete_gig/<int:gig_id>', methods=['POST'])
def delete_gig(gig_id):
    gig = Gig.query.get(gig_id)
    if gig:
        flash(f"Gig \"{gig.title}\" is deleted", "success")
        db.session.delete(gig)
        db.session.commit()
    
    if "gig/info" in request.referrer:
        return redirect(url_for("admin.gigs"))
    else:
        return redirect(request.referrer)


@admin.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        flash(f"USer \"{user.username}\" is deleted", "success")
        db.session.delete(user)
        db.session.commit()
    
    if "user/profile" in request.referrer:
        return redirect(url_for("admin.users"))
    else:
        return redirect(request.referrer)
