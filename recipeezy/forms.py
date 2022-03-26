from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    '''
    Form to log in to account
    '''
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class MakeAcctForm(FlaskForm):
    '''
    Form to make an account
    '''
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    # submit = SubmitField('Create Account')


class SubmitRecForm(FlaskForm):
    '''
    Form to Submit a Recipe
    '''
    title = StringField('Recipe Title', validators=[DataRequired()])
    recipe = TextAreaField('Recipe', validators=[DataRequired()])
    submit = SubmitField('Submit')
