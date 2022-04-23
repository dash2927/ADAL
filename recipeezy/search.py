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

# from database import db

searchbp = Blueprint('search_bp',
                     __name__,
                    #  url_prefix='/',
                     template_folder='templates',
                     static_folder='static')
'''
def load_file(key):
    if ca.config['FLASK_ENV'] == 'development':
        try:

        except Exception as e:
            return -1
    else:
        s3 = boto3.client('s3',
                          aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
        try:
            image_obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
            imageb = image_obj['Body'].read()
            image = Image.open(BytesIO(imageb))
        except Exception as e:
            print("AWS upload error: ", e)
            return -1
        return image
'''

@searchbp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    postlst=None
    form = SearchForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
    #if request.method == 'POST':
        print(request.form)
        print(request)
        print('****Test', flush=True)
        data = request.form['query']
        print(data.encode('unicode_escape'), flush=True)
        postlst = Post.query.join(Tag,
                                   Post.id==Tag.post_id).filter(or_(
                                       Tag._tag.op('regexp')(rf'(?i){data}'),
                                       Post.name.op('regexp')(rf'(?i){data}')
                                   )).all()
        print(postlst, flush=True)
        return redirect(url_for('search_bp.recipe', recipe_id=postlst[0].id))
        #return render_template('search.html', user=current_user,
        #                       posti=postlst[0], postlst=postlst)
    # post = Post.query.filter_by(name="Baked Cod Burgers").first()
    # print(post.name)
    # return render_template('search_bp.recipe', post=post, name=post.name)
    return render_template('search.html', form=form, user=current_user, postlst=postlst)


@searchbp.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    '''
    Page for recipe data.

    post: SQLAlchemy class object : database object which
          details all information of the recipe post
    '''
    post = Post.query.filter_by(id = recipe_id).first()
    print(f"**************{post.filename}", flush=True)
    author = User.query.filter_by(id = post.author_id).first()
    vote = Vote.query.filter_by(user_id=current_user.id,
                                post_id=post.id).first()
    upvote = "null"
    if vote is not None:
        upvote = str(vote.upvote).lower()
    print(f'{post.name}, {author.uname}, {current_user.uname}, {upvote}', flush=True)
    return render_template('recipe.html', name=post.name,
                           post=post, author=author, upvote=upvote)
