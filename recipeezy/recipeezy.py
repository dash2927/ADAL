from flask import Flask, session, redirect, url_for, request, render_template
from markupsafe import escape
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)


def menu_selection(req):
    if 'username' in session:
        username = escape(session['username'])
    else:
        username = None
    if req.form.get('menu', None):
        return redirect(url_for('index', username=username))
    elif req.form.get('login', None):
        return redirect(url_for('login'))
    elif req.form.get('logout', None):
        return redirect(url_for('logout'))
    elif req.form.get('create', None):
        return redirect(url_for('create', username=username))
    elif req.form.get('search', None):
        return redirect(url_for('search', username=username))
    return render_template('home.html', name=username)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<username>', methods=['GET', 'POST'])
def index(username=None):
    if request.method == 'POST':
        return menu_selection(request)
    if username:
        body = f'Logged in as {username}'
    else:
        body = ""
    return render_template('home.html', body=body, name=username)


@app.route('/create', methods=['GET', 'POST'])
@app.route('/create/<username>', methods=['GET', 'POST'])
def create(username=None):
    if request.method == 'POST':
        return menu_selection(request)
    if username:
        body = 'Woops, cant add anything yet :('
    else:
        body = 'Need to login before adding a recipe'
    return render_template('home.html', body=body, name=username)


@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<username>', methods=['GET', 'POST'])
def search(username=None):
    if request.method == 'POST':
        return menu_selection(request)
    with app.open_resource('static/recipes/Key_Lime_Cake') as f:
        read_content = str(f.read().decode('utf-8'))
    return render_template('search.html', text=read_content, name=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username'):
            session['username'] = request.form['username']
            return redirect(url_for('index',
                                    username=escape(session['username'])))
        else:
            return menu_selection(request)
    return render_template('login.html', body="")


@app.route('/logout')
def logout():
    session.pop('username', None)
    body = f'Succesfully logged out'
    return render_template('home.html', body=body)
