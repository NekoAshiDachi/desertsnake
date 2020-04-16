from flask import render_template, request
from application import db
from application.errors import bp
from application.api.errors import error_response as api_error_response

#  Successful view function second return value by default is 200
# same as @app.errorhandler, but @bp.app_errorhandler keeps blueprint independent
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# content negotiation
def wants_json_response():
    # if JSON rates higher as preferred format than HTML
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500