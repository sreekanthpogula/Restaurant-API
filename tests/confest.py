import os
import tempfile
import requests
import pytest
from restaurant import create_app
from restaurant.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


BASE_URL = 'http://localhost:5000'  # Replace with the base URL of your API


@pytest.fixture
def existing_order_id():
    # Return the ID of an existing order
    return 1


@pytest.fixture
def non_existent_order_id():
    # Return the ID of a non-existent order
    return 99


@pytest.fixture
def new_order_data():
    # Return the data for a new order
    return {
        "customer_id": 10,
        "order_id": 10,
        "order_time": "Tue, 10 Jan 2023 11:12:30 GMT",
        "ordered_items": [
            {
                "Item_name": "biryani",
                "Quantity": 2,
                "size": "Full"
            }
        ],
        "status": "Not-paid"
    }


@pytest.fixture
def updated_order_data():
    # Return the updated data for an existing order
    return {
        "Item_name": "Chicken Curry",
        "Quantity": 4,
        "customer_id": 1,
        "order_id": 1,
        "order_time": "Thu, 05 Jan 2023 15:00:32 GMT",
        "size": "Full",
        "status": "Paid"
    }


def test_get_orders(existing_order_id, non_existent_order_id):
    # Test getting a list of all orders
    response = requests.get(f'{BASE_URL}/orders')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Test getting a specific order
    response = requests.get(f'{BASE_URL}/orders/{existing_order_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    # Test trying to get a non-existent order
    response = requests.get(f'{BASE_URL}/orders/{non_existent_order_id}')
    assert response.status_code == 404


def test_create_order(new_order_data):
    # Test creating a new order
    response = requests.post(f'{BASE_URL}/orders', json=new_order_data)
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


def test_update_order(existing_order_id, non_existent_order_id, updated_order_data):
    # Test updating an existing order
    response = requests.put(
        f'{BASE_URL}/orders/{existing_order_id}', json=updated_order_data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    # Test trying to update a non-existent order
    response = requests.put(
        f'{BASE_URL}/orders/{non_existent_order_id}', json=updated_order_data)
    assert response.status_code == 404


def test_delete_order(existing_order_id, non_existent_order_id):
    # Test deleting an order
    response = requests.delete(f'{BASE_URL}/orders/{existing_order_id}')
    assert response.status_code == 204

    # Test trying to delete a non-existent order
    response = requests.delete(f'{BASE_URL}/orders/{non_existent_order_id}')
    assert response.status_code == 404


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
