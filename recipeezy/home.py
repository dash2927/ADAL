# Import Flask components and current app
# Import components to pull posts for homepage, and exception handling
from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask_login import current_user, logout_user
from flask import current_app as ca
from .database import Post
from werkzeug.exceptions import abort


# Create a new blueprint instance for the homepage
homebp = Blueprint('home_bp', __name__)


if ca.config['FLASK_ENV'] == 'development':
    regex = 'regexp'
else:
    regex = '~'


# Define routing for the homepage on different endpoints
@homebp.route('/', methods=('GET', 'POST'))
@homebp.route('/home', methods=('GET', 'POST'))
def home():
    """
    Function to handle homepage instantiaion and rendering
    Arguments:
        None
    Returns:
        Rendered home page
    """

    # Get the top posts by upvote currently on the Post db
    postlst = list(Post.query.filter(Post.name.op(regex)(rf'(?i).'))
                   .order_by(Post.upvotes.desc()).all())
    # Render the final homepage with the current user and top posts
    return render_template('home.html', user=current_user, postlst=postlst,
                           ca=ca)
