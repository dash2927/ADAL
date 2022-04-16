import os, json, time, boto3, botocore
from io import BytesIO
from PIL import Image
from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import exc
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename
from .database import User, Post, Vote
from .forms import LoginForm, SubmitRecForm
from . import login_manager, db

# from database import db

createbp = Blueprint('search_bp',
                     __name__,
                    #  url_prefix='/',
                     template_folder='templates',
                     static_folder='static')

def load_file(key):
    if ca.config['FLASK_ENV'] == 'development':
        try:
            file.load(os.path.join(ca.config['UPLOAD_FOLDER'], key))
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


@searchbp.route('/search', methods=('GET', 'POST'))
@login_required
def search(Post, data):
    if request.method == 'POST':
        print('Test', flush=True)
    post = Post.query.filter_by(=).first()
    return render_template('search.html')



@searchbp.route('/<data.name>', methods=('GET'))
def recipe(Post, data):
    '''
    Page for recipe data.

    Post: SQLAlchemy class object : database object which
          details all information of the recipe post
    data : dictionary : json data on the recipe post
    '''
    return

