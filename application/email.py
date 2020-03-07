from threading import Thread
from flask import current_app
from flask_mail import Message
from application import mail

def send_async_email(app, msg):
    """app context automatically managed by Flask
    allows Flask to avoid passing args/instances across functions
    may need to be manually created for custom threads
    many extensions need to know app instance because their config stored in app.config
    app.app_context() makes app instance accessible via Flask's current_app"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # runs in background thread
    Thread(
        target=send_async_email, args=(current_app._get_current_object(), msg)
    ).start()
