import datetime

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, create_app

app = create_app()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    records = db.relationship('Record', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User: {}>".format(self.username)

    # AUTH & REGISTRATION

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(token)
        return User.query.get(data['id'])

    def get_url(self):
        return url_for('users_api.get_user', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'username': self.username
        }


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))
    ticket = db.Column(db.Integer)
    time_spent = db.Column(db.Numeric(precision=3))
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def import_data(self, data):
        self.description = data['description']
        self.time_spent = data['time_spent']
        return self

    def get_url(self):
        # TODO: implement me
        return 'not implemented'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
