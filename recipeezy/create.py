# Import necessary Flask components, sqlalchemy, and utils for parsing filenames
import os, json, time, boto3, botocore
from flask import Blueprint, abort, flash, redirect, session, render_template, request, url_for
from flask import current_app as ca
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import exc
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename
from .database import User, Post, Vote, Tag
from . import login_manager, db, tags, words

# Create a new blueprint instance for the create page, with necessary settings
createbp = Blueprint('create_bp',
                     __name__,
                    #  url_prefix='/',
                     template_folder='templates',
                     static_folder='static')


def allowed_file(filename):
    """
    Determine if the filename contains an allowed extension
    Arguments:
        filename: filename to be parsed
    Returns:
        Allowed filetypes for the app
    """

    # Return the allowed extensions from the app configuration if filename matches
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ca.config['ALLOWED_EXTENSIONS']

def save_image(file):
    """
    Save image to the appropriate database depending on environment settings
    Arguments:
        file: Handle to the file to be saved
    Returns:
        Path to where the file has been saved within applicable db
    """

    # If in development environment, save image file to development db instance
    if ca.config['FLASK_ENV'] == 'development':
        try:
            file.save(os.path.join(ca.config['UPLOAD_FOLDER'], file.filename))
        # Throw exception on fail
        except Exception as e:
            print(e, flush=True)
            return -1
        # Return the final location of the file
        return f"{os.path.join('images', file.filename)}"

    # Otherwise, in prod development and save to S3 instance
    else:
        # Use aws access credentials to create new s3 client
        s3 = boto3.client('s3',
                          aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        # Get the S3 bucket from environment vars, define appropriate fields
        S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
        fields = {"ACL": "public-read", "ContentType": file.content_type}
        # Upload image file to S3 using config
        try:
            s3.upload_fileobj(
                file,
                S3_BUCKET,
                file.filename,
                ExtraArgs=fields
            )
        # Throw exception on save fail
        except Exception as e:
            print("AWS upload error: ", e)
            return -1
        # Return app path for S3 and the filename
        return f"{ca.config['S3_LOCATION']}{file.filename}"


@createbp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """
    Function to handle the creation of new recipes when hitting the create endpoint
    Arguments:
        None
    Returns:
        Rendered create page
        Connection exceptions if applicable
    """
    # Handle POST requests after user submits recipe
    if request.method == 'POST':
        # Convert form data to JSON
        data = request.form['submitData']
        data = json.loads(data)
        file = request.files.get('file')
        # Get necessary fields from parsed JSON request (name, category, tags,...)
        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        tags = data.get('tags')
        steps = data.get('steps')
        ingredients = data.get('ingredients')
        # Handle case where not all form fields are filled
        if not (name and category and description):
            return {'status': -1, 'message': 'Please fill every field'}
        # Handle filename errors and potential file exploits
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
            output = save_image(file)
            file.filename=output
            # Handle any file upload errors after save
            if output == -1:
                return {'status': -1, 'message': 'Error when uploading file'}

        # Once form has been validated, save all elements to the dbs
        try:
            print("***********OUTPUT: ", flush=True, end='')
            print(output, flush=True)
            # Create Post entity with necessary fields
            post = Post(current_user.id, data, output)
            # Save post entity to db
            db.session.add(post)
            db.session.commit()
            # Print statements for debugging
            print(f"*********Post ID: {post.id}")
            print(f"*********Current_User ID: {current_user.id}")
            # Create Vote entity with necessary fields
            vote = Vote(user_id=current_user.id, post_id=post.id)
            # Get each tag from the parsed data and save to the db
            for tagi in tags:
                tag = Tag(post_id=vote.post_id, tag=tagi)
                db.session.add(tag)
            # Upvote on the recipe once added, save changes to the db
            current_user.upvotes += 1
            db.session.add(vote)
            db.session.commit()
        # Handle exceptions and flush any db additions
        except ValueError as e:
            db.session.flush()
            db.session.rollback()
            error_msg = e
        # Handle case where user has posted recipe more than once
        except exc.IntegrityError as e:
            print(e, flush=True)
            error_msg = 'You have already posted this recipe.'
            return {'status': -1, 'message': error_msg}
        return {'status': 0, 'message': 'success'}
    # Return create page for the current user
    return render_template('create.html', user=current_user)
