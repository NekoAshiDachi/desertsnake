import os
from time import time
from datetime import datetime, timedelta

from hashlib import md5
import json
import base64
from flask import current_app, url_for

""" ----------------------------------------------------------------------------

Flask-Login requires is_authenticated (True if valid credentials), is_active
(True if user account active), is_anonymous (True if anon user), get_id()
(returns unique str user ID); these are provided with UserMixin

Each logged-in user has a Flask user session (assigned storage space), and each
time the user navigates to a new page, Flask-Login retrieves the user id from the
session and loads the user into memory. A user loader function bridging the DB
and the Flask-Login extension is also required."""
from flask_login import UserMixin

"""
installed with Flask; password hash has no known reverse operation and can has
same password with different hashes"""
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
from application import db, login

""" ----------------------------------------------------------------------------

if Elasticsearch used
from application.search import add_to_index, remove_from_index, query_index"""
from application.search import query_index

import redis
import rq

""" ============================================================================

in python prompt:
    # from application import db
    # from application.models import <table1>, <table2>
    # u = Model(<column1>='<value1>', <backref>=<Model_instance>)
    # db.session.add(u); db.session.delete(u)
    # db.session.commit()  writes all changes to db at once
    # db.session.rollback()  aborts session and removes changes stored in it

    # Model.query.all(); Model_instance.backref.all()
    # Model.query.get(<id>)
    # Model.query.order_by(Model.column.desc()).all()
    # Model.query.filter_by(<column>='<value>').first()  1st returns 1st user or None
    # Model.filter(table.c.column == model.column).count() > 0
    # Model.query.join(
        # <Model|Table>,
        (Table.c.col == Model.col)).filter(condition).order_by(Model.col.desc())

# Flask models typically defined with uppercase character
# SQLAlchemy uses lowercase characters or snake case for multi-word models
# db.ForeignKey() uses SQLAlchemy case
# db.relationship() uses Flask model case"""

# ==============================================================================

class SearchableMixin(object):
    @classmethod
    def search(cls, query, page, per_page):
        # cls.__tablename__ = model name as assigned by Flask-SQLAlchemy
        # ids, total = query_index(cls.__tablename__, query, page, per_page)
        ids, total = query_index(cls, query, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0

        when = [(ids[i], i) for i in range(len(ids))]
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

"""for SQLAlchemy-Elasticsearch integration; replaces list of object IDs with
actual objects"""

#     @classmethod
#     def before_commit(cls, session):
#         # saves session objects before they are committed and disappear
#         session._changes = {
#             'add': list(session.new),
#             'update': list(session.dirty),
#             'delete': list(session.deleted)
#         }

#     # updates Elasticsearch index
#     @classmethod
#     def after_commit(cls, session):
#         for obj in session._changes['add']:
#             if isinstance(obj, SearchableMixin):
#                 add_to_index(obj.__tablename__, obj)
#         for obj in session._changes['update']:
#             if isinstance(obj, SearchableMixin):
#                 add_to_index(obj.__tablename__, obj)
#         for obj in session._changes['delete']:
#             if isinstance(obj, SearchableMixin):
#                 remove_from_index(obj.__tablename__, obj)
#         session._changes = None

      # add all data from db
#     @classmethod
#     def reindex(cls):
#         for obj in cls.query:
#             add_to_index(cls.__tablename__, obj)

# db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
# db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """first 3 args Flask-SQLAlchemy query obj, page #, page size"""
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(
                    endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(
                    endpoint, page=page + 1, per_page=per_page, **kwargs
                    ) if resources.has_next else None,
                'prev': url_for(
                    endpoint, page=page - 1, per_page=per_page, **kwargs
                    ) if resources.has_prev else None
            }
        }
        return data

# ------------------------------------------------------------------------------

# Auxiliary/association table with no data other than foreign keys; does not
# need Model class
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')) )


