# provides alternative way for non-web browser clients to log in

from flask import jsonify, g
from application import db
from application.api import bp
from application.api.auth import basic_auth, token_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

"""
(venv) $ http POST http://localhost:5000/api/tokens -> unauthorized
(venv) $ http --auth <username>:<password> POST http://localhost:5000/api/tokens -> authorized

HTTPie doesn't directly support bearer token, so Authorization header needs to be provided:
(venv) $ http GET http://localhost:5000/api/users/1 "Authorization:Bearer pC1Nu9wwyNt8VCj1trWilFdFI276AcbS"
"""

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204 # request has no body; 204 code for successful requests with no body