from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import bcrypt
import re

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.Integer, nullable=False)
    _pwdhash = db.Column(db.String(64), nullable=False)
    _email = db.Column(db.String(64), unique=True)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.current_timestamp())

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, name):
        self._username = name

    @property
    def password(self):
        raise ValueError("ERROR: Password is not retreivable")

    @password.setter
    def password(self, pwd):
        self._pwdhash = generate_password_hash(pwd)

    @property
    def email(self):
        raise ValueError("Error: Email is not retreivable")

    @email.setter
    def email(self, email):
        if(re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]\.[A-Za-z]$')):
            self._email = email
        else:
            raise ValueError("invalid email address")

    def verify_pwd(self, pwd):
        return check_password_hash(self._pwdhash, pwd)


class Post(db.Model):
    __tablename__ = "post"
    postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('userinfo.id'),
                          nullable=False)
    # One-to-one relationship with userinfo.id
    author = db.relationship("User", backref=db.backref("userinfo",
                                                        uselist=False))

    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.current_timestamp())
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
