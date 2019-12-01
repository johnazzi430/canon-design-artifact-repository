
import os
from server import app


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    DATABASE = 'server/data/data.db'

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'client/dist')

    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))

class BaseConfig(object):
 '''
 Base config class
 '''
 DEBUG = True
 TESTING = False
class ProductionConfig(BaseConfig):
 """
 Production specific config
 """
 DEBUG = False
class DevelopmentConfig(BaseConfig):
 """
 Development environment specific configuration
 """
 DEBUG = True
 TESTING = True


app.config.from_object('server.config.Config')
