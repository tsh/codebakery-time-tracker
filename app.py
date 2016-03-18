import os

from flask import Flask, url_for, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

# from models import User, Record

db = SQLAlchemy(session_options={'expire_on_commit': False})


def create_app():

    basedir = os.path.abspath(os.path.dirname(__file__))
    # db_path = os.path.join(basedir, 'data.sqlite')

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql:///time-tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'top-secret!'
    return app

