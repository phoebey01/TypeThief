# py
# https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 5000


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


CONFIGS = {
    'dev': DevelopmentConfig,
    'stage': StagingConfig,
    'prod': ProductionConfig,
    'test': TestingConfig,
}
