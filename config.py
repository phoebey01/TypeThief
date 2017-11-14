# config.py
# https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 5000


class TestingConfig(Config):
    TESTING = True
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 5000
