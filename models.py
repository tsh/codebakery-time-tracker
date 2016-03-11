import datetime

from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer)
    username = db.Column(db.String(64), primary_key=True)
    records = db.relationship('Record', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))
    ticket = db.Column(db.Integer)
    time_spent = db.Column(db.Numeric(precision=3))
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
