#!/usr/bin/env python
import glob
import os
import shutil
import subprocess
import click
from flask.cli import FlaskGroup
from backend.config import DevelopmentConfig
from backend.api import db, create_app
from backend.api.models import User

app = create_app(DevelopmentConfig())

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
def lint(with_appcontext=False):
    """Lint source code"""
    click.echo('Running flake8...\n')
    subprocess.call(['flake8', './backend'])
    click.echo('\nRunning ESLint...')
    subprocess.call(['./node_modules/.bin/eslint', 'js'])


@cli.command()
def build(with_appcontext=False):
    subprocess.call(
        ['./node_modules/.bin/webpack', '--config', 'webpack.config.prod.js'],
        env=dict(os.environ, NODE_ENV='production')
    )


@cli.command()
def frontend(with_appcontext=False):
    subprocess.call(
        ['node', 'server.js'],
    )


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
    
@cli.command()
def run():
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
    cli.main()
