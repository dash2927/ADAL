from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

import re


class User(UserMixin, db.Model):
    '''
    database table for user
    '''
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(32), nullable=False)
    _pwdhash = db.Column(db.String(64), nullable=False)
    _email = db.Column(db.String(64), unique=True)
    posts = db.Column(db.Integer, default=0)
    upvotes = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.current_timestamp())

    def __init__(self, name, pword):
        self.uname = name
        self.password = pword

    @property
    def username(self):
        return self.uname

    @username.setter
    def username(self, name):
        self.uname = name

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
        if(re.fullmatch(r'^[A-Za-z0-9\._-]+@[A-Za-z0-9]+\.[A-Za-z]{2,}$', email)):
            self._email = email
        else:
            raise ValueError("invalid email address")

    def verify_pwd(self, pwd):
        return check_password_hash(self._pwdhash, pwd)


class Post(db.Model):
    '''
    database table for recipe posts
    '''
    __tablename__ = "post"
    postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('userinfo.id'),
                          nullable=False)
    # One-to-one relationship with userinfo.id
    author = db.relationship("User", backref=db.backref("userinfo",
                                                        uselist=False))
    upvotes = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.current_timestamp())
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

