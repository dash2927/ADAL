# Import Flask form helper and wtform fields and validators
from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, FileField, IntegerField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Regexp

# Login form extending on FlaskForm with fields for accepting username/password
class LoginForm(FlaskForm):

    # Define necessary fields for the login form
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Submit button
    submit = SubmitField('Login')

# Account creation form extending on FlaskForm with fields for accepting username/password and email
class MakeAcctForm(FlaskForm):

    # Define necessary fields for the account creation form
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    # submit = SubmitField('Create Account')

# Search recipes form extending on FlaskForm with fields for a search query and submit button
class SearchForm(FlaskForm):
    
    # Styling elements for query field and submit button
    style_query = {'class': 'form-control', 'style': "float: left; width: calc(100% - 100px);"}
    style_button = {'class': 'btn btn-danger', 'value': 'Search'}
    # Instance creation for query field and submit query button
    query = StringField('Query', render_kw=style_query)
    submit = SubmitField('Search', render_kw=style_button)

