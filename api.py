from flask import jsonify, Blueprint, url_for, request, g
from flask.ext.httpauth import HTTPBasicAuth
import itsdangerous

from app import create_app, db
from models import User, Record, Project


app = create_app()
auth = HTTPBasicAuth()

users_api = Blueprint('users_api', 'users_api', url_prefix='/api/users/')
records_api = Blueprint('records_api', 'records_api', url_prefix='/api/records/')
auth_api = Blueprint('auth_api', 'auth_api', url_prefix='/api/auth/')
projects_api = Blueprint('projects_api', 'projects_api', url_prefix='/api/projects/')


# AUTH

@auth.verify_password
def verify_password(username_or_token, password=None):
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


# USERS


@users_api.route('/', methods=['GET'])
def users():
    return jsonify({'users': [user.get_url() for user in User.query.all()]})


@users_api.route('<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


# REPORTS


@records_api.route('/', methods=['GET'])
def reports():
    return jsonify({'records': [record.get_url() for record in Record.query.all()]})


@records_api.route('/', methods=['POST'])
@auth.login_required
def create_report():
    user = g.user
    record = Record(user=user)
    record.import_data(request.json)
    db.session.add(record)
    db.session.commit()
    return jsonify({}), 201, {'Location': record.get_url()}


@records_api.route('<int:id>', methods=['GET'])
def record_detail(id):
    return jsonify(Record.query.get_or_404(id).export_data())


# PROJECTS


@projects_api.route('/', methods=['POST'])
@auth.login_required
def create_project():
    project = Project()
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return jsonify({}), 201, {'Location': project.get_url()}


@projects_api.route('<int:id>', methods=['GET'])
@auth.login_required
def project_detail(id):
    return jsonify(Project.query.get_or_404(id).export_data())