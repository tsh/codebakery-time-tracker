import unittest

from flask import url_for, json

from app import create_app, db
from models import User, Record
from api import users_api, records_api, auth_api

app = create_app()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SERVER_NAME'] = 'test'
        db.init_app(app)
        with app.app_context():
            db.create_all()
        app.testing = True
        self.client = app.test_client()

    def test_users(self):
        user = User(username="username")
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            resp = self.client.get('api/users/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(url_for('users_api.get_user', id=user.id), str(resp.data))

    def test_create_report(self):
        record_data = {'description': 'test description',
                       'time_spent': 4}
        resp = self.client.post('api/reports/', data=json.dumps(record_data),
                                headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, 201)
        with app.app_context():
            record = Record.query.all()[0]
            self.assertEqual(record.description, record_data['description'])
            self.assertEqual(record.time_spent, record_data['time_spent'])

    def test_get_token(self):
        resp = self.client.get('api/auth/')
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    app.register_blueprint(users_api)
    app.register_blueprint(records_api)
    app.register_blueprint(auth_api)
    unittest.main()
