import datetime

import dateutil.parser

from flask import url_for, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, create_app, api



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<User: {}>".format(self.username)

    # AUTH & REGISTRATION

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def change_password(self, old_password, new_password):
        if self.verify_password(old_password):
            self.set_password(new_password)
        else:
            abort(403)  # TODO: it should return json

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token)
        return User.query.get(data['id'])

    # Other

    def get_url(self):
        from app.api import UserDetails
        return api.url_for(UserDetails, id=self.id, _external=True)

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
    user = relationship('User', backref='record_set')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = relationship('Project', backref='record_set')
    date = db.Column(db.Date)
    ticket = db.Column(db.Integer)
    time_spent = db.Column(db.Numeric(precision=3))
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def import_data(self, data):
        self.time_spent = data['time_spent']
        self.ticket = data.get('ticket')
        if isinstance(data.get('date'), datetime.date):
            self.date = data['date']
        else:
            self.date = dateutil.parser.parse(data['date']) if 'date' in data else None
        self.description = data['description']
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
        return url_for('api_v1.record_detail', id=self.id, _external=True)


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