class User(PaginatedAPIMixin, UserMixin, db.Model):
    # unique/index flags optimize db searches
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)

    # indirect password
    password_hash = db.Column(db.String(128))

    """
    db.relationship() is a view and defined on "one" side of "one-to-many"
    backref = name of field added to "many" objects pointing back to "one" """
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    """
    - links User to Users followed; secondary=association table defined below;
      lazy=dynamic means query not run until requested
    - Model.relationship is like list; can append and remove"""
    followed = db.relationship('User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    messages_sent = db.relationship(
        # backref=author uses same logic as for blog posts
        'Message', foreign_keys='Message.sender_id', backref='author',
        lazy='dynamic')
    messages_received = db.relationship(
        'Message', foreign_keys='Message.recipient_id', backref='recipient',
        lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship(
        'Notification', backref='user', lazy='dynamic')

    tasks = db.relationship('Task', backref='user', lazy='dynamic')


    # how class will print
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    """
    Gravatar default size 80x80p; s arg specifies size; d arg predetermines
    avatar; some sites don't accept Gravatar"""
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=monsterid&s={size}"

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    """
    followed gets all users that are followed, then all with follower = user;
    queries Post and returns posts only, rather than all joined columns"""
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        """The dict is the payload written into the token.

        The payload is signed, meaning that an attempt to forge or tamper with
        the payload invalidates the signature, and to generate a new signature
        the secret key is needed.

        The exp field is standard for JWTs and indicates the token's expiration.
        If a token is past expiration, then it will also be invalid."""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # invoked directly from class; doesn't take class as 1st arg
    @staticmethod
    def verify_reset_password_token(token):
        try:
            # algorithm=how to generate token; HS256 is the most widely used
            id = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256']
                )['reset_password']
        except:
            return
        return User.query.get(id)

    # --------------------------------------------------------------------------

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    # updates notification for user; e.g., when notification = # of messages
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue(
            'application.tasks.' + name, self.id, *args, **kwargs)
        task = Task(
            id=rq_job.get_id(), name=name, description=description, user=self)

        """adds task obj to session without committing; best to operate on
        session in higher level functions: can combine lower level updates in
        single transaction"""
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.query.filter_by(
            name=name, user=self, complete=False).first()

    # --------------------------------------------------------------------------

    def to_dict(self, include_email=False):
        """converts model to python representation"""

        data = {
            "id": self.id,
            "username": self.username,

            # +Z since python datetime does not record timezone in state
            "last_seen": self.last_seen.isoformat() + 'Z',

            "about_me": self.about_me,

            # these do not exist as fields in db, but provided to client for convenience
            "post_count": self.posts.count(),
            "follower_count": self.followers.count(),
            "followed_count": self.followed.count(),

            # hypermedia REST reqs; links to current resource, followers/followed, avatar
            "_links": {
                "self": url_for('api.get_user', id=self.id),
                "followers": url_for('api.get_followers', id=self.id),
                "followed": url_for('api.get_followed', id=self.id),
                "avatar": self.avatar(128)
            }
        }
        # only returned when users request own entry
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        """imports fields client can set
        """
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])

        # only when new user registered, as password saved in db as hash
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()

        # check for if current token has at least a minute before expiration
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        # base64 encoding so all characters in readable range
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    # best practice to have strategy to revoke token immediately
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ------------------------------------------------------------------------------

class Post(SearchableMixin, db.Model):
    __tablename__ = 'post'
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # can set default time zone to UTC in MySQL config
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

# ------------------------------------------------------------------------------

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        """
        If job ID not in RQ queue, job already finished and data expired and
        removed from queue, so returns progress as 100%. 2nd dict.get arg is
        default value if no value; assumed job is scheduled but not started yet
        """
        return job.meta.get('progress', 0) if job is not None else 100

# ------------------------------------------------------------------------------

class Style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    kanji = db.Column(db.String(25), unique=True)
    start_date = db.Column(db.String(25))
    founder_person_id = db.Column(db.Integer)
    notes= db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

    orgs = db.relationship('Org', backref='style')

class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(25))
    name = db.Column(db.String(50))
    japaneseName = db.Column(db.String(50))
    kanji = db.Column(db.String(25))
    start_date = db.Column(db.DateTime)
    founder_person_id = db.Column(db.Integer)
    headInstructor_person_id = db.Column(db.Integer)
    president_person_id = db.Column(db.Integer)
    honbu_dojo_id = db.Column(db.Integer)
    logo = db.Column(db.String(25))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

    dojos = db.relationship('Dojo', backref='org')
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25), nullable=False)
    altLastName = db.Column(db.String(25))
    DoB =db.Column(db.DateTime)
    DoD =db.Column(db.DateTime)
    org_id = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    style_id = db.Column(db.Integer)
    pic = db.Column(db.String(25))
    bio = db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

o = lambda id: url_for('library.org', id=id)
p = lambda id: url_for('library.person', id=id),

class Dojo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headInstructor_person_id = db.Column(db.Integer)
    name = db.Column(db.String(125))
    street = db.Column(db.String(125))
    city = db.Column(db.String(125))
    zip = db.Column(db.String(125))
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    siteURL = db.Column(db.String(125), unique=True)
    email = db.Column(db.String(125), unique=True)
    phone = db.Column(db.Integer, unique=True)
    fax = db.Column(db.Integer, unique=True)
    mapURL = db.Column(db.String(125))
    isCountryHQ = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

    org_id = db.Column(db.Integer, db.ForeignKey('org.id'))

class Glossary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(25))
    translation = db.Column(db.String(25))
    kanji = db.Column(db.String(25))
    type = db.Column(db.String(25))
    notes= db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Drill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Kata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    kanji = db.Column(db.String(25))
    parent_kata_id = db.Column(db.Integer, db.ForeignKey('kata.id'))
    child_kata_id = db.Column(db.Integer, db.ForeignKey('kata.id'))
    history = db.Column(db.Text)
    tips = db.Column(db.Text)
    creator_person_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, primary_key=True)
    table_inner_id = db.Column(db.Integer, primary_key=True)
    style_id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, primary_key=True)
    performer_person_id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(50), unique=True)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author_person_id = db.Column(db.String(25))
    publisher = db.Column(db.String(25))
    format = db.Column(db.String(25))
    year = db.Column(db.String(25))
    store_link = db.Column(db.String(50))
    cover_link = db.Column(db.String(50))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), unique=True)
    ISO = db.Column(db.String(3), unique=True)
    ISO3 = db.Column(db.String(3), unique=True)
    code = db.Column(db.String(3), unique=True)
    phone_code = db.Column(db.String(4))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

    states = db.relationship('State', backref='country')

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    country_id = db.Column(db.Integer)
    code = db.Column(db.String(2))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

# categories, or relational table cross-reference--necessary?
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Kata_style_org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style_id = db.Column(db.Integer)
    org_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)
