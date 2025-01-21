import sqlite3
import pytest

def test_create_db(db):
    assert isinstance(db.conn, sqlite3.Connection)
    assert db.tables == []

def test_table_definition(Author, Book):
    assert Author.name.type == str
    assert Book.author.table == Author

    assert Author.name.sql_type == "TEXT"
    assert Author.age.sql_type == "INTEGER"

def test_create_tables(db, Author, Book):
    db.create(Author)
    db.create(Book)

    assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
    assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"

    for table in ("author", "book"):
        assert table in db.tables

def test_create_table_instances(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=44)

    assert john.name == "John Doe"
    assert john.age == 44
    assert john.id is None

def test_save_table_instances(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=44)
    db.save(john)

    assert john._get_insert_sql() == (
        "INSERT INTO author (age, name) VALUES (?, ?);",
        [44, "John Doe"]
    )
    assert john.id == 1

    jack = Author(name="Jack Ma", age=55)
    db.save(jack)
    assert jack.id == 2

def test_query_all_authors(db, Author):
    db.create(Author)

    john = Author(name = "John Doe", age=43)
    jack = Author(name = "Jack Ma", age=23)
    db.save(john)
    db.save(jack)

    authors = db.all(Author)

    assert Author._get_select_all_sql() == (
        "SELECT id, age, name FROM author;",
        ["id", "age", "name"]
    )
    assert len(authors) == 2
    assert isinstance(authors[0], Author)
    assert isinstance(authors[1], Author)
    for author in authors:
        assert author.age in {43, 23}
        assert author.name in {"John Doe", "Jack Ma"}
        assert author.id in {1, 2}

def test_get_author(db, Author):
    db.create(Author)
    john = Author(name = "John Doe", age=43)
    db.save(john)

    john_from_db = db.get(Author, id=1)

    assert Author._get_select_by_id_sql(id=1) == (
        "SELECT id, age, name FROM author WHERE id = 1;",
        ["id", "age", "name"]
    )
    assert isinstance(john_from_db, Author)
    assert john_from_db.id == 1
    assert john_from_db.age == 43
    assert john_from_db.name == "John Doe"

def test_get_book(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name = "John Doe", age=45)
    jack = Author(name = "Jack Ma", age=35)

    book1 = Book(title="Best Book", published=False, author=john)
    book2 = Book(title="Average Book", published=True, author=jack)

    db.save(john)
    db.save(jack)
    db.save(book1)
    db.save(book2)

    book_from_db = db.get(Book, id=2)
    
    assert book_from_db.title == "Average Book"
    assert book_from_db.author.id == 2
    assert book_from_db.author.name == "Jack Ma"
    assert book_from_db.author.age == 35

def test_get_all_books(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name = "John Doe", age=45)
    jack = Author(name = "Jack Ma", age=35)

    book1 = Book(title="Best Book", published=False, author=john)
    book2 = Book(title="Average Book", published=True, author=jack)

    db.save(john)
    db.save(jack)
    db.save(book1)
    db.save(book2)

    books = db.all(Book)

    assert len(books) == 2
    assert books[1].author.name == "Jack Ma"

def test_update_author(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=25)
    db.save(john)

    john.age = 40
    john.name = "John Wick"
    db.update(john)

    john_from_db = db.get(Author, id=john.id)

    assert john_from_db.name == "John Wick"
    assert john_from_db.age == 40

def test_delete_author(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=25)
    db.save(john)

    db.delete(Author, id=1)

    with pytest.raises(Exception):
        db.get(Author, id=1)