from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from .database import User
from .forms import LoginForm, MakeAcctForm
import os
from sqlite3 import IntegrityError
from . import login_manager, db
# from database import db

# Create out blueprint
loginbp = Blueprint('login_bp',
                    __name__,
                    template_folder='templates',
                    static_folder='static')

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login_bp.login'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@loginbp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error_msg = None
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(uname=username).first()
        if user is not None:
            if user.verify_pwd(password):
                login_user(user)
                return redirect(url_for('home_bp.home'))
            else:
                error_msg = f'Password is incorrect.'
        else:
            error_msg = f'{username} is not valid. Please make a new' + \
            ' account or try another username.'
    return render_template('login.html', form=form, error_msg=error_msg)


@loginbp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = MakeAcctForm()
    error_msg = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(uname=username).first()
        if user is None:
            try:
                user = User(username, password)
                if email:
                    user.email = email
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('home_bp.home'))
            except ValueError as e:
                error_msg = e
            except exc.IntegrityError:
                error_msg = 'Email address is already in use. Please ' + \
                            'try another or login.'
        else:
            error_msg = f'Username is already taken.'
    return render_template('signup.html', form=form, error_msg=error_msg)


@loginbp.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('home_bp.home'))
