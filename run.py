from flask import jsonify, url_for

from app import create_app, db
from app.api import users_api, records_api, auth_api, projects_api
from config import DevelopmentConfig


if __name__ == '__main__':
    dev_config = DevelopmentConfig()
    app = create_app(dev_config)
    with app.app_context():
        db.create_all()
    app.register_blueprint(users_api)
    app.register_blueprint(records_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(projects_api)
    app.run(host='0.0.0.0', debug=True, port=8000)
