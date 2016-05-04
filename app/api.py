import csv
import io

from flask import jsonify, Blueprint, url_for, request, g, redirect, make_response, render_template, flash, session
from flask.ext.httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
import itsdangerous

from app import db, app
from app.forms import LoginForm
from .models import User, Record, Project


auth = HTTPBasicAuth()
api_v1 = Blueprint('api_v1', 'api_v1', url_prefix='/api/v1/')
api = Api(api_v1)


@app.route('/', methods=['GET'])
def main():
    user = User.query.filter_by(username=session.get('username')).first()
    return render_template('main.html', user=user)


@app.route('/submit', methods=['POST'])
def submit_time():
    user = User.query.filter_by(username=session.get('username')).first()
    if not user:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    if form.validate() and verify_password(form.username.data, form.password.data):
        session['username'] = form.username.data
        flash('You were successfully logged in')
        return redirect(url_for('main'))
    else:
        flash("Something went wrong, can't login")
        return render_template('login.html', form=form)


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


@api_v1.route('auth/', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})


# USERS

class Users(Resource):
    def get(self):
        return jsonify({'users': [user.get_url() for user in User.query.all()]})

api.add_resource(Users, 'users/')



@api_v1.route('users/', methods=['POST'])
def create_user():
    user = User()
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({}), 201, {'Location': user.get_url()}


@api_v1.route('users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


@api_v1.route('users/<int:id>/change-password/', methods=['POST'])
@auth.login_required
def user_change_password(id):
    user = User.query.get_or_404(id)
    user.change_password(old_password=request.json['password'],
                         new_password=request.json['new_password'])
    return jsonify({}), 205


@api_v1.route('users/<int:id>/work-report.csv/', methods=['GET'])
def get_user_work(id):
    user = User.query.get_or_404(id)
    si = io.StringIO()
    cw = csv.writer(si)
    for r in Record.query.filter_by(user_id=user.id):
        cw.writerow([r.date, r.user.username, r.time_spent, r.description])
    output = make_response(si.getvalue())
    # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# RECORDS


@api_v1.route('records/', methods=['GET'])
def records():
    return jsonify({'records': [record.get_url() for record in Record.query.all()]})


@api_v1.route('records/', methods=['POST'])
@auth.login_required
def create_record():
    user = g.user
    if 'project_id' in request.json:
        project = Project.query.get_or_404(request.json['project_id'])
    else:
        project = None
    record = Record(user=user, project=project)
    record.import_data(request.json)
    db.session.add(record)
    db.session.commit()
    return jsonify({}), 201, {'Location': record.get_url()}


@api_v1.route('records/<int:id>', methods=['GET'])
def record_detail(id):
    return jsonify(Record.query.get_or_404(id).export_data())


# PROJECTS


@api_v1.route('projects/', methods=['POST'])
@auth.login_required
def create_project():
    project = Project()
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return jsonify({}), 201, {'Location': project.get_url()}


@api_v1.route('projects/<int:id>', methods=['GET'])
@auth.login_required
def project_detail(id):
    return jsonify(Project.query.get_or_404(id).export_data())
