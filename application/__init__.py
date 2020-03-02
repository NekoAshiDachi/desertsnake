from flask import Flask, request
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

"""allows bootstrap/base.html template to be referenced with extends clause;
template exports some blocks for derived templates such as title/navbar/content
(https://pythonhosted.org/Flask-Bootstrap/basic-usage.html#available-blocks)
"""
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

# ------------------------------------------------------------------------------

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# ------------------------------------------------------------------------------

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

# creates application object as instance of class Flask imported from flask
# package; sets to name of the module in which it is used
app = Flask(__name__)
app.config.from_object(Config)

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)
# test py mail server
# $ python -m smtpd -n -c DebuggingServer localhost:8025
# $ export MAIL_SERVER=localhost
# $ export MAIL_PORT=8025

bootstrap = Bootstrap(app)

# all templates must include moment.js (added in base.html)
moment = Moment(app)

babel = Babel(app)

"""selects language to use for request; Flask.request.accept_languages works with
HTTP Accept-Language header (specifies browser language and locale preferences as
weighted list) that clients send with a request

_(text) translates text in the language selected by localeselector to;
lazy_gettext() provides lazy evaluation of text so that transalation occurs only
when text is used

Once all the _() and _l() are in place and a babel.cfg (tells pybabel what
files should be scanned for translatable texts) created, the below command
extracts them to a .pot file; -k flag indicates other text markers (_l for lazy
evaluation)
$ pybabel extract -F babel.cfg -k _l -o messages.pot ."""
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

"""creates translation folder and file where Flask_babel expects translation
files by default; command can be repeated for other languages; most popular .po
editor is poedit; uses base language for missing translations
$ pybabel init -i messages.pot -d application/translations -l es

compiles translations as messages.mo, which Flask-Babel uses to load
translations; can recompile if more translations added
$ pybabel compile -d application/translations

create new .pot and merges it with all .po files; useful if adding _(); can then
add translations and recompile
$ pybabel update -i messages.pot -d app/translations
"""

# LOGIN ------------------------------------------------------------------------

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
login = LoginManager(app)
login.login_view = 'login'  # endpoint name for login view (for url_for() call)

# overrides Flask-Login's default English redirect message
login.login_message = _l('Please log in to access this page.')

# EMAIL ------------------------------------------------------------------------

"""Python's SMTP debugging server is a fake email server that accepts emails,
but instead of sending them, prints them to the console. To run this server,
open a second terminal session and run the following command on it:
$ python -m smtpd -n -c DebuggingServer localhost:8025
Return to your first terminal (use set instead of export if using Windows):
$ export MAIL_SERVER=localhost
$ export MAIL_PORT=8025
Make sure FLASK_DEBUG = 0 or is not set at all; run the application and trigger
the SQLAlchemy error to see how the second terminal session shows an email with
the full stack trace of the error. Security features in actual email accounts
may prevent the application from sending emails through it unless the account
explicitly allows "less secure apps" access to the account. """

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
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

        # ensures log files don't grow too large
        file_handler = RotatingFileHandler(
            'logs/microblog.log', maxBytes=10240, backupCount=10)

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

# ------------------------------------------------------------------------------

from application import routes, models, errors