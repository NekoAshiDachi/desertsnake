from flask import request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Regexp

from application.models import Style, Org, Person, Publication, Reference, Ref_category

# TRAINING_ADD ----------------------------------------------------------------------

class TrainingAddForm(FlaskForm):
    training_add_source = SelectField(
        'Source', choices=[(c, c.title()) for c in ('video', 'person', 'publication', 'text')], default='Text')

    category = QuerySelectField('Category', query_factory=lambda: Ref_category.query, default='Description')

    video_id = StringField('YouTube ID', default='placeholder', validators=[DataRequired()])
    video_name = StringField('Video name', default='Video name', validators=[DataRequired()])

    style = QuerySelectField('Style', query_factory=lambda: Style.query, allow_blank=True, blank_text='None')

    org = QuerySelectField(
        'Organization', allow_blank=True, blank_text='None',
        query_factory=lambda: Org.query.order_by(Org.acronym))

    # TODO https://gomakethings.com/how-to-create-a-form-input-autocomplete-without-a-library-or-framework/
    person = QuerySelectField(
        'Performer', allow_blank=True, blank_text='Person, Unknown',
        query_factory=lambda: Person.query.filter_by(persons_hide=None).order_by(Person.lastName))

    pub = QuerySelectField('Book title', query_factory=lambda: Publication.query.filter_by(format='BOOK').order_by(Publication.title))

    text_field = TextAreaField('Text', widget=TextArea(), validators=[DataRequired()])

    # TODO if video, youtube ID (include pic as example)
    submit = SubmitField('Submit')
