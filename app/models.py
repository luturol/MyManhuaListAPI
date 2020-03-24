from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    first_access = db.Column(db.String(1))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name = db.Column(db.String(256))
    chapter = db.Column(db.Integer)
    state = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.name)