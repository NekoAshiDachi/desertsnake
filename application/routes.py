from datetime import datetime

"""Flask passes url_for(**kwargs) in to URL query args; request.args returns
k-v pairs after ? in URL"""
from flask import render_template, flash, redirect, url_for, request, g
from flask_babel import get_locale

"""current_user can be used at any time during handling to obtain user object;
read through user loader callback in application.models"""
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from application import app, db

from application.forms import (
    LoginForm, RegistrationForm, EditProfileForm, PostForm,
    ResetPasswordRequestForm, ResetPasswordForm)

from application.models import User, Post
from application.email import send_password_reset_email

# ------------------------------------------------------------------------------

# registers decorated function to be executed before view function
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # user_loader in models puts target user into db session
        db.session.commit()
    # adds language code to base template through flask_babel's get_locale()
    g.locale = str(get_locale())

# INDEX ------------------------------------------------------------------------

"""creates an association between the URL given as an argument and the function;
associates the URLs / and /index to this function

paginate() = Flask-SQLAlchemy obj method returning Pagination obj; P.items
returns list of requested page's items; error_out=True returns 404 error when
out-of-range page requested, and if false, returhs empty list"""

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))

    # pagination

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    """render_template() invokes the Jinja2 template engine that comes bundled
    with the Flask framework, substituting {{ ... }} blocks with the
    corresponding values, given by the arguments provided in the
    render_template() call."""
    return render_template(
        'index.html', title='Home', form=form, posts=posts.items,
        next_url=next_url, prev_url=prev_url)

# LOGIN ------------------------------------------------------------------------

# The HTTP protocol states that GET requests are those that return information
# to the client (the web browser in this case). POST requests are typically used
# when the browser submits form data to the server

# overrides default, which is to accept only GET requests.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # form.validate_on_submit() returns True if all fields are valid, otherwise
    # form renders back to user
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # login_user comes from Flask-Login; sets current_user to user
        login_user(user, remember=form.remember_me.data)

        # Flask's request = data client sent
        next_page = request.args.get('next')

        # url_parse check ensures only relative redirect, protecting against
        # inserted URLs
        if not next_page or url_parse(next_page).netloc != '':
            # redirect URL /login?next=/<this_view>
            next_page = url_for('index')

        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template(
        'reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# PROFILES ---------------------------------------------------------------------

# Flask accepts <text> dynamic component, also defined in base.html
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# FOLLOWING ---------------------------------------------------------------------

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}!')
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}.')
    return redirect(url_for('user', username=username))

# EXPLORE ----------------------------------------------------------------------

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("index.html", title='Explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)

