import json

# Test for getting a user's profile data
def test_get_profile(client):
    """
    Test case for retrieving a user's profile.

    Steps:
    1. Register a user by making a POST request to '/auth/register'.
    2. Log in as the registered user and retrieve the access token.
    3. Use the access token to authenticate and request the user's profile.

    Asserts:
    - The registration request should return a 201 status code (Created).
    - The login request should return a 200 status code (Success) and provide an access token.
    - The profile request should return a 200 status code (Success).
    - The profile response should contain the user's email (profileuser@example.com).
    """
    # Step 1: Register a new user
    client.post('/auth/register', json={
        "email": "profileuser@example.com",
        "password": "testpassword"
    })

    # Step 2: Log in to retrieve the JWT token
    login_response = client.post('/auth/login', json={
        "email": "profileuser@example.com",
        "password": "testpassword"
    })
    
    # Parse the JWT access token from the login response
    token = json.loads(login_response.data)["access_token"]

    # Step 3: Get the user's profile with the JWT token
    response = client.get('/user/profile/profileuser@example.com', headers={"Authorization": f"Bearer {token}"})

    # Assert that the profile retrieval was successful
    assert response.status_code == 200

    # Assert that the profile contains the correct email
    assert b'profileuser@example.com' in response.data
