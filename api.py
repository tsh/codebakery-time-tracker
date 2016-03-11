from flask import jsonify, Blueprint, url_for

from app import create_app

app = create_app()

users_api = Blueprint('users_api', __name__, url_prefix='/api/users')


@users_api.route('/')
def users():
    return 'hello'
