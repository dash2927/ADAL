from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

import re, boto3, os, hashlib, json


class User(UserMixin, db.Model):
    '''
    database table for user
    '''
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(32), nullable=False)
    _pwdhash = db.Column(db.String(128), nullable=False)
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
        raise ValueError("ERROR: Email is not retreivable")

    @email.setter
    def email(self, email):
        if(re.fullmatch(r'^[A-Za-z0-9\._-]+@[A-Za-z0-9]+\.[A-Za-z]{2,}$',
                        email)):
            self._email = email
        else:
            raise ValueError("Invalid email address.")

    def verify_pwd(self, pwd):
        return check_password_hash(self._pwdhash, pwd)


class Post(db.Model):
    '''
    database table for recipe posts
    '''

    __tablename__ = "postinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    _filename = db.Column(db.String(128), nullable=False)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('userinfo.id'),
                          nullable=False)
    # One-to-one relationship with userinfo.id
    author = db.relationship("User",
                             primaryjoin='Post.author_id==User.id',
                             backref=db.backref("post_author",
                                                uselist=False))
    upvotes = db.Column(db.Integer, default=1)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.current_timestamp())
    data = db.Column(db.JSON, nullable=False)
    # delete when reroute gets implemented
    # hash_values = db.Column(db.String(32), nullable=False, unique=True)

    def __init__(self, author_id, data, filename):
        self.author_id = author_id
        self.data = data
        # delete when reroute gets implemented
        # self.hash_values = hashlib.md5(
        #                         json.dumps(
        #                             data,
        #                             sort_keys=True
        #                         ).encode("utf-8")).hexdigest()
        self.name = data['name']
        self.upvotes = 1
        self._filename = filename
        user = User.query.filter_by(id=self.author_id).first()
        user.posts += 1

    def upvote(self, amt):
        user = User.query.filter_by(id=self.author_id).first()
        user.upvotes += amt
        self.upvotes += amt

    @property
    def filename(self):
        '''getter for image data'''
        return self._filename


    @filename.setter
    def filename(self, image_filename):
        '''setter for image data'''
        self._filename = image_filename


class Vote(db.Model):
    '''
    database table to manage voting
    '''
    __tablename__ = "voteinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('postinfo.id'),
                        nullable=False)
    post = db.relationship('Post',
                           primaryjoin='Post.id==Vote.post_id',
                           backref=db.backref('voted_post',
                                              uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey('userinfo.id'))
    user = db.relationship('User', backref=db.backref('voted_user',
                                                      uselist=False))
    upvote = db.Column(db.Boolean, default=True, unique=False, nullable=False)

    # @property
    # def post_id(self):
    #     return self.post_id

    # @post_id.setter
    # def post_id(self, upvote_post_id):
    #     self.post_id = upvote_post_id

    # @property
    # def user_id(self):
    #     return self.user_id

    # @user_id.setter
    # def user_id(self, upvote_user_id):
    #     self.user_id = upvote_user_id

    # @property
    # def upvote(self):
    #     return self.upvote

    # @upvote.setter
    # def upvote(self, upvote_post):
    #     self.upvote = upvote_post

class Tag(db.Model):
    '''
    database table to link tags to post id
    '''
    __tablename__= "taginfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _tag = db.Column(db.String(16), )
    post_id = db.Column(db.Integer, db.ForeignKey('postinfo.id'))
    post = db.relationship('Post', backref=db.backref('taged_post',
                                                      uselist=False))

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        assert len(tag) <= 10, "Tag must be smaller than 10 characters"
        self._tag = tag
        self._tag = tag
