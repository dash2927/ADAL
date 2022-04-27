# Import Flask components and SqlAlchemy
# Import libs for working with json, handling parsing and validations
# Import forms and db definitions
from flask import redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from sqlalchemy import or_
from .database import Tag, User, Post, Vote
from .forms import SearchForm
from . import db


# Create a new blueprint instance for the search page
searchbp = Blueprint('search_bp',
                     __name__,
                    #  url_prefix='/',
                     template_folder='templates',
                     static_folder='static')


if ca.config['FLASK_ENV'] == 'development':
    regex = 'regexp'
else:
    regex = '~'


def changevote(recipe_id, action):
    post = Post.query.filter_by(id = recipe_id).first()
    user = User.query.filter_by(id = post.author_id).first()
    action_arr = action.split('_') # action will be in form {vote_type}_{inc_a}_{inc_p}
    vote_type = action_arr[0] # will be either upvote, downvote, or none
    inc_a = int(action_arr[1]) # new value of author upvotes
    inc_p = int(action_arr[2]) # new value of post upvotes
    if vote_type == "none":
        # if vote_type is none, we are removing the vote from Vote
        try:
            post.upvotes = inc_p
            user.upvotes = inc_a
            Vote.query.filter_by(user_id=current_user.id,
                                post_id=recipe_id).delete()
            db.session.commit()
        except Exception as e:
            print(f"Error in vote deletion. Rolling back db: {e}", flush=True)
            db.session.flush()
            db.session.rollback()
        return
    # since vote_type is not none, we can check upvote or downvote
    vote_type = vote_type == "upvote"
    vote = Vote.query.filter_by(user_id=current_user.id,
                                post_id=recipe_id).first()
    try:
        if vote is None:
            # if we dont have a vote, we need to add it:
            vote = Vote(post_id=recipe_id, user_id=current_user.id, upvote=vote_type)
            db.session.add(vote)
        else:
            vote.upvote = vote_type
        post.upvotes = inc_p
        user.upvotes = inc_a
        db.session.commit()
    except Exception as e:
        print(f"Error when changing current Vote entry. Rolling back db: {e}", flush=True)
        db.session.flush()
        db.session.rollback()
    return


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
    # Initialize post list result to none
    postlst=None
    # Create new instance of the search form
    form = SearchForm()
    # Handle POST requests on the search endpoint
    if request.method == 'POST':
    #if request.method == 'POST':
        # Get the request data from the submitted form
        data = request.form['query']
        # Redirect the user to the search endpoint based on passed search terms
        return redirect(url_for('search_bp.search', searchterm=data))
        return recipe(postlst[0].id)
    # If there are search terms passed by the user, attempt to retrieve recipes
    if searchterm != '':
        # Build list of posts based on query result using search terms
        postlst = list(Post.query.join(Tag,
                                   Post.id==Tag.post_id).filter(or_(
                                       Tag._tag.op(regex)(rf'(?i){searchterm}'),
                                       Post.name.op(regex)(rf'(?i){searchterm}')
                                   )).order_by(Post.upvotes.desc()).all())
        # Get at most 20 posts matching search terms
        postlst = postlst[:min(20, len(postlst))]
        # Render the search page with the posts matching the search term request
        return render_template('search.html', form=form, user=current_user,
                               postlst=postlst, ca=ca)
    # On default render the basic search page
    return render_template('search.html', form=form, user=current_user, postlst=postlst)


# Routing for recipe page based on recipe id
@searchbp.route('/recipe/<recipe_id>', methods=["POST", "GET"])
@searchbp.route('/recipe/<recipe_id>/<action>', methods=["POST", "GET"])
def recipe(recipe_id, action=None):
    """
    Function to handle rendering recipe details depending on recipe id
    Arguments:
        recipe_id: unique recipe id generated on recipe creation
    Returns:
        Rendered recipe page for unique recipe
    """
    # Get post by performing query on Post db by recipe_id
    if request.method == "POST":
        changevote(recipe_id=recipe_id, action=request.json["htmlstr"])
    post = Post.query.filter_by(id = recipe_id).first()
    # Get the post author by perfoming query on User db by post's author id
    author = User.query.filter_by(id = post.author_id).first()
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
