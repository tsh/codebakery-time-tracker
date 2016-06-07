import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask(__name__)

api = Api(prefix='/api/v1')
db = SQLAlchemy()

def create_app(config=None):
    if not config:
        config = os.environ.get('FLASK_CONFIG', 'backend.config:DevelopmentConfig')
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    return app
    
from . import views  # noqa
