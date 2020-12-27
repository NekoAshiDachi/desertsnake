import re
from datetime import datetime

from flask import request, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Regexp

from application import db
from application.models import Style, Org, Person, Video, Publication, Reference, Ref_category, Ref_order

# TRAINING_ADD ---------------------------------------------------------------------------------------------------------

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
        'Person', allow_blank=True, blank_text='Person, Unknown',
        query_factory=lambda: Person.query.filter_by(persons_hide=None).order_by(Person.lastName))

    pub = QuerySelectField('Book title', query_factory=lambda: Publication.query.filter_by(format='BOOK').order_by(Publication.title))

    text_field = TextAreaField('Text', widget=TextArea(), validators=[DataRequired()])

    # TODO if video, youtube ID (include pic as example)
    submit = SubmitField('Submit')


# VALIDATION -----------------------------------------------------------------------------------------------------------

def validate_add_reference_form(form, request, route: str, id: int):

#     flash('Request method: ' + request.method, 'info')

    submission = request.form
#         flash(f"""raw submission:
#             {[k + ' - ' + v for k, v in submission.items() if k not in ('csrf_token', 'submit')]}
#             """, 'info')

    src = submission.get('training_add_source')

    video_valid = src != 'video' or (src == 'video' and re.search(r'[-_\w\d]{11}', submission.get('video_id')))
    if form.validate_on_submit() and video_valid:

        # VIDEO ----------------------------------------------------------------------------------------------------
        if submission.get('training_add_source') == 'video':

            video = Video.query.filter_by(URL=submission.get('video_id')).first()
            if not video:
                video = Video()
                db.session.add(video)
                db.session.commit()
                db.session.refresh(video)
#                     flash(f'New video record created with ID {video.id}', 'info')
            else:
#                     flash(f'Previous video record with ID {video.id}', 'info')
                pass

            org_id = submission.get('org')
            video_dict = {
                'style_id': submission.get('style'),
                'org_id': org_id if org_id and org_id != '__None' else None,
                'performer_person_id': submission.get('person').replace('__None', '99999'),
                'name': submission.get('video_name'),
                'URL': submission.get('video_id')
            }

            [setattr(video, k, v) for k, v in video_dict.items()]

#                 flash(f"""video:
#                     {[k + ' - ' + str(v) for k, v in video.__dict__.items() if v and k != '_sa_instance_state']}""",
#                     'info')

            db.session.add(video)
            db.session.commit()

        # BASE ---------------------------------------------------------------------------------------------------------
        glossary_kata = 'glossary' if 'tech' in route else 'kata'

        new_ref_dict = {
            'glossary_id': str(id) if glossary_kata == 'glossary' else None,
            'kata_id': str(id) if glossary_kata == 'kata' else None,
            'category_id': submission.get('category'),
            'person_id': submission.get('person').replace('__None', '99999') if src in ('person', 'video') else None,
            'video_id': video.id if src == 'video' else None,
            'pub_id': submission.get('pub') if src == 'publication' else None,
            'text': submission.get('text_field'),
            'created_date': datetime.now()
        }

        # TODO until can add video/people/pubs on the fly, dropdown menu and separate function for adding people/pub
        new_ref = Reference(**new_ref_dict)
#             flash(f"""new_ref: {[k + ' - ' + str(v) for k, v in new_ref_dict.items() if v]}""", 'info')

        db.session.add(new_ref)
        db.session.commit()
        db.session.refresh(new_ref)  # ID added to new_ref after insert and refresh

        glossary_kata_id = new_ref_dict[f'{glossary_kata}_id']
        ref_len = Ref_order.query.filter_by(**{f'{glossary_kata}_id': glossary_kata_id}).count()
        db.session.add(
            Ref_order(**{f'{glossary_kata}_id': glossary_kata_id, 'ref_id': new_ref.id, 'order': ref_len + 1}))

        db.session.commit()

        flash(f'Your changes have been saved.', 'success')

    else:
        if src == 'video' and not video_valid:
            flash('Check YouTube address for 11-character alphanumeric YouTube ID after "v=".', 'alert')

        for k, v in form.errors.items():
            flash(f"{k} field: {v[0]}", 'danger')
