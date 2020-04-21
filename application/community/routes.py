from flask import render_template
from flask_babel import _

from application.community import bp

@bp.route('/events')
def events():
    return render_template("community/events.html", title=_('Events'))

@bp.route('/directory')
def directory():
    return render_template("community/directory.html", title=_('Directory'))

@bp.route('/training_notes')
def training_notes():
    return render_template("community/training_notes.html", title=_('Training Notes'))
