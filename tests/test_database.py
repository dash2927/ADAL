from flask_testing import TestCase
from flask import Flask
from recipeezy import db, app
from recipeezy.database import User
import pytest
import unittest


class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///sqltesting.sqlite3"
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # pass in test configuration
        self.app = app
        return app

    def setUp(self):
        self.create_app()
        # self.app = app.test_client()
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_add_user():
        first_user = User("First_User", "password1")
        second_user = User("Second_User", "password2")
        db.session.add(first_user)
        db.session.add(second_user)
        db.session.commit()
        assert first_user in db.session
        with pytest.raises(ValueError):
            first_user.email = "bademail"
            print(first_user.password)
        try:
            first_user.email = "good@email.com"
        except ValueError:
            assert False
        user = User.query.filter_by(uname="First_User").first()
        assert user.name == "First_User"


if __name__ == '__main__':
    unittest.main()
