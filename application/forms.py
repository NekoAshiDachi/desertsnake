# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# Most Flask extensions use a flask_<name> naming convention for their top-level import symbol.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # may have >1 validator per field
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')