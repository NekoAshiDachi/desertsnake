from flask import render_template, url_for
from flask_babel import _

from application.library import bp
from application.models import Org, Person, o, p

@bp.route('/history')
def history():
    return render_template("library/history.html", title=_('History'))

@bp.route('/orgs')
def orgs():
    return render_template("library/orgs.html", title=_('Organizations'))

@bp.route('/org/<int:id>')
def org(id):
    o = Org.query.filter_by(id=id).first_or_404()
    return render_template("library/org.html", o=o)

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

@bp.route('/media')
def media():
    return render_template("library/media.html", title=_('Media'))
