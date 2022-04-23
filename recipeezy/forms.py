from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, FileField, IntegerField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Regexp


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


class SearchForm(FlaskForm):
    '''
    Form for ingredient measurements
    '''
    style_query = {'class': 'form-control', 'style': "float: left; width: calc(100% - 100px);"}
    style_button = {'class': 'btn btn-danger', 'value': 'Search'}
    query = StringField('Query', render_kw=style_query)
    submit = SubmitField('Search', render_kw=style_button)

