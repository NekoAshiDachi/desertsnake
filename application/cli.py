from application import app
import os 
import click

@app.cli.group()
def translate():
    """Translation and localization commands."""
    """only exists to provide a base for the sub-commands; standard way in which 
    Click builds group of commands"""
    pass

@translate.command()
def update():
    """Update all languages."""
    # os.system() returns 0 if command runs smoothly
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')