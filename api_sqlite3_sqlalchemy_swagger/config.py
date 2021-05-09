from sys import platform
"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


if platform == "linux" or platform == "linux2":
    db_uri = environ.get('SQLALCHEMY_DATABASE_URI_LINUX')
elif platform == "win32":
    db_uri = environ.get('SQLALCHEMY_DATABASE_URI_WIN')


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_uri