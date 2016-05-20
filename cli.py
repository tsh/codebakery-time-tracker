#!/usr/bin/env python
import click
import glob
import shutil
from flask.cli import FlaskGroup
from backend import app, db
from backend.models import User


cli = FlaskGroup(
    add_app_option=False,
    create_app=lambda _: app,
    help='Time tracker CLI',
)


@cli.command(with_appcontext=False)
def clean():
    """Cleans build files."""
    shutil.rmtree('./dist', ignore_errors=True)
    for path in glob.iglob('./backend/**/__pycache__', recursive=True):
        shutil.rmtree(path, ignore_errors=True)


@cli.command()
def create_db():
    """Create database"""
    db.create_all()


@cli.command()
@click.argument('username')
def create_user(username):
    """Creates user from passed params."""
    password = click.prompt('Password', hide_input=True)
    if not password:
        create_user(username)

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli.main()
