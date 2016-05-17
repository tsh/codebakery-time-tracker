import argparse

from app import create_app, db
from app.models import User
from config import DevelopmentConfig

app = create_app(DevelopmentConfig())


def create_user(username, password):
    with app.app_context():
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()
    create_user(args.username, args.password)
