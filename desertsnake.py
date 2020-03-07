"""
Main application module

Never run Flask in debug mode on production server; the debugger allows the user
to remotely execute code in the server. Reloader in debug mode automatically
restarts application when a source file is modified.

To debug (does not work in pythonanywhere; stop Flask first):
$ export FLASK_DEBUG=1
$ flask run

running --flask help will list commands and additional cli commands
"""

from application import create_app, db, cli
from application.models import User, Post

app = create_app()
cli.register(app)

"""
Adds shell reference name and items to shell; pre-imports
$ flask shell
"""

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
