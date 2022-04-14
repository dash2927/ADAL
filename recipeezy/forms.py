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


class IngredientForm(FlaskForm):
    '''
    Form for ingredient measurements
    '''
    amount = IntegerField('Amount')
    ing = StringField('Ingredient')


class SubmitRecForm(FlaskForm):
    '''
    Form to Submit a Recipe
    '''
    title = StringField('Recipe Title', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    image = FileField('Image File',
                      validators=[Regexp(u'^.*(\.jpeg|\.png)')])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(TextAreaField('Steps', validators=[DataRequired()]), min_entries=1)
    tags = FieldList(StringField('Tags', validators=[Optional()]), min_entries=0)
    # submit = SubmitField('Submit')

