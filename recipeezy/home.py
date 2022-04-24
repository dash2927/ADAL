from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask_login import current_user, logout_user
from flask import current_app as ca
from .database import Post
from werkzeug.exceptions import abort

homebp = Blueprint('home_bp', __name__)

if ca.config['FLASK_ENV'] == 'development':
    regex = 'regexp'
else:
    regex = '~'


@homebp.route('/', methods=('GET', 'POST'))
@homebp.route('/home', methods=('GET', 'POST'))
def home():
    print("Switched to home", flush=True)
    # print(f'user: {current_user.uname}', flush=True)
    postlst = list(Post.query.filter(Post.name.op(regex)(rf'(?i).'))
                   .order_by(Post.upvotes.desc()).all())
    print(f'************{postlst}', flush=True)
    return render_template('home.html', user=current_user, postlst=postlst,
                           ca=ca)
