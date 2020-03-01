from threading import Thread

from flask import render_template
from flask_mail import Message

from application import app, mail

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
    mail.send(msg)
    # runs in background thread
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[Microblog] Reset Your Password',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt', user=user, token=token),
        html_body=render_template(
            'email/reset_password.html', user=user, token=token))
