import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# provides single place for adjustments
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # must be True if order to log new db rows in whoosh index
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    MAX_SEARCH_RESULTS = 50

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['covrev.skynet@gmail.com']

    LANGUAGES = ['en', 'es']
    SYSTRAN_TRANSLATOR_KEY = os.environ.get('SYSTRAN_TRANSLATOR_KEY')

    POSTS_PER_PAGE = 25

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
