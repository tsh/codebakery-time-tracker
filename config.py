import os


class Base(object):
    SECRET_KEY = 'top secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class DevelopmentConfig(Base):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql:///time-tracker'
    SESSION_TYPE = 'filesystem'


class TestConfig(Base):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SERVER_NAME = 'test'