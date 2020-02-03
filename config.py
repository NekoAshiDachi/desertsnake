import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'

    # 'mysql://username:password@localhost/db_name')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://desertsnake:watashinokatawaempi' + \
        '@desertsnake.mysql.pythonanywhere-services.com/desertsnake$shotokan_scholar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
