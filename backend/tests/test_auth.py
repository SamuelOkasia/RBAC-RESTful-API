import json
import pytest

pytest_plugins = "pytester"  # Include pytest plugin for running tests within pytest itself


# Test the Google login route (this should trigger a redirect to Google OAuth)
def test_google_login(client):
    """
    Test case for the Google OAuth login route.

    Steps:
    1. Make a GET request to the '/auth/google' route.
    
    Asserts:
    - The response status code should be 302 (redirect) because Google OAuth triggers a redirect to Google login page.
    """
    response = client.get('/auth/google')
    
    # Assert that the response is a redirect (302)
    assert response.status_code == 302


# Test the regular login functionality (email/password)
def test_login(client):
    """
    Test case for the regular email/password login route.

    Steps:
    1. First, register a user by making a POST request to '/auth/register'.
    2. Then, log in using the newly registered user's credentials.

    Asserts:
    - The registration request should return a 201 status code (Created).
    - The login request should return a 200 status code (Success).
    - The login response should include an access token for further authentication.
    """
    # Step 1: Register a new user
    response = client.post('/auth/register', json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })

    # Assert that the user registration was successful
    assert response.status_code == 201

    # Step 2: Test logging in with the registered user credentials
    response = client.post('/auth/login', json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })

    # Assert that the login was successful
    assert response.status_code == 200

    # Convert the response data from JSON and assert that the access token is present
    data = json.loads(response.data)
    assert "access_token" in data
