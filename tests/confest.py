import sqlite3
import requests
import pytest
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/order/<int:order_id>')
def get_specific_order(order_id):
    return f'Order {order_id}'


app.config['TESTING'] = True
client = app.test_client()


@app.before_request
def before_request():
    app.config['DATABASE'] = ':memory:'
    get_db()


def create_app():
    return app


def get_db():
    db = sqlite3.connect(
        app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    return db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


BASE_URL = 'http://localhost:5099'  # Replace with the base URL of your API


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


@pytest.fixture
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


@pytest.fixture
def test_create_order(new_order_data):
    # Test creating a new order
    response = requests.post(f'{BASE_URL}/orders', json=new_order_data)
    assert response.status_code == 201
    assert isinstance(response.json(), dict)


@pytest.fixture
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


@pytest.fixture
def test_delete_order(existing_order_id, non_existent_order_id):
    # Test deleting an order
    response = requests.delete(f'{BASE_URL}/orders/{existing_order_id}')
    assert response.status_code == 204

    # Test trying to delete a non-existent order
    response = requests.delete(f'{BASE_URL}/orders/{non_existent_order_id}')
    assert response.status_code == 404


@pytest.fixture
def api_url():
    return BASE_URL


@pytest.fixture
def api_session():
    return requests.Session()


@pytest.fixture
def valid_order():
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


def test_get_specific_order_not_found():
    response = client.get('/order/99')
    assert response.status_code == 404
    assert response.data == b"Order Not Found"


def test_get_specific_order_invalid_id(client):
    response = client.get('/orders/1000')
    assert response.status_code == 404
    assert b"Order Not Found" in response.data


def test_get_orders_invalid_method(client):
    response = client.post('/orders')
    assert response.status_code == 405
    assert b"Method Not Allowed 405" in response.data


def test_post_orders_invalid_payload(client):
    response = client.post('/orders', json={'customer_id': '123'})
    assert response.status_code == 400
    assert b"Bad Request Error -400" in response.data


def test_db_connection_error(client, monkeypatch):
    def mock_get_db():
        raise sqlite3.OperationalError()

    monkeypatch.setattr('restaurant.db.get_db', mock_get_db)

    response = client.get('/orders')
    assert response.status_code == 500
    assert b"Internal Server Error 500" in response.data
