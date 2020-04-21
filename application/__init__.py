import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# ------------------------------------------------------------------------------

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# ------------------------------------------------------------------------------
"""Python's SMTP debugging server accepts emails, but instead of sending emails,
prints them to the console.

To run this server:
    Open a 2nd terminal session:
    $ python -m smtpd -n -c DebuggingServer localhost:8025

    And in the 1st terminal (using set instead of export in Windows):
    $ export MAIL_SERVER=localhost
    $ export MAIL_PORT=8025

    Make sure FLASK_DEBUG = 0 or is not set at all; run the application and
    trigger an SQLAlchemy error to see how the second terminal session shows an
    email with the full stack trace of the error.

Security features in actual email accounts may prevent the application from
sending emails through it unless the account explicitly allows "less secure
apps" access to the account or two-factor authorization."""

from flask_mail import Mail

# ------------------------------------------------------------------------------
"""allows bootstrap/base.html template to be referenced with extends clause;
template exports some blocks for derived templates such as title/navbar/content
(https://pythonhosted.org/Flask-Bootstrap/basic-usage.html#available-blocks)
"""
from flask_bootstrap import Bootstrap

# all templates must include moment.js (added in base.html)
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config

from redis import Redis
import rq

db = SQLAlchemy()
migrate = Migrate()

# ------------------------------------------------------------------------------
login = LoginManager()

# endpoint name for login view (for url_for() call)
login.login_view = 'auth.login'

# overrides Flask-Login's default English redirect message
login.login_message = _l('Please log in to access this page.')

# ------------------------------------------------------------------------------

mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()

# ==============================================================================

def create_app(config_class=Config):
    """
    creates application object as instance of class Flask imported from flask
    package; __name__ = name of this module"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Elasticsearch([app.config['ELASTICSEARCH_URL']]) if...
    app.search = app.config['WHOOSH_BASE'] if app.config['WHOOSH_BASE'] \
        else None

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('tasks', connection=app.redis)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from application.errors import bp as errors_bp
    """when blueprint registered, any view functions, templates, static files,
    error handlers, etc. are connected to the application"""
    app.register_blueprint(errors_bp)

    """When blueprint route defined, must pass blueprint_name.view_function_name;
    url_for('login') becomes url_for('auth.login'); optional url_prefix arg adds
    prefix before blueprint route"""
    from application.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from application.main import bp as main_bp
    app.register_blueprint(main_bp)

    from application.library import bp as library_bp
    app.register_blueprint(library_bp, url_prefix='/library')

    from application.community import bp as community_bp
    app.register_blueprint(community_bp, url_prefix='/community')

    from application.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

# ------------------------------------------------------------------------------
"""
selects language to use for request; Flask.request.accept_languages works with
HTTP Accept-Language header (specifies browser language and locale preferences
as weighted list) that clients send with a request

_(text) translates text in the language selected by localeselector to;
lazy_gettext() provides lazy evaluation of text so that translation occurs only
when text is used

Once all the _() and _l() are in place and a babel.cfg (tells pybabel what
files should be scanned for translatable texts) created, the below command
extracts them to a .pot file; -k flag indicates other text markers (_l for lazy
evaluation)
$ pybabel extract -F babel.cfg -k _l -o messages.pot ."""

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

"""creates translation folder and file where Flask_babel expects translation
files by default; command can be repeated for other languages; most popular .po
editor is poedit; uses base language for missing translations
$ pybabel init -i messages.pot -d application/translations -l es

compiles translations as messages.mo, which Flask-Babel uses to load
translations; can recompile if more translations added
$ pybabel compile -d application/translations

create new .pot and merges it with all .po files; useful if adding _(); can then
add translations and recompile
$ pybabel update -i messages.pot -d application/translations"""

# ------------------------------------------------------------------------------

from application import models
