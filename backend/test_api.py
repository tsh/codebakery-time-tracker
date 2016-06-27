import unittest

import flask


app = flask.Flask(__name__)
app.config.from_object('config.TestConfig')


class TestUsers(unittest.TestCase):
    def setUp(self):
        ctx = app.app_context()
        ctx.push()
        self.client = app.test_client()
        
    def test(self):
        import ipdb; ipdb.set_trace()        

if __name__ == '__main__':
    unittest.main()