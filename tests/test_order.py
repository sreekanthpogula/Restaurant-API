import pytest
from restaurant import order


def test_hello_restaurant(app):
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome, To the Restaurant Application, YOU CAN ORDER NOW!' in response.data


def test_get_orders(app):
    with app.test_client() as client:
        response = client.get('/orders')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'


def test_get_specific_order(app):
    with app.test_client() as client:
        response = client.get('/orders/1')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'


def test_create_order(app):
    with app.test_client() as client:
        response = client.post('/orders', json={
            "customer_id": 1,
            "status": "pending",
            "order_time": "2022-01-01T12:00:00",
            "items": [
                {
                    "Item_name": "Pizza",
                    "Quantity": 1,
                    "size": "large"
                }
            ]
        })
        assert response.status_code == 201
        assert response.headers['Content-Type'] == 'application/json'


def test_update_order(app):
    with app.test_client() as client:
        response = client.put('/orders/1', json={
            "status": "completed"
        })
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'


def test_delete_order(app):
    with app.test_client() as client:
        response = client.delete('/orders/1')
        assert response.status_code == 204
