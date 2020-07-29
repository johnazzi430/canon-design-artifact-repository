# python -m pytest tests
import pytest
import os

os.environ['DATABASE_URL'] = 'test'
os.environ['FLASK_ENV'] = 'testing'
os.environ['APP_SETTINGS'] = 'server.config.TestingConfig'

from server import app as flask_app

@pytest.fixture(autouse=True)
def app(mocker):

    flask_app.config["TESTING"] = True

    mocker.patch("flask_sqlalchemy.SQLAlchemy.init_app", return_value=True)
    mocker.patch("flask_sqlalchemy.SQLAlchemy.create_all", return_value=True)
    mocker.patch('flask_sqlalchemy._QueryProperty.__get__', return_value=True)

    yield flask_app


@pytest.fixture(autouse=True)
def client(app):
    return app.test_client()
