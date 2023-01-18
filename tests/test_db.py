import sqlite3

import pytest
from restaurant.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT *')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def test_db():
    conn = get_db()
    c = conn.cursor()
    c.execute(
        '''Select * from information_schema.tables
        '''
    )
    print(c.fetchall())
    conn.commit()
    close_db(conn)
