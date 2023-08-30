import pytest
from main import app

@pytest.fixture
def app():
    return app
