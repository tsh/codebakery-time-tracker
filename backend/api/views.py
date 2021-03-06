import csv
import io

import itsdangerous
import simplejson
from flask import jsonify, url_for, request, g, redirect, make_response, render_template, flash, session
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource

from . import db, app, api
from .forms import LoginForm, SubmitTimeForm
from .models import User, Record, Project


auth = HTTPBasicAuth()


@app.route('/', methods=['GET'])
def main():
    user = User.query.filter_by(username=session.get('username')).first()
    form = SubmitTimeForm()
    return render_template('main.html', user=user, form=form)


@app.route('/', methods=['POST'])
def post_time():
    user = User.query.filter_by(username=session.get('username')).first()
    if not user:
        return redirect(url_for('login'))
    form = SubmitTimeForm(request.form)
    if form.validate():
        record = Record().import_data(form.data)
        record.user = user
        db.session.add(record)
        db.session.commit()
        flash('Record added')
        return redirect(url_for('main'))
    else:
        return render_template('main.html', user=user, form=form)


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


@app.route('/api/v1/auth/', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})


# USERS

class Users(Resource):
    def get(self):
        return jsonify({'users': [user.get_url() for user in User.query.all()]})

    def post(self):
        user = User()
        user.import_data(request.json)
        db.session.add(user)
        db.session.commit()
        return {}, 201, {'Location': user.get_url()}

api.add_resource(Users, '/users/')


class UserDetails(Resource):
    def get(self, id):
        return jsonify(User.query.get_or_404(id).export_data())

api.add_resource(UserDetails, '/users/<int:id>', endpoint="user_detail")


@app.route('/api/v1/users/<int:id>/change-password/', methods=['POST'])
@auth.login_required
def user_change_password(id):
    user = User.query.get_or_404(id)
    user.change_password(old_password=request.json['password'],
                         new_password=request.json['new_password'])
    return jsonify({}), 205


class UserWork(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        si = io.StringIO()
        cw = csv.writer(si)
        for r in Record.query.filter_by(user_id=user.id):
            cw.writerow([r.date, r.user.username, r.time_spent, r.description])
        output = make_response(si.getvalue())
        # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

api.add_resource(UserWork, '/users/<int:id>/work-report.csv/')


# RECORDS

class Records(Resource):
    def get(self):
        return jsonify({'records': [record.get_url() for record in Record.query.all()]})

api.add_resource(Records, '/records/')


@app.route('/api/v1/records/', methods=['POST'])
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


@app.route('/api/v1/records/<int:id>', methods=['GET'])
def record_detail(id):
    return simplejson.dumps(Record.query.get_or_404(id).export_data())


# PROJECTS


@app.route('/api/v1/projects/', methods=['POST'])
@auth.login_required
def create_project():
    project = Project()
    project.import_data(request.json)
    db.session.add(project)
    db.session.commit()
    return jsonify({}), 201, {'Location': project.get_url()}


@app.route('/api/v1/projects/<int:id>', methods=['GET'])
@auth.login_required
def project_detail(id):
    return jsonify(Project.query.get_or_404(id).export_data())
