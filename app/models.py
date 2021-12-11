from enum import unique
from operator import truediv
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
from sqlalchemy import event
from slugify import slugify

def generate_token():
    return token_urlsafe(20)

def generate_hash(token):
    return generate_password_hash(token)

def _check_token(hash, token):
    return check_password_hash(hash, token)

class Role:
    ADMIN = 1
    MUSICIAN = 2
    EMPLOYER = 3

applications = db.Table("applications",
    db.Column("gig_id", db.Integer(), db.ForeignKey("gigs.id")),
    db.Column("musician_id", db.Integer(), db.ForeignKey("users.id"))
)

class Gig(db.Model):
    __tablename__ = "gigs"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    payment = db.Column(db.Float())
    location = db.Column(db.String(255))
    employer_id = db.Column(db.Integer(), db.ForeignKey("users.id"), index=True)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)

    def __init__(self, title, description, payment, location, employer_id):
        self.title = title
        self.description = description
        self.payment = payment
        self.location = location
        self.employer_id = employer_id

@event.listens_for(Gig.title, 'set')
def update_slug(target, value, old_value, initiator):
    target.slug = slugify(value) + "-" + token_urlsafe(3)

class Remember(db.Model):
    __tablename__ = "remembers"

    id = db.Column(db.Integer(), primary_key=True)
    remember_hash = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), index=True)

    def __init__(self, user_id: int):
        self.token = generate_token()
        self.remember_hash = generate_hash(self.token)
        self.user_id = user_id

    def check_token(self, token):
        return _check_token(self.remember_hash, token)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.Text(), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    remember_hashes = db.relationship("Remember", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    role_id = db.Column(db.Integer(), default=0)
    gigs = db.relationship("Gig", backref="employer", lazy="dynamic", cascade="all, delete-orphan")
    applied_gigs = db.relationship("Gig",
                        secondary=applications,
                        backref=db.backref("musicians", lazy="dynamic"),
                        lazy="dynamic")

    def __init__(self, username="", email="", password="", 
                    location="", description="", role_id=Role.ADMIN):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.location = location
        self.description = description
        self.role_id = role_id

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def password(self):
        raise AttributeError("Passwords should be be read like this")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return not "" == self.username

    def is_anonymous(self):
        return "" == self.username

    def create_remember_token(self):
        remember_instance = Remember(self.id)
        db.session.add(remember_instance)
        return remember_instance.token

    def check_remember_token(self, token):
        if token:
            for remember_hash in self.remember_hashes:
                if remember_hash.check_token(token):
                    return True
        return False

    def forget(self):
        self.remember_hashes.delete()

    def is_admin(self):
        return self.role_id == Role.ADMIN

    def is_role(self, role: Role):
        return self.role_id == role

    def is_gig_owner(self, gig):
        return self.id == gig.employer_id
        
    def is_applied_to(self, gig):
        if gig is None:
            return False
        return self.applied_gigs.filter_by(id=gig.id).first() is not None

    def apply(self, gig):
        if not self.is_applied_to(gig):
            self.applied_gigs.append(gig)
            db.session.add(self)