# Project Title:

Recipeezy

# Team member's names:

* Luis Mendoza
* Alex Plazas
* David Shackelford
* Adhir Uchil

# Automated Test Cases:

PRECONDITION TO RUN ALL TESTS:
1. create a new environment
2. run `pip install -r requirements.txt` in environment to get requirements
---
Use case name
    Verify login with valid user name and password
Description
    Test for logging in only. This tests for access to the User database and
    return to the HOME page.
Pre-conditions
    No preconditions
Test steps
    1. run app using `python recipeezy.py`
    2. open browser and delete cookies
    3. go to the url given by app
    4. click on CREATE
    5. In Username, type "New_User"
    6. In Password, type "Password"
    7. Click submit button
Expected result
    User should login and be returned to HOME page
Actual result
    User is logged in and returned to HOME page
Status (Pass/Fail)
    Pass
Notes
    * User is not given notification of user being logged in. It will show up on flask CLI and as a flash() message for debugging.
    * Cookies will save your credentials so if you click on CREATE and aren't redirected, clear cookies and return to homepage.
    * New account creation is not tested here, we are basically using a user that is manually added to the db and checking for validation.
Post-conditions
    User is validated with database and successfully signed into their account.

---
Use case name
    Add a recipe to the database
Description
    Test recipe submission by adding a test recipe to the database and checking for re-submission
Pre-conditions
    User has a valid user name and password and logged in
Test steps
    1. Navigate to LOGIN page
    2. Provide valid user name
    3. Provide valid password
    4. Click submit button
    5. Navigate to CREATE page
    6. Add something in every field
    7. Click submit button button
    8. Without changing any fields, click submit again
Expected result
    User should get confirmation that they submitted a recipe and then, upon clicking submit again, a notification that recipe is already submitted
Actual result
    User gets gets confirmation that they submitted a recipe and then resubmit notification
Status (Pass/Fail)
    Pass
Notes
    * The CREATE page is very basic right now and does not have any extra options besides title and recipe
Post-conditions
    User submitted recipe is now in the Post table of the database

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

