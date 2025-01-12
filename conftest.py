import pytest
from pyframekit.app import PyFrameKitApp

@pytest.fixture
def app():
    return PyFrameKitApp()

@pytest.fixture
def test_client(app):
    return app.test_session()