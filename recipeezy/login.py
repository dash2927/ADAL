from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user
from urllib.parse import urlparse, urljoin
from .database import User
from .forms import LoginForm, MakeAcctForm
import os
from . import login_manager
# from database import db

# Create out blueprint
loginbp = Blueprint('login_bp',
                    __name__,
                    # url_prefix='/',
                    template_folder='templates',
                    static_folder='static')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(username=user_id)


@loginbp.route('/login', methods=('GET', 'POST'))
def login():
    user = current_user
    form = LoginForm()
    if form.validate_on_submit():
        print(user, flush=True)
        login_user(user)
        flash('Logged in succesfully')
        # next gets the page you were previously on for redirect
        nxt = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(nxt):
            return abort(400)
        return redirect(nxt or url_for('home_bp.home'))
    print(form.errors, flush=True)
    print(current_user, flush=True)
    return render_template('login.html', form=form)


@loginbp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        pass
    return render_template('signup.html')


@loginbp.route('/signout')
def signout():
    pass
