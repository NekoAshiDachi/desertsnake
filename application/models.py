from application import db

class User(db.Model):
    # unique/index flags optimize db searches
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # indirect password
    password_hash = db.Column(db.String(128))

    # how class will print
    def __repr__(self):
        return f'<User {self.username}>'