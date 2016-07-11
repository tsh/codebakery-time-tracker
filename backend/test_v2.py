import json
import unittest

import flask

from api_v2.api import app

app.config.from_object('config.TestConfig')


class TestUsers(unittest.TestCase):
    def setUp(self):
        ctx = app.app_context()
        ctx.push()
        self.client = app.test_client()

    def test(self):
        resp = self.client.get('/')
        
        
    def test_get_token(self):
        resp = self.client.post('/auth', data=json.dumps({'username': 'test', 'password': 'test'}), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, 200, msg=str(resp.data))  
        self.assertIn('access_token', str(resp.data))
        


if __name__ == '__main__':
    unittest.main()