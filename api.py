from flask import jsonify, Blueprint, url_for, request, g
from flask.ext.httpauth import HTTPBasicAuth
import itsdangerous

from app import create_app, db
from models import User, Record


app = create_app()
auth = HTTPBasicAuth()

users_api = Blueprint('users_api', 'users_api', url_prefix='/api/users/')
records_api = Blueprint('records_api', 'records_api', url_prefix='/api/reports/')
auth_api = Blueprint('auth_api', 'auth_api', url_prefix='/api/auth/')  # TODO: remove me


@auth.verify_password
def verify_password(username_or_token, password=None):
    import ipdb; ipdb.set_trace()
    # first try to authenticate by token
    try:
        user = User.verify_auth_token(username_or_token)
    except itsdangerous.BadSignature:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth_api.route('/', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})



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