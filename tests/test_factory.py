from restaurant import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/order')
    assert response.data == b'Welcome, To the Restaurant Appliaction, YOU CAN ORDER NOW!'
