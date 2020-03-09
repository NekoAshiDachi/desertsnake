from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app

# ------------------------------------------------------------------------------
"""
Flask-Login requires is_authenticated (True if valid credentials), is_active
(True if user account active), is_anonymous (True if anon user), get_id()
(returns unique str user ID); these are provided with UserMixin

Each logged-in user has a Flask user session (assigned storage space), and each
time the user navigates to a new page, Flask-Login retrieves the user id from the
session and loads the user into memory. A user loader function bridging the DB
and the Flask-Login extension is also required."""
from flask_login import UserMixin

# ------------------------------------------------------------------------------
"""
installed with Flask; password hash has no known reverse operation and can has
same password with different hashes"""
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------------------------------------------------------------

import jwt
from application import db, login

# ==============================================================================
"""
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

# ------------------------------------------------------------------------------

# Auxiliary/association table with no data other than foreign keys; does not
# need Model class
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')) )


class User(UserMixin, db.Model):
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

    """
    - links User to Users followed; secondary=association table defined below;
      lazy=dynamic means query not run until requested
    - Model.relationship is like list; can append and remove"""
    followed = db.relationship('User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ------------------------------------------------------------------------------

class Post(db.Model):
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

# ------------------------------------------------------------------------------

class Chronology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text)
    media = db.Column(db.String(125))
    media_credit = db.Column(db.String(125))
    media_caption = db.Column(db.Text)
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

class Dojo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer)
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

class Glossary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(25))
    translation = db.Column(db.String(25))
    kanji = db.Column(db.String(25))
    type = db.Column(db.String(25))
    notes= db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Kata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    kanji = db.Column(db.String(25))
    parent_kata_id = db.Column(db.Integer, db.ForeignKey('kata.id'))
    child_kata_id = db.Column(db.Integer, db.ForeignKey('kata.id'))
    creator_person_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Kata_style_org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style_id = db.Column(db.Integer)
    org_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(25))
    name = db.Column(db.String(25))
    japaneseName = db.Column(db.String(25))
    kanji = db.Column(db.String(25))
    start_date = db.Column(db.DateTime)
    style_id = db.Column(db.Integer)
    headInstructor_person_id = db.Column(db.Integer)
    president_person_id = db.Column(db.Integer)
    honbu_dojo_id = db.Column(db.Integer)
    logo = db.Column(db.String(25))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25))
    lastName = db.Column(db.String(25), nullable=False)
    altLastName = db.Column(db.String(25))
    DoB =db.Column(db.DateTime)
    DoD =db.Column(db.DateTime)
    style_id = db.Column(db.Integer)
    org_id = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    pic = db.Column(db.String(25))
    bio = db.Column(db.Text)
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

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    country_id = db.Column(db.Integer)
    code = db.Column(db.String(2))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    kanji = db.Column(db.String(25), unique=True)
    start_date = db.Column(db.String(25))
    founder_person_id = db.Column(db.Integer)
    notes= db.Column(db.Text)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, nullable=False)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
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
