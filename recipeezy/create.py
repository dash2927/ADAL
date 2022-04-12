import os, json, time, boto3, botocore
from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename
from .database import User, Post
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
        print('test - dev', flush=True)
    else:
        print('test - prod', flush=True)
        s3 = boto3.client('s3',
                          aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        S3_BUCKET = os.environ.get('S3_BUCKET')


@createbp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    # form = SubmitRecForm()
    # if form.validate_on_submit():
    #     print("---Submit button pressed", flush=True)
    #     title = request.form['title']
    #     recipe = request.form['recipe']
    #     if Post.query.filter_by(title=title).first() is not None:
    #         flash("Recipe already in db")
    #     else:
    #         post = Post(current_user.id, title)  # add post to db
    #         current_user.posts += 1
    #         post.body = recipe
    #         db.session.add(post)
    #         db.session.commit()
    form = SubmitRecForm()
    if request.method == 'POST':
        data = request.form['submitData']
        data = json.loads(data)
        file = request.files.get('file')
        print("***** --- test file: " + file.filename + '|' + file.content_type, flush=True)
        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        tags = data.get('tags')
        steps = data.get('steps')
        ingredients = data.get('ingredients')

        print(steps)
        print(type(steps))

        print(ingredients[1])

        if not (name and category and description):
            return {'status': -1, 'message': 'Please fill every field'}

        if file:
            if not allowed_file(file.filename):
                return {'status': -1, 'message': 'Invalid image file format'}

            timestamp = int(time.time())
            filename = file.filename.rsplit(".", 1)
            filename = filename[0] + str(timestamp) + "." + filename[1] # filename
            save_file(file)
            file.save(os.path.join(ca.config['UPLOAD_FOLDER'], filename)) # save file

        # Add insert to database code here
        print("Submit_data: ", flush=True)
        print(data, flush=True)

        return {'status': 0, 'message': 'success'}

    return render_template('create.html', user=current_user)
