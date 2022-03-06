from flask import (
    Blueprint, session, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user, logout_user

from werkzeug.exceptions import abort


homebp = Blueprint('home_bp',
                   __name__,
                   # url_prefix='/',
                   )


def menu_selection(req):
    # if 'username' in session:
    #     username = escape(session['username'])
    # else:
    #     username = None
    if req.form.get('menu', None):
        return redirect(url_for('home_bp.home'))
    elif req.form.get('login', None):
        return redirect(url_for('login_bp.login'))
    elif req.form.get('logout', None):
        return redirect(url_for('login_bp.logout'))
    elif req.form.get('create', None):
        return redirect(url_for('create_bp.create'))
    # elif req.form.get('search', None):
    #     return redirect(url_for('search', username=username))
    return render_template('home.html')


@homebp.route('/', methods=('GET', 'POST'))
@homebp.route('/home', methods=('GET', 'POST'))
def home():
    print("Switched to home", flush=True)
    if request.method == 'POST':
        print(request.form, flush=True)
        return menu_selection(request)
    return render_template('home.html')


