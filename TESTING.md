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
    Test the Google login page
Pre-conditions
    User has valid user name and password
Test steps
    1. Navigate to login page
    2. Provide valid user name
    3. Provide valid password
    4. Click login button
Expected result
    User should be able to login
Actual result
    User is notified of succesful login and is allowed to return to home
Status (Pass/Fail)
    Pass
Notes
    N/A
Post-conditions
    User is validated with database and successfully signed into their account.
    The account session details are logged in database.

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
    The create page isn't fully running
Post-conditions

---
Use case name
    [entry]
Description
    [entry]
Pre-conditions
    [entry]
Test steps
    1. Step 1 here
Expected result
    [entry]
Actual result
    [entry]
Status (Pass/Fail)
    Pass/Fail
Notes
    N/A
Post-conditions
    [entry]

