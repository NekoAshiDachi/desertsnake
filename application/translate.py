import json
import requests
from flask import current_app
from flask_babel import _

def translate(text, source_language, dest_language):
    if 'SYSTRAN_TRANSLATOR_KEY' not in current_app.config \
        or not current_app.config['SYSTRAN_TRANSLATOR_KEY']:
        return _("%s Error: the translation service is not configured." %
        current_app.config['SYSTRAN_TRANSLATOR_KEY'])

    host = "systran-systran-platform-for-language-processing-v1.p.rapidapi.com"
    translate_path = "/translation/text/translate"

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': current_app.config['SYSTRAN_TRANSLATOR_KEY']}

    querystring = {
        "source": source_language, "target": dest_language, "input": text}

    response = requests.request(
        "GET", 'https://'+host+translate_path, headers=headers, params=querystring)

    if response.status_code != 200:
        return _('Error %s: the translation service failed.' % response.status_code)

    return json.loads(response.text)['outputs'][0]['output']
