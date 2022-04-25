# Import Flask components and SqlAlchemy
# Import libs for working with json, handling parsing and validations
# Import forms and db definitions
import os, json, time, boto3, botocore
from io import BytesIO
from PIL import Image
from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import exc, or_, and_
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename
from .database import Tag, User, Post, Vote
from .forms import SearchForm
from . import login_manager, db

# Create a new blueprint instance for the search page
searchbp = Blueprint('search_bp',
                     __name__,
                    #  url_prefix='/',
                     template_folder='templates',
                     static_folder='static')

# Routing for search page with appended search terms taking GET and POST request types
@searchbp.route('/search/', methods=('GET', 'POST'))
@searchbp.route('/search/<searchterm>', methods=('GET', 'POST'))
@login_required
def search(searchterm='.'):
    """
    Function to handle recipe searches when hitting the /search/ or /search/<searchterm> endpoints
    Arguments:
        searchterm: search request parameters, initialized to '.'
    Returns:
        Rendered search page
    """

    print(f'****Test{searchterm}', flush=True)

    # Initialize post list result to none
    postlst=None
    # Create new instance of the search form
    form = SearchForm()
    print("SEARCH PAGE VISIT", flush=True)

    # Handle POST requests on the search endpoint
    if request.method == 'POST':
    #if request.method == 'POST':
        print(request.form)
        print(request)
        # Get the request data from the submitted form
        data = request.form['query']
        print(f'****Test{data}', flush=True)
        # Redirect the user to the search endpoint based on passed search terms
        return redirect(url_for('search_bp.search', searchterm=data))
        return recipe(postlst[0].id)
    # If there are search terms passed by the user, attempt to retrieve recipes
    if searchterm is not '':
        # Build list of posts based on query result using search terms
        postlst = list(Post.query.join(Tag,
                                   Post.id==Tag.post_id).filter(or_(
                                       Tag._tag.op('regexp')(rf'(?i){searchterm}'),
                                       Post.name.op('regexp')(rf'(?i){searchterm}')
                                   )).order_by(Post.upvotes.desc()).all())
        # Get at most 20 posts matching search terms
        postlst = postlst[:min(20, len(postlst))]
        print("TESTING FOR REDIRECT", flush=True)
        # Render the search page with the posts matching the search term request
        return render_template('search.html', form=form, user=current_user,
                               postlst=postlst, ca=ca)
    # On default render the basic search page
    return render_template('search.html', form=form, user=current_user, postlst=postlst)

# Routing for recipe page based on recipe id
@searchbp.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    """
    Function to handle rendering recipe details depending on recipe id
    Arguments:
        recipe_id: unique recipe id generated on recipe creation
    Returns:
        Rendered recipe page for unique recipe
    """

    # Get post by performing query on Post db by recipe_id
    post = Post.query.filter_by(id = recipe_id).first()
    print(f"**************{post.filename}", flush=True)
    # Get the post author by perfoming query on User db by post's author id
    author = User.query.filter_by(id = post.author_id).first()
    print(f'*************{current_user.is_authenticated}')
    # Get the nuber of votes by performing query on Vote db based on user id and post id
    if current_user.is_authenticated:
        vote = Vote.query.filter_by(user_id=current_user.id,
                                post_id=post.id).first()
    else:
        vote = None
    # Otherwise, no upvote data available
    upvote = "null"
    # Cast vote count to string
    if vote is not None:
        upvote = str(vote.upvote).lower()
    # If in development, get the filename from static files
    if ca.config['FLASK_ENV'] == 'development':
        filename = url_for('static', filename = post.filename)
    # Otherwise, pull filename from user input
    else:
        filename = post.filename

    # Render the recipe page with the authenticated user, and recipe details such as name, post, number of upvotes...
    return render_template('recipe.html', user=current_user, name=post.name,
                           post=post, author=author, upvote=upvote,
                           filename=filename)
