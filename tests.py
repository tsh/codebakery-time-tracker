import unittest

from app import create_app, db
from models import User

app = create_app()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        with app.app_context():
            db.create_all()
        self.client = app.test_client()

    def test_smth(self):
        resp = self.client.get('api/users/')
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
