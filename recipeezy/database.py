# Import flask components and security functions
# Import app db and libs for hashing and parsing json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import re, boto3, os, hashlib, json

# User db schema definition and necessary functions, extending on user mixin and db model object
class User(UserMixin, db.Model):

    # Set tablename parameter as user
    __tablename__ = "userinfo"

    # Define table columns using sqlalchemy wrapper
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(32), nullable=False)
    _pwdhash = db.Column(db.String(128), nullable=False)
    _email = db.Column(db.String(64), unique=True)
    posts = db.Column(db.Integer, default=0)
    upvotes = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.current_timestamp())

    def __init__(self, name, pword):
        """
        Initialze the user object vars
        Arguments:
            self: user object instance
            name: username
            pword: password hash
        Returns:
            None
        """
        self.uname = name
        self.password = pword

    # Return the current username 
    @property
    def username(self):
        return self.uname

    # Set the user username
    @username.setter
    def username(self, name):
        self.uname = name

    # Prevent sensitive password leakage
    @property
    def password(self):
        raise ValueError("ERROR: Password is not retreivable")

    # Set the password hash using a user-given password
    @password.setter
    def password(self, pwd):
        self._pwdhash = generate_password_hash(pwd)

    # Prevent sensitive email information leakage
    @property
    def email(self):
        raise ValueError("ERROR: Email is not retreivable")

    # Set the user email; validate the passed email
    @email.setter
    def email(self, email):
        if(re.fullmatch(r'^[A-Za-z0-9\._-]+@[A-Za-z0-9]+\.[A-Za-z]{2,}$',
                        email)):
            self._email = email
        else:
            raise ValueError("Invalid email address.")

    # Verify that the password hash matches the plaintext password
    def verify_pwd(self, pwd):
        return check_password_hash(self._pwdhash, pwd)

# Post db schema definition and necessary functions, extending on db model object
class Post(db.Model):

    # Set the tablename parameter as post
    __tablename__ = "postinfo"

    # Define all necessary table columns 
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
        """
        Initialze the post object vars
        Arguments:
            self: post object instance
            author_id: unique id of the post author
            data: post data as json
            filename: name of the image file to be uploaded
        Returns:
            None
        """        
        
        # Set the post object author anddata
        self.author_id = author_id
        self.data = data
        # delete when reroute gets implemented
        # self.hash_values = hashlib.md5(
        #                         json.dumps(
        #                             data,
        #                             sort_keys=True
        #                         ).encode("utf-8")).hexdigest()

        # Get the name from the data json
        self.name = data['name']
        # Set the default upvotes as 1
        self.upvotes = 1
        # Set the object filename as the passed filename
        self._filename = filename
        # Increment the number of user posts
        user = User.query.filter_by(id=self.author_id).first()
        user.posts += 1

    def upvote(self, amt):
        """
        Helper function to upvote a post
        Arguments:
            self: post object instance
            amt: factor by which to set the number of votes
        Returns:
            None
        """
        # Get the user from post id and increment the user and post upvotes
        user = User.query.filter_by(id=self.author_id).first()
        user.upvotes += amt
        self.upvotes += amt

    # Get the filename from post object
    @property
    def filename(self):
        return self._filename

    # Set the post object filename with the image filename
    @filename.setter
    def filename(self, image_filename):
        self._filename = image_filename


# Vote db schema definition, extending on db model object
class Vote(db.Model):

    # Set the tablename parameter as vote
    __tablename__ = "voteinfo"

    # Define all necessary table columns
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

# Tag db schema definition, extending on db model object
class Tag(db.Model):

    # Set the tablename parameter as tag
    __tablename__= "taginfo"

    # Define all necessary table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _tag = db.Column(db.String(16), )
    post_id = db.Column(db.Integer, db.ForeignKey('postinfo.id'))
    post = db.relationship('Post', backref=db.backref('taged_post',
                                                      uselist=False))

    # Get the tag from the current Tag object
    @property
    def tag(self):
        return self._tag

    # Set the tag on the current Tag object
    @tag.setter
    def tag(self, tag):
        assert len(tag) <= 10, "Tag must be smaller than 10 characters"
        self._tag = tag
        self._tag = tag
