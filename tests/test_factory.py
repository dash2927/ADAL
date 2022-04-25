# Import app creator from recipeezy app
from recipeezy import create_app

# Test for validating that testing configuration is working
def test_config():
    # Assert that the test configuration is valid, true
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

# Test for ensuring response from test client is valid
def test_client(client):
    # Perform get on base path and ensure response is non-null without errors
    response = client.get('/')
    assert response
    