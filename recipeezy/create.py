import os, json, time, boto3, botocore
from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import exc
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename
from .database import User, Post, Vote, Tag
from .forms import LoginForm, SubmitRecForm
from . import login_manager, db

# from database import db

createbp = Blueprint('create_bp',
                     __name__,
                    #  url_prefix='/',
                     template_folder='templates',
                     static_folder='static')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ca.config['ALLOWED_EXTENSIONS']

def save_file(file):
    if ca.config['FLASK_ENV'] == 'development':
        try:
            file.save(os.path.join(ca.config['UPLOAD_FOLDER'], file.filename))
        except Exception as e:
            return -1
        return f"{os.path.join(ca.config['UPLOAD_FOLDER'], file.filename)}"
    else:
        s3 = boto3.client('s3',
                          aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
        fields = {"ACL": "public-read", "ContentType": file.content_type}
        try:
            s3.upload_fileobj(
                file,
                S3_BUCKET,
                file.filename,
                ExtraArgs=fields
            )
        except Exception as e:
            print("AWS upload error: ", e)
            return -1
        return f"{ca.config['S3_LOCATION']}{file.filename}"


@createbp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        data = request.form['submitData']
        data = json.loads(data)
        file = request.files.get('file')
        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        tags = data.get('tags')
        steps = data.get('steps')
        ingredients = data.get('ingredients')
        if not (name and category and description):
            return {'status': -1, 'message': 'Please fill every field'}
        if file:
            if not allowed_file(file.filename):
                return {'status': -1, 'message': 'Invalid image file format'}
            timestamp = int(time.time())
            file.filename = file.filename.rsplit(".", 1)
            # filename - using username to prevent upload attacks
            file.filename = file.filename[0] + "__" +\
                            name + "__" + current_user.uname +\
                            "." + file.filename[1]
            file.filename = secure_filename(file.filename)
            output = save_file(file)
            if output == -1:
                return {'status': -1, 'message': 'Error when uploading file'}
        try:
            print("***********OUTPUT: ", flush=True, end='')
            print(output, flush=True)
            post = Post(current_user.id, data, output)
            db.session.commit()
            db.session.add(post)
            print(f"*********Post ID: {post.id}")
            print(f"*********Current_User ID: {current_user.id}")
            vote = Vote(user_id=current_user.id, post_id=post.id) # ensure user cant upvote own post
            for tagi in tags:
                tag = Tag(post_id=vote.post_id, tag=tagi)
                db.session.add(tag)
            current_user.upvotes += 1
            db.session.add(vote)
            db.session.commit()
        except ValueError as e:
            db.session.flush()
            db.session.rollback()
            error_msg = e
        except exc.IntegrityError as e:
            print(e, flush=True)
            error_msg = 'You have already posted this recipe.'
            return {'status': -1, 'message': error_msg}
        return {'status': 0, 'message': 'success'}
    return render_template('create.html', user=current_user)
