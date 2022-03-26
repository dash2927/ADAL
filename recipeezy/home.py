from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask_login import current_user, logout_user
from werkzeug.exceptions import abort

homebp = Blueprint('home_bp', __name__)

@homebp.route('/', methods=('GET', 'POST'))
@homebp.route('/home', methods=('GET', 'POST'))
def home():
    print("Switched to home", flush=True)
    # print(f'user: {current_user.uname}', flush=True)
    return render_template('home.html', user=current_user)
