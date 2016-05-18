from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy

from flask_restful import Api


db = SQLAlchemy(session_options={'expire_on_commit': False})

app = Flask(__name__)
api_v1 = Blueprint('api_v1', 'api_v1', url_prefix='/api/v1/')
api = Api(api_v1)


def create_app(config_object):
    app.config.from_object(config_object)
    db.init_app(app)
    app.register_blueprint(api_v1)
    return app
