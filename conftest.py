import os
import pytest
from pyframekit.app import PyFrameKitApp
from pyframekit.orm import Database, Table, Column, ForeignKey

@pytest.fixture
def app():
    return PyFrameKitApp()

@pytest.fixture
def test_client(app):
    return app.test_session()

@pytest.fixture
def Author():
    class Author(Table):
        name = Column(str)
        age = Column(int)
    
    return Author

@pytest.fixture
def Book(Author):
    class Book(Table):
        title = Column(str)
        published = Column(bool)
        author = ForeignKey(Author)

    return Book

@pytest.fixture
def db():
    DB_PATH = "./test.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = Database(DB_PATH)
    return db  