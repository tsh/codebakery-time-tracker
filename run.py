from flask import jsonify, url_for

from app import create_app, db
from app.api import api_v1
from config import DevelopmentConfig


if __name__ == '__main__':
    dev_config = DevelopmentConfig()
    app = create_app(dev_config)
    with app.app_context():
        db.create_all()
    app.register_blueprint(api_v1)
    app.run(host='0.0.0.0', debug=True, port=8000)
