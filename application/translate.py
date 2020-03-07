import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if 'SYSTRAN_TRANSLATOR_KEY' not in app.config or \
            not app.config['SYSTRAN_TRANSLATOR_KEY']:
        return _(f"{app.config['SYSTRAN_TRANSLATOR_KEY']} Error: the translation service is not configured.")

    host = "systran-systran-platform-for-language-processing-v1.p.rapidapi.com"
    translate_path = "/translation/text/translate"

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': app.config['SYSTRAN_TRANSLATOR_KEY']}

    querystring = {
        "source": source_language, "target": dest_language, "input": text}

    response = requests.request(
        "GET", 'https://'+host+translate_path, headers=headers, params=querystring)

    if response.status_code != 200:
        return _(f'Error {response.status_code}: the translation service failed.')

    return json.loads(response.text)['outputs'][0]['output']
