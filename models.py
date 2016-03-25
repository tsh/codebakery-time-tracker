import datetime

import dateutil.parser

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, create_app

app = create_app()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    username = db.Column(db.String(64))
    records = db.relationship('Record', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

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

    # Other

    def get_url(self):
        return url_for('users_api.get_user', id=self.id, _external=True)

    def import_data(self, data):
        self.username = data['username']
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'username': self.username
        }


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    date = db.Column(db.Date)
    ticket = db.Column(db.Integer)
    time_spent = db.Column(db.Numeric(precision=3))
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def import_data(self, data):
        self.description = data['description']
        self.time_spent = data['time_spent']
        self.ticket = data['ticket']
        self.date = dateutil.parser.parse(data['date'])
        return self

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'user': self.user,
            'project': self.project_id,
            'date': self.date,
            'ticket': self.ticket,
            'time_spent': self.time_spent,
            'description': self.description
        }

    def get_url(self):
        return url_for('records_api.record_detail', id=self.id, _external=True)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def import_data(self, data):
        self.name = data['name']
        return self

    def export_data(self):
        return {
            'name': self.name
        }

    def get_url(self):
        # TODO: implement me
        return 'not implemented'


class DayOff(db.Model):
    """
    Which day is counted as day off. Holiday, weekends, etc.
    """
    __tablename__ = 'days_off'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    description = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))