from datetime import datetime

from flask import (
    render_template, flash, redirect, url_for, request, g, jsonify, current_app)

from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language

from application import db

from application.main.forms import (
    EditProfileForm, PostForm, SearchForm, MessageForm)

from application.models import User, Post, Message, Notification, o, p
from application.translate import translate
from application.main import bp

# ==============================================================================

# registers decorated function to be executed before view function
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()

        # user_loader in models puts target user into db session
        db.session.commit()

        # g = container for data persisting through life of each client request
        g.search_form = SearchForm()

    # adds language code to base template through flask_babel's get_locale()
    g.locale = str(get_locale())

# INDEX ------------------------------------------------------------------------
"""
creates an association between the URL given as an argument and the function;
associates the URLs / and /index to this function

paginate() = Flask-SQLAlchemy obj method returning Pagination obj; P.items
returns list of requested page's items; error_out=True returns 404 error when
out-of-range page requested, and if false, returhs empty list

@login_required redirects to HTML login page, so problematic for API approach
"""

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))

    # pagination
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None

    """
    render_template() invokes the Jinja2 template engine that comes bundled with
    the Flask framework, substituting {{ ... }} blocks with the corresponding
    values, given by the arguments provided in the render_template() call."""
    return render_template(
        'index.html', title=_('Home'), form=form, posts=posts.items,
        next_url=next_url, prev_url=prev_url)

# EXPLORE ----------------------------------------------------------------------

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        "index.html", title=_('Explore'), posts=posts.items,
        next_url=next_url, prev_url=prev_url)


# PROFILES ---------------------------------------------------------------------

# Flask accepts <text> dynamic component, also defined in base.html
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'user.html', user=user, posts=posts.items,
        next_url=next_url, prev_url=prev_url)

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %{username}s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %{username}s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %{username}s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %{username}s.', username=username))
    return redirect(url_for('main.user', username=username))


# TRANSLATE --------------------------------------------------------------------

@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    """request.form=submission data since not accessed via Flask-WTF; returns
    HTTP response to client as JSON payload"""
    return jsonify({'text': translate(
        request.form['text'], request.form['source_language'],
        request.form['dest_language'])})

# SEARCH --------------------------------------------------------------------

@bp.route('/search')
@login_required
def search():
    """form.validate_on_submit() only works for POST forms; form.validate()
    checks if field values not empty, without checking how data was submitted"""
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))

    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(
        g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])

    # different since Post.search() doesn't return pagination obj
    next_url = url_for('main.search', q=g.search_form.q.data, page=page+1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page-1) \
        if page > 1 else None

    return render_template(
        'search.html', title=_('Search'), posts=posts,
        next_url=next_url, prev_url=prev_url)

# MESSAGE ----------------------------------------------------------------------

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    # marks all messages as read
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None

    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/notifications')
@login_required
def notifications():
    # since comes from client config for notification timing, from request URL
    since = request.args.get('since', 0.0, type=float)

    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_posts', _('Exporting posts...'))
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))

# SHOTOKAN SCHOLAR =============================================================

@bp.route('/faq')
def faq():
    return render_template("faq.html", title=_('Frequently Asked Questions'),
    o=o, p=p)

@bp.route('/about')
def about():
    return render_template("about.html", title=_('About Us'), o=o, p=p)

@bp.route('/partners')
def partners():
    return render_template("partners.html", title=_('Partners'))

@bp.route('/terms_of_use')
def terms_of_use():
    return render_template("terms_of_use.html", title=_('Terms of Use'))

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MessageForm()
    admin=User.query.filter_by(id=1).first()

    if form.validate_on_submit():
        msg = Message(
            author=User.query.filter_by(id=2).first(),
            recipient=User.query.filter_by(id=1).first(),
            body=form.message.data)

        db.session.add(msg)
        admin.add_notification('unread_message_count', admin.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.contact'))
    return render_template('contact.html', title=_('Contact Us'), form=form)


