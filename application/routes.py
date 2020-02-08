from flask import render_template, flash, redirect
from application import app
from application.forms import LoginForm


# creates an association between the URL given as an argument and the function;
# associates the URLs / and /index to this function

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jamie'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


# The HTTP protocol states that GET requests are those that return information
# to the client (the web browser in this case). POST requests are typically used
# when the browser submits form data to the server

# overrides default, which is to accept only GET requests.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # form.validate_on_submit() returns True if all fields are valid, otherwise
    # form renders back to user
    if form.validate_on_submit():

        # Flask stores the message, but it  will not magically appear in web pages
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")

        # instructs web browser to automatically navigate to different page
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)