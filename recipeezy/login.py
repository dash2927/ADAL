from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

from database import db
from recipeezy.db import get_db

# Create out blueprint
bp = Blueprint('login',
               __name__,
               url_prefix='/',
               template_folder='templates',
               static_folder='static')

# Insert all config options
ca.config['SECRET_KEY'] = os.urandom(24)
ca.config['DEBUG'] = True
ca.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ca.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

# Create a database object
db = SQLAlchemy(bp)


class User(db.Model):
    username = db.Column(db.Integer, primary_key=True)
    pwd_encrpt = db.Column(db.String(64))

    @property.setter
    def password(self, pwd):
        self.pwd_encrpt = bcrypt.hashpw('pwd', bcrypt.gensalt())

    @property.setter
    def email(self, pwd):

    def verify_pwd(self, pwd):
        return bcrypt.hashpw('pwd', bcrypt.gensalt()) == self.pwd_encrpt


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if request.form.get('username'):
            session['username'] = request.form['username']
            return redirect(url_for('index',
                                    username=escape(session['username'])))
        else:
            return menu_selection(request)
    return render_template('login.html', body="")
