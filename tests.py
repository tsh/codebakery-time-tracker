import base64
import datetime
import unittest

from flask import url_for, json

from app import create_app, db
from models import User, Record, Project
from api import users_api, records_api, auth_api, projects_api

app = create_app()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SERVER_NAME'] = 'test'
        ctx = app.app_context()
        ctx.push()
        db.init_app(app)
        db.create_all()
        self.user = User(username="test")
        self.user.set_password('test')
        db.session.add(self.user)
        db.session.commit()
        self.client = app.test_client()

    def test_users(self):
        user = User(username="username")
        db.session.add(user)
        db.session.commit()
        resp = self.client.get('api/users/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(url_for('users_api.get_user', id=user.id), str(resp.data))

    def test_get_records(self):
        record = Record()
        db.session.add(record)
        db.session.commit()
        resp = self.client.get('api/records/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(record.get_url(), str(resp.data))

    def test_create_record(self):
        record_data = {'description': 'test description',
                       'time_spent': 4,
                       'ticket': 22,
                       'date': '2016-03-18'
                       }
        resp = self.client.post('api/records/', data=json.dumps(record_data),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 201)
        record = Record.query.all()[0]
        self.assertEqual(record.description, record_data['description'])
        self.assertEqual(record.time_spent, record_data['time_spent'])
        self.assertEqual(record.ticket, record_data['ticket'])
        self.assertEqual(record.date, datetime.date(2016, 3, 18))
        self.assertEqual(record.user.id, self.user.id)

    def test_create_project(self):
        project_data = {'name': 'new project'}
        resp = self.client.post('api/projects/', data=json.dumps(project_data),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 201)
        project = Project.query.all()[0]
        self.assertEqual(project.name, project_data['name'])


    def test_get_token(self):
        resp = self.client.get('api/auth/', headers={'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', str(resp.data))

    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    app.register_blueprint(users_api)
    app.register_blueprint(records_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(projects_api)
    unittest.main()
