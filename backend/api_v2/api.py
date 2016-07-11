from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

# -- AUTH --

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username=username
        self.password=password
        
users_table = {'test': User(1, 'test', 'test')}

def authenticate(username, password):
    user = users_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return users_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)


# -- end AUTH --

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/', methods=['GET'])
def main():
    return 'test'