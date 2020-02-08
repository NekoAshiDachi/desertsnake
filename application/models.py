from datetime import datetime
from application import db

# in python prompt:
# from app import db
# from app.models import <table1>, <table2>
# u = Model(<column1>='<value1>', <column2>='<value2>')
# db.session.add(u)
# db.session.commit()  writes all changes to db at once
# db.session.rollback()  aborts session and removes changes stored in it

# Flask models typically defined with uppercase character
# SQLAlchemy uses lowercase characters or snake case for multi-word models
# db.ForeignKey() uses SQLAlchemy case
# db.relationship() uses Flask model case

class User(db.Model):
    # unique/index flags optimize db searches
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))  # indirect password

    # db.relationship() is a view and defined on "one" side of "one-to-many"
    # backref = name of field added to "many" objects pointing back to "one"
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # how class will print
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # can set default time zone to UTC in MySQL config
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

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
