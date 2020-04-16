from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message

    # returns default status code of 200
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    """most common error in API is code 400, "bad request" (client sent request
    with invalid data)"""
    return error_response(400, message)

