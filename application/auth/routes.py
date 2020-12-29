"""Flask passes url_for(**kwargs) in to URL query args; request.args returns
k-v pairs after ? in URL"""
from flask import render_template, redirect, url_for, flash, request

"""current_user can be used at any time during handling to obtain user object;
read through user loader callback in application.models"""
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _

from application import db
from application.auth import bp

from application.auth.forms import (
    LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm)

from application.models import User
from application.auth.reset_email import send_password_reset_email

# ==============================================================================

# The HTTP protocol states that GET requests are those that return information
# to the client (the web browser in this case). POST requests are typically used
# when the browser submits form data to the server

# overrides default, which is to accept only GET requests.
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    # form.validate_on_submit() returns True if all fields are valid, otherwise
    # form renders back to user
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))

        # login_user comes from Flask-Login; sets current_user to user
        login_user(user, remember=form.remember_me.data)

        # Flask's request = data client sent
        next_page = request.args.get('next')

        # url_parse check ensures only relative redirect, protecting against
        # inserted URLs
        if not next_page or url_parse(next_page).netloc != '':
            # redirect URL /login?next=/<this_view>
            next_page = url_for('main.index')

        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/reset_password_request.html', title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
