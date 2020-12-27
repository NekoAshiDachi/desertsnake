from flask import render_template, Response, request, flash, redirect
from flask_login import login_required

from application.covparser import bp
from application.covparser.forms import ClientLinkForm
from application.scripts.cov_parser.webscrape import logger
from application.scripts.cov_parser.run_web import get_client_covs

from time import sleep

def covparser_logger():
    with open("./application/static/logs/covparser.log") as log_info:
        data = log_info.read()
        yield data.encode()
        sleep(1)

@bp.route("/stream_logger", methods=["GET"])
def stream_logger():
    # stream log to route
    return Response(covparser_logger(), mimetype="text/plain", content_type="text/event-stream")

# ----------------------------------------------------------------------------------------------------------------------

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ClientLinkForm()

    # TODO receive form URL and send to new route to execute covparser py
    if request.method == 'POST':
        submission = request.form
        flash(f"""raw submission:
            {[k + ' - ' + v for k, v in submission.items() if k not in ('csrf_token', 'submit')]}
            """, 'info')

        client_url = submission.get('url')
        get_client_covs(client_url)

    return render_template("covparser/index.html", title='Index', form=form)
