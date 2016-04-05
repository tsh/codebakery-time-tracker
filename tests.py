import base64
import datetime
import unittest

from flask import url_for, json

from app import create_app, db
from app.models import User, Record, Project
from app.api import users_api, records_api, auth_api, projects_api
from config import TestConfig


app = create_app(TestConfig())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SERVER_NAME'] = 'test'


class TestUsers(unittest.TestCase):
    def setUp(self):
        ctx = app.app_context()
        ctx.push()
        db.init_app(app)
        db.create_all()
        self.user = User(username="test")
        self.user_password = 'test'
        self.user.set_password(self.user_password)
        db.session.add(self.user)
        db.session.commit()
        self.client = app.test_client()

    def test_get_users(self):
        user = User(username="username")
        db.session.add(user)
        db.session.commit()
        resp = self.client.get('api/users/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(url_for('users_api.get_user', id=self.user.id), str(resp.data))

    def test_post_users(self):
        user_data = {
            'username': 'new_user'
        }
        resp = self.client.post('api/users/', data=json.dumps(user_data),
                                headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(1, len(db.session.query(User).filter(User.username == user_data['username']).all()))

    def test_user_detail(self):
        resp = self.client.get('/api/users/{}'.format(self.user.id))
        self.assertEqual(resp.status_code, 200, msg=resp.data)
        self.assertIn(self.user.username, str(resp.data))

    def test_get_token(self):
        resp = self.client.get('api/auth/', headers={'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', str(resp.data))

    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()


class TestUserChangePassword(unittest.TestCase):
    def setUp(self):
        ctx = app.app_context()
        ctx.push()
        db.init_app(app)
        db.create_all()
        self.user = User(username="test")
        self.user_password = 'test'
        self.user.set_password(self.user_password)
        db.session.add(self.user)
        db.session.commit()
        self.client = app.test_client()

    def test_change_password(self):
        new_password = 'new_password'
        self.assertFalse(self.user.verify_password(new_password))
        resp = self.client.post('api/users/{}/change-password/'.format(self.user.id),
                                data=json.dumps({'password': self.user_password,
                                                 'new_password': new_password}),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 205, msg=resp.data)
        self.assertTrue(self.user.verify_password(new_password))

    def test_change_password_for_other_user_not_allowed(self):
        other_user = User(username='other_user')
        other_user_password = 'other_user_password'
        other_user.set_password(other_user_password)
        db.session.add(other_user)
        db.session.commit()
        resp = self.client.post('api/users/{}/change-password/'.format(self.user.id),
                                data=json.dumps({'password': other_user_password,
                                                 'new_password': 'some_password'}),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(other_user.verify_password(other_user_password))


    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()


class TestRecords(unittest.TestCase):
    def setUp(self):
        ctx = app.app_context()
        ctx.push()
        db.init_app(app)
        db.create_all()
        self.user = User(username="test")
        self.user.set_password('test')
        db.session.add(self.user)
        db.session.commit()
        self.client = app.test_client()

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

    def test_record_detail(self):
        record = Record(time_spent=8.5)
        db.session.add(record)
        db.session.commit()
        resp = self.client.get('api/records/{}'.format(record.id))
        self.assertEqual(resp.status_code, 200, msg=resp.data)
        self.assertIn(str(record.time_spent), str(resp.data))

    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()


class TestProjects(unittest.TestCase):
    def setUp(self):
        ctx = app.app_context()
        ctx.push()
        db.init_app(app)
        db.create_all()
        self.user = User(username="test")
        self.user.set_password('test')
        db.session.add(self.user)
        db.session.commit()
        self.client = app.test_client()

    def test_create_project(self):
        project_data = {'name': 'new project'}
        resp = self.client.post('api/projects/', data=json.dumps(project_data),
                                headers={'Content-Type': 'application/json',
                                         'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 201)
        project = Project.query.all()[0]
        self.assertEqual(project.name, project_data['name'])

    def test_project_detail(self):
        project = Project(name='prj')
        db.session.add(project)
        db.session.commit()
        resp = self.client.get('/api/projects/{}'.format(project.id), headers={'Content-Type': 'application/json',
                                         'Authorization': b'Basic ' + base64.b64encode(b'test:test')})
        self.assertEqual(resp.status_code, 200, msg=resp.data)
        self.assertIn(project.name, str(resp.data))

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
