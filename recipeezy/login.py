from flask import Blueprint, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from .database import User
import os

from . import login_manager
from database import db

# Create out blueprint
loginbp = Blueprint('login_bp',
                    __name__,
                    # url_prefix='/',
                    template_folder='templates',
                    static_folder='static')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@loginbp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if request.form.get('username'):
            session['username'] = request.form['username']
            return redirect(url_for('home_bp.home'))
        # else:
        #     return menu_selection(request)
    return render_template('login.html')


@loginbp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        continue
    return render_template('signup.html')


@loginbp.route('/signout')
def signout():
    pass
