import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')


class BaseConfig(object):
    SECRET_KEY = 'F}E\x1f\xea6"\xfe\xfb\x8fm{\'\x05\x9e\x99\xafZ\xc1\xdbC\x9a\x02\xc8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(SQLITE_DB_PATH)
    SESSION_TYPE = 'filesystem'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SERVER_NAME = 'test'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///time_tracker'
