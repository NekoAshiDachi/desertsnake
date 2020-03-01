import os
basedir = os.path.abspath(os.path.dirname(__file__))

# provides single place for adjustments
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'

    # 'mysql://username:password@localhost/db_name')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://desertsnake:watashinokatawaempi' + \
        '@desertsnake.mysql.pythonanywhere-services.com/desertsnake$shotokan_scholar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['covrev.skynet@gmail.com']

    POSTS_PER_PAGE = 25