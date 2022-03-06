# Project Title:

Recipeezy

# Team member's names:

* Luis Mendoza
* Alex Plazas
* David Shackelford
* Adhir Uchil

# Automated Test Cases:

---
Use case name
    Verify login with valid user name and password
Description
    Test for logging in only. This tests for access to the User database and
    return to the previous page.
Pre-conditions
    No preconditions
Test steps
    1. Navigate to Login page
    2. In Username, type "New_User"
    3. In Password, type "Password"
    4. Click login button
Expected result
    User should login and be returned to homepage
Actual result
    User is logged in and returned to homepage
Status (Pass/Fail)
    Pass
Notes
    * There is no notification of user being logged in. It will show up on flask CLI.
    * New account creation is not tested here, we are basically using a user that is manually added to the db and checking for validation.

Post-conditions
    User is validated with database and successfully signed into their account.

---
Use case name
    Add a recipe to the database
Description
    Test recipe submission by adding a test recipe to the database
Pre-conditions
    User has a valid user name and password and logged in
Test steps
    1. Navigate to login page
    2. Provide valid user name
    3. Provide valid password
    4. Click login button
    5. Navigate to create page
    6. Add something in every field
    7. Hit create button
Expected result
    User should get confirmation that they submitted a recip
Actual result
    User gets a page error and cant create anything
Status (Pass/Fail)
    Fail
Notes
    * The create page isn't fully running
Post-conditions

---
Use case name
    Test database
Description
    Tests database using unittest (addition, query, value change, password hashing)
Pre-conditions
    No preconditions
Test steps
    1. From project page, type `python -m unittest tests/test_database.py`
Expected result
    All succesful tests
Actual result
    All succesful tests
Status (Pass/Fail)
    Pass
Notes
    * This test only tests for the User and Post dbs. Future dbs will need added tests
Post-conditions
    All tests pass

