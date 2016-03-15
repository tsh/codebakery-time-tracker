from flask import jsonify, Blueprint, url_for, request

from app import create_app, db
from models import User, Record

app = create_app()

users_api = Blueprint('users_api', __name__, url_prefix='/api/users')
records_api = Blueprint('records_api', __name__, url_prefix='/api/reports/')

@users_api.route('/', methods=['GET'])
def users():
    return jsonify({'users': [user.get_url() for user in User.query.all()]})


@users_api.route('<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


@records_api.route('/', methods=['POST'])
def create_report():
    record = Record()
    record.import_data(request.json)
    db.session.add(record)
    db.session.commit()
    return jsonify({}), 201, {'Location': record.get_url()}