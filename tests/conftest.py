
# python -m pytest tests
import pytest

from dotenv import load_dotenv
load_dotenv()

from server import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True

    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
