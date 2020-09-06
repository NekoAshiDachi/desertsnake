import os
import re
from datetime import datetime

from flask import render_template, url_for, redirect, flash, request, get_flashed_messages
from flask_login import current_user, login_required
from flask_babel import _
from application import db

from application.library import bp
from application.models import Org, Person, Dojo, Country, State, Glossary, \
    Reference, Ref_category, ref_rel, Video, Kata, Publication, \
    o, p

from application.library.forms import TrainingAddForm

@bp.route('/history')
def history():
    pubs = Publication.query.join()
    return render_template("library/history.html", title=_('History'), pubs=pubs)

@bp.route('/orgs')
def orgs():
    return render_template("library/orgs.html", title=_('Organizations'), orgs=Org.query.all())

@bp.route('/org/<int:id>')
def org(id):
    org = Org.query.filter_by(id=id).first_or_404()
    founder = Person.query.filter_by(id=org.founder_person_id).first()
    head_instructor = Person.query.filter_by(id=org.headInstructor_person_id).first()
    president = Person.query.filter_by(id=org.president_person_id).first()
    honbu = Dojo.query.filter_by(id=org.honbu_dojo_id).first()
    honbu_state = State.query.filter_by(id=honbu.state_id).first() if honbu else None
    return render_template(
        "library/org.html", org=org, founder=founder, head_instructor=head_instructor, president=president,
        honbu=honbu, honbu_state=honbu_state,
        google_api_key=os.environ['GOOGLE_API_KEY'], o=o, p=p)

@bp.route('/people')
def people():
    people = Person.query.filter_by(persons_hide=None).order_by(Person.lastName).all()
    return render_template("library/people.html", people=people, enumerate=enumerate, title=_('People'))

@bp.route('/person/<int:id>')
def person(id):
    p = Person.query.filter_by(id=id).first_or_404()
    r = Publication.query.all()
    return render_template("library/person.html", p=p, r=r)

@bp.route('/glossary')
def glossary():
    glossary = Glossary.query.order_by(Glossary.type).all()
    return render_template("library/glossary.html", title=_('Glossary'), glossary=glossary)


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

        new_ref_dict = {
            'glossary_id': str(id),
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
        db.session.refresh(new_ref)  # gets new Reference ID

        ref_category = Ref_category.query.filter_by(id=submission.get('category')).first()
        new_ref.category.append(ref_category)
        db.session.add(new_ref)
        db.session.commit()

        flash(f'Your changes have been saved.', 'success')

    else:
        if src == 'video' and not video_valid:
            flash('Check YouTube address for 11-character alphanumeric YouTube ID after "v=".')

        for k, v in form.errors.items():
            flash(f"{k} field: {v[0]}", 'danger')


@bp.route('/kata_all')
def kata_all():
    pubs = Publication.query.join()
    kata = Kata.query.all()
    return render_template("library/kata_all.html", pubs=pubs, kata=kata, p=p, o=o, enumerate = enumerate, title=_('Kata'))

@bp.route('/kata/<int:id>', methods=['GET', 'POST'])
def kata(id):
    k = Kata.query.filter_by(id=id).first_or_404()
    creator = Person.query.filter_by(id=k.creator_person_id).first()
    form = TrainingAddForm()

    if request.method == 'POST':
        validate_add_reference_form(form, request, 'library.kata', id)
        return redirect(url_for('library.kata', id=id))

    return render_template("library/kata.html", title=_('Kata'), k=k, creator=creator, form=form, enumerate=enumerate,
        len=len)

@bp.route('/kihon')
def kihon():
    return render_template("library/kihon.html", title=_('Kihon'), o=o, p=p)

@bp.route('/kumite')
def kumite():
    return render_template("library/kumite.html", title=_('Kumite'))

@bp.route('/tech/<int:id>', methods=['GET', 'POST'])
@login_required
def tech(id):
    term = Glossary.query.filter_by(id=id).first_or_404()
    form = TrainingAddForm()

    if request.method == 'POST':
        validate_add_reference_form(form, request, 'library.tech', id)
        return redirect(url_for('library.tech', id=id))

    return render_template("library/tech.html", term=term, form=form)

@bp.route('/training')
def training():
    drills = Reference.query \
        .join(Ref_category, Reference.category).filter_by(name='drill') \
        .join(Glossary, Reference.term).order_by(Glossary.word).all()
    return render_template("library/training.html", title=_('Training'), drills=drills)

@bp.route('/media')
def media():
    return render_template("library/media.html", title=_('Media'))
