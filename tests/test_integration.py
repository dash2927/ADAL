# Integration tests needed for signup flow
# Integration tests needed for login -> logout flow
# Integration tests needed for login -> create flow 
# Integration tests needed for login -> create -> logout flow

# Necessary imports here

# Define before_test function(s) setting up the test app and test client for performing requests

# (Maybe?) Define after_test function(s) to tear down the app and client, clear dbs
    # This might not be necessary, as we will want to use the client and app for each test in their current forms 

# Note: Does not require authentication on request
# Define signup integration test
    # Build a signup form data entity and fill in with test values
    # Use a test client to send a put request on the signup endpoint with details from the signup form entity
    # Validate that the client request result is 200
    # Check the test app database and verify that the values placed on the db are the same as those in the request

# Note: Does require authentication on request
# Define login -> logout integration test
    # Build a login request using the test user currently stored on the db, or the user from the initial signup integration test
    # Use a test client to send a put request on the login endpoint
    # Validate that the request result is 200
    # Validate that logged in user is redirected to the home page
    # Use the test client to navigate to the logout endpoint
    # Validate result of hitting logout endpoint is 200
    # Validate that logged out user is redirected to the home page 

# Note: Does require authentication on request
# Define login -> create integration test
    # Build a login request as described previously using user info already on the users db
    # Use a test client to send a request to the login endpoint
    # Validate that result of the login request is 200
    # Validate that user is redirected to homepage
    # Use the test client to navigate to the create page (credentials required)
    # Validate that request result is 200
    # Validate that create page is rendered
    # Create a create form entity and fill in the required values (recipe name, steps, etc.)
    # Use the test client to make a put request on the create page with values from the create form entity
    # Validate that the request result is 200
    # Validate that the post db and vote dbs reflect changes made
    # Validate that the contents of the post db match the create recipe request

# Note: Does require authentication on request
# Define login -> create -> logout integration test
    # Build a login request as described previously using user info already on the users db
    # Use a test client to send a request to the login endpoint
    # Validate that result of the login request is 200
    # Validate that user is redirected to homepage
    # Use the test client to navigate to the create page (credentials required)
    # Validate that request result is 200
    # Validate that create page is rendered
    # Create a create form entity and fill in the required values (recipe name, steps, etc.)
    # Use the test client to make a put request on the create page with values from the create form entity
    # Validate that the request result is 200
    # Validate that the post db and vote dbs reflect changes made
    # Validate that the contents of the post db match the create recipe request
    # Use the test client to hit the signout endpoint
    # Verify that request result is 200
    # Verify that user is redirected to homepage (that the homepage is returned after logout)