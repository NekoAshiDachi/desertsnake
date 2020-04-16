# Most Flask extensions use a flask_<name> naming convention for their top-level import symbol.
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from application.models import User

# PROFILE ----------------------------------------------------------------------

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

# POST -------------------------------------------------------------------------

class PostForm(FlaskForm):
    post = TextAreaField(
        _l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

# SEARCH -----------------------------------------------------------------------

class SearchForm(FlaskForm):
    """
    q = standard search term and allows searches to be completely encapsulated
    in URL, so can be shared; e.g., google.com/search?q=python

    Does not need submit field, as browser submits when pressing Enter when
    focused on text field
    """
    q = StringField(_l('Search'), validators=[DataRequired()])

    """provides values for formdata and csrf_enabled if not provided by caller;
    Flask-WTF by default from POST uses request.form, but from GET uses
    request.args; CSRF needs to be disabled for clickable search links to work
    """
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

# MESSAGE ----------------------------------------------------------------------

class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'),
        validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))
