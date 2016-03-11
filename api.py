from flask import jsonify, Blueprint, url_for

from app import create_app
from models import User

app = create_app()

users_api = Blueprint('users_api', __name__, url_prefix='/api/users')


@users_api.route('/', methods=['GET'])
def users():
    return jsonify({'users': [user.get_url() for user in User.query.all()]})


@users_api.route('<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())
