import os, json, boto3, botocore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from fast_autocomplete.misc import read_csv_gen
from sqlalchemy.exc import OperationalError


db = SQLAlchemy()
words = {}
login_manager = LoginManager()
login_manager.setup_app = "strong"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Choose environment (change to production when using heroku):
    # ENV = 'development'
    ENV = 'production'
    # Add configuration options:
    app.config.from_mapping(
        # Main options
        FLASK_APP='home.py',
        SECRET_KEY='dev',  # replace with os.urandom(24) on final push
        FLASK_ENV=ENV,
        DEBUG=True,
        # SQL options
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_ECHO=True,  # log statements issued to stderr
        # Folder options
        STATIC_FOLDER="static",
        TEMPLATES_FOLDER="templates",
        UPLOAD_FOLDER = "recipeezy/static/images",
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    )
    # Choose postgresql for heroku (outside development environment):
    if ENV == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.recipeezy'
        app.config['DATABASE'] = os.path.join(app.instance_path,
                                              'recipeezy.sqlite')
        if os.path.exists(os.path.join(app.instance_path,
                                       "static/words.csv")):
            with open(os.path.join(app.instance_path, "static/words.txt"), 'r') as f:
                words = json.load(f)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ktorfzoozadwle:95f08adfeb8e558d62c7ab82a977ff9a135e7f03f931dcf77f752df1ff31fcf6@ec2-54-157-79-121.compute-1.amazonaws.com:5432/d8v8dimv7h3a6o'
        app.config['S3_LOCATION'] = f"http://{os.environ.get('S3_BUCKET_NAME')}.s3.amazonaws.com/"
        s3 = boto3.client('s3',
                          aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Init app
    db.init_app(app)
    # Init login manager
    login_manager.init_app(app)

    # function to create all tables before request
    @app.before_first_request
    def create_tables():
        try:
            db.create_all()
        except OperationalError as e:
            print(f"SQLAlchemy error: {e}", flush=True)

    with app.app_context():
        # Add all blueprints
        from . import home
        from . import login
        from . import create
        from . import search
        app.register_blueprint(home.homebp)
        app.register_blueprint(login.loginbp)
        app.register_blueprint(create.createbp)
        app.register_blueprint(search.searchbp)

        # Create Database Models
        create_tables()
    return app
