import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from sqlalchemy.exc import OperationalError


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.setup_app = "strong"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Add configuration options:
    ENV = 'development'
    ENV = 'production'
    app.config.from_mapping(
        # Main options
        FLASK_APP='home.py',
        SECRET_KEY='dev',  # replace with os.urandom(24),
        FLASK_ENV=ENV,
        DEBUG=True,
        S3_BUCKET = "recipeezy.data",
        S3_KEY = "AKIAZK6PLAL7TET4SNNO",
        S3_SECRET = "hnwYf/AoPqZKztx/gnglsBopptYjZWeE7cogStcm",
        S3_LOCATION = 'http://recipeezy.data.s3.amazonaws.com/',
        # DATABASE=os.path.join(app.instance_path, 'recipeezy.sqlite'),
        # SQL options
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        # SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
        SQLALCHEMY_ECHO=True,  # log statements issued to stderr
        # Folder options
        STATIC_FOLDER="static",
        TEMPLATES_FOLDER="templates",
        UPLOAD_FOLDER = "recipeezy/static/images",
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    )
    # Set up postgresql for heroku:
    if ENV == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ktorfzoozadwle:95f08adfeb8e558d62c7ab82a977ff9a135e7f03f931dcf77f752df1ff31fcf6@ec2-54-157-79-121.compute-1.amazonaws.com:5432/d8v8dimv7h3a6o'
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

    # Init database app from sqlalchemy
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
        from . import home
        from . import login
        from . import create
        app.register_blueprint(home.homebp)
        app.register_blueprint(login.loginbp)
        app.register_blueprint(create.createbp)

        # Create Database Models
        create_tables()
    return app
