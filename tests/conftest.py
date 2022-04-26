# Import pytest lib for test setup
import pytest

# Test fixture for yielding an app instance for further testing
@pytest.fixture
def app():
    # Use app creation func and pass testing flag
    from recipeezy import create_app
    app = create_app({'TESTING': True})
    # Return app for future use
    yield app

# Test fixture for getting app test client
@pytest.fixture
def client(app):
    # Return test client from current app
    return app.test_client()

# Test fixture for getting CLI runner from current app
@pytest.fixture
def runner(app):
    # Return current app CLI runner
    return app.test_cli_runner()

