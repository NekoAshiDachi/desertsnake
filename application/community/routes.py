from flask import render_template
from flask_babel import _
from sqlalchemy import func

from application.community import bp
from application.models import Dojo, Org

@bp.route('/events')
def events():
    return render_template("community/events.html", title=_('Events'))

@bp.route('/directory')
def directory():
    dojos = Dojo.query.join(Org, Dojo.org).order_by(Org.name).all()
    return render_template("community/directory.html", dojos=dojos, title=_('Directory'))

@bp.route('/training_notes')
def training_notes():
    return render_template("community/training_notes.html", title=_('Training Notes'))
