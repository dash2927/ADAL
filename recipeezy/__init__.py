import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.setup_app = "strong"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Add configuration options:
    app.config.from_mapping(
        # Main options
        FLASK_APP='home.py',
        SECRET_KEY='dev',  # replace with os.urandom(24),
        FLASK_ENV='development',
        DEBUG=True,
        # DATABASE=os.path.join(app.instance_path, 'recipeezy.sqlite'),
        # SQL options
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
        SQLALCHEMY_ECHO=True,  # log statements issued to stderr
        # Folder options
        STATIC_FOLDER="static",
        TEMPLATES_FOLDER="templates"
    )
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

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    # Init database app from sqlalchemy
    db.init_app(app)
    # Init login manager
    login_manager.init_app(app)

    # if we are not using sqlalchemy:
    # app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)

    with app.app_context():
        from . import home
        from . import login
        app.register_blueprint(home.homebp)
        app.register_blueprint(login.loginbp)

        # Create Database Models
        db.create_all()




    return app
