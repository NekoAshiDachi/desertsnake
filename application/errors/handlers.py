from flask import render_template
from application import db
from application.errors import bp

#  Successful view function second return value by default is 200
# same as @app.errorhandler, but @bp.app_errorhandler keeps blueprint independent
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
