# test/conftest.py

import pytest

from enigma_bombe.app import app

def pytest_addoption(parser):
    parser.addoption("--flask-url")

@pytest.fixture(scope="session")
def redis_url(request):
    return request.config.getoption("--redis-url")

@pytest.fixture
def http_client():
    return app.test_client()
