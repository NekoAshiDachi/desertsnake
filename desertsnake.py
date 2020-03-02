# Main application module
from application import app, db

# running --flask help will list the translate command
from application import cli

# To run:
# export shares defined variables and functions shared with new processes
# $ export FLASK_APP=desertsnake.py
# $ flask run

"""
# Never run Flask in debug mode on production server; the debugger allows the
user to remotely execute code in the server. Reloader in debug mode automatically
restarts application when a source file is modified.
To debug (does not work in pythonanywhere; stop Flask first):
$ export FLASK_DEBUG=1
$ flask run"""

from application.models import User, Post

# Adds shell reference name and items to shell; as if imported
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# $ flask shell