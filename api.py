from flask import jsonify, Blueprint

api = Blueprint('api', __name__, url_prefix='/api/')


@api.route('hello')
def hello():
    return 'hello'
