from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from .database import User
from .forms import LoginForm, MakeAcctForm
import os
from . import login_manager, db
# from database import db

# Create out blueprint
loginbp = Blueprint('login_bp',
                    __name__,
                    # url_prefix='/',
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
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(uname=username).first()
        print(f'***{username} filter_by result: {user}', flush=True)
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
    return render_template('login.html', form=form)


@loginbp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        pass
    return render_template('signup.html')


@loginbp.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('home_bp.home'))
