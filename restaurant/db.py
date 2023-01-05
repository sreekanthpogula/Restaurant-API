import sqlite3
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_orders_table():
    """
    Creates the orders table in the database
    """
    conn = get_db()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            status VARCHAR(255) NOT NULL,
            order_time TIMESTAMP NOT NULL
        )'''
    )
    conn.commit()
    close_db(conn)


def create_ordered_items_table():
    """
    Creates the ordered_items table in the database
    """
    conn = get_db()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS ordered_items (
            order_id INTEGER NOT NULL,
            item_name VARCHAR(255) NOT NULL,
            quantity INTEGER NOT NULL,
            size VARCHAR(255) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )'''
    )
    conn.commit()
    close_db(conn)
