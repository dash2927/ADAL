from recipeezy import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_client(client):
    response = client.get('/')
    print(type(response))