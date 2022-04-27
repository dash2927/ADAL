# Import Flask components and SqlAlchemy
# Import app db definitions, forms,  and libs for parsing urls
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


# Create a new blueprint instance for the login page
loginbp = Blueprint('login_bp',
                    __name__,
                    template_folder='templates',
                    static_folder='static')


# Decorator for handling unauthorized logins, redirect to base login url
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login_bp.login'))


# Decorator for loading a user from the User db on user id
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


# Route definition for login endpoint, accepting GET and POST request types
@loginbp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Function to handle user login when hitting the /login endpoint
    Arguments:
        None
    Returns:
        Rendered login page
        Validation exceptions if applicable
    """
    # Create new instance of login form and initialize error dialogue
    form = LoginForm()
    error_msg = None
    # If form validation is successful, direct user through the auth flow
    if form.validate_on_submit():
        # Get username and password from request form
        username = request.form['username']
        password = request.form['password']
        # Fetch user from User db
        user = User.query.filter_by(uname=username).first()
        # If user is found, verify the password given, error otherwise
        if user is not None:
            if user.verify_pwd(password):
                login_user(user)
                return redirect(url_for('home_bp.home'))
            else:
                error_msg = f'Password is incorrect.'
        else:
            error_msg = f'{username} is not valid. Please make a new' + \
            ' account or try another username.'
    # Return the rendered login page
    return render_template('login.html', form=form, error_msg=error_msg)


# Route definition for signup endpoint, accepting GET and POST request types
@loginbp.route('/signup', methods=('GET', 'POST'))
def signup():
    """
    Function to handle signup upon hitting /signup endpoint
    Arguments:
        None
    Returns:
        Rendered signup page
        Validation errors if applicable
    """
    # Create new instance of account signup form and initialize error dialogue
    form = MakeAcctForm()
    error_msg = None

    # Get necessary form elements on POST request type
    if request.method == 'POST':
        # Get fields username, password, email, from request form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Get the (potential) user from User db
        user = User.query.filter_by(uname=username).first()
        # If user is not found, then it does not exist and creation is validated
        if user is None:
            try:
                # Create new user entity from username and password
                user = User(username, password)
                # Set email property if applicable
                if email:
                    user.email = email
                # Add user to db and commit
                db.session.add(user)
                db.session.commit()
                # User creation successful; redirect user home
                return redirect(url_for('home_bp.home'))
            # Handle errors
            except ValueError as e:
                error_msg = e
                db.session.flush()
                db.session.rollback()
            except exc.IntegrityError:
                error_msg = 'Email address is already in use. Please ' + \
                            'try another or login.'
                db.session.flush()
                db.session.rollback()
        # If user already exists, prompt user to try again
        else:
            error_msg = f'Username is already taken.'
    # Return the rendered signup page with form elements and errors if applicable
    return render_template('signup.html', form=form, error_msg=error_msg)


# Route to signout a user, must be logged-in to perform action
@loginbp.route('/signout')
@login_required
def signout():
    """
    Function to handle signout upon hitting /signout endpoint
    Arguments:
        None
    Returns:
        Redirect to home page
    """
    # Call the logout user util function
    logout_user()
    # Redirect user to the homepage upon successful logout
    return redirect(url_for('home_bp.home'))
