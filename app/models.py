from enum import unique
from operator import truediv
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe

def generate_token():
    return token_urlsafe(20)

def generate_hash(token):
    return generate_password_hash(token)

def _check_token(hash, token):
    return check_password_hash(hash, token)


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

    def __init__(self, username="", email="", password="", location="", description=""):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.location = location
        self.description = description

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