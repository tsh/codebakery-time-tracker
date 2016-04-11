from flask import jsonify, url_for

from app import create_app, db
from app.api import api_v1
from app.models import User
from config import DevelopmentConfig


def create_admin():
    if User.query.filter(User.username == 'test').count() == 0:
        user = User(username='test')
        user.set_password('pwd')
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    dev_config = DevelopmentConfig()
    app = create_app(dev_config)
    with app.app_context():
        db.create_all()
        create_admin()
    app.register_blueprint(api_v1)
    app.run(host='0.0.0.0', debug=True, port=8000)
