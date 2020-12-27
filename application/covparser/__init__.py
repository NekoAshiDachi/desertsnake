from flask import Blueprint

bp = Blueprint('covparser', __name__)

from application.covparser import routes
