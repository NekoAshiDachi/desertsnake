from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

# creates application object as instance of class Flask imported from flask
# package; sets to name of the module in which it is used
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
migrate = Migrate(app, db)

from application import routes, models