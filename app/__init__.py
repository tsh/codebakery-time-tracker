import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'expire_on_commit': False})


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    return app

