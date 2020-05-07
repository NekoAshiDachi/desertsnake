import os

from flask import render_template, url_for
from flask_babel import _

from application.library import bp
from application.models import Org, Person, Dojo, Country, State, o, p

@bp.route('/history')
def history():
    return render_template("library/history.html", title=_('History'))

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
    honbu_country = Country.query.filter_by(id=honbu.country_id).first() if honbu else None
    honbu_state = State.query.filter_by(id=honbu.state_id, country_id=honbu.country_id).first() if honbu else None
    return render_template(
        "library/org.html", org=org, founder=founder, head_instructor=head_instructor, president=president,
        honbu=honbu, honbu_country=honbu_country, honbu_state=honbu_state,
        google_api_key=os.environ['GOOGLE_API_KEY'], o=o, p=p)

@bp.route('/people')
def people():
    return render_template("library/people.html", title=_('People'))

@bp.route('/person/<int:id>')
def person(id):
    p = Person.query.filter_by(id=id).first_or_404()
    return render_template("library/person.html", p=p)

@bp.route('/glossary')
def glossary():
    return render_template("library/glossary.html", title=_('Glossary'))

@bp.route('/kihon')
def kihon():
    return render_template("library/kihon.html", title=_('Kihon'))

@bp.route('/kata')
def kata():
    return render_template("library/kata.html", title=_('Kata'))

@bp.route('/kumite')
def kumite():
    return render_template("library/kumite.html", title=_('Kumite'))

@bp.route('/training')
def training():
    return render_template("library/training.html", title=_('Training'))

@bp.route('/media')
def media():
    return render_template("library/media.html", title=_('Media'))
