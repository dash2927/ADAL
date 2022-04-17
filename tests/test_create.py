import pytest

from recipeezy.database import db

def test_create(client, app):
    response = client.get("/")
    print(response.data)
    assert 1 == 1
    


