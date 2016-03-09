from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    records = db.relationship('Record', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))


class Record(db.Model):
    __tablename__ = 'records'


