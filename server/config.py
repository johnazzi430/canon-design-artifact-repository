
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # If not set fall back to production for safety
    DEBUG = True
    TESTING = True

    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'client/dist')

    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))


class ProductionConfig(Config):
 DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
 DEBUG = True
 TESTING = True

class TestingConfig(Config):
    TESTING = True
