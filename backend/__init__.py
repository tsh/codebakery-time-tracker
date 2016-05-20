import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

config = os.environ.get('FLASK_CONFIG', 'backend.config:DevelopmentConfig')

app = Flask(__name__)
app.config.from_object(config)

api = Api(app)
db = SQLAlchemy(app)

from . import views  # noqa
