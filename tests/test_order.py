from sqlite3 import OperationalError
from flask import Flask
import pytest
import requests
from confest import client


BASE_URL = 'http://localhost:5000'  # Replace with the base URL of your API


def test_get_orders():
    # Test getting a list of all orders
    response = requests.get(f'{BASE_URL}/orders')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_specific_order():
    # Test getting a specific order
    order_id = 3  # Replace with the ID of an existing order
    response = requests.get(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


# def test_create_order():
#     # Test creating a new order
#     data = {
#         "customer_id": 10,
#         "order_id": 10,
#         "order_time": "Tue, 10 Jan 2023 11:12:30 GMT",
#         "ordered_items": [
#             {
#                 "Item_name": "biryani",
#                 "Quantity": 2,
#                 "size": "Full"
#             }
#         ],
#         "status": "Not-paid"
#     }
#     response = requests.post(f'{BASE_URL}/orders', json=data)
#     assert response.status_code == 500
#     assert isinstance(response.json(), dict)


def test_update_order():
    # Test updating an existing order
    order_id = 1  # Replace with the ID of an existing order
    data = {
        "Item_name": "Chicken Curry",
        "Quantity": 4,
        "customer_id": 1,
        "order_id": 1,
        "order_time": "Thu, 05 Jan 2023 15:00:32 GMT",
        "size": "Full",
        "status": "Paid"
    }
    response = requests.put(f'{BASE_URL}/orders/{order_id}', json=data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_delete_order():
    # Test deleting an order
    order_id = 1  # Replace with the ID of an existing order
    response = requests.delete(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 200


def test_get_non_existent_order():
    # Test trying to get a non-existent order
    order_id = 99  # Replace with the ID of a non-existent order
    response = requests.get(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 404


def test_update_non_existent_order():
    # Test trying to update a non-existent order
    order_id = 99  # Replace with the ID of a non-existent order
    data = {
        "order_id": 99,
        "customer_id": 99,
        "ordered_items": [
            {
                "Item_name": "biryani",
                "Quantity": 2,
                "size": "Full"
            }
        ],
        "status": "Not-paid"
    }
    response = requests.put(f'{BASE_URL}/orders/{order_id}', json=data)
    assert response.status_code == 200


def test_delete_non_existent_order():
    # Test trying to delete a non-existent order
    order_id = 99  # Replace with the ID of a non-existent order
    response = requests.delete(f'{BASE_URL}/orders/{order_id}')
    assert response.status_code == 200
