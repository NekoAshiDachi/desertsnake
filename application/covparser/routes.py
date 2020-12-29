import sys
from flask import render_template, Response, request, flash, redirect
from flask_login import login_required
from time import sleep

from application.covparser import bp
from application.covparser.forms import ClientLinkForm

sys.path.append(r'./application/scripts/')
from cov_parser import get_client_covs


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
# @login_required
def index():
    form = ClientLinkForm()

    # TODO receive form URL and send to new route to execute covparser py
    if request.method == 'POST':
        submission = request.form
        client_url = submission.get('url')

        covs = get_client_covs(client_url)

        # clears log file
        # with open('./application/static/logs/covparser.log', 'w'):
        #     pass
        #
        # sec_doc = Sec_Doc(client_url)
        # covenants = models.find_covs(sec_doc)
        # return covenants

    return render_template("covparser/index.html", title='Covenant Classifier', form=form)
