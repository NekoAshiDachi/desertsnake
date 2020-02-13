from flask import render_template, flash, redirect, url_for, request
from application import app, db
from application.forms import LoginForm, RegistrationForm, EditProfileForm
from werkzeug.urls import url_parse

# ------------------------------------------------------------------------------
from datetime import datetime

# registers decorated function to be executed before view function
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # user_loader in models puts target user into db session
        db.session.commit()

# ------------------------------------------------------------------------------

"""current_user can be used at any time during handling to obtain user object;
read through user loader callback in application.models"""
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User

# creates an association between the URL given as an argument and the function;
# associates the URLs / and /index to this function

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
    {
        'author': {'username': 'Skye'},
        'body': 'There is darkness before light'
    },
    {
        'author': {'username': 'Skye'},
        'body': 'Which wipes day\'s glare from weary eyes'
    } ]

    # render_template() invokes the Jinja2 template engine that comes bundled
    # with the Flask framework, substituting {{ ... }} blocks with the
    # corresponding values, given by the arguments provided in the
    # render_template() call.
    return render_template('index.html', title='Home', posts=posts)

# ------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------

# Flask accepts <text> dynamic component, also defined in base.html
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)