import os

from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_required
from flask_babel import _

from application import db
from application.library import bp
from application.models import Org, Person, Dojo, Country, State, Glossary, \
    Reference, Ref_category, Ref_order, Video, Kata, Publication, \
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
@login_required
def kata(id):
    k = Kata.query.filter_by(id=id).first_or_404()

    conditions = (Ref_order.kata_id==k.id) & (Ref_order.ref_id==Reference.id)
    refs = k.refs.outerjoin(Ref_order, conditions).add_columns(Ref_order.order).all()

    null_check = [order for ref, order in refs if order]
    if not null_check:
        [db.session.add(Ref_order(kata_id=id, ref_id=r[0].id, order=n + 1)) for n, r in enumerate(refs)]
        db.session.commit()
        refs = k.refs.outerjoin(Ref_order, conditions).add_columns(Ref_order.order).all()

    refs = [ref for ref, order in sorted(refs, key=lambda x: x[1])]
    ref_data = {'ref_type': 'kata', 'ref_type_id': id}

    creator = Person.query.filter_by(id=k.creator_person_id).first()
    form = TrainingAddForm()

    if request.method == 'POST':
        validate_add_reference_form(form, request, 'library.kata', id)
        return redirect(url_for('library.kata', id=id))

    return render_template("library/kata.html", title=_('Kata'), k=k, refs=refs, ref_data=ref_data, creator=creator,
        form=form, enumerate=enumerate, len=len)

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

    conditions = (Ref_order.glossary_id==term.id) & (Ref_order.ref_id==Reference.id)
    refs = term.refs.outerjoin(Ref_order, conditions).add_columns(Ref_order.order).all()

    null_check = [order for ref, order in refs if order]
    if not null_check:
        [db.session.add(Ref_order(glossary_id=id, ref_id=r[0].id, order=n + 1)) for n, r in enumerate(refs)]
        db.session.commit()
        refs = term.refs.outerjoin(Ref_order, conditions).add_columns(Ref_order.order).all()

    refs = [ref for ref, order in sorted(refs, key=lambda x: x[1])]
    ref_data = {'ref_type': 'glossary', 'ref_type_id': id}

    form = TrainingAddForm()

    if request.method == 'POST':
        validate_add_reference_form(form, request, 'library.tech', id)
        return redirect(url_for('library.tech', id=id))

    return render_template("library/tech.html", term=term, refs=refs, ref_data=ref_data, form=form, enumerate=enumerate,
    len=len)

@bp.route('/training')
def training():
    drills = Reference.query \
        .join(Ref_category, Reference.category).filter_by(name='drill') \
        .join(Glossary, Reference.term).order_by(Glossary.word).all()
    return render_template("library/training.html", title=_('Training'), drills=drills)

@bp.route('/media')
def media():
    return render_template("library/media.html", title=_('Media'))

# ----------------------------------------------------------------------------------------------------------------------

def get_ref(ref_type, ref_type_id: int, order: int):
    ref_type_col = getattr(Ref_order, f'{ref_type}_id')
    return Ref_order.query.filter((ref_type_col==ref_type_id) & (Ref_order.order==order)).first_or_404()

@bp.route('/prioritize/<ref_type>/<int:ref_type_id>/<int:order>')
@login_required
def prioritize(ref_type, ref_type_id, order):
    ref_current_id = get_ref(ref_type, ref_type_id, order).id
    ref_above_id = get_ref(ref_type, ref_type_id, order - 1).id

    Ref_order.query.filter_by(id=ref_current_id).update({'order': order - 1})
    Ref_order.query.filter_by(id=ref_above_id).update({'order': order})
    db.session.commit()

    library_url = f"library.{'kata' if ref_type=='kata' else 'tech'}"
    return redirect(url_for(library_url, id=ref_type_id))

@bp.route('/deprioritize/<ref_type>/<int:ref_type_id>/<int:order>')
@login_required
def deprioritize(ref_type, ref_type_id, order):
    ref_current_id = get_ref(ref_type, ref_type_id, order).id
    ref_below_id = get_ref(ref_type, ref_type_id, order + 1).id

    Ref_order.query.filter_by(id=ref_current_id).update({'order': order + 1})
    Ref_order.query.filter_by(id=ref_below_id).update({'order': order})
    db.session.commit()

    library_url = f"library.{'kata' if ref_type=='kata' else 'tech'}"
    return redirect(url_for(library_url, id=ref_type_id))
