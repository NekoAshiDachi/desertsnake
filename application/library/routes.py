import os

from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_required
from flask_babel import _

from application.library import bp
from application.models import Org, Person, Dojo, Country, State, Glossary, \
    Reference, Ref_category, Video, Kata, Publication, \
    o, p

from application.library.forms import TrainingAddForm, validate_add_reference_form

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

@bp.route('/kata_all')
def kata_all():
    pubs = Publication.query.all()
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
