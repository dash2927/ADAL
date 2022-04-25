<<<<<<< HEAD
# Import pytest framework, database
=======

>>>>>>> 04b911e4177ff4df61aed6a32f62336cea2a1ec0
import pytest
from recipeezy.database import db

# Test for getting default page from base directory
def test_default_page_routing(client):
    response = client.get("/")
    responseData = response.data
    assert b'<title> - Recipeezy</title>' in responseData
    assert b'<nav class="navbar navbar-expand-lg navbar-light bg-white">' in responseData
    assert b'<div class="content">' in responseData
    assert b'<p class="body">' in responseData
    assert response.status_code == 200

# Test for getting home page
# Note: This test might need to be changed once the homepage is complete, as the exact display html will be different in the final implementation
def test_home_page_routing(client):
    response = client.get("/home")
    responseData = response.data
    assert b'<title> - Recipeezy</title>' in responseData
    assert b'<div class="album py-5 bg-light">' in responseData
    assert b'<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">' in responseData
    assert b'<p class="body">' in responseData
    assert response.status_code == 200

# Test for getting the create page, following redirects
# Note: Rendering the create page requires auth credentials (login requried), which will be tested in a follow-up integration test
def test_create_page_routing(client):
    response = client.get("/create", follow_redirects=True)
    responseData = response.data
    assert b'<title> - Recipeezy</title>' in responseData
    assert b'<nav class="navbar navbar-expand-lg navbar-light bg-white">' in responseData
    assert b'<div class="content">' in responseData
    assert b'<p class="body">' in responseData
    assert response.status_code == 200

# Test for getting the login page
def test_login_page_routing(client):
    response = client.get("/login")
    responseData = response.data
    assert b'<title> - Recipeezy</title>' in responseData
    assert b'<main class="form-signin">' in responseData
    assert b'<form method="POST">' in responseData
    assert b'<h1 class="h3 mt-5 mb-3 fw-normal">Login</h1>' in responseData
    assert b'<div class="form-floating">' in responseData
    assert response.status_code == 200

# Test for getting the signup page
def test_signup_routing(client):
    response = client.get("/signup")
    responseData = response.data
    assert b'<title> - Recipeezy</title>' in responseData
    assert b'<main class="form-signin">' in responseData
    assert b'<form method="POST">' in responseData
    assert b'<h1 class="h3 mt-5 mb-3 fw-normal">Sign Up</h1>' in responseData
    assert b'<div class="form-floating mb-3">' in responseData
    assert b'<div class="form-floating">' in responseData
    assert b'<button class="w-100 btn btn-lg btn-danger" type="submit">Sign Up</button>' in responseData
    assert response.status_code == 200

# Test for getting the signout page, following redirects
# Note: Rendering the signout page requires auth credentials (login requried), which will be tested in a follow-up integration test
def test_signout_page_routing(client):
    response = client.get("/signout", follow_redirects=True)
    responseData = response.data
    assert b'<title> - Recipeezy</title>' in responseData
    assert b'<nav class="navbar navbar-expand-lg navbar-light bg-white">' in responseData
    assert b'<div class="content">' in responseData
    assert b'<p class="body">' in responseData
    assert response.status_code == 200



