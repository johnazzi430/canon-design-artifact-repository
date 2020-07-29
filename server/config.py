import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # If not set fall back to production for safety
    DEBUG = True
    TESTING = True

    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("FLASK_SECRET", "Secret")

    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, "client/dist")

    CLIENT_ID = "33623831-ae6e-4d3b-96b2-9f9c55ebb42b"
    CLIENT_SECRET = "Enter_the_Client_Secret_Here"
    AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

    if not os.path.exists(DIST_DIR):
        raise Exception("DIST_DIR not found: {}".format(DIST_DIR))


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    TESTING = True
