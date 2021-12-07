from enum import unique
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.Text(), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

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