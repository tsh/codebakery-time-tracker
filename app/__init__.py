import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'expire_on_commit': False})

app = Flask(__name__)

def create_app(config_object):
    app.config.from_object(config_object)
    db.init_app(app)
    return app

