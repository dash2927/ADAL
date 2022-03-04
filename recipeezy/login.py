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


def is_safe_url(target):
    '''
    taken from recommended method to check for safe url
    in flask_login API doumentation
    '''
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@loginbp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("---Submit button pressed", flush=True)
        print(request.form, flush=True)
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(uname=username).first()
        print(f'***{username} filter_by result: {user}', flush=True)
        # print(f'Verification: {password} = {user.verify_pwd(password)}')
        print(User.query.all())
        if user is not None:
            if user.verify_pwd(password):
                login_user(user)
                flash('Logged in succesfully')
                # next gets the page you were previously on for redirect
                nxt = request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                if not is_safe_url(nxt):
                    return abort(400)
                return redirect(nxt or url_for('home_bp.home'))
            else:
                print("Incorrect password check", flush=True)
                flash("Incorrect password")
        else:
            # this is temporary. it essentially just adds a constant new user
            # replace this section with account creation redirect!
            new_user = User('new_user', 'password')
            db.session.commit()
            db.session.add(new_user)
            try:
                new_user.email = 'bademail'
            except ValueError:
                new_user.email = 'good@email.com'
            db.session.commit()

    print(form.errors, flush=True)
    print(current_user, flush=True)
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
    nxt = request.args.get('next')
    if not is_safe_url(nxt):
        return abort(400)
    return redirect(nxt or url_for('home_bp.home'))
