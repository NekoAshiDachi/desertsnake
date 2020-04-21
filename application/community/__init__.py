from flask import Blueprint

bp = Blueprint('community', __name__)

from application.community import routes
