from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from .database import User, Post
from .forms import LoginForm, SubmitRecForm
import os
from . import login_manager, db
# from database import db

createbp = Blueprint('create_bp',
                     __name__,
                     # url_prefix='/',
                     template_folder='templates',
                     static_folder='static')


def menu_selection(req, form):
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
    return render_template('create.html', form=form)


@createbp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print("Switched to create", flush=True)
    form = SubmitRecForm()
    if form.validate_on_submit():
        print("---Submit button pressed", flush=True)
        title = request.form['title']
        recipe = request.form['recipe']
        if Post.query.filter_by(title=title).first() is not None:
            flash("Recipe already in db")
        else:
            post = Post(current_user.id, title)  # add post to db
            current_user.posts += 1
            post.body = recipe
            db.session.add(post)
            db.session.commit()
    elif request.method == 'POST':
        return menu_selection(request, form=form)
    return render_template('create.html', form=form)
