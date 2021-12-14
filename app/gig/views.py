from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
from werkzeug.utils import escape
from app.models import Gig, Role
from app import db
from app.auth.views import current_user, login_required, role_required
from app.gig.forms import CreateGigForm, UpdateGigForm
from functools import wraps

gig = Blueprint("gig", __name__, template_folder="templates")


def gig_owner_required(f):
    @wraps(f)
    def _gig_owner_required(*args, **kwargs):
        gig = Gig.query.filter_by(slug=request.view_args["slug"]).first()
        if not gig or not current_user.is_gig_owner(gig):
            flash("You are not the owner of that gig.", "danger")
            return redirect(url_for("main.home"))
        return f("8args, **kwargs")
    return _gig_owner_required


@gig.route('/create', methods=['GET', 'POST'])
@login_required
@role_required(Role.EMPLOYER)
def create():
    form = CreateGigForm()

    if form.validate_on_submit():
        title =         escape(form.title.data)
        description =   escape(form.description.data)
        payment =       form.payment.data
        location =      escape(form.location.data)

        gig = Gig(title, description, payment, location, current_user.id)
        db.session.add(gig)
        db.session.commit()
        flash(f"The new gig has been add. \"{gig.title}\"", "success")
        return redirect(url_for("gig.show", slug=gig.slug))
        
    return render_template("create_gig.html", form=form)

@gig.route('/edit/<slug>', methods=['GET', 'POST'])
@login_required
@role_required(Role.EMPLOYER)
@gig_owner_required
def edit(slug):
    form = UpdateGigForm()
    
    gig = Gig.query.filter_by(slug=slug).first()

    if form.validate_on_submit():
        gig.title       = escape(form.title.data)
        gig.description = escape(form.description.data)
        gig.payment     = form.payment.data
        gig.location    = escape(form.location.data)

        db.session.add(gig)
        db.session.commit()
        flash(f"The gig has been updated. \"{gig.title}\"", "success")
        return redirect(url_for("gig.show", slug=gig.slug))

    form.title.data = gig.title
    form.description.data = gig.description
    form.payment.data = gig.payment
    form.location.data = gig.location        
    return render_template("edit_gig.html", gig=gig, form=form)


@gig.route("/info/<slug>")
@login_required
def show(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)
    musicians = gig.musicians.all()
    return render_template("show_gig.html", gig=gig, musicians=musicians)


@gig.route('/delete/<slug>', methods=['POST'])
@login_required
@role_required(Role.EMPLOYER)
@gig_owner_required
def delete(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)
    db.session.delete(gig)
    db.session.commit()
    flash("The gig is deleted", "success")
    return redirect(url_for("main.home"))

@gig.route('/my_gigs')
@login_required
def my_gigs():
    gigs = None
    if current_user.is_admin():
        return redirect(url_for("admin.gigs"))
    if current_user.is_role(Role.MUSICIAN):
        gigs = current_user.applied_gigs.all()
    if current_user.is_role(Role.EMPLOYER):
        gigs = current_user.gigs.all()

    return render_template("my_gigs.html", gigs=gigs)



@gig.route('/apply/<slug>', methods=['POST'])
def apply(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)

    current_user.apply(gig)
    db.session.commit()

    flash(f"You applied to the gig: \"{gig.title}\"", "success")
    return redirect(request.referrer)

@gig.route("/cancel_application/<slug>", methods=['POST'])
def cancel_application(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)

    current_user.unapply(gig)
    db.session.commit()

    flash(f"You unapplied from the gig: \"{gig.title}\"", "success")
    return redirect(request.referrer)