from restaurant.app import create_app


import requests


def test_hello_endpoint():
    response = requests.get('http://127.0.0.1:5000/hello')
    assert response.status_code == 200
    assert response.content == b'Hello, World!'
