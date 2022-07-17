"""Flask configuration."""
import json
import redis
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    SECRET_KEY = environ.get('SECRET_KEY')
    #SESSION_TYPE = redis
    #SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))
class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        "db": environ.get('PROD_MONGO_DB'),
        "host": environ.get('PROD_MONGO_URI')
        }

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        "db": environ.get('DEV_MONGO_DB'),
        "host": environ.get('DEV_MONGO_URI')
        